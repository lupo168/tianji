#!/usr/bin/env python3
"""天玑 · ProductHunt新品采集器"""
import json, os, sys
from datetime import datetime

# 添加父目录到 path 以导入安全层
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from safe_requests import safe_get_raw

OUTPUT_DIR = os.path.expanduser("~/tianji-data/producthunt")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch():
    result = {"posts": []}
    try:
        query = '{"query":"{posts(first:10,order:VOTES){edges{node{id name tagline votesCount url}}}}"}'
        url = "https://api.producthunt.com/v2/api/graphql"
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        # ProductHunt GraphQL API via POST
        import urllib.request
        req = urllib.request.Request(url, data=query.encode(), headers=headers)
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
        edges = data.get("data", {}).get("posts", {}).get("edges", [])
        for e in edges:
            n = e["node"]
            result["posts"].append({"name": n["name"], "tagline": n.get("tagline", "")[:100], "votes": n["votesCount"], "url": n["url"]})
        result["status"] = "ok"
    except Exception as e:
        result["status"] = f"error: {str(e)[:80]}"
    return result

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"天玑 · ProductHunt新品 | {today}")
    d = fetch()
    if d["status"] == "ok":
        print(f"  ✅ {len(d['posts'])}个新产品")
        for p in d["posts"][:5]:
            print(f"    [{p['votes']}票] {p['name'][:30]} | {p['tagline'][:50]}")
    else:
        print(f"  ⚠️ {d['status']}")
    json.dump({"date":today,"data":d}, open(os.path.join(OUTPUT_DIR,f"{today}.json"),"w"),indent=2)
    print(f"  💾 saved")

if __name__ == "__main__":
    main()
