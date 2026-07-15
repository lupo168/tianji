"""
safe_requests.py — 天玑网络白名单强制层

所有采集器（scripts/collectors/*.py）必须通过这个模块发起 HTTP 请求，
禁止直接 `import requests` 或 `urllib`。

原则：
- 白名单外的域名，在这里就被拒绝，不依赖采集器代码"记得"检查
- 任何写操作（POST/PUT/DELETE）一律硬拒绝，不区分域名——天玑是纯采集子系统
- 新增信源域名必须由人在 domain_whitelist.yaml 里手动加，代码运行时不能自行决定访问新域名
"""

import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import requests
import yaml

_WHITELIST_PATH = Path(__file__).parent / "domain_whitelist.yaml"
_PENDING_PATH = Path(__file__).parent / "pending_domains.yaml"


class DomainNotWhitelistedError(Exception):
    """访问了白名单之外的域名"""


class WriteOperationBlockedError(Exception):
    """天玑试图执行写操作"""


def _load_whitelist() -> set:
    with open(_WHITELIST_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return set(data.get("allowed_domains", []))


def _is_allowed(url: str, whitelist: set) -> bool:
    host = urlparse(url).hostname or ""
    for pattern in whitelist:
        # 支持 *.example.com 这种通配写法
        regex = "^" + re.escape(pattern).replace(r"\*", ".*") + "$"
        if re.match(regex, host):
            return True
    return False


def _log_pending_domain(host: str, url: str, reason: str = "") -> None:
    """把被拒绝的域名记录到待审核队列，而不是只报错完事。

    审核流程：开阳可以在这个队列上写评估/推荐意见（kaiyang_annotation 字段），
    但只有人类在 domain_whitelist.yaml 里手动加入才算生效——
    这一步任何 agent 都没有写权限。
    """
    data = {"pending": []}
    if _PENDING_PATH.exists():
        with open(_PENDING_PATH, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {"pending": []}

    # 同一个域名已经在队列里就不重复记录
    if any(item.get("domain") == host for item in data["pending"]):
        return

    data["pending"].append({
        "domain": host,
        "first_seen_url": url,
        "requested_at": datetime.now(timezone.utc).isoformat(),
        "task_reason": reason or "未说明",
        "kaiyang_annotation": None,   # 开阳可以填这一栏：是否推荐、为什么
        "human_decision": None,        # 人类审批结果：approved / rejected，只有人能填
    })

    with open(_PENDING_PATH, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)


def _check_domain(url: str, reason: str = "") -> None:
    whitelist = _load_whitelist()
    if not _is_allowed(url, whitelist):
        host = urlparse(url).hostname
        _log_pending_domain(host, url, reason)
        raise DomainNotWhitelistedError(
            f"[天玑安全层] 拒绝访问未授权域名: {host}\n"
            f"已自动记录到 scripts/security/pending_domains.yaml 待审核。\n"
            f"开阳可以在这个文件里写评估意见，但只有人类能把域名正式加入 domain_whitelist.yaml。"
        )


def get(url: str, reason: str = "", **kwargs):
    """唯一允许的请求方式：只读 GET，且域名必须在白名单内。

    reason: 可选，说明这次请求是为了什么任务/信源评估，
    会被记录进 pending_domains.yaml，方便人类审核时了解上下文。
    """
    _check_domain(url, reason)
    return requests.get(url, **kwargs)


_DEFAULT_HEADERS = {"User-Agent": "Tianji/1.0"}


def get_json(url: str, reason: str = "", timeout: int = 15, headers: dict = None):
    """GET 并直接解析为 JSON，采集器里最常见的用法，统一走这个而不是各自拼 urllib。"""
    resp = get(url, reason=reason, headers=headers or _DEFAULT_HEADERS, timeout=timeout)
    return resp.json()


def get_text(url: str, reason: str = "", timeout: int = 15, headers: dict = None, encoding: str = None):
    """GET 并返回文本（RSS/HTML等），需要手动解析的场景用这个。"""
    resp = get(url, reason=reason, headers=headers or _DEFAULT_HEADERS, timeout=timeout)
    if encoding:
        resp.encoding = encoding
    return resp.text


def post(url: str, **kwargs):
    raise WriteOperationBlockedError(
        "[天玑安全层] 检测到 POST 请求。天玑是纯采集子系统，禁止任何写操作/提交动作。"
        "如果这是分析或执行需求，应该属于开阳的职责范围，不应该出现在 collectors/ 目录下。"
    )


def put(url: str, **kwargs):
    raise WriteOperationBlockedError("[天玑安全层] 禁止 PUT 请求，天玑不允许任何写操作。")


def delete(url: str, **kwargs):
    raise WriteOperationBlockedError("[天玑安全层] 禁止 DELETE 请求，天玑不允许任何写操作。")


def patch(url: str, **kwargs):
    raise WriteOperationBlockedError("[天玑安全层] 禁止 PATCH 请求，天玑不允许任何写操作。")


# === OAuth token 交换：唯一被允许的、窄口径的 POST 例外 ===
#
# 天玑的"禁止写操作"红线针对的是对外部业务系统的写入（下单、改价、发消息）。
# OAuth client_credentials 认证握手不属于这一类——它换来的只是一个访问令牌，
# 用来让后续的 GET 请求能通过认证，本身不对任何外部系统产生业务后果。
#
# 但这仍然是一个POST，所以：
#   1. 只允许访问下面这个硬编码的白名单（不读 domain_whitelist.yaml，避免被间接放宽）
#   2. 每次调用都记录一条审计日志，方便事后检查这个例外有没有被滥用
_OAUTH_ENDPOINT_WHITELIST = {
    "https://www.reddit.com/api/v1/access_token",
}

_OAUTH_LOG_PATH = Path(__file__).parent / "oauth_token_exchange_log.yaml"


def oauth_token_exchange(url: str, **kwargs):
    """唯一被允许发起的 POST：仅用于 OAuth client_credentials 换取访问令牌。

    url 必须完全匹配 _OAUTH_ENDPOINT_WHITELIST 里的条目，不支持通配符——
    新增一个OAuth端点需要改这份代码本身，不是改配置文件，这是故意的，
    保证这条窄口径不会被"顺手"扩大成一般性的POST能力。
    """
    if url not in _OAUTH_ENDPOINT_WHITELIST:
        raise WriteOperationBlockedError(
            f"[天玑安全层] {url} 不在 OAuth token 交换白名单内，拒绝执行。"
            f"这个函数只能用于换取访问令牌，不是通用POST接口。"
        )

    _log_oauth_call(url)
    return requests.post(url, **kwargs)


def _log_oauth_call(url: str) -> None:
    data = {"calls": []}
    if _OAUTH_LOG_PATH.exists():
        with open(_OAUTH_LOG_PATH, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {"calls": []}
    data["calls"].append({"url": url, "at": datetime.now(timezone.utc).isoformat()})
    with open(_OAUTH_LOG_PATH, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)
