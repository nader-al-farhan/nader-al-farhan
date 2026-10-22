# Build the bilingual management report (HTML for Chromium PDF). Usage: b360_report.py data.json evdir out.html en|ar
import json, sys, html, collections
D = json.load(open(sys.argv[1])); EV = sys.argv[2]; OUT = sys.argv[3]; L = sys.argv[4]
AR = L == 'ar'
def T(en, ar): return ar if AR else en
e = html.escape
R = D['rows']; S = D['stats']; C = D['coverage']; byid = {r['fid']: r for r in R}
P = lambda k: S['plevel'].get(k, 0)
H = []
css = f"""
@page {{ size: A4; margin: 16mm 14mm 15mm 14mm; }}
@page cover {{ margin: 0; }}
* {{ font-feature-settings: "calt" 0, "case" 0; }}
body {{ font-family: {'"Noto Naskh Arabic", Inter' if AR else 'Inter, "Noto Naskh Arabic"'}, sans-serif; font-size: {'10.6pt' if AR else '9.6pt'}; line-height: {1.75 if AR else 1.5}; color: #1b1b1b; direction: {'rtl' if AR else 'ltr'}; }}
h1 {{ font-size: 17pt; color: #1F3864; margin: 0 0 6pt; border-bottom: 2px solid #1F3864; padding-bottom: 4pt; break-after: avoid; }}
h2 {{ font-size: 12.5pt; color: #1F3864; margin: 14pt 0 5pt; break-after: avoid; }}
h3 {{ font-size: 10.5pt; color: #2E5597; margin: 10pt 0 4pt; break-after: avoid; }}
p {{ margin: 0 0 6pt; text-align: justify; }}
.sec {{ break-before: page; }}
table {{ width: 100%; border-collapse: collapse; margin: 4pt 0 10pt; font-size: {'9pt' if AR else '8.3pt'}; }}
th {{ background: #1F3864; color: #fff; padding: 4pt 5pt; text-align: {'right' if AR else 'left'}; font-weight: 600; }}
td {{ border: 0.6pt solid #C9D3E3; padding: 3.5pt 5pt; vertical-align: top; }}
tr:nth-child(even) td {{ background: #F6F8FC; }}
tr {{ break-inside: avoid; }}
.ltr {{ direction: ltr; unicode-bidi: isolate; text-align: left; font-family: Inter, sans-serif; }}
.q {{ direction: ltr; unicode-bidi: isolate; text-align: left; font-family: Inter, sans-serif; font-size: 8pt; color: #333; background: #F3F3F3; border-{'right' if AR else 'left'}: 3px solid #9E9E9E; padding: 3pt 6pt; margin: 3pt 0; display: block; }}
.kpis {{ display: flex; gap: 8pt; margin: 8pt 0 10pt; }}
.kpi {{ flex: 1; border: 1px solid #C9D3E3; border-top: 4px solid #1F3864; padding: 6pt; text-align: center; }}
.kpi .v {{ font-size: 18pt; font-weight: 700; color: #1F3864; font-family: Inter, sans-serif; }}
.kpi .l {{ font-size: 8pt; color: #555; }}
.p0 {{ background: #FFC7CE; color: #9C0006; font-weight: 700; padding: 0 4pt; border-radius: 2pt; font-family: Inter; }}
.p1 {{ background: #FFEB9C; color: #7F4F00; font-weight: 700; padding: 0 4pt; border-radius: 2pt; font-family: Inter; }}
.p2 {{ background: #DDEBF7; color: #1F3864; font-weight: 700; padding: 0 4pt; border-radius: 2pt; font-family: Inter; }}
.p3 {{ background: #E2EFDA; color: #375623; font-weight: 700; padding: 0 4pt; border-radius: 2pt; font-family: Inter; }}
.card {{ border: 1px solid #C9D3E3; border-{'right' if AR else 'left'}: 4px solid #1F3864; padding: 6pt 8pt; margin: 0 0 8pt; break-inside: avoid; }}
.card .h {{ font-weight: 700; color: #1F3864; }}
.meta {{ font-size: 8pt; color: #555; }}
.status {{ border: 2px solid #9C0006; color: #9C0006; padding: 6pt 8pt; font-weight: 600; margin: 8pt 0; }}
.note {{ background: #FFF8E1; border: 1px solid #F0D58C; padding: 6pt 8pt; margin: 8pt 0; font-size: 8.8pt; }}
figure {{ margin: 6pt 0 12pt; break-inside: avoid; }}
figure img {{ width: 100%; border: 1px solid #BFBFBF; }}
figcaption {{ font-size: 8pt; color: #444; margin-top: 2pt; }}
.cover {{ page: cover; height: 287mm; overflow: hidden; position: relative; box-sizing: border-box; padding: 48mm 22mm 0; background: linear-gradient(180deg,#fff 0,#fff 74%,#1F3864 74%); }}
.cover .t {{ font-size: 25pt; font-weight: 700; color: #1F3864; line-height: 1.25; }}
.cover .s {{ font-size: 13pt; color: #2E5597; margin-top: 8pt; }}
.cover .m {{ margin-top: 26mm; font-size: 10pt; line-height: 1.9; }}
.cover .w {{ color: #fff; position: absolute; bottom: 22mm; left: 22mm; right: 22mm; font-size: 9.5pt; line-height: 1.6; }}
.small {{ font-size: 8pt; }}
"""
H.append(f'<!doctype html><html lang="{L}" dir="{"rtl" if AR else "ltr"}"><head><meta charset="utf-8"><title>{T("PMU Admissions Office — Content Review Report", "تقرير مراجعة محتوى مكتب القبول")}</title><style>{css}</style></head><body>')
# ---------------- cover
H.append(f'''<div class="cover"><div class="t">{T('Admissions Office Webpages', 'صفحات مكتب القبول')}<br>{T('Independent Content Review', 'مراجعة مستقلة للمحتوى')}</div>
<div class="s">{T('Prince Mohammad Bin Fahd University (PMU) — Prepared for Management Review', 'جامعة الأمير محمد بن فهد — معد للمراجعة الإدارية')}</div>
<div class="m"><b>{T('Prepared for', 'معد لـ')}:</b> Mr. Radhi H. Alkhaldi, Associate Director of Enrollment<br>
<b>{T('Prepared by', 'إعداد')}:</b> {T('Nader Al Farhan, Administrative Assistant | Student Affairs', 'نادر الفرحان، مساعد إداري | شؤون الطلاب')}<br>
<b>{T('Root source', 'المصدر الجذري')}:</b> <span class="ltr">https://www.pmu.edu.sa/admission/admission</span><br>
<b>{T('Observation', 'تاريخ الرصد')}:</b> <span class="ltr">{D['obs_at']}</span> {T('(baseline reads 10–11 Oct 2026)', '(قراءات الأساس 10–11 أكتوبر 2026)')}<br>
<b>{T('Companion register', 'السجل المرافق')}:</b> <span class="ltr">{T('L2-01_Evidence_and_Follow-up_Pack_EN.xlsx', 'L2-01_Evidence_and_Follow-up_Pack_AR.xlsx')}</span><br>
<b>{T('Status', 'الحالة')}:</b> {T('Prepared for Management Review — not an approval, publication confirmation or closure certificate', 'معد للمراجعة الإدارية — لا يمثل اعتمادًا أو تأكيد نشر أو شهادة إغلاق')}</div>
<div class="w">{T('Read-only review of published content. No website content was changed, no forms were submitted and no applicant systems were accessed.', 'مراجعة قراءة فقط للمحتوى المنشور. لم يُعدَّل أي محتوى في الموقع، ولم تُرسل نماذج، ولم يُدخل إلى أنظمة المتقدمين.')}</div></div>''')

