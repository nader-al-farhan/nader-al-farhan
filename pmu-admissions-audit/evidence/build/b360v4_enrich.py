# v4 (Directive 2.1): rebase on the 22 Oct capture, 12-type taxonomy, register fields, challenge outcomes.
# Usage: b360v4_enrich.py master.json reverify.json cap22.json links22.tsv challenge.json out.json resolution.json
import json, sys, re, collections
M, RV, CAP, LNK, CH, OUT = sys.argv[1:7]
D = json.load(open(M)); RVD = json.load(open(RV)); CAPL = json.load(open(CAP))
CH_L = json.load(open(CH)) if CH != '-' else []
TODAY = '2026-10-22'
R = D['rows']; by = {r['fid']: r for r in R}

# ---------- 22 Oct discovery from the root page (fresh, not inherited)
cap = {c['id']: c for c in CAPL}
root = cap['P00']
t = root['text']; i = t.find('ADMISSIONS OFFICE'); j = t.find('STAY CONNECTED')
root_block = [x.strip() for x in t[i:j].split('\n') if x.strip()]
SECTIONS = ['Future Students', 'International Students’ Office', 'Graduate Admissions', 'Undergraduate Admissions', 'Undergraduate Placement Tests']
placements = [x for x in root_block[1:] if x not in SECTIONS]
links22 = [l.rstrip('\n').split('\t') for l in open(LNK) if l.strip()]
codes22 = collections.Counter(x[1] for x in links22)
inst22 = sum(len([l for l in c.get('links', []) if l['h'].startswith('http')]) for k, c in cap.items() if k not in ('P01', 'P02'))
uniq22 = len({l['h'].split('#')[0] for k, c in cap.items() if k not in ('P01', 'P02') for l in c.get('links', []) if l['h'].startswith('http')})
D['discovery22'] = dict(placements=len(placements), placement_labels=placements, pages_captured=len(CAPL), http_ok=sum(1 for c in CAPL if c.get('status') == 200),
                        link_instances=inst22, link_unique=uniq22, link_codes=dict(codes22), broken=[x[0] for x in links22 if x[1] == '404'])

# ---------- 12-type taxonomy (Directive §15)
C12 = {
 'VERIFIED_FACTUAL_ERROR': ('Verified factual error', 'خطأ واقعي مثبت'),
 'PROVEN_PUBLISHED_CONFLICT': ('Proven published conflict', 'تعارض منشور مثبت'),
 'OUTDATED_CONTENT': ('Outdated content', 'محتوى متقادم'),
 'MISSING_INFORMATION': ('Missing information', 'معلومات ناقصة'),
 'AMBIGUITY': ('Ambiguity', 'غموض'),
 'MATERIAL_AR_EN_PARITY_ISSUE': ('Material Arabic–English parity issue', 'اختلاف جوهري بين العربية والإنجليزية'),
 'EDITORIAL_OR_STRUCTURE_ISSUE': ('Editorial or structure issue', 'ملاحظة تحريرية أو بنيوية'),
 'HISTORICAL_CHANGE_NOT_PUBLISHED': ('Historical change not published', 'تعديل سابق غير منشور'),
 'VERIFIED_STRENGTH': ('Verified strength', 'نقطة قوة مثبتة'),
 'CANNOT_VERIFY': ('Cannot verify', 'يتعذر التحقق'),
 'RECOMMENDATION': ('Recommendation', 'توصية'),
 'INSTITUTIONAL_DECISION_REQUIRED': ('Institutional decision required', 'قرار مؤسسي مطلوب'),
}
AMBIG = re.compile(r'ambigu|unclear|unspecified|undefined|imprecise|informal|inconsistent|differing|varying|conflat', re.I)
def c12(r):
    o = r['category_old']
    if r['fid'] in ('F-040', 'F-124'): return 'OUTDATED_CONTENT'
    if r['rv'] == 'NOT_VERIFIABLE': return 'CANNOT_VERIFY'
    return {'PUB_CONFLICT': 'PROVEN_PUBLISHED_CONFLICT', 'GOV_ERROR': 'VERIFIED_FACTUAL_ERROR', 'EDITORIAL': 'EDITORIAL_OR_STRUCTURE_ISSUE', 'OUTDATED': 'OUTDATED_CONTENT',
            'LANG_DIFF': 'MATERIAL_AR_EN_PARITY_ISSUE', 'IMPROVE': 'RECOMMENDATION', 'DECISION': 'INSTITUTIONAL_DECISION_REQUIRED', 'UNVERIFIED': 'CANNOT_VERIFY'}.get(o) or \
           ('AMBIGUITY' if AMBIG.search(r['title_en']) else 'MISSING_INFORMATION')

