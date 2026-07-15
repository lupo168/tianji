#!/usr/bin/env python3
"""
review_suspicious_content.py — 可疑内容审计日志查看工具

用法：
    python3 scripts/security/review_suspicious_content.py         # 列出所有被标记的可疑内容
    python3 scripts/security/review_suspicious_content.py --clear  # 清空日志（人工确认已处理后）
"""

import argparse
from pathlib import Path

import yaml

_HERE = Path(__file__).parent
_LOG_PATH = _HERE / "suspicious_content_log.yaml"


def list_entries():
    if not _LOG_PATH.exists():
        print("目前没有被标记的可疑内容。")
        return

    with open(_LOG_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {"entries": []}

    entries = data.get("entries", [])
    if not entries:
        print("目前没有被标记的可疑内容。")
        return

    print(f"共 {len(entries)} 条被标记的可疑内容：\n")
    for i, e in enumerate(entries, start=1):
        print(f"[{i}] 来源: {e['source_url']}")
        print(f"    时间: {e['detected_at']}")
        print(f"    命中模式: {', '.join(e['matched_patterns'])}")
        print(f"    片段: {e['snippet'][:150]}...")
        print(f"    已人工核实: {'是' if e.get('human_reviewed') else '否'}")
        print()

    print(
        "说明：这些内容已经被 content_sanitizer.py 包裹为不可信数据块，"
        "不会被当成指令执行。这个日志的作用是让你定期抽查，判断是不是某个"
        "信源经常出现这类内容，值得考虑要不要从白名单里移除。"
    )


def clear():
    if _LOG_PATH.exists():
        _LOG_PATH.unlink()
    print("日志已清空。")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--clear", action="store_true")
    args = parser.parse_args()

    if args.clear:
        clear()
    else:
        list_entries()


if __name__ == "__main__":
    main()