# ---------------- 1 executive summary
H.append(f'<div class="sec"><h1>1. {T("Executive summary", "الملخص التنفيذي")}</h1>')
H.append(f'''<div class="kpis"><div class="kpi"><div class="v">{C['eligible']}</div><div class="l">{T('eligible resources examined', 'موردًا مؤهلًا فُحص')}</div></div>
<div class="kpi"><div class="v">{S['n']}</div><div class="l">{T('consolidated findings', 'ملاحظة موحدة')}</div></div>
<div class="kpi"><div class="v" style="color:#9C0006">{P('P0')} | {P('P1')}</div><div class="l">{T('P0 | P1 findings', 'ملاحظات P0 | P1')}</div></div>
<div class="kpi"><div class="v">{S['conflicts']}</div><div class="l">{T('proven published conflicts', 'تعارضًا منشورًا مثبتًا')}</div></div>
<div class="kpi"><div class="v">{len(D['decisions'])}</div><div class="l">{T('decisions requested', 'قرارات مطلوبة')}</div></div></div>''')
H.append('<p>' + T(
 f"The published content of the Admissions Office page, its five sections, their {C['root_unique']} direct destinations and the files and fee pages needed for verification were reviewed line by line and re-checked on the live website on 21 October 2026. The review recorded {S['n']} findings ({P('P0')} P0, {P('P1')} P1, {P('P2')} P2, {P('P3')} P3), including {S['conflicts']} proven published conflicts, together with {len(D['strengths'])} evidenced strengths. The content is substantial and largely structured by applicant category; the principal weaknesses lie in currency, consistency across pages and the absence of a single authoritative source for fees and requirements.",
 f"رُوجع المحتوى المنشور لصفحة مكتب القبول وأقسامها الخمسة ووجهاتها المباشرة الـ{C['root_unique']} والملفات وصفحات الرسوم اللازمة للتحقق سطرًا بسطر، وأُعيد التحقق منه على الموقع الحي في 21 أكتوبر 2026. ورُصدت {S['n']} ملاحظة ({P('P0')} من P0، و{P('P1')} من P1، و{P('P2')} من P2، و{P('P3')} من P3)، منها {S['conflicts']} تعارضًا منشورًا مثبتًا، إلى جانب {len(D['strengths'])} نقاط قوة موثقة. والمحتوى وافٍ ومنظم في معظمه حسب فئة المتقدم، وتتركز نقاط الضعف الرئيسة في الحداثة والاتساق بين الصفحات وغياب مصدر موحد معتمد للرسوم والمتطلبات.") + '</p>')
H.append(f'<h3>{T("Principal findings (P0)", "أبرز الملاحظات (P0)")}</h3><ul>')
for f in ['F-014', 'F-039', 'F-052', 'F-040']:
    r = byid[f]; H.append(f'<li><b>{e(T(r["title_en"], r["title_ar"]))}</b> ({f}) — {e(T(r["description_en"], r["description"]))}</li>')
H.append('</ul>')
H.append(f'<h3>{T("Also material (P1, selected)", "ملاحظات جوهرية أخرى (P1، مختارة)")}</h3><ul>')
for f in ['F-073', 'F-100', 'F-097', 'F-036', 'F-005', 'F-035', 'F-023']:
    r = byid[f]; H.append(f'<li><b>{e(T(r["title_en"], r["title_ar"]))}</b> ({f})</li>')
H.append('</ul>')
H.append(f'<h3>{T("Decisions requested from management", "القرارات المطلوبة من الإدارة")}</h3><p>' + T(
 'Ten institutional decisions are set out in Section 9 (D-01 to D-10). The most time-sensitive are D-01 (application fees and VAT basis by applicant category), D-02 (current admission cycle and interim notice) and D-03/D-04 (undergraduate and graduate eligibility and English requirements). Where pages conflict, this report does not select a value: each conflict is stated as "Proven published conflict; the correct policy requires institutional confirmation."',
 'تعرض الفقرة 9 عشرة قرارات مؤسسية (D-01 إلى D-10)، أكثرها إلحاحًا: D-01 (رسوم التقديم وأساس الضريبة حسب فئة المتقدم)، وD-02 (دورة القبول الحالية والإشعار المؤقت)، وD-03/D-04 (أهلية البكالوريوس والدراسات العليا ومتطلبات اللغة). وحيث تتعارض الصفحات لا يختار هذا التقرير قيمة بعينها، بل يُثبت كل تعارض بصيغة: «تعارض منشور مثبت؛ السياسة الصحيحة تحتاج تأكيدًا مؤسسيًا».') + '</p>')
am_nr = sum(1 for a in D['amend'] if a['code'] == 'NOT_PUBLISHED'); am_pr = sum(1 for a in D['amend'] if a['code'] == 'PARTIALLY_PUBLISHED')
H.append('<p>' + T(f'Of the six amendments requested in this correspondence on 26 October 2025, {am_nr} are NOT_PUBLISHED and {am_pr} are PARTIALLY_PUBLISHED (Annex A); none is fully published.',
                   f'ومن التعديلات الستة المطلوبة في هذه المراسلات بتاريخ 26 أكتوبر 2025، حالة {am_nr} منها NOT_PUBLISHED و{am_pr} PARTIALLY_PUBLISHED (الملحق أ)؛ ولم يُنشر أيٌّ منها كاملًا.') + '</p>')
