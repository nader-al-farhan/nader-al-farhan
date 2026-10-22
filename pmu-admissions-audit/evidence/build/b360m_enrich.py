# Enrich the 360 dataset for the Unified Master Directive (PMU-ADM-360-MASTER-20261022).
# Usage: b360m_enrich.py data.json recheck_results.tsv out_master.json
import json, sys, re, collections
D = json.load(open(sys.argv[1])); RECHK = sys.argv[2]; OUT = sys.argv[3]
R = D['rows']
TODAY = '2026-10-22'
rc = [l.rstrip('\n').split('\t') for l in open(RECHK) if l.strip()]
RECHECKED = {x[0].rstrip('b').rstrip('c') for x in rc if x[0].startswith('F-')}

# ---------- 06: nine-type classification taxonomy
CLS = {
 'VERIFIED_ERROR': ('Verified error in published information', 'خطأ مثبت في معلومة منشورة'),
 'CONFLICT': ('Conflict between two or more sources', 'تعارض بين مصدرين أو أكثر'),
 'OUTDATED': ('Outdated or expired content', 'محتوى قديم أو منتهي الصلاحية'),
 'MISSING_INFO': ('Missing information important to applicants', 'نقص معلومات مهم للمتقدم'),
 'AR_EN_MISMATCH': ('Arabic–English difference', 'اختلاف بين العربية والإنجليزية'),
 'AMBIGUITY': ('Ambiguity in procedures or fees', 'غموض في الإجراءات أو الرسوم'),
 'PRIOR_REQUEST_OPEN': ('Prior amendment request not fully implemented', 'طلب تعديل سابق لم يُنفذ بالكامل'),
 'VERIFIED_CORRECT': ('Verified correct information', 'معلومة صحيحة تم التحقق منها'),
 'CANNOT_VERIFY': ('Cannot currently be verified', 'مسألة يتعذر التحقق منها حاليًا'),
}
NATURE = {'PUB_CONFLICT': ('Conflict', 'تعارض'), 'GOV_ERROR': ('Error vs. governing reference', 'خطأ مقابل مرجع حاكم'), 'GAP': ('Gap', 'نقص'),
          'OUTDATED': ('Outdated', 'متقادم'), 'LANG_DIFF': ('Language difference', 'اختلاف لغوي'), 'EDITORIAL': ('Editorial', 'تحريري'),
          'IMPROVE': ('Improvement', 'تحسين'), 'DECISION': ('Decision needed', 'يحتاج قرارًا'), 'UNVERIFIED': ('Unverified', 'غير متحقق')}
AMBIG = re.compile(r'ambigu|unclear|unspecified|undefined|imprecise|informal|inconsistent|differing|varying|conflat', re.I)
# prior requests of 26 Oct 2025 linked to findings
PRIOR = {'F-040': 'H-4', 'F-039': 'H-3', 'F-036': 'H-6', 'F-071': 'H-1', 'F-070': 'H-2', 'F-119': 'H-5'}
def classify(r):
    c = r['category']
    if r['fid'] in ('F-040', 'F-124'): return 'OUTDATED'
    if c == 'PUB_CONFLICT': return 'CONFLICT'
    if c in ('GOV_ERROR', 'EDITORIAL'): return 'VERIFIED_ERROR'
    if c == 'OUTDATED': return 'OUTDATED'
    if c == 'LANG_DIFF': return 'AR_EN_MISMATCH'
    if c == 'UNVERIFIED': return 'CANNOT_VERIFY'
    if c == 'DECISION': return 'AMBIGUITY'
    if c in ('GAP', 'IMPROVE'): return 'AMBIGUITY' if AMBIG.search(r['title_en']) else 'MISSING_INFO'
    return 'MISSING_INFO'

