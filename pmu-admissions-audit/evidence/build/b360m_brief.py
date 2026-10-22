# Executive Management Brief (Level 1). Usage: b360m_brief.py master.json evdir out.html ar|en
import json, sys, html, re
D = json.load(open(sys.argv[1])); EV = sys.argv[2]; OUT = sys.argv[3]; AR = sys.argv[4] == 'ar'
def T(en, ar): return ar if AR else en
e = html.escape
R = D['rows']; S = D['stats']; C = D['coverage']; by = {r['fid']: r for r in R}
P = lambda k: S['plevel'].get(k, 0)
css = f"""
* {{ font-feature-settings: "calt" 0, "case" 0; }}
@page {{ size: A4; margin: 14mm 13mm 14mm 13mm; }}
body {{ font-family: {'"Noto Naskh Arabic", Inter' if AR else 'Inter, "Noto Naskh Arabic"'}, sans-serif; font-size: {'10.2pt' if AR else '9.2pt'}; line-height: {1.7 if AR else 1.45}; color: #1b1b1b; direction: {'rtl' if AR else 'ltr'}; margin: 0; }}
.band {{ background: #1F3864; color: #fff; padding: 10pt 12pt; }}
.band .t {{ font-size: 16pt; font-weight: 700; }} .band .s {{ font-size: 9pt; opacity: .9; }}
.meta {{ display: grid; grid-template-columns: 1fr 1fr; gap: 2pt 14pt; font-size: 8.6pt; padding: 7pt 2pt; border-bottom: 1px solid #C9D3E3; }}
.badges {{ margin: 7pt 0; }} .b {{ display: inline-block; padding: 3pt 8pt; font-weight: 700; font-family: Inter; font-size: 8.5pt; margin-{'left' if AR else 'right'}: 6pt; border-radius: 3pt; }}
.ok {{ background: #E2EFDA; color: #375623; border: 1px solid #A9D08E; }} .no {{ background: #FFC7CE; color: #9C0006; border: 1px solid #F4A7B1; }}
h2 {{ font-size: 11.5pt; color: #1F3864; margin: 11pt 0 4pt; border-bottom: 1.5px solid #1F3864; padding-bottom: 2pt; break-after: avoid; }}
p {{ margin: 0 0 5pt; text-align: justify; }}
table {{ width: 100%; border-collapse: collapse; font-size: {'8.4pt' if AR else '7.8pt'}; margin: 3pt 0 6pt; }}
th {{ background: #1F3864; color: #fff; padding: 3pt 4pt; text-align: {'right' if AR else 'left'}; font-weight: 600; }}
td {{ border: .6pt solid #C9D3E3; padding: 2.5pt 4pt; vertical-align: top; }} tr {{ break-inside: avoid; }} tr:nth-child(even) td {{ background: #F6F8FC; }}
.ltr {{ direction: ltr; unicode-bidi: isolate; font-family: Inter, sans-serif; white-space: nowrap; }}
.kpis {{ display: flex; gap: 6pt; margin: 6pt 0; }} .kpi {{ flex: 1; border: 1px solid #C9D3E3; border-top: 3px solid #1F3864; padding: 4pt; text-align: center; }}
.kpi .v {{ font-size: 15pt; font-weight: 700; color: #1F3864; font-family: Inter; }} .kpi .l {{ font-size: 7.6pt; color: #555; }}
.p0,.p1,.p2,.p3 {{ font-family: Inter; font-weight: 700; padding: 0 3pt; border-radius: 2pt; }}
.p0 {{ background: #FFC7CE; color: #9C0006; }} .p1 {{ background: #FFEB9C; color: #7F4F00; }} .p2 {{ background: #DDEBF7; color: #1F3864; }} .p3 {{ background: #E2EFDA; color: #375623; }}
.risk {{ border-{'right' if AR else 'left'}: 4px solid #9C0006; background: #FFF5F6; padding: 4pt 7pt; margin: 0 0 5pt; break-inside: avoid; }}
.req {{ border: 2px solid #1F3864; background: #EAF1FB; padding: 7pt 9pt; margin-top: 8pt; break-inside: avoid; }}
.small {{ font-size: 7.8pt; color: #444; }}
.figs {{ display: grid; grid-template-columns: 1fr 1fr; gap: 6pt; }} .figs img {{ width: 100%; border: 1px solid #BFBFBF; }} .figs div {{ font-size: 7.4pt; color: #444; break-inside: avoid; }}
"""
H = [f'<!doctype html><html lang="{"ar" if AR else "en"}" dir="{"rtl" if AR else "ltr"}"><head><meta charset="utf-8"><title>{T("Executive Management Brief", "الموجز التنفيذي للإدارة")}</title><style>{css}</style></head><body>']
H.append(f'''<div class="band"><div class="t">{T('Executive Management Brief — Admissions Office Content Audit 360', 'الموجز التنفيذي للإدارة — تدقيق محتوى مكتب القبول 360')}</div>
<div class="s">Prince Mohammad Bin Fahd University (PMU) · Deanship of Enrollment and Registration · PMU-ADM-360-MASTER-20261022 · v3.0</div></div>
<div class="meta"><div><b>{T('To', 'إلى')}:</b> Mr. Radhi H. Alkhaldi — Associate Director of Enrollment</div><div><b>{T('From', 'من')}:</b> {T('Nader Al Farhan — Administrative Assistant | Student Affairs', 'نادر الفرحان — مساعد إداري | شؤون الطلاب')}</div>
<div><b>{T('Root source', 'المصدر الجذري')}:</b> <span class="ltr">https://www.pmu.edu.sa/admission/admission</span></div><div><b>{T('Verified on', 'تاريخ التحقق الفعلي')}:</b> <span class="ltr">21–22 Oct 2026 (Asia/Riyadh)</span></div></div>
<div class="badges"><span class="b ok">READY FOR MANAGEMENT REVIEW</span><span class="b no">NOT READY FOR VERIFIED CLOSURE</span></div>''')
# 1
H.append(f'<h2>1. {T("Executive result", "النتيجة التنفيذية")}</h2><p>' + T(
 f"The published content of the Admissions Office section is extensive and generally organised by applicant category, but it is not currently reliable as a single source for applicants: on 22 October 2026 the four highest-risk issues remain live — no current admission cycle is visible, application fees conflict for two applicant groups, and a discontinued test (SAT II) is still required. Across {C['eligible']} examined resources the review records {S['n']} findings ({P('P0')} P0, {P('P1')} P1), {S['conflicts']} of them open conflicts between published sources. None of the six amendments requested on 26 October 2025 is fully published. Ten decisions are required; most fee and requirement values sit with authorities outside the Admissions Office and should be referred rather than decided within it.",
 f"محتوى قسم مكتب القبول المنشور وافٍ ومنظم في معظمه حسب فئة المتقدم، لكنه لا يصلح حاليًا مصدرًا موحدًا يُعتمد عليه: ففي 22 أكتوبر 2026 ما زالت المخاطر الأربع الأعلى قائمة — لا تظهر دورة قبول سارية، وتتعارض رسوم التقديم لفئتين من المتقدمين، وما زال اختبار موقوف (SAT II) مشروطًا. وعبر {C['eligible']} موردًا مفحوصًا سجلت المراجعة {S['n']} ملاحظة ({P('P0')} من P0 و{P('P1')} من P1)، منها {S['conflicts']} تعارضًا مفتوحًا بين مصادر منشورة. ولم يُنشر كاملًا أيٌّ من التعديلات الستة المطلوبة في 26 أكتوبر 2025. والمطلوب عشرة قرارات، أغلب قيم الرسوم والمتطلبات فيها بيد جهات خارج مكتب القبول، فتُحال إليها لا تُحسم داخله.") + '</p>')
