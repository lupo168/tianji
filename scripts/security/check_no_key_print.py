#!/usr/bin/env python3
"""
check_no_key_print.py — pre-commit 静态检查

作用：扫描所有暂存的 .py 文件，禁止出现任何形式的
"把变量名含 key/token/secret 的东西打印/写日志/塞进字符串" 的代码模式。

这道检查直接针对上次事故的根因：
不是任务执行时读了 key，是调试/验证代码时把 key 打印出来确认，
这个打印动作进了 Hermes 的对话上下文，然后被路由到了 DeepSeek。

原则：验证 key 是否有效，只能用 verify_key.sh 这类不经过模型上下文的方式，
不能在 Python 代码里 print/log 任何密钥变量。
"""

import re
import sys
from pathlib import Path

KEY_NAME_PATTERN = re.compile(r"(api[_-]?key|token|secret|password)", re.IGNORECASE)

# 匹配 print(...key...) / logging.info(...key...) / f"...{key}..." 里带 key 变量的写法
DANGEROUS_CALL_PATTERN = re.compile(
    r"(print|log(ger)?\.\w+)\s*\([^)]*(" + KEY_NAME_PATTERN.pattern + r")[^)]*\)",
    re.IGNORECASE,
)


def check_file(path: Path) -> list:
    violations = []
    text = path.read_text(encoding="utf-8", errors="ignore")
    for lineno, line in enumerate(text.splitlines(), start=1):
        if DANGEROUS_CALL_PATTERN.search(line):
            violations.append((path, lineno, line.strip()))
    return violations


def main() -> int:
    files = [Path(f) for f in sys.argv[1:]]
    all_violations = []
    for f in files:
        if f.exists() and f.suffix == ".py":
            all_violations.extend(check_file(f))

    if all_violations:
        print("❌ 检测到疑似打印/记录密钥明文的代码：\n")
        for path, lineno, line in all_violations:
            print(f"  {path}:{lineno}: {line}")
        print("\n验证 key 是否有效，请使用 scripts/security/verify_key.sh，")
        print("不要在 Python 代码里 print/log 任何密钥变量。")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