H.append(f'<div class="status">{T("Audit status: NOT READY FOR VERIFIED CLOSURE", "حالة التدقيق: NOT READY FOR VERIFIED CLOSURE (غير جاهز للإغلاق المتحقق منه)")}<br><span style="font-weight:400">' + T(
 'Inventory and examination of the discovered scope are complete; closure is not possible while conflicting policy values await institutional confirmation, two items remain unverifiable from published content, no applicant data or feedback was available, and no correction has yet been published. The package is Prepared for Management Review.',
 'اكتمل جرد النطاق المكتشف وفحصه؛ ويتعذر الإغلاق ما دامت القيم المتعارضة تنتظر تأكيدًا مؤسسيًا، وبقي بندان يتعذر التحقق منهما من المحتوى المنشور، ولم تتوفر بيانات أو آراء للمتقدمين، ولم يُنشر أي تصحيح بعد. أما الحزمة نفسها فمعدّة للمراجعة الإدارية.') + '</span></div></div>')

# ---------------- 2 scope & method
H.append(f'<div class="sec"><h1>2. {T("Scope, date, method and limits", "النطاق والتاريخ والمنهج والحدود")}</h1>')
H.append(f'<h3>{T("Scope", "النطاق")}</h3><p>' + T(
 'Start point: https://www.pmu.edu.sa/admission/admission. In scope: the five sections listed on the root page (Future Students; International Students’ Office; Graduate Admissions; Undergraduate Admissions; Undergraduate Placement Tests), every destination they link to directly, the bilingual content of /apply, the public landing page of the application portal, the two linked PDF guides, and nine adjacent official pages used only to verify specific statements (fee schedules, the generic graduate application form, the MIBL application form, the list of majors, the 2021/2022 calendar opened by the footer link, and the preparatory study plan). Global header and footer menus were not treated as admissions branches.',
 'نقطة البداية: https://www.pmu.edu.sa/admission/admission. يشمل النطاق: الأقسام الخمسة في الصفحة الجذرية (الطلاب المستقبليون؛ مكتب الطلاب الدوليين؛ القبول في الدراسات العليا؛ القبول في البكالوريوس؛ اختبارات تحديد المستوى)، وكل وجهة مرتبطة بها مباشرة، والمحتوى ثنائي اللغة لصفحة /apply، والصفحة العامة لبوابة التقديم، ودليلي PDF المرتبطين، وتسع صفحات رسمية مجاورة استُخدمت للتحقق من معلومات محددة فقط (جداول الرسوم، ونموذج التقديم العام للدراسات العليا، ونموذج تقديم MIBL، وقائمة التخصصات، وتقويم 2021/2022 الذي يفتحه رابط التذييل، والخطة الدراسية للبرنامج التحضيري). ولم تُعامل قوائم الرأس والتذييل العامة كفروع للقبول.') + '</p>')
H.append(f'<h3>{T("Method", "المنهج")}</h3><ul>' + ''.join(f'<li>{x}</li>' for x in (T(
 ['Discovery and capture: automated Chromium (Playwright) navigation from the root page, read-only GET requests only; full-page captures and visible/hidden text of every page; status checks of all 434 unique URLs linked from in-scope pages.',
  'Line-by-line reading of every content unit against six axes: language, accuracy, function, organisation, consistency and applicant experience; PDF text extraction with visual checks of informative images.',
  'Evidence: each finding quotes the published text verbatim with its URL and location; each proven conflict is documented by at least two sources; key findings carry highlighted screenshots of the live page taken on 21 Oct 2026.',
  'Re-verification: on 21 Oct 2026 the verbatim text of every finding was re-matched against a fresh capture; changed items are flagged rather than silently removed.',
  'Classification and priority follow the nine-type classification of the Master Directive and the P0–P3 scale (Definitions sheet); verification statuses are VERIFIED, BLOCKED or NOT_APPLICABLE. AI-assisted tools (Claude) supported reading, matching, translation and drafting; results were checked against the captured evidence.'],
 ['الاكتشاف والالتقاط: تصفح آلي عبر Chromium (Playwright) من الصفحة الجذرية بطلبات قراءة فقط؛ ولقطات كاملة ونصوص ظاهرة ومخفية لكل صفحة؛ وفحص حالة 434 رابطًا فريدًا من صفحات النطاق.',
  'قراءة كل وحدة محتوى سطرًا بسطر على ستة محاور: اللغة والدقة والوظيفة والتنظيم والاتساق وتجربة المتقدم؛ واستخراج نصوص PDF مع فحص بصري للصور المعلوماتية.',
  'الأدلة: كل ملاحظة تقتبس النص المنشور حرفيًا مع رابطه وموضعه؛ وكل تعارض مثبت موثق بمصدرين على الأقل؛ وللملاحظات الرئيسة لقطات مظللة من الصفحة الحية بتاريخ 21 أكتوبر 2026.',
  'إعادة التحقق: في 21 أكتوبر 2026 طوبق النص الحرفي لكل ملاحظة مع لقطة جديدة؛ ووُسمت البنود المتغيرة بدل حذفها.',
  'التصنيف والأولوية وفق التصنيف التساعي للأمر الموحد وسلم P0–P3 (ورقة التعريفات)؛ وحالات التحقق VERIFIED أو BLOCKED أو NOT_APPLICABLE. واستُعين بأدوات الذكاء الاصطناعي (Claude) في القراءة والمطابقة والترجمة والصياغة، مع التحقق من النتائج مقابل الأدلة الملتقطة.']))) + '</ul>')
H.append(f'<h3>{T("Limits and exclusions", "الحدود والاستبعادات")}</h3><ul>' + ''.join(f'<li>{x}</li>' for x in T(
 ['No security, vulnerability, performance or load testing; no form submission or data entry; no login to the applicant portal or internal systems; no access to applicant records; no change to the website; no contact with staff or applicants.',
  'The portal was reviewed only as a published referral destination (public landing page); its registration labels were read from the published script bundle, and four labels loaded dynamically could not be verified.',
  'External, social-media and internal hosts returned no response from the review network (status 000); this is recorded as an environment limit, not as a public failure. The http:// portal link (F-131) is recorded as unverifiable for the same reason.',
  'The staff list linked as "Contact Us" was checked only for its destination because it contains personal data.',
  'Published procedures were assessed as stated; their operational application was not verified.'],
 ['لا اختبارات أمن أو ثغرات أو أداء أو تحميل؛ ولا إرسال نماذج أو إدخال بيانات؛ ولا دخول إلى بوابة المتقدمين أو الأنظمة الداخلية؛ ولا وصول إلى سجلات المتقدمين؛ ولا تعديل على الموقع؛ ولا تواصل مع موظفين أو متقدمين.',
  'رُوجعت البوابة بوصفها وجهة إحالة منشورة فقط (الصفحة العامة)؛ وقُرئت تسميات التسجيل من ملف البرمجة المنشور، وتعذر التحقق من أربع تسميات تُحمَّل ديناميكيًا.',
  'لم تستجب النطاقات الخارجية ومواقع التواصل والأنظمة الداخلية من شبكة المراجعة (الحالة 000)؛ وسُجل ذلك قيدًا في بيئة المراجعة لا عطلًا لدى الجمهور. وسُجل رابط البوابة http (F-131) متعذر التحقق للسبب نفسه.',
  'فُحصت وجهة رابط «Contact Us» فقط لأن قائمة الموظفين تحتوي بيانات شخصية.',
  'قُيّمت الإجراءات المنشورة كما هي معلنة؛ ولم يُتحقق من تطبيقها التشغيلي.'])) + '</ul></div>')

