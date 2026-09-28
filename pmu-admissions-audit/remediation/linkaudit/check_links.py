"""Read-only link check for the live Admissions Office hub.
Input: links.json (from extract.js). For every unique http(s) URL: GET with curl -L
(TLS verified against the environment CA bundle), record each redirect hop, the final
status, final URL and <title>. Hosts outside pmu.edu.sa are not reachable from this
environment and are recorded as "not tested". No forms, no logins, no POST.

Usage: python3 check_links.py links.json checks.json
"""
import concurrent.futures as cf
import json
import re
import subprocess
import sys
import tempfile
import urllib.parse
from datetime import datetime, timezone

UA = "PMU-Admissions-LinkAudit/1.0 (read-only)"


def reachable(url):
    h = urllib.parse.urlsplit(url).hostname or ""
    return url.startswith("https://") and (h == "pmu.edu.sa" or h.endswith(".pmu.edu.sa"))


def check(url):
    if not reachable(url):
        why = "http:// is refused by this environment's proxy" if url.startswith("http://") else "host outside pmu.edu.sa is not reachable from this environment"
        return {"url": url, "tested": False, "why": why}
    with tempfile.NamedTemporaryFile() as hdr, tempfile.NamedTemporaryFile() as body:
        p = subprocess.run(["curl", "-sS", "-L", "--max-redirs", "10", "-m", "60", "-A", UA, "-D", hdr.name, "-o", body.name,
                            "-w", "%{http_code} %{num_redirects} %{url_effective}", url], capture_output=True, text=True)
        hops, cur = [], url
        for line in open(hdr.name, encoding="latin-1").read().splitlines():
            if line.startswith("HTTP/") and "connection established" not in line.lower():
                hops.append({"url": cur, "status": int(line.split()[1]), "location": None})
            elif hops and line.lower().startswith("location:"):
                hops[-1]["location"] = line.split(":", 1)[1].strip()
                cur = urllib.parse.urljoin(cur, hops[-1]["location"])
        raw = open(body.name, "rb").read()
    parts = p.stdout.split(" ", 2)
    text = raw.decode("utf-8", "replace")
    m = re.search(r"<title[^>]*>(.*?)</title>", text, re.S | re.I)
    return {"url": url, "tested": True, "status": int(parts[0]) if parts[0].isdigit() else 0,
            "redirects": int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0,
            "final_url": parts[2] if len(parts) > 2 else None, "hops": hops, "bytes": len(raw),
            "title": re.sub(r"\s+", " ", m.group(1)).strip() if m else None,
            "error": p.stderr.strip()[:160] or None, "_text": text}


def main(links_path, checks_path):
    links = json.load(open(links_path, encoding="utf-8"))["desktop"]["links"]
    checks = json.load(open(checks_path, encoding="utf-8"))
    urls = sorted({l["abs"] for l in links if l["abs"].startswith("http")})
    with cf.ThreadPoolExecutor(8) as ex:
        res = dict(zip(urls, ex.map(check, urls)))
    # known issue strings (from the G3 verifier's checks.json) found on each target
    # the 2021/22 calendar link sits in the site-wide footer, so it is reported once (footer row), not per page
    needles = [(c["finding"], c["text"]) for c in checks.get("forbidden", []) if c.get("text") and c["text"] != "academic_calendar_2021_2022"]
    for r in res.values():
        t = r.pop("_text", "")
        r["issue_strings"] = [{"finding": f, "text": n} for f, n in dict.fromkeys(needles) if n in t]
    out = {"run_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "user_agent": UA, "results": res}
    json.dump(out, open("checks-result.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    tested = [r for r in res.values() if r["tested"]]
    print(len(urls), "unique;", len(tested), "tested;",
          sum(r["status"] == 200 for r in tested), "final 200;", sum(r["redirects"] > 0 for r in tested), "redirected")
    for r in tested:
        if r["status"] != 200 or r["error"]:
            print("  !", r["status"], r["url"], r["error"])


if __name__ == "__main__":
    main(*sys.argv[1:])
