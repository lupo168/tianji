#!/usr/bin/env python3
"""天玑 · Agent Reach 采集器

通过 Agent Reach 读取指定平台的公开内容，覆盖 Twitter/Reddit/YouTube/B站/RSS 等渠道。
Agent Reach 负责平台接入和反爬，本采集器只做调度和结构化入库。

用法:
  python agentreach_collector.py                          # 默认采集所有可用渠道
  python agentreach_collector.py --channel youtube        # 只采 YouTube
  python agentreach_collector.py --channel reddit --query "water filter"

依赖: agent-reach (pip install agent-reach)
"""

import json, os, sys, subprocess, time
from datetime import datetime

# 添加父目录到 path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

OUTPUT_DIR = os.path.expanduser("~/tianji-data/agentreach")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Agent Reach 可用渠道 → 采集策略
CHANNELS = {
    "web": {
        "label": "网页阅读",
        "tool": "curl https://r.jina.ai/{url}",
        "queries": [],
        "enabled": True,
    },
    "youtube": {
        "label": "YouTube",
        "tool": "yt-dlp",
        "queries": [
            "pet water fountain review",
            "water filter review",
            "best pet products 2026",
        ],
        "enabled": True,
    },
    "rss": {
        "label": "RSS/Atom",
        "tool": "feedparser",
        "feeds": [
            "https://news.google.com/rss/search?q=pet+water+fountain&hl=en-US",
            "https://news.google.com/rss/search?q=water+filter&hl=en-US",
        ],
        "enabled": True,
    },
    "v2ex": {
        "label": "V2EX",
        "tool": "curl",
        "queries": ["宠物", "净水", "跨境电商"],
        "enabled": False,  # 中文技术社区，暂时不跑
    },
    "semantic": {
        "label": "语义搜索",
        "tool": "mcporter",
        "queries": [
            "pet water fountain market trends 2026",
            "water filtration technology breakthrough",
        ],
        "enabled": True,
    },
    "bilibili": {
        "label": "B站",
        "tool": "curl",
        "queries": ["宠物饮水机", "净水器测评"],
        "enabled": False,  # 中文内容
    },
}


def run_cmd(cmd, timeout=30):
    """运行 shell 命令，返回 stdout"""
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.stdout[:5000] if r.stdout else r.stderr[:1000]
    except Exception as e:
        return f"[error: {e}]"


def collect_youtube():
    """通过 yt-dlp 搜索 YouTube 并提取字幕/信息"""
    results = []
    for q in CHANNELS["youtube"]["queries"]:
        # yt-dlp 搜索
        search_url = f"ytsearch3:{q}"
        try:
            r = subprocess.run(
                ["yt-dlp", "--dump-json", "--flat-playlist", search_url],
                capture_output=True, text=True, timeout=30,
            )
            for line in r.stdout.strip().split("\n"):
                if not line:
                    continue
                try:
                    info = json.loads(line)
                    results.append({
                        "title": info.get("title", "")[:120],
                        "url": info.get("webpage_url", ""),
                        "channel": info.get("channel", ""),
                        "duration": info.get("duration"),
                        "views": info.get("view_count"),
                    })
                except json.JSONDecodeError:
                    pass
        except Exception as e:
            results.append({"query": q, "error": str(e)[:100]})
        time.sleep(0.5)
    return results


def collect_rss():
    """读取 RSS 源"""
    results = []
    for feed_url in CHANNELS["rss"]["feeds"]:
        try:
            r = subprocess.run(
                ["python3", "-c", f"""
import feedparser, json
d = feedparser.parse('{feed_url}')
items = [{{'title': e.get('title','')[:120], 'link': e.get('link',''), 'published': e.get('published','')}} for e in d.entries[:5]]
print(json.dumps(items, ensure_ascii=False))
"""],
                capture_output=True, text=True, timeout=20,
            )
            items = json.loads(r.stdout)
            results.extend([{**i, "feed": feed_url} for i in items])
        except Exception as e:
            results.append({"feed": feed_url, "error": str(e)[:100]})
    return results


def collect_semantic():
    """通过 mcporter + Exa 语义搜索"""
    results = []
    for q in CHANNELS["semantic"]["queries"]:
        try:
            # mcporter 语义搜索
            r = subprocess.run(
                ["mcporter", "search", q],
                capture_output=True, text=True, timeout=30,
            )
            output = r.stdout[:3000]
            results.append({"query": q, "results": output})
        except FileNotFoundError:
            results.append({"query": q, "error": "mcporter not in PATH"})
            break
        except Exception as e:
            results.append({"query": q, "error": str(e)[:100]})
    return results


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"天玑 · Agent Reach 采集器 | {today}")
    print("=" * 50)

    report = {"date": today, "collected_at": datetime.now().isoformat(), "channels": {}}

    # YouTube
    if CHANNELS["youtube"]["enabled"]:
        print(f"\n📺 YouTube: {CHANNELS['youtube']['queries']}")
        yt_results = collect_youtube()
        report["channels"]["youtube"] = yt_results
        print(f"  ✅ {len(yt_results)} 个视频")

    # RSS
    if CHANNELS["rss"]["enabled"]:
        print(f"\n📡 RSS: {len(CHANNELS['rss']['feeds'])} 个源")
        rss_results = collect_rss()
        report["channels"]["rss"] = rss_results
        print(f"  ✅ {len(rss_results)} 条")

    # Semantic
    if CHANNELS["semantic"]["enabled"]:
        print(f"\n🔍 语义搜索")
        sem_results = collect_semantic()
        report["channels"]["semantic"] = sem_results
        for s in sem_results:
            if "error" in s:
                print(f"  ⚠️ {s['query']}: {s['error']}")
            else:
                print(f"  ✅ {s['query']}: {len(s.get('results',''))} chars")

    # Save
    path = os.path.join(OUTPUT_DIR, f"{today}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"\n💾 {path}")

    # Summary
    total = sum(
        len(v) if isinstance(v, list) else 1
        for v in report["channels"].values()
    )
    print(f"📊 共 {total} 条数据，来自 {len(report['channels'])} 个渠道")


if __name__ == "__main__":
    main()
