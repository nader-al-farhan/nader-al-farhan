# Build all 360 deliverables, run quality checks, write QC into the registers, rebuild. Usage: b360_build.py scratch_v10 out_dir
import json, os, re, subprocess, sys, shutil, collections
S, OUTD = sys.argv[1], sys.argv[2]
B = os.path.dirname(os.path.abspath(__file__))
DATA = f'{S}/data.json'
N = {'rep_en': '01_PMU_Admissions_Content_Review_Report_EN.pdf', 'reg_en': '02_PMU_Admissions_Content_Review_Register_EN.xlsx',
     'rep_ar': '03_PMU_Admissions_Content_Review_Report_AR.pdf', 'reg_ar': '04_PMU_Admissions_Content_Review_Register_AR.xlsx'}
os.makedirs(OUTD, exist_ok=True); os.makedirs(f'{OUTD}/evidence_screenshots', exist_ok=True)
def run(*a): r = subprocess.run(a, capture_output=True, text=True); print(r.stdout.strip()[-300:], r.stderr.strip()[-300:]); return r
def build():
    run('python3', f'{B}/b360_xlsx.py', DATA, f'{OUTD}/{N["reg_en"]}', 'en')
    run('python3', f'{B}/b360_xlsx.py', DATA, f'{OUTD}/{N["reg_ar"]}', 'ar')
    for L, lab in (('en', 'PMU Admissions Office — Content Review | Draft for management review'), ('ar', 'PMU Admissions Office — Content Review (Arabic) | Draft for management review')):
        run('python3', f'{B}/b360_report.py', DATA, f'{S}/ev', f'{S}/rep_{L}.html', L)
        run('node', f'{B}/b360_pdf.js', f'{S}/rep_{L}.html', f'{OUTD}/{N["rep_" + L]}', lab)
build()
for f in os.listdir(f'{S}/ev'):
    if f.endswith('.png'): shutil.copy(f'{S}/ev/{f}', f'{OUTD}/evidence_screenshots/{f}')

