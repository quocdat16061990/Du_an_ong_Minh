"""Module tạo các phiếu mua hàng"""

import random
from datetime import timedelta
from .price_calculator import PriceCalculator


class PurchaseOrderGenerator:
    """Class tạo các phiếu mua hàng"""
    
    def __init__(self, revenue_df, supplier_df, additional_supplier_df, 
                 product_prices, inventory_manager):
        self.revenue_df = revenue_df
        self.supplier_df = supplier_df
        self.additional_supplier_df = additional_supplier_df
        self.product_prices = product_prices
        self.inventory_manager = inventory_manager
        self.purchase_orders = []
        self.used_combinations = set()
        self.product_order_tracker = {}
        self.supplier_targets = self._init_supplier_targets()
        self.additional_suppliers = self._init_additional_suppliers()
    
    def _init_supplier_targets(self):
        """Khởi tạo target giá trị mua cho từng NCC"""
        targets = {}
        for _, row in self.supplier_df.iterrows():
            targets[row['Mã NCC']] = {
                'Tên NCC': row['Tên NCC'],
                'target_value': abs(float(row['Tổng giá trị mua'])),
                'current_value': 0
            }
        return targets
    
    def _init_additional_suppliers(self):
        """Khởi tạo danh sách NCC mua thêm"""
        return {row['Mã NCC']: row['Tên NCC'] 
                for _, row in self.additional_supplier_df.iterrows()}
    
    def _get_product_info(self, ma_hh):
        """Lấy thông tin sản phẩm"""
        product_rows = self.revenue_df[self.revenue_df['Mã HH'] == ma_hh]
        if len(product_rows) > 0:
            row = product_rows.iloc[0]
            return {'Tên HH': row['Tên HH'], 'dvt': row['dvt']}
        return {'Tên HH': 'Unknown', 'dvt': 'cai'}
    
    def _calculate_purchase_quantity(self, ma_hh, purchase_date, purchase_price):
        """Tính số lượng mua dựa trên yêu cầu"""
        current_inv = self.inventory_manager.get_inventory_at_date(
            ma_hh, purchase_date, self.purchase_orders)
        future_sales = self.inventory_manager.get_future_sales(ma_hh, purchase_date)
        min_qty = max(0, future_sales - current_inv)
        
        # Xen kẽ giá trị lớn/nhỏ
        if ma_hh not in self.product_order_tracker:
            self.product_order_tracker[ma_hh] = {'next_large': True}
        
        if self.product_order_tracker[ma_hh]['next_large']:
            target_value = random.uniform(100_000_000, 200_000_000)
            self.product_order_tracker[ma_hh]['next_large'] = False
        else:
            target_value = random.uniform(10_000_000, 50_000_000)
            self.product_order_tracker[ma_hh]['next_large'] = True
        
        sl_mua = max(min_qty, int(target_value / purchase_price))
        actual_value = sl_mua * purchase_price
        
        # Đảm bảo giá trị trong khoảng 10-200 triệu
        if actual_value < 10_000_000:
            sl_mua = int(10_000_000 / purchase_price) + 1
        elif actual_value > 200_000_000:
            sl_mua = int(200_000_000 / purchase_price)
        
        return sl_mua, sl_mua * purchase_price
    
    def _select_supplier(self, actual_value):
        """Chọn NCC phù hợp"""
        available = [(code, info) for code, info in self.supplier_targets.items()
                    if info['current_value'] < info['target_value']]
        
        if not available:
            if self.additional_suppliers:
                ma_ncc = random.choice(list(self.additional_suppliers.keys()))
                return ma_ncc, self.additional_suppliers[ma_ncc]
            else:
                ma_ncc = list(self.supplier_targets.keys())[0]
                return ma_ncc, self.supplier_targets[ma_ncc]['Tên NCC']
        
        ma_ncc, supplier_info = max(available, 
                                   key=lambda x: x[1]['target_value'] - x[1]['current_value'])
        
        remaining = supplier_info['target_value'] - supplier_info['current_value']
        if actual_value > remaining:
            actual_value = remaining
        
        supplier_info['current_value'] += actual_value
        return ma_ncc, supplier_info['Tên NCC'], actual_value
    
    def generate_orders(self, num_orders=None):
        """Tạo các phiếu mua hàng"""
        if num_orders is None:
            num_orders = random.randint(150, 250)
        
        min_date = self.revenue_df['ngày'].min()
        max_date = self.revenue_df['ngày'].max()
        products = self.revenue_df['Mã HH'].unique()
        
        order_count = 0
        while order_count < num_orders:
            days_offset = random.randint(0, (max_date - min_date).days)
            purchase_date = min_date + timedelta(days=days_offset)
            ma_hh = random.choice(products)
            
            base_price = self.product_prices.get(ma_hh, 1000)
            purchase_price = PriceCalculator.get_varied_price(base_price)
            
            sl_mua, actual_value = self._calculate_purchase_quantity(
                ma_hh, purchase_date, purchase_price)
            
            # Kiểm tra combination đã dùng
            combination_key = (ma_hh, round(purchase_price, -2), sl_mua)
            if combination_key in self.used_combinations:
                continue
            self.used_combinations.add(combination_key)
            
            # Chọn NCC
            supplier_result = self._select_supplier(actual_value)
            if len(supplier_result) == 3:
                ma_ncc, ten_ncc, actual_value = supplier_result
            else:
                ma_ncc, ten_ncc = supplier_result
                actual_value = sl_mua * purchase_price
            
            product_info = self._get_product_info(ma_hh)
            
            self.purchase_orders.append({
                'STT': order_count + 1,
                'Mã HH': ma_hh,
                'Tên HH': product_info['Tên HH'],
                'Mã NCC': ma_ncc,
                'tên NCC': ten_ncc,
                'Ngày mua': purchase_date,
                'DVT': product_info['dvt'],
                'SL mua': sl_mua,
                'Don gia mua': purchase_price,
                'Thanhtienmua': actual_value
            })
            order_count += 1
        
        return self.purchase_orders
    
    def handle_negative_inventory(self):
        """Xử lý trường hợp âm kho"""
        negative_dates = self.inventory_manager.check_negative_inventory(self.purchase_orders)
        
        for ma_hh, date, needed_qty in negative_dates:
            base_price = self.product_prices.get(ma_hh, 1000)
            purchase_price = PriceCalculator.get_varied_price(base_price)
            
            sl_mua = needed_qty + random.randint(10, 100)
            actual_value = sl_mua * purchase_price
            
            if actual_value < 10_000_000:
                sl_mua = int(10_000_000 / purchase_price) + 1
            elif actual_value > 200_000_000:
                sl_mua = int(200_000_000 / purchase_price)
            
            actual_value = sl_mua * purchase_price
            
            if self.additional_suppliers:
                ma_ncc = random.choice(list(self.additional_suppliers.keys()))
                ten_ncc = self.additional_suppliers[ma_ncc]
            else:
                ma_ncc = self.supplier_df.iloc[0]['Mã NCC']
                ten_ncc = self.supplier_df.iloc[0]['Tên NCC']
            
            product_info = self._get_product_info(ma_hh)
            
            self.purchase_orders.append({
                'STT': len(self.purchase_orders) + 1,
                'Mã HH': ma_hh,
                'Tên HH': product_info['Tên HH'],
                'Mã NCC': ma_ncc,
                'tên NCC': ten_ncc,
                'Ngày mua': date - timedelta(days=1),
                'DVT': product_info['dvt'],
                'SL mua': sl_mua,
                'Don gia mua': purchase_price,
                'Thanhtienmua': actual_value
            })
    
    def adjust_supplier_values(self):
        """Điều chỉnh giá trị mua để khớp với target"""
        current_values = {}
        for po in self.purchase_orders:
            ma_ncc = po['Mã NCC']
            current_values[ma_ncc] = current_values.get(ma_ncc, 0) + po['Thanhtienmua']
        
        for _, row in self.supplier_df.iterrows():
            ma_ncc = row['Mã NCC']
            target_value = abs(float(row['Tổng giá trị mua']))
            current_value = current_values.get(ma_ncc, 0)
            
            if abs(current_value - target_value) > 100:
                diff = target_value - current_value
                ncc_orders = [i for i, po in enumerate(self.purchase_orders) 
                             if po['Mã NCC'] == ma_ncc]
                
                if ncc_orders:
                    ncc_orders_sorted = sorted(ncc_orders, 
                                              key=lambda i: self.purchase_orders[i]['Thanhtienmua'],
                                              reverse=True)
                    
                    remaining_diff = diff
                    for idx in ncc_orders_sorted:
                        if abs(remaining_diff) < 100:
                            break
                        
                        po = self.purchase_orders[idx]
                        price = po['Don gia mua']
                        
                        if price > 0:
                            qty_adjustment = int(remaining_diff / price)
                            if qty_adjustment != 0:
                                new_qty = max(1, po['SL mua'] + qty_adjustment)
                                new_value = new_qty * price
                                
                                if 10_000_000 <= new_value <= 200_000_000:
                                    po['SL mua'] = new_qty
                                    po['Thanhtienmua'] = new_value
                                    remaining_diff = target_value - sum(
                                        self.purchase_orders[i]['Thanhtienmua'] 
                                        for i in ncc_orders
                                    )

