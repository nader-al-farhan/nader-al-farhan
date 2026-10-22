# Assemble the 360 review dataset (findings, evidence, inventory, coverage, language pairs, decisions, plan, QC).
import json, re, sys, hashlib, os, collections
S = sys.argv[1]                      # scratch v10 dir
OUT = sys.argv[2]                    # output data.json
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
R = json.load(open(f'{S}/rows_m.json'))
CAP = {c['id']: c for c in json.load(open(f'{S}/cap/capture.json'))}
PM = json.load(open(f'{REPO}/final_review/pagemap.json'))
EVS = {e['id']: e for e in json.load(open(f'{S}/ev/evshots.json'))}
ZIP = json.load(open(f'{S}/../v8/zip_inscope_v.json'))
OBS_AT = '2026-10-21 10:22–10:45 (Asia/Riyadh, UTC+3)'
OBS_DATE = '2026-10-21'

# ---------- page naming
SECT = {'P03':'FS','P04':'FS','P05':'FS','P06':'FS','P07':'FS','P08':'FS','P09':'ISO','P38':'APPLY'}
for i in range(10,24): SECT[f'P{i}']='GA'
for i in range(24,33): SECT[f'P{i}']='UA'
for i in range(33,38): SECT[f'P{i}']='UPT'
SECT_N = {'ROOT':('Root page','الصفحة الجذرية'),'FS':('Future Students','الطلاب المستقبليون'),'ISO':("International Students' Office",'مكتب الطلاب الدوليين'),
          'GA':('Graduate Admissions','القبول في الدراسات العليا'),'UA':('Undergraduate Admissions','القبول في البكالوريوس'),'UPT':('Undergraduate Placement Tests','اختبارات تحديد المستوى'),
          'APPLY':('Application route (redirect)','مسار التقديم (إعادة توجيه)'),'L2':('Level-2 resource (verification source)','مورد من المستوى الثاني (مصدر تحقق)'),'X':('Outside scope','خارج النطاق')}
def pname(pid, lang):
    if pid == 'Shared menu': return 'Admissions side menu (shared)' if lang=='en' else 'القائمة الجانبية لصفحات القبول'
    if lang=='ar': return PM[pid]['ar']
    t = PM[pid]['title'].strip().split('::')[0].strip()
    return t or pid

# ---------- re-verification statuses (21 Oct 2026)
RV_TXT = {'MATCH':('Re-verified: text unchanged','أُعيد التحقق: النص قائم دون تغيير')}
manual = {
 'F-003':'MATCH','F-004':'MATCH','F-008':'MATCH','F-022':'MATCH','F-023':'MATCH','F-024':'MATCH','F-025':'MATCH','F-026':'MATCH','F-027':'MATCH',
 'F-028':'MATCH','F-029':'MATCH','F-030':'MATCH','F-036':'MATCH','F-037':'MATCH','F-050':'MATCH','F-059':'MATCH','F-060':'MATCH','F-064':'MATCH',
 'F-065':'MATCH','F-078':'MATCH','F-111':'MATCH','F-113':'MATCH','F-118':'MATCH','F-121':'MATCH','F-123':'MATCH','F-129':'MATCH','F-130':'MATCH',
 'F-009':'PARTLY_CHANGED','F-019':'RESOLVED','F-035':'PARTLY_CHANGED','F-033':'NOT_VERIFIABLE','F-069':'NOT_RETESTED'}
RVL = {'MATCH':('Re-verified 21 Oct 2026 — still published','أُعيد التحقق 21 أكتوبر 2026 — ما زال منشورًا'),
       'PARTLY_CHANGED':('Partly changed since 11 Oct 2026 — residual issue remains','تغيّر جزئيًا منذ 11 أكتوبر 2026 — تبقى مشكلة متبقية'),
       'RESOLVED':('Appears resolved on 21 Oct 2026 — owner to confirm','يبدو أنه عولج في 21 أكتوبر 2026 — يحتاج تأكيد المالك'),
       'NOT_VERIFIABLE':('Not verifiable from published content','تعذر التحقق من المحتوى المنشور'),
       'NOT_RETESTED':('Verified 11 Oct 2026 (layout probe); not re-tested','تحقق في 11 أكتوبر 2026 (فحص العرض)؛ لم يُعد اختباره')}
RV_NOTE = {
 'F-009':('A meta description has since been added to the Admissions Office page; the multiple-host and legacy-URL issue remains.','أُضيف وصف للصفحة (meta description) إلى صفحة مكتب القبول، وتبقى مشكلة تعدد النطاقات وصيغ الروابط القديمة.'),
 'F-019':('On 21 Oct 2026 the "Apply Now" control on the Admissions Calendar page is a standard link (href="https://pmu.edu.sa/Apply"); no postback was found.','في 21 أكتوبر 2026 أصبح زر «Apply Now» في صفحة التقويم رابطًا عاديًا (https://pmu.edu.sa/Apply)، ولم يُرصد استدعاء postback.'),
 'F-035':('On 21 Oct 2026 the three scholarship links still return HTTP 404; the GPA-calculator link was not present among the in-scope links.','في 21 أكتوبر 2026 ما زالت روابط المنح الثلاثة تعيد الخطأ 404، ولم يظهر رابط حاسبة المعدل ضمن روابط النطاق.'),
 'F-036':('The PDF downloaded on 21 Oct 2026 is byte-identical (MD5 83e0d463…) to the copy reviewed on 11 Oct 2026; page 20 (image) states the SR 500 fee.','ملف PDF المنزّل في 21 أكتوبر 2026 مطابق بايتًا ببايت (MD5 83e0d463…) للنسخة المراجعة في 11 أكتوبر 2026؛ وتذكر الصفحة 20 (صورة) رسم 500 ريال.'),
}
for r in R:
    st = manual.get(r['fid'], r['reverify'])
    if st in ('NOT_FOUND','PARTIAL','NO_TEXT'): st = 'MATCH' if r['_hit'] else 'NOT_VERIFIABLE'
    r['rv'] = st

# ---------- new item from 21 Oct link check (unverifiable from this environment)
R.append({'fid':'F-131','page_id':'P28','url':'https://pmu.edu.sa/admission/admission-from-other-universities',
 'location':'«Complete online application» link (Transfer, Visiting and CS & Engineering pages)','current_text':'<a href="http://admissions.pmu.edu.sa/" class="anker">Complete online application</a>',
 'description':'تستخدم روابط «Complete online application» في صفحات التحويل والزائرين ومتطلبات الحاسب والهندسة بروتوكول http غير المشفّر لبوابة التقديم. ومن بيئة المراجعة لم يستجب العنوان عبر المنفذ 80 (انتهاء مهلة الاتصال عبر وكيل الشبكة)، بينما يعمل العنوان المشفّر https. لا يمكن الجزم بأثر ذلك على الجمهور.',
 'description_en':'The "Complete online application" links on the Transfer, Visiting and CS & Engineering requirements pages point to the unencrypted http:// address of the application portal. From the review environment the http address did not respond (connection timeout via the network proxy), whereas the https address works. The effect on the public cannot be confirmed from this environment.',
 'recommendation':'تحديث الروابط إلى https://admissions.pmu.edu.sa/welcome، والتحقق يدويًا من سلوك الرابط الحالي من متصفح عام.','recommendation_ar':'تحديث الروابط إلى https://admissions.pmu.edu.sa/welcome، والتحقق يدويًا من سلوك الرابط الحالي من متصفح عام.',
 'recommendation_en':'Update the links to https://admissions.pmu.edu.sa/welcome and manually check the current link behaviour from a public browser.',
 'title_en':'Application links use the unencrypted portal address (http)','title_ar':'روابط التقديم تستخدم عنوان البوابة غير المشفّر (http)',
 'location_en':'"Complete online application" link (Transfer, Visiting and CS & Engineering pages)','note':'','note_en':'',
 'category':'UNVERIFIED','plevel':'P2','rationale_en':'Could block the primary application step if the http address fails publicly; effect not yet confirmed.',
 'rationale_ar':'قد يعطّل خطوة التقديم الرئيسة إذا تعذّر العنوان http لدى الجمهور؛ والأثر غير مؤكد بعد.','owner_en':'Website content publisher','owner_ar':'ناشر محتوى الموقع',
 'conflict_statement':'','axis':'وظيفي وتقني','type':'رابط غير آمن','classification':'متابعة وتحقق','priority':'متوسطة','refs':['LINKCHECK-2026-10-21'],
 'page_name_ar':PM['P28']['ar'],'page_title_en':PM['P28']['title'],'rv':'NOT_VERIFIABLE','group':'NEW'})

CAT = {'PUB_CONFLICT':('Proven published conflict','تعارض منشور مثبت'),'GOV_ERROR':('Error proven against a governing reference','خطأ مثبت بمرجع حاكم'),
       'GAP':('Documented gap or ambiguity','نقص أو غموض موثق'),'OUTDATED':('Outdated information proven no longer valid','معلومة متقادمة ثبت عدم سريانها'),
       'LANG_DIFF':('Material Arabic–English difference','اختلاف عربي–إنجليزي مؤثر'),'EDITORIAL':('Editorial or organisational note','ملاحظة تحريرية أو تنظيمية'),
       'IMPROVE':('Improvement recommendation','توصية تحسين'),'DECISION':('Institutional decision required','قرار مؤسسي مطلوب'),
       'UNVERIFIED':('Could not be verified','حالة تعذر التحقق منها'),'STRENGTH':('Proven strength','نقطة قوة مثبتة')}
PL = {'P0':('Proven serious impact: may mislead an admission decision or cause direct financial/procedural harm','أثر جسيم مثبت قد يضلل قرار القبول أو يسبب ضررًا ماليًا أو إجرائيًا مباشرًا'),
      'P1':('High impact on applicants or operations; limited interim mitigation possible','أثر مرتفع على المتقدم أو التشغيل مع إمكانية معالجة مؤقتة محدودة'),
      'P2':('Significant clarity, consistency or findability issue','مشكلة مهمة في الوضوح أو الاتساق أو سهولة الوصول'),
      'P3':('Limited editorial or organisational improvement','تحسين تحريري أو تنظيمي محدود الأثر')}
CONFLICT_AR = 'تعارض منشور مثبت؛ السياسة الصحيحة تحتاج تأكيدًا مؤسسيًا.'

# second sources for proven conflicts (each conflict needs >= 2 evidence items)
SECOND = {'F-012':['P22','P00'],'F-024':['P37','P31'],'F-027':['P24'],'F-029':['P24','P09'],'F-030':['P05'],'F-039':['P28','L2-STU-FEES'],
          'F-050':['P08','P09'],'F-052':['L2-MED-FEES'],'F-061':['P26','P09'],'F-065':['L2-PREP-PLAN'],'F-070':['P37','P08'],
          'F-073':['L2-GR-FORM','P17'],'F-100':['L2-MILBL-FORM'],'F-117':['P36','P08']}
URLX = {k: (CAP[k]['final'] if k in CAP else None) for k in CAP}
URLX['L2-PREP-PLAN'] = 'https://www.pmu.edu.sa/admission/preparatory-program-study-plan'
URLX['P08'] = 'https://www.pmu.edu.sa/apply'
SHOT = {'F-014':['EV-01'],'F-039':['EV-02','EV-03'],'F-040':['EV-04'],'F-052':['EV-05','EV-06'],'F-073':['EV-07','EV-08'],'F-097':['EV-09'],
        'F-119':['EV-10'],'F-005':['EV-11'],'F-100':['EV-12','EV-13'],'F-030':['EV-14']}

ev = []
for r in R:
    r['cat_en'], r['cat_ar'] = CAT[r['category']]
    r['page_en'] = pname(r['page_id'], 'en'); r['page_ar'] = pname(r['page_id'], 'ar')
    r['section'] = SECT.get(r['page_id'], 'ROOT' if r['page_id'] in ('P00','Shared menu') else 'L2')
    if r['category'] == 'PUB_CONFLICT':
        r['conflict_statement'] = 'Proven published conflict; the correct policy requires institutional confirmation.'; r['conflict_ar'] = CONFLICT_AR
    else: r['conflict_ar'] = ''
    r['rv_en'], r['rv_ar'] = RVL[r['rv']]
    r['rv_note_en'], r['rv_note_ar'] = RV_NOTE.get(r['fid'], ('', ''))
    # evidence
    eids = []
    pid = r['page_id']; src = r['url'] if r['url'].startswith('http') else 'https://pmu.edu.sa/admission/admission'
    e = {'eid': f"E-{r['fid'][2:]}-1", 'fid': r['fid'], 'url': src, 'excerpt': r['current_text'], 'locator': r.get('location_en', ''),
         'locator_ar': r['location'], 'observed': OBS_DATE if r['rv'] in ('MATCH','PARTLY_CHANGED','RESOLVED') else '2026-10-11',
         'first_observed': '2026-10-10/11', 'pub_date': '', 'shot': ', '.join(f'{s}.png' for s in SHOT.get(r['fid'], [])),
         'page_shot': f'{pid}_full.jpg' if pid in CAP else ''}
    if r['fid'] == 'F-036': e['pub_date'] = 'PDF created/modified 2018-12-20 (file metadata)'; e['locator'] += ' — PDF p. 20 (image), pp. 1–21 read'
    if r['fid'] == 'F-121': e['pub_date'] = 'PDF created 2017-08-30, modified 2019-03-12 (file metadata)'
    ev.append(e); eids.append(e['eid'])
    for k, p2 in enumerate(SECOND.get(r['fid'], []), 2):
        e2 = {'eid': f"E-{r['fid'][2:]}-{k}", 'fid': r['fid'], 'url': URLX.get(p2, ''), 'excerpt': '(counterpart statement quoted in E-%s-1)' % r['fid'][2:],
              'locator': 'Counterpart page', 'locator_ar': 'الصفحة المقابلة', 'observed': OBS_DATE if p2 != 'L2-PREP-PLAN' else '2026-10-11', 'first_observed': '2026-10-10/11',
              'pub_date': '', 'shot': '', 'page_shot': f'{p2}_full.jpg' if p2 in CAP else ''}
        ev.append(e2); eids.append(e2['eid'])
    r['eids'] = eids