# ---------------- 3 coverage
H.append(f'<div class="sec"><h1>3. {T("Coverage", "التغطية")}</h1><table><tr><th>{T("Measure", "المقياس")}</th><th>{T("Value", "القيمة")}</th></tr>')
for a, b in [(T('Root-page link placements / unique destinations', 'روابط الصفحة الجذرية / الوجهات الفريدة'), f"{C['root_placements']} / {C['root_unique']}"),
             (T('Eligible resources', 'الموارد المؤهلة'), C['eligible']), (T('Fully examined', 'مفحوصة بالكامل'), C['full']), (T('Partially examined', 'مفحوصة جزئيًا'), C['partial']),
             (T('Unreachable / not examined', 'تعذر الوصول / لم يُفحص'), '0 / 0'), (T('Coverage: full | any examination', 'التغطية: كاملة | أي فحص'), f"{C['pct_full']}% | {C['pct_any']}%"),
             (T('Link instances / unique URLs checked', 'روابط مرصودة / فريدة فُحصت'), f"{C['links_instances']} / {C['links_unique']}"), (T('Confirmed HTTP 404', 'روابط 404 مؤكدة'), len(C['broken'])),
             (T('PDF files / pages read', 'ملفات PDF / صفحات مقروءة'), f"{C['pdfs']} / {C['pdf_pages']}"), (T('Language pairs compared', 'أزواج لغوية مقارنة'), 10)]:
    H.append(f'<tr><td>{a}</td><td class="ltr">{b}</td></tr>')
H.append('</table><p class="small">' + T('Coverage percentages refer to the eligible resources discovered from the root page; they are not a claim about the whole website. Partial items: staff list (personal data), portal (public page only), Aptis guide images, and the preparatory study plan (read 11 Oct, not re-read).',
 'نسب التغطية تخص الموارد المؤهلة المكتشفة من الصفحة الجذرية، وليست ادعاءً بشأن الموقع كله. البنود الجزئية: قائمة الموظفين (بيانات شخصية)، والبوابة (الصفحة العامة فقط)، وصور دليل Aptis، والخطة الدراسية للتحضيري (قُرئت في 11 أكتوبر ولم يُعد فحصها).') + '</p>')
H.append(f'<h3>{T("Findings by category and priority", "الملاحظات حسب التصنيف والأولوية")}</h3><table><tr><th>{T("Category", "التصنيف")}</th><th>P0</th><th>P1</th><th>P2</th><th>P3</th><th>{T("Total", "المجموع")}</th></tr>')
cc = collections.Counter((r['category'], r['plevel']) for r in R)
for k, v in D['cat'].items():
    if k == 'STRENGTH': continue
    row = [cc[(k, p)] for p in ('P0', 'P1', 'P2', 'P3')]
    if sum(row): H.append(f'<tr><td>{T(v[0], v[1])}</td>' + ''.join(f'<td class="ltr">{x}</td>' for x in row) + f'<td class="ltr"><b>{sum(row)}</b></td></tr>')
H.append(f'<tr><td><b>{T("Total", "المجموع")}</b></td>' + ''.join(f'<td class="ltr"><b>{P(p)}</b></td>' for p in ('P0', 'P1', 'P2', 'P3')) + f'<td class="ltr"><b>{S["n"]}</b></td></tr></table>')
rv = S['rv']
H.append('<p class="small">' + T(f"Re-verification on 21 Oct 2026: {rv.get('MATCH',0)} still published as quoted; {rv.get('PARTLY_CHANGED',0)} partly changed; {rv.get('RESOLVED',0)} appears resolved (F-019); {rv.get('NOT_VERIFIABLE',0)} not verifiable from published content; {rv.get('NOT_RETESTED',0)} not re-tested (mobile layout).",
 f"إعادة التحقق في 21 أكتوبر 2026: {rv.get('MATCH',0)} ما زالت منشورة كما اقتُبست؛ و{rv.get('PARTLY_CHANGED',0)} تغيرت جزئيًا؛ و{rv.get('RESOLVED',0)} يبدو أنها عولجت (F-019)؛ و{rv.get('NOT_VERIFIABLE',0)} يتعذر التحقق منها من المحتوى المنشور؛ و{rv.get('NOT_RETESTED',0)} لم يُعد اختبارها (عرض الجوال).") + '</p></div>')

# ---------------- 4 strengths
H.append(f'<div class="sec"><h1>4. {T("Proven strengths", "نقاط القوة المثبتة")}</h1><table><tr><th>ID</th><th>{T("Strength", "نقطة القوة")}</th><th>{T("Evidence (verbatim)", "الدليل (حرفيًا)")}</th></tr>')
for s in D['strengths']:
    H.append(f'<tr><td class="ltr">{s["sid"]}</td><td>{e(T(s["en"], s["ar"]))}<div class="meta">{e(T(s["page_en"], s["page_ar"]))}</div></td><td><span class="q">{e(s["excerpt"])}</span></td></tr>')
H.append('</table></div>')

