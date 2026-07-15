#!/usr/bin/env python3
"""天玑 · 品牌声誉+资本情报采集器

覆盖维度: 品牌声誉 / 舆情 / 融资动态
数据源: Trustpilot, BBB, Crunchbase, TechCrunch, 新闻搜索
费用: 全部免费
"""

import json
import os
from datetime import datetime

from scripts.security.safe_search import search_anysearch

OUTPUT_DIR = os.path.expanduser("~/tianji-data/reputation")
os.makedirs(OUTPUT_DIR, exist_ok=True)

BRANDS = ["Petkit", "PetSafe", "Waterdrop", "iSpring"]

QUERIES = {
    "funding": "{brand} funding investment raised 2026",
    "acquisition": "{brand} acquisition acquired 2026",
    "reputation": "{brand} review complaint rating 2026",
    "partnership": "{brand} partnership collaboration launch 2026",
}


def search_news(brand, topic):
    """搜索品牌相关新闻。统一走 search_anysearch，返回内容已经过防注入过滤。"""
    if topic not in QUERIES:
        return {"status": "error", "message": "unknown topic"}

    query = QUERIES[topic].format(brand=brand)
    output, flagged = search_anysearch(query, max_results=3)
    if not output:
        return {"status": "error", "message": "no results"}

    headlines = []
    for line in output.split("\n"):
        if line.strip().startswith("|") and "http" in line:
            headlines.append(line.strip()[:120])

    return {"status": "ok", "headlines": headlines[:5], "content_flagged": flagged}


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"天玑 · 品牌声誉+资本情报采集器 | {today}")
    print("=" * 50)

    results = {}

    for brand in BRANDS:
        print(f"\n🏷️ {brand}")

        funding = search_news(brand, "funding")
        if funding.get("status") == "ok" and funding["headlines"]:
            print(f"  💰 融资动态: {len(funding['headlines'])}条")

        reputation = search_news(brand, "reputation")
        if reputation.get("status") == "ok" and reputation["headlines"]:
            print(f"  📊 品牌声誉: {len(reputation['headlines'])}条")

        partnership = search_news(brand, "partnership")
        if partnership.get("status") == "ok" and partnership["headlines"]:
            print(f"  🤝 合作动态: {len(partnership['headlines'])}条")

        results[brand] = {
            "funding": funding,
            "reputation": reputation,
            "partnership": partnership,
        }

    if not any(r.get("funding", {}).get("headlines") for r in results.values()):
        print("\n未发现重大资本动态")

    output = {"date": today, "collected_at": datetime.now().isoformat(), "results": results}
    filepath = os.path.join(OUTPUT_DIR, f"{today}.json")
    with open(filepath, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n💾 已保存: {filepath}")


if __name__ == "__main__":
    main()
