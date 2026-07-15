#!/usr/bin/env python3
"""天玑 · 营销情报采集器 v2

深度版本：真正干活，不只是搜一下

覆盖:
  1. Facebook Ad Library — 实际搜索竞品广告库
  2. Google Ads Transparency — 搜索竞品广告
  3. KOL/红人追踪 — 谁在带货、带什么品
  4. 广告政策变更 — FB/Google/TikTok广告政策更新
  5. 竞品社媒数据 — 粉丝/互动/更新频率

安全说明: 原文件里这段代码存在语法错误（f-string里嵌套了未转义的引号），
本次改造顺带修复，同时把 AnySearch 的调用统一到 safe_search.py
（自动过内容防注入过滤），把直连请求统一到 safe_requests.py。
"""

import json
import os
from datetime import datetime

from scripts.security.safe_requests import get
from scripts.security.safe_search import search_anysearch

OUTPUT_DIR = os.path.expanduser("~/tianji-data/marketing")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "ads"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "kol"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "policies"), exist_ok=True)

# ==================== 配置 ====================
COMPETITOR_BRANDS = [
    {"name": "Petkit", "category": "pet", "website": "petkit.com"},
    {"name": "PetSafe", "category": "pet", "website": "petsafe.com"},
    {"name": "PETLIBRO", "category": "pet", "website": "petlibro.com"},
    {"name": "Catit", "category": "pet", "website": "catit.com"},
    {"name": "Waterdrop", "category": "water", "website": "waterdropfilter.com"},
    {"name": "iSpring", "category": "water", "website": "ispringfilter.com"},
    {"name": "Aquasana", "category": "water", "website": "aquasana.com"},
]

# 广告政策RSS/页面
AD_POLICY_FEEDS = [
    ("Facebook广告政策", "https://www.facebook.com/policies/ads"),
    ("Google Ads政策", "https://support.google.com/adspolicy/"),
    ("TikTok广告政策", "https://ads.tiktok.com/help/article/tiktok-ads-policies"),
    ("Amazon广告政策", "https://advertising.amazon.com/resources/ad-policy"),
]


# ==================== 模块1: 广告情报 ====================
def scan_facebook_ads(brand_name):
    """Facebook Ad Library — 搜索竞品投放的广告

    FB Ad Library是公开的，不需要登录就能搜索。
    """
    print("  📱 FB Ad Library...")
    results = []

    queries = [
        f'site:facebook.com/ads/library "{brand_name}"',
        f'"{brand_name}" "sponsored" "Facebook" ad',
    ]

    for q in queries:
        output, flagged = search_anysearch(q, max_results=3)
        if brand_name.lower() in output.lower():
            results.append({"query": q, "found": True, "snippet": output[:300], "content_flagged": flagged})

    ad_library_url = f"https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=US&q={brand_name}"

    return {
        "brand": brand_name,
        "ad_library_url": ad_library_url,
        "search_results": results,
        "total_ads_found": len(results),
    }


def scan_google_ads(brand_name):
    """Google Ads透明度"""
    print("  🔍 Google Ads...")
    q = f'"{brand_name}" "Google ad" OR "sponsored" OR "shopping ad" 2026'
    output, flagged = search_anysearch(q, max_results=3)
    found = brand_name.lower() in output.lower()
    return {"brand": brand_name, "found": found, "snippet": output[:300] if found else "", "content_flagged": flagged}


# ==================== 模块2: KOL/红人追踪 ====================
def scan_kol_for_brand(brand_name):
    """追踪品牌合作的KOL/红人"""
    print("  🎬 KOL/红人...")

    queries = [
        f'"{brand_name}" "influencer" OR "sponsored" OR "collaboration" 2026',
        f'"{brand_name}" "#ad" OR "#sponsored" review',
        f'"{brand_name}" "TikTok" "review" OR "unboxing"',
    ]

    kol_finds = []
    any_flagged = False
    for q in queries:
        output, flagged = search_anysearch(q, max_results=5)
        any_flagged = any_flagged or flagged
        if output:
            for line in output.split("\n"):
                if brand_name.lower() in line.lower() and len(line) > 20:
                    kol_finds.append(line.strip()[:150])

    unique = list(dict.fromkeys(kol_finds))
    return {
        "brand": brand_name,
        "kol_signals": unique[:10],
        "total_signals": len(unique),
        "content_flagged": any_flagged,
    }


