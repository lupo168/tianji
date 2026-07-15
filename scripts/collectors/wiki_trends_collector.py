#!/usr/bin/env python3
"""天玑 · Wikipedia热门趋势采集器 — 零成本，无需API key

数据源: Wikipedia API (免费，无认证)
"""

import json
import os
from datetime import datetime, timedelta

from scripts.security.safe_requests import get_json

OUTPUT_DIR = os.path.expanduser("~/tianji-data/trends")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def fetch_trending():
    """获取Wikipedia热门文章"""
    result = {}

    try:
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y/%m/%d")
        url = f"https://en.wikipedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia.org/all-access/{yesterday}"
        data = get_json(url, reason="Wikipedia每日热门文章", headers={"User-Agent": "Tianji/1.0"})
        articles = data["items"][0]["articles"][:15]
        result["today_top"] = [
            {"title": a["article"], "views": a["views"]}
            for a in articles
            if not a["article"].startswith("Special:") and not a["article"].startswith("Wikipedia:")
        ][:10]
        result["today_status"] = "ok"
    except Exception as e:
        result["today_status"] = f"error: {str(e)[:80]}"

    try:
        randoms = []
        for _ in range(5):
            page = get_json(
                "https://en.wikipedia.org/api/rest_v1/page/random/summary",
                reason="Wikipedia随机文章",
                headers={"User-Agent": "Tianji/1.0"},
            )
            randoms.append({"title": page.get("title", ""), "extract": page.get("extract", "")[:200]})
        result["random_articles"] = randoms
        result["random_status"] = "ok"
    except Exception as e:
        result["random_status"] = f"error: {str(e)[:80]}"

    return result


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"天玑 · Wikipedia趋势采集器 | {today}")
    print("=" * 40)

    data = fetch_trending()

    if data.get("today_status") == "ok":
        print(f"✅ 今日热门: {len(data['today_top'])}条")
        for a in data["today_top"][:5]:
            print(f"   ├ {a['title'][:50]} ({a['views']}次浏览)")
    else:
        print(f"⚠️ 热门: {data.get('today_status')}")

    output = {"date": today, "collected_at": datetime.now().isoformat(), "data": data}
    filepath = os.path.join(OUTPUT_DIR, f"{today}.json")
    with open(filepath, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n💾 已保存: {filepath}")


if __name__ == "__main__":
    main()
