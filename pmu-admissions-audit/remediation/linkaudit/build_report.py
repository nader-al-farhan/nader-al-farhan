"""Build the Admissions Office link audit report (AR HTML + MD + JSON) from:
links.json (extract.js), checks-result.json (check_links.py), page-meta.json (shots.js),
notes.py (manual observations), ../blueprint/ia.json (target IA action per legacy link)."""
import base64
import html
import io
import json
import pathlib
import re
from collections import Counter
from PIL import Image
from notes import NOTES, HUB

H = pathlib.Path(__file__).parent
GH = "https://github.com/nader-al-farhan/nader-al-farhan/blob/claude/pmu-admissions-audit-jm54d8/pmu-admissions-audit/remediation/linkaudit/"
HUB_URL = "https://pmu.edu.sa/admission/admission"
links = json.loads((H / "links.json").read_text(encoding="utf-8"))
ids = json.loads((H / "ids.json").read_text(encoding="utf-8"))
chk = json.loads((H / "checks-result.json").read_text(encoding="utf-8"))
res = chk["results"]
meta = json.loads((H / "page-meta.json").read_text(encoding="utf-8"))
ia = json.loads((H / "../blueprint/ia.json").read_text(encoding="utf-8"))
legacy = {l["url"]: l for l in ia["legacy"]}
L = links["desktop"]["links"]
SEVN = {"H": "عالية", "M": "متوسطة", "L": "منخفضة"}
REG = {"B": "مسار التنقّل", "C": "محتوى الصفحة", "F": "التذييل", "H": "الرأس"}
BROKEN = {"C06", "C08"}  # portal SPA: not rendered by the curl-fed method

def thumb(path, w=260):
    im = Image.open(path).convert("RGB"); im.thumbnail((w, 10_000))
    b = io.BytesIO(); im.save(b, "JPEG", quality=60)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()

rows = []
for x in ids:
    if x["region"] == "header":
        continue
    l = L[x["i"]]; r = res.get(x["abs"], {}); m = meta.get(x["id"], {})
    obs = []
    if x["href"] == "#":
        pass  # covered by NOTES for the user-facing ones
    if r.get("tested") is False:
        obs.append(("—", "لم يُختبر: " + ("نطاق خارج pmu.edu.sa غير متاح من بيئة التدقيق" if "outside" in r["why"] else r["why"]), ""))
    if r.get("tested") and r.get("redirects"):
        chain = " → ".join(str(h["status"]) for h in r["hops"])
        obs.append(("L", f"سلسلة تحويل ({r['redirects']}): {chain}", "الربط بالعنوان النهائي مباشرة"))
    for s in r.get("issue_strings", []):
        if x["id"] == "C07" and s["finding"] == "F-05":
            continue  # detailed in NOTES
        if x["id"] == "F07" and s["finding"] == "F-17":
            obs.append(("—", "«#» يعيد تحميل الصفحة نفسها", "")); continue
        obs.append(("H" if s["finding"] in ("F-07", "F-21") else "M", f"نص معيب موثّق في الصفحة المستهدفة: «{s['text']}» ({s['finding']})", "تصحيح المحتوى وفق سجل الملاحظات"))
    hl = [u for u in m.get("http_links", []) if x["id"] not in ("F08",)]
    if hl and x["id"] not in ("C34",):
        obs.append(("M", "الصفحة المستهدفة تحوي روابط http:// غير مشفّرة: " + "، ".join(f"«{u}»" for u in hl), "تحويلها إلى https"))
    obs += NOTES.get(x["id"], [])
    lg = legacy.get(x["href"])
    rank = {"H": 3, "M": 2, "L": 1, "—": 0}
    sev = max((o[0] for o in obs), key=lambda s: rank[s], default="—")
    shot = m.get("shot") if x["id"] not in BROKEN else None
    rows.append({
        "id": x["id"], "region": x["region"], "group": l["heading"] if x["region"] in ("main", "footer") else "",
        "text": l["text"] or "(أيقونة)", "href": x["href"], "resolved": x["abs"], "visible": x["visible"],
        "status": r.get("status"), "redirects": r.get("redirects"), "final_url": r.get("final_url") or m.get("final"),
        "title": r.get("title"), "h1": m.get("h1"), "tested": r.get("tested"),
        "observations": [{"severity": o[0], "note": o[1], "action": o[2]} for o in obs],
        "severity": sev, "findings": sorted({s["finding"] for s in r.get("issue_strings", [])} | set(lg["findings"] if lg else [])),
        "blueprint": {"page": lg["page"], "to": lg["to"], "action": lg["action"], "note": lg["note"]["ar"]} if lg else None,
        "screenshot": shot, "screenshot_note": ("لم تُلتقط: الصفحة تعرض أسماء موظفين" if m.get("skipped") else None) or ("البوابة تطبيق JavaScript لم يُعرض بطريقة الالتقاط هذه" if x["id"] in BROKEN else None),
    })