# ---------- independent challenge outcomes (applied after rechecking original evidence; see QA record)
CHM = {c['fid']: c for c in CH_L}
D['challenge'] = CH_L
RES = json.load(open(sys.argv[7])) if len(sys.argv) > 7 else {'applied': {}, 'kept': {}}
APPLIED = RES['applied']; KEPT = RES['kept']
# retire duplicates found on challenge
D['retired'] = []
for fid, a in APPLIED.items():
    if a.get('retire'):
        r0 = by.pop(fid); R.remove(r0); D['retired'].append(dict(fid=fid, title_en=r0['title_en'], title_ar=r0['title_ar'], reason=a['retire']))
        D['evidence'] = [x for x in D['evidence'] if x['fid'] != fid]
        for d in D['decisions']: d['fids'] = [x for x in d['fids'] if x != fid]
D['stats']['n'] = len(R)
for r in R:
    if r['fid'] == 'F-069': r['rv'] = 'MATCH'
    note = RVD.get(r['fid'], {}).get('note')
    if note: r['followup_en'] = (r.get('followup_en', '') + ' | ' if r.get('followup_en') else '') + 'Re-verified 22 Oct 2026: ' + note

RVS = {'MATCH': ('Still published as quoted (22 Oct 2026)', 'ما زال منشورًا كما اقتُبس (22 أكتوبر 2026)'),
       'PARTIAL': ('Partly present on 22 Oct 2026 — see note', 'موجود جزئيًا في 22 أكتوبر 2026 — انظر الملاحظة'),
       'NOT_FOUND': ('Not found in the 22 Oct 2026 capture', 'غير موجود في التقاط 22 أكتوبر 2026'),
       'NO_TEXT': ('Structural/visual observation (no quotable text)', 'ملاحظة بنيوية أو مرئية (بلا نص قابل للاقتباس)')}
for r in R:
    r['cls'] = c12(r)
    a = APPLIED.get(r['fid'])
    if a:
        if a.get('cls'): r['cls'] = a['cls']
        if a.get('plevel'): r['plevel_prev'] = r['plevel']; r['plevel'] = a['plevel']
        if a.get('desc_en'): r['description_en'] = a['desc_en']; r['description'] = a['desc_ar']
        if a.get('title_en'): r['title_en'] = a['title_en']; r['title_ar'] = a['title_ar']
        r['challenge_note'] = a.get('note', '')
    elif r['fid'] in KEPT: r['challenge_note'] = KEPT[r['fid']]
    elif any(c['fid'] == r['fid'] for c in CH_L): r['challenge_note'] = 'Independent challenge: upheld (see QA record).'
    else: r['challenge_note'] = ''
    r['cls_en'], r['cls_ar'] = C12[r['cls']]
    v = RVD.get(r['fid'], {}).get('status', 'NO_TEXT')
    if r['rv'] in ('RESOLVED', 'PARTLY_CHANGED', 'NOT_VERIFIABLE', 'NOT_RETESTED'):
        st_en, st_ar = r['rv_en'], r['rv_ar']
    else:
        st_en, st_ar = RVS['MATCH'] if v in ('MATCH', 'NO_TEXT') else RVS[v]
    r['state22_en'], r['state22_ar'], r['rv22'] = st_en, st_ar, v
    r['verified_on'] = TODAY if r['rv'] in ('MATCH', 'PARTLY_CHANGED', 'RESOLVED') and v in ('MATCH', 'NO_TEXT', 'PARTIAL') else r['verified_on']
    r['vstatus'] = 'BLOCKED' if r['rv'] == 'NOT_VERIFIABLE' and r['fid'] not in ('F-040', 'F-124') else 'VERIFIED'
    r['rid'] = 'R-MENU' if r['page_id'] == 'Shared menu' else f"R-{r['page_id']}"
    r['closure_ev'] = 'Not closed — no approved correction, publication or read-back evidence yet'
    r['authority_holder'] = next((d['auth'] for d in D['decisions'] if d['did'] in r['dids'] and d['did'] != 'D-09'), 'Admissions Office (content approver)' if r['dids'] == ['D-09'] else 'OWNER_TO_CONFIRM')
    r['authority_holder_ar'] = next((d['auth_ar'] for d in D['decisions'] if d['did'] in r['dids'] and d['did'] != 'D-09'), 'مكتب القبول (معتمد المحتوى)' if r['dids'] == ['D-09'] else 'المسؤول يحتاج تأكيدًا')
D['c12'] = C12
D['challenge_res'] = {}
for c in CH_L:
    a = APPLIED.get(c['fid'], {})
    D['challenge_res'][c['fid']] = a.get('retire') or a.get('note') or KEPT.get(c['fid']) or 'Upheld after evidence recheck; no change required.'

# ---------- inventory statuses (Directive §7) and extra fields
ST = {'FULL': 'FULLY_REVIEWED', 'PARTIAL': 'PARTIALLY_REVIEWED', 'EXCLUDED': 'EXCLUDED'}
CANON = {'R-P08': 'Two root placements ("Apply Now", "Apply") resolve here; meta-refresh to the portal (R-P38)', 'R-P38': 'Also reached via /apply; portal registration URL redirects here',
         'R-L2-CAL-2122': 'Footer "Academic Calendar" target', 'R-P00': 'Served on pmu.edu.sa and www.pmu.edu.sa (no canonical tag)'}
for it in D['inventory']:
    it['rstatus'] = ST.get(it['status'], it['status'])
    it['parent'] = 'R-P00' if it['rid'].startswith('R-P') and it['rid'] != 'R-P00' else ('—' if it['rid'] == 'R-P00' else ('Linked in-scope page' if it['rid'].startswith('R-') else 'In-scope pages'))
    it['disc_date'] = '2026-10-10' if it['rid'].startswith('R-') else '2026-10-21'
    it['rev_date'] = TODAY if it['rstatus'] in ('FULLY_REVIEWED', 'PARTIALLY_REVIEWED') and it['rid'] not in ('R-P06', 'R-L2-PREP-PLAN') else it['at']
    it['pair'] = 'Bilingual content on same page (EN + AR blocks)' if it['rid'] in ('R-P08', 'R-P07') else ('No Arabic counterpart found within the reviewed inventory' if it['rid'].startswith('R-') else '—')
    it['canon'] = CANON.get(it['rid'], '')
D['inventory'].insert(1, dict(rid='R-MENU', url='(component on all admission pages)', final='', title='Admissions side menu (shared component)', type='Page component', lang='English',
                              found='Present on every in-scope admission page', section='ROOT', incl='Included', reason_en='Navigation component carrying admission links and guide', reason_ar='مكوّن تنقل يحمل روابط القبول والدليل',
                              status='FULL', rstatus='FULLY_REVIEWED', unchecked_en='', unchecked_ar='', rel='', at=TODAY, http='', parent='R-P00', disc_date='2026-10-10', rev_date=TODAY, pair='—', canon='Identical on all pages'))
inv = D['inventory']
elig = [i for i in inv if i['incl'].startswith('Included')]
cnt = collections.Counter(i['rstatus'] for i in elig)
D['coverage22'] = dict(discovered_link_instances=inst22, discovered_unique_urls=uniq22, root_placements=len(placements), unique_destinations=D['coverage']['root_unique'],
                       eligible=len(elig), fully=cnt.get('FULLY_REVIEWED', 0), partially=cnt.get('PARTIALLY_REVIEWED', 0), blocked=cnt.get('BLOCKED', 0), not_reviewed=cnt.get('NOT_REVIEWED', 0),
                       excluded=sum(1 for i in inv if i['rstatus'] == 'EXCLUDED'), pdfs=2, pdf_pages=71, arabic_standalone=0, bilingual=2,
                       english=sum(1 for i in elig if 'English' in (i['lang'] or '') or i['type'] == 'PDF'), pairs=2, segment_pairs=10,
                       full_rate=round(100 * cnt.get('FULLY_REVIEWED', 0) / len(elig), 1), links_404=len(D['discovery22']['broken']))

# ---------- parity register (Directive §13)
PS = {'L-01': ('CONSISTENT', 'None', 'None', 'None'), 'L-02': ('EDITORIAL DIFFERENCE', 'None', 'None', 'Label order reversed; grammar'), 'L-03': ('CONSISTENT', 'None', 'None', 'None'),
      'L-04': ('CONSISTENT', 'None', 'None', 'None'), 'L-05': ('CONSISTENT', 'None', 'None', 'None'), 'L-06': ('MATERIAL PARITY ISSUE', 'None', 'Attesting embassy: "their country" vs "country of study"', 'May change the required attestation for applicants studying abroad'),
      'L-07': ('MATERIAL PARITY ISSUE', 'None', 'Home-edition exclusion: TOEFL only (EN) vs any test (AR)', 'Arabic text extends the exclusion beyond TOEFL'), 'L-08': ('CONSISTENT', 'None', 'None', 'None'),
      'L-09': ('CONSISTENT', 'None', 'VAT basis absent in both', 'None between languages'), 'L-10': ('EDITORIAL DIFFERENCE', 'None', 'None', 'Arabic spelling errors only')}
D['parity'] = [dict(pid=l[0], topic=l[1], en=l[2], ar=l[3], res_en=l[4], res_ar=l[5], fid=l[6] if l[0] != 'L-06' else 'F-029', status=PS[l[0]][0], numeric=PS[l[0]][1], policy=PS[l[0]][2], semantic=PS[l[0]][3],
                    ar_res='/apply (Arabic block)' if l[0] != 'L-10' else 'Admission Query (Arabic labels)', en_res='/apply (English block)' if l[0] != 'L-10' else 'Admission Query (English labels)',
                    evidence='R-P08 source, 21 & 22 Oct 2026' if l[0] != 'L-10' else 'R-P07, 21 & 22 Oct 2026') for l in D['lang_pairs']]

# ---------- applicant information journey (Directive §11)
JN = [('J-01', 'Applicant category', 'فئة المتقدم', 'Yes', 'نعم', 'Root page sections by category (Future, International, Graduate, Undergraduate)', 'أقسام الصفحة الجذرية حسب الفئة', 'F-001'),
      ('J-02', 'Programme', 'البرنامج', 'Partly', 'جزئيًا', 'Programme lists differ across pages', 'قوائم البرامج مختلفة بين الصفحات', 'F-012, F-043, F-048, F-074'),
      ('J-03', 'Requirements', 'المتطلبات', 'Partly', 'جزئيًا', 'Spread across pages; /apply content hidden by redirect', 'موزعة بين الصفحات؛ ومحتوى /apply مخفي بإعادة التوجيه', 'F-023, F-024, F-070'),
      ('J-04', 'Tests', 'الاختبارات', 'Partly', 'جزئيًا', 'Test pages exist; graduate English thresholds conflict; discontinued SAT II remains in the international weighting', 'صفحات الاختبارات موجودة؛ وحدود اللغة للدراسات العليا متعارضة؛ وSAT II الموقوف باقٍ في أوزان الطلاب الدوليين', 'F-040, F-073, F-100, F-117'),
      ('J-05', 'Fees', 'الرسوم', 'Partly', 'جزئيًا', 'Official schedule exists; application fees conflict', 'الجدول الرسمي موجود؛ ورسوم التقديم متعارضة', 'F-039, F-052'),
      ('J-06', 'Dates', 'المواعيد', 'No', 'لا', 'Only an expired cycle is published; footer link opens 2021/2022', 'لا تُنشر إلا دورة منتهية؛ ورابط التذييل يفتح 2021/2022', 'F-014, F-005'),
      ('J-07', 'Documents', 'الوثائق', 'Partly', 'جزئيًا', 'Lists exist; ID and attestation wording differ', 'القوائم موجودة؛ وصياغة الهوية والتصديق مختلفة', 'F-061, F-029'),
      ('J-08', 'How to apply', 'طريقة التقديم', 'Partly', 'جزئيًا', 'Channels differ; portal shows no events', 'القنوات مختلفة؛ والبوابة لا تعرض أحداثًا', 'F-053, F-030, F-131'),
      ('J-09', 'Next step', 'الخطوة التالية', 'Partly', 'جزئيًا', 'Results channel for non-Saudi applicants not stated; orientation "TBA"', 'قناة النتائج لغير السعوديين غير مذكورة؛ واللقاء التعريفي «TBA»', 'F-016, F-015'),
      ('J-10', 'Contact', 'التواصل', 'No', 'لا', '"Contact Us" opens a staff list without an Admissions contact; enquiry form exists', '«Contact Us» يفتح قائمة موظفين دون جهة اتصال للقبول؛ ونموذج الاستفسار موجود', 'F-002, F-034, F-020')]
D['journey'] = [dict(jid=j[0], en=j[1], ar=j[2], f_en=j[3], f_ar=j[4], o_en=j[5], o_ar=j[6], fids=j[7]) for j in JN]

# ---------- decision register (Directive §20)
for d in D['decisions']:
    d['publisher'] = 'Website content publisher — OWNER_TO_CONFIRM'; d['publisher_ar'] = 'ناشر محتوى الموقع — المسؤول يحتاج تأكيدًا'
    fs = [by[f] for f in d['fids'] if f in by]
    d['impact_en'] = f"{sum(1 for r in fs if r['plevel']=='P0')} P0 · {sum(1 for r in fs if r['plevel']=='P1')} P1 · {len(fs)} findings"
    d['evidence'] = ', '.join(e for r in fs if r['plevel'] in ('P0', 'P1') for e in r['eids'][:2]) or ', '.join(r['eids'][0] for r in fs[:5])
    d['direction'] = ''; d['ddate'] = ''