# ---------------- 5 material findings
H.append(f'<div class="sec"><h1>5. {T("Material findings, impact and evidence", "الملاحظات الجوهرية وأثرها وأدلتها")}</h1><p>' + T('All P0 and P1 findings are summarised below; the complete set of findings, with full evidence, is in the register (Findings and Evidence sheets).', 'تُلخَّص أدناه جميع ملاحظات P0 وP1؛ والمجموعة الكاملة بأدلتها في السجل (ورقتا الملاحظات والأدلة).') + '</p>')
for r in [x for x in R if x['plevel'] in ('P0', 'P1')]:
    q = r['current_text'] if len(r['current_text']) < 420 else r['current_text'][:420] + ' …'
    H.append(f'''<div class="card"><div class="h"><span class="{r['plevel'].lower()}">{r['plevel']}</span> {r['fid']} — {e(T(r['title_en'], r['title_ar']))}</div>
<div class="meta">{e(T(r['page_en'], r['page_ar']))} · {e(T(r['cat_en'], r['cat_ar']))} · {T('Decision', 'القرار')}: {', '.join(r['dids']) or '—'} · {T('Evidence', 'الأدلة')}: {', '.join(r['eids'])} · {e(T(r['rv_en'], r['rv_ar']))}</div>
<p>{e(T(r['description_en'], r['description']))}</p>{('<p><b>' + e(T(r['conflict_statement'], r['conflict_ar'])) + '</b></p>') if r.get('conflict_ar') else ''}
<span class="q">{e(q)}</span><p><b>{T('Proposed action', 'الإجراء المقترح')}:</b> {e(T(r['recommendation_en'], r.get('recommendation_ar') or r['recommendation']))}</p></div>''')
H.append(f'<h2>{T("Evidence figures (live pages, 21 October 2026)", "أشكال الأدلة (الصفحات الحية، 21 أكتوبر 2026)")}</h2>')
FIG = [('EV-01', 'F-014', 'Admissions Calendar — the only published cycle is Fall 2026-2027', 'تقويم القبول — الدورة الوحيدة المنشورة خريف 2026-2027'),
       ('EV-14', 'F-030', 'Application portal — "No events are currently published"', 'بوابة التقديم — «No events are currently published»'),
       ('EV-02', 'F-039', 'International Students — SAR 500 (excl. VAT) for transfer/visiting', 'الطلاب الدوليون — 500 ريال (غير شاملة الضريبة) للمحولين والزائرين'),
       ('EV-03', 'F-039', 'Transfer admission — SAR 950 (incl. VAT)', 'القبول بالتحويل — 950 ريالًا (شاملة الضريبة)'),
       ('EV-05', 'F-052', 'College of Medicine — SAR 1000 (incl. VAT)', 'كلية الطب — 1000 ريال (شاملة الضريبة)'),
       ('EV-06', 'F-052', 'Medical Program Fees — SAR 1,150 (VAT inclusive)', 'رسوم البرنامج الطبي — 1,150 ريالًا (شاملة الضريبة)'),
       ('EV-04', 'F-040', 'International Students — SAT II weighted at 30%', 'الطلاب الدوليون — SAT II بوزن 30%'),
       ('EV-07', 'F-073', 'Generic graduate application form — IELTS 6.5', 'نموذج التقديم العام للدراسات العليا — IELTS 6.5'),
       ('EV-08', 'F-073', 'MSEE requirements — IELTS 6.0', 'متطلبات MSEE — IELTS 6.0'),
       ('EV-12', 'F-100', 'MIBL requirements — IELTS 6.5', 'متطلبات MIBL — IELTS 6.5'),
       ('EV-13', 'F-100', 'MIBL application form — IELTS 6.0', 'نموذج تقديم MIBL — IELTS 6.0'),
       ('EV-09', 'F-097', 'EMGMS requirements — endorsement from "UA Center for English as Second Language (CESL)"', 'متطلبات EMGMS — «UA Center for English as Second Language (CESL)»'),
       ('EV-10', 'F-119', 'Other Fees — APTIS Exam Fees SAR 575', 'الرسوم الأخرى — رسوم اختبار APTIS ‏575 ريالًا'),
       ('EV-11', 'F-005', 'Footer "Academic Calendar" target — Academic Year 2021/2022', 'وجهة رابط «Academic Calendar» في التذييل — العام الأكاديمي 2021/2022')]
for i, (ev, f, cen, car) in enumerate(FIG, 1):
    H.append(f'<figure><img src="file://{EV}/{ev}.png"><figcaption>{T("Figure", "الشكل")} {i} ({ev}, {f}): {e(T(cen, car))}. {T("Highlight added by the reviewer; captured", "التظليل من المراجع؛ التُقطت")} 2026-10-21.</figcaption></figure>')
H.append('</div>')

# ---------------- 6 information quality & journey
J = [(T('Choose a programme', 'اختيار البرنامج'), T('Programme lists differ between the root page, Degrees & Programs, Graduate Programs, International Students and the fees pages; Medicine, EMGMS and one priced master’s programme are missing from some lists; B.S. Chemical Engineering appears in programme lists but not in the special-requirements list.', 'تختلف قوائم البرامج بين الصفحة الجذرية والدرجات والبرامج وبرامج الدراسات العليا والطلاب الدوليين وصفحات الرسوم؛ ويغيب الطب وEMGMS وبرنامج ماجستير مسعّر عن بعض القوائم؛ وتظهر الهندسة الكيميائية في قوائم البرامج دون قائمة المتطلبات الخاصة.'), 'F-012, F-043, F-048, F-070, F-074, F-104'),
     (T('Understand requirements', 'فهم المتطلبات'), T('Requirements are spread across /apply (hidden by an immediate redirect), the undergraduate, CS & Engineering, international and test pages. Substitution rules (SAT 1 1200), English thresholds (IELTS 6.0/6.5; TOEFL) and the discontinued SAT II differ between pages.', 'تتوزع المتطلبات بين /apply (المخفية بإعادة توجيه فورية) وصفحات البكالوريوس والحاسب والهندسة والدوليين والاختبارات. وتختلف قواعد الإحلال (SAT 1 بدرجة 1200) وحدود اللغة (IELTS 6.0/6.5؛ TOEFL) واشتراط SAT II الموقوف بين الصفحات.'), 'F-023, F-024, F-040, F-059, F-073, F-100, F-117'),
     (T('Find fees and dates', 'معرفة الرسوم والمواعيد'), T('Application fees conflict (SAR 500/950; 1,000/1,150); the only admission calendar is expired; the footer calendar link opens 2021/2022; payment schedules for completed terms remain listed.', 'تتعارض رسوم التقديم (500/950؛ 1,000/1,150)؛ والتقويم الوحيد منتهٍ؛ ورابط التقويم في التذييل يفتح 2021/2022؛ وجداول السداد لفصول منتهية ما زالت معروضة.'), 'F-039, F-052, F-014, F-005, F-111'),
     (T('Apply and follow up', 'التقديم والمتابعة'), T('Channels differ (Qabool for Medicine; PMU portal elsewhere); the portal states that no events are published; "Contact Us" leads to a staff list without an Admissions contact; the enquiry form shows no privacy notice. The journey was followed only to the portal boundary.', 'تختلف القنوات (قبول للطب؛ وبوابة الجامعة لغيره)؛ وتذكر البوابة أنه لا توجد أحداث منشورة؛ ويقود «Contact Us» إلى قائمة موظفين دون جهة اتصال للقبول؛ ولا يعرض نموذج الاستفسار إشعار خصوصية. وتُتبعت الرحلة حتى حدود البوابة فقط.'), 'F-053, F-030, F-002, F-034, F-020')]
