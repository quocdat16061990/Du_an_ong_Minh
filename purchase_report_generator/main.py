"""Entry point chính của ứng dụng"""

import sys
import io
import os
import warnings
from pathlib import Path
warnings.filterwarnings('ignore')

# Fix encoding for Windows console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    except:
        pass

from src.purchase_report import PurchaseReportGenerator


def main():
    """Hàm chính"""
    print("=" * 60)
    print("CHUONG TRINH TAO BAO CAO MUA HANG")
    print("=" * 60)
    
    try:
        # Lấy đường dẫn root (thư mục cha của purchase_report_generator)
        base_dir = Path(__file__).parent.parent
        input_dir = str(base_dir / 'INPUT')
        output_dir = str(base_dir / 'OUTPUT')
        
        generator = PurchaseReportGenerator(input_dir=input_dir, output_dir=output_dir)
        generator.load_data()
        filename = generator.generate_report()
        
        print("=" * 60)
        print("HOAN THANH!")
        print(f"File output: {filename}")
        print("=" * 60)
        
    except Exception as e:
        print(f"LOI: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