# ---------- strengths
STR = [
 ('S-01','P31','HS GPA out of 100 ≥ 85 40% Qudrat ≥ 65 30% Tahseely ≥ 65 30%','Undergraduate CS & Engineering requirements are published as a structured table of minimum marks and weights, which allows applicants to self-assess eligibility.','تُنشر متطلبات تخصصات الحاسب والهندسة في جدول منظم للحدود الدنيا والأوزان، مما يمكّن المتقدم من تقدير أهليته ذاتيًا.'),
 ('S-02','L2-STU-FEES','Admission Application Fees- Undergraduate Programs Fees (includes the VAT 15%) Non-refundable SAR 950','The official fees page states the application fee, its VAT basis (15% included) and non-refundability explicitly, providing a natural single reference for fee statements.','تنص صفحة الرسوم الرسمية صراحةً على رسم التقديم وأساسه الضريبي (شامل 15%) وعدم استرداده، فتصلح مرجعًا موحدًا لبيانات الرسوم.'),
 ('S-03','P08','IELTS Academic: Overall 6.0, Writing 5.5 TOEFL iBT: Overall 83, Writing 19','The /apply page presents undergraduate requirements in parallel English and Arabic, and the numerical values match in both languages (see Language Comparison).','تعرض صفحة /apply متطلبات البكالوريوس بالإنجليزية والعربية بالتوازي، وتتطابق القيم الرقمية في اللغتين (انظر ورقة المقارنة اللغوية).'),
 ('S-04','P05','For Saudi Students: Apply online through Qabool platform … For non Saudi Students: Apply online through Study in Saudi platform','The Admissions Calendar distinguishes application channels by applicant category (Saudi via Qabool; non-Saudi via Study in Saudi) and lists dated milestones.','يميز تقويم القبول قنوات التقديم حسب فئة المتقدم (السعوديون عبر «قبول» وغير السعوديين عبر «ادرس في السعودية») ويعرض محطات مؤرخة.'),
 ('S-05','P36','Two years from the date of TOEFL iBT test … (online or home edition is not accepted) … PMU DI code: 6993','The TOEFL page specifies score validity, excluded test formats and the institutional score-reporting code, which reduces avoidable submission errors.','تحدد صفحة TOEFL مدة صلاحية النتيجة والصيغ غير المقبولة ورمز الجامعة لإرسال النتائج، مما يقلل أخطاء التقديم الممكن تجنبها.'),
 ('S-06','P25','Total weighted score* 60% Interview 40% *20% high school + 40% Qudrat + 40% Tahseely','The College of Medicine page publishes its selection method (weighted score and interview weights) and a minimum score, which supports transparency of a competitive admission decision.','تنشر صفحة كلية الطب نموذج المفاضلة (أوزان النسبة الموزونة والمقابلة) وحدًّا أدنى، مما يدعم شفافية قرار قبول تنافسي.'),
 ('S-07','P07','مرحباً بكم بجامعة الأمير محمد بن فهد، مكتب القبول يسعد بالإجابة على إستفساراتكم','A bilingual Admission Query form gives applicants a direct written channel to the Admissions Office.','يوفر نموذج استفسار القبول ثنائي اللغة قناة كتابية مباشرة للتواصل مع مكتب القبول.'),
 ('S-08','P22','A 15% VAT will be charged for Tuition and Fees for Non-Saudi Students … Saudi Students do not pay VAT for Tuition','The graduate fees page states VAT treatment for Saudi students explicitly and publishes PMU-alumni and non-alumni tuition side by side.','تنص صفحة رسوم الدراسات العليا صراحةً على معاملة ضريبة القيمة المضافة للطلاب السعوديين، وتعرض رسوم خريجي الجامعة وغيرهم جنبًا إلى جنب.'),
]
def norm(s): return re.sub(r'\s+', ' ', s).replace('…', '').strip()
strengths = []
for sid, pid, snip, en, ar in STR:
    raw = norm(CAP[pid]['raw'])
    parts = [p.strip() for p in snip.split('…')]
    ok = all(norm(p) in raw for p in parts)
    strengths.append({'sid': sid, 'pid': pid, 'url': CAP[pid]['final'] if pid != 'P08' else 'https://www.pmu.edu.sa/apply', 'excerpt': snip, 'en': en, 'ar': ar, 'verified': ok,
                      'page_en': pname(pid, 'en') if pid in PM else 'Other Fees (Tuition & Fees)', 'page_ar': PM[pid]['ar'] if pid in PM else 'الرسوم الأخرى'})
# P08 raw comes from /apply source (meta refresh) – verify there
apply_txt = norm(re.sub(r'<[^>]+>', ' ', open(f'{S}/raw/APPLY_noredirect.html', errors='ignore').read()))
for s in strengths:
    if s['pid'] == 'P08': s['verified'] = all(norm(p) in apply_txt for p in s['excerpt'].split('…'))

# ---------- inventory
inv = []
def add(rid, url, final, title, typ, lang, found, sect, incl, reason_en, reason_ar, status, unchecked_en, unchecked_ar, rel='', at=OBS_DATE, http=''):
    inv.append(dict(rid=rid, url=url, final=final, title=title, type=typ, lang=lang, found=found, section=sect, incl=incl, reason_en=reason_en, reason_ar=reason_ar,
                    status=status, unchecked_en=unchecked_en, unchecked_ar=unchecked_ar, rel=rel, at=at, http=http))