H.append(f'<div class="sec"><h1>6. {T("Quality of published information, procedures and the applicant information journey", "جودة المعلومات والإجراءات المنشورة ورحلة المتقدم في الوصول إلى المعلومات")}</h1><p>' + T(
 'Assessment is based on published content. It describes how the information journey reads to an applicant; it does not report actual applicant experience, and it does not infer how procedures are applied internally.',
 'يستند التقييم إلى المحتوى المنشور. ويصف كيف تبدو رحلة المعلومات للمتقدم؛ ولا ينقل تجربة متقدمين فعلية، ولا يستنتج كيفية تطبيق الإجراءات داخليًا.') + '</p>')
H.append(f'<table><tr><th>{T("Journey step", "خطوة الرحلة")}</th><th>{T("Observation (content-based)", "الملاحظة (مستندة إلى المحتوى)")}</th><th>{T("Findings", "الملاحظات")}</th></tr>')
for a, b, c in J: H.append(f'<tr><td><b>{a}</b></td><td>{b}</td><td class="ltr">{c}</td></tr>')
H.append('</table>')
H.append(f'<h3>{T("Assessment by quality dimension", "التقييم حسب أبعاد الجودة")}</h3><ul>' + ''.join(f'<li>{x}</li>' for x in T(
 ['Accuracy and currency — weakest dimension: an expired cycle, a 2018 guide, a 2021/2022 calendar link, a discontinued test and conflicting fees.',
  'Consistency — the same requirement is restated on several pages with different values or wording; there is no single source of truth for fees, tests or programme lists.',
  'Completeness — key items are missing in places (Admissions contact details, TOEFL minimum on undergraduate pages, MIBL GPA and documents, Aptis scores and fees).',
  'Clarity and organisation — content is generally organised by applicant category, which is a sound structure; editorial errors are frequent but low in impact.',
  'Arabic–English — /apply mirrors English and Arabic with matching values; no separate Arabic version of the section was found.'],
 ['الدقة والحداثة — أضعف الأبعاد: دورة منتهية، ودليل 2018، ورابط تقويم 2021/2022، واختبار موقوف، ورسوم متعارضة.',
  'الاتساق — يتكرر المتطلب نفسه في عدة صفحات بقيم أو صياغات مختلفة؛ ولا يوجد مصدر موحد للرسوم أو الاختبارات أو قوائم البرامج.',
  'الاكتمال — تغيب عناصر أساسية في مواضع (بيانات تواصل القبول، والحد الأدنى لـTOEFL في صفحات البكالوريوس، ومعدل MIBL ووثائقه، ودرجات Aptis ورسومه).',
  'الوضوح والتنظيم — المحتوى منظم عمومًا حسب فئة المتقدم وهي بنية سليمة؛ والأخطاء التحريرية كثيرة لكنها محدودة الأثر.',
  'العربية والإنجليزية — تعرض /apply النصين بقيم متطابقة؛ ولم يُعثر على نسخة عربية مستقلة للقسم.'])) + '</ul></div>')

# ---------------- 7 data & feedback
H.append(f'<div class="sec"><h1>7. {T("Data and applicant feedback", "تحليل البيانات وآراء المتقدمين")}</h1><p>' + T(
 'No published aggregate admissions data (application volumes, processing times, conversion) and no published or supplied applicant-feedback summaries were found within the inventoried scope. Consequently no quantitative indicator is reported and no rate was calculated. Statements about the applicant journey in this report are content-based observations, not reported experience.',
 'لم يُعثر ضمن نطاق الجرد على بيانات قبول إجمالية منشورة (أعداد الطلبات ومدد المعالجة ونسب التحويل)، ولا على ملخصات منشورة أو مقدمة لآراء المتقدمين. ولذلك لا يُعرض أي مؤشر كمي ولم تُحسب أي نسبة. وما يرد عن رحلة المتقدم ملاحظات مستندة إلى المحتوى لا تجربة مرصودة.') + '</p>')
H.append(f'<h3>{T("Proposed design for future evidence (not executed)", "تصميم مقترح لجمع الأدلة مستقبلًا (لم يُنفذ)")}</h3><ol>' + ''.join(f'<li>{x}</li>' for x in T(
 ['Web analytics per admission cycle: page views, exits and internal search terms for admissions pages.', 'Enquiry log: monthly categorisation of Admission Query topics to show which information applicants cannot find.',
  'Short anonymous post-application survey (six items: findability of requirements, fees, dates and channel; clarity; confidence).', 'Review of the results before each cycle opens. Requires separate authorisation, privacy review and owner approval.'],
 ['تحليلات الموقع لكل دورة قبول: مشاهدات صفحات القبول ونقاط الخروج ومصطلحات البحث الداخلي.', 'سجل الاستفسارات: تصنيف شهري لموضوعات نموذج الاستفسار لمعرفة المعلومات التي لا يجدها المتقدمون.',
  'استبيان قصير مجهول الهوية بعد التقديم (ستة بنود: سهولة العثور على المتطلبات والرسوم والمواعيد والقناة؛ الوضوح؛ الثقة).', 'مراجعة النتائج قبل فتح كل دورة. ويتطلب ذلك تكليفًا مستقلًا ومراجعة خصوصية واعتماد المالك.'])) + '</ol></div>')

