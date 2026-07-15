#!/usr/bin/env python3
"""
review_pending_domains.py — 待审核域名队列查看工具

用法：
    python3 scripts/security/review_pending_domains.py            # 列出所有待审核域名
    python3 scripts/security/review_pending_domains.py --approve example.com
    python3 scripts/security/review_pending_domains.py --reject example.com

approve 操作只做一件事：把这个域名从 pending_domains.yaml 挪到
domain_whitelist.yaml，并要求你手动确认（不是脚本自动帮你决定值不值得加）。
"""

import argparse
import sys
from pathlib import Path

import yaml

_HERE = Path(__file__).parent
_PENDING_PATH = _HERE / "pending_domains.yaml"
_WHITELIST_PATH = _HERE / "domain_whitelist.yaml"


def load_pending():
    if not _PENDING_PATH.exists():
        return {"pending": []}
    with open(_PENDING_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {"pending": []}


def save_pending(data):
    with open(_PENDING_PATH, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)


def load_whitelist():
    with open(_WHITELIST_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {"allowed_domains": [], "review_log": []}


def save_whitelist(data):
    with open(_WHITELIST_PATH, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)


def list_pending():
    data = load_pending()
    if not data["pending"]:
        print("当前没有待审核的域名。")
        return

    print(f"共 {len(data['pending'])} 个待审核域名：\n")
    for item in data["pending"]:
        print(f"域名: {item['domain']}")
        print(f"  首次出现: {item['first_seen_url']}")
        print(f"  请求时间: {item['requested_at']}")
        print(f"  任务原因: {item['task_reason']}")
        print(f"  开阳评估: {item.get('kaiyang_annotation') or '（尚未评估）'}")
        print(f"  人类决定: {item.get('human_decision') or '（待审核）'}")
        print()


def approve(domain: str):
    pending_data = load_pending()
    match = next((i for i in pending_data["pending"] if i["domain"] == domain), None)
    if not match:
        print(f"没有在待审核队列里找到 {domain}")
        sys.exit(1)

    print(f"即将批准域名: {domain}")
    print(f"  任务原因: {match['task_reason']}")
    print(f"  开阳评估: {match.get('kaiyang_annotation') or '（无）'}")
    confirm = input("确认加入白名单？[y/N] ").strip().lower()
    if confirm != "y":
        print("已取消。")
        return

    whitelist_data = load_whitelist()
    whitelist_data.setdefault("allowed_domains", []).append(domain)
    whitelist_data.setdefault("review_log", []).append({
        "domain": domain,
        "added_by": "human_review",
        "date": match["requested_at"],
        "reason": match["task_reason"],
    })
    save_whitelist(whitelist_data)

    pending_data["pending"] = [i for i in pending_data["pending"] if i["domain"] != domain]
    save_pending(pending_data)
    print(f"✅ {domain} 已加入 domain_whitelist.yaml")


def reject(domain: str):
    pending_data = load_pending()
    before = len(pending_data["pending"])
    pending_data["pending"] = [i for i in pending_data["pending"] if i["domain"] != domain]
    if len(pending_data["pending"]) == before:
        print(f"没有在待审核队列里找到 {domain}")
        sys.exit(1)
    save_pending(pending_data)
    print(f"❌ {domain} 已从待审核队列移除，不加入白名单")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--approve", metavar="DOMAIN")
    parser.add_argument("--reject", metavar="DOMAIN")
    args = parser.parse_args()

    if args.approve:
        approve(args.approve)
    elif args.reject:
        reject(args.reject)
    else:
        list_pending()


if __name__ == "__main__":
    main()
