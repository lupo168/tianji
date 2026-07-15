#!/usr/bin/env python3
"""天玑 · 日报生成器 v2 — 展示所有采集结果
"""

import json, os
from datetime import datetime

from scripts.security.report_filter import check_report, SubjectiveContentDetectedError

DATA_DIR = os.path.expanduser("~/tianji-data")
REPORT_DIR = os.path.join(DATA_DIR, "reports")

def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return None

def generate_daily_report():
    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%H:%M")
    
    lines = []
    def p(s=""): lines.append(s)
    
    def sep(): p("-" * 50)
    
    p("=" * 50)
    p(f"  天玑日报 — {today}  {now}")
    p("=" * 50)
    p()
    
    # === 汇率 ===
    fx = load_json(os.path.join(DATA_DIR, "exchange-rates", f"{today}.json"))
    p("📊 汇率")
    sep()
    if fx:
        cbr = fx.get("sources", {}).get("cbr", {})
        p(f"  CBR俄罗斯央行: {cbr.get('cbr_status', 'N/A')}")
        er = fx.get("sources", {}).get("exchangerate", {})
        for k, v in er.items():
            if k != "exchangerate_status" and v != "N/A":
                p(f"  {k}: {v}")
    else:
        p("  （无数据）")
    p()
    
    # === Hacker News热门 ===
    hn = load_json(os.path.join(DATA_DIR, "hackernews", f"{today}.json"))
    p("🔥 Hacker News 热门")
    sep()
    if hn and hn.get("data", {}).get("status") == "ok":
        stories = hn["data"]["stories"][:8]
        for s in stories:
            p(f"  [{s['score']:>3}票] {s['title'][:70]}")
    else:
        p("  （无数据）")
    p()
    
    # === 新闻摘要 ===
    news = load_json(os.path.join(DATA_DIR, "news", f"{today}.json"))
    p("📰 新闻摘要")
    sep()
    if news:
        for feed in news.get("feeds", []):
            if feed.get("status") == "ok":
                p(f"  {feed['name']}:")
                for item in feed.get("items", [])[:2]:
                    p(f"    ├ {item['title'][:65]}")
    else:
        p("  （无数据）")
    p()
    
    # === 科技趋势 ===
    wiki = load_json(os.path.join(DATA_DIR, "trends", f"{today}.json"))
    p("🌐 科技/商业趋势")
    sep()
    if wiki:
        wd = wiki.get("data", {})
        top = wd.get("today_top", [])
        if top:
            p("  Wikipedia今日热门:")
            for a in top[:4]:
                p(f"    ├ {a['title'][:50]} ({a['views']}次)")
    else:
        p("  （Wikipedia数据可能有1天延迟）")
    p()
    
    # === 告警区 ===
    p("🔴 告警区")
    sep()
    p("  （告警规则引擎开发中）")
    p()
    p("🟡 关注区")
    sep()
    p("  （关注规则引擎开发中）")
    p()
    
    p("=" * 50)
    p(f"  天玑 · 全球商业情报系统 | 报告结束")
    p("=" * 50)
    
    return "\n".join(lines)

def main():
    os.makedirs(REPORT_DIR, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    report = generate_daily_report()

    try:
        check_report(report)
    except SubjectiveContentDetectedError as e:
        print(f"❌ 日报未通过事实层检查，拒绝写入：\n{e}")
        return

    print(report)
    filepath = os.path.join(REPORT_DIR, f"daily-{today}.md")
    with open(filepath, "w") as f:
        f.write(report)
    print(f"\n💾 日报已保存: {filepath}")

if __name__ == "__main__":
    main()