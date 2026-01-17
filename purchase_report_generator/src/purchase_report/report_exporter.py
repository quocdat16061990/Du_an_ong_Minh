"""Module xuất báo cáo ra Excel"""

import pandas as pd
from datetime import datetime


class ReportExporter:
    """Class xuất báo cáo ra Excel"""
    
    def __init__(self, revenue_df, supplier_df, purchase_orders, output_dir='data/output'):
        self.revenue_df = revenue_df
        self.supplier_df = supplier_df
        self.purchase_orders = purchase_orders
        self.output_dir = output_dir
    
    def create_detail_sheet(self):
        """Tạo sheet chi tiết mua hàng"""
        df = pd.DataFrame(self.purchase_orders)
        df = df.sort_values('Ngày mua')
        df['STT'] = range(1, len(df) + 1)
        return df[['STT', 'Mã HH', 'Tên HH', 'Mã NCC', 'tên NCC', 
                  'Ngày mua', 'DVT', 'SL mua', 'Don gia mua', 'Thanhtienmua']]
    
    def create_reconciliation_sheet(self):
        """Tạo sheet đối chiếu"""
        purchase_df = pd.DataFrame(self.purchase_orders)
        data = []
        for _, row in self.supplier_df.iterrows():
            ma_ncc = row['Mã NCC']
            actual_value = purchase_df[purchase_df['Mã NCC'] == ma_ncc]['Thanhtienmua'].sum()
            data.append({
                'Mã NCC': ma_ncc,
                'Tên NCC': row['Tên NCC'],
                'Tổng giá trị mua': actual_value,
                'đối chiếu với tổng giá trị mua': abs(float(row['Tổng giá trị mua']))
            })
        return pd.DataFrame(data)
    
    def create_inventory_sheet(self):
        """Tạo sheet tồn kho"""
        purchase_df = pd.DataFrame(self.purchase_orders)
        products = self.revenue_df['Mã HH'].unique()
        data = []
        
        initial_inventory = {}
        for ma_hh in products:
            product_rows = self.revenue_df[self.revenue_df['Mã HH'] == ma_hh]
            initial_inventory[ma_hh] = product_rows.iloc[0]['SL tồn'] if len(product_rows) > 0 else 0
        
        for idx, ma_hh in enumerate(products, 1):
            product_rows = self.revenue_df[self.revenue_df['Mã HH'] == ma_hh]
            product_info = product_rows.iloc[0] if len(product_rows) > 0 else None
            
            sl_nhap = purchase_df[purchase_df['Mã HH'] == ma_hh]['SL mua'].sum()
            gia_tri_nhap = purchase_df[purchase_df['Mã HH'] == ma_hh]['Thanhtienmua'].sum()
            sl_xuat = self.revenue_df[self.revenue_df['Mã HH'] == ma_hh]['SL bán'].sum()
            gia_von_xuat_ban = (gia_tri_nhap / sl_nhap * sl_xuat) if sl_nhap > 0 else 0
            sl_ton = initial_inventory[ma_hh] + sl_nhap - sl_xuat
            gia_tri_ton = sl_ton * (gia_tri_nhap / sl_nhap) if sl_nhap > 0 else 0
            
            data.append({
                'STT': idx,
                'Mã HH': ma_hh,
                'Tên HH': product_info['Tên HH'] if product_info is not None else 'Unknown',
                'DVT': product_info['dvt'] if product_info is not None else 'cai',
                'SL nhap': sl_nhap,
                'Gia tri nhap': gia_tri_nhap,
                'SL xuất': sl_xuat,
                'Giá vốn xuất bán': gia_von_xuat_ban,
                'SL tồn': sl_ton,
                'Giá trị tồn': gia_tri_ton
            })
        
        return pd.DataFrame(data)
    
    def export(self, filename=None):
        """Xuất file Excel"""
        import os
        os.makedirs(self.output_dir, exist_ok=True)
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"Bao_cao_muahang_{timestamp}.xlsx"
        
        filepath = os.path.join(self.output_dir, filename)
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            self.create_detail_sheet().to_excel(writer, sheet_name='ChiTietmuahang', index=False)
            self.create_reconciliation_sheet().to_excel(writer, sheet_name='Đối chieu', index=False)
            self.create_inventory_sheet().to_excel(writer, sheet_name='File xuat nhap ton', index=False)
        
        return filepath

