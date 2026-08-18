"""
get_cookie.py
Mở Chrome thật, vào Shopee, lấy cookie hợp lệ → lưu vào cookie.txt
Chạy 1 lần trước khi chạy main.py

Yêu cầu:
    uv add selenium webdriver-manager
"""

import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def get_shopee_cookies():
    options = Options()
    # Không dùng headless — cần browser thật để qua anti-bot
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )

    print("Đang mở Shopee...")
    driver.get("https://shopee.vn")

    # Chờ trang load + Shopee gán cookie
    print("Chờ 5 giây để Shopee load cookie...")
    time.sleep(5)

    # Lấy tất cả cookies
    cookies = driver.get_cookies()
    driver.quit()

    # Chuyển sang dạng string "key=value; key=value; ..."
    cookie_str = "; ".join(f"{c['name']}={c['value']}" for c in cookies)

    with open("cookie.txt", "w") as f:
        f.write(cookie_str)

    print(f"✅ Lưu {len(cookies)} cookies vào cookie.txt")
    return cookie_str


if __name__ == "__main__":
    get_shopee_cookies()