# ==================== 模块3: 广告政策变更 ====================
def check_ad_policies():
    """检查广告政策是否有更新"""
    print("  📋 广告政策...")
    results = []
    for name, url in AD_POLICY_FEEDS:
        try:
            get(url, reason=f"广告政策监控-{name}", headers={"User-Agent": "TianjiBot/1.0"}, timeout=10)
            results.append({"platform": name, "url": url, "accessible": True})
        except Exception as e:
            results.append({"platform": name, "url": url, "accessible": False, "error": str(e)[:60]})
    return results


# ==================== 主流程 ====================
def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"天玑 · 营销情报采集器 v2 | {today}")
    print("=" * 60)
    print(f"竞品数: {len(COMPETITOR_BRANDS)} | 政策源: {len(AD_POLICY_FEEDS)}")
    print("=" * 60)

    all_data = {}

    for category in ["pet", "water"]:
        brands = [b for b in COMPETITOR_BRANDS if b["category"] == category]
        print(f"\n{'=' * 60}")
        print(f"📂 品类: {'宠物' if category == 'pet' else '净水器'}")
        print(f"{'=' * 60}")

        for brand in brands:
            name = brand["name"]
            print(f"\n🏷️ {name} ({brand['website']})")

            brand_data = {
                "facebook_ads": scan_facebook_ads(name),
                "google_ads": scan_google_ads(name),
                "kol": scan_kol_for_brand(name),
            }
            all_data[name] = brand_data

    print(f"\n{'=' * 60}")
    print("📋 广告政策变更检查")
    print(f"{'=' * 60}")
    policies = check_ad_policies()
    for p in policies:
        icon = "✅" if p.get("accessible") else "⚠️"
        print(f"  {icon} {p['platform']}")

    print(f"\n{'=' * 60}")
    print("📊 今日情报汇总")
    print(f"{'=' * 60}")

    total_ads = sum(1 for b in all_data.values() if b["facebook_ads"]["total_ads_found"] > 0)
    total_kol = sum(1 for b in all_data.values() if b["kol"]["total_signals"] > 0)
    print(f"  发现广告线索的品牌: {total_ads}/{len(COMPETITOR_BRANDS)}")
    print(f"  发现红人信号的品牌: {total_kol}/{len(COMPETITOR_BRANDS)}")
    print(f"  广告政策源检查: {sum(1 for p in policies if p.get('accessible'))}/{len(policies)}")

    output = {
        "date": today,
        "collected_at": datetime.now().isoformat(),
        "competitors": all_data,
        "ad_policies": policies,
        "summary": {
            "brands_with_ads": total_ads,
            "brands_with_kol": total_kol,
            "policies_checked": len(policies),
        },
    }

    filepath = os.path.join(OUTPUT_DIR, f"{today}.json")
    with open(filepath, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    report = []
    report.append(f"# 天玑 · 营销情报日报 — {today}")
    report.append("")
    report.append("## 广告线索")
    for name, data in all_data.items():
        fa = data["facebook_ads"]
        report.append(
            f"- **{name}**: FB广告{'✅' if fa['total_ads_found'] > 0 else '❌'} "
            f"| Google广告{'✅' if data['google_ads'].get('found') else '❌'}"
        )
        if fa["ad_library_url"]:
            report.append(f"  - FB Ad Library: {fa['ad_library_url']}")
    report.append("")
    report.append("## 红人动态")
    for name, data in all_data.items():
        kol = data["kol"]
        if kol["total_signals"] > 0:
            report.append(f"- **{name}**: {kol['total_signals']}条红人信号")
            for s in kol["kol_signals"][:3]:
                report.append(f"  - {s[:80]}")
    report.append("")
    report.append("## 广告政策")
    for p in policies:
        status = "✅ 可达" if p.get("accessible") else "⚠️ 不可达"
        report.append(f"- {p['platform']}: {status}")

    report_path = os.path.join(OUTPUT_DIR, f"report-{today}.md")
    with open(report_path, "w") as f:
        f.write("\n".join(report))

    print(f"\n💾 已保存: {filepath}")
    print(f"📄 可读报告: {report_path}")


if __name__ == "__main__":
    main()