# authoritative references (05)
EXT = {
 'F-040': ('College Board — "An Update on Reducing and Simplifying Demands on Students" (SAT Subject Tests discontinued; final international administration June 2021). https://allaccess.collegeboard.org/update-reducing-and-simplifying-demands-students',
           'College Board, 19 Jan 2021 (official; located by web search on 22 Oct 2026, page not retrievable from the review network)'),
 'F-124': ('ETS — TOEFL iBT score scale update (1–6 scale for tests on/after 21 Jan 2026; dual 0–120 reporting through Jan 2028). https://www.ets.org/toefl/institutions/ibt/score-scale-update.html',
           'ETS, effective 21 Jan 2026 (official; located by web search on 22 Oct 2026, page not retrievable from the review network)'),
 'F-035': ('HTTP response of the linked URLs (404 – File or directory not found)', 'Link checks 21 and 22 Oct 2026'),
 'F-097': ('The published page itself names another institution (UA CESL); no PMU reference can make this correct', 'Observed 21–22 Oct 2026'),
 'F-054': ('Arithmetic of the published formula on the same page (20% HS + 40% Qudrat + 40% Tahseely; minimum 86)', 'Observed 21 Oct 2026'),
 'F-126': ('Target URL of the link (ETEC Humanities-track page)', 'Observed 21 Oct 2026; ETEC page not retrievable from the review network'),
 'F-014': ('Dates published in the calendar compared with the observation date', 'Observed 21–22 Oct 2026'),
 'F-015': ('Dates published in the calendar compared with the observation date', 'Observed 21 Oct 2026'),
 'F-111': ('Dates published in the payment schedules compared with the observation date', 'Observed 21 Oct 2026'),
 'F-005': ('Target page of the footer link: Academic Year 2021/2022', 'Observed 21–22 Oct 2026'),
 'F-036': ('PDF metadata (created 20 Dec 2018) and file content; byte-identical on 11 and 21 Oct 2026', 'PDF v2-2, 20-12-18'),
 'F-121': ('PDF metadata (created 30 Aug 2017; modified 12 Mar 2019)', 'Aptis Candidate Guide, Aug 2017'),
}
FEE = {'F-039', 'F-052', 'F-026', 'F-104', 'F-105', 'F-108', 'F-119'}
def authority(r, cls):
    if r['fid'] in EXT: return EXT[r['fid']]
    if r['fid'] in FEE and cls == 'CONFLICT': return ('OPEN CONFLICT — published fee statements conflict; the PMU "Other Fees" schedule states "includes the VAT 15%", but no approved, dated fee decision is available → ESCALATION REQUIRED', 'Published schedules observed 21–22 Oct 2026; approval reference: not available')
    if r['fid'] in FEE: return ('PMU "Other Fees" / fee schedules as published (e.g. "includes the VAT 15%"); no approved, dated fee decision available to the review → ESCALATION REQUIRED', 'Published schedules observed 21–22 Oct 2026; approval reference: not available')
    if cls == 'CONFLICT': return ('OPEN CONFLICT — no governing institutional reference available to the review', 'Not available')
    if r['category'] == 'EDITORIAL': return ('Standard Arabic/English usage — no policy reference required', 'Not applicable')
    if cls == 'CANNOT_VERIFY': return ('Not determinable from published content', 'Not available')
    return ('Published content (self-evident observation); governing policy not available to the review', 'Not available')

def impact(r):
    t = (r['title_en'] + ' ' + r['description_en']).lower()
    if re.search(r'\bfee|vat|sar\b|tuition|payment', t): return ('Applicant · Financial', 'المتقدم · مالي')
    if re.search(r'ielts|toefl|sat\b|sat |gpa|eligib|requirement|tahseely|qudrat|aptis|weighted|test', t): return ('Applicant · Academic', 'المتقدم · أكاديمي')
    if re.search(r'calendar|date|portal|link|contact|channel|deadline|cycle|form', t): return ('Applicant · Operational', 'المتقدم · تشغيلي')
    if re.search(r'alternative text|language attribute|landmark|mobile|accessib', t): return ('Accessibility · Operational', 'الإتاحة · تشغيلي')
    return ('Applicant · Clarity', 'المتقدم · وضوح')

def auth_ar(r, cls):
    m = {'F-040': 'College Board — إعلان 19 يناير 2021 بإيقاف اختبارات SAT Subject Tests (آخر انعقاد دولي يونيو 2021)',
         'F-124': 'ETS — تحديث سلم TOEFL iBT (من 1 إلى 6 للاختبارات من 21 يناير 2026، مع إصدار مزدوج حتى يناير 2028)',
         'F-035': 'استجابة الروابط (404) في فحص 21 و22 أكتوبر 2026', 'F-097': 'الصفحة المنشورة نفسها تسمي مؤسسة أخرى (UA CESL)',
         'F-054': 'حساب المعادلة المنشورة في الصفحة نفسها', 'F-126': 'وجهة الرابط (صفحة المسار الإنساني في هيئة تقويم التعليم والتدريب)',
         'F-014': 'المواعيد المنشورة مقارنة بتاريخ الرصد', 'F-015': 'المواعيد المنشورة مقارنة بتاريخ الرصد', 'F-111': 'مواعيد جداول السداد مقارنة بتاريخ الرصد',
         'F-005': 'وجهة رابط التذييل: العام الأكاديمي 2021/2022', 'F-036': 'بيانات ملف PDF (أُنشئ 20 ديسمبر 2018) ومحتواه؛ مطابق بايتًا في 11 و21 أكتوبر 2026',
         'F-121': 'بيانات ملف PDF (أُنشئ 30 أغسطس 2017؛ عُدّل 12 مارس 2019)'}
    if r['fid'] in m: return m[r['fid']]
    if r['fid'] in FEE and cls == 'CONFLICT': return 'تعارض مفتوح (OPEN CONFLICT) — بيانات الرسوم المنشورة متعارضة؛ ويذكر جدول «الرسوم الأخرى» أنها «شاملة ضريبة 15%»، ولا يتوفر قرار رسوم معتمد ومؤرخ ← يلزم تصعيد (ESCALATION REQUIRED)'
    if r['fid'] in FEE: return 'جداول الرسوم المنشورة؛ ولا يتوفر قرار رسوم معتمد ومؤرخ ← يلزم تصعيد'
    if cls == 'CONFLICT': return 'تعارض مفتوح (OPEN CONFLICT) — لا مرجع مؤسسي حاكم متاح للمراجعة'
    if r['category'] == 'EDITORIAL': return 'الاستخدام اللغوي السليم بالعربية والإنجليزية — لا يلزم مرجع سياسات'
    if cls == 'CANNOT_VERIFY': return 'لا يمكن تحديده من المحتوى المنشور'
    return 'المحتوى المنشور (ملاحظة ظاهرة بذاتها)؛ والسياسة الحاكمة غير متاحة للمراجعة'

VS = {'MATCH': 'VERIFIED', 'PARTLY_CHANGED': 'VERIFIED', 'RESOLVED': 'VERIFIED', 'NOT_RETESTED': 'VERIFIED', 'NOT_VERIFIABLE': 'BLOCKED'}
for r in R:
    cls = 'CANNOT_VERIFY' if r['rv'] == 'NOT_VERIFIABLE' else classify(r)
    r['category_old'] = r['category']; r['nature_en'], r['nature_ar'] = NATURE[r['category']]
    r['category'] = cls; r['cat_en'], r['cat_ar'] = CLS[cls]
    r['prior'] = PRIOR.get(r['fid'], '')
    r['vstatus'] = VS[r['rv']]
    r['verified_on'] = TODAY if r['fid'] in RECHECKED else ('2026-10-11' if r['rv'] == 'NOT_RETESTED' else ('—' if r['rv'] == 'NOT_VERIFIABLE' else '2026-10-21'))
    r['auth_ref'], r['auth_ver'] = authority(r, cls)
    r['auth_ref_ar'] = auth_ar(r, cls)
    if r['fid'] in ('F-040', 'F-124') and r['rv'] == 'NOT_VERIFIABLE': r['vstatus'] = 'VERIFIED'
    r['impact_en'], r['impact_ar'] = impact(r)
    r['res_status'] = 'OPEN CONFLICT' if cls == 'CONFLICT' else ('ESCALATION REQUIRED' if r['dids'] and r['dids'] != ['D-09'] and cls in ('AMBIGUITY', 'MISSING_INFO', 'OUTDATED') and r['plevel'] in ('P0', 'P1') else 'OPEN')
    if r['rv'] == 'RESOLVED': r['res_status'] = 'CHANGE OBSERVED — OWNER TO CONFIRM'
    if r['vstatus'] == 'BLOCKED': r['res_status'] = 'BLOCKED — MANUAL CHECK'
    r['pub_status'] = 'Change observed on site; not confirmed by owner' if r['rv'] in ('RESOLVED', 'PARTLY_CHANGED') else 'Not corrected — no approved correction published'
    r['owner_code'] = 'OWNER_TO_CONFIRM' if 'to be confirmed' in r['owner_en'].lower() else r['owner_en']
    shot = [e['shot'] for e in D['evidence'] if e['fid'] == r['fid'] and e['shot']]
    pdfp = 'PDF p. 20 (image)' if r['fid'] == 'F-036' else ''
    r['shot_ref'] = '; '.join([s for s in shot] + ([pdfp] if pdfp else []) + [f"{r['page_id']}_full.jpg" if r['page_id'].startswith('P') else ''])
    r['artifact'] = 'PDF' if r['fid'] in ('F-036', 'F-121') else ('Web application (public page)' if r['page_id'] == 'P38' else 'HTML page')
    r['lang_res'] = 'EN + AR' if r['fid'] in ('F-022', 'F-028') else 'EN'
    notes = []
    if r['prior']: notes.append(f"Linked to prior request {r['prior']} (26 Oct 2025)")
    if r['rv_note_en']: notes.append(r['rv_note_en'])
    if r['fid'] in RECHECKED: notes.append('Re-confirmed on the live site on 22 Oct 2026')
    r['followup_en'] = ' | '.join(notes)

# strengths become verified-correct records
VC = [dict(vid=s['sid'].replace('S-', 'V-'), **s) for s in D['strengths']]
VC.append(dict(vid='V-09', sid='', pid='P04', url='https://pmu.edu.sa/admission/degrees_programs_fs_ro', excerpt='B.S. in Chemical Engineering', page_en='Degrees & Programs', page_ar='الدرجات والبرامج',
               en='B.S. Chemical Engineering is listed on Degrees & Programs and on the list of majors, as requested on 26 Oct 2025 (re-confirmed 22 Oct 2026).',
               ar='برنامج B.S. Chemical Engineering مدرج في صفحة الدرجات والبرامج وقائمة التخصصات كما طُلب في 26 أكتوبر 2025 (أُعيد التأكد في 22 أكتوبر 2026).', verified=True))
VC.append(dict(vid='V-10', sid='', pid='P08', url='https://www.pmu.edu.sa/apply', excerpt='Numerical values in L-01 … L-09', page_en='/apply (bilingual)', page_ar='/apply (ثنائية اللغة)',
               en='All numerical admission values on /apply are identical in the English and Arabic blocks (9 segment pairs compared).',
               ar='جميع القيم الرقمية للقبول في /apply متطابقة بين الكتلتين الإنجليزية والعربية (قورن 9 أزواج).', verified=True))
D['verified_correct'] = VC

# 07: historical amendments with prescribed statuses
H = {'A-1': ('H-1', 'NOT_PUBLISHED'), 'A-2': ('H-2', 'PARTIALLY_PUBLISHED'), 'A-3': ('H-3', 'PARTIALLY_PUBLISHED'), 'A-4': ('H-4', 'PARTIALLY_PUBLISHED'),
     'A-5': ('H-5', 'NOT_PUBLISHED'), 'A-6': ('H-6', 'NOT_PUBLISHED')}
for a in D['amend']:
    a['hid'], a['code'] = H[a['aid']]
    a['basis_en'] = 'Historical request (email of 26 Oct 2025); compared with current published content — not treated as approved policy.'
    a['basis_ar'] = 'طلب تعديل تاريخي (رسالة 26 أكتوبر 2025)؛ قورن بالمحتوى المنشور حاليًا — ولا يُعامل سياسة معتمدة.'
    a['checked'] = TODAY
    if a['aid'] == 'A-4':
        a['ev_en'] = '"SAT 2" no longer appears on the CS & Engineering requirements page, but "(SAAT – Tahseely)" is still listed there and "SAT II 30%" remains on the International Students page. The intended scope of the request (removing SAT 2 only, or Tahseely as well) needs confirmation.'
        a['ev_ar'] = 'لم يعد «SAT 2» واردًا في صفحة متطلبات الحاسب والهندسة، لكن «(SAAT – Tahseely)» ما زال مذكورًا فيها، ويبقى «SAT II 30%» في صفحة الطلاب الدوليين. ويحتاج النطاق المقصود بالطلب (إزالة SAT 2 فقط أم التحصيلي أيضًا) إلى تأكيد.'
    if a['aid'] == 'A-3':
        a['ev_en'] += ' Escalation: the VAT basis of the request conflicts with the published official schedule.'
        a['ev_ar'] += ' يحتاج تصعيدًا: أساس الضريبة في الطلب يخالف الجدول الرسمي المنشور.'

# 08: decision & approval matrix
DM = {
 'D-01': dict(risk_en='Applicants may pay or budget for the wrong fee; refunds, complaints and reputational risk.', risk_ar='قد يدفع المتقدم رسمًا خاطئًا أو يخطط على أساسه؛ مع مخاطر الاسترداد والشكاوى والسمعة.',
              rec_en='Option A: Financial Affairs confirms one dated fee schedule by applicant category (with VAT basis); all admissions pages link to it instead of restating amounts.', rec_ar='البديل أ: تؤكد الشؤون المالية جدول رسوم مؤرخًا واحدًا حسب الفئة (مع أساس الضريبة)، وتحيل إليه صفحات القبول بدل تكرار المبالغ.',
              ref_en='Approved, dated fee schedule 2026/2027 by applicant category, with VAT basis and effective date', ref_ar='جدول رسوم 2026/2027 معتمد ومؤرخ حسب الفئة مع أساس الضريبة وتاريخ السريان',
              auth='Financial Affairs (fee authority)', role='REFER', impl='Website content publisher — OWNER_TO_CONFIRM', ver='Admissions Office (read-back)'),
 'D-02': dict(risk_en='Applicants act on expired dates or cannot tell whether admission is open.', risk_ar='يعتمد المتقدم على مواعيد منتهية أو لا يعرف هل القبول مفتوح.',
              rec_en='Option B immediately (dated interim notice), then Option A when next-cycle dates are approved.', rec_ar='البديل ب فورًا (إشعار مؤقت مؤرخ)، ثم البديل أ عند اعتماد مواعيد الدورة القادمة.',
              ref_en='Approved admission calendar for the next cycle; channel per applicant category', ref_ar='تقويم القبول المعتمد للدورة القادمة وقناة التقديم لكل فئة',
              auth='Deanship of Enrollment and Registration / Admissions (academic calendar: Registrar)', role='DIRECT (interim notice) · REFER (calendar)', impl='Admissions Office + publisher', ver='Admissions Office'),
 'D-03': dict(risk_en='Inconsistent eligibility decisions and applicant disputes; discontinued SAT II still required.', risk_ar='قرارات أهلية غير متسقة ونزاعات مع المتقدمين؛ واستمرار اشتراط SAT II الموقوف.',
              rec_en='Option A: one approved undergraduate admission matrix (tests, minimums, weights, substitutions, documents), referenced by every page.', rec_ar='البديل أ: مصفوفة قبول بكالوريوس معتمدة واحدة (الاختبارات والحدود والأوزان والبدائل والوثائق) تحيل إليها الصفحات كلها.',
              ref_en='Approved undergraduate admission criteria (incl. minimum weighted totals requested on 26 Oct 2025)', ref_ar='معايير قبول البكالوريوس المعتمدة (بما فيها الحدود الدنيا للنسبة الموزونة المطلوبة في 26 أكتوبر 2025)',
              auth='Competent academic authority (colleges / academic council) with Admissions', role='REFER (values) · DIRECT (page alignment)', impl='Admissions Office + publisher', ver='Admissions Office'),
 'D-04': dict(risk_en='Applicants judged against different English and GPA thresholds for the same programme; another university’s text on a PMU page.', risk_ar='تقييم المتقدمين بحدود لغة ومعدل مختلفة للبرنامج نفسه؛ ونص جامعة أخرى في صفحة للجامعة.',
              rec_en='Remove the non-PMU (UA CESL) text now; then Option A: an approved graduate entry matrix by programme.', rec_ar='إزالة نص UA CESL فورًا؛ ثم البديل أ: مصفوفة قبول معتمدة للدراسات العليا حسب البرنامج.',
              ref_en='Approved graduate admission requirements per programme (English thresholds, GPA rules, special conditions)', ref_ar='متطلبات القبول المعتمدة لكل برنامج دراسات عليا (حدود اللغة، قواعد المعدل، الشروط الخاصة)',
              auth='Graduate studies authority / programme councils', role='DIRECT (removal request) · REFER (values)', impl='Programme owners + publisher', ver='Admissions Office'),
 'D-05': dict(risk_en='Applicants cannot reliably tell which programmes are open; programmes priced without an application route.', risk_ar='لا يستطيع المتقدم معرفة البرامج المفتوحة بدقة؛ وبرامج مسعّرة دون مسار تقديم.',
              rec_en='Option A: one authoritative list of programmes open for admission, with official names and abbreviations.', rec_ar='البديل أ: قائمة معتمدة واحدة للبرامج المفتوحة للقبول بأسمائها واختصاراتها الرسمية.',
              ref_en='Official list of programmes open for admission (academic affairs)', ref_ar='القائمة الرسمية للبرامج المفتوحة للقبول (الشؤون الأكاديمية)',
              auth='Academic affairs / colleges', role='REFER', impl='Admissions Office + publisher', ver='Admissions Office'),
 'D-06': dict(risk_en='The 2018 guide contradicts current fees and procedures; broken scholarship links.', risk_ar='دليل 2018 يخالف الرسوم والإجراءات الحالية؛ وروابط منح معطلة.',
              rec_en='Option A: withdraw the 2018 guide now and replace it later; restore or remove the three 404 links.', rec_ar='البديل أ: سحب دليل 2018 الآن واستبداله لاحقًا؛ ومعالجة الروابط الثلاثة المعطلة أو إزالتها.',
              ref_en='Not required for withdrawal; replacement guide requires Admissions approval', ref_ar='لا يلزم مرجع للسحب؛ والدليل البديل يحتاج اعتماد القبول',
              auth='Admissions Office', role='DIRECT', impl='Website content publisher — OWNER_TO_CONFIRM', ver='Admissions Office'),
 'D-07': dict(risk_en='Applicants cannot reach Admissions directly; personal data collected without a visible privacy notice.', risk_ar='يتعذر على المتقدم الوصول المباشر إلى القبول؛ وتُجمع بيانات شخصية دون إشعار خصوصية ظاهر.',
              rec_en='Publish an official Admissions contact block; link the university privacy notice from the enquiry form (privacy wording owner to be confirmed).', rec_ar='نشر بيانات تواصل رسمية للقبول؛ وربط إشعار الخصوصية الجامعي من نموذج الاستفسار (جهة صياغة الخصوصية تحتاج تأكيدًا).',
              ref_en='Official Admissions contact details; university privacy notice', ref_ar='بيانات التواصل الرسمية للقبول؛ وإشعار الخصوصية الجامعي',
              auth='Admissions Office (contacts) · OWNER_TO_CONFIRM (privacy notice)', role='DIRECT (contacts) · REFER (privacy)', impl='Admissions Office + publisher', ver='Admissions Office'),
 'D-08': dict(risk_en='Without named owners and a review cycle, the same defects will recur each admission cycle.', risk_ar='دون ملاك مسمَّين ودورة مراجعة تتكرر العيوب نفسها في كل دورة قبول.',
              rec_en='Option A: a named owner per page, a review before each cycle opens, and a visible "last reviewed" date.', rec_ar='البديل أ: مالك مسمى لكل صفحة، ومراجعة قبل فتح كل دورة، وتاريخ «آخر مراجعة» ظاهر.',
              ref_en='Content ownership register approved by Admissions leadership', ref_ar='سجل ملكية المحتوى المعتمد من قيادة القبول',
              auth='Admissions leadership', role='DIRECT', impl='Admissions Office', ver='Admissions leadership'),
 'D-09': dict(risk_en='Low-impact errors persist and reduce credibility.', risk_ar='تبقى أخطاء محدودة الأثر وتضعف المصداقية.',
              rec_en='Option A: approve the 48 editorial corrections as a batch (none changes a value or requirement).', rec_ar='البديل أ: اعتماد التصحيحات التحريرية الـ48 دفعة واحدة (لا يغير أيٌّ منها قيمة أو شرطًا).',
              ref_en='Not required (no policy content)', ref_ar='لا يلزم (لا محتوى سياسات)',
              auth='Admissions Office (content approver)', role='DIRECT', impl='Website content publisher — OWNER_TO_CONFIRM', ver='Admissions Office'),
 'D-10': dict(risk_en='Pages are harder to use with assistive technology and on mobile; one portal link uses http.', risk_ar='صعوبة استخدام الصفحات بالتقنيات المساعدة وعلى الجوال؛ ورابط للبوابة يستخدم http.',
              rec_en='Option B now (fix listed items); consider Option A (WCAG 2.1 AA baseline) with the publisher.', rec_ar='البديل ب الآن (معالجة البنود المرصودة)؛ ودراسة البديل أ (WCAG 2.1 AA) مع جهة النشر.',
              ref_en='University web/accessibility standard (if any) — OWNER_TO_CONFIRM', ref_ar='معيار الجامعة للويب/الإتاحة (إن وجد) — المسؤول يحتاج تأكيدًا',
              auth='Website publisher / IT — OWNER_TO_CONFIRM', role='REFER', impl='Website publisher / IT — OWNER_TO_CONFIRM', ver='Admissions Office'),
}
DMAR = {
 'D-01': ('الشؤون المالية (صاحبة صلاحية الرسوم)', 'إحالة', 'ناشر محتوى الموقع — المسؤول يحتاج تأكيدًا', 'مكتب القبول (إعادة القراءة)'),
 'D-02': ('عمادة القبول والتسجيل / مكتب القبول (التقويم الأكاديمي: التسجيل)', 'توجيه (الإشعار المؤقت) · إحالة (التقويم)', 'مكتب القبول + ناشر المحتوى', 'مكتب القبول'),
 'D-03': ('الجهة الأكاديمية المختصة (الكليات / المجلس الأكاديمي) مع مكتب القبول', 'إحالة (القيم) · توجيه (مواءمة الصفحات)', 'مكتب القبول + ناشر المحتوى', 'مكتب القبول'),
 'D-04': ('جهة الدراسات العليا / مجالس البرامج', 'توجيه (طلب الإزالة) · إحالة (القيم)', 'مالكو البرامج + ناشر المحتوى', 'مكتب القبول'),
 'D-05': ('الشؤون الأكاديمية / الكليات', 'إحالة', 'مكتب القبول + ناشر المحتوى', 'مكتب القبول'),
 'D-06': ('مكتب القبول', 'توجيه', 'ناشر محتوى الموقع — المسؤول يحتاج تأكيدًا', 'مكتب القبول'),
 'D-07': ('مكتب القبول (بيانات التواصل) · المسؤول يحتاج تأكيدًا (إشعار الخصوصية)', 'توجيه (التواصل) · إحالة (الخصوصية)', 'مكتب القبول + ناشر المحتوى', 'مكتب القبول'),
 'D-08': ('قيادة القبول', 'توجيه', 'مكتب القبول', 'قيادة القبول'),
 'D-09': ('مكتب القبول (معتمد المحتوى)', 'توجيه', 'ناشر محتوى الموقع — المسؤول يحتاج تأكيدًا', 'مكتب القبول'),
 'D-10': ('ناشر الموقع / تقنية المعلومات — المسؤول يحتاج تأكيدًا', 'إحالة', 'ناشر الموقع / تقنية المعلومات — المسؤول يحتاج تأكيدًا', 'مكتب القبول'),
}
for d in D['decisions']:
    d['auth_ar'], d['role_ar'], d['impl_ar'], d['ver_ar'] = DMAR[d['did']]
    d.update(DM[d['did']]); d['status'] = 'PENDING — NOT APPROVED'; d['follow'] = 'To be set on management direction'
    d['nP0'] = sum(1 for r in R if d['did'] in r['dids'] and r['plevel'] == 'P0'); d['nP1'] = sum(1 for r in R if d['did'] in r['dids'] and r['plevel'] == 'P1')

# 09: corrective action roadmap (10 fields)
RM = {
 'A-01': ('No current admission cycle visible (F-014, F-015, F-030, F-005)', 'Applicants see a dated statement of the current cycle status', 'Dated notice on root page and Admissions Calendar; fix footer calendar link', 'D-02', 'None for an interim notice; calendar approval for dates', 'Immediately after direction'),
 'A-02': ('Conflicting application fees (F-039, F-052, F-026)', 'One fee per category, one VAT basis, everywhere', 'Replace restated amounts with a link to the approved schedule', 'D-01', 'Financial Affairs confirmation', 'After D-01'),
 'A-03': ('Discontinued SAT II required (F-040)', 'No discontinued test is required', 'Remove SAT II or replace with the approved alternative', 'D-03', 'Academic authority confirmation of the alternative', 'After D-03'),
 'A-04': ('Another university’s text on EMGMS page (F-097)', 'Page contains PMU-only, approved requirements', 'Remove UA CESL text; publish confirmed thresholds', 'D-04', 'Programme owner confirmation', 'Removal immediately; values after D-04'),
 'A-05': ('Graduate English thresholds conflict (F-073, F-100)', 'Forms and programme pages state the same approved thresholds', 'Align generic form and programme pages to the approved matrix', 'D-04', 'Graduate authority approval', 'After D-04'),
 'A-06': ('Undergraduate criteria inconsistent (F-024, F-059, F-070, F-117 …)', 'One approved matrix referenced by all pages', 'Publish matrix; align pages', 'D-03', 'Academic authority approval', 'Before next cycle opens'),
 'A-07': ('Outdated guide and broken links (F-036, F-121, F-035)', 'No outdated guide or 404 link in the section', 'Withdraw/replace guides; fix links', 'D-06', 'Admissions direction', 'Immediately after direction'),
 'A-08': ('Programme lists inconsistent (F-012, F-043, F-048, F-074)', 'One authoritative programme list', 'Publish list; align pages and names', 'D-05', 'Academic affairs confirmation', 'Before next cycle opens'),
 'A-09': ('No Admissions contact; no privacy notice (F-002, F-020, F-034)', 'Official contacts and privacy link visible', 'Add contact block; link privacy notice', 'D-07', 'Admissions; privacy owner to confirm', 'After D-07'),
 'A-10': ('Editorial errors (48 corrections + editorial findings)', 'Corrected text on all affected pages', 'Apply the 48 approved before/after corrections', 'D-09', 'Admissions content approval', 'After D-09'),
 'A-11': ('Accessibility and link-protocol items (F-003, F-004, F-008, F-069, F-131)', 'Listed items pass a re-check', 'Fix lang attribute, alt text, landmarks, reflow, https link', 'D-10', 'Publisher/IT agreement', 'After D-10'),
 'A-12': ('No named owners or review cycle', 'Owner register and pre-cycle review in place', 'Approve owner register; show "last reviewed" dates', 'D-08', 'Admissions leadership', 'Before next cycle opens'),
 'A-13': ('No applicant feedback evidence', 'Evidence base for future reviews', 'Approve survey/enquiry-log design before any collection', 'D-08', 'Separate authorisation + privacy review', 'To be set'),
}
for p in D['plan']:
    pr, out, act, dec, appr, tgt = RM[p['aid']]
    p.update(problem=pr, outcome=out, action=act, dec_pending=dec, approval=appr, target=tgt + ' (proposed, non-binding)', status='NOT_STARTED', evidence='', reverify='')

# 02: project source register
D['sources'] = [
 ('SRC-01', 'Live Admissions Office section (root + 35 destinations + verification pages)', 'pmu.edu.sa', '2026-10-10 → 2026-10-22', 'Object of review; evidence of published state', 'Complete for discovered scope', 'ACCESSED'),
 ('SRC-02', 'Linked PDFs: Web Admission Guide (v2-2, 20-12-18); Aptis Candidate Guide (Aug 2017)', 'pmu.edu.sa', '2026-10-11; 2026-10-21', 'Object of review', '71 pages read; Aptis images not individually inspected', 'ACCESSED'),
 ('SRC-03', 'Email thread "updates on Admission pages" → "comments on Admission pages" (Jun 2025 – Feb 2026), incl. reply of 26 Oct 2025', 'Gmail (forwarded copies, read-only)', '2025-06-24 → 2026-02-17', 'Historical requests and correspondence; not policy', 'Message bodies read; attached "Admissions pages update" PDFs not opened', 'ACCESSED (partial)'),
 ('SRC-04', 'Remediation package PMU_Content_Remediation.zip (530 actions)', 'User upload', '2026-10-13', 'Working observations; leads to verify', 'In-scope items extracted (73 actions, 48 edits, 32 decisions)', 'ACCESSED'),
 ('SRC-05', 'Four third-party working files dated 2026-10-13 (Executive Content Review; Management Brief; Content Review Register; Decision Register)', 'User upload', '2026-10-13', 'Unverified secondary analysis', 'Read in full; claims re-verified individually', 'ACCESSED'),
 ('SRC-06', 'Earlier audit rounds in this project (127/130-row Arabic register; 71-finding English package)', 'Project repository', '2026-10-11 → 2026-10-13', 'Superseded working outputs', 'Reconciled into the current register', 'ACCESSED'),
 ('SRC-07', 'Prior conversations outside this project', '—', '—', 'Unknown', 'Not retrievable from this environment', 'NOT AVAILABLE'),
 ('SRC-08', 'Approved PMU admission policies, fee decisions, academic council decisions', 'Institutional', '—', 'Would be governing references', 'None supplied or published within scope', 'NOT AVAILABLE'),
 ('SRC-09', 'College Board announcement on SAT Subject Tests (19 Jan 2021)', 'allaccess.collegeboard.org', '2026-10-22', 'Official external reference (test owner)', 'Located via web search; direct retrieval blocked by review network', 'LOCATED'),
 ('SRC-10', 'ETS TOEFL iBT score-scale update (effective 21 Jan 2026)', 'ets.org', '2026-10-22', 'Official external reference (test owner)', 'Located via web search; direct retrieval blocked by review network', 'LOCATED'),
 ('SRC-11', 'Applicant data, enquiry logs, analytics, surveys', 'Institutional', '—', 'Would support experience analysis', 'None available', 'NOT AVAILABLE'),
]
# change log
D['changelog'] = [
 ('v1.0', '2026-10-11', 'Baseline line-by-line audit; Arabic register (127 findings); English executive package (71 key findings)'),
 ('v1.1', '2026-10-13', 'Reconciled the remediation package: +3 findings (130); in-scope editorial/decision annex; 26 Oct 2025 amendment status'),
 ('v2.0', '2026-10-21', 'Fresh live capture and re-verification; 131 findings; P0–P3 scale; 14 evidence screenshots; bilingual report and 14-sheet registers'),
 ('v2.1', '2026-10-22', 'All deliverables labelled "Prepared for Management Review"'),
 ('v3.0', '2026-10-22', 'Master Directive edition: nine-type taxonomy; VERIFIED/BLOCKED statuses; authoritative-reference fields; official College Board and ETS references; Decision & Approval Matrix (authority vs. implementer vs. verifier); 10-field Corrective Action Roadmap; historical amendments with PUBLISHED-type statuses; source register; quality gates G1–G5; Arabic and English executive briefs; live re-confirmation of P0 items on 22 Oct 2026'),
]
D['recheck'] = [dict(id=x[0], http=x[1], hits=x[2], snippet=x[3] if len(x) > 3 else '') for x in rc]
D['cat'] = {k: v for k, v in CLS.items()}
D['stats']['category'] = dict(collections.Counter(r['category'] for r in R))
D['stats']['vstatus'] = dict(collections.Counter(r['vstatus'] for r in R))
D['stats']['res'] = dict(collections.Counter(r['res_status'] for r in R))
D['obs_at'] = '2026-10-21 10:22–10:45 (full capture) · 2026-10-22 14:48 (P0 re-confirmation) — Asia/Riyadh'
json.dump(D, open(OUT, 'w'), ensure_ascii=False, indent=1)
print(json.dumps({k: D['stats'][k] for k in ('category', 'vstatus', 'res', 'plevel')}, ensure_ascii=False))
