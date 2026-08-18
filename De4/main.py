"""
Shopee Crawler — entry point (Selenium version)

Chạy:
    uv add selenium webdriver-manager openpyxl
    python main.py

Output:
    output/
    ├── men_clothes.csv / .xlsx
    ├── women_clothes.csv / .xlsx
    └── ...
"""

from API      import make_driver, fetch_categories, crawl_category
from Exporter import export_category


def main():
    print("🚀 Khởi động browser...")
    driver = make_driver()

    try:
        # Vào trang chủ trước để lấy cookie tự nhiên
        driver.get("https://shopee.vn")
        import time; time.sleep(3)

        print("\n📦 Đang lấy danh sách categories...")
        categories = fetch_categories(driver)
        print(f"   Tìm thấy {len(categories)} categories\n")

        for cat in categories:
            rows = crawl_category(driver, cat)
            if rows:
                export_category(cat["name"], rows)
            else:
                print(f"  ⚠️  No products found for category: {cat['name']}")

    finally:
        driver.quit()
        print("\n✅ Hoàn tất!")


if __name__ == "__main__":
    main()