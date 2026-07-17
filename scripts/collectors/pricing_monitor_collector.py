#!/usr/bin/env python3
"""天玑 · 竞品定价监控"""
import json, os, subprocess, sys, re
from datetime import datetime

OUTPUT_DIR = os.path.expanduser("~/tianji-data/pricing")
os.makedirs(OUTPUT_DIR, exist_ok=True)

PRODUCTS = [
    ("Petkit","Eversweet Solo SE"),
    ("PETLIBRO","Dockstream"),
    ("Waterdrop","10UA filter"),
    ("iSpring","RCC7AK"),
]
AS = os.path.expanduser("~/.hermes/skills/anysearch/scripts/anysearch_cli.py")

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"天玑 · 竞品定价 | {today}")
    results = []
    for brand, prod in PRODUCTS:
        try:
            r = subprocess.run([sys.executable, AS, "search", f"{brand} {prod} price 2026", "--max_results", "2"],
                capture_output=True, text=True, timeout=20)
            prices = re.findall(r'\$(\d+[\.]?\d{0,2})', r.stdout)
            p = prices[0] if prices else "?"
            print(f"  {'✅' if prices else '⚪'} {brand} {prod}: ${p}")
            results.append({"brand":brand, "product":prod, "price":p})
        except:
            results.append({"brand":brand, "product":prod, "price":"err"})
    json.dump({"date":today,"data":results}, open(os.path.join(OUTPUT_DIR,f"{today}.json"),"w"),indent=2)
    print(f"  💾 saved")

if __name__ == "__main__":
    main()
