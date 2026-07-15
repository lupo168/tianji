#!/usr/bin/env python3
"""天玑 · YouTube视频趋势采集器

数据源: YouTube Data API v3
费用: 免费 (10,000配额/日)
接入: 需Google Cloud API key

配置步骤:
  1. 打开 https://console.cloud.google.com/
  2. 创建项目 → 启用 YouTube Data API v3
  3. 创建API密钥
  4. 写进项目根目录的 .env：
     YOUTUBE_API_KEY=你的API密钥
"""

import json
import os
import time
from datetime import datetime

from scripts.security.env_loader import load_env
from scripts.security.safe_requests import get_json

OUTPUT_DIR = os.path.expanduser("~/tianji-data/youtube")
os.makedirs(OUTPUT_DIR, exist_ok=True)

load_env()

SEARCH_QUERIES = [
    "pet water fountain review",
    "pet feeder review",
    "best pet products 2026",
    "product review",
    "unboxing pet supplies",
]


def search_videos(api_key, query, max_results=5):
    url = (
        f"https://www.googleapis.com/youtube/v3/search?part=snippet"
        f"&q={query.replace(' ', '%20')}&maxResults={max_results}&order=date&type=video&key={api_key}"
    )
    try:
        data = get_json(url, reason=f"YouTube搜索-{query}", timeout=10)
        items = []
        for item in data.get("items", []):
            snippet = item.get("snippet", {})
            items.append({
                "title": snippet.get("title", "")[:120],
                "channel": snippet.get("channelTitle", ""),
                "published": snippet.get("publishedAt", "")[:10],
                "description": (snippet.get("description", "") or "")[:200],
                "video_id": item.get("id", {}).get("videoId", ""),
                "url": f"https://youtube.com/watch?v={item.get('id', {}).get('videoId', '')}",
            })
        return {"status": "ok", "items": items}
    except Exception as e:
        return {"status": f"error: {str(e)[:80]}"}


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"天玑 · YouTube趋势采集器 | {today}")
    print("=" * 50)

    api_key = os.getenv("YOUTUBE_API_KEY", "")

    if not api_key:
        print("""
  ⏳ YouTube API 未配置

  要启用YouTube采集器：
    1. 打开 https://console.cloud.google.com/
    2. 创建项目 → 启用 YouTube Data API v3
    3. 创建API密钥
    4. 写进项目根目录的 .env：
       YOUTUBE_API_KEY=你的API密钥
""")
        output = {"date": today, "status": "skipped"}
        with open(os.path.join(OUTPUT_DIR, f"{today}.json"), "w") as f:
            json.dump(output, f, indent=2)
        return

    all_videos = []
    for q in SEARCH_QUERIES:
        result = search_videos(api_key, q)
        if result["status"] == "ok":
            all_videos.extend(result["items"])
            print(f"  ✅ \"{q}\": {len(result['items'])}条")
        else:
            print(f"  ⚠️ \"{q}\": {result['status']}")
        time.sleep(0.3)

    print(f"\n📊 共 {len(all_videos)} 条视频")

    output = {"date": today, "collected_at": datetime.now().isoformat(), "status": "ok", "videos": all_videos}
    filepath = os.path.join(OUTPUT_DIR, f"{today}.json")
    with open(filepath, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n💾 已保存: {filepath}")


if __name__ == "__main__":
    main()
