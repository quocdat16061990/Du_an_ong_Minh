# Purchase Report Generator

Hệ thống tạo báo cáo mua hàng tự động từ dữ liệu doanh thu và nhà cung cấp.

## Cấu trúc Project

```
purchase_report_generator/
├── src/
│   └── purchase_report/
│       ├── __init__.py
│       ├── data_loader.py          # Đọc và chuẩn hóa dữ liệu
│       ├── price_calculator.py     # Tính toán giá mua
│       ├── inventory_manager.py    # Quản lý tồn kho
│       ├── purchase_order_generator.py  # Tạo phiếu mua
│       ├── report_exporter.py     # Xuất báo cáo Excel
│       └── main.py                 # Class chính điều phối
├── data/
│   ├── input/                      # Thư mục chứa file input
│   │   ├── Doanh thu 2024.xlsx
│   │   ├── No NCC.xlsx
│   │   └── NCC mua them.xlsx
│   └── output/                     # Thư mục chứa file output
├── tests/                          # Unit tests
├── main.py                         # Entry point
├── requirements.txt                # Dependencies
└── README.md                       # File này
```

## Cài đặt

1. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

2. Đặt các file input vào thư mục `data/input/`:
   - `Doanh thu 2024.xlsx`
   - `No NCC.xlsx`
   - `NCC mua them.xlsx`

## Sử dụng

Chạy script từ thư mục root:
```bash
python main.py
```

File output sẽ được tạo trong thư mục `data/output/` với tên:
`Bao_cao_muahang_YYYYMMDD_HHMMSS.xlsx`

## Tính năng

- ✅ Đọc và chuẩn hóa dữ liệu từ Excel
- ✅ Tính giá mua tự động (86%-88% doanh thu)
- ✅ Tạo 150-250 phiếu mua hàng
- ✅ Đảm bảo không âm kho
- ✅ Phân bổ giá trị mua theo NCC
- ✅ Xử lý trường hợp âm kho tự động
- ✅ Xuất 3 sheet: Chi tiết, Đối chiếu, Tồn kho

## Cấu trúc Code

Project được tổ chức theo mô hình OOP với các module riêng biệt:

- **DataLoader**: Xử lý I/O dữ liệu
- **PriceCalculator**: Tính toán giá mua
- **InventoryManager**: Quản lý tồn kho
- **PurchaseOrderGenerator**: Tạo phiếu mua
- **ReportExporter**: Xuất báo cáo
- **PurchaseReportGenerator**: Điều phối toàn bộ quá trình

## Yêu cầu

- Python 3.8+
- pandas >= 2.0.0
- openpyxl >= 3.1.0
- numpy >= 1.24.0

## Tác giả

Expert Python Developer

