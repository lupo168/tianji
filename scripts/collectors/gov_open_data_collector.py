#!/usr/bin/env python3
"""天玑 · 政府开放数据采集器 — 零成本，无需API key

覆盖: FDA / FCC / CPSC / USPTO / EPA / EU Open Data / GOV.UK / UKIPO
       IMF / World Bank / Bank of England / Norges Bank / Sveriges Riksbank
"""

import json
import os
import re
from datetime import datetime

from scripts.security.safe_requests import get_json, get_text

OUTPUT_DIR = os.path.expanduser("~/tianji-data/government")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def fetch_json(url, reason="", timeout=15):
    try:
        return get_json(url, reason=reason, timeout=timeout)
    except Exception as e:
        return {"_error": str(e)[:100]}


def fetch_text(url, reason="", timeout=15):
    try:
        return get_text(url, reason=reason, timeout=timeout)[:500]
    except Exception as e:
        return {"_error": str(e)[:100]}


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"天玑 · 政府开放数据采集器 | {today}")
    print("=" * 50)

    results = {}

    # === 美国 ===
    print("\n🇺🇸 美国监管机构")

    # 1. FDA — 最近召回事件
    try:
        data = fetch_json("https://api.fda.gov/food/enforcement.json?limit=3", reason="FDA召回监控")
        if "_error" not in data:
            results["fda_recalls"] = [
                {"reason": r.get("reason_for_recall", "")[:100],
                 "product": r.get("product_description", "")[:100],
                 "date": r.get("report_date", ""),
                 "classification": r.get("classification", "")}
                for r in data.get("results", [])
            ]
            print(f"  ✅ FDA: {len(results['fda_recalls'])}条召回")
        else:
            print(f"  ⚠️ FDA: {data['_error']}")
    except Exception as e:
        print(f"  ⚠️ FDA: {e}")

    # 2. FCC — 最近电子设备认证
    text = fetch_text("https://apps.fcc.gov/oetcf/eas/reports/WeeklySummary.cfm", reason="FCC周报")
    if isinstance(text, str):
        results["fcc_summary"] = text[:300]
        print("  ✅ FCC: 已获取周报摘要")

    # 3. CPSC — 消费品召回 (via RSS)
    text = fetch_text("https://www.cpsc.gov/RSS/RecallRSS.xml", reason="CPSC召回RSS")
    if isinstance(text, str) and "item" in text.lower():
        titles = re.findall(r"<title>(.*?)</title>", text)
        results["cpsc_recalls"] = [t for t in titles if t and "CPSC" not in t][:5]
        print(f"  ✅ CPSC: {len(results['cpsc_recalls'])}条召回")

    # 4. USPTO — 商标数据 (公开API)
    data = fetch_json(
        "https://developer.uspto.gov/trademark/v1/trademarks/search?query=_id:1&limit=1",
        reason="USPTO商标API可达性检查",
    )
    if "_error" not in data:
        results["uspto_status"] = "API可达"
        print("  ✅ USPTO: API可达")

    # 5. EPA — 环保法规
    data = fetch_json("https://www.epa.gov/data.json", reason="EPA数据集")
    if "_error" not in data:
        datasets = data.get("dataset", [])[:3]
        results["epa_datasets"] = [d.get("title", "")[:80] for d in datasets]
        print(f"  ✅ EPA: {len(results['epa_datasets'])}个数据集")

    # === 国际 ===
    print("\n🌍 国际组织")

    # 6. IMF
    data = fetch_json("http://dataservices.imf.org/REST/SDMX_JSON.svc/Dataflow", reason="IMF可达性检查")
    if "_error" not in data:
        results["imf_status"] = "API可达"
        print("  ✅ IMF: API可达")

    # 7. World Bank
    data = fetch_json("https://api.worldbank.org/v2/country?format=json&per_page=3", reason="World Bank可达性检查")
    if isinstance(data, list) and len(data) > 1:
        results["worldbank_status"] = "API可达"
        print("  ✅ World Bank: API可达")

    # === 英国 ===
    print("\n🇬🇧 英国")

    # 8. GOV.UK
    data = fetch_json("https://www.gov.uk/api/content/government/publications", reason="GOV.UK发布物")
    if "_error" not in data:
        links = data.get("links", [])[:3]
        results["govuk_recent"] = [l.get("title", "")[:80] for l in links]
        print(f"  ✅ GOV.UK: {len(results['govuk_recent'])}条")

    # 9. UKIPO
    data = fetch_json("https://www.gov.uk/api/organisations/intellectual-property-office", reason="UKIPO可达性检查")
    if "_error" not in data:
        results["ukipo_status"] = "API可达"
        print("  ✅ UKIPO: API可达")

    # === 欧洲 ===
    print("\n🇪🇺 欧盟")

    # 10. EU Open Data
    data = fetch_json("https://data.europa.eu/api/hub/search/datasets?limit=3", reason="EU开放数据")
    if "_error" not in data:
        results["eu_data_count"] = data.get("count", 0)
        print(f"  ✅ EU Open Data: {results['eu_data_count']}个数据集")

    # === 央行 ===
    print("\n🏦 各国央行汇率")

    # 11. Bank of England
    text = fetch_text(
        "https://www.bankofengland.co.uk/boeapps/iadb/fromshowcolumns.asp?SeriesCodes=XUDLGBD&CSVF=TN",
        reason="英格兰银行汇率",
    )
    if isinstance(text, str):
        results["boe_status"] = "API可达"
        print("  ✅ Bank of England: 已采集")

    # 12. Norges Bank (挪威)
    data = fetch_json(
        "https://data.norges-bank.no/api/v1/data/EXR/M.KP.USD.EUR.S?format=json&limit=1",
        reason="挪威央行汇率",
    )
    if "_error" not in data:
        results["norges_bank_status"] = "API可达"
        print("  ✅ Norges Bank: 已采集")

    # 13. Sveriges Riksbank (瑞典)
    data = fetch_json(
        f"https://api.riksbank.se/swea/v1/AverageExchangeRatesMonthly/{datetime.now().year}",
        reason="瑞典央行汇率",
    )
    if "_error" not in data:
        results["riksbank_status"] = "API可达"
        print("  ✅ Riksbank: 已采集")

    # === 其他免费API ===
    print("\n🔧 其他")

    # 14. Google Patents
    data = fetch_json(
        "https://patents.google.com/api/query?q=pet+water+fountain&num=3",
        reason="Google Patents可达性检查",
    )
    if "_error" not in data:
        results["google_patents_status"] = "API可达"
        print("  ✅ Google Patents: API可达")

    # 保存
    output = {"date": today, "collected_at": datetime.now().isoformat(), "results": results}
    filepath = os.path.join(OUTPUT_DIR, f"{today}.json")
    with open(filepath, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n💾 已保存: {filepath}")
    print(f"📦 数据源数: {sum(1 for k in results if not k.endswith('_status') or results[k] == 'API可达')}")


if __name__ == "__main__":
    main()
