#!/usr/bin/env python3
"""天玑 · Reddit消费者洞察采集器

数据源: Reddit API (免费, 60req/min)
接入条件: 需注册Reddit App (免费, 1分钟搞定)

注册步骤:
  1. 打开 https://www.reddit.com/prefs/apps
  2. 点击 "are you a developer? create an app..."
  3. 选 "script", 填任何名称/描述/redirect uri (填 http://localhost)
  4. 把 client_id 和 client_secret 配置到项目根目录的 .env 文件：
     REDDIT_CLIENT_ID=你的client_id
     REDDIT_CLIENT_SECRET=你的client_secret

用法:
  python reddit_collector.py         # 采集所有配置的子版块
"""

import base64
import json
import os
import time
from datetime import datetime
from urllib.parse import urlencode

from scripts.security.env_loader import load_env
from scripts.security.safe_requests import get, oauth_token_exchange

OUTPUT_DIR = os.path.expanduser("~/tianji-data/reddit")
os.makedirs(OUTPUT_DIR, exist_ok=True)

load_env()

USER_AGENT = "TianjiRedditBot/1.0"

SUBREDDITS = [
    "pets", "dogs", "cats", "PetAdvice", "DogAdvice", "CatAdvice",
    "puppy101", "kittens",
    "BuyItForLife", "ProductReviews", "AmazonReviews",
    "ecommerce", "dropshipping", "shopify", "Entrepreneur",
    "smallbusiness", "FulfillmentByAmazon",
    "startups", "tech", "gadgets", "homeautomation",
    "WaterTreatment", "WaterFilters",
]


def get_access_token(client_id, client_secret):
    """OAuth2 获取访问令牌。

    走 scripts/security/safe_requests.py 里的 oauth_token_exchange()——
    这是天玑唯一被允许的POST出口，硬编码白名单只认Reddit这一个token端点，
    每次调用都会被记录审计，不是绕开"禁止写操作"红线，是给这个特定、
    无业务后果的例外单独开了一条可审查的窄通道。
    """
    if not client_id or not client_secret:
        return None
    try:
        auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        resp = oauth_token_exchange(
            "https://www.reddit.com/api/v1/access_token",
            data={"grant_type": "client_credentials"},
            headers={"Authorization": f"Basic {auth}", "User-Agent": USER_AGENT},
            timeout=10,
        )
        return resp.json().get("access_token")
    except Exception as e:
        print(f"  ⚠️ Reddit认证失败: {e}")
        return None


def fetch_subreddit(token, subreddit, limit=5):
    try:
        headers = {"Authorization": f"Bearer {token}", "User-Agent": USER_AGENT}
        url = f"https://oauth.reddit.com/r/{subreddit}/hot?limit={limit}"
        resp = get(url, reason=f"Reddit采集-r/{subreddit}", headers=headers, timeout=10)
        data = resp.json()

        posts = []
        for post in data.get("data", {}).get("children", []):
            p = post.get("data", {})
            posts.append({
                "title": p.get("title", "")[:200],
                "score": p.get("score", 0),
                "comments": p.get("num_comments", 0),
                "url": p.get("url", ""),
                "permalink": f"https://reddit.com{p.get('permalink', '')}",
                "created_utc": p.get("created_utc", 0),
                "subreddit": subreddit,
                "domain": p.get("domain", ""),
                "is_self": p.get("is_self", False),
                "selftext": (p.get("selftext", "") or "")[:300],
            })
        return {"status": "ok", "posts": posts}
    except Exception as e:
        return {"status": f"error: {str(e)[:60]}", "posts": []}


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().isoformat()

    print(f"天玑 · Reddit消费者洞察 | {today}")
    print("=" * 50)

    client_id = os.getenv("REDDIT_CLIENT_ID", "")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET", "")
    token = get_access_token(client_id, client_secret)

    if not token:
        print("""
  ⏳ Reddit API 未配置

  要启用Reddit采集器，只需1分钟：
    1. 打开 https://www.reddit.com/prefs/apps
    2. 点击 "are you a developer? create an app..."
    3. 选 "script"，填名称/描述/redirect uri (http://localhost)
    4. 把 client_id / client_secret 写进项目根目录的 .env：
       REDDIT_CLIENT_ID=你的client_id
       REDDIT_CLIENT_SECRET=你的client_secret
""")
        output = {"date": today, "collected_at": now, "status": "skipped", "message": "Reddit API未配置"}
        filepath = os.path.join(OUTPUT_DIR, f"{today}.json")
        with open(filepath, "w") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        return

    print(f"📡 采集 {len(SUBREDDITS)} 个子版块...")
    all_posts = []

    for i, sub in enumerate(SUBREDDITS):
        result = fetch_subreddit(token, sub)
        if result["status"] == "ok" and result["posts"]:
            all_posts.extend(result["posts"])
            print(f"  [{i + 1:2d}/{len(SUBREDDITS)}] r/{sub:20s} → {len(result['posts'])}条 (↑{result['posts'][0]['score']})")
        elif i < 5:
            print(f"  [{i + 1:2d}/{len(SUBREDDITS)}] r/{sub:20s} → ⚠️")
        time.sleep(0.5)

    all_posts.sort(key=lambda p: p["score"], reverse=True)

    print(f"\n📊 共采集 {len(all_posts)} 条帖子")
    print("🏆 热门TOP 5:")
    for p in all_posts[:5]:
        print(f"    ↑{p['score']:>4} 💬{p['comments']:>3}  r/{p['subreddit']}  {p['title'][:60]}")

    output = {
        "date": today,
        "collected_at": now,
        "status": "ok",
        "total_posts": len(all_posts),
        "subreddits_checked": len(SUBREDDITS),
        "top_posts": all_posts[:10],
        "all_posts": all_posts,
    }
    filepath = os.path.join(OUTPUT_DIR, f"{today}.json")
    with open(filepath, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n💾 已保存: {filepath} ({os.path.getsize(filepath)} bytes)")


if __name__ == "__main__":
    main()
