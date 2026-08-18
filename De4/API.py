"""
Giao tiếp với Shopee API qua Selenium
— dùng browser thật để tránh anti-bot
"""

import time
import random
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from Cfg import BASE_URL, PAGE_SIZE, DELAY, TIME_LIMIT_PER_CAT


def make_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--headless=new")          # chạy ngầm, không hiện cửa sổ
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )


def fetch_json(driver: webdriver.Chrome, url: str) -> dict:
    """Dùng browser fetch URL → parse JSON từ body"""
    driver.get(url)
    time.sleep(random.uniform(*DELAY))
    body = driver.find_element("tag name", "body").text
    return json.loads(body)


def fetch_categories(driver: webdriver.Chrome) -> list[dict]:
    url  = f"{BASE_URL}/api/v4/pages/get_category_tree"
    data = fetch_json(driver, url)
    cats = data["data"]["category_list"]
    return [c for c in cats if c.get("parent_catid") == 0]


def shopee_price(raw: int) -> float:
    return raw / 100_000 if raw else 0.0


def make_product_url(name: str, item_id: int, shop_id: int) -> str:
    slug = name.replace(" ", "-").replace("&", "").replace("/", "-")
    return f"{BASE_URL}/{slug}-i.{shop_id}.{item_id}"


def crawl_category(driver: webdriver.Chrome, cat: dict) -> list[dict]:
    catid    = cat["catid"]
    catname  = cat["name"]
    rows     = []
    newest   = 0
    deadline = time.monotonic() + TIME_LIMIT_PER_CAT if TIME_LIMIT_PER_CAT else None

    print(f"  ▶ [{catid}] {catname}")

    while True:
        if deadline and time.monotonic() > deadline:
            print(f"    ⏱ {catname}: hết giờ — dừng tại {len(rows)} sản phẩm")
            break

        url = (
            f"{BASE_URL}/api/v4/search/search_items"
            f"?catid={catid}&limit={PAGE_SIZE}&newest={newest}"
            f"&page_type=search&scenario=PAGE_CATEGORY&version=2"
        )

        try:
            data  = fetch_json(driver, url)
            items = data.get("items") or []
        except Exception as e:
            print(f"    ✗ {catname} newest={newest}: {e}")
            break

        if not items:
            break

        for it in items:
            info      = it.get("item_basic") or it
            raw_price = info.get("price") or info.get("price_min") or 0
            hist_sold = info.get("historical_sold") or 0
            price     = shopee_price(raw_price)
            rating    = (info.get("item_rating") or {}).get("rating_star") or 0

            rows.append({
                "product_name":    info.get("name", ""),
                "product_url":     make_product_url(
                                       info.get("name", ""),
                                       info.get("itemid", 0),
                                       info.get("shopid", 0),
                                   ),
                "product_rating":  round(rating, 2),
                "product_price":   price,
                "product_revenue": price * hist_sold,
            })

        newest += PAGE_SIZE
        print(f"    ✓ {catname}: {len(rows)} sản phẩm")

    print(f"  ✅ {catname}: xong ({len(rows)} sản phẩm)")
    return rows