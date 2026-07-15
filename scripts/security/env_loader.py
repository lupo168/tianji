"""
env_loader.py — 极简 .env 加载器

不引入 python-dotenv 依赖，手写一个最小实现：
在项目根目录放 .env 文件（KEY=VALUE 每行一个），运行时读入 os.environ。

用这个替代原来分散在各个采集器里的 ~/.hermes/secrets/tianji_config.json：
那个文件是明文JSON，且路径在 Hermes 的家目录下，等于所有key都摆在
Hermes 随手可读的地方。统一到项目根目录 .env，配合 .gitignore 和
verify_key.sh，管理起来是一个入口，不是三四个。
"""

import os
from pathlib import Path

_ENV_PATH = Path(__file__).resolve().parents[2] / ".env"


def load_env(env_path=None) -> None:
    """把 .env 读入 os.environ。已存在的环境变量不覆盖（环境变量优先级更高）。"""
    path = Path(env_path) if env_path else _ENV_PATH
    if not path.exists():
        return
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)


def mask_secret(value: str, keep: int = 4) -> str:
    """打印/记录日志时用这个，绝不要在日志里出现密钥全文。"""
    if not value:
        return "(未配置)"
    if len(value) <= keep:
        return "***"
    return value[:keep] + "***"