# ---------------- 8 recommendations
REC = [('P0', T('Interim notice on the admission cycle; single fee reference by applicant category; removal or replacement of the SAT II requirement after confirmation.', 'إشعار مؤقت بحالة دورة القبول؛ ومرجع رسوم موحد حسب الفئة؛ وإزالة SAT II أو استبداله بعد التأكيد.'), T('Prevents applicants acting on expired dates or wrong fees (to be measured: zero conflicting statements on re-read).', 'يمنع اعتماد المتقدم على مواعيد منتهية أو رسوم خاطئة (يُقاس: صفر تعارضات عند إعادة القراءة).')),
       ('P1', T('Approved undergraduate and graduate admission matrices referenced by every page; removal of non-PMU text (EMGMS); withdrawal or replacement of the 2018 guide; one authoritative programme list; official Admissions contact block and privacy notice.', 'مصفوفتا قبول معتمدتان للبكالوريوس والدراسات العليا تحيل إليهما الصفحات؛ وإزالة النص غير الخاص بالجامعة (EMGMS)؛ وسحب دليل 2018 أو استبداله؛ وقائمة برامج معتمدة واحدة؛ وبيانات تواصل رسمية للقبول وإشعار خصوصية.'), T('Expected to reduce contradictory guidance and enquiries (to be measured through the enquiry log).', 'يُتوقع أن يقلل الإرشادات المتناقضة والاستفسارات (يُقاس عبر سجل الاستفسارات).')),
       ('P2', T('Batch of approved editorial corrections; accessibility baseline (language attribute, image alternatives, landmarks, mobile reflow, https links); organisation of content by applicant category with a short FAQ.', 'دفعة التصحيحات التحريرية المعتمدة؛ والحد الأدنى للإتاحة (سمة اللغة، بدائل الصور، المعالم، الملاءمة للجوال، روابط https)؛ وتنظيم المحتوى حسب فئة المتقدم مع أسئلة شائعة موجزة.'), T('Improves clarity and access (to be measured by automated re-check and analytics).', 'يحسن الوضوح والوصول (يُقاس بإعادة الفحص الآلي والتحليلات).')),
       ('P3', T('Named owner per page, pre-cycle review, visible "last reviewed" date; applicant information-experience survey design.', 'مالك مسمى لكل صفحة، ومراجعة قبل كل دورة، وتاريخ «آخر مراجعة» ظاهر؛ وتصميم استبيان تجربة المتقدمين.'), T('Sustains accuracy over cycles (to be measured: proportion of pages reviewed before each cycle).', 'يحافظ على الدقة عبر الدورات (يُقاس: نسبة الصفحات المراجعة قبل كل دورة).'))]
H.append(f'<div class="sec"><h1>8. {T("Recommendations for correction and development, by priority", "توصيات التصحيح والتطوير مرتبة بالأولوية")}</h1><table><tr><th>{T("Priority", "الأولوية")}</th><th>{T("Recommendation", "التوصية")}</th><th>{T("Expected benefit (to be measured)", "الفائدة المتوقعة (تحتاج قياسًا)")}</th></tr>')
for p, a, b in REC: H.append(f'<tr><td><span class="{p.lower()}">{p}</span></td><td>{a}</td><td>{b}</td></tr>')
H.append('</table><p class="small">' + T('Recommendations are proposals and do not represent approved decisions or management commitments. Where a recommendation depends on a policy value, it is conditional on the decision listed in Section 9.', 'التوصيات مقترحات ولا تمثل قرارات معتمدة أو التزامات إدارية. وحيث تتوقف التوصية على قيمة سياسة فهي مشروطة بالقرار الوارد في الفقرة 9.') + '</p></div>')

# ---------------- 9 decisions
H.append(f'<div class="sec"><h1>9. {T("Institutional decisions requested", "القرارات المؤسسية المطلوبة")}</h1><table><tr><th>ID</th><th>{T("Question", "السؤال")}</th><th>{T("Options", "البدائل")}</th><th>{T("Proposed owner", "الجهة المقترحة")}</th><th>{T("Findings", "الملاحظات")}</th></tr>')
for d in D['decisions']:
    fl = ', '.join(d['fids']) if d['did'] != 'D-09' else T(f"{len(d['fids'])} editorial findings + {len(D['edits'])} annex corrections", f"{len(d['fids'])} ملاحظة تحريرية + {len(D['edits'])} تصحيحًا")
    H.append(f'<tr><td class="ltr"><b>{d["did"]}</b></td><td><b>{e(T(d["t_en"], d["t_ar"]))}</b><br>{e(T(d["q_en"], d["q_ar"]))}</td><td>{e(T(d["alt_en"], d["alt_ar"]))}</td><td>{e(T(d["owner_en"], d["owner_ar"]))}</td><td class="ltr small">{fl}</td></tr>')
H.append('</table><p class="small">' + T('All decisions are pending; approval fields in the register are intentionally blank. Proposed owners require confirmation.', 'جميع القرارات معلقة؛ وحقول الاعتماد في السجل فارغة عمدًا. والجهات المقترحة تحتاج تأكيدًا.') + '</p></div>')

# ---------------- 10 follow-up plan
H.append(f'<div class="sec"><h1>10. {T("Proposed follow-up plan", "خطة المتابعة المقترحة")}</h1><table><tr><th>ID</th><th>{T("Action", "الإجراء")}</th><th>{T("Priority", "الأولوية")}</th><th>{T("Decision", "القرار")}</th><th>{T("Proposed owner", "الجهة المقترحة")}</th><th>{T("Indicator", "المؤشر")}</th></tr>')
for p in D['plan']:
    H.append(f'<tr><td class="ltr">{p["aid"]}</td><td>{e(T(p["en"], p["ar"]))}</td><td><span class="{p["prio"].lower()}">{p["prio"]}</span></td><td class="ltr">{p["did"]}</td><td>{e(p["owner"])}</td><td>{e(T(p["kpi_en"], p["kpi_ar"]))}</td></tr>')
H.append('</table><p>' + T('Each action closes only after publication and a documented re-read of the affected pages. A request for approval, a local draft and a completed website update are distinct states and are tracked separately in the register.',
                          'لا يُغلق أي إجراء إلا بعد النشر وإعادة قراءة موثقة للصفحات المتأثرة. وطلب الاعتماد والمسودة المحلية والتحديث المنجز في الموقع حالات مختلفة تُتابع منفصلة في السجل.') + '</p></div>')