# 2
H.append(f'<h2>2. {T("Scope, dates and proven coverage", "النطاق والتاريخ والتغطية المثبتة")}</h2>')
H.append(f'''<div class="kpis"><div class="kpi"><div class="v">{C['root_unique']}</div><div class="l">{T('direct destinations of the root page', 'وجهة مباشرة من الصفحة الجذرية')}</div></div>
<div class="kpi"><div class="v">{C['eligible']}</div><div class="l">{T('eligible resources (43 full · 4 partial)', 'موردًا مؤهلًا (43 كليًا · 4 جزئيًا)')}</div></div>
<div class="kpi"><div class="v">{C['links_unique']}</div><div class="l">{T('unique links checked (3 × 404)', 'رابطًا فريدًا فُحص (3 × 404)')}</div></div>
<div class="kpi"><div class="v">{C['pdf_pages']}</div><div class="l">{T('PDF pages read (2 guides)', 'صفحة PDF مقروءة (دليلان)')}</div></div>
<div class="kpi"><div class="v">{S['vstatus'].get('VERIFIED', 0)}/{S['n']}</div><div class="l">{T('findings VERIFIED (2 BLOCKED)', 'ملاحظة VERIFIED (2 BLOCKED)')}</div></div></div>''')
H.append('<p class="small">' + T('Five sections of the root page (Future Students; International Students’ Office; Graduate Admissions; Undergraduate Admissions; Undergraduate Placement Tests), their 35 destinations, two PDF guides and nine official verification pages. Full capture 21 Oct 2026; P0 items re-confirmed live 22 Oct 2026. Read-only: no forms submitted, no portal login, no applicant data, no website change. Coverage refers to the discovered inventory, not the whole website.',
 'الأقسام الخمسة في الصفحة الجذرية (الطلاب المستقبليون؛ مكتب الطلاب الدوليين؛ الدراسات العليا؛ البكالوريوس؛ اختبارات تحديد المستوى) ووجهاتها الـ35 ودليلا PDF وتسع صفحات رسمية للتحقق. التقاط كامل في 21 أكتوبر 2026، وإعادة تأكيد حية لبنود P0 في 22 أكتوبر 2026. قراءة فقط: لا إرسال نماذج ولا دخول للبوابة ولا بيانات متقدمين ولا تعديل في الموقع. والتغطية تخص الجرد المكتشف لا الموقع كله.') + '</p>')
