#!/usr/bin/env python3
"""天玑 · 安全 HTTP 请求层

所有采集器的网络请求必须走这个模块。
提供: UA伪装、自动重试、超时控制、错误日志

用法:
    from safe_requests import safe_get
    data = safe_get("https://api.example.com/data", headers={"x-key": key})
"""

import json, time
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


USER_AGENT = (
    "Tianji/1.0 (+https://github.com/lupo168/tianji; "
    "Business Intelligence Collector)"
)

DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
RETRY_DELAY = 1.0


def safe_get(url, headers=None, timeout=None, max_retries=None):
    """GET 请求，带安全层

    Returns:
        dict: 解析后的 JSON，失败时返回 {"error": "..."}
    """
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


def safe_get_raw(url, headers=None, timeout=None):
    """GET 请求，返回原始字节（用于非 JSON 响应）"""
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