# ---------------- 11 gaps
H.append(f'<div class="sec"><h1>11. {T("Unexamined resources and material gaps", "الموارد غير المفحوصة والفجوات المؤثرة")}</h1><table><tr><th>{T("Gap", "الفجوة")}</th><th>{T("Effect", "الأثر")}</th><th>{T("Route to completion", "طريق الاستكمال")}</th></tr>')
G = [(T('Four portal registration labels (F-033) load dynamically and could not be read without using the form.', 'أربع تسميات في تسجيل البوابة (F-033) تُحمَّل ديناميكيًا ولم يمكن قراءتها دون استخدام النموذج.'), T('Possible spelling errors remain unconfirmed.', 'تبقى أخطاء إملائية محتملة غير مؤكدة.'), T('Manual visual check by Admissions staff.', 'فحص بصري يدوي من موظفي القبول.')),
     (T('http:// portal link (F-131) did not respond from the review network.', 'رابط البوابة http (F-131) لم يستجب من شبكة المراجعة.'), T('Primary application step may fail for some users.', 'قد تتعطل خطوة التقديم الرئيسة لبعض المستخدمين.'), T('Open the link from a public browser; replace with https.', 'فتح الرابط من متصفح عام؛ واستبداله بـhttps.')),
     (T('Staff list (personal data) checked for destination only.', 'قائمة الموظفين (بيانات شخصية) فُحصت وجهتها فقط.'), T('Accuracy of listed contacts not assessed.', 'لم تُقيَّم دقة جهات الاتصال المدرجة.'), T('Owner review.', 'مراجعة المالك.')),
     (T('Aptis Candidate Guide: text of 50 pages read; illustrations not individually inspected.', 'دليل Aptis: قُرئ نص الصفحات الخمسين؛ ولم تُفحص الرسوم كلٌّ على حدة.'), T('Limited; the guide is recommended for replacement.', 'محدود؛ ويُوصى باستبدال الدليل.'), T('Replace with current British Council resources.', 'الاستبدال بموارد المجلس الثقافي البريطاني الحالية.')),
     (T('No applicant data or feedback available.', 'لا تتوفر بيانات أو آراء للمتقدمين.'), T('Experience findings are content-based only.', 'ملاحظات التجربة مستندة إلى المحتوى فقط.'), T('Proposed design in Section 7.', 'التصميم المقترح في الفقرة 7.')),
     (T('Operational application of published procedures not verified.', 'لم يُتحقق من التطبيق التشغيلي للإجراءات المنشورة.'), T('The report does not state how procedures are applied internally.', 'لا يحدد التقرير كيفية تطبيق الإجراءات داخليًا.'), T('Owner confirmation in D-01 to D-04.', 'تأكيد المالك في D-01 إلى D-04.')),
     (T('Legacy admission pages not linked from the current root were not audited.', 'لم تُدقق صفحات القبول القديمة غير المرتبطة من الجذر الحالي.'), T('They may still be indexed by search engines.', 'قد تبقى مفهرسة في محركات البحث.'), T('Decide retirement under D-06/D-08.', 'تقرير إلغائها ضمن D-06/D-08.'))]
for a, b, c in G: H.append(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>')
H.append('</table></div>')

# ---------------- 12 references
H.append(f'<div class="sec"><h1>12. {T("References to the register and evidence", "الإحالات إلى السجل والأدلة")}</h1><table><tr><th>{T("Register sheet", "ورقة السجل")}</th><th>{T("Content", "المحتوى")}</th></tr>')
SH = [('README / Source Register', T('Order, versions, sources and their authority', 'الأمر والنسخ والمصادر وسلطتها')),
      ('Master Findings Register', T(f"{S['n']} findings F-001 … F-131 + H-1 … H-6 + V-01 … V-10 (19 mandatory fields)", f"{S['n']} ملاحظة F-001 … F-131 + H-1 … H-6 + V-01 … V-10 (19 حقلًا إلزاميًا)")),
      ('Evidence Register', T(f"{len(D['evidence'])} evidence items (E-…), live re-confirmations (RC-…), screenshots EV-01 … EV-14", f"{len(D['evidence'])} دليلًا (E-…) وإعادات تأكيد حية (RC-…) ولقطات EV-01 … EV-14")),
      ('URL & Resource Inventory / Scope Coverage Matrix', T('Resources, discovery paths, statuses and coverage by section', 'الموارد ومسارات الاكتشاف والحالات والتغطية حسب القسم')),
      ('Arabic-English Parity', T('10 pairs and search steps', '10 أزواج وخطوات البحث')), ('Historical Amendment Verification', 'H-1 … H-6'),
      ('Decision Register (= Decision & Approval Matrix)', 'D-01 … D-10'), ('Corrective Action Tracker (= Roadmap)', 'A-01 … A-13'),
      ('QC & Acceptance Matrix', 'G1 … G5'), ('Change Log; Editorial Corrections; Definitions', T(f"v1.0 … v3.0; {len(D['edits'])} corrections", f"v1.0 … v3.0؛ {len(D['edits'])} تصحيحًا"))]
for a, b in SH: H.append(f'<tr><td class="ltr">{a}</td><td>{b}</td></tr>')
H.append('</table></div>')

# ---------------- Annex A amendments
H.append(f'<div class="sec"><h1>{T("Annex A — Status of the amendments requested on 26 October 2025", "الملحق أ — حالة التعديلات المطلوبة في 26 أكتوبر 2025")}</h1><table><tr><th>ID</th><th>{T("Requested amendment", "التعديل المطلوب")}</th><th>{T("Status (21 Oct 2026)", "الحالة (21 أكتوبر 2026)")}</th><th>{T("Published evidence", "الدليل المنشور")}</th></tr>')
for a in D['amend']: H.append(f'<tr><td class="ltr">{a["hid"]}</td><td>{e(T(a["req_en"], a["req_ar"]))}</td><td class="ltr"><b>{a["code"]}</b></td><td>{e(T(a["ev_en"], a["ev_ar"]))}</td></tr>')
H.append('</table></div>')
# ---------------- Annex B index
H.append(f'<div class="sec"><h1>{T("Annex B — Index of all findings", "الملحق ب — فهرس جميع الملاحظات")}</h1><table><tr><th>ID</th><th>P</th><th>{T("Title", "العنوان")}</th><th>{T("Page", "الصفحة")}</th><th>{T("Category", "التصنيف")}</th><th>{T("Verification", "التحقق")}</th></tr>')
RVS = {'MATCH': T('Current', 'قائم'), 'PARTLY_CHANGED': T('Partly changed', 'تغير جزئيًا'), 'RESOLVED': T('Appears resolved', 'يبدو معالجًا'), 'NOT_VERIFIABLE': T('Not verifiable', 'تعذر التحقق'), 'NOT_RETESTED': T('Not re-tested', 'لم يُعد اختباره')}
for r in R:
    H.append(f'<tr><td class="ltr">{r["fid"]}</td><td><span class="{r["plevel"].lower()}">{r["plevel"]}</span></td><td>{e(T(r["title_en"], r["title_ar"]))}</td><td>{e(T(r["page_en"], r["page_ar"]))}</td><td>{e(T(r["cat_en"], r["cat_ar"]))}</td><td>{RVS[r["rv"]]}</td></tr>')
H.append('</table></div></body></html>')
import re as _re
_doc = '\n'.join(H)
_parts = _re.split(r'(<[^>]+>)', _doc)
_parts = [p if p.startswith('<') else _re.sub(r'\b((?:EV|[FEDASRL])-\d{1,3}(?:-\d)?)\b', r'<span style="white-space:nowrap">\1</span>', p) for p in _parts]
open(OUT, 'w').write(''.join(_parts)); print('html', OUT)
