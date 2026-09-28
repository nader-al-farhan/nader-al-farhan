"""Content audit report for the 36 links on the live Admissions Office page.
Inputs: content_findings.py (observations), texts.json (live text, extract_text.js),
shots.json (evidence screenshots), ../ids.json + ../links.json (link order and groups),
../../blueprint/ia.json (the 17 proposed pages). Fails if any quote is not verbatim."""
import base64
import html
import io
import json
import pathlib
import re
from collections import Counter, defaultdict
from PIL import Image
from content_findings import PAGES, MATRIX, CORRECTIONS

H = pathlib.Path(__file__).parent
GH = "https://github.com/nader-al-farhan/nader-al-farhan/blob/claude/pmu-admissions-audit-jm54d8/pmu-admissions-audit/remediation/linkaudit/"
T = json.loads((H / "texts.json").read_text(encoding="utf-8"))
SH = json.loads((H / "shots.json").read_text(encoding="utf-8"))
ids = [x for x in json.loads((H / "../ids.json").read_text(encoding="utf-8")) if x["id"].startswith("C")]
L = json.loads((H / "../links.json").read_text(encoding="utf-8"))["desktop"]["links"]
ia = json.loads((H / "../../blueprint/ia.json").read_text(encoding="utf-8"))
SITE = {n["id"]: n for n in ia["sitemap"]}
assert len(ids) == 36 and len(ia["legacy"]) == 36
LEG = {x["id"]: ia["legacy"][k] for k, x in enumerate(ids)}  # same order as the live page
SEV = {"H": "عالية", "M": "متوسطة", "L": "منخفضة"}
KIND = {"conflict": "تعارض بين الصفحات", "error": "معلومة خاطئة", "gap": "معلومة ناقصة", "stale": "متقادم", "wording": "صياغة/لغة", "claim": "ادعاء يحتاج تحقق"}
GROUP_AR = {"Future Students": "الطلاب الجدد", "International Students’ Office": "مكتب الطلاب الدوليين", "Graduate Admissions": "الدراسات العليا",
            "Undergraduate Admissions": "البكالوريوس", "Undergraduate Placement Tests": "اختبارات تحديد المستوى"}

norm = lambda s: re.sub(r"\s+", " ", s.replace("’", "'").replace("–", "-")).strip()
missing = [(k, q) for k, p in PAGES.items() for i in p["issues"] for q in i[2] if norm(q) not in norm(T.get(k, {}).get("text", ""))]
assert not missing, missing
assert set(PAGES) == {x["id"] for x in ids}, set(x["id"] for x in ids) ^ set(PAGES)

issues = [(k, n, i) for k, p in PAGES.items() for n, i in enumerate(p["issues"], 1)]
sevc = Counter(i[0] for _, _, i in issues)
newc = sum(1 for _, _, i in issues if i[5] == "NEW")
refs = sorted({i[5] for _, _, i in issues if i[5] != "NEW"}, key=lambda r: int(r[2:]))
quotes = sum(len(i[2]) for _, _, i in issues)
run_at = "2026-09-28"

rows = []
for x in ids:
    k = x["id"]; p = PAGES[k]; lg = LEG[k]
    rows.append({"id": k, "label": L[x["i"]]["text"], "group": L[x["i"]]["heading"], "url": x["abs"], "final_url": T[k].get("final"),
                 "purpose": p["purpose"], "key_data": p["data"], "verified": p.get("verified", []),
                 "proposed_page": {"id": lg["to"], "title": SITE[lg["to"]]["t"]["ar"], "path": SITE[lg["to"]]["path"], "action": lg["action"]},
                 "issues": [{"n": n, "severity": i[0], "kind": i[1], "quotes": i[2], "note": i[3], "action": i[4], "ref": i[5],
                             "screenshot": SH.get(f"{k}-{n}", {}).get("shot")} for n, i in enumerate(p["issues"], 1)]})
