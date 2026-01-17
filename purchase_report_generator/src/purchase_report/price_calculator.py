"""Module tính toán giá mua"""

import math
import random
import pandas as pd


class PriceCalculator:
    """Class tính toán giá mua"""
    
    @staticmethod
    def calculate_base_prices(revenue_df):
        """Tính giá mua cơ sở cho từng mã hàng"""
        revenue_df = revenue_df.copy()
        revenue_df['Tháng'] = revenue_df['ngày'].dt.to_period('M')
        monthly_stats = revenue_df.groupby(['Mã HH', 'Tháng']).agg({
            'ThanhTienBan': 'sum', 'SL bán': 'sum'
        }).reset_index()
        
        prices = {}
        for ma_hh in revenue_df['Mã HH'].unique():
            product_data = monthly_stats[monthly_stats['Mã HH'] == ma_hh]
            if len(product_data) > 0:
                total_revenue = product_data['ThanhTienBan'].sum()
                total_sold = product_data['SL bán'].sum()
                if total_sold > 0:
                    factor = random.uniform(0.86, 0.88)
                    base_price = (total_revenue / total_sold) * factor
                    rounded_price = math.ceil(base_price * 100) / 100
                    prices[ma_hh] = round(rounded_price / 100) * 100
                else:
                    prices[ma_hh] = 0
            else:
                prices[ma_hh] = 0
        return prices
    
    @staticmethod
    def get_varied_price(base_price, variation_range=(0.95, 1.05)):
        """Tạo giá mua có biến động"""
        price = base_price * random.uniform(*variation_range)
        return max(100, round(round(price / 100) * 100))

