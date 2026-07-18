#!/usr/bin/env python3
"""天玑 · Etsy 竞品情报采集器

数据源: Etsy Open API v3
费用: 免费 (需注册 Etsy App)
接入: https://www.etsy.com/developers

用法:
  python etsy_collector.py --keyword "pet water fountain" --limit 20
  python etsy_collector.py --shop-id 123456 --limit 10
  python etsy_collector.py --keyword "separation anxiety" --price-min 5 --price-max 50

配置:
  在 ~/.hermes/secrets/ecommerce.json 添加:
    {"etsy": {"api_key": "你的keystring"}}
  或设置环境变量: TIANJI_ETSY_API_KEY=你的key

数据输出: ~/tianji-data/etsy/
"""

import json, os, sys, time, argparse
from datetime import datetime
from urllib.parse import quote

# 添加父目录到 path 以导入安全层
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from safe_requests import safe_get
from env_loader import load_key

BASE = "https://openapi.etsy.com/v3"
OUTPUT_DIR = os.path.expanduser("~/tianji-data/etsy")
os.makedirs(os.path.join(OUTPUT_DIR, "search"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "shops"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "listings"), exist_ok=True)

API_KEY = None


def etsy_get(path, params=None):
    """Etsy API 调用，走天玑安全层"""
    if not API_KEY:
        return None
    url = f"{BASE}{path}"
    if params:
        parts = []
        for k, v in params.items():
            if v is not None:
                parts.append(f"{k}={quote(str(v), safe='')}")
        if parts:
            url += "?" + "&".join(parts)
    return safe_get(url, headers={"x-api-key": API_KEY})


# ---------- 采集函数 ----------

def search_listings(keyword, limit=20, offset=0, min_price=None, max_price=None):
    params = {
        "keywords": keyword,
        "limit": min(limit, 100),
        "offset": offset,
        "sort_on": "score",
        "sort_order": "down",
    }
    if min_price is not None:
        params["min_price"] = min_price
    if max_price is not None:
        params["max_price"] = max_price
    return etsy_get("/application/listings/active", params)


def get_shop_listings(shop_id, limit=20, offset=0):
    return etsy_get(
        f"/application/shops/{shop_id}/listings/active",
        {"limit": min(limit, 100), "offset": offset},
    )


def get_shop_info(shop_id):
    return etsy_get(f"/application/shops/{shop_id}")


def get_shop_reviews(shop_id, limit=20, offset=0):
    return etsy_get(
        f"/application/shops/{shop_id}/reviews",
        {"limit": min(limit, 100), "offset": offset},
    )