c0 = CAP['P00']
add('R-P00', 'https://www.pmu.edu.sa/admission/admission', c0['final'], c0['title'], 'HTML page', 'English (lang attribute empty)', 'START', 'ROOT', 'Included', 'Root page of the review', 'الصفحة الجذرية للمراجعة', 'FULL', '', '', http=c0['status'])
lab = {'P03':'Overview','P04':'Degrees & Programs','P05':'Admissions Calendar','P06':'Contact Us','P07':'Admission Query','P08':'Apply Now / Apply','P09':'International Students without Saudi Residence','P38':'(redirect from /apply)'}
for pid in sorted(k for k in PM if re.fullmatch(r'P\d\d', k)):
    if pid in ('P00',): continue
    c = CAP.get(pid)
    if pid in ('P01', 'P02'):
        add(f'R-{pid}', PM[pid]['url'], c['final'], c['title'], 'HTML page', 'English', 'Root page header/breadcrumb', 'X', 'Excluded', 'General university page reached through global navigation, not an admissions branch', 'صفحة عامة للجامعة يُوصل إليها من التنقل العام وليست فرعًا من فروع القبول', 'EXCLUDED', '', '', http=c['status']); continue
    if pid == 'P06':
        add('R-P06', 'https://pmu.edu.sa/Staff_Profile/Staff_List.aspx?&DEpt=4&Name=Staff%20Name', PM[pid]['url'], 'Department staff list', 'HTML page (external host)', 'English', 'Root › Future Students › Contact Us', 'FS', 'Included (link only)', 'Destination contains personal data; only the link target was checked', 'تحتوي الوجهة بيانات شخصية؛ فُحصت وجهة الرابط فقط', 'PARTIAL', 'Staff names and contacts not copied (personal data)', 'لم تُنسخ أسماء الموظفين وبياناتهم (بيانات شخصية)', at='2026-10-11'); continue
    if pid == 'P38':
        add('R-P38', 'https://admissions.pmu.edu.sa/welcome', c['final'], c['title'], 'Web application (public landing page)', 'English (lang="en")', 'Root › Apply Now → /apply (meta refresh)', 'APPLY', 'Included (public landing page only)', 'Public pre-login page of the application portal; login and forms excluded', 'الصفحة العامة لبوابة التقديم قبل الدخول؛ الدخول والنماذج مستبعدة', 'PARTIAL', 'Login, registration form use and applicant records excluded by mandate; registration labels read only from the portal’s published page files', 'الدخول واستخدام نموذج التسجيل وسجلات المتقدمين مستبعدة بحكم التكليف؛ قُرئت تسميات التسجيل من ملفات الصفحة المنشورة للبوابة فقط', http=c['status']); continue
    if pid == 'P08':
        add('R-P08', 'https://www.pmu.edu.sa/apply', c['final'], 'Admissions :: PMU (source of /apply)', 'HTML page (meta refresh)', 'English + Arabic (bilingual body)', 'Root › Future Students › Apply Now; ISO › Apply', 'FS', 'Included', 'Linked twice from the root page; body content read from page source', 'مرتبط مرتين من الصفحة الجذرية؛ قُرئ المحتوى من مصدر الصفحة', 'FULL', 'Content is not displayed to visitors because of the immediate redirect', 'لا يُعرض المحتوى للزائر بسبب إعادة التوجيه الفورية', rel='Bilingual pair (EN/AR blocks)', http=c['status']); continue
    t = c['title'].split('::')[0].strip() if c else ''
    add(f'R-{pid}', PM[pid]['url'], c['final'], c['title'], 'HTML page', 'English (lang attribute empty)', f"Root › {SECT_N[SECT[pid]][0]}" + (f" › {lab[pid]}" if pid in lab else ''), SECT[pid], 'Included', 'Direct link from the Admissions Office root page', 'رابط مباشر من صفحة مكتب القبول الجذرية', 'FULL', 'Images reviewed for informational content; no text-bearing images found' if pid != 'P05' else '', '', http=c['status'])
L2 = [('L2-STU-FEES','Other Fees (Tuition & Fees)','Fee verification (application, Aptis)','الرسوم الأخرى'),('L2-MED-FEES','Medical Program Fees','Medicine application fee verification','رسوم البرنامج الطبي'),
      ('L2-FEES-2627','Undergraduate fees 2026/2027','Fee schedule verification','رسوم البكالوريوس 2026/2027'),('L2-MILBL-FORM','MIBL application form','Counterpart of MIBL requirements','نموذج تقديم MIBL'),
      ('L2-GR-FORM','Graduate application form (generic)','Target of four "Application Form" links','نموذج التقديم العام للدراسات العليا'),('L2-LIST-MAJORS','List of majors','Programme-offering verification','قائمة التخصصات'),
      ('L2-CAL-2122','Academic Calendar 2021/2022','Target of the root-page footer "Academic Calendar" link','التقويم الأكاديمي 2021/2022')]
for rid, t, why, tar in L2:
    c = CAP[rid]
    add(f'R-{rid}', c['url'], c['final'], c['title'], 'HTML page', 'English', 'Linked from an in-scope page', 'L2', 'Included (verification source)', why, f'مصدر تحقق: {tar}', 'FULL', '', '', http=c['status'])
add('R-PDF-WAG', 'https://www.pmu.edu.sa/Attachments/Admission/Images/PDF/Web-Admission-Guide-v2-2_20-12-18.pdf', '', 'PMU Web Admission Guide (21 pages)', 'PDF', 'English', 'Admissions side menu › Web Admission Guide', 'L2', 'Included', 'Applicant guide linked from all admission pages', 'دليل للمتقدمين مرتبط من جميع صفحات القبول', 'FULL', 'All 21 pages read (text + page-image check of p. 20)', 'قُرئت الصفحات الـ21 كلها (النص والتحقق البصري من الصفحة 20)', http=200)
add('R-PDF-APTIS', 'https://www.pmu.edu.sa/Attachments/Admission/PDF/Appendix%203.3%20(Aptis%20Candidate%20Guide).pdf', '', 'Aptis Candidate Guide (50 pages)', 'PDF', 'English', 'Aptis page › Candidate Guide link', 'UPT', 'Included', 'Guide linked from the Aptis placement-test page', 'دليل مرتبط من صفحة اختبار Aptis', 'PARTIAL', 'Text of all 50 pages extracted; illustrations and sample-task images not individually inspected', 'استُخرج نص الصفحات الخمسين؛ لم تُفحص الرسوم وصور نماذج المهام كلٌّ على حدة', http=200)
add('R-L2-PREP-PLAN', 'https://www.pmu.edu.sa/admission/preparatory-program-study-plan', '', 'Preparatory Program study plan', 'HTML page', 'English', 'Preparatory Program pages', 'L2', 'Included (verification source)', 'Counterpart of the mathematics requirements table', 'مقابل جدول متطلبات الرياضيات', 'PARTIAL', 'Read on 11 Oct 2026; not re-read on 21 Oct 2026', 'قُرئت في 11 أكتوبر 2026؛ ولم يُعد فحصها في 21 أكتوبر 2026', at='2026-10-11')
for rid, url, t, why_en, why_ar in [
 ('X-EXT', 'etec.gov.sa; britishcouncil.org; uap.sa; studyinsaudi.sa; ets.org', 'External test and admission platforms', 'External official sites referenced for verification only', 'مواقع رسمية خارجية يُرجع إليها للتحقق فقط'),
 ('X-SYS', 'Banner, IT Helpdesk, Workflow, Webmail, Blackboard', 'Internal systems', 'Login-protected internal systems are excluded by mandate', 'الأنظمة الداخلية المحمية بتسجيل الدخول مستبعدة بحكم التكليف'),
 ('X-SOC', 'Facebook, X/Twitter, Instagram, LinkedIn, YouTube', 'Social media links', 'Not admissions content', 'ليست محتوى قبول'),
 ('X-GLOBAL', 'Header/footer navigation of pmu.edu.sa', 'University-wide navigation', 'Global menus are not treated as admissions branches', 'لا تُعامل القوائم العامة كفروع للقبول'),
 ('X-LEGACY', 'pmu.edu.sa/admission/* pages not linked from the current root (e.g. admission/default, legacy calendars)', 'Legacy or orphan admission pages', 'Not reachable from the current root page; listed for information only', 'لا يُوصل إليها من الصفحة الجذرية الحالية؛ تُذكر للعلم فقط')]:
    add(rid, url, '', t, 'Group', '', 'Links on in-scope pages', 'X', 'Excluded', why_en, why_ar, 'EXCLUDED', '', '')

# ---------- links
lst = [l.rstrip('\n').split('\t') for l in open(f'{S}/links_status.tsv') if l.strip()]
codes = collections.Counter(x[1].split(' ')[0] if len(x) > 1 else 'ERR' for x in lst)
link_inst = sum(1 for _ in open(f'{S}/links_all.tsv'))
broken = [x[0] for x in lst if len(x) > 1 and x[1].startswith('404')]

# ---------- coverage
elig = [i for i in inv if i['incl'].startswith('Included')]
full = [i for i in elig if i['status'] == 'FULL']; part = [i for i in elig if i['status'] == 'PARTIAL']
cov = dict(links_instances=link_inst, links_unique=len(lst), link_codes=dict(codes), broken=broken,
           root_placements=36, root_unique=35, resources_unique=len(inv), eligible=len(elig), full=len(full), partial=len(part),
           unreachable=0, not_examined=0, excluded=len([i for i in inv if i['status'] == 'EXCLUDED']), pdfs=2, pdf_pages=71, lang_pairs=1,
           pct_full=round(100 * len(full) / len(elig), 1), pct_any=round(100 * (len(full) + len(part)) / len(elig), 1))

# ---------- language comparison (/apply EN vs AR blocks + query form)
LP = [
 ('L-01','Non-engineering minimums','High school 80% or higher; Qudrat 60% or equivalent SAT 1 score','شهادة الثانوية العامة بنسبة 80% أو أعلى؛ اختبار القدرات العامة بنسبة 60% أو ما يعادلها من SAT 1','Consistent','متطابق',''),
 ('L-02','Non-engineering weights','High School GPA 60%; Qudrat / SAT 1 40%','الثانوية 60%؛ القدرات / 1 SAT 40%','Consistent values; Arabic label "1 SAT" reversed and heading "نسب الموزونة" ungrammatical','القيم متطابقة؛ وتسمية «1 SAT» معكوسة وعنوان «نسب الموزونة» غير سليم نحويًا','F-028'),
 ('L-03','AI/CS/Architecture/Engineering minimums','85% / Qudrat 65% / Tahseely 65%; SAT 1 1200 in place of both Qudrat and Tahseely','85% / القدرات 65% / التحصيلي 65%؛ SAT 1 بدرجة 1200 بديلًا عن القدرات والتحصيلي','Consistent','متطابق','F-024'),
 ('L-04','AI/CS/Architecture/Engineering weights','40% / 30% / 30%','40% / 30% / 30%','Consistent','متطابق',''),
 ('L-05','Lower-percentage note','Students with a lower percentage can apply; acceptance will depend on the overall weight','يمكن للطلاب الحاصلين على نسبة أقل التقديم، إلا أن القبول يعتمد على النسبة الموزونة','Consistent','متطابق','F-027'),
 ('L-06','International certificate attestation','Have the certificate stamped by the Saudi Embassy in their country','تصديق الشهادة من السفارة السعودية في بلد الدراسة','Editorial difference: "their country" vs "country of study" — may differ for applicants studying abroad','اختلاف تحريري: «بلدهم» مقابل «بلد الدراسة» — قد يختلف لمن درس خارج بلده','F-029'),
 ('L-07','Direct-entry English tests','IELTS Academic 6.0 (Writing 5.5); TOEFL iBT 83 (Writing 19); TOEFL Home Edition not accepted','الآيلتس الأكاديمي 6.0 (الكتابة 5.5)؛ التوفل iBT 83 (الكتابة 19)؛ لا يُقبل اختبار النسخة المنزلية','Values consistent; Arabic note does not name TOEFL, so its scope is wider in Arabic','القيم متطابقة؛ والملاحظة العربية لا تسمّي TOEFL فيتسع نطاقها بالعربية','F-028'),
 ('L-08','Interview','The Admission Office will schedule an appointment for a personal interview','سيقوم مكتب القبول بتحديد موعد لإجراء مقابلة شخصية','Consistent','متطابق',''),
 ('L-09','Application fee','A non-refundable application fee of SAR 950','950 ريالًا رسوم تقديم غير مستردة','Consistent; neither version states the VAT basis','متطابق؛ ولا تذكر أيٌّ من النسختين أساس الضريبة','F-026'),
 ('L-10','Admission Query welcome','The Admissions Office is glad to answer your inquiries. Please fill the below request:','مكتب القبول يسعد بالإجابة على إستفساراتكم. الرجاء ملء الطلب أدناه','Consistent meaning; Arabic spelling errors (إستفساراتكم، الأسم)','المعنى متطابق؛ وفي العربية أخطاء إملائية (إستفساراتكم، الأسم)','F-022'),
]
LANG_NOTE = ('No separate Arabic version of the Admissions Office page or its branches was found within the inventoried scope. Steps: (1) inspected all 46 captured resources for language-switch links and /ar/ paths; (2) checked page source for hreflang declarations; (3) reviewed header and footer navigation. Only /apply and the Admission Query form carry Arabic text, as bilingual content on the same page.',
             'لم يُعثر على مقابل عربي لصفحة مكتب القبول أو فروعها ضمن نطاق الجرد المفحوص. الخطوات: (1) فحص الموارد الـ46 الملتقطة بحثًا عن روابط تبديل اللغة ومسارات /ar/؛ (2) فحص مصدر الصفحات بحثًا عن وسوم hreflang؛ (3) مراجعة قوائم الرأس والتذييل. ولا يحمل نصًا عربيًا إلا صفحة /apply ونموذج استفسار القبول، بوصفه محتوى ثنائي اللغة في الصفحة نفسها.')

# ---------- decisions
D = [
 ('D-01','Application fees, VAT basis and test fees','رسوم التقديم وأساس الضريبة ورسوم الاختبارات',
  'Which application fee applies to each applicant category (international transfer/visiting, Medicine, undergraduate, graduate), on what VAT basis and from which effective date? What is the current Aptis (and retake) fee?',
  'ما رسم التقديم المعتمد لكل فئة (المحولون والزائرون الدوليون، الطب، البكالوريوس، الدراسات العليا)، وما أساسه الضريبي وتاريخ سريانه؟ وما الرسم الحالي لاختبار Aptis وإعادته؟',
  'A. Adopt the official Other Fees schedule as the single source and link all pages to it; B. Confirm category-specific exceptions in writing and publish them in the schedule.','أ. اعتماد جدول «الرسوم الأخرى» مصدرًا وحيدًا وربط الصفحات به؛ ب. تأكيد الاستثناءات حسب الفئة كتابيًا ونشرها في الجدول.',
  'Admissions Office + Financial Affairs','مكتب القبول + الشؤون المالية',['F-039','F-052','F-026','F-036','F-119','F-104','F-105','F-108','F-111']),
 ('D-02','Current admission cycle, calendar and application channels','دورة القبول الحالية والتقويم وقنوات التقديم',
  'Is an admission cycle currently open (e.g. Spring 2027)? Which dates, channels (Qabool, Study in Saudi, PMU portal) and orientation date apply, and what should be shown while no cycle is open?',
  'هل توجد دورة قبول مفتوحة حاليًا (مثل ربيع 2027)؟ وما المواعيد والقنوات (قبول، ادرس في السعودية، بوابة الجامعة) وموعد اللقاء التعريفي، وماذا يُعرض حين لا توجد دورة مفتوحة؟',
  'A. Publish the next cycle with dates; B. Publish an interim notice stating that applications are closed and when the next cycle opens.','أ. نشر الدورة القادمة بمواعيدها؛ ب. نشر إشعار مؤقت بإغلاق التقديم وموعد فتح الدورة القادمة.',
  'Admissions Office (with Registrar for the academic calendar)','مكتب القبول (مع التسجيل للتقويم الأكاديمي)',['F-014','F-015','F-005','F-030','F-041','F-053','F-016']),
 ('D-03','Undergraduate eligibility, test equivalences and weightings','أهلية البكالوريوس ومعادلات الاختبارات والأوزان',
  'Confirm for each applicant category: accepted tests (SAT I/II, Tahseely, IELTS, TOEFL), minimum scores, SAT 1 (1200) substitution rules, minimum weighted totals (including the values requested on 26 Oct 2025), identity documents and attestation authority.',
  'تأكيد ما يلي لكل فئة: الاختبارات المقبولة (SAT I/II، التحصيلي، IELTS، TOEFL) والحدود الدنيا، وقواعد بديل SAT 1 (1200)، والحد الأدنى للنسبة الموزونة (بما فيها القيم المطلوبة في 26 أكتوبر 2025)، ووثائق الهوية وجهة التصديق.',
  'A. One approved undergraduate admission matrix referenced by all pages; B. Page-by-page correction after written confirmation.','أ. مصفوفة قبول بكالوريوس معتمدة واحدة تحيل إليها الصفحات؛ ب. تصحيح الصفحات كلًّا على حدة بعد التأكيد الكتابي.',
  'Admissions Office + relevant colleges / Preparatory Program','مكتب القبول + الكليات المعنية / البرنامج التحضيري',['F-040','F-023','F-024','F-025','F-027','F-042','F-054','F-059','F-060','F-071','F-070','F-117','F-124','F-065','F-067','F-061','F-029','F-050']),
 ('D-04','Graduate eligibility and English-language requirements','أهلية الدراسات العليا ومتطلبات اللغة الإنجليزية',
  'Which IELTS/TOEFL thresholds govern each graduate programme (6.0 vs 6.5; EMGMS 7), which GPA rules apply (PhD BA 2.80/3.00/3.20; "Very Good"), and which programme-specific conditions (work experience, written test, duration) are current?',
  'ما حدود IELTS وTOEFL المعتمدة لكل برنامج دراسات عليا (6.0 مقابل 6.5؛ وEMGMS 7)، وما قواعد المعدل (دكتوراه الأعمال 2.80/3.00/3.20؛ «جيد جدًا»)، وما الشروط الخاصة السارية (الخبرة، الاختبار التحريري، المدة)؟',
  'A. Approved graduate entry matrix by programme; B. Remove non-PMU text (EMGMS) immediately and confirm values afterwards.','أ. مصفوفة قبول معتمدة للدراسات العليا حسب البرنامج؛ ب. إزالة النص غير الخاص بالجامعة (EMGMS) فورًا ثم تأكيد القيم.',
  'Graduate programme owners + Admissions Office','مالكو برامج الدراسات العليا + مكتب القبول',['F-073','F-100','F-097','F-077','F-084','F-087','F-099','F-092','F-095','F-101','F-089']),
 ('D-05','Programme portfolio and official names','البرامج المطروحة وأسماؤها الرسمية',
  'Which programmes are currently open for admission (including B.S. Chemical Engineering, EMGMS, the Master of Engineering in Innovation, Sustainability and Entrepreneurship, Medicine), and what are their official names and abbreviations?',
  'ما البرامج المفتوحة للقبول حاليًا (بما فيها الهندسة الكيميائية وEMGMS وماجستير الهندسة في الابتكار والاستدامة وريادة الأعمال والطب)، وما أسماؤها واختصاراتها الرسمية؟',
  'A. Publish one authoritative programme list used by all admission pages; B. Mark programmes not open for admission.','أ. نشر قائمة برامج معتمدة واحدة تستخدمها صفحات القبول كلها؛ ب. وسم البرامج غير المفتوحة للقبول.',
  'Admissions Office + college/programme owners','مكتب القبول + الكليات ومالكو البرامج',['F-012','F-043','F-048','F-074','F-106','F-094','F-083']),
 ('D-06','Legacy guides and linked resources','الأدلة القديمة والموارد المرتبطة',
  'Should the 2018 Web Admission Guide and the 2017 Aptis guide be withdrawn, replaced or archived, and who restores or removes the broken scholarship links?',
  'هل يُسحب دليل التقديم الإلكتروني (2018) ودليل Aptis (2017) أو يُستبدلان أو يؤرشفان، ومن يعالج روابط المنح المعطلة أو يزيلها؟',
  'A. Withdraw now and replace later; B. Replace before withdrawal; C. Archive with a dated "historical" label.','أ. السحب الآن والاستبدال لاحقًا؛ ب. الاستبدال قبل السحب؛ ج. الأرشفة بوسم «تاريخي» مؤرخ.',
  'Admissions Office + website content publisher','مكتب القبول + ناشر محتوى الموقع',['F-036','F-121','F-035']),
 ('D-07','Contact channels and enquiry-form privacy','قنوات التواصل وخصوصية نموذج الاستفسار',
  'Which official Admissions contact details (email, telephone, hours) should be published, and which privacy notice applies to the Admission Query form and the portal?',
  'ما بيانات التواصل الرسمية لمكتب القبول (البريد والهاتف وأوقات العمل) الواجب نشرها، وما إشعار الخصوصية المنطبق على نموذج الاستفسار والبوابة؟',
  'A. Publish an official Admissions contact block on every admissions page; B. Link the university privacy notice from forms.','أ. نشر بيانات تواصل رسمية لمكتب القبول في كل صفحات القبول؛ ب. ربط إشعار الخصوصية الجامعي من النماذج.',
  'Admissions Office (privacy wording: owner to be confirmed)','مكتب القبول (صياغة الخصوصية: المسؤول يحتاج تأكيدًا)',['F-002','F-020','F-034','F-044','F-110','F-031']),
 ('D-08','Content ownership, review cycle and single source of truth','ملكية المحتوى ودورية المراجعة والمصدر الموحد',
  'Who is the accountable owner and approver for each admissions page, what review cycle applies (e.g. before each cycle opens), and should pages display a "last reviewed" date?',
  'من المالك والمعتمد المسؤول عن كل صفحة قبول، وما دورية المراجعة (مثل: قبل فتح كل دورة)، وهل تُعرض «آخر مراجعة» على الصفحات؟',
  'A. Named owner per page plus a pre-cycle review; B. Central editor with owner sign-off.','أ. مالك مسمّى لكل صفحة مع مراجعة قبل كل دورة؛ ب. محرر مركزي مع اعتماد المالك.',
  'Admissions leadership','قيادة القبول',[]),
 ('D-09','Approval of ready editorial corrections','اعتماد التصحيحات التحريرية الجاهزة',
  'May the 48 editorial corrections (Annex sheet) and the editorial findings be implemented directly, given that none changes a value or requirement?',
  'هل يجوز تنفيذ التصحيحات التحريرية الـ48 (ورقة المرفق) والملاحظات التحريرية مباشرة، علمًا بأن أيًّا منها لا يغيّر قيمة أو شرطًا؟',
  'A. Approve as a batch; B. Approve page by page.','أ. الاعتماد دفعة واحدة؛ ب. الاعتماد صفحة صفحة.',
  'Admissions Office (content approver)','مكتب القبول (معتمد المحتوى)',[r['fid'] for r in R if r['category'] == 'EDITORIAL']),
 ('D-10','Accessibility and technical publishing baseline','الحد الأدنى للإتاحة والنشر التقني',
  'Should admissions pages meet a stated accessibility baseline (e.g. WCAG 2.1 AA: language attribute, image alternatives, landmarks, mobile reflow) and secure links?',
  'هل تلتزم صفحات القبول بحد أدنى معلن للإتاحة (مثل WCAG 2.1 AA: سمة اللغة، بدائل الصور، المعالم، الملاءمة للجوال) وبروابط آمنة؟',
  'A. Adopt WCAG 2.1 AA for admissions pages; B. Address listed items only.','أ. اعتماد WCAG 2.1 AA لصفحات القبول؛ ب. معالجة البنود المرصودة فقط.',
  'Website content publisher / IT (owner to be confirmed)','ناشر محتوى الموقع / تقنية المعلومات (المسؤول يحتاج تأكيدًا)',['F-003','F-004','F-008','F-069','F-009','F-131']),
]
decisions = [dict(did=d[0], t_en=d[1], t_ar=d[2], q_en=d[3], q_ar=d[4], alt_en=d[5], alt_ar=d[6], owner_en=d[7], owner_ar=d[8], fids=d[9]) for d in D]
fid2d = collections.defaultdict(list)
for d in decisions:
    for f in d['fids']: fid2d[f].append(d['did'])
for r in R: r['dids'] = fid2d.get(r['fid'], [])

# ---------- amendments of 26 Oct 2025 (status at 21 Oct 2026)
AM = [
 ('A-1','Minimum weighted scores 74% (CS & Engineering) / 72% (non-Engineering) with competitive-minimum and interview note','الحد الأدنى للمجموع الموزون 74% (الحاسب والهندسة) و72% (غير الهندسية) مع ملاحظة المفاضلة والمقابلة','Not reflected','لم يُنفَّذ','No "74%" or "72%" appears on any captured page; the CS & Engineering page refers to a "minimum weighted total, defined by the Admissions Office".','لا ترد «74%» أو «72%» في أي صفحة ملتقطة؛ وتشير صفحة الحاسب والهندسة إلى «حد أدنى للمجموع الموزون يحدده مكتب القبول».','D-03'),
 ('A-2','Addition of B.S. Chemical Engineering','إضافة برنامج B.S. Chemical Engineering','Partially reflected','منفّذ جزئيًا','Listed on Degrees & Programs and the list of majors; absent from the special-requirements majors list on the CS & Engineering requirements page.','مدرج في صفحتي الدرجات والبرامج وقائمة التخصصات؛ وغير مدرج في قائمة التخصصات ذات المتطلبات الخاصة بصفحة الحاسب والهندسة.','D-05'),
 ('A-3','Application fee SAR 500 → SAR 950 for international, transfer and visiting students','رسم التقديم من 500 إلى 950 ريالًا للدوليين والمحولين والزائرين','Partially reflected','منفّذ جزئيًا','SAR 950 (incl. VAT) on Transfer and Visiting pages; SAR 500 (excl. VAT) remains on the International Students page. The request specified "excl. VAT"; the official schedule states "includes the VAT 15%".','950 ريالًا (شاملة الضريبة) في صفحتي التحويل والزائرين؛ ويبقى 500 ريال (غير شاملة) في صفحة الطلاب الدوليين. وقد نص الطلب على «excl. VAT» بينما ينص الجدول الرسمي على «شاملة ضريبة 15%».','D-01'),
 ('A-4','Removal of SAAT / SAT 2 requirement for CS & Engineering','إزالة اشتراط SAAT / SAT 2 للحاسب والهندسة','Partially reflected','منفّذ جزئيًا','Not present on the CS & Engineering requirements page; "SAT II 30%" remains on the International Students page.','غير موجود في صفحة متطلبات الحاسب والهندسة؛ ويبقى «SAT II 30%» في صفحة الطلاب الدوليين.','D-03'),
 ('A-5','APTIS retake fee SAR 575 → SAR 950 (VAT)','رسم إعادة APTIS من 575 إلى 950 ريالًا (مع الضريبة)','Not reflected','لم يُنفَّذ','"APTIS Exam Fees SAR 575" on the Other Fees page.','«APTIS Exam Fees SAR 575» في صفحة الرسوم الأخرى.','D-01'),
 ('A-6','Revision of the Web Admission Guide','تحديث دليل التقديم الإلكتروني','Not reflected','لم يُنفَّذ','The linked guide is unchanged (MD5-identical to 11 Oct 2026; dated December 2018; p. 20 states SR 500).','الدليل المرتبط لم يتغير (مطابق MD5 لنسخة 11 أكتوبر 2026؛ مؤرخ ديسمبر 2018؛ وتذكر الصفحة 20 رسم 500 ريال).','D-06'),
]
amend = [dict(aid=a[0], req_en=a[1], req_ar=a[2], st_en=a[3], st_ar=a[4], ev_en=a[5], ev_ar=a[6], did=a[7]) for a in AM]

