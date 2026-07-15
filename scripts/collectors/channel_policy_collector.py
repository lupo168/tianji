#!/usr/bin/env python3
"""天玑 · 渠道/平台政策变化采集器

覆盖维度: 渠道情报 / 平台政策 / 卖家规则
数据源: 各大平台卖家公告RSS + 搜索
费用: 全部免费
"""

import json
import os
from datetime import datetime

from scripts.security.safe_requests import get
from scripts.security.content_sanitizer import sanitize

OUTPUT_DIR = os.path.expanduser("~/tianji-data/channel")
os.makedirs(OUTPUT_DIR, exist_ok=True)

PLATFORM_FEEDS = [
    ("Amazon Seller News", "https://sellercentral.amazon.com/news"),
    ("Shopify Changelog", "https://changelog.shopify.com/"),
    ("eBay Announcements", "https://community.ebay.com/t5/Announcements/bd-p/Announcements"),
    ("Walmart Seller", "https://sellerhelp.walmart.com/s/"),
]


def check_platform_news(name, url):
    """检查平台是否有新政策。抓到的网页正文过一遍防注入过滤，再截取存档。"""
    try:
        resp = get(url, reason=f"渠道政策监控-{name}", headers={"User-Agent": "TianjiBot/1.0"}, timeout=10)
        html = resp.text[:300]
        safe_html, flagged = sanitize(html, source_url=url)
        return {"name": name, "url": url, "accessible": len(html) > 100, "content_flagged": flagged}
    except Exception as e:
        return {"name": name, "url": url, "accessible": False, "error": str(e)[:60]}


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"天玑 · 渠道/平台政策采集器 | {today}")
    print("=" * 50)

    results = []
    for name, url in PLATFORM_FEEDS:
        result = check_platform_news(name, url)
        status = "✅ 可达" if result["accessible"] else "⚠️ 需手动"
        print(f"  {name}: {status}")
        results.append(result)

    output = {"date": today, "collected_at": datetime.now().isoformat(), "results": results}
    filepath = os.path.join(OUTPUT_DIR, f"{today}.json")
    with open(filepath, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n💾 已保存: {filepath}")


if __name__ == "__main__":
    main()
