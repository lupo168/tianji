#!/usr/bin/env python3
"""
check_no_raw_requests.py — pre-commit 静态检查

作用：扫描 scripts/collectors/ 下的所有 .py 文件，
禁止直接 `import requests` 或 `import urllib`，强制统一走 safe_requests.py。

原理：白名单/写操作拦截只在 safe_requests.py 里生效，
如果采集器绕过它直接用 requests，所有的网络白名单机制就形同虚设。
所以这道检查本身也必须是代码层强制，而不是文档里写"请统一使用xxx"。
"""

import re
import sys
from pathlib import Path

FORBIDDEN_PATTERNS = [
    re.compile(r"^\s*import requests\b"),
    re.compile(r"^\s*from requests\b"),
    re.compile(r"^\s*import urllib\.request\b"),
    re.compile(r"^\s*from urllib\.request\b"),
]

ALLOWED_FILE = "safe_requests.py"


def check_file(path: Path) -> list:
    if path.name == ALLOWED_FILE:
        return []
    violations = []
    text = path.read_text(encoding="utf-8", errors="ignore")
    for lineno, line in enumerate(text.splitlines(), start=1):
        for pattern in FORBIDDEN_PATTERNS:
            if pattern.match(line):
                violations.append((path, lineno, line.strip()))
    return violations


def main() -> int:
    files = [Path(f) for f in sys.argv[1:]]
    all_violations = []
    for f in files:
        if f.exists():
            all_violations.extend(check_file(f))

    if all_violations:
        print("❌ 检测到采集器直接使用了 requests/urllib，必须改用 scripts/security/safe_requests.py：\n")
        for path, lineno, line in all_violations:
            print(f"  {path}:{lineno}: {line}")
        print("\n修复方式：将 `import requests` 改为")
        print("  from scripts.security.safe_requests import get")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