# ---------- follow-up plan
PLAN = [
 ('A-01','Publish an interim notice on the current admission cycle on the root page and Admissions Calendar','نشر إشعار مؤقت بحالة دورة القبول في الصفحة الجذرية وتقويم القبول','P0','D-02','Admissions Office','Notice visible on both pages; dated','ظهور الإشعار مؤرخًا في الصفحتين'),
 ('A-02','Confirm the fee schedule by applicant category (incl. VAT basis) and align all fee statements','تأكيد جدول الرسوم حسب الفئة (مع أساس الضريبة) ومواءمة جميع بيانات الرسوم','P0','D-01','Admissions Office + Financial Affairs','Zero conflicting fee statements on re-read','صفر بيانات رسوم متعارضة عند إعادة القراءة'),
 ('A-03','Remove or replace the discontinued SAT II requirement after confirming the accepted alternative','إزالة اشتراط SAT II الموقوف أو استبداله بعد تأكيد البديل المقبول','P0','D-03','Admissions Office + colleges','Requirement aligned on all pages','مواءمة المتطلب في جميع الصفحات'),
 ('A-04','Remove non-PMU (UA CESL) text from the EMGMS page and confirm its English threshold','إزالة النص غير الخاص بالجامعة (UA CESL) من صفحة EMGMS وتأكيد حد اللغة','P1','D-04','Graduate programme owner + Admissions','Text removed; threshold confirmed','إزالة النص وتأكيد الحد'),
 ('A-05','Approve one graduate English-requirements matrix and correct the generic application form','اعتماد مصفوفة موحدة لمتطلبات اللغة للدراسات العليا وتصحيح نموذج التقديم العام','P1','D-04','Graduate programme owners','Form and programme pages match','تطابق النموذج وصفحات البرامج'),
 ('A-06','Approve one undergraduate admission matrix (tests, minimums, weights, documents)','اعتماد مصفوفة موحدة لقبول البكالوريوس (الاختبارات، الحدود، الأوزان، الوثائق)','P1','D-03','Admissions Office + colleges','All undergraduate pages reference the matrix','إحالة صفحات البكالوريوس كلها إلى المصفوفة'),
 ('A-07','Withdraw or replace the 2018 Web Admission Guide; restore or remove broken scholarship links','سحب دليل 2018 أو استبداله؛ ومعالجة روابط المنح المعطلة أو إزالتها','P1','D-06','Admissions Office + publisher','No 404 links; guide current or withdrawn','لا روابط 404؛ والدليل محدّث أو مسحوب'),
 ('A-08','Publish one authoritative programme list and fix programme naming','نشر قائمة برامج معتمدة واحدة وتصحيح أسماء البرامج','P1','D-05','Admissions Office + programme owners','Lists identical across pages','تطابق القوائم بين الصفحات'),
 ('A-09','Publish official Admissions contact details and link a privacy notice from forms','نشر بيانات التواصل الرسمية لمكتب القبول وربط إشعار الخصوصية من النماذج','P1','D-07','Admissions Office','Contact block and privacy link present','وجود بيانات التواصل ورابط الخصوصية'),
 ('A-10','Implement the 48 approved editorial corrections and editorial findings','تنفيذ التصحيحات التحريرية الـ48 والملاحظات التحريرية بعد اعتمادها','P2','D-09','Admissions content editor + publisher','Each corrected occurrence re-read and logged','إعادة قراءة كل موضع مصحح وتوثيقه'),
 ('A-11','Address the accessibility baseline items (lang attribute, alt text, landmarks, mobile reflow, https links)','معالجة بنود الإتاحة الأساسية (سمة اللغة، النص البديل، المعالم، الملاءمة للجوال، روابط https)','P2','D-10','Publisher / IT','Automated re-check passes for listed items','نجاح إعادة الفحص الآلي للبنود المرصودة'),
 ('A-12','Assign a named owner per page, set a pre-cycle review and display "last reviewed" dates','تعيين مالك لكل صفحة وتحديد مراجعة قبل كل دورة وإظهار تاريخ «آخر مراجعة»','P2','D-08','Admissions leadership','Owner register approved; dates visible','اعتماد سجل الملاك وظهور التواريخ'),
 ('A-13','Design and run a short applicant information-experience survey (design only in this review)','تصميم استبيان قصير لتجربة المتقدمين في الوصول إلى المعلومات وتنفيذه (التصميم فقط في هذه المراجعة)','P3','D-08','Admissions Office (owner to be confirmed)','Survey approved before any data collection','اعتماد الاستبيان قبل أي جمع بيانات'),
]
plan = [dict(aid=p[0], en=p[1], ar=p[2], prio=p[3], did=p[4], owner=p[5], kpi_en=p[6], kpi_ar=p[7]) for p in PLAN]

# ---------- editorial corrections annex (from remediation package, in scope)
edits = []
for e in sorted(ZIP['E'], key=lambda e: (not e['_v'], e['change_id'])):
    edits.append(dict(cid=e['change_id'], url=e['url'], before=e['before'], after=e['after'], verified=e['_v']))

# ---------- stats
cnt = lambda key: dict(collections.Counter(r[key] for r in R))
stats = dict(n=len(R), plevel=cnt('plevel'), category=cnt('category'), rv=cnt('rv'), conflicts=sum(1 for r in R if r['category'] == 'PUB_CONFLICT'),
             open=sum(1 for r in R if r['rv'] != 'RESOLVED'))

data = dict(obs_at=OBS_AT, obs_date=OBS_DATE, rows=R, evidence=ev, strengths=strengths, inventory=inv, coverage=cov, lang_pairs=LP, lang_note=LANG_NOTE,
            decisions=decisions, amend=amend, plan=plan, edits=edits, stats=stats, cat=CAT, pl=PL, sect=SECT_N)
json.dump(data, open(OUT, 'w'), ensure_ascii=False, indent=1)
print(json.dumps(stats, ensure_ascii=False)); print(json.dumps(cov, ensure_ascii=False)[:600]); print([ (s['sid'], s['verified']) for s in strengths])
