#!/usr/bin/env python3
"""天玑 · Hacker News科技趋势采集器 — 零成本，无需API key

数据源: HN Firebase API (免费，无认证)
"""

import json
import os
from datetime import datetime

from scripts.security.safe_requests import get_json

OUTPUT_DIR = os.path.expanduser("~/tianji-data/hackernews")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def fetch_top_stories(limit=20):
    result = {"status": "error", "stories": []}
    try:
        ids = get_json(
            "https://hacker-news.firebaseio.com/v0/topstories.json",
            reason="HN热门文章ID列表",
        )[:limit]

        stories = []
        for sid in ids:
            try:
                item = get_json(
                    f"https://hacker-news.firebaseio.com/v0/item/{sid}.json",
                    reason="HN单篇文章详情",
                    timeout=5,
                )
                stories.append({
                    "title": item.get("title", "")[:120],
                    "url": item.get("url", f"https://news.ycombinator.com/item?id={sid}"),
                    "score": item.get("score", 0),
                    "by": item.get("by", "unknown"),
                    "descendants": item.get("descendants", 0),
                })
            except Exception:
                continue

        result["status"] = "ok"
        result["stories"] = stories
    except Exception as e:
        result["status"] = f"error: {str(e)[:80]}"
    return result


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"天玑 · Hacker News趋势采集器 | {today}")
    print("=" * 40)

    data = fetch_top_stories()

    if data["status"] == "ok":
        print(f"✅ 热门文章: {len(data['stories'])}条")
        for s in data["stories"][:5]:
            print(f"   ├ [{s['score']}票] {s['title'][:60]}")
    else:
        print(f"⚠️ {data['status']}")

    output = {"date": today, "collected_at": datetime.now().isoformat(), "data": data}
    filepath = os.path.join(OUTPUT_DIR, f"{today}.json")
    with open(filepath, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n💾 已保存: {filepath}")


if __name__ == "__main__":
    main()
