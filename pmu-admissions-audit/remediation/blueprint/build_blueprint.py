"""Build the UX / IA Blueprint from ia.json, the canonical record and hub-config.json.
Fails loudly if the data is inconsistent, so the blueprint can never drift from its sources.
Output: ../../PMU-Admissions-UX-IA-Blueprint.html (doctype, UTF-8 charset, lang, BOM)."""
import json, pathlib, itertools

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
canon = json.loads((HERE.parent / "canonical" / "admissions-canonical.json").read_text(encoding="utf-8"))
cfg = json.loads((HERE.parent / "hub" / "hub-config.json").read_text(encoding="utf-8"))
ia = json.loads((HERE / "ia.json").read_text(encoding="utf-8"))

known = {r["id"] for r in canon}
nodes = {n["id"] for n in ia["sitemap"]}
errors = []
for n in ia["sitemap"]:
    if n["parent"] and n["parent"] not in nodes: errors.append(f"sitemap {n['id']}: unknown parent {n['parent']}")
    errors += [f"sitemap {n['id']}: unknown field {f}" for f in n["feeds"] if f not in known]
for x in ia["legacy"]:
    if x["to"] not in nodes: errors.append(f"legacy {x['label']}: unknown target {x['to']}")
for c in ia["components"]:
    errors += [f"component {c['id']}: unknown field {f}" for f in c["fields"] if f not in known]
    errors += [f"component {c['id']}: unknown page {w}" for w in c["where"] if w not in nodes]
for r in ia["routes"]:
    if r["node"] not in nodes: errors.append(f"route {r['id']}: unknown node")
for s in ia["stages"]:
    errors += [f"stage {s['id']}: unknown field {f}" for f in s["feeds"] if f not in known]
    if s["touch"] != "route" and s["touch"] not in nodes: errors.append(f"stage {s['id']}: unknown page")
for p, st in ia["pain"].items():
    if p not in {r["id"] for r in ia["routes"]}: errors.append(f"pain: unknown persona {p}")
    if set(st) != {s["id"] for s in ia["stages"]}: errors.append(f"pain {p}: stages incomplete")
for r in ia["rules"]:
    if r["channel"] and r["channel"] not in ia["channels"]: errors.append(f"rule {r['id']}: unknown channel")
# every combination of answers must resolve to exactly one most-specific rule
qs = {q["id"]: [o[0] for o in q["opts"]] for q in ia["questions"]}
def applicable(ans):
    return [q for q in ia["questions"] if q["id"] not in ans and all(ans.get(k) == v for k, v in (q.get("when") or {}).items())]
def walk(ans):
    nxt = applicable(ans)
    if not nxt:
        m = [r for r in ia["rules"] if all(ans.get(k) == v for k, v in r["when"].items())]
        top = max((len(r["when"]) for r in m), default=0)
        best = [r for r in m if len(r["when"]) == top]
        if len(best) != 1: errors.append(f"routing: answers {ans} match {len(best)} rules")
        return
    q = nxt[0]
    for v in qs[q["id"]]: walk({**ans, q["id"]: v})
walk({})
if len(ia["legacy"]) != 36: errors.append(f"legacy map has {len(ia['legacy'])} links; the live hub has 36")
if errors: raise SystemExit("blueprint data errors:\n  " + "\n  ".join(errors))

dump = lambda o: json.dumps(o, ensure_ascii=False).replace("</", "<\\/")
src = (HERE / "blueprint.src.html").read_text(encoding="utf-8")
out = src.replace("/*CANON*/null", dump(canon)).replace("/*CFG*/null", dump(cfg)).replace("/*IA*/null", dump(ia))
head = '<!doctype html>\n<html lang="ar" dir="rtl">\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
(ROOT / "PMU-Admissions-UX-IA-Blueprint.html").write_text(head + out + "\n</html>\n", encoding="utf-8-sig")
print(f"built PMU-Admissions-UX-IA-Blueprint.html: {len(ia['sitemap'])} pages, {len(ia['legacy'])} legacy links, {len(ia['rules'])} rules; data checks passed")
