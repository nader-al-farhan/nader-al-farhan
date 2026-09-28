"""Export everything the English Word/PDF report needs into report-en-data.json (single source:
content_findings.py + content_findings_en.py + registers/findings-register.md + ia.json)."""
import json, pathlib, re
from collections import Counter
import content_findings as A, content_findings_en as B
H = pathlib.Path(__file__).parent
ROOT = H / "../../.."
T = json.loads((H / "texts.json").read_text(encoding="utf-8"))
SH = json.loads((H / "shots.json").read_text(encoding="utf-8"))
ids = [x for x in json.loads((H / "../ids.json").read_text(encoding="utf-8")) if x["id"].startswith("C")]
L = json.loads((H / "../links.json").read_text(encoding="utf-8"))["desktop"]["links"]
ia = json.loads((ROOT / "remediation/blueprint/ia.json").read_text(encoding="utf-8"))
reg = (ROOT / "registers/findings-register.md").read_text(encoding="utf-8")
cols = ["id", "severity", "type", "finding", "where", "current", "conflicting", "screenshot", "impact", "treatment", "owner"]
F = {}
for line in reg.splitlines():
    m = re.match(r"\| (F-\d\d) \|", line)
    if m:
        cells = [c.strip() for c in line.strip().strip("|").split(" | ")]
        if len(cells) == 11:
            F[m.group(1)] = dict(zip(cols, cells))
clean = lambda s: re.sub(r"\*\*|`", "", s)
for f in F.values():
    for k in f: f[k] = clean(f[k])
assert len(F) == 45, len(F)
norm = lambda s: re.sub(r"\s+", " ", s.replace("’", "'").replace("–", "-")).strip()
links = []
for k_, x in enumerate(ids):
    k = x["id"]; p = A.PAGES[k]; lg = ia["legacy"][k_]
    obs = []
    for n, i in enumerate(p["issues"], 1):
        for q in i[2]: assert norm(q) in norm(T[k]["text"]), (k, q)
        note, action = B.ISSUES[(k, n)]
        obs.append({"n": n, "sev": i[0], "kind": B.KIND[i[1]], "quotes": i[2], "note": note, "action": action, "ref": i[5],
                    "shot": SH.get(f"{k}-{n}", {}).get("shot"), "spelling": B.SPELLING.get((k, n), [])})
    links.append({"id": k, "label": L[x["i"]]["text"], "group": L[x["i"]]["heading"], "url": T[k].get("final") or x["abs"],
                  "purpose": B.PURPOSE[k], "data": B.DATA[k], "verified": B.VERIFIED.get(k, []),
                  "dest": {"id": lg["to"], "title": B.SITEMAP_EN[lg["to"]], "path": next(n["path"] for n in ia["sitemap"] if n["id"] == lg["to"])}, "obs": obs})
allobs = [o for l in links for o in l["obs"]]
sev = Counter(o["sev"] for o in allobs)
refs = sorted({o["ref"] for o in allobs}, key=lambda r: int(r[2:]))
data = {"date": "28 September 2026", "hub": "https://pmu.edu.sa/admission/admission",
        "summary": {"links": 36, "obs": len(allobs), "H": sev["H"], "M": sev["M"], "L": sev["L"], "quotes": sum(len(o["quotes"]) for o in allobs),
                    "shots": sum(1 for o in allobs if o["shot"]), "new_findings": 15, "register_total": 45},
        "links": links, "matrix": [{"topic": t, "values": v, "sev": A.MATRIX[i][2], "ref": A.MATRIX[i][3]} for i, (t, v) in enumerate(B.MATRIX)],
        "register": {r: F[r] for r in refs}, "new": [F[f"F-{n}"] for n in range(31, 46)],
        "sitemap": [{"id": n["id"], "title": B.SITEMAP_EN[n["id"]], "path": n["path"], "links": [l["id"] for l in links if l["dest"]["id"] == n["id"]]} for n in ia["sitemap"]],
        "sources": [
            ("X01", "ETS — TOEFL iBT score scale update (1–6 band scale from 21 January 2026)", "https://www.ets.org/toefl/institutions/ibt/score-scale-update.html"),
            ("X06", "College Board — SAT Subject Tests discontinued (January 2021)", "https://blog.collegeboard.org/what-were-sat-subject-tests"),
            ("X09", "University of Arizona CESL — Graduate English Endorsement ('for UA admission only')", "https://cesl.arizona.edu/endorsement"),
            ("X10", "AACSB — The value of accreditation (fewer than 6% of business schools)", "https://www.aacsb.edu/educators/accreditation/value-of-accreditation")]}
(H / "report-en-data.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(data["summary"]), len(data["register"]), "register rows referenced")