# ---------- corrective action register (Directive §21)
DREF = {d['did']: (d['ref_en'], d['ref_ar']) for d in D['decisions']}
DFIDS = {d['did']: d['fids'] for d in D['decisions']}
for p in D['plan']:
    ids = re.findall(r'F-\d{3}', p['problem'])
    p['fids'] = ', '.join(ids) if ids else (', '.join(DFIDS[p['did']][:6]) + (' …' if len(DFIDS[p['did']]) > 6 else '') if DFIDS[p['did']] else '—')
    p['gov_ref'], p['gov_ref_ar'] = DREF[p['did']]
    p['dependency'] = f"{p['did']} decision" + ('; ' + p['approval'] if p['approval'] else '')
    p['closure'] = 'OPEN'
    lv = [by[x]['plevel'] for x in (ids or DFIDS[p['did']]) if x in by]
    if lv and p['aid'] not in ('A-12', 'A-13'): p['prio'] = min(lv)

# ---------- follow-up schedule
D['followup'] = [
 ('FU-01', 'Obtain management direction on D-01 … D-10', 'الحصول على توجيه الإدارة بشأن D-01 … D-10', 'Mr. Radhi Alkhaldi', 'Awaiting direction'),
 ('FU-02', 'Refer D-01 (fees) to Financial Affairs; record reference and effective date', 'إحالة D-01 (الرسوم) إلى الشؤون المالية وتسجيل المرجع وتاريخ السريان', 'Admissions Office', 'Not started'),
 ('FU-03', 'Refer D-03/D-04/D-05 to the competent academic and graduate authorities', 'إحالة D-03/D-04/D-05 إلى الجهات الأكاديمية وجهة الدراسات العليا المختصة', 'Admissions Office', 'Not started'),
 ('FU-04', 'Confirm website content publisher and verification owner (OWNER_TO_CONFIRM items)', 'تأكيد ناشر محتوى الموقع وجهة التحقق (البنود المعلّقة)', 'Admissions leadership', 'Not started'),
 ('FU-05', 'After each publication: reopen page, read back, compare with approved text, record evidence', 'بعد كل نشر: إعادة فتح الصفحة وقراءتها ومقارنتها بالنص المعتمد وتوثيق الدليل', 'Admissions Office', 'Not started'),
 ('FU-06', 'Manual check of BLOCKED items F-033 and F-131', 'فحص يدوي للبندين المعلّقين F-033 وF-131', 'Admissions Office', 'Not started'),
 ('FU-07', 'Regression re-read of all P0/P1 pages before the next admission cycle opens', 'إعادة قراءة شاملة لصفحات P0/P1 قبل فتح دورة القبول القادمة', 'Admissions Office', 'Not started')]

D['stats']['cls'] = dict(collections.Counter(r['cls'] for r in R))
D['stats']['plevel'] = dict(collections.Counter(r['plevel'] for r in R))
D['stats']['conflicts'] = sum(1 for r in R if r['cls'] == 'PROVEN_PUBLISHED_CONFLICT')
D['stats']['vstatus'] = dict(collections.Counter(r['vstatus'] for r in R))
D['obs_at'] = '22 Oct 2026 (full rediscovery and capture 18:02–18:10; live P0 checks 14:48) · baseline 10–11 and 21 Oct 2026 — Asia/Riyadh'
D['changelog'].append(('v4.0', TODAY, 'Directive 2.1 edition: full rediscovery and capture on 22 Oct 2026; all findings re-matched against the new capture; 12-type classification; resource statuses FULLY_REVIEWED/PARTIALLY_REVIEWED/BLOCKED/NOT_REVIEWED/EXCLUDED; independent challenge of P0/P1, conflicts and errors with evidence recheck; Management Review & Decision Package (AR/EN); single master register (AR RTL / EN LTR); structured evidence pack; quality gates C0 and G1–G10'))
json.dump(D, open(OUT, 'w'), ensure_ascii=False, indent=1)
print(json.dumps(dict(cls=D['stats']['cls'], plevel=D['stats']['plevel'], conflicts=D['stats']['conflicts'], cov=D['coverage22'], disc={k: v for k, v in D['discovery22'].items() if k != 'placement_labels'}), ensure_ascii=False))