# ---------- 分析函数 ----------
def analyze_prices(results):
    """分析搜索结果的价格分布"""
    prices = []
    for r in results:
        p = parse_price(r.get("price", {}))
        if p > 0:
            prices.append(p)
    if not prices:
        return {}
    return {
        "avg": round(sum(prices) / len(prices), 2),
        "min": min(prices),
        "max": max(prices),
        "median": sorted(prices)[len(prices) // 2],
        "count": len(prices),
    }


def analyze_tags(results):
    tag_count = {}
    for r in results:
        for t in r.get("tags", []):
            tag_count[t] = tag_count.get(t, 0) + 1
    return sorted(tag_count.items(), key=lambda x: -x[1])[:20]


# ---------- 序列化辅助 ----------

def parse_price(price_obj):
    """Etsy API price: {amount, divisor, currency_code} → 实际金额"""
    if isinstance(price_obj, dict):
        amount = float(price_obj.get("amount", 0))
        divisor = float(price_obj.get("divisor", 100))
        return round(amount / divisor, 2)
    if isinstance(price_obj, (int, float)):
        return float(price_obj)
    return 0

def parse_currency(price_obj):
    if isinstance(price_obj, dict):
        return price_obj.get("currency_code")
    return None

def serialize_listing(r):
    """提取 Etsy 商品关键字段"""
    price_obj = r.get("price", {})
    return {
        "title": (r.get("title") or "")[:120],
        "listing_id": r.get("listing_id"),
        "shop_id": r.get("shop_id"),
        "price": parse_price(price_obj),
        "currency": parse_currency(price_obj),
        "url": r.get("url"),
        "tags": r.get("tags", [])[:10],
        "review_count": r.get("reviews_count", 0),
        "rating": r.get("rating"),
        "num_favorers": r.get("num_favorers", 0),
    }


# ---------- 主流程 ----------

def main():
    global API_KEY

    parser = argparse.ArgumentParser(description="天玑 · Etsy 竞品情报采集器")
    parser.add_argument("--keyword", help="搜索关键词")
    parser.add_argument("--shop-id", type=int, help="目标店铺数字ID")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--price-min", type=float)
    parser.add_argument("--price-max", type=float)
    parser.add_argument("--reviews", action="store_true", help="同时获取评价")
    parser.add_argument("--api-key", help="直接传 Etsy API key（优先级最高）")
    args = parser.parse_args()

    today = datetime.now().strftime("%Y-%m-%d")

    # 加载 API key
    API_KEY = args.api_key or load_key("etsy_api_key")
    if not API_KEY:
        print("⏳ Etsy API 未配置")
        print()
        print("  要启用 Etsy 采集器：")
        print("    1. 打开 https://www.etsy.com/developers")
        print("    2. 创建 App → 获取 keystring")
        print("    3. 配置到 ~/.hermes/secrets/ecommerce.json:")
        print('       {"etsy": {"api_key": "你的keystring"}}')
        print("    或设置环境变量: TIANJI_ETSY_API_KEY=你的key")
        output = {"date": today, "status": "skipped", "reason": "no api key"}
        path = os.path.join(OUTPUT_DIR, "search", f"{today}.json")
        with open(path, "w") as f:
            json.dump(output, f, indent=2)
        print(f"\n💾 状态已保存: {path}")
        return

    print(f"天玑 · Etsy 采集器 | {today}")
    print("=" * 50)

    if args.shop_id:
        _run_shop_mode(args, today)
    elif args.keyword:
        _run_search_mode(args, today)
    else:
        _run_default_search(today)


def _run_search_mode(args, today):
    print(f"\n🔍 搜索: '{args.keyword}'")
    data = search_listings(args.keyword, args.limit, 0, args.price_min, args.price_max)

    if data is None:
        print("  ❌ API 未配置")
        return
    if "error" in data:
        print(f"  ❌ {data['error']}")
        return

    results = data.get("results", [])
    count = data.get("count", len(results))
    print(f"  ✅ 关键词 '{args.keyword}': {count} 条结果")

    prices = analyze_prices(results)
    if prices:
        print(f"     价格: ${prices['avg']} avg | ${prices['min']}-${prices['max']}")

    tags = analyze_tags(results)
    if tags:
        top5 = ", ".join(f"{t}({c})" for t, c in tags[:5])
        print(f"     热门标签: {top5}")

    # 序列化输出
    listings = [serialize_listing(r) for r in results[:args.limit]]
    output = {
        "date": today,
        "collected_at": datetime.now().isoformat(),
        "source": "etsy",
        "keyword": args.keyword,
        "total_results": count,
        "price_stats": prices,
        "top_tags": [{"tag": t, "count": c} for t, c in tags[:10]],
        "listings": listings,
    }
    fname = f"search_{args.keyword[:30].replace(' ', '_')}_{today}"
    path = os.path.join(OUTPUT_DIR, "search", f"{fname}.json")
    with open(path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n💾 已保存: {path}")


def _run_shop_mode(args, today):
    sid = args.shop_id
    print(f"\n🏪 店铺 ID: {sid}")

    shop = get_shop_info(sid)
    if shop and "shop_name" in shop:
        print(f"   店铺: {shop.get('shop_name')}")
        print(f"   标题: {shop.get('title', 'N/A')}")
        print(f"   货币: {shop.get('currency_code', 'N/A')}")

    listings_data = get_shop_listings(sid, args.limit)
    if listings_data and "results" in listings_data:
        results = listings_data["results"]
        print(f"  ✅ 商品列表: {len(results)} 条")
        for r in results[:5]:
            title = (r.get("title") or "?")[:60]
            disp_price = parse_price(r.get("price", {}))
            print(f"    📄 {title} | ${disp_price}")

        shop_listings = [serialize_listing(r) for r in results]
        output = {
            "date": today,
            "collected_at": datetime.now().isoformat(),
            "source": "etsy",
            "shop_id": sid,
            "shop_name": shop.get("shop_name") if shop else None,
            "listing_count": len(results),
            "listings": shop_listings,
        }
        path = os.path.join(OUTPUT_DIR, "shops", f"shop_{sid}_{today}.json")
        with open(path, "w") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"\n💾 已保存: {path}")

    if args.reviews:
        reviews = get_shop_reviews(sid, args.limit)
        if reviews and "results" in reviews:
            print(f"  ✅ 评价: {len(reviews['results'])} 条")


def _run_default_search(today):
    """默认采集：宠物饮水机 + 训犬产品"""
    default_keywords = [
        "pet water fountain",
        "dog training guide",
        "pet drinking fountain",
        "dog separation anxiety",
    ]
    all_results = []
    for kw in default_keywords:
        data = search_listings(kw, limit=10)
        if data and "results" in data:
            all_results.extend([serialize_listing(r) for r in data["results"]])
            print(f"  ✅ '{kw}': {len(data['results'])} 条")
        else:
            err = data.get("error", "no response") if data else "no response"
            print(f"  ⚠️ '{kw}': {err}")
        time.sleep(0.3)

    print(f"\n📊 共 {len(all_results)} 条商品")

    output = {
        "date": today,
        "collected_at": datetime.now().isoformat(),
        "source": "etsy",
        "mode": "default_search",
        "total": len(all_results),
        "listings": all_results,
    }
    path = os.path.join(OUTPUT_DIR, "search", f"default_{today}.json")
    with open(path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n💾 已保存: {path}")


if __name__ == "__main__":
    main()
