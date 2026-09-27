"""Build the Admissions Hub concept prototype from the canonical record.

Injects ../canonical/admissions-canonical.json and hub-config.json into hub.src.html,
so the page never carries hand-typed values. Output: admissions-hub-prototype.html
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
canon = json.loads((HERE.parent / "canonical" / "admissions-canonical.json").read_text(encoding="utf-8"))
cfg = json.loads((HERE / "hub-config.json").read_text(encoding="utf-8"))
known = {r["id"] for r in canon}
refs = {f["canon"] for f in cfg["formulas"]} | {v["canon"] for m in cfg["minimums"].values() for v in m.values()} | set(cfg["faq_keywords"])
missing = refs - known
if missing:
    raise SystemExit(f"hub-config refers to unknown canonical records: {sorted(missing)}")
src = (HERE / "hub.src.html").read_text(encoding="utf-8")
dump = lambda o: json.dumps(o, ensure_ascii=False).replace("</", "<\\/")
out = src.replace("/*CANON*/null", dump(canon)).replace("/*CFG*/null", dump(cfg))
(HERE / "admissions-hub-prototype.html").write_text(out, encoding="utf-8-sig")
print(f"built admissions-hub-prototype.html ({len(out):,} chars, {len(canon)} canonical records)")
