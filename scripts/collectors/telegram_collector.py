#!/usr/bin/env python3
"""天玑 · Telegram行业群监控采集器

数据源: Telegram Bot API
费用: 完全免费 (无限制)
接入: 通过 @BotFather 创建Bot，获取token

配置步骤:
  1. 打开 Telegram, 搜索 @BotFather
  2. 发送 /newbot, 按提示创建
  3. 拿到 bot token
  4. 写进项目根目录的 .env：
     TELEGRAM_BOT_TOKEN=你的bot token

安全说明: Telegram Bot API 的设计本身要求 token 出现在URL路径里，
这是它协议层面的限制，不是天玑能绕开的。为了不让 token 出现在任何
日志/异常信息里，所有错误处理都只打印遮罩后的 token。
"""

import json
import os
from datetime import datetime

from scripts.security.env_loader import load_env, mask_secret
from scripts.security.safe_requests import get_json

OUTPUT_DIR = os.path.expanduser("~/tianji-data/telegram")
os.makedirs(OUTPUT_DIR, exist_ok=True)

load_env()


def get_updates(token, limit=10):
    """获取Bot收到的最近消息"""
    try:
        url = f"https://api.telegram.org/bot{token}/getUpdates?limit={limit}"
        return get_json(url, reason="Telegram Bot消息拉取")
    except Exception as e:
        # 注意：这里不打印完整异常信息，因为部分HTTP库的异常信息里会包含完整URL（含token）
        return {"ok": False, "description": f"请求失败（token={mask_secret(token)}）"}


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"天玑 · Telegram监控采集器 | {today}")
    print("=" * 50)

    token = os.getenv("TELEGRAM_BOT_TOKEN", "")

    if not token:
        print("""
  ⏳ Telegram Bot 未配置

  要启用Telegram采集器（30秒）:
    1. 打开 Telegram, 搜索 @BotFather
    2. 发送 /newbot, 按提示创建
    3. 拿到 bot token
    4. 写进项目根目录的 .env：
       TELEGRAM_BOT_TOKEN=你的bot token

  然后把你Bot加入行业群/频道, 它就开始采集了。
""")
        output = {"date": today, "status": "skipped"}
        with open(os.path.join(OUTPUT_DIR, f"{today}.json"), "w") as f:
            json.dump(output, f, indent=2)
        return

    data = get_updates(token)

    if data.get("ok"):
        messages = []
        for update in data.get("result", []):
            msg = update.get("message") or update.get("channel_post", {})
            chat = msg.get("chat", {})
            messages.append({
                "chat_name": chat.get("title", chat.get("username", "unknown")),
                "chat_type": chat.get("type", "unknown"),
                "text": (msg.get("text", "") or msg.get("caption", "") or "")[:500],
                "date": datetime.fromtimestamp(msg.get("date", 0)).isoformat(),
            })

        print(f"  ✅ 最近消息: {len(messages)}条")
        for m in messages[:5]:
            print(f"     [{m['chat_name']}] {m['text'][:60]}")

        output = {"date": today, "collected_at": datetime.now().isoformat(), "status": "ok", "messages": messages}
    else:
        print(f"  ⚠️ {data.get('description', '未知错误')}")
        output = {"date": today, "status": "error", "message": data.get("description", "")}

    filepath = os.path.join(OUTPUT_DIR, f"{today}.json")
    with open(filepath, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n💾 已保存: {filepath}")


if __name__ == "__main__":
    main()
