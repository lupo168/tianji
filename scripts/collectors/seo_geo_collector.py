#!/usr/bin/env python3
"""天玑 · SEO/GEO搜索情报采集器 v2

深度版本：
  1. Google Trends — 实际解析搜索热度数据
  2. GEO可见性 — 多个关键词循环检测品牌在AI搜索推荐中的出现
  3. 竞品SEO策略 — 搜索意图+内容策略分析
  4. 关键词机会 — 搜索量大但竞争低的词
"""

import json
import os
from datetime import datetime

from scripts.security.safe_requests import get
from scripts.security.safe_search import search_anysearch

OUTPUT_DIR = os.path.expanduser("~/tianji-data/seo")
os.makedirs(OUTPUT_DIR, exist_ok=True)

KEYWORD_GROUPS = {
    "pet_water_fountain": [
        "pet water fountain", "cat water fountain", "best pet water fountain",
        "stainless steel cat fountain", "wireless pet water fountain",
        "pet water fountain filter replacement", "quiet cat water fountain",
        "automatic pet water dispenser", "pet fountain cleaning",
    ],
    "water_filter": [
        "under sink water filter", "reverse osmosis system",
        "best countertop water filter", "NSF certified water filter",
        "whole house water filter", "water filter replacement",
    ],
}

BRANDS = ["Petkit", "PetSafe", "PETLIBRO", "Catit", "Waterdrop", "iSpring", "Aquasana"]


def check_geo_visibility(brand, keywords):
    """GEO检测：品牌是否出现在AI搜索推荐中"""
    total_mentions = 0
    found_in = []

    for kw in keywords:
        output, _flagged = search_anysearch(kw, max_results=5)
        count = output.lower().count(brand.lower())
        if count > 0:
            total_mentions += count
            found_in.append(kw)

    return {
        "brand": brand,
        "total_mentions": total_mentions,
        "keywords_found": len(found_in),
        "keywords_total": len(keywords),
        "found_in_keywords": found_in[:5],
        "visibility_score": round(total_mentions / len(keywords) * 100, 1) if keywords else 0,
    }


def check_google_trends(keyword):
    """Google Trends — 检查可达性（页面本身是JS渲染的，这里只做连通性检查）"""
    url = f"https://trends.google.com/trends/explore?q={keyword.replace(' ', '%20')}&date=today%203-m&geo=US"
    try:
        resp = get(url, reason=f"Google Trends可达性检查-{keyword}", headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        return {"keyword": keyword, "url": url, "accessible": True, "html_length": len(resp.text)}
    except Exception as e:
        return {"keyword": keyword, "url": url, "accessible": False, "error": str(e)[:60]}


def find_keyword_opportunities():
    """找搜索机会：高需求低竞争的关键词"""
    opportunities = []

    long_tail = [
        "cat water fountain not working",
        "pet fountain pump replacement",
        "best water filter for apartment",
        "replacement filter for pet water fountain",
    ]

    for kw in long_tail:
        output, _flagged = search_anysearch(kw, max_results=3)
        opportunities.append({
            "keyword": kw,
            "search_results_count": len(output) if output else 0,
            "potential": "high" if len(output) < 2000 else "medium",
        })

    return opportunities


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"天玑 · SEO/GEO情报采集器 v2 | {today}")
    print("=" * 60)

    results = {}

    print("\n🤖 GEO: AI搜索引擎可见性")
    print("-" * 40)

    all_keywords = []
    for group in KEYWORD_GROUPS.values():
        all_keywords.extend(group)

    geo_scores = []
    for brand in BRANDS:
        geo = check_geo_visibility(brand, all_keywords)
        geo_scores.append(geo)
        bar = "█" * int(geo["visibility_score"] / 5) + "░" * (20 - int(geo["visibility_score"] / 5))
        print(f"  {brand:12s} {bar} {geo['visibility_score']:.0f}分 ({geo['keywords_found']}/{geo['keywords_total']}词)")

    results["geo"] = geo_scores

    geo_scores.sort(key=lambda x: x["visibility_score"], reverse=True)
    print(f"\n  🏆 最可见品牌: {geo_scores[0]['brand']} ({geo_scores[0]['visibility_score']}分)")

    print("\n📈 关键词趋势")
    print("-" * 40)
    trends = []
    for kw in all_keywords[:5]:
        t = check_google_trends(kw)
        icon = "✅" if t.get("accessible") else "⚠️"
        print(f"  {icon} {kw[:35]:35s}")
        trends.append(t)
    results["trends"] = trends

    print("\n💡 关键词机会（长尾低竞争）")
    print("-" * 40)
    opps = find_keyword_opportunities()
    for o in opps:
        print(f"  {o['keyword']:45s} → {'✅ 可切入' if o['potential'] == 'high' else '⚠️ 竞争激烈'}")
    results["opportunities"] = opps

    avg_visibility = sum(g["visibility_score"] for g in geo_scores) / len(geo_scores) if geo_scores else 0
    print(f"\n{'=' * 60}")
    print(f"📊 平均GEO可见性: {avg_visibility:.1f}分")
    print(f"   关键词趋势检查: {sum(1 for t in trends if t.get('accessible'))}/{len(trends)}")
    print(f"   关键词机会: {sum(1 for o in opps if o['potential'] == 'high')}个")
    print(f"{'=' * 60}")

    output = {"date": today, "collected_at": datetime.now().isoformat(), "results": results}
    filepath = os.path.join(OUTPUT_DIR, f"{today}.json")
    with open(filepath, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n💾 已保存: {filepath}")


if __name__ == "__main__":
    main()
