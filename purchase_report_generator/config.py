"""File cấu hình cho ứng dụng"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Data directories
DATA_DIR = BASE_DIR / 'data'
INPUT_DIR = DATA_DIR / 'input'
OUTPUT_DIR = DATA_DIR / 'output'

# File paths
REVENUE_FILE = INPUT_DIR / 'Doanh thu 2024.xlsx'
SUPPLIER_FILE = INPUT_DIR / 'No NCC.xlsx'
ADDITIONAL_SUPPLIER_FILE = INPUT_DIR / 'NCC mua them.xlsx'

# Sheet names
SUPPLIER_SHEET = 'NCC'
ADDITIONAL_SUPPLIER_SHEET = 'q'

# Purchase order settings
MIN_ORDERS = 150
MAX_ORDERS = 250
MIN_PURCHASE_VALUE = 10_000_000  # 10 triệu VND
MAX_PURCHASE_VALUE = 200_000_000  # 200 triệu VND

# Price calculation settings
MIN_PRICE_FACTOR = 0.86
MAX_PRICE_FACTOR = 0.88
PRICE_VARIATION_RANGE = (0.95, 1.05)

# Create directories if they don't exist
INPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

