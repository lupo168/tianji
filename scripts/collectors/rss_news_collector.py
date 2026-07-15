#!/usr/bin/env python3
"""天玑 · RSS新闻采集器 — 零成本，无需API key

数据源: Google News RSS / 政府RSS / 商业新闻RSS
"""

import json
import os
from datetime import datetime
from xml.etree import ElementTree as ET

from scripts.security.safe_requests import get_text

OUTPUT_DIR = os.path.expanduser("~/tianji-data/news")
os.makedirs(OUTPUT_DIR, exist_ok=True)

RSS_FEEDS = [
    {"name": "Google News - Business", "url": "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en"},
    {"name": "Google News - Technology", "url": "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en"},
    {"name": "Reuters - Business", "url": "https://www.reutersagency.com/feed/"},
    {"name": "BBC - Business", "url": "https://feeds.bbci.co.uk/news/business/rss.xml"},
    {"name": "BBC - Technology", "url": "https://feeds.bbci.co.uk/news/technology/rss.xml"},
    {"name": "BBC - World", "url": "https://feeds.bbci.co.uk/news/world/rss.xml"},
    {"name": "Nikkei Asia", "url": "https://www.nikkei.com/rss/english/"},
    {"name": "FTC News", "url": "https://www.ftc.gov/feeds/press-release.xml"},
    {"name": "CPSC Recalls", "url": "https://www.cpsc.gov/RSS/RecallRSS.xml"},
]


def fetch_rss(name, url, timeout=15):
    result = {"name": name, "url": url, "status": "error", "items": []}
    try:
        text = get_text(url, reason=f"RSS采集-{name}", headers={"User-Agent": "Mozilla/5.0 (compatible; Tianji/1.0)"}, timeout=timeout)

        root = ET.fromstring(text)

        items = []
        for item in root.iter("item"):
            title = item.findtext("title", "")[:120]
            link = item.findtext("link", "")
            pubdate = item.findtext("pubDate", "")
            desc = item.findtext("description", "")[:200]
            items.append({"title": title, "link": link, "date": pubdate, "summary": desc})
            if len(items) >= 5:
                break

        if not items:
            for entry in root.iter("{http://www.w3.org/2005/Atom}entry"):
                title = entry.findtext("{http://www.w3.org/2005/Atom}title", "")[:120]
                link_el = entry.find("{http://www.w3.org/2005/Atom}link")
                link = link_el.get("href", "") if link_el is not None else ""
                pubdate = entry.findtext("{http://www.w3.org/2005/Atom}published", "")[:20]
                items.append({"title": title, "link": link, "date": pubdate})
                if len(items) >= 5:
                    break

        result["status"] = "ok"
        result["items"] = items
        result["count"] = len(items)
    except Exception as e:
        result["status"] = f"error: {str(e)[:80]}"
    return result


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"天玑 · RSS新闻采集器 | {today}")
    print("=" * 40)

    results = []
    for feed in RSS_FEEDS:
        result = fetch_rss(feed["name"], feed["url"])
        results.append(result)
        if result["status"] == "ok":
            print(f"✅ {feed['name']}: {result['count']}条")
            for item in result["items"][:2]:
                print(f"   ├ {item['title'][:60]}")
        else:
            print(f"⚠️ {feed['name']}: {result['status']}")

    output = {
        "date": today,
        "collected_at": datetime.now().isoformat(),
        "feeds": results,
    }

    filepath = os.path.join(OUTPUT_DIR, f"{today}.json")
    with open(filepath, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n💾 已保存: {filepath}")


if __name__ == "__main__":
    main()
