#!/usr/bin/env python3
"""天玑 · 竞品定价监控

修复记录 (2026-07-18, A3审计项):
  旧版逻辑：re.findall抓搜索结果文本里第一个 $数字，直接当作产品价格存下来。
  问题：搜索片段里可能先出现运费/配件价/无关产品价，"取第一个"没有任何校验，
        产出的数字看起来很确定，实际上不可信。

  本次修复不是接入付费的Amazon/官网结构化API（那是C1项，需要JUN决定是否付费），
  而是让现有的免费搜索方案变得"诚实"：
    1. 不再只取第一个匹配，而是收集全部候选价格
    2. 用价格是否落在"上次记录价格的±40%区间"做基础异常检测，
       超出区间的标记为 low_confidence，需要人工复核
    3. 无历史价格可比对时（首次运行），只要出现1个候选价直接标 medium_confidence，
       出现≥2个候选价（说明搜索结果里价格信息不唯一）标 low_confidence
    4. 保留匹配到的原始文本片段（snippet_context），方便人工核实数字到底是不是产品价
    5. 历史价格存档在同一个JSON里，供下次运行时做环比校验

  仍然依赖外部路径 ~/.hermes/skills/anysearch/scripts/anysearch_cli.py（A5待修）。
  这个修复只解决"数据可信度"问题，不解决"外部依赖是否存在"的问题。
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime

OUTPUT_DIR = os.path.expanduser("~/tianji-data/pricing")
os.makedirs(OUTPUT_DIR, exist_ok=True)

PRODUCTS = [
    ("Petkit", "Eversweet Solo SE"),
    ("PETLIBRO", "Dockstream"),
    ("Waterdrop", "10UA filter"),
    ("iSpring", "RCC7AK"),
]
AS = os.path.expanduser("~/.hermes/skills/anysearch/scripts/anysearch_cli.py")

# 环比异常检测阈值：新价格与上次记录价格偏离超过这个比例，标记为需要人工复核
DEVIATION_THRESHOLD = 0.40


def _load_last_known_prices():
    """从历史JSON里找最近一次每个产品的可信价格，用于环比校验"""
    last_prices = {}
    if not os.path.isdir(OUTPUT_DIR):
        return last_prices
    files = sorted(f for f in os.listdir(OUTPUT_DIR) if f.endswith(".json"))
    for fname in reversed(files):  # 从最新的文件往回找
        try:
            with open(os.path.join(OUTPUT_DIR, fname)) as f:
                data = json.load(f)
        except Exception:
            continue
        for item in data.get("data", []):
            key = (item.get("brand"), item.get("product"))
            if key in last_prices:
                continue
            price = item.get("price")
            confidence = item.get("confidence", "unknown")
            if price not in (None, "?", "err") and confidence in ("high", "medium"):
                try:
                    last_prices[key] = float(price)
                except (TypeError, ValueError):
                    continue
        if len(last_prices) == len(PRODUCTS):
            break
    return last_prices


def _extract_price_candidates(text, window=25):
    """抓取所有 $数字 候选，附带前后文片段方便人工核实"""
    candidates = []
    for m in re.finditer(r"\$(\d+(?:\.\d{1,2})?)", text):
        price = m.group(1)
        start = max(0, m.start() - window)
        end = min(len(text), m.end() + window)
        snippet = text[start:end].replace("\n", " ").strip()
        candidates.append({"price": price, "snippet_context": snippet})
    return candidates


def check_one(brand, product, last_known_price):
    try:
        r = subprocess.run(
            [sys.executable, AS, "search", f"{brand} {product} price 2026", "--max_results", "2"],
            capture_output=True, text=True, timeout=20,
        )
    except Exception as e:
        return {"brand": brand, "product": product, "price": "err", "confidence": "none",
                "reason": f"subprocess_error: {e}"}

    candidates = _extract_price_candidates(r.stdout)
    if not candidates:
        return {"brand": brand, "product": product, "price": "?", "confidence": "none",
                "reason": "no_dollar_amount_found", "candidates": []}

    chosen = candidates[0]
    price_value = float(chosen["price"])

    if len(candidates) > 1:
        confidence = "low"
        reason = f"multiple_price_candidates_found({len(candidates)})"
    elif last_known_price is not None:
        deviation = abs(price_value - last_known_price) / last_known_price
        if deviation > DEVIATION_THRESHOLD:
            confidence = "low"
            reason = f"deviation_{deviation:.0%}_from_last_known_{last_known_price}"
        else:
            confidence = "high"
            reason = f"within_{DEVIATION_THRESHOLD:.0%}_of_last_known_price"
    else:
        confidence = "medium"
        reason = "single_candidate_no_history_to_compare"

    return {
        "brand": brand, "product": product, "price": chosen["price"],
        "confidence": confidence, "reason": reason,
        "snippet_context": chosen["snippet_context"],
        "candidates": candidates,
    }


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"天玑 · 竞品定价 | {today}")
    last_known = _load_last_known_prices()

    results = []
    for brand, product in PRODUCTS:
        item = check_one(brand, product, last_known.get((brand, product)))
        icon = {"high": "✅", "medium": "🟡", "low": "⚠️", "none": "⚪"}.get(item["confidence"], "⚪")
        print(f"  {icon} {brand} {product}: ${item['price']} [{item['confidence']}] {item.get('reason', '')}")
        results.append(item)

    low_confidence_count = sum(1 for r in results if r["confidence"] in ("low", "none"))
    if low_confidence_count:
        print(f"\n  ⚠️ {low_confidence_count}/{len(results)} 条数据置信度低，建议人工复核后再用于决策")

    json.dump(
        {"date": today, "deviation_threshold": DEVIATION_THRESHOLD, "data": results},
        open(os.path.join(OUTPUT_DIR, f"{today}.json"), "w"),
        indent=2, ensure_ascii=False,
    )
    print(f"  💾 saved")


if __name__ == "__main__":
    main()
