"""Module quản lý tồn kho"""

import pandas as pd


class InventoryManager:
    """Class quản lý tồn kho"""
    
    def __init__(self, revenue_df):
        self.revenue_df = revenue_df.sort_values('ngày').copy()
        self.initial_inventory = self._calculate_initial_inventory()
    
    def _calculate_initial_inventory(self):
        """Tính tồn kho ban đầu cho từng mã hàng"""
        inventory = {}
        for ma_hh in self.revenue_df['Mã HH'].unique():
            product_rows = self.revenue_df[self.revenue_df['Mã HH'] == ma_hh]
            inventory[ma_hh] = product_rows.iloc[0]['SL tồn'] if len(product_rows) > 0 else 0
        return inventory
    
    def get_inventory_at_date(self, ma_hh, date, purchase_orders):
        """Tính tồn kho tại một ngày cụ thể"""
        sold = self.revenue_df[
            (self.revenue_df['Mã HH'] == ma_hh) & 
            (self.revenue_df['ngày'] <= date)
        ]['SL bán'].sum()
        
        purchased = sum(po['SL mua'] for po in purchase_orders 
                       if po['Mã HH'] == ma_hh and po['Ngày mua'] <= date)
        
        return self.initial_inventory[ma_hh] + purchased - sold
    
    def get_future_sales(self, ma_hh, date):
        """Tính SL bán từ ngày này đến cuối kỳ"""
        return self.revenue_df[
            (self.revenue_df['Mã HH'] == ma_hh) & 
            (self.revenue_df['ngày'] > date)
        ]['SL bán'].sum()
    
    def check_negative_inventory(self, purchase_orders):
        """Kiểm tra và trả về danh sách các ngày bị âm kho"""
        negative_dates = []
        all_dates = sorted(self.revenue_df['ngày'].unique())
        
        for date in all_dates:
            for ma_hh in self.revenue_df['Mã HH'].unique():
                inventory = self.get_inventory_at_date(ma_hh, date, purchase_orders)
                if inventory < 0:
                    negative_dates.append((ma_hh, date, abs(inventory)))
        return negative_dates

