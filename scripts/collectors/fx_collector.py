#!/usr/bin/env python3
"""天玑 · 汇率采集器 — 每日自动运行

数据源:
  - CBR (俄罗斯央行) — USD/RUB, EUR/RUB etc.
  - FRED (美联储) — USD index
  - ExchangeRate-API — 多币种（备用）

输出: JSON格式汇率数据，按天存档

安全说明:
  - 所有网络请求走 scripts/security/safe_requests.py，非白名单域名会被拒绝
  - API key 从环境变量读取（.env 文件），不再硬编码在源代码里
"""

import json
import os
from datetime import datetime

from scripts.security.safe_requests import get

# === 配置 ===
OUTPUT_DIR = os.path.expanduser("~/tianji-data/exchange-rates")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def fetch_cbr():
    """俄罗斯央行汇率 (免费，境外可访问)"""
    url = "https://www.cbr.ru/scripts/XML_daily.asp"
    result = {"cbr_url": url}
    try:
        resp = get(url, reason="每日汇率采集-CBR", headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        result["cbr_xml_daily"] = resp.content.decode("windows-1251")[:500]
        result["cbr_status"] = "ok"
    except Exception as e:
        result["cbr_status"] = f"error: {e}"
    return result


def fetch_fred():
    """美联储经济数据 (免费API)

    key 从环境变量 FRED_API_KEY 读取，需要先在 .env 里配置：
        FRED_API_KEY=你的真实key
    验证 key 是否有效用 scripts/security/verify_key.sh fred，
    不要在这个文件里手动填写或打印 key 的值。
    """
    api_key = os.getenv("FRED_API_KEY")
    result = {}
    if not api_key:
        result["fred_status"] = "skipped: FRED_API_KEY 未配置（见 .env）"
        return result

    series = {"DEXUSEU": "EUR/USD", "DEXJPUS": "JPY/USD"}
    for code, name in series.items():
        try:
            url = (
                f"https://api.stlouisfed.org/fred/series/observations"
                f"?series_id={code}&api_key={api_key}&file_type=json&sort_order=desc&limit=1"
            )
            resp = get(url, reason="每日汇率采集-FRED", timeout=10)
            data = resp.json()
            result[name] = data["observations"][0]["value"]
        except Exception as e:
            result[f"{name}_error"] = str(e)
    result["fred_status"] = "ok"
    return result


def fetch_exchangerate():
    """ExchangeRate-API 备用 (免费1000次/月)

    key 从环境变量 EXCHANGERATE_API_KEY 读取，配置方式同上。
    """
    api_key = os.getenv("EXCHANGERATE_API_KEY")
    result = {}
    if not api_key:
        result["exchangerate_status"] = "skipped: EXCHANGERATE_API_KEY 未配置（见 .env）"
        return result

    base = "USD"
    try:
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base}"
        resp = get(url, reason="每日汇率采集-ExchangeRate", timeout=10)
        data = resp.json()
        for code in ["CNY", "EUR", "GBP", "JPY", "KRW", "SGD", "MXN",
                     "THB", "SAR", "AED", "SEK", "NOK", "MYR", "RUB"]:
            result[f"USD/{code}"] = data["conversion_rates"].get(code, "N/A")
        result["exchangerate_status"] = "ok"
    except Exception as e:
        result["exchangerate_status"] = f"error: {e}"
    return result


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().isoformat()

    print(f"天玑 · 汇率采集器 | {now}")
    print("=" * 40)

    results = {
        "cbr": fetch_cbr(),
        "fred": fetch_fred(),
        "exchangerate": fetch_exchangerate(),
    }

    summary = {"date": today, "collected_at": now, "sources": results}

    if results["cbr"].get("cbr_status") == "ok":
        print("✅ CBR俄罗斯央行: 已采集")
    else:
        print(f"⚠️ CBR: {results['cbr'].get('cbr_status')}")

    if results["fred"]["fred_status"].startswith("skipped"):
        print(f"⏳ FRED: {results['fred']['fred_status']}")
    elif results["fred"]["fred_status"] == "ok":
        print("✅ FRED美联储: 已采集")

    if results["exchangerate"]["exchangerate_status"].startswith("skipped"):
        print(f"⏳ ExchangeRate-API: {results['exchangerate']['exchangerate_status']}")
    elif results["exchangerate"]["exchangerate_status"] == "ok":
        rates = results["exchangerate"]
        print(f"✅ ExchangeRate-API: 已采集")
        print(f"   USD/CNY: {rates.get('USD/CNY', 'N/A')}")
        print(f"   USD/EUR: {rates.get('USD/EUR', 'N/A')}")
        print(f"   USD/GBP: {rates.get('USD/GBP', 'N/A')}")

    filepath = os.path.join(OUTPUT_DIR, f"{today}.json")
    with open(filepath, "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"\n💾 已保存: {filepath}")
    print(f"📦 文件大小: {os.path.getsize(filepath)} bytes")


if __name__ == "__main__":
    main()
