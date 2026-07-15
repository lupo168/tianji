"""
safe_search.py — AnySearch 聚合搜索的统一安全封装

三个采集器（marketing_intel / reputation_capital / seo_geo）都通过
subprocess 调用 AnySearch CLI。这个封装做两件事：
1. 统一 subprocess 调用方式，不用每个采集器各写一遍
2. 强制把返回结果过一遍 content_sanitizer——AnySearch 返回的内容来自
   任意网页，域名白名单管不到这一层，必须在内容层面做防注入处理

用法：
    from scripts.security.safe_search import search_anysearch

    safe_text, flagged = search_anysearch("pet water fountain reviews", max_results=3)
    # safe_text 才是允许往下传给数据库/日报/开阳的版本
"""

import subprocess
import sys
from pathlib import Path
from typing import Tuple

from scripts.security.content_sanitizer import sanitize

_ANYSEARCH_CLI = Path.home() / ".hermes" / "skills" / "anysearch" / "scripts" / "anysearch_cli.py"


def search_anysearch(query: str, max_results: int = 3, timeout: int = 20) -> Tuple[str, bool]:
    """调用 AnySearch，返回 (清洗后的文本, 是否检测到可疑内容)。

    调用失败时返回空字符串，不抛异常——采集器应该把失败当成"这次没采到"处理，
    不应该让单次搜索失败中断整个采集流程。
    """
    if not _ANYSEARCH_CLI.exists():
        return "", False

    try:
        result = subprocess.run(
            [sys.executable, str(_ANYSEARCH_CLI), "search", query, "--max_results", str(max_results)],
            capture_output=True, text=True, timeout=timeout,
        )
        raw = result.stdout if result.returncode == 0 else ""
    except Exception:
        raw = ""

    if not raw:
        return "", False

    return sanitize(raw, source_url=f"anysearch:{query}")
