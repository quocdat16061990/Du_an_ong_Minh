"""Module xử lý việc đọc và chuẩn hóa dữ liệu từ Excel"""

import pandas as pd


class DataLoader:
    """Class xử lý việc đọc và chuẩn hóa dữ liệu từ Excel"""
    
    @staticmethod
    def load_revenue(file_path='Doanh thu 2024.xlsx'):
        """Đọc file doanh thu và chuẩn hóa cột"""
        df = pd.read_excel(file_path)
        df.columns = df.columns.str.strip()
        if len(df.columns) >= 8:
            df = df.rename(columns=dict(zip(df.columns[:8], 
                ['ngày', 'Mã HH', 'Tên HH', 'dvt', 'SL bán', 'SL tồn', 'DonGiaBan', 'ThanhTienBan'])))
        df['ngày'] = pd.to_datetime(df['ngày'])
        return df
    
    @staticmethod
    def load_suppliers(file_path='No NCC.xlsx', sheet='NCC'):
        """Đọc file NCC và chuẩn hóa cột"""
        df = pd.read_excel(file_path, sheet_name=sheet)
        df.columns = df.columns.str.strip()
        if len(df.columns) >= 3:
            df = df.rename(columns=dict(zip(df.columns[:3], 
                ['Mã NCC', 'Tên NCC', 'Tổng giá trị mua'])))
        return df
    
    @staticmethod
    def load_additional_suppliers(file_path='NCC mua them.xlsx', sheet='q'):
        """Đọc file NCC mua thêm và chuẩn hóa cột"""
        df = pd.read_excel(file_path, sheet_name=sheet)
        df.columns = df.columns.str.strip()
        if len(df.columns) >= 2:
            df = df.rename(columns=dict(zip(df.columns[:2], ['Mã NCC', 'Tên NCC'])))
        return df

