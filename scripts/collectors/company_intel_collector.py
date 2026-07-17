#!/usr/bin/env python3
"""天玑 · 公司/融资情报"""
import json, os, subprocess, sys
from datetime import datetime

OUTPUT_DIR = os.path.expanduser("~/tianji-data/companies")
os.makedirs(OUTPUT_DIR, exist_ok=True)

BRANDS = ["Petkit","PetSafe","PETLIBRO","Waterdrop","iSpring"]
AS = os.path.expanduser("~/.hermes/skills/anysearch/scripts/anysearch_cli.py")

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"天玑 · 公司/融资情报 | {today}")
    results = {}
    for b in BRANDS:
        try:
            r = subprocess.run([sys.executable, AS, "search", f"{b} funding raised 2026", "--max_results", "2"],
                capture_output=True, text=True, timeout=20)
            out = r.stdout.lower()
            found = b.lower() in out and ("fund" in out or "raises" in out)
            print(f"  {'💰' if found else '⚪'} {b}")
            results[b] = found
        except:
            results[b] = "timeout"
    json.dump({"date":today,"results":results}, open(os.path.join(OUTPUT_DIR,f"{today}.json"),"w"),indent=2)
    print(f"  💾 saved")

if __name__ == "__main__":
    main()