header = [{"id": x["id"], "text": L[x["i"]]["text"], "href": x["href"], "visible": x["visible"],
           "status": res.get(x["abs"], {}).get("status"), "final_url": res.get(x["abs"], {}).get("final_url"),
           "tested": res.get(x["abs"], {}).get("tested")} for x in ids if x["region"] == "header"]
sevc = Counter(r["severity"] for r in rows)
tested = [r for r in res.values() if r["tested"]]
summary = {
    "hub": HUB_URL, "run_at": chk["run_at"], "anchors_total": len(L), "unique_urls": len(res),
    "tested": len(tested), "final_200": sum(r["status"] == 200 for r in tested), "redirected": sum(r["redirects"] > 0 for r in tested),
    "not_tested": len(res) - len(tested), "rows": len(rows), "header_links": len(header),
    "severity": {SEVN.get(k, "بلا ملاحظة"): v for k, v in sevc.items()},
    "hash_links": sum(1 for l in L if l["href"] == "#"),
}
(H / "linkaudit-2026-09-28.json").write_text(json.dumps({"summary": summary, "hub_observations": [dict(zip(("severity", "note", "action"), h)) for h in HUB],
    "rows": rows, "header": header}, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------- Markdown ----------
md = [f"# تدقيق روابط صفحة Admissions Office — {chk['run_at'][:10]}", "",
      f"**الصفحة:** {HUB_URL} · **وقت التشغيل:** {chk['run_at']} UTC · **الطريقة:** قراءة فقط (لا نقر، لا نماذج، لا تسجيل دخول).", "",
      f"- روابط `<a>` في الصفحة: **{summary['anchors_total']}** (رأس {len(header)}، مسار تنقّل 2، محتوى 36، تذييل 32، ورابط فارغ بلا href)",
      f"- عناوين فريدة: **{summary['unique_urls']}** — اختُبر {summary['tested']}؛ أعاد 200 نهائيًا {summary['final_200']}؛ مرّ بتحويل {summary['redirected']}؛ لم يُختبر {summary['not_tested']} (خارج النطاق المتاح).",
      f"- روابط «#»: {summary['hash_links']}", "",
      "## ملاحظات على مستوى الصفحة", "", "| الخطورة | الملاحظة | المعالجة |", "|---|---|---|"]
md += [f"| {SEVN[s]} | {n} | {a} |" for s, n, a in HUB]
md += ["", "## الروابط رابطًا رابطًا", "", "| # | المنطقة / المجموعة | النص | الحالة | الملاحظات | المعالجة | الخطورة | لقطة |", "|---|---|---|---|---|---|---|---|"]
for r in rows:
    st = "لم يُختبر" if r["tested"] is False else f"{r['status']} ({r['redirects']} تحويل)"
    ob = "<br>".join(o["note"] for o in r["observations"]) or "—"
    ac = "<br>".join(dict.fromkeys(o["action"] for o in r["observations"] if o["action"])) or "—"
    sh = f"[{r['id']}](shots/{r['id']}.jpg)" if r["screenshot"] else (r["screenshot_note"] or "—")
    md.append(f"| {r['id']} | {REG[r['id'][0]]} / {r['group']} | [{r['text']}]({r['resolved']}) | {st} | {ob} | {ac} | {SEVN.get(r['severity'], '—')} | {sh} |")
md += ["", "## روابط الرأس (قوائم منسدلة مشتركة في الموقع كله)", "", "| # | النص | href | الحالة |", "|---|---|---|---|"]
for h_ in header:
    st = "لم يُختبر" if h_["tested"] is False else (h_["status"] if h_["status"] is not None else "—")
    md.append(f"| {h_['id']} | {h_['text'] or '(أيقونة)'} | `{h_['href']}` | {st} |")
md += ["", "## حدود الطريقة (حقيقة مقابل افتراض)", "",
       "- الصفحات عُرضت في Chromium مع جلب كل طلب بـ curl (تحقق TLS كامل)؛ المتصفح لم يتصل بالشبكة مباشرة. البوابة (C06/C08) تطبيق JavaScript لم يُعرض بهذه الطريقة، فلا لقطة لها هنا (الدليل السابق F-08 قائم).",
       "- النطاقات خارج pmu.edu.sa (Twitter/X، Facebook، LinkedIn، YouTube، Instagram، Taleo) غير متاحة من بيئة التدقيق فلم تُختبر.",
       "- `http://admissions.pmu.edu.sa` أعاد 503 بنص «upstream connect error … connection timeout» ثلاث مرات — النص صادر عن وكيل البيئة لا عن PMU، لذلك **غير مؤكَّد** إن كان الخلل في الخادم.",
       "- `ithelpdesk.pmu.edu.sa` رُفض بـ 502 عند CONNECT من وكيل البيئة — غير مختبر.",
       "- صفحة قائمة الموظفين (C04) لم تُلتقط لأنها تعرض أسماء شخصية.", ""]
(H / "LINK-AUDIT-2026-09-28.md").write_text("\n".join(md), encoding="utf-8")

# ---------- HTML ----------
e = html.escape
def ltr(s): return f'<bdi dir="ltr">{e(s)}</bdi>'
def iso(s):
    """escape, then isolate quoted spans and status chains so RTL does not reorder them"""
    s = e(s)
    s = re.sub(r"«([^»]*)»", r"«<bdi>\1</bdi>»", s)
    return re.sub(r"\d{3}(?: → \d{3})+|https?://\S+|[A-Za-z_]+/[A-Za-z_./]+", lambda m: f'<bdi dir="ltr">{m.group(0)}</bdi>', s)
hub_img = Image.open(H / "shots/hub-annotated-desktop.png").convert("RGB").crop((0, 330, 1366, 1720))
b = io.BytesIO(); hub_img.save(b, "JPEG", quality=70); hub_src = "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()
trs = []
for r in rows:
    st = '<span class="nt">لم يُختبر</span>' if r["tested"] is False else f'{r["status"]}' + (f' · {r["redirects"]}↪' if r["redirects"] else "")
    ob = "".join(f'<li class="s{o["severity"]}">{iso(o["note"])}</li>' for o in r["observations"]) or '<li class="ok">لا ملاحظات</li>'
    ac = "".join(f"<li>{iso(a)}</li>" for a in dict.fromkeys(o["action"] for o in r["observations"] if o["action"])) or "—"
    bp = f'<div class="bp">الهيكل المقترح: {e(r["blueprint"]["action"])} → {e(r["blueprint"]["to"])}</div>' if r["blueprint"] else ""
    fd = f'<div class="fd">{" ".join(r["findings"])}</div>' if r["findings"] else ""
    if r["screenshot"]:
        sh = f'<a href="{GH}{r["screenshot"]}" target="_blank" rel="noopener"><img loading="lazy" alt="لقطة {r["id"]}" src="{thumb(H / r["screenshot"])}"></a>'
    else:
        sh = f'<span class="nt">{e(r["screenshot_note"] or "—")}</span>'
    trs.append(f'''<tr class="r{r["severity"]}" data-sev="{r["severity"]}" data-reg="{r["id"][0]}"><td class="id">{r["id"]}</td>
<td><div class="lb">{ltr(r["text"])}</div><div class="gp">{e(REG[r["id"][0]])}{" / " + ltr(r["group"]) if r["group"] else ""}</div>
<a class="u" href="{e(r["resolved"])}" target="_blank" rel="noopener">{ltr(r["href"] or "")}</a>{"<div class=u>⇢ " + ltr(r["final_url"]) + "</div>" if r["final_url"] and r["final_url"] != r["resolved"] else ""}{bp}{fd}</td>
<td class="st">{st}</td><td><ul>{ob}</ul></td><td><ul class="ac">{ac}</ul></td><td class="sv">{SEVN.get(r["severity"], "—")}</td><td class="sh">{sh}</td></tr>''')
hubrows = "".join(f'<tr><td class="sv s{s}">{SEVN[s]}</td><td>{iso(n)}</td><td>{iso(a)}</td></tr>' for s, n, a in HUB)
hdrrows = "".join(f'<tr><td class="id">{h_["id"]}</td><td>{ltr(h_["text"] or "(أيقونة)")}</td><td class="u">{ltr(h_["href"] or "")}</td><td>{"لم يُختبر" if h_["tested"] is False else (h_["status"] if h_["status"] is not None else "—")}</td></tr>' for h_ in header)
S = summary
page = f'''<!doctype html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>تدقيق روابط صفحة القبول</title>
<style>
:root{{--bg:#f6f7fb;--card:#fff;--ink:#1b2033;--mut:#5b6275;--line:#dfe3ec;--H:#c62828;--M:#e08a00;--L:#2f6db5;--ok:#2e7d32;--nav:#1a237e}}
@media (prefers-color-scheme:dark){{:root:not([data-theme=light]){{--bg:#11131a;--card:#1a1d27;--ink:#e8eaf2;--mut:#a3a9ba;--line:#2c3140}}}}
:root[data-theme=dark]{{--bg:#11131a;--card:#1a1d27;--ink:#e8eaf2;--mut:#a3a9ba;--line:#2c3140}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.65 "Segoe UI",Tahoma,"Noto Naskh Arabic",Arial,sans-serif}}
.wrap{{max-width:1280px;margin:auto;padding:24px 16px 60px}}
h1{{font-size:1.6rem;margin:.2em 0}}h2{{font-size:1.2rem;margin:1.8em 0 .6em;border-inline-start:4px solid var(--nav);padding-inline-start:10px}}
.meta{{color:var(--mut);font-size:.9rem;overflow-wrap:anywhere}}
.kpi{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:18px 0}}
.kpi div{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px}}.kpi b{{display:block;font-size:1.5rem}}.kpi span{{color:var(--mut);font-size:.85rem}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;overflow:hidden}}
.hub img{{width:100%;height:auto;display:block;border-radius:8px;border:1px solid var(--line)}}
.tw{{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:12px}}
table{{border-collapse:collapse;width:100%;font-size:.88rem}}th,td{{border-bottom:1px solid var(--line);padding:8px;vertical-align:top;text-align:start}}
th{{background:var(--nav);color:#fff;position:sticky;top:0}}
td.id{{font:700 .85rem monospace;white-space:nowrap}}.lb{{font-weight:600}}.gp{{color:var(--mut);font-size:.8rem}}
.u{{display:block;font:.76rem monospace;color:var(--mut);overflow-wrap:anywhere;direction:ltr;text-align:left}}
ul{{margin:0;padding-inline-start:18px}}li.sH::marker{{color:var(--H)}}li.sM::marker{{color:var(--M)}}li.sL::marker{{color:var(--L)}}li.ok{{color:var(--ok)}}
li.sH{{color:var(--H)}}.sv{{white-space:nowrap;font-weight:700}}tr.rH .sv,.sv.sH{{color:var(--H)}}tr.rM .sv,.sv.sM{{color:var(--M)}}tr.rL .sv,.sv.sL{{color:var(--L)}}
.sh img{{width:200px;max-width:40vw;border:1px solid var(--line);border-radius:6px}}.nt{{color:var(--mut);font-size:.8rem}}
.bp{{font-size:.78rem;color:var(--nav);margin-top:4px}}.fd{{font:.75rem monospace;color:var(--H)}}
.flt{{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0}}.flt button{{border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:20px;padding:5px 12px;cursor:pointer;font:inherit;font-size:.85rem}}
.flt button[aria-pressed=true]{{background:var(--nav);color:#fff}}
.note{{background:var(--card);border-inline-start:4px solid var(--M);padding:10px 14px;border-radius:8px}}
@media(max-width:700px){{#t thead{{display:none}}#t,#t tbody,#t tr,#t td{{display:block;width:100%}}#t tr{{border-bottom:6px solid var(--bg);padding:6px 0}}#t td{{border:0;padding:4px 10px}}
#t td.st::before{{content:"الحالة: "}}#t td.sv::before{{content:"الخطورة: "}}#t td:nth-child(5)::before{{content:"المعالجة:";display:block;color:var(--mut);font-size:.8rem}}.sh img{{width:100%;max-width:100%}}}}
</style></head><body><div class="wrap">
<p class="meta">تدقيق مستقل · قراءة فقط · مفهوم للنقاش الداخلي — ليس وثيقة رسمية لـ PMU</p>
<h1>تدقيق روابط صفحة <bdi dir="ltr">Admissions Office</bdi> الحية</h1>
<p class="meta">الصفحة: <a href="{HUB_URL}">{ltr(HUB_URL)}</a> · التشغيل: {ltr(S["run_at"])} UTC · لا نقر، لا نماذج، لا تسجيل دخول</p>
<div class="kpi">
<div><b>{S["anchors_total"]}</b><span>رابط &lt;a&gt; في الصفحة</span></div>
<div><b>{S["unique_urls"]}</b><span>عنوان فريد · اختُبر {S["tested"]}</span></div>
<div><b>{S["final_200"]}/{S["tested"]}</b><span>انتهى بـ 200</span></div>
<div><b>{S["redirected"]}</b><span>يمر بتحويل واحد أو أكثر</span></div>
<div><b>{sevc.get("H",0)}</b><span>رابط بملاحظة عالية</span></div>
<div><b>{sevc.get("M",0)}</b><span>متوسطة</span></div>
<div><b>{S["hash_links"]}</b><span>روابط «#» (3 ظاهرة في التذييل + «Objectives» في قائمة About)</span></div>
</div>
<p class="note"><b>الخلاصة:</b> لا يوجد رابط مكسور (404) بين {S["tested"]} رابطًا مختبرًا، لكن المشكلة في <b>ما تفتحه الروابط</b>: محتوى متقادم أو متعارض، عناوين خاطئة، أخطاء إملائية، روابط «#» لا تعمل، وسلاسل تحويل تبطئ الوصول. صُنّف {sevc.get("H",0)} رابطًا بخطورة عالية.</p>

<h2>الصفحة مرقّمة (لقطة حية، 1366px)</h2>
<div class="card hub"><img alt="صفحة Admissions Office مع أرقام الروابط C01–C36؛ الأحمر = ملاحظة على الرابط نفسه" src="{hub_src}">
<p class="meta">الأزرق = رقم الرابط، الأحمر = ملاحظة على الرابط نفسه، الخلفية الصفراء = «Visting». اللقطات الكاملة: <a href="{GH}shots/hub-annotated-desktop.png">سطح المكتب</a> · <a href="{GH}shots/hub-annotated-mobile.png">الجوال 390px</a></p></div>

<h2>ملاحظات على مستوى الصفحة</h2>
<div class="tw"><table><thead><tr><th>الخطورة</th><th>الملاحظة</th><th>المعالجة</th></tr></thead><tbody>{hubrows}</tbody></table></div>

<h2>الروابط رابطًا رابطًا ({len(rows)})</h2>
<div class="flt" role="group" aria-label="تصفية">
<button aria-pressed="true" data-f="all">الكل</button><button aria-pressed="false" data-f="H">عالية</button><button aria-pressed="false" data-f="M">متوسطة</button>
<button aria-pressed="false" data-f="C">محتوى الصفحة</button><button aria-pressed="false" data-f="F">التذييل</button></div>
<div class="tw"><table id="t"><thead><tr><th>#</th><th>الرابط</th><th>الحالة</th><th>الملاحظات</th><th>المعالجة</th><th>الخطورة</th><th>لقطة</th></tr></thead><tbody>
{"".join(trs)}</tbody></table></div>
<p class="meta">اضغط على أي لقطة لفتحها بالحجم الكامل في المستودع. «↪» = عدد التحويلات. «الهيكل المقترح» = مصير الرابط في مخطط الـ UX/IA Blueprint.</p>

<h2>روابط الرأس ({len(header)}) — قوائم مشتركة في الموقع كله</h2>
<details class="card"><summary>عرض الجدول</summary><div class="tw"><table><thead><tr><th>#</th><th>النص</th><th>href</th><th>الحالة</th></tr></thead><tbody>{hdrrows}</tbody></table></div></details>

<h2>حدود الطريقة (حقيقة مقابل افتراض)</h2>
<ul class="card">
<li>عُرضت الصفحات في Chromium مع جلب كل طلب عبر curl بتحقق TLS كامل؛ المتصفح لم يتصل بالشبكة ومخزن شهاداته لم يُعدَّل.</li>
<li>البوابة (C06/C08) تطبيق JavaScript لم يُعرض بهذه الطريقة؛ دليلها السابق (F-08، S30–S35) قائم.</li>
<li>مواقع التواصل و Taleo خارج النطاق المتاح فلم تُختبر.</li>
<li>{ltr("http://admissions.pmu.edu.sa")} أعاد 503 «upstream connect error … connection timeout» ثلاث مرات — النص صادر عن وكيل البيئة، <b>فلا يُنسب خلل للخادم دون تحقق من شبكة أخرى</b>.</li>
<li>{ltr("ithelpdesk.pmu.edu.sa")} رُفض بـ 502 من وكيل البيئة — غير مختبر.</li>
<li>C04 (قائمة الموظفين) لم تُلتقط لأنها تعرض أسماء شخصية.</li>
</ul>
<p class="meta">الأدوات: <bdi dir="ltr">extract.js · check_links.py · shots.js · build_report.py</bdi> في <bdi dir="ltr">remediation/linkaudit/</bdi> — قابلة لإعادة التشغيل.</p>
</div>
<script>
document.querySelectorAll(".flt button").forEach(b=>b.onclick=()=>{{
 document.querySelectorAll(".flt button").forEach(x=>x.setAttribute("aria-pressed",x===b));
 const f=b.dataset.f;document.querySelectorAll("#t tbody tr").forEach(tr=>{{
  tr.hidden=!(f==="all"||tr.dataset.sev===f||tr.dataset.reg===f)}})}});
</script></body></html>'''
(H / "PMU-Admissions-Hub-Link-Audit.html").write_text(page, encoding="utf-8-sig")
print(json.dumps(summary, ensure_ascii=False))
