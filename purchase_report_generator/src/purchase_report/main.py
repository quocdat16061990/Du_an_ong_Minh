"""Module chính điều phối toàn bộ quá trình"""

from .data_loader import DataLoader
from .price_calculator import PriceCalculator
from .inventory_manager import InventoryManager
from .purchase_order_generator import PurchaseOrderGenerator
from .report_exporter import ReportExporter


class PurchaseReportGenerator:
    """Class chính điều phối toàn bộ quá trình"""
    
    def __init__(self, input_dir='INPUT', output_dir='OUTPUT'):
        self.revenue_df = None
        self.supplier_df = None
        self.additional_supplier_df = None
        self.purchase_orders = []
        self.input_dir = input_dir
        self.output_dir = output_dir
    
    def load_data(self):
        """Đọc dữ liệu từ các file Excel"""
        import os
        print("Đang đọc dữ liệu từ các file Excel...")
        
        revenue_path = os.path.join(self.input_dir, 'Doanh thu 2024.xlsx')
        supplier_path = os.path.join(self.input_dir, 'No NCC.xlsx')
        additional_supplier_path = os.path.join(self.input_dir, 'NCC mua them.xlsx')
        
        self.revenue_df = DataLoader.load_revenue(revenue_path)
        print(f"✓ Đã đọc {len(self.revenue_df)} dòng từ Doanh thu 2024.xlsx")
        
        self.supplier_df = DataLoader.load_suppliers(supplier_path)
        print(f"✓ Đã đọc {len(self.supplier_df)} NCC từ No NCC.xlsx")
        
        self.additional_supplier_df = DataLoader.load_additional_suppliers(additional_supplier_path)
        print(f"✓ Đã đọc {len(self.additional_supplier_df)} NCC từ NCC mua them.xlsx")
    
    def generate_report(self):
        """Tạo báo cáo mua hàng"""
        # Tính giá mua
        print("Đang tính toán giá mua...")
        product_prices = PriceCalculator.calculate_base_prices(self.revenue_df)
        print(f"✓ Đã tính giá mua cho {len(product_prices)} mã hàng")
        
        # Quản lý tồn kho
        inventory_manager = InventoryManager(self.revenue_df)
        
        # Tạo phiếu mua
        print("Đang tạo các phiếu mua hàng...")
        order_generator = PurchaseOrderGenerator(
            self.revenue_df, self.supplier_df, self.additional_supplier_df,
            product_prices, inventory_manager
        )
        order_generator.generate_orders()
        print(f"✓ Đã tạo {len(order_generator.purchase_orders)} phiếu mua hàng")
        
        # Xử lý âm kho
        print("Đang kiểm tra và xử lý trường hợp âm kho...")
        order_generator.handle_negative_inventory()
        print(f"✓ Đã xử lý âm kho, tổng số phiếu mua: {len(order_generator.purchase_orders)}")
        
        # Điều chỉnh giá trị mua
        print("Đang điều chỉnh giá trị mua theo NCC...")
        order_generator.adjust_supplier_values()
        print("✓ Đã điều chỉnh giá trị mua theo NCC")
        
        self.purchase_orders = order_generator.purchase_orders
        
        # Xuất file
        print("Đang xuất file Excel...")
        exporter = ReportExporter(self.revenue_df, self.supplier_df, self.purchase_orders, self.output_dir)
        filename = exporter.export()
        print(f"✓ Đã xuất file: {filename}")
        
        return filename

