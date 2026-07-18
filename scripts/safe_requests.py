#!/usr/bin/env python3
"""天玑 · 安全 HTTP 请求层

所有采集器的网络请求必须走这个模块。
提供: 域名白名单、UA伪装、自动重试、超时控制、错误日志

用法:
    from safe_requests import safe_get, load_whitelist
    data = safe_get("https://api.example.com/data", headers={"x-key": key})
"""

import json, time, os
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse


USER_AGENT = (
    "Tianji/1.0 (+https://github.com/lupo168/tianji; "
    "Business Intelligence Collector)"
)

DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
RETRY_DELAY = 1.0

# ---------- 白名单 ----------

_whitelist = None
_whitelist_loaded = False

def load_whitelist():
    """加载域名白名单，返回 set"""
    global _whitelist, _whitelist_loaded
    if _whitelist_loaded:
        return _whitelist

    paths = [
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "DOMAIN_WHITELIST.json"),
        os.path.expanduser("~/.hermes/skills/tianji-base/config/DOMAIN_WHITELIST.json"),
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                with open(p, encoding="utf-8") as f:
                    data = json.load(f)
                _whitelist = set(data.get("domains", []))
                _whitelist_loaded = True
                return _whitelist
            except Exception:
                pass

    _whitelist = set()
    _whitelist_loaded = True
    return _whitelist


def _check_domain(url):
    """检查 URL 域名是否在白名单中。不在 → 返回错误。
    也接受 IP 地址和相对路径。
    """
    parsed = urlparse(url)
    hostname = parsed.hostname
    if not hostname:
        return None  # 相对路径，放行

    # 去掉 www 前缀后匹配
    hostname = hostname.lower()
    if hostname.startswith("www."):
        hostname = hostname[4:]

    wl = load_whitelist()
    if not wl:
        return None  # 白名单为空，放行（开发模式）

    if hostname in wl:
        return None

    # 检查父域名（如 api.etsy.com 匹配 etsy.com）
    parts = hostname.split(".")
    for i in range(len(parts) - 1):
        parent = ".".join(parts[i + 1:])
        if parent in wl:
            return None

    return f"Domain '{hostname}' not in whitelist"


# ---------- 请求函数 ----------

def safe_get(url, headers=None, timeout=None, max_retries=None, skip_whitelist=False):
    """GET 请求，带安全层

    Args:
        skip_whitelist: 跳过白名单检查（仅调试用）

    Returns:
        dict: 解析后的 JSON，失败时返回 {"error": "..."}
    """
    if not skip_whitelist:
        err = _check_domain(url)
        if err:
            return {"error": err}

    if headers is None:
        headers = {}
    headers.setdefault("User-Agent", USER_AGENT)

    timeout = timeout or DEFAULT_TIMEOUT
    max_retries = max_retries if max_retries is not None else MAX_RETRIES

    req = Request(url, headers=headers)

    last_error = None
    for attempt in range(max_retries):
        try:
            with urlopen(req, timeout=timeout) as resp:
                body = resp.read().decode("utf-8", errors="replace")
                return json.loads(body)
        except HTTPError as e:
            last_error = f"HTTP {e.code}: {e.reason}"
            if e.code in (429, 503):
                time.sleep(RETRY_DELAY * (attempt + 1))
                continue
            return {"error": last_error}
        except URLError as e:
            last_error = f"URL Error: {e.reason}"
            time.sleep(RETRY_DELAY)
        except json.JSONDecodeError as e:
            last_error = f"JSON Parse Error: {e}"
            return {"error": last_error}
        except Exception as e:
            last_error = f"Error: {e}"
            time.sleep(RETRY_DELAY)

    return {"error": last_error}


def safe_get_raw(url, headers=None, timeout=None, skip_whitelist=False):
    """GET 请求，返回原始字节（用于非 JSON 响应）"""
    if not skip_whitelist:
        err = _check_domain(url)
        if err:
            return None

    if headers is None:
        headers = {}
    headers.setdefault("User-Agent", USER_AGENT)

    timeout = timeout or DEFAULT_TIMEOUT
    req = Request(url, headers=headers)

    try:
        with urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except Exception as e:
        return None
