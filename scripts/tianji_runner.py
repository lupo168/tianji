#!/usr/bin/env python3
"""天玑 · 采集运行器 — 一键运行所有P0/P1采集器

用法:
  python tianji_runner.py           # 运行所有采集器
  python tianji_runner.py --daily   # 仅运行每日采集
  python tianji_runner.py --weekly  # 仅运行每周采集
"""

import sys, os, subprocess, json
from datetime import datetime

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPTS_DIR)

def run_collector(name, script):
    """运行单个采集器并返回结果"""
    script_path = os.path.join(SCRIPTS_DIR, script)
    if not os.path.exists(script_path):
        return {"status": "error", "message": f"脚本不存在: {script_path}"}
    
    print(f"\n{'='*40}")
    print(f"▶ 运行: {name}")
    print(f"{'='*40}")

    # 采集器内部用 `from scripts.security.xxx import yyy` 这种包路径导入，
    # 需要把仓库根目录加进子进程的 PYTHONPATH，否则找不到 scripts 包。
    env = os.environ.copy()
    env["PYTHONPATH"] = REPO_ROOT + os.pathsep + env.get("PYTHONPATH", "")

    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=True, text=True, timeout=120,
        cwd=REPO_ROOT, env=env,
    )
    
    if result.returncode == 0:
        print(result.stdout)
        return {"status": "ok", "output": result.stdout}
    else:
        print(f"❌ 错误:\n{result.stderr}")
        return {"status": "error", "message": result.stderr}

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    
    collectors = {
        "daily": [
            ("汇率采集", "collectors/fx_collector.py"),
            ("RSS新闻采集", "collectors/rss_news_collector.py"),
            ("Wikipedia趋势", "collectors/wiki_trends_collector.py"),
            ("Hacker News趋势", "collectors/hn_trends_collector.py"),
            ("政府开放数据", "collectors/gov_open_data_collector.py"),
            ("Reddit消费者洞察", "collectors/reddit_collector.py"),
            ("营销广告情报", "collectors/marketing_intel_collector.py"),
            ("SEO/GEO搜索情报", "collectors/seo_geo_collector.py"),
            ("品牌声誉资本", "collectors/reputation_capital_collector.py"),
            ("渠道政策监控", "collectors/channel_policy_collector.py"),
            ("YouTube趋势", "collectors/youtube_collector.py"),
            ("Telegram行业监控", "collectors/telegram_collector.py"),
            ("大宗商品参考价", "collectors/commodity_collector.py"),
        ],
        "weekly": [],
        "monthly": [],
    }
    
    if mode == "--daily" or mode == "all":
        for name, script in collectors["daily"]:
            run_collector(name, script)
        run_collector("日报生成", "tianji_daily_report.py")
    
    if mode == "--weekly" or mode == "all":
        for name, script in collectors["weekly"]:
            run_collector(name, script)
    
    if mode == "--monthly" or mode == "all":
        for name, script in collectors["monthly"]:
            run_collector(name, script)
    
    print(f"\n{'='*40}")
    print(f"✅ 天玑采集完成 | {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*40}")

if __name__ == "__main__":
    main()