# 3
H.append(f'<h2>3. {T("Principal risks (P0)", "أهم المخاطر (P0)")}</h2>')
for f in ['F-014', 'F-039', 'F-052', 'F-040']:
    r = by[f]
    H.append(f'<div class="risk"><b><span class="p0">P0</span> <span class="ltr">{f}</span> — {e(T(r["title_en"], r["title_ar"]))}</b> · {e(T(r["cat_en"], r["cat_ar"]))} · {T("Decision", "القرار")} <span class="ltr">{", ".join(r["dids"])}</span><br>{e(T(r["description_en"], r["description"]))}<br><span class="small">{T("Reference", "المرجع")}: {e(T(r["auth_ref"], r["auth_ref_ar"]))}</span></div>')
H.append('<div class="figs">' + ''.join(f'<div><img src="file://{EV}/{ev}.png">{cap}</div>' for ev, cap in [
    ('EV-02', T('EV-02 · International Students: SAR 500 (excl. VAT)', 'EV-02 · الطلاب الدوليون: 500 ريال (غير شاملة الضريبة)')), ('EV-03', T('EV-03 · Transfer: SAR 950 (incl. VAT)', 'EV-03 · التحويل: 950 ريالًا (شاملة الضريبة)')),
    ('EV-05', T('EV-05 · Medicine page: SAR 1000', 'EV-05 · صفحة الطب: 1000 ريال')), ('EV-06', T('EV-06 · Medical fees: SAR 1,150', 'EV-06 · رسوم البرنامج الطبي: 1,150 ريالًا'))]) + '</div>')
# 4
H.append(f'<h2>4. {T("Priority findings (P0–P1)", "الملاحظات ذات الأولوية (P0–P1)")}</h2><table><tr><th>ID</th><th>P</th><th>{T("Finding", "الملاحظة")}</th><th>{T("Classification", "التصنيف")}</th><th>{T("Status", "الحالة")}</th><th>{T("Decision", "القرار")}</th></tr>')
for r in [x for x in R if x['plevel'] in ('P0', 'P1')]:
    H.append(f'<tr><td class="ltr">{r["fid"]}</td><td><span class="{r["plevel"].lower()}">{r["plevel"]}</span></td><td>{e(T(r["title_en"], r["title_ar"]))}</td><td>{e(T(r["cat_en"], r["cat_ar"]))}</td><td class="ltr" style="white-space:normal">{e(r["res_status"])}</td><td class="ltr">{", ".join(r["dids"])}</td></tr>')
H.append('</table>')
# 5
H.append(f'<h2>5. {T("Decision & Approval Matrix", "مصفوفة القرارات والاعتماد")}</h2><p class="small">' + T('DIRECT = can be directed within the Admissions Office; REFER = to be referred to the competent authority. No decision has been approved.', 'DIRECT = يوجَّه ضمن مكتب القبول؛ REFER = يُحال إلى صاحب الصلاحية. لم يُعتمد أي قرار.') + f'</p><table><tr><th>ID</th><th>{T("Matter", "المسألة")}</th><th>{T("Recommendation", "التوصية")}</th><th>{T("Decision authority", "صاحب الصلاحية")}</th><th>{T("Role", "الدور")}</th><th>{T("Verification", "التحقق")}</th></tr>')
for d in D['decisions']:
    H.append(f'<tr><td class="ltr">{d["did"]}</td><td><b>{e(T(d["t_en"], d["t_ar"]))}</b></td><td>{e(T(d["rec_en"], d["rec_ar"]))}</td><td>{e(T(d["auth"], d["auth_ar"]))}</td><td>{e(T(d["role"], d["role_ar"]))}</td><td>{e(T(d["ver"], d["ver_ar"]))}</td></tr>')
H.append('</table>')
# 6
H.append(f'<h2>6. {T("Corrective Action Roadmap", "خارطة الإجراءات التصحيحية")}</h2><table><tr><th>ID</th><th>P</th><th>{T("Action", "الإجراء")}</th><th>{T("Decision", "القرار")}</th><th>{T("Prior approval", "الاعتماد السابق")}</th><th>{T("Proposed target", "الموعد المقترح")}</th></tr>')
for p in D['plan']:
    H.append(f'<tr><td class="ltr">{p["aid"]}</td><td><span class="{p["prio"].lower()}">{p["prio"]}</span></td><td>{e(T(p["en"], p["ar"]))}</td><td class="ltr">{p["did"]}</td><td>{e(p["approval"])}</td><td>{e(p["target"])}</td></tr>')
H.append('</table><p class="small">' + T('Every action follows APPROVE → IMPLEMENT → SAVE → REOPEN → READ BACK → COMPARE → VERIFY → CLOSE. Targets are proposals; no commitment is attributed to any unit.', 'يتبع كل إجراء: اعتماد ← تنفيذ ← حفظ ← إعادة فتح ← إعادة قراءة ← مقارنة ← تحقق ← إغلاق. والمواعيد مقترحة؛ ولا يُنسب التزام إلى أي جهة.') + '</p>')
# 7
H.append(f'<h2>7. {T("Status of amendments requested on 26 October 2025", "حالة التعديلات المطلوبة في 26 أكتوبر 2025")}</h2><table><tr><th>ID</th><th>{T("Request", "الطلب")}</th><th>{T("Status (22 Oct 2026)", "الحالة (22 أكتوبر 2026)")}</th><th>{T("Evidence", "الدليل")}</th></tr>')
for a in D['amend']:
    H.append(f'<tr><td class="ltr">{a["hid"]}</td><td>{e(T(a["req_en"], a["req_ar"]))}</td><td class="ltr"><b>{a["code"]}</b></td><td>{e(T(a["ev_en"], a["ev_ar"]))}</td></tr>')
H.append('</table><p class="small">' + T('The requests are treated as historical requests compared with the published content, not as approved policy.', 'تُعامل الطلبات بوصفها طلبات تاريخية تُقارن بالمحتوى المنشور، لا سياسات معتمدة.') + '</p>')
# 8
H.append(f'<h2>8. {T("Gaps, exceptions and residual risks", "الفجوات والاستثناءات والمخاطر المتبقية")}</h2><ul>' + ''.join(f'<li>{x}</li>' for x in T(
 ['No approved, dated policy or fee decision was available to the review; conflicting values are reported as OPEN CONFLICT, not corrected.', 'Two items are BLOCKED: four dynamic portal registration labels (F-033) and the http:// portal link (F-131) — manual check required.',
  'No applicant data or feedback was available; journey findings are content-based.', 'Excluded by mandate: portal login, form submission, security/performance testing, individual applications and student data.',
  'No correction has yet been published; all P0 risks remain live as of 22 Oct 2026.'],
 ['لم تتوفر للمراجعة سياسة أو قرار رسوم معتمد ومؤرخ؛ فتُعرض القيم المتعارضة بوصفها OPEN CONFLICT دون تصحيحها.', 'بندان بحالة BLOCKED: أربع تسميات ديناميكية في تسجيل البوابة (F-033) ورابط البوابة http (F-131) — يلزم فحص يدوي.',
  'لا تتوفر بيانات أو آراء للمتقدمين؛ وملاحظات الرحلة مستندة إلى المحتوى.', 'مستبعد بحكم التكليف: دخول البوابة وإرسال النماذج واختبارات الأمن والأداء والطلبات الفردية وبيانات الطلاب.',
  'لم يُنشر أي تصحيح بعد؛ وجميع مخاطر P0 قائمة حتى 22 أكتوبر 2026.'])) + '</ul>')
# 9
H.append(f'<h2>9. {T("Quality gates", "معايير الجودة")}</h2><table><tr><th>{T("Gate", "المعيار")}</th><th>{T("Result", "النتيجة")}</th><th>{T("Residual note", "ملاحظة متبقية")}</th></tr>')
for g in D.get('gates', [])[:5]:
    H.append(f'<tr><td>{e(T(g["en"], g["ar"]))}</td><td class="ltr"><b>{g["result"]}</b></td><td>{e(g.get("residual", ""))}</td></tr>')
H.append('</table>')
# 10
H.append(f'<h2>10. {T("Attachments and traceability", "المرفقات والإحالات")}</h2><ul>' + ''.join(f'<li><span class="ltr" style="white-space:normal">{x}</span></li>' for x in [
 'L1-02 Decision & Approval Matrix and Corrective Action Roadmap (XLSX, EN/AR)', 'L1-03 Detailed Audit Report (PDF, EN/AR) — findings, evidence figures, method',
 'L2-01 Evidence & Follow-up Pack (XLSX, EN/AR) — Master Findings Register, Evidence, Inventory, Coverage, Parity, Amendments, Decisions, Tracker, QC, Change Log']) + '</ul><p class="small">' + T('All IDs (F-, D-, A-, H-, E-, EV-) are identical across the brief, the matrix, the report and the evidence pack.', 'المعرفات (F- وD- وA- وH- وE- وEV-) موحدة بين الموجز والمصفوفة والتقرير وحزمة الأدلة.') + '</p>')
# 11
H.append(f'<div class="req"><b>{T("Management request", "الطلب الإداري")}</b><br>' + T(
 'It is respectfully requested that the competent units be directed to: (1) confirm the governing values for fees, the admission cycle, and undergraduate and graduate requirements (D-01 to D-05); (2) authorise the actions within the Admissions Office’s remit — interim cycle notice, withdrawal of the 2018 guide, contact details, and the 48 editorial corrections (D-02, D-06, D-07, D-09); (3) designate owners for implementation and publication verification (D-08, D-10); and (4) note that closure will be recorded only after publication and read-back verification.',
 'يُرجى التكرم بتوجيه الجهات المختصة إلى: (1) تأكيد القيم الحاكمة للرسوم ودورة القبول ومتطلبات البكالوريوس والدراسات العليا (D-01 إلى D-05)؛ (2) اعتماد الإجراءات الواقعة ضمن صلاحية مكتب القبول — الإشعار المؤقت بالدورة، وسحب دليل 2018، وبيانات التواصل، والتصحيحات التحريرية الـ48 (D-02 وD-06 وD-07 وD-09)؛ (3) تسمية المسؤولين عن التنفيذ والتحقق من النشر (D-08 وD-10)؛ (4) والعلم بأن الإغلاق لن يُسجَّل إلا بعد النشر والتحقق بإعادة القراءة.') + '</div>')
H.append('</body></html>')
doc = '\n'.join(H)
parts = re.split(r'(<[^>]+>)', doc)
parts = [p if p.startswith('<') else re.sub(r'\b((?:EV|[FEDASRLHV])-\d{1,3}(?:-\d)?)\b', r'<span style="white-space:nowrap">\1</span>', p) for p in parts]
open(OUT, 'w').write(''.join(parts)); print('brief', OUT)