(H / "content-audit-2026-09-28.json").write_text(json.dumps({"scope": "content only — 36 links on https://pmu.edu.sa/admission/admission", "run_at": run_at,
    "summary": {"links": 36, "issues": len(issues), "severity": {SEV[s]: c for s, c in sevc.items()}, "new": newc, "existing_refs": refs, "verbatim_quotes": quotes},
    "matrix": [{"topic": t, "values": [{"where": w, "value": v} for w, v in vals], "severity": s, "ref": r} for t, vals, s, r in MATRIX],
    "corrections": [{"finding": f, "note": n} for f, n in CORRECTIONS], "links": rows}, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------- HTML ----------
e = html.escape
def ltr(s): return f'<bdi dir="ltr">{e(s)}</bdi>'
def iso(s):
    """escape, isolate Latin runs as LTR, then isolate «quoted» spans — so RTL does not reorder them"""
    s = html.escape(s, quote=False)
    s = re.sub(r"(?<![&\w])[A-Za-z][A-Za-z0-9 .,&;()/'’\-–:%]*[A-Za-z0-9)%]", lambda m: f'<bdi dir="ltr">{m.group(0)}</bdi>', s)
    return re.sub(r"«([^»<]*(?:<bdi[^>]*>[^<]*</bdi>[^»<]*)*)»", r"«<bdi>\1</bdi>»", s)
def thumb(path, w=420):
    im = Image.open(H / ".." / path).convert("RGB"); im.thumbnail((w, 330))
    b = io.BytesIO(); im.save(b, "JPEG", quality=62); return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()

def issue_html(k, it):
    q = "".join(f'<blockquote dir="ltr" lang="en">{e(s)}</blockquote>' for s in it["quotes"])
    ref = '<span class="tag new">جديد — مقترح</span>' if it["ref"] == "NEW" else f'<span class="tag ref">{it["ref"]}</span>'
    sh = ""
    if it["screenshot"]:
        sh = f'<a class="ev" href="{GH}{it["screenshot"]}" target="_blank" rel="noopener"><img loading="lazy" alt="دليل {k}-{it["n"]}" src="{thumb(it["screenshot"])}"><span>الدليل مظلّل — اضغط للحجم الكامل</span></a>'
    return f'''<div class="iss s{it["severity"]}"><div class="ih"><span class="sev">{SEV[it["severity"]]}</span><span class="kind">{KIND[it["kind"]]}</span>{ref}</div>
<p>{iso(it["note"])}</p>{q}<p class="act"><b>المعالجة:</b> {iso(it["action"])}</p>{sh}</div>'''

groups = defaultdict(list)
for r in rows: groups[r["group"]].append(r)
cards = []
for g, rs in groups.items():
    cards.append(f'<h3 class="grp">{e(GROUP_AR.get(g, g))} <bdi dir="ltr" class="en">{e(g)}</bdi> <span class="cnt">({len(rs)})</span></h3>')
    for r in rs:
        worst = min((i["severity"] for i in r["issues"]), key="HML".index, default=None)
        data = "".join(f"<li>{iso(d)}</li>" for d in r["key_data"])
        ver = "".join(f'<li class="ok">✓ {iso(v)}</li>' for v in r["verified"])
        body = "".join(issue_html(r["id"], it) for it in r["issues"]) or '<p class="ok">لا ملاحظات على المحتوى.</p>'
        cards.append(f'''<details class="card w{worst or 'ok'}" id="{r["id"]}" data-sev="{worst or 'ok'}"{' open' if worst == 'H' else ''}>
<summary><span class="id">{r["id"]}</span><span class="lb">{ltr(r["label"])}</span><span class="pill">{len(r["issues"])} ملاحظة</span>{f'<span class="dot s{worst}">{SEV[worst]}</span>' if worst else '<span class="dot ok">سليم</span>'}</summary>
<div class="meta2"><a href="{e(r["url"])}" target="_blank" rel="noopener">{ltr(r["final_url"] or r["url"])}</a> · يصبح في الهيكل المقترح: <b>{e(r["proposed_page"]["title"])}</b> {ltr(r["proposed_page"]["path"])}</div>
<p><b>الغرض:</b> {iso(r["purpose"])}</p><ul class="kd">{data}{ver}</ul>{body}</details>''')

mx = "".join(f'<tr class="s{s}"><td><b>{e(t)}</b><div class="ref">{e(r)}</div></td><td><ul>' + "".join(f"<li><b>{iso(w)}:</b> {iso(v)}</li>" for w, v in vals) + f'</ul></td><td class="sv">{SEV[s]}</td></tr>' for t, vals, s, r in MATRIX)
top = [(k, n, i) for k, n, i in issues if i[0] == "H"]
toph = "".join(f'<li><a href="#{k}">{k}</a> — {iso(i[3])}</li>' for k, n, i in top)
m17 = defaultdict(list)
for r in rows: m17[r["proposed_page"]["id"]].append(r)
t17 = "".join(f'<tr><td><b>{e(n["t"]["ar"])}</b><div class="u">{ltr(n["path"])}</div></td><td>' + (" ".join(f'<a href="#{r["id"]}">{r["id"]}</a>' for r in m17.get(n["id"], [])) or '<span class="mut">صفحة جديدة (لا مصدر حالي)</span>') + f'</td><td>{sum(len(r["issues"]) for r in m17.get(n["id"], []))}</td><td>{sum(1 for r in m17.get(n["id"], []) for i in r["issues"] if i["severity"] == "H")}</td></tr>' for n in ia["sitemap"])
corr = "".join(f'<p><b>{f}:</b> {iso(n)}</p>' for f, n in CORRECTIONS)

page = f'''<!doctype html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>تدقيق محتوى صفحة القبول</title>
<style>
:root{{--bg:#f5f6fa;--card:#fff;--ink:#1b2033;--mut:#5b6275;--line:#dfe3ec;--H:#c62828;--M:#d97706;--L:#2f6db5;--ok:#2e7d32;--nav:#16325c;--q:#f3f5fa}}
@media (prefers-color-scheme:dark){{:root:not([data-theme=light]){{--bg:#11131a;--card:#1a1d27;--ink:#e8eaf2;--mut:#a3a9ba;--line:#2c3140;--q:#232735}}}}
:root[data-theme=dark]{{--bg:#11131a;--card:#1a1d27;--ink:#e8eaf2;--mut:#a3a9ba;--line:#2c3140;--q:#232735}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15.5px/1.75 "Segoe UI",Tahoma,"Noto Naskh Arabic",Arial,sans-serif}}
.wrap{{max-width:1100px;margin:auto;padding:24px 16px 64px}}a{{color:var(--nav)}}
h1{{font-size:1.65rem;margin:.1em 0 .2em}}h2{{font-size:1.25rem;margin:2em 0 .7em;border-inline-start:4px solid var(--nav);padding-inline-start:10px}}
.mut,.meta{{color:var(--mut);font-size:.9rem}}
.scope{{background:var(--card);border:1px solid var(--line);border-inline-start:4px solid var(--nav);border-radius:10px;padding:12px 16px}}
.kpi{{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px;margin:16px 0}}.kpi div{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px}}
.kpi b{{display:block;font-size:1.55rem}}.kpi span{{color:var(--mut);font-size:.85rem}}
.tw{{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:12px}}
table{{border-collapse:collapse;width:100%;font-size:.9rem}}th,td{{border-bottom:1px solid var(--line);padding:9px;text-align:start;vertical-align:top}}th{{background:var(--nav);color:#fff}}
td ul{{margin:0;padding-inline-start:18px}}.ref{{font:.75rem monospace;color:var(--mut)}}.sv{{font-weight:700;white-space:nowrap}}tr.sH .sv{{color:var(--H)}}tr.sM .sv{{color:var(--M)}}
.u{{font:.75rem monospace;color:var(--mut)}}
.top li{{margin:.25em 0}}
h3.grp{{margin:1.6em 0 .6em;font-size:1.1rem}}h3 .en{{color:var(--mut);font-weight:400;font-size:.9rem}}.cnt{{color:var(--mut);font-weight:400}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:12px;margin:8px 0;padding:0 14px;border-inline-start:5px solid var(--line)}}
.card.wH{{border-inline-start-color:var(--H)}}.card.wM{{border-inline-start-color:var(--M)}}.card.wL{{border-inline-start-color:var(--L)}}.card.wok{{border-inline-start-color:var(--ok)}}
summary{{cursor:pointer;display:flex;flex-wrap:wrap;gap:8px;align-items:center;padding:12px 0;list-style:none}}summary::-webkit-details-marker{{display:none}}
.id{{font:700 .85rem monospace;background:var(--q);padding:2px 6px;border-radius:5px}}.lb{{font-weight:600;flex:1 1 240px}}
.pill{{font-size:.8rem;color:var(--mut)}}.dot{{font-size:.78rem;font-weight:700;border-radius:20px;padding:1px 10px;color:#fff}}.dot.sH{{background:var(--H)}}.dot.sM{{background:var(--M)}}.dot.sL{{background:var(--L)}}.dot.ok{{background:var(--ok)}}
.meta2{{font-size:.82rem;color:var(--mut);overflow-wrap:anywhere;margin-bottom:6px}}
.kd{{margin:.2em 0 .8em;padding-inline-start:20px;font-size:.92rem}}.ok{{color:var(--ok)}}
.iss{{border:1px solid var(--line);border-radius:10px;padding:10px 12px;margin:10px 0 14px}}
.ih{{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:4px}}.sev,.kind,.tag{{font-size:.76rem;border-radius:5px;padding:1px 8px;border:1px solid var(--line)}}
.sH .sev{{background:var(--H);color:#fff;border-color:var(--H)}}.sM .sev{{background:var(--M);color:#fff;border-color:var(--M)}}.sL .sev{{background:var(--L);color:#fff;border-color:var(--L)}}
.tag.new{{border-color:var(--H);color:var(--H)}}.tag.ref{{font-family:monospace}}
blockquote{{margin:6px 0;background:var(--q);border-left:3px solid var(--mut);padding:6px 10px;font:.86rem/1.55 Georgia,"Times New Roman",serif;text-align:left;overflow-wrap:anywhere}}
.act{{font-size:.92rem}}.ev{{display:block;margin-top:6px;text-decoration:none}}.ev img{{max-width:100%;border:1px solid var(--line);border-radius:8px;display:block}}.ev span{{font-size:.78rem;color:var(--mut)}}
.flt{{display:flex;gap:6px;flex-wrap:wrap;margin:8px 0}}.flt button{{font:inherit;font-size:.85rem;border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:20px;padding:4px 12px;cursor:pointer}}.flt button[aria-pressed=true]{{background:var(--nav);color:#fff}}
.corr{{background:var(--card);border:1px solid var(--line);border-inline-start:4px solid var(--M);border-radius:10px;padding:10px 14px}}
</style></head><body><div class="wrap">
<p class="meta">تدقيق مستقل · محتوى فقط · قراءة فقط · {run_at} — ليس وثيقة رسمية لـ PMU</p>
<h1>تدقيق محتوى صفحة <bdi dir="ltr">Admissions Office</bdi>: الروابط الـ36</h1>
<div class="scope"><b>النطاق:</b> ما تقوله كل صفحة من الصفحات التي تفتحها الروابط الـ36 في <a href="https://pmu.edu.sa/admission/admission">{ltr("pmu.edu.sa/admission/admission")}</a> — البيانات والشروط والأرقام والتواريخ واتساقها ودقتها واكتمالها. <b>خارج النطاق:</b> الجوانب التقنية (التحويلات، الروابط، إمكانية الوصول).<br>
<b>الـ17:</b> هي صفحات الهيكل المقترح في مخطط الـ Blueprint؛ كل رابط من الـ36 مُسند إلى الصفحة التي سينتقل إليها (القسم الأخير).</div>
<div class="kpi">
<div><b>36</b><span>رابطًا راجعتُ محتواها</span></div>
<div><b>{len(issues)}</b><span>ملاحظة على المحتوى</span></div>
<div><b style="color:var(--H)">{sevc["H"]}</b><span>عالية</span></div><div><b style="color:var(--M)">{sevc["M"]}</b><span>متوسطة</span></div><div><b style="color:var(--L)">{sevc["L"]}</b><span>منخفضة</span></div>
<div><b>{newc}</b><span>جديدة (مقترحة)</span></div><div><b>{quotes}</b><span>اقتباسًا حرفيًا تحققت منها آليًا</span></div>
</div>

<h2>القرارات ذات الأولوية (الملاحظات العالية)</h2>
<ul class="card top" style="padding:12px 30px">{toph}</ul>

<h2>المعلومة نفسها بقيم مختلفة عبر الروابط</h2>
<div class="tw"><table><thead><tr><th>المعلومة</th><th>ما تقوله الصفحات</th><th>الخطورة</th></tr></thead><tbody>{mx}</tbody></table></div>

<h2>الروابط رابطًا رابطًا</h2>
<div class="flt" role="group" aria-label="تصفية"><button aria-pressed="true" data-f="all">الكل</button><button aria-pressed="false" data-f="H">فيها ملاحظة عالية</button><button aria-pressed="false" data-f="M">متوسطة</button><button aria-pressed="false" data-f="open">فتح الكل</button></div>
{"".join(cards)}

<h2>من 36 رابطًا إلى 17 صفحة مقترحة</h2>
<div class="tw"><table><thead><tr><th>الصفحة المقترحة</th><th>الروابط الحالية التي تغذيها</th><th>ملاحظات محتوى</th><th>منها عالية</th></tr></thead><tbody>{t17}</tbody></table></div>
<p class="meta">لا تُنقل صفحة حالية إلى مكانها الجديد قبل حسم ملاحظاتها؛ وإلا انتقل التعارض إلى الموقع الجديد.</p>

<h2>تصحيح على سجل الملاحظات</h2>
<div class="corr">{corr}</div>

<h2>المنهج والحدود</h2>
<ul class="card" style="padding:12px 30px">
<li>استُخرج النص الكامل لكل صفحة (مع فتح الأقسام المطوية محليًا) يوم {run_at}؛ كل اقتباس في التقرير تحقق منه البرنامج حرفيًا مقابل النص الحي، وكل لقطة تُظهر الاقتباس مظلّلًا في مكانه.</li>
<li>C04 (قائمة موظفين) لم يُنسخ محتواها لأنها أسماء أشخاص. C06/C08 بوابة التقديم (تطبيق JavaScript) لم تُعرض بهذه الطريقة.</li>
<li>تعليمات دفع ببيانات بنكية موجودة في كود C07 مخفية عن الزائر؛ لم تُنسخ في أي ملف.</li>
<li>اعتماد AACSB: مصدر التحقق <a href="https://www.aacsb.edu/educators/accreditation/value-of-accreditation">{ltr("aacsb.edu — Value of Accreditation")}</a> (الاعتماد مؤسسي، وأقل من 6% من كليات الأعمال عالميًا). لم أتحقق من اعتماد كلية PMU نفسها ولا من رمزي ETS (6993) و College Board (7647).</li>
<li>«جديد — مقترح» = ملاحظة غير موجودة في سجل الملاحظات؛ لا تُضاف إليه إلا بقرار صاحب التدقيق.</li>
</ul>
</div>
<script>
document.querySelectorAll(".flt button").forEach(b=>b.onclick=()=>{{const f=b.dataset.f;
 if(f==="open"){{document.querySelectorAll("details.card").forEach(d=>d.open=true);return}}
 document.querySelectorAll(".flt button").forEach(x=>x.setAttribute("aria-pressed",x===b));
 document.querySelectorAll("details.card").forEach(d=>{{d.hidden=!(f==="all"||d.dataset.sev===f)}})}});
</script></body></html>'''
(H / "PMU-Admissions-Content-Audit.html").write_text(page, encoding="utf-8-sig")

# ---------- Markdown ----------
md = [f"# تدقيق محتوى صفحة Admissions Office — الروابط الـ36 ({run_at})", "",
      "النطاق: محتوى الصفحات (بيانات، شروط، أرقام، تواريخ) — لا الجوانب التقنية. كل اقتباس حرفي ومتحقق منه آليًا.", "",
      f"- ملاحظات: **{len(issues)}** (عالية {sevc['H']} · متوسطة {sevc['M']} · منخفضة {sevc['L']}) — جديدة مقترحة: {newc}", f"- اقتباسات حرفية: {quotes}", "",
      "## المعلومة نفسها بقيم مختلفة", "", "| المعلومة | القيم | الخطورة | المرجع |", "|---|---|---|---|"]
md += [f"| {t} | " + "<br>".join(f"{w}: {v}" for w, v in vals) + f" | {SEV[s]} | {r} |" for t, vals, s, r in MATRIX]
md += ["", "## الروابط", ""]
for r in rows:
    md += [f"### {r['id']} — {r['label']}", f"{r['url']} → الصفحة المقترحة: {r['proposed_page']['title']} (`{r['proposed_page']['path']}`)", "", f"**الغرض:** {r['purpose']}", ""]
    md += [f"- {d}" for d in r["key_data"]] + [f"- ✓ {v}" for v in r["verified"]] + [""]
    for it in r["issues"]:
        md += [f"- **{SEV[it['severity']]} · {KIND[it['kind']]} · {'جديد (مقترح)' if it['ref'] == 'NEW' else it['ref']}** — {it['note']}"]
        md += [f"  > {q}" for q in it["quotes"]]
        md += [f"  - المعالجة: {it['action']}"] + ([f"  - الدليل: [{r['id']}-{it['n']}](../{it['screenshot']})"] if it["screenshot"] else [])
    md.append("")
md += ["## تصحيح على السجل", ""] + [f"- **{f}:** {n}" for f, n in CORRECTIONS]
(H / "CONTENT-AUDIT-2026-09-28.md").write_text("\n".join(md), encoding="utf-8")
print(json.dumps({"issues": len(issues), "sev": dict(sevc), "new": newc, "refs": refs, "quotes": quotes}, ensure_ascii=False))
