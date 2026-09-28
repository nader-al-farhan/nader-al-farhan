"""Derive shot-jobs.json (one screenshot per quoted observation) from content_findings.py. Run from ../"""
import json, sys
sys.path.insert(0, "content")
from content_findings import PAGES
ids = {x["id"]: x["abs"] for x in json.load(open("ids.json"))}
jobs = [{"id": k, "n": n, "url": ids[k], "quotes": i[2], "sev": i[0]}
        for k, p in PAGES.items() for n, i in enumerate(p["issues"], 1) if i[2] and k not in ("C04", "C06", "C08")]
json.dump(jobs, open("content/shot-jobs.json", "w"), ensure_ascii=False)
print(len(jobs), "jobs")
