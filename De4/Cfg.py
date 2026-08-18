"""
Cấu hình chung cho Shopee crawler
"""

import os

BASE_URL           = "https://shopee.vn"
PAGE_SIZE          = 60          # max mỗi request
MAX_CONCURRENT     = 3           # số request đồng thời
DELAY              = (60, 70)  # random delay (giây) giữa các request
TIME_LIMIT_PER_CAT = None         # giây crawl tối đa mỗi category (None = không giới hạn)
OUTPUT_DIR         = "output"    # thư mục lưu file

# Đọc cookie từ file (chạy get_cookie.py trước)
_cookie_file = "cookie.txt"
_cookie = open(_cookie_file).read().strip() if os.path.exists(_cookie_file) else ""

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Referer": "https://shopee.vn/",
    "X-Requested-With": "XMLHttpRequest",
    "Cookie": _cookie,
}

CSV_FIELDS = [
    "product_name",
    "product_url",
    "product_rating",
    "product_price",
    "product_revenue",
]