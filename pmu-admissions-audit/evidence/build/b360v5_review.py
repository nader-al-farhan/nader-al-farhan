# Management Review & Decision Package (Directive 2.2 §22). Usage: b360v5_review.py data.json annotated_dir out.html ar|en
import json, sys, html, re, collections
D = json.load(open(sys.argv[1])); EV = sys.argv[2]; OUT = sys.argv[3]; AR = sys.argv[4] == 'ar'
def T(en, ar): return ar if AR else en
e = html.escape
R = D['rows']; S = D['stats']; C = D['coverage22']; DS = D['discovery22']; by = {r['fid']: r for r in R}
P = lambda k: S['plevel'].get(k, 0)
NAVY, GOLD = '#1F3864', '#A8863A'
css = f"""
* {{ font-feature-settings: "calt" 0, "case" 0; }}
@page {{ size: A4; margin: 15mm 14mm 15mm 14mm; }}
@page cover {{ margin: 0; }}
body {{ font-family: {'"Noto Naskh Arabic", Inter' if AR else 'Inter, "Noto Naskh Arabic"'}, sans-serif; font-size: {'10.3pt' if AR else '9.3pt'}; line-height: {1.72 if AR else 1.48}; color: #1c1c1c; direction: {'rtl' if AR else 'ltr'}; margin: 0; }}
h1 {{ font-size: 15pt; color: {NAVY}; margin: 0 0 6pt; padding-bottom: 3pt; border-bottom: 2px solid {NAVY}; break-after: avoid; }}
h1 .n {{ color: {GOLD}; font-family: Inter; margin-{'left' if AR else 'right'}: 6pt; }}
h3 {{ font-size: 10.2pt; color: #2E5597; margin: 8pt 0 3pt; break-after: avoid; }}
p {{ margin: 0 0 5pt; text-align: justify; }}
.sec {{ break-before: page; }}
table {{ width: 100%; border-collapse: collapse; margin: 3pt 0 8pt; font-size: {'8.6pt' if AR else '8pt'}; }}
th {{ background: {NAVY}; color: #fff; padding: 3.5pt 4.5pt; text-align: {'right' if AR else 'left'}; font-weight: 600; vertical-align: bottom; }}
td {{ border: .6pt solid #C9D3E3; padding: 3pt 4.5pt; vertical-align: top; }} tr {{ break-inside: avoid; }} tr:nth-child(even) td {{ background: #F6F8FC; }}
.ltr {{ direction: ltr; unicode-bidi: isolate; font-family: Inter, sans-serif; }}
.q {{ direction: ltr; unicode-bidi: isolate; text-align: left; font-family: Inter, sans-serif; font-size: 7.8pt; color: #333; background: #F3F3F3; border-{'right' if AR else 'left'}: 3px solid #9E9E9E; padding: 2.5pt 6pt; display: block; margin: 3pt 0; }}
.kpis {{ display: flex; gap: 6pt; margin: 6pt 0 8pt; }} .kpi {{ flex: 1; border: 1px solid #C9D3E3; border-top: 3px solid {NAVY}; padding: 5pt; text-align: center; }}
.kpi .v {{ font-size: 16pt; font-weight: 700; color: {NAVY}; font-family: Inter; }} .kpi .l {{ font-size: 7.6pt; color: #555; }}
.p0,.p1,.p2,.p3 {{ font-family: Inter; font-weight: 700; padding: 0 3pt; border-radius: 2pt; white-space: nowrap; }}
.p0 {{ background: #FFC7CE; color: #9C0006; }} .p1 {{ background: #FFEB9C; color: #7F4F00; }} .p2 {{ background: #DDEBF7; color: {NAVY}; }} .p3 {{ background: #E2EFDA; color: #375623; }}
.card {{ border: 1px solid #C9D3E3; border-{'right' if AR else 'left'}: 4px solid #9C0006; padding: 5pt 8pt; margin: 0 0 6pt; break-inside: avoid; }}
.st {{ display: inline-block; padding: 3pt 9pt; font-family: Inter; font-weight: 700; font-size: 8.4pt; border-radius: 3pt; margin: 2pt 0; }}
.ok {{ background: #E2EFDA; color: #375623; border: 1px solid #A9D08E; }} .no {{ background: #FFC7CE; color: #9C0006; border: 1px solid #F4A7B1; }}
.small {{ font-size: 7.8pt; color: #444; }} .meta {{ font-size: 7.8pt; color: #555; }}
figure {{ margin: 3pt 0 7pt; break-inside: avoid; }} figure img {{ width: 100%; max-height: 105mm; object-fit: contain; object-position: top; border: 1px solid #BFBFBF; display: block; }} figcaption {{ font-size: 7.4pt; color: #333; margin-top: 2pt; }}
.pair {{ display: flex; gap: 6pt; break-inside: avoid; }} .pair figure.half {{ flex: 1; min-width: 0; }} .pair figure.half img {{ max-height: 95mm; }}
.fl {{ font-size: 7.2pt; font-weight: 600; color: {GOLD}; font-family: Inter; }} .src {{ color: #666; font-size: 6.9pt; word-break: break-all; }}
.evb {{ border-top: 1px solid #C9D3E3; padding-top: 4pt; margin-top: 6pt; }} .evh {{ font-weight: 700; color: {NAVY}; break-after: avoid; }} .why {{ font-size: 8pt; color: #444; margin: 1pt 0 3pt; break-after: avoid; }} h3.grp {{ font-size: 11pt; border-bottom: 1px solid {GOLD}; }}
.cover {{ page: cover; height: 287mm; position: relative; overflow: hidden; box-sizing: border-box; padding: 40mm 22mm 0; }}
.cover .bar {{ position: absolute; top: 0; {'right' if AR else 'left'}: 0; width: 9mm; height: 100%; background: {NAVY}; }}
.cover .gold {{ position: absolute; top: 0; {'right' if AR else 'left'}: 9mm; width: 1.6mm; height: 100%; background: {GOLD}; }}
.cover .k {{ font-size: 10pt; letter-spacing: .12em; color: {GOLD}; font-family: Inter; font-weight: 600; }}
.cover .t {{ font-size: 25pt; font-weight: 700; color: {NAVY}; line-height: 1.25; margin-top: 6pt; }}
.cover .ta {{ font-size: 17pt; color: #2E5597; margin-top: 6pt; font-family: "Noto Naskh Arabic"; direction: rtl; }}
.cover .blk {{ margin-top: 22mm; font-size: 10pt; line-height: 1.75; }} .cover .blk b {{ color: {NAVY}; }}
.cover .foot {{ position: absolute; bottom: 20mm; {'right' if AR else 'left'}: 22mm; {'left' if AR else 'right'}: 22mm; border-top: 1px solid #C9D3E3; padding-top: 6pt; font-size: 9pt; color: #444; }}
.dc td:first-child {{ width: 32%; font-weight: 600; color: {NAVY}; }}
"""
H = [f'<!doctype html><html lang="{"ar" if AR else "en"}" dir="{"rtl" if AR else "ltr"}"><head><meta charset="utf-8"><title>{T("PMU Admissions — Management Review & Decision Package", "مراجعة محتوى القبول وحزمة القرارات الإدارية")}</title><meta name="author" content="Nader Al Farhan"><style>{css}</style></head><body>']
# ---------- cover (§26)
H.append(f'''<div class="cover"><div class="bar"></div><div class="gold"></div>
<div class="k">PRINCE MOHAMMAD BIN FAHD UNIVERSITY · ADMISSIONS OFFICE</div>
<div class="t">PMU Admissions<br>Management Review &amp; Decision Package</div>
<div class="ta">مراجعة محتوى القبول وحزمة القرارات الإدارية</div>
<div class="blk"><b>Prepared for | مقدم إلى</b><br>Mr. Radhi Alkhaldi<br>Associate Director of Enrollment<br><br>
<b>Prepared by | إعداد</b><br>Nader Al Farhan | نادر آل فرحان<br>Administrative Assistant, Student Affairs, Admission Office<br>Prince Mohammad Bin Fahd University (PMU)</div>
<div class="foot"><b>Prepared for Management Review</b> · {T('Version 5.0 · Review date 22 October 2026 · English edition', 'الإصدار 5.0 · تاريخ المراجعة 22 أكتوبر 2026 · النسخة العربية')}</div></div>''')
# ---------- document control (§31)
H.append(f'<div class="sec"><h1>{T("Document control", "ضبط الوثيقة")}</h1><table class="dc">')
for a, b in [(T('Title', 'العنوان'), T('PMU Admissions — Management Review & Decision Package', 'مراجعة محتوى القبول وحزمة القرارات الإدارية')), (T('Reference', 'المرجع'), 'PMU-ADM-360-MASTER-20261022'),
             (T('Version', 'الإصدار'), '5.0'), (T('Review date', 'تاريخ المراجعة'), T('22 October 2026 (Asia/Riyadh)', '22 أكتوبر 2026 (بتوقيت الرياض)')),
             (T('Prepared by', 'إعداد'), 'Nader Al Farhan | نادر آل فرحان'), (T('Position', 'المسمى'), 'Administrative Assistant, Student Affairs, Admission Office'),
             (T('Recipient', 'المستلم'), 'Mr. Radhi Alkhaldi — Associate Director of Enrollment'),
             (T('Purpose', 'الغرض'), T('To present verified findings on the published Admissions Office content and the decisions and actions required', 'عرض النتائج المتحقق منها في المحتوى المنشور لمكتب القبول والقرارات والإجراءات المطلوبة')),
             (T('Classification', 'التصنيف'), T('Internal — for management review', 'داخلي — للمراجعة الإدارية')),
             (T('Management status', 'الحالة الإدارية'), 'READY FOR MANAGEMENT REVIEW'), (T('Closure status', 'حالة الإغلاق'), 'NOT READY FOR VERIFIED CLOSURE'),
             (T('Companion files', 'الملفات المرافقة'), T('02/04 Master Register (AR/EN) · 05 Evidence Pack', '02/04 السجل الرئيس (عربي/إنجليزي) · 05 حزمة الأدلة'))]:
    H.append(f'<tr><td>{a}</td><td>{e(b) if "|" in b or "—" in b else b}</td></tr>')
H.append('</table>')
# ---------- 1 executive summary
H.append(f'<h1><span class="n">1</span>{T("Executive summary", "الملخص التنفيذي")}</h1>')
H.append(f'''<div class="kpis"><div class="kpi"><div class="v">{C['eligible']}</div><div class="l">{T('eligible resources reviewed', 'موردًا مؤهلًا رُوجع')}</div></div>
<div class="kpi"><div class="v">{S['n']}</div><div class="l">{T('findings', 'ملاحظة')}</div></div>
<div class="kpi"><div class="v" dir="ltr" style="color:#9C0006;unicode-bidi:isolate">{P('P0')} · {P('P1')}</div><div class="l" dir="ltr">P0 · P1</div></div>
<div class="kpi"><div class="v">{S['conflicts']}</div><div class="l">{T('proven published conflicts', 'تعارضًا منشورًا مثبتًا')}</div></div>
<div class="kpi"><div class="v">{len(D['decisions'])}</div><div class="l">{T('decisions required', 'قرارات مطلوبة')}</div></div></div>''')
am = collections.Counter(a['code'] for a in D['amend'])
H.append('<p>' + T(
 f"The Admissions Office content is extensive and generally organised by applicant category, but it cannot currently serve as a reliable single source for applicants. On 22 October 2026 the two P0 issues remain live: the published application fee conflicts for international transfer and visiting applicants (SAR 500 vs SAR 950) and for the College of Medicine (SAR 1,000 vs SAR 1,150). High-priority (P1) issues include the absence of a current admission cycle, the discontinued SAT II test in the international weighting, conflicting graduate English thresholds, and another university’s text on a graduate requirements page. Across {C['eligible']} eligible resources the review recorded {S['n']} findings — {P('P0')} P0, {P('P1')} P1, {P('P2')} P2 and {P('P3')} P3 — including {S['conflicts']} proven conflicts between published statements, together with {len(D['verified_correct'])} verified strengths. Of the six amendments requested on 26 October 2025, {am.get('NOT_PUBLISHED',0)} are not published and {am.get('PARTIALLY_PUBLISHED',0)} are partially published.",
 f"محتوى مكتب القبول وافٍ ومنظم في معظمه حسب فئة المتقدم، لكنه لا يصلح حاليًا مصدرًا موحدًا موثوقًا للمتقدمين. ففي 22 أكتوبر 2026 ما زالت ملاحظتا P0 قائمتين: تعارض رسم التقديم المنشور للمحولين والزائرين الدوليين (500 مقابل 950 ريالًا) ولكلية الطب (1,000 مقابل 1,150 ريالًا). ومن الملاحظات المرتفعة (P1): غياب دورة قبول سارية، واختبار SAT II الموقوف في أوزان الطلاب الدوليين، وتعارض حدود اللغة للدراسات العليا، ونص جامعة أخرى في صفحة متطلبات للدراسات العليا. وعبر {C['eligible']} موردًا مؤهلًا سجلت المراجعة {S['n']} ملاحظة — {P('P0')} من P0 و{P('P1')} من P1 و{P('P2')} من P2 و{P('P3')} من P3 — منها {S['conflicts']} تعارضًا مثبتًا بين بيانات منشورة، إلى جانب {len(D['verified_correct'])} نقاط قوة متحقق منها. ومن التعديلات الستة المطلوبة في 26 أكتوبر 2025، {am.get('NOT_PUBLISHED',0)} غير منشورة و{am.get('PARTIALLY_PUBLISHED',0)} منشورة جزئيًا.") + '</p><p>' + T(
 'Ten decisions are required. Most fee and admission-requirement values rest with authorities outside the Admissions Office and are presented for referral; five matters fall within the Office’s own remit and can be directed now: an interim cycle notice, withdrawal of the 2018 guide, official contact details, content ownership and 48 editorial corrections. Where published statements conflict, no value has been chosen; each conflict awaits institutional confirmation.',
 'المطلوب عشرة قرارات. أغلب قيم الرسوم ومتطلبات القبول بيد جهات خارج مكتب القبول فتُعرض للإحالة؛ وخمس مسائل ضمن صلاحية المكتب يمكن توجيهها الآن: إشعار مؤقت بالدورة، وسحب دليل 2018، وبيانات التواصل الرسمية، وملكية المحتوى، و48 تصحيحًا تحريريًا. وحيث تتعارض البيانات المنشورة لم تُختر قيمة بعينها؛ فكل تعارض ينتظر تأكيدًا مؤسسيًا.') + '</p>')
H.append(f'<span class="st ok">READY FOR MANAGEMENT REVIEW</span> <span class="st no">NOT READY FOR VERIFIED CLOSURE</span></div>')
# ---------- 2 scope & method
H.append(f'<div class="sec"><h1><span class="n">2</span>{T("Scope and method", "النطاق والمنهج")}</h1><h3>{T("Scope", "النطاق")}</h3><p>' + T(
 f"Starting point: https://www.pmu.edu.sa/admission/admission. The scope was rediscovered on 22 October 2026: the five sections of the root page carry {DS['placements']} link placements resolving to {C['unique_destinations']} unique destinations. In scope are those destinations, the shared admissions menu, the bilingual content of /apply, the public landing page of the application portal, two linked PDF guides, and nine official pages used to verify specific statements (fee schedules, application forms, list of majors, the calendar opened by the footer link, the preparatory study plan). University-wide navigation is not treated as an admissions branch.",
 f"نقطة البداية: https://www.pmu.edu.sa/admission/admission. أُعيد اكتشاف النطاق في 22 أكتوبر 2026: تحمل الأقسام الخمسة في الصفحة الجذرية {DS['placements']} موضع رابط تقود إلى {C['unique_destinations']} وجهة فريدة. ويشمل النطاق هذه الوجهات، والقائمة الجانبية المشتركة للقبول، والمحتوى ثنائي اللغة في /apply، والصفحة العامة لبوابة التقديم، ودليلَي PDF المرتبطين، وتسع صفحات رسمية استُخدمت للتحقق من معلومات محددة (جداول الرسوم، ونماذج التقديم، وقائمة التخصصات، والتقويم الذي يفتحه رابط التذييل، والخطة الدراسية للتحضيري). ولا تُعامل قوائم التنقل العامة للجامعة كفروع للقبول.") + f'</p><h3>{T("Method", "المنهج")}</h3><ul>' + ''.join(f'<li>{x}</li>' for x in T(
 ['Independent review of every published content unit against seven areas: requirements, tests and English, fees, programmes, admission cycle, applicant categories and content quality.',
  'Systematic capture of each page (visible and tab content) and full reading of both PDF guides; status check of every link found on in-scope pages.',
  'Source verification: each finding quotes the published text verbatim with its URL and location; each conflict is documented on both sides; errors are tied to a governing reference.',
  'Cross-source comparison of values across pages, forms, fee schedules and the Arabic and English text.',
  'Evidence validation: all findings were re-matched against the 22 October 2026 capture; highest-risk items were re-checked live the same day.',
  'Visual evidence: original captures of the live pages and PDF taken on 22 October 2026 for every P0/P1 finding, both sides of each proven conflict, the material Arabic–English item and the historical amendments; each original is kept unaltered and a separate annotated copy carries the reference frame.',
  'Independent challenge of every P0/P1 finding, conflict and error against the original evidence before acceptance; disagreements were resolved by returning to the source.',
  'Quality control across all deliverables (identifiers, counts, statuses, Arabic–English equivalence and document integrity).'],
 ['مراجعة مستقلة لكل وحدة محتوى منشورة وفق سبعة محاور: المتطلبات، والاختبارات واللغة، والرسوم، والبرامج، ودورة القبول، وفئات المتقدمين، وجودة المحتوى.',
  'التقاط منهجي لكل صفحة (المحتوى الظاهر ومحتوى التبويبات) وقراءة كاملة لدليلَي PDF؛ وفحص حالة كل رابط في صفحات النطاق.',
  'التحقق من المصادر: كل ملاحظة تقتبس النص المنشور حرفيًا مع رابطه وموضعه؛ وكل تعارض موثق الطرفين؛ وكل خطأ مرتبط بمرجع حاكم.',
  'المقارنة بين المصادر لقيم الصفحات والنماذج وجداول الرسوم والنصين العربي والإنجليزي.',
  'التحقق من الأدلة: طوبقت الملاحظات كلها مع التقاط 22 أكتوبر 2026، وأُعيد فحص أعلى المخاطر حيًا في اليوم نفسه.',
  'الأدلة المرئية: لقطات أصلية للصفحات الحية وملف PDF في 22 أكتوبر 2026 لكل ملاحظات P0/P1 وطرفي كل تعارض مثبت والبند العربي–الإنجليزي الجوهري والتعديلات السابقة؛ يُحفظ كل أصل دون تعديل، وتحمل نسخة مستقلة إطار الإشارة.',
  'تحدٍّ مستقل لكل ملاحظات P0/P1 والتعارضات والأخطاء مقابل الأدلة الأصلية قبل اعتمادها؛ وحُسم أي اختلاف بالعودة إلى المصدر.',
  'ضبط الجودة عبر جميع المخرجات (المعرفات والأعداد والحالات والتكافؤ العربي–الإنجليزي وسلامة المستندات).'])) + f'</ul><h3>{T("Exclusions", "الاستبعادات")}</h3><p>' + T(
 'Read-only review. No form was submitted, no portal or internal system was accessed, no applicant data was used, no security or performance testing was performed and no website content was changed. Applicant opinions are not part of this assignment.',
 'مراجعة قراءة فقط. لم يُرسل أي نموذج، ولم يُدخل إلى البوابة أو الأنظمة الداخلية، ولم تُستخدم بيانات متقدمين، ولم تُجر اختبارات أمن أو أداء، ولم يُعدَّل أي محتوى في الموقع. وآراء المتقدمين ليست ضمن هذا التكليف.') + '</p></div>')
# ---------- 3 coverage
H.append(f'<div class="sec"><h1><span class="n">3</span>{T("Coverage", "التغطية")}</h1><table><tr><th>{T("Measure", "المقياس")}</th><th>{T("Value", "القيمة")}</th></tr>')
for a, b in [(T('Link instances / unique URLs on in-scope pages', 'روابط مرصودة / روابط فريدة في صفحات النطاق'), f"{C['discovered_link_instances']} / {C['discovered_unique_urls']}"),
             (T('Root-page placements / unique destinations', 'مواضع الصفحة الجذرية / الوجهات الفريدة'), f"{C['root_placements']} / {C['unique_destinations']}"),
             (T('Eligible resources', 'الموارد المؤهلة'), C['eligible']), ('FULLY_REVIEWED', C['fully']), ('PARTIALLY_REVIEWED', C['partially']), ('BLOCKED', C['blocked']), ('NOT_REVIEWED', C['not_reviewed']),
             ('EXCLUDED', C['excluded']), (T('Full coverage rate (FULLY_REVIEWED / eligible)', 'نسبة التغطية الكاملة (FULLY_REVIEWED / المؤهلة)'), f"{C['full_rate']}%"),
             (T('Review contact rate ((FULLY + PARTIALLY_REVIEWED) / eligible)', 'نسبة ملامسة المراجعة ((الكاملة + الجزئية) / المؤهلة)'), f"{C['contact_rate']}%"),
             (T('Visual evidence items (original + annotated) / findings covered', 'أدلة مرئية (أصل + نسخة مشروحة) / ملاحظات مغطاة'), f"{C['visual_items']} / {C['visual_findings']}"),
             (T('PDF files / pages', 'ملفات PDF / صفحاتها'), f"{C['pdfs']} / {C['pdf_pages']}"), (T('Standalone Arabic pages found', 'صفحات عربية مستقلة'), C['arabic_standalone']),
             (T('Bilingual resources / Arabic–English segment pairs compared', 'موارد ثنائية اللغة / أزواج مقارنة'), f"{C['bilingual']} / {C['segment_pairs']}"),
             (T('Links returning HTTP 404', 'روابط تعيد 404'), C['links_404'])]:
    H.append(f'<tr><td>{a}</td><td class="ltr">{b}</td></tr>')
H.append('</table><p class="small">' + T('Partially reviewed: department staff list (destination only — personal data), portal (public landing page only), Aptis guide illustrations, preparatory study plan (read 11 Oct). The rate refers to the discovered inventory, not to the whole website.',
 'مراجعة جزئية: قائمة موظفي القسم (الوجهة فقط — بيانات شخصية)، والبوابة (الصفحة العامة فقط)، ورسوم دليل Aptis، والخطة الدراسية للتحضيري (قُرئت 11 أكتوبر). والنسبة تخص الجرد المكتشف لا الموقع كله.') + '</p>')
H.append(f'<h3>{T("Findings by classification and severity", "الملاحظات حسب التصنيف والخطورة")}</h3><table><tr><th>{T("Classification", "التصنيف")}</th><th>P0</th><th>P1</th><th>P2</th><th>P3</th><th>{T("Total", "المجموع")}</th></tr>')
cc = collections.Counter((r['cls'], r['plevel']) for r in R)
for k, v in D['c12'].items():
    row = [cc[(k, p)] for p in ('P0', 'P1', 'P2', 'P3')]
    if sum(row): H.append(f'<tr><td>{T(v[0], v[1])}</td>' + ''.join(f'<td class="ltr">{x}</td>' for x in row) + f'<td class="ltr"><b>{sum(row)}</b></td></tr>')
H.append(f'<tr><td><b>{T("Total", "المجموع")}</b></td>' + ''.join(f'<td class="ltr"><b>{P(p)}</b></td>' for p in ('P0', 'P1', 'P2', 'P3')) + f'<td class="ltr"><b>{S["n"]}</b></td></tr></table></div>')
# ---------- 4 priority findings
H.append(f'<div class="sec"><h1><span class="n">4</span>{T("Priority findings", "الملاحظات ذات الأولوية")}</h1>')
for r in [x for x in R if x['plevel'] == 'P0']:
    H.append(f'<div class="card"><b><span class="p0">P0</span> <span class="ltr">{r["fid"]}</span> — {e(T(r["title_en"], r["title_ar"]))}</b><div class="meta">{e(T(r["page_en"], r["page_ar"]))} · {e(T(r["cls_en"], r["cls_ar"]))} · {T("Decision", "القرار")} <span class="ltr">{", ".join(r["dids"])}</span> · {e(T(r["state22_en"], r["state22_ar"]))}</div><p>{e(T(r["description_en"], r["description"]))}</p><p class="small"><b>{T("Severity rationale", "مبرر الخطورة")}:</b> {e(T(r["rationale_en"], r["rationale_ar"]))}</p></div>')
H.append(f'<table><tr><th>ID</th><th>P</th><th>{T("Finding", "الملاحظة")}</th><th>{T("Classification", "التصنيف")}</th><th>{T("Decision", "القرار")}</th></tr>')
for r in [x for x in R if x['plevel'] == 'P1']:
    H.append(f'<tr><td class="ltr">{r["fid"]}</td><td><span class="p1">P1</span></td><td>{e(T(r["title_en"], r["title_ar"]))}</td><td>{e(T(r["cls_en"], r["cls_ar"]))}</td><td class="ltr">{", ".join(r["dids"])}</td></tr>')
H.append('</table></div>')
# ---------- 5 conflicts
pname = {i['rid']: i['title'].split('::')[0].strip() for i in D['inventory']}
H.append(f'<div class="sec"><h1><span class="n">5</span>{T("Proven published conflicts", "التعارضات المنشورة المثبتة")}</h1><p>' + T('Each conflict is documented on both sides and concerns the same programme, applicant category and period. Status of all: OPEN CONFLICT — the correct policy requires institutional confirmation.',
 'كل تعارض موثق الطرفين ويتعلق بالبرنامج وفئة المتقدم والفترة نفسها. وحالة الجميع: تعارض مفتوح — السياسة الصحيحة تحتاج تأكيدًا مؤسسيًا.') + f'</p><table><tr><th>ID</th><th>P</th><th>{T("Conflict", "التعارض")}</th><th>{T("Sources (evidence)", "المصادر (الأدلة)")}</th><th>{T("Decision", "القرار")}</th></tr>')
evb = collections.defaultdict(list)
for x in D['evidence']: evb[x['fid']].append(x)
for r in [x for x in R if x['cls'] == 'PROVEN_PUBLISHED_CONFLICT']:
    srcs = '<br>'.join(f'<span class="ltr">{x["eid"]}</span> · <span class="ltr">{e(x["url"].replace("https://", "").replace("www.", "")[:62])}</span>' for x in evb[r['fid']])
    H.append(f'<tr><td class="ltr">{r["fid"]}</td><td><span class="{r["plevel"].lower()}">{r["plevel"]}</span></td><td>{e(T(r["title_en"], r["title_ar"]))}</td><td class="small">{srcs}</td><td class="ltr">{", ".join(r["dids"])}</td></tr>')
H.append('</table></div>')
# ---------- 6 strengths
H.append(f'<div class="sec"><h1><span class="n">6</span>{T("Verified strengths", "نقاط القوة المتحقق منها")}</h1><table><tr><th>ID</th><th>{T("Strength", "نقطة القوة")}</th><th>{T("Evidence (verbatim)", "الدليل (حرفيًا)")}</th></tr>')
for v in D['verified_correct']:
    H.append(f'<tr><td class="ltr">{v["vid"]}</td><td>{e(T(v["en"], v["ar"]))}<div class="meta">{e(T(v["page_en"], v["page_ar"]))}</div></td><td><span class="q">{e(v["excerpt"])}</span></td></tr>')
H.append('</table>')
# ---------- 7 journey
H.append(f'<h1 style="margin-top:12pt"><span class="n">7</span>{T("Published applicant information journey", "رحلة المتقدم في الوصول إلى المعلومات المنشورة")}</h1><p class="small">' + T('Assesses only whether the published content lets an applicant find each element; no applicant data or opinion is used.', 'يقيّم فقط قدرة المتقدم على العثور على كل عنصر في المحتوى المنشور؛ ولا تُستخدم بيانات أو آراء متقدمين.') + f'</p><table><tr><th>{T("Element", "العنصر")}</th><th>{T("Findable", "متاح")}</th><th>{T("Observation", "الملاحظة")}</th><th>{T("Findings", "الملاحظات")}</th></tr>')
for j in D['journey']:
    H.append(f'<tr><td><b>{e(T(j["en"], j["ar"]))}</b></td><td>{e(T(j["f_en"], j["f_ar"]))}</td><td>{e(T(j["o_en"], j["o_ar"]))}</td><td class="ltr small">{j["fids"]}</td></tr>')
H.append('</table></div>')
# ---------- 8 amendments
H.append(f'<div class="sec"><h1><span class="n">8</span>{T("Historical amendment status (requests of 26 October 2025)", "حالة التعديلات السابقة (طلبات 26 أكتوبر 2025)")}</h1><table><tr><th>ID</th><th>{T("Request", "الطلب")}</th><th>{T("Status", "الحالة")}</th><th>{T("Current published evidence (22 Oct 2026)", "الدليل المنشور الحالي (22 أكتوبر 2026)")}</th></tr>')
for a in D['amend']:
    H.append(f'<tr><td class="ltr">{a["hid"]}</td><td>{e(T(a["req_en"], a["req_ar"]))}</td><td class="ltr"><b>{a["code"]}</b></td><td>{e(T(a["ev_en"], a["ev_ar"]))}</td></tr>')
H.append('</table><p class="small">' + T('Requests are compared with the published content as historical requests; they are not treated as approved policy.', 'تُقارن الطلبات بالمحتوى المنشور بوصفها طلبات تاريخية، ولا تُعامل سياسات معتمدة.') + '</p>')
# ---------- 9 decisions
H.append(f'<h1 style="margin-top:12pt"><span class="n">9</span>{T("Decisions required", "القرارات المطلوبة")}</h1><p class="small">' + T('DIRECT: within the Admissions Office’s remit. REFER: to the competent authority. No decision has been approved.', 'توجيه: ضمن صلاحية مكتب القبول. إحالة: إلى صاحب الصلاحية المختص. لم يُعتمد أي قرار.') + f'</p><table><tr><th>ID</th><th>{T("Matter", "المسألة")}</th><th>{T("Recommendation", "التوصية")}</th><th>{T("Authority", "صاحب الصلاحية")}</th><th>{T("Role", "الدور")}</th><th>{T("Risk if deferred", "المخاطر عند التأجيل")}</th></tr>')
for d in D['decisions']:
    H.append(f'<tr><td class="ltr">{d["did"]}</td><td><b>{e(T(d["t_en"], d["t_ar"]))}</b><div class="meta">{d["impact_en"]}</div></td><td>{e(T(d["rec_en"], d["rec_ar"]))}</td><td>{e(T(d["auth"], d["auth_ar"]))}</td><td>{e(T(d["role"], d["role_ar"]))}</td><td>{e(T(d["risk_en"], d["risk_ar"]))}</td></tr>')
H.append('</table></div>')
# ---------- 10 roadmap
H.append(f'<div class="sec"><h1><span class="n">10</span>{T("Corrective action roadmap", "خارطة الإجراءات التصحيحية")}</h1><table><tr><th>ID</th><th>P</th><th>{T("Current state → target state", "الحالة الحالية ← الحالة المستهدفة")}</th><th>{T("Required change", "التغيير المطلوب")}</th><th>{T("Depends on", "يعتمد على")}</th><th>{T("Proposed target", "الموعد المقترح")}</th></tr>')
for p in D['plan']:
    H.append(f'<tr><td class="ltr">{p["aid"]}</td><td><span class="{p["prio"].lower()}">{p["prio"]}</span></td><td>{e(p["problem"])} → {e(p["outcome"])}</td><td>{e(T(p["en"], p["ar"]))}</td><td class="ltr">{p["did"]}</td><td>{e(p["target"])}</td></tr>')
H.append('</table><p class="small">' + T('After authorisation each action follows: APPROVE → IMPLEMENT → SAVE → REOPEN → READ BACK → COMPARE → VERIFY → CLOSE. Targets are proposals and commit no unit.', 'بعد التفويض يتبع كل إجراء: اعتماد ← تنفيذ ← حفظ ← إعادة فتح ← إعادة قراءة ← مقارنة ← تحقق ← إغلاق. والمواعيد مقترحة ولا تُلزم أي جهة.') + '</p>')
# ---------- 11 gaps
H.append(f'<h1 style="margin-top:12pt"><span class="n">11</span>{T("Gaps and limitations", "الفجوات والقيود")}</h1><ul>' + ''.join(f'<li>{x}</li>' for x in T(
 ['No approved, dated policy or fee decision was available; conflicting values are reported as open conflicts and were not resolved by assumption.',
  'BLOCKED: four portal registration labels load dynamically (F-033); the http:// portal link could not be confirmed from the review network (F-131). Manual check recommended.',
  'Official external references (College Board, ETS) were located but their pages could not be retrieved directly; they are cited by URL.',
  'Operational application of the published procedures was not verified. Legacy admission pages not linked from the current root were not reviewed.',
  'Visual evidence was not captured for the two BLOCKED items (F-033, F-131) or for the application portal, which did not render from the review network.',
  'No correction has been published; all P0 risks remain live on 22 October 2026.'],
 ['لم يتوفر قرار سياسات أو رسوم معتمد ومؤرخ؛ فعُرضت القيم المتعارضة تعارضاتٍ مفتوحة دون حسمها بالافتراض.',
  'معلّق: أربع تسميات في تسجيل البوابة تُحمَّل ديناميكيًا (F-033)؛ وتعذّر تأكيد رابط البوابة http من شبكة المراجعة (F-131). يُوصى بفحص يدوي.',
  'حُدد موقع المرجعين الخارجيين الرسميين (College Board وETS) دون إمكان فتح صفحاتهما مباشرة؛ ويُستشهد بهما بالرابط.',
  'لم يُتحقق من التطبيق التشغيلي للإجراءات المنشورة. ولم تُراجع صفحات القبول القديمة غير المرتبطة من الجذر الحالي.',
  'لم تُلتقط أدلة مرئية للبندين المعلّقين (F-033 وF-131) ولا لبوابة التقديم التي لم تُعرض من شبكة المراجعة.',
  'لم يُنشر أي تصحيح؛ وجميع مخاطر P0 قائمة حتى 22 أكتوبر 2026.'])) + '</ul>')
# ---------- 12 management status
H.append(f'<h1 style="margin-top:12pt"><span class="n">12</span>{T("Management status", "الحالة الإدارية")}</h1>')
H.append(f'<p><span class="st ok">Management Package: READY FOR MANAGEMENT REVIEW</span><br><span class="st no">Overall Closure: NOT READY FOR VERIFIED CLOSURE</span></p><p>' + T(
 'Closure requires, for each matter: DECISION → APPROVAL → IMPLEMENTATION → PUBLICATION → READ-BACK → VERIFY → REGRESSION → ACCEPTANCE. Delivery of this package is not implementation, and implementation is not verification.',
 'يتطلب الإغلاق لكل مسألة: قرار ← اعتماد ← تنفيذ ← نشر ← إعادة قراءة ← تحقق ← فحص ارتدادي ← قبول. وتسليم هذه الحزمة ليس تنفيذًا، والتنفيذ ليس تحققًا.') + f'</p><table><tr><th>{T("Quality gate", "معيار الجودة")}</th><th>{T("Result", "النتيجة")}</th></tr>')
for g in D.get('gates5', []):
    H.append(f'<tr><td>{e(T(g["en"], g["ar"]))}</td><td class="ltr"><b>{g["result"]}</b></td></tr>')
H.append('</table></div>')
# ---------- 13 evidence annex (§22A/§22B)
VIS = D['visual']; vb = collections.defaultdict(list)
for v in VIS: vb[v['fid']].append(v)
def fig(v, half=False):
    return (f'<figure class="{"half" if half else ""}"><div class="fl">{e(T(v["role_en"], v["role_ar"]))} · <span class="ltr">{v["eid"]}</span></div><img src="file://{EV}/{v["ann"]}">'
            f'<figcaption>{e(T(v["claim_en"], v["claim_ar"]))}<br><span class="src">{T("Source", "المصدر")}: <span class="ltr">{e(v["title"])}</span> — <span class="ltr">{e(v["url"].replace("https://", ""))}</span><br>'
            f'{T("Observed", "رُصد")}: <span class="ltr">{v["date"]} {v["time"]} (Asia/Riyadh)</span> · {T("Original", "الأصل")}: <span class="ltr">{v["orig"]}</span></span></figcaption></figure>')
GROUPS = [(T('P0 — conflict pairs', 'P0 — أزواج التعارض'), lambda r: r['plevel'] == 'P0'),
          (T('P1 — high-priority findings', 'P1 — الملاحظات المرتفعة'), lambda r: r['plevel'] == 'P1'),
          (T('Other proven published conflicts', 'تعارضات منشورة مثبتة أخرى'), lambda r: r['plevel'] not in ('P0', 'P1') and r['cls'] == 'PROVEN_PUBLISHED_CONFLICT'),
          (T('Arabic–English parity and historical amendments (current state)', 'التكافؤ العربي–الإنجليزي والتعديلات السابقة (الحالة الحالية)'), lambda r: r['plevel'] not in ('P0', 'P1') and r['cls'] != 'PROVEN_PUBLISHED_CONFLICT')]
H.append(f'<div class="sec"><h1><span class="n">13</span>{T("Selected evidence annex", "ملحق أدلة مختارة")}</h1><p class="small">' + T(
 f"{len(VIS)} visual evidence items for {len(vb)} findings, captured from the live pages and the published PDF on 22 October 2026. Each image shown is the annotated copy: the red frame and the dark label band were added for reference and are not part of the source. Conflict sources are shown side by side as separate pages, never merged. The unaltered originals, with the full visual evidence register, are in the Evidence Pack (01 and 02) and in the Master Register.",
 f"{len(VIS)} دليلًا مرئيًا لـ{len(vb)} ملاحظة، التُقطت من الصفحات الحية وملف PDF المنشور في 22 أكتوبر 2026. والصورة المعروضة هي النسخة المشروحة: أُضيف الإطار الأحمر والشريط الداكن للإشارة وليسا جزءًا من المصدر. وتُعرض مصادر التعارض متجاورة بوصفها صفحات مستقلة دون دمج. والأصول غير المعدلة مع سجل الأدلة المرئية الكامل في حزمة الأدلة (01 و02) وفي السجل الرئيس.") + '</p>')
by_f = {r['fid']: r for r in R}
for gt, cond in GROUPS:
    fids = [f for f in sorted(vb, key=lambda f: (by_f[f]['plevel'], f)) if cond(by_f[f])]
    if not fids: continue
    H.append(f'<h3 class="grp">{gt}</h3>')
    for f in fids:
        r = by_f[f]; vs = vb[f]
        H.append(f'<div class="evb"><div class="evh"><span class="{r["plevel"].lower()}">{r["plevel"]}</span> <span class="ltr">{f}</span> — {e(T(r["title_en"], r["title_ar"]))}</div><p class="why">{e(T(vs[0]["why_en"], vs[0]["why_ar"]))}</p>')
        if len(vs) == 1: H.append(fig(vs[0]))
        else:
            for k in range(0, len(vs), 2): H.append('<div class="pair">' + ''.join(fig(v, True) for v in vs[k:k + 2]) + '</div>')
        H.append('</div>')
H.append('</div></body></html>')
doc = '\n'.join(H)
parts = re.split(r'(<[^>]+>)', doc)
parts = [p if p.startswith('<') else re.sub(r'\b((?:EV|[FEDASRLHVJ])-\d{1,3}(?:-\d)?)\b', r'<span style="white-space:nowrap">\1</span>', p) for p in parts]
open(OUT, 'w').write(''.join(parts)); print('review', OUT)