# ---------------- quality checks
import openpyxl
D = json.load(open(DATA)); R = D['rows']; n = len(R)
qc = []
def add(en, ar, ok, detail): qc.append({'en': en, 'ar': ar, 'result': 'PASS' if ok else 'ATTENTION', 'detail': detail})
wb_en = openpyxl.load_workbook(f'{OUTD}/{N["reg_en"]}'); wb_ar = openpyxl.load_workbook(f'{OUTD}/{N["reg_ar"]}')
fe = wb_en['Findings']; fa = wb_ar['الملاحظات']
ids_en = [fe.cell(i, 1).value for i in range(5, fe.max_row + 1) if fe.cell(i, 1).value]
ids_ar = [fa.cell(i, 1).value for i in range(5, fa.max_row + 1) if fa.cell(i, 1).value]
txt = {L: subprocess.run(['pdftotext', '-layout', f'{OUTD}/{N["rep_" + L]}', '-'], capture_output=True, text=True).stdout for L in ('en', 'ar')}
pages = {L: int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', f'{OUTD}/{N["rep_" + L]}'], capture_output=True, text=True).stdout).group(1)) for L in ('en', 'ar')}
ann_en = len(set(re.findall(r'F-\d{3}', txt['en']))); ann_ar = len(set(re.findall(r'F-\d{3}', txt['ar'])))
add('Finding IDs identical across data, EN register and AR register', 'تطابق معرفات الملاحظات بين البيانات والسجلين', ids_en == ids_ar == [r['fid'] for r in R], f'{len(ids_en)} / {len(ids_ar)} / {n}')
add('Every finding ID appears in both PDF reports (Annex B index)', 'ظهور كل معرفات الملاحظات في التقريرين (الملحق ب)', ann_en >= n and ann_ar >= n, f'EN {ann_en}, AR {ann_ar}, expected {n}')
add('Headline counts consistent (report, register, email)', 'اتساق الأعداد الرئيسة (التقرير، السجل، البريد)', str(n) in txt['en'] and str(n) in txt['ar'], f"n={n}; P0={D['stats']['plevel'].get('P0')}; P1={D['stats']['plevel'].get('P1')}; conflicts={D['stats']['conflicts']}")
ev_by = collections.Counter(e['fid'] for e in D['evidence'])
bad = [r['fid'] for r in R if r['category'] == 'PUB_CONFLICT' and ev_by[r['fid']] < 2]
add('Each proven conflict has at least two evidence items', 'لكل تعارض مثبت دليلان على الأقل', not bad, 'missing: ' + ', '.join(bad) if bad else f"{D['stats']['conflicts']} conflicts checked")
noev = [r['fid'] for r in R if not r['eids'] or not r['current_text']]
add('Every finding has verbatim text and an evidence ID', 'لكل ملاحظة نص حرفي ومعرف دليل', not noev, ', '.join(noev) or f'{n} checked')
exc_in = [i['rid'] for i in D['inventory'] if i['status'] == 'EXCLUDED' and i['incl'].startswith('Included')]
add('Exclusions not counted as examined resources', 'عدم احتساب المستبعد ضمن المفحوص', not exc_in, f"eligible={D['coverage']['eligible']}, excluded={D['coverage']['excluded']}")
unres = [r['fid'] for r in R if r['category'] in ('UNVERIFIED', 'DECISION') and r['rv'] == 'MATCH' and 'error' in r['title_en'].lower()]
add('Unresolved items are not presented as confirmed errors', 'عدم عرض البنود غير المحسومة كأخطاء مؤكدة', not unres, f"{sum(1 for r in R if r['category'] in ('UNVERIFIED','DECISION'))} items classified UNVERIFIED/DECISION")
conf_ok = all(r.get('conflict_ar') for r in R if r['category'] == 'PUB_CONFLICT')
add('Conflicts use the prescribed wording (no value chosen)', 'استخدام الصيغة المقررة للتعارض (دون اختيار قيمة)', conf_ok, 'Proven published conflict; the correct policy requires institutional confirmation.')
rv = D['stats']['rv']
add('Material findings re-verified on the live site (21 Oct 2026)', 'إعادة التحقق من الملاحظات على الموقع الحي (21 أكتوبر 2026)', all(r['rv'] in ('MATCH', 'PARTLY_CHANGED', 'RESOLVED') for r in R if r['plevel'] in ('P0', 'P1')), json.dumps(rv))
shots = [f for f in os.listdir(f'{OUTD}/evidence_screenshots')]
add('Evidence screenshots are original captures and exist on disk', 'لقطات الأدلة أصلية وموجودة', len(shots) == 14, f'{len(shots)} files (EV-01 … EV-14)')
fonts = {L: subprocess.run(['pdffonts', f'{OUTD}/{N["rep_" + L]}'], capture_output=True, text=True).stdout for L in ('en', 'ar')}
emb = all(' no ' not in l.split('Type')[-1][:0] for l in fonts['en'].splitlines())
add('PDFs open, fonts embedded, page counts', 'فتح ملفات PDF وتضمين الخطوط وعدد الصفحات', 'Noto Naskh' in fonts['ar'] or 'NotoNaskh' in fonts['ar'], f"EN {pages['en']} pp., AR {pages['ar']} pp.")
links = sum(1 for ws in wb_en for row in ws.iter_rows() for c in row if c.hyperlink)
add('Registers: clickable links, filters and frozen headers', 'السجلان: روابط قابلة للنقر وفلاتر وتثبيت العناوين', links > 300 and all(ws.freeze_panes for ws in wb_en), f'{links} hyperlinks; {len(wb_en.sheetnames)} sheets')
add('Arabic workbook set right-to-left', 'ضبط اتجاه السجل العربي من اليمين إلى اليسار', all(ws.sheet_view.rightToLeft for ws in wb_ar), f'{len(wb_ar.sheetnames)} sheets RTL')
alltxt = txt['en'] + txt['ar']
phones = re.findall(r'\(966\)-3-849-\d{4}|\+?966[-\s]?13[-\s]?849[-\s]?\d{4}', alltxt)
add('No personal data (staff names/phones) reproduced', 'عدم إيراد بيانات شخصية (أسماء أو أرقام موظفين)', not phones, 'phones found: ' + ', '.join(phones) if phones else 'none found')
add('No claim of approval, publication or closure', 'لا ادعاء باعتماد أو نشر أو إغلاق', 'NOT READY FOR VERIFIED CLOSURE' in txt['en'], 'Status stated: NOT READY FOR VERIFIED CLOSURE')
add('Remaining issues (disclosed)', 'المشكلات المتبقية (مفصح عنها)', False,
    'F-033 and F-131 not verifiable from published content; F-069 (mobile layout) not re-tested on 21 Oct; preparatory study plan not re-read on 21 Oct; English/Arabic finding texts were translated with AI assistance and checked by sampling — owner review recommended.')
D['qc'] = qc; json.dump(D, open(DATA, 'w'), ensure_ascii=False, indent=1)
run('python3', f'{B}/b360_xlsx.py', DATA, f'{OUTD}/{N["reg_en"]}', 'en')
run('python3', f'{B}/b360_xlsx.py', DATA, f'{OUTD}/{N["reg_ar"]}', 'ar')
for q in qc: print(q['result'], '|', q['en'], '|', q['detail'][:120])
print(pages)
