#!/usr/bin/env python3
"""天玑 · 公司/融资情报

修复记录 (2026-07-18, A4审计项):
  旧版逻辑：判断"是否融资"只看搜索结果文本里是否同时出现品牌名 + "fund"/"raises"
  这两类关键词共现。问题：误判率高——"品牌名...founded in..."会命中"fund"，
  "raises awareness"这种无关短语会命中"raises"，产出的是布尔值(found=True/False)，
  没有任何可供人工复核的依据。

  本次修复：
    1. 关键词共现升级为要求同时出现"金额格式"(如 $12M / $3.5 million / 融资金额)
       + 融资动词，降低"品牌名+泛泛提及fund"这类误判
    2. 不再只输出布尔值，改为输出匹配到的原文片段(evidence_snippet)，
       人工一眼就能判断这条线索是不是真的融资新闻
    3. 增加 signal_strength 分级：strong(金额+动词都命中) / weak(只命中动词，无金额)
       / none(什么都没命中)，取代过去简单的 found=True/False

  仍然依赖外部路径 ~/.hermes/skills/anysearch/scripts/anysearch_cli.py（A5待修），
  仍然不是Crunchbase级别的结构化数据源——这只是把"猜测"变得更可核实，
  真正解决还是要接C类清单里的付费融资数据库。
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime

OUTPUT_DIR = os.path.expanduser("~/tianji-data/companies")
os.makedirs(OUTPUT_DIR, exist_ok=True)

BRANDS = ["Petkit", "PetSafe", "PETLIBRO", "Waterdrop", "iSpring"]
AS = os.path.expanduser("~/.hermes/skills/anysearch/scripts/anysearch_cli.py")

# 融资动词（比旧版的"fund"/"raises"更精确，避免"founded"、"raises awareness"这类噪音）
FUNDING_VERBS = re.compile(
    r"\b(raised|raises|secures?|closes?)\b.{0,30}\b(funding|round|financing|investment)\b"
    r"|\b(series [a-e])\b"
    r"|\b(seed round)\b",
    re.IGNORECASE,
)
# 金额格式：$12M / $3.5 million / $500K 等
AMOUNT_PATTERN = re.compile(r"\$\s?\d+(?:\.\d+)?\s?(?:million|billion|[mkbMKB])\b", re.IGNORECASE)


def _classify_signal(text, brand):
    """返回 (signal_strength, evidence_snippet)"""
    if brand.lower() not in text.lower():
        return "none", None

    verb_match = FUNDING_VERBS.search(text)
    amount_match = AMOUNT_PATTERN.search(text)

    if verb_match and amount_match:
        start = max(0, min(verb_match.start(), amount_match.start()) - 20)
        end = min(len(text), max(verb_match.end(), amount_match.end()) + 20)
        snippet = text[start:end].replace("\n", " ").strip()
        return "strong", snippet
    elif verb_match:
        start = max(0, verb_match.start() - 20)
        end = min(len(text), verb_match.end() + 20)
        snippet = text[start:end].replace("\n", " ").strip()
        return "weak", snippet
    else:
        return "none", None


def check_one(brand):
    try:
        r = subprocess.run(
            [sys.executable, AS, "search", f"{brand} funding raised 2026", "--max_results", "2"],
            capture_output=True, text=True, timeout=20,
        )
    except Exception as e:
        return {"brand": brand, "signal_strength": "none", "error": str(e)}

    signal_strength, snippet = _classify_signal(r.stdout, brand)
    return {
        "brand": brand,
        "signal_strength": signal_strength,  # strong / weak / none
        "evidence_snippet": snippet,
    }


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"天玑 · 公司/融资情报 | {today}")
    results = {}
    for brand in BRANDS:
        item = check_one(brand)
        icon = {"strong": "💰", "weak": "🟡", "none": "⚪"}.get(item["signal_strength"], "⚪")
        print(f"  {icon} {brand}: {item['signal_strength']}"
              + (f" — {item['evidence_snippet']}" if item.get("evidence_snippet") else ""))
        results[brand] = item

    weak_or_strong = [b for b, v in results.items() if v["signal_strength"] != "none"]
    if weak_or_strong:
        print(f"\n  ⚠️ 发现{len(weak_or_strong)}条潜在融资信号，"
              f"weak信号仍需人工核实原文，不要直接当结论用")

    json.dump({"date": today, "results": results}, open(os.path.join(OUTPUT_DIR, f"{today}.json"), "w"),
               indent=2, ensure_ascii=False)
    print(f"  💾 saved")


if __name__ == "__main__":
    main()
