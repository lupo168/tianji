#!/usr/bin/env python3
"""天玑 · 大宗商品参考价采集器 — 零成本

数据源: 公开免费的商品价格
"""

import json
import os
from datetime import datetime

from scripts.security.safe_requests import get_json

OUTPUT_DIR = os.path.expanduser("~/tianji-data/commodities")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"天玑 · 大宗商品参考价采集器 | {today}")
    print("=" * 40)

    results = {}

    # 黄金价格 (免费公开API)
    try:
        data = get_json(
            "https://api.nbp.pl/api/cenyzlota/last/1",
            reason="每日大宗商品采集-黄金价格",
        )
        results["gold_price"] = data[0] if data else "N/A"
        print("✅ 黄金价格: 已采集")
    except Exception as e:
        print(f"⚠️ 黄金: {str(e)[:60]}")

    print("\n⏳ 更多商品价格需要专用API key")
    print("   (原油/塑料期货等需要专业数据源)")

    output = {"date": today, "collected_at": datetime.now().isoformat(), "data": results}
    filepath = os.path.join(OUTPUT_DIR, f"{today}.json")
    with open(filepath, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n💾 已保存: {filepath}")


if __name__ == "__main__":
    main()
