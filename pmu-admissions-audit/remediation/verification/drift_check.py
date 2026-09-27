"""Closure Gate G3 verifier: re-crawl admissions surfaces and prove zero drift.

Usage
  python3 drift_check.py                       # live fetch (needs network access to pmu.edu.sa)
  python3 drift_check.py --fixtures DIR        # offline: DIR/<page_key>.txt holds page text
  python3 drift_check.py --out report          # writes report.md and report.json

Exit code 0 = G3 PASS (no forbidden text, no contradictions, every consistency
group has exactly one value and matches the approved canonical value if set).
Exit code 1 = G3 NOT MET. Pages that cannot be fetched count as NOT MET: a gate
that cannot be proven is not passed.
"""
import argparse
import html
import json
import pathlib
import re
import sys
import urllib.request

HERE = pathlib.Path(__file__).parent
CANONICAL = HERE.parent / "canonical" / "admissions-canonical.json"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "PMU-Admissions-G3-Verifier/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return html_to_text(r.read().decode("utf-8", "replace"))


def html_to_text(raw):
    # keep href/src targets in either quote style (links and embedded files are
    # checked too), drop scripts/styles, strip tags
    raw = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", raw)
    refs = " ".join(m[1] for m in re.findall(r"""(?i)\b(?:href|src)\s*=\s*(["'])(.*?)\1""", raw))
    text = html.unescape(re.sub(r"(?s)<[^>]+>", " ", raw))
    return re.sub(r"\s+", " ", text) + " " + refs


def load_pages(cfg, fixtures):
    pages, errors = {}, {}
    for key, url in cfg["pages"].items():
        try:
            if fixtures:
                f = pathlib.Path(fixtures) / f"{key}.txt"
                if not f.exists():
                    continue
                pages[key] = re.sub(r"\s+", " ", f.read_text(encoding="utf-8"))
            else:
                pages[key] = fetch(url)
        except Exception as e:  # network or HTTP error -> unprovable
            errors[key] = f"{type(e).__name__}: {e}"
    return pages, errors


def approved_values():
    if not CANONICAL.exists():
        return {}
    out = {}
    for rec in json.loads(CANONICAL.read_text(encoding="utf-8")):
        if rec.get("approved_value") and isinstance(rec.get("expected"), dict):
            out.update({f"{rec['id']}.{k}": str(v) for k, v in rec["expected"].items()})
    return out


def run(cfg, pages, errors):
    issues = []
    for c in cfg["forbidden"]:
        t = pages.get(c["page"])
        if t is not None and c["text"] in t:
            issues.append({"type": "forbidden", "finding": c["finding"], "page": c["page"],
                           "detail": f"still contains: {c['text']!r}"})
    for c in cfg["contradiction"]:
        t = pages.get(c["page"])
        if t is not None and c["a"] in t and c["b"] in t:
            issues.append({"type": "contradiction", "finding": c["finding"], "page": c["page"],
                           "detail": f"contains both {c['a']!r} and {c['b']!r}"})
    expected = approved_values()
    groups = []
    for g in cfg["consistency"]:
        found = {}
        for p in g["pages"]:
            if p in pages:
                vals = sorted(set(v.replace(",", "") for v in re.findall(g["regex"], pages[p])))
                if vals:
                    found[p] = vals
        distinct = sorted({v for vs in found.values() for v in vs})
        exp = expected.get(g["rule"])
        ok = len(distinct) <= 1 and (exp is None or distinct in ([], [exp]))
        groups.append({"rule": g["rule"], "finding": g["finding"], "values_by_page": found,
                       "distinct": distinct, "expected": exp, "ok": ok})
        if not ok:
            issues.append({"type": "conflict", "finding": g["finding"], "page": ",".join(found),
                           "detail": f"{g['rule']}: {distinct}" + (f" (expected {exp})" if exp else "")})
    for k, e in errors.items():
        issues.append({"type": "unverifiable", "finding": "G3", "page": k, "detail": e})
    return issues, groups


def report(issues, groups, pages, errors, out):
    verdict = "PASS" if not issues else "NOT MET"
    md = [f"# Gate G3 — Surface conformance: **{verdict}**", "",
          f"Pages checked: {len(pages)} · unreachable: {len(errors)} · issues: {len(issues)}", "",
          "| Type | Finding | Page(s) | Detail |", "|---|---|---|---|"]
    md += [f"| {i['type']} | {i['finding']} | {i['page']} | {i['detail']} |" for i in issues] or ["| — | — | — | none |"]
    md += ["", "## Consistency groups", "", "| Rule | Values by page | Expected | OK |", "|---|---|---|---|"]
    for g in groups:
        md.append(f"| {g['rule']} | {json.dumps(g['values_by_page'])} | {g['expected'] or '(pending decision)'} | {'yes' if g['ok'] else 'NO'} |")
    if out:
        pathlib.Path(f"{out}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
        pathlib.Path(f"{out}.json").write_text(json.dumps(
            {"verdict": verdict, "issues": issues, "groups": groups}, ensure_ascii=False, indent=2), encoding="utf-8")
    return verdict, "\n".join(md)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixtures")
    ap.add_argument("--out")
    ap.add_argument("--config", default=str(HERE / "checks.json"))
    a = ap.parse_args(argv)
    cfg = json.loads(pathlib.Path(a.config).read_text(encoding="utf-8"))
    pages, errors = load_pages(cfg, a.fixtures)
    issues, groups = run(cfg, pages, errors)
    verdict, md = report(issues, groups, pages, errors, a.out)
    print(md)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
