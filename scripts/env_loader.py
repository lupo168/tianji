#!/usr/bin/env python3
"""天玑 · 环境与密钥加载器

统一从多个安全源加载 API key 和配置。
优先级: 环境变量 > secrets JSON > 默认值

用法:
    from env_loader import load_key, load_config
    api_key = load_key("etsy_api_key")
    config = load_config()
"""

import json, os

SECRETS_DIR = os.path.expanduser("~/.hermes/secrets")
CONFIG_FILES = [
    "tianji_config.json",
    "ecommerce.json",
]


def load_config():
    """合并所有配置文件返回一个 dict。先加载的优先级低。"""
    merged = {}
    for fname in CONFIG_FILES:
        path = os.path.join(SECRETS_DIR, fname)
        try:
            with open(path) as f:
                data = json.load(f)
            # ecommerce.json 结构可能是嵌套的，展平
            _flatten_dict(data, merged)
        except (FileNotFoundError, json.JSONDecodeError):
            pass
    return merged


def load_key(key_name):
    """加载单个密钥。先查环境变量，再查 secrets 文件。

    环境变量命名: TIANJI_<KEY>  (如 TIANJI_ETSY_API_KEY)
    """
    env_name = f"TIANJI_{key_name.upper()}"
    val = os.environ.get(env_name)
    if val:
        return val

    config = load_config()
    return config.get(key_name)


def _flatten_dict(d, out, prefix=""):
    """递归展开嵌套 dict 到扁平 key"""
    if isinstance(d, dict):
        for k, v in d.items():
            full_key = f"{prefix}_{k}" if prefix else k
            if isinstance(v, dict):
                _flatten_dict(v, out, full_key)
            else:
                out[full_key] = v
