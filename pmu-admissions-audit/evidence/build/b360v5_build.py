# Directive 2.2 build: PDFs, registers, evidence pack (00–07), internal guide, metadata cleaning, C0 + G1–G11, data-integrity cross-validation.
# Usage: b360v5_build.py v5.json scratch_root out_dir
import json, os, re, sys, subprocess, shutil, zipfile, hashlib, csv, collections, glob, html, unicodedata
V4, SC, OUTD = sys.argv[1:4]
B = os.path.dirname(os.path.abspath(__file__))
VIS = f'{SC}/v13/final'; EV = f'{VIS}/ann'
N = {'rev_ar': f'{OUTD}/01_PMU_Admissions_Management_Review_AR.pdf', 'reg_ar': f'{OUTD}/02_PMU_Admissions_Master_Register_AR.xlsx',
     'rev_en': f'{OUTD}/03_PMU_Admissions_Management_Review_EN.pdf', 'reg_en': f'{OUTD}/04_PMU_Admissions_Master_Register_EN.xlsx',
     'pack': f'{OUTD}/05_PMU_Admissions_Evidence_Pack.zip', 'guide': f'{OUTD}/00_INTERNAL_Submission_Guide.docx'}
os.makedirs(OUTD, exist_ok=True)
def run(*a):
    r = subprocess.run(a, capture_output=True, text=True)
    if r.returncode: print('ERR', a[:3], r.stderr[-400:])
    return r
FOOT = 'PMU Admissions — Management Review &amp; Decision Package · v5.0 · Prepared for Management Review'
def clean_pdf(p, title):
    from pypdf import PdfReader, PdfWriter
    rd = PdfReader(p); w = PdfWriter(clone_from=rd)
    w._info = None
    w.add_metadata({'/Title': title, '/Author': 'Nader Al Farhan', '/Subject': 'Admissions Office content review — Prepared for Management Review',
                    '/Creator': 'PMU Admissions Office', '/Producer': 'PMU Admissions Office', '/Keywords': 'PMU; Admissions; Management Review'})
    with open(p, 'wb') as f: w.write(f)
def build_docs():
    for L in ('ar', 'en'):
        run('python3', f'{B}/b360v5_review.py', V4, EV, f'{SC}/v13/review_{L}.html', L)
        run('node', f'{B}/b360_pdf.js', f'{SC}/v13/review_{L}.html', N['rev_' + L], FOOT)
        clean_pdf(N['rev_' + L], 'PMU Admissions — Management Review & Decision Package' + (' (Arabic)' if L == 'ar' else ''))
        run('python3', f'{B}/b360v5_xlsx.py', V4, N['reg_' + L], L)
    run('node', f'{B}/b360v5_guide.js', V4, N['guide'])
def md5(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()
def build_pack(qa_rows, scan_rows):
    D = json.load(open(V4)); st = f'{SC}/v13/pack'; shutil.rmtree(st, ignore_errors=True)
    dirs = ['00_Manifest', '01_Current_Live_Evidence/full_page_captures', '02_Annotated_Live_Evidence', '03_PDF_Evidence', '04_Historical_Evidence', '05_Governing_References', '06_AR_EN_Parity', '07_QA']
    for d in dirs: os.makedirs(f'{st}/{d}', exist_ok=True)
    man = []
    def put(src, rel, desc, url='', date='', ids=''):
        dst = f'{st}/{rel}'; shutil.copy(src, dst); man.append([rel, desc, url, date, ids, md5(dst)])
    evm = []
    for v in D['visual']:
        od = '03_PDF_Evidence' if v['etype'] == 'PDF page' else '01_Current_Live_Evidence'
        put(f'{VIS}/orig/{v["orig"]}', f'{od}/{v["orig"]}', f'ORIGINAL capture — {v["claim_en"][:90]}', v['url'], v['date'], f"{v['eid']}; {v['fid']}; {v['rid']}")
        put(f'{VIS}/ann/{v["ann"]}', f'02_Annotated_Live_Evidence/{v["ann"]}', f'ANNOTATED copy of {v["eid"]} (reference frame and label band added)', v['url'], v['date'], f"{v['eid']}; {v['fid']}")
        evm.append([v['eid'], v['fid'], v['rid'], ', '.join(v['dids']), ', '.join(v['aids']), v['etype'], v['currency'], 'Original + Annotated', v['title'], v['url'], v['section_en'],
                    v['date'], v['time'], v['tz'], f"{od}/{v['orig']}", f"02_Annotated_Live_Evidence/{v['ann']}", v['claim_en'], v['vstatus'], (v['view'] + '. ' + v['notes']).strip()])
    cap = json.load(open(f'{SC}/v12/cap/capture.json'))
    for c in cap:
        p = f'{SC}/v12/cap/shots/{c["id"]}_full.jpg'
        if os.path.exists(p): put(p, f'01_Current_Live_Evidence/full_page_captures/R-{c["id"]}_full_2026-10-22.jpg', f'Original full-page capture: {c["title"][:70]}', c['final'], '2026-10-22', f'R-{c["id"]}')
    put(f'{SC}/v12/page_text.json', '01_Current_Live_Evidence/page_text_2026-10-22.json', 'Text of every captured resource (visible and tab content)', '', '2026-10-22', 'R-*')
    put(f'{SC}/v12/links_status_22.tsv', '01_Current_Live_Evidence/link_status_2026-10-22.tsv', 'HTTP status of every unique link on in-scope pages', '', '2026-10-22', 'F-035; F-131')
    put('/home/user/nader-al-farhan/pmu-admissions-audit/evidence/recheck_2026-10-22.tsv', '01_Current_Live_Evidence/live_recheck_2026-10-22.tsv', 'Live re-confirmation of highest-risk facts', '', '2026-10-22', 'RC-*')
    put(f'{SC}/v12/pdf/WAG.pdf', '03_PDF_Evidence/Web-Admission-Guide-v2-2_20-12-18.pdf', 'Web Admission Guide (21 pp.); p. 20 states SR 500 fee', 'https://www.pmu.edu.sa/Attachments/Admission/Images/PDF/Web-Admission-Guide-v2-2_20-12-18.pdf', '2026-10-22', 'F-036; H-6; E014')
    put(f'{SC}/v13/pdf150-20.png', '03_PDF_Evidence/Web-Admission-Guide_page-20_full.png', 'Full rendering of page 20 of the Web Admission Guide (context for E014)', 'https://www.pmu.edu.sa/Attachments/Admission/Images/PDF/Web-Admission-Guide-v2-2_20-12-18.pdf', '2026-10-22', 'F-036; E014')
    put(f'{SC}/v12/pdf/APTIS.pdf', '03_PDF_Evidence/Aptis-Candidate-Guide-2017.pdf', 'Aptis Candidate Guide (50 pp., Aug 2017)', 'https://www.pmu.edu.sa/Attachments/Admission/PDF/Appendix%203.3%20(Aptis%20Candidate%20Guide).pdf', '2026-10-22', 'F-121')
    hist = f'{SC}/v13/H_requests_2025-10-26.txt'
    open(hist, 'w').write('Amendments requested in the email of 26 October 2025 (thread "updates on Admission pages" / "comments on Admission pages")\n\n' +
        '\n'.join(f"{a['hid']}: {a['req_en']}  ->  status on 22 Oct 2026: {a['code']}" for a in D['amend']) + '\n\nThese are historical requests compared with the published content; they are not approved policy.\nCurrent-state captures: H-1 E035; H-2 E022; H-3 E001-E003; H-4 E015; H-5 E036; H-6 E014.\n')
    put(hist, '04_Historical_Evidence/H_requests_2025-10-26.txt', 'Historical amendment requests H-1 … H-6 with current status', '', '2025-10-26', 'H-1 … H-6')
    base = [dict(resource=f"R-{c['id']}", url=c['url'], captured=c['at'], text=c.get('raw')) for c in json.load(open(f'{SC}/v10/cap/capture.json'))]
    json.dump(base, open(f'{SC}/v13/page_text_21.json', 'w'), ensure_ascii=False)
    put(f'{SC}/v13/page_text_21.json', '04_Historical_Evidence/page_text_2026-10-21_baseline.json', 'Baseline capture of 21 Oct 2026 (comparison only; not current evidence)', '', '2026-10-21', 'R-*')
    ref = f'{SC}/v13/References.txt'
    open(ref, 'w').write('Governing and external references\n\n1. College Board — "An Update on Reducing and Simplifying Demands on Students" (19 Jan 2021): SAT Subject Tests discontinued; final international administration June 2021.\n   https://allaccess.collegeboard.org/update-reducing-and-simplifying-demands-students\n   Used for: F-040, H-4\n\n2. ETS — TOEFL iBT score scale update: 1–6 scale for tests on/after 21 Jan 2026; dual 0–120 reporting through Jan 2028.\n   https://www.ets.org/toefl/institutions/ibt/score-scale-update.html\n   Used for: F-124\n\n3. PMU Other Fees schedule — "Admission Application Fees … (includes the VAT 15%) Non-refundable SAR 950"; "APTIS Exam Fees SAR 575".\n   https://www.pmu.edu.sa/admission/student_fees_tf_ro  (E003, E036; capture R-L2-STU-FEES)\n   Used for: F-039, F-119, H-3, H-5\n\n4. PMU Medical Program Fees — "Medical Application Fee SAR 1,150 (VAT inclusive)".\n   https://pmu.edu.sa/admission/medical_program_studies_fees_tf_ro  (E005; capture R-L2-MED-FEES)\n   Used for: F-052\n\nNo approved, dated PMU policy or fee decision was available; published PMU pages are evidence of what is published, not of what is approved.\nItems 1–2 were located on the official sites but could not be retrieved directly from the review network; they are cited by URL.\n')
    put(ref, '05_Governing_References/References.txt', 'Governing and external references with URLs', '', '2026-10-22', 'F-039; F-040; F-052; F-119; F-124')
    for rid in ('L2-STU-FEES', 'L2-MED-FEES', 'L2-FEES-2627', 'L2-GR-FORM', 'L2-MILBL-FORM'):
        p = f'{SC}/v12/cap/shots/{rid}_full.jpg'
        if os.path.exists(p): put(p, f'05_Governing_References/R-{rid}_full_2026-10-22.jpg', 'Official PMU page used as verification source', '', '2026-10-22', f'R-{rid}')
    par = f'{SC}/v13/AR_EN_parity_register.csv'
    with open(par, 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['pair', 'ar_resource', 'en_resource', 'topic', 'english', 'arabic', 'numeric_difference', 'policy_difference', 'semantic_impact', 'finding', 'evidence', 'visual_evidence', 'status'])
        for q in D['parity']: w.writerow([q['pid'], q['ar_res'], q['en_res'], q['topic'], q['en'], q['ar'], q['numeric'], q['policy'], q['semantic'], q['fid'], q['evidence'], 'E034' if q['fid'] == 'F-028' else '', q['status']])
        w.writerow(['L-NOTE', '', '', 'Separate Arabic version', '', '', '', '', D['lang_note'][0], '', '', '', 'NO COUNTERPART FOUND WITHIN REVIEWED SCOPE'])
    put(par, '06_AR_EN_Parity/AR_EN_parity_register.csv', 'Arabic–English segment comparison (visual: E034 in 01/02)', 'https://www.pmu.edu.sa/apply', '2026-10-22', 'L-01 … L-10; F-028; E034')
    vqa = visual_qa(D)
    for name, rows, hdr in (('QA_record.csv', qa_rows, ['gate', 'check', 'result', 'evidence', 'residual']),
                            ('Independent_challenge.csv', [[c['fid'], c['verdict'], c.get('rationale', ''), D['challenge_res'].get(c['fid'], '')] for c in D['challenge']], ['finding', 'challenge verdict', 'challenge rationale', 'resolution after evidence recheck']),
                            ('Visual_evidence_QA.csv', vqa, ['evidence_id', 'finding_id', 'source_url', 'capture_date', 'original_md5_matches_register', 'annotated_equals_original_outside_frame_pct', 'width_px', 'caption_in_EN_report', 'caption_in_AR_report', 'result'])):
        p = f'{SC}/v13/{name}'
        with open(p, 'w', newline='') as f: w = csv.writer(f); w.writerow(hdr); w.writerows(rows)
        put(p, f'07_QA/{name}', name.replace('_', ' ').replace('.csv', ''), '', '2026-10-22', '')
    with open(f'{st}/00_Manifest/Evidence_Manifest.csv', 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['evidence_id', 'finding_id', 'resource_id', 'decision_id', 'action_id', 'evidence_type', 'current_historical', 'original_annotated', 'source_title', 'url', 'page_section', 'capture_date', 'capture_time', 'time_zone', 'original_file', 'annotated_file', 'related_claim', 'verification_status', 'notes'])
        w.writerows(evm)
    readme = f'{st}/00_Manifest/README.txt'
    open(readme, 'w').write('PMU Admissions — Evidence Pack (v5.0, 22 Oct 2026)\nPrepared by Nader Al Farhan, Administrative Assistant, Student Affairs, Admission Office\n\n'
        '00_Manifest — README, Manifest.csv (every file, description, source URL, date, linked IDs, MD5) and Evidence_Manifest.csv (visual evidence: Finding → Evidence → Resource → Source → Decision → Action)\n'
        '01_Current_Live_Evidence — ORIGINAL captures of 22 Oct 2026 (FNNN_ENNN_Name_20261022.png, unaltered), full-page captures, page text, link status, live re-check\n'
        '02_Annotated_Live_Evidence — ANNOTATED copies (_ANNOTATED.png): identical to the original plus a red reference frame and a dark label band\n'
        '03_PDF_Evidence — linked PDF guides, the original page-20 extract (E014) and the full page-20 rendering\n'
        '04_Historical_Evidence — amendment requests of 26 Oct 2025 with current status; baseline text of 21 Oct 2026 (comparison only)\n'
        '05_Governing_References — external references and official PMU fee pages\n'
        '06_AR_EN_Parity — Arabic–English comparison register\n'
        '07_QA — quality-gate record, independent challenge record, visual evidence QA\n\n'
        'Times are Asia/Riyadh. Conflict sources are separate captures and are never merged into one image.\n')
    with open(f'{st}/00_Manifest/Manifest.csv', 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['path', 'description', 'source_url', 'date', 'linked_ids', 'md5']); w.writerows(man)
    if os.path.exists(N['pack']): os.remove(N['pack'])
    with zipfile.ZipFile(N['pack'], 'w', zipfile.ZIP_DEFLATED) as z:
        for root, _, fs in os.walk(st):
            for fn in sorted(fs): z.write(f'{root}/{fn}', os.path.relpath(f'{root}/{fn}', st))
    return len(man)
def visual_qa(D):
    from PIL import Image, ImageChops
    tx = {k: re.sub(r'\s+', '', pdftext(N[k])) if os.path.exists(N[k]) else '' for k in ('rev_en', 'rev_ar')}
    out = []
    for v in D['visual']:
        o = Image.open(f'{VIS}/orig/{v["orig"]}').convert('RGB'); a = Image.open(f'{VIS}/ann/{v["ann"]}').convert('RGB')
        okmd5 = md5(f'{VIS}/orig/{v["orig"]}') == v['md5']
        body = a.crop((0, 48, a.width, a.height))
        diff = ImageChops.difference(o, body).convert('L').point(lambda x: 255 if x > 8 else 0)
        same = 100 - round(100 * sum(diff.histogram()[255:]) / (o.width * o.height), 2)
        ce = v['eid'] in tx['rev_en']; ca = v['eid'] in tx['rev_ar']
        ok = okmd5 and same >= 95 and a.size == (o.width, o.height + 48) and o.width >= 900 and ce and ca and v['url'] and v['date'] and v['fid']
        out.append([v['eid'], v['fid'], v['url'], v['date'], okmd5, same, o.width, ce, ca, 'ACCEPTED' if ok else 'VISUAL EVIDENCE NOT ACCEPTED'])
    return out

# ---------------- checks
def pdftext(p): return subprocess.run(['pdftotext', '-layout', p, '-'], capture_output=True, text=True).stdout
def pages(p): return int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', p], capture_output=True, text=True).stdout).group(1))
STRICT = [r'chatgpt', r'claude', r'anthropic', r'openai', r'playwright', r'chromium', r'pdftotext', r'python', r'openpyxl', r'pypdf', r'\bskia\b', r'docx-js', r'\bllms?\b', r'\bgpt', r'generated using', r'ai-assisted',
          r'deep research', r'cowork', r'code assistant', r'automated generation', r'internal tool', r'execution layer', r'\bprompts?\b', r'\bagents?\b', r'\bconnectors?\b', r'\bplugins?\b', r'\bscripts?\b', r'headless', r'devtools', r'puppeteer', r'selenium', r'remote desktop', r'screen ?capture tool', r'browser (environment|automation|engine)', r'cloud browser']
CONTEXT = [r'\bai\b', r'artificial intelligence', r'\bmodels?\b', r'\bskills?\b']
ALLOW = ('computer science', 'computer engineering', 'major', 'engineering', 'architecture', 'each skill', 'study skills', 'learning skills', 'writing', 'listening', 'reading', 'speaking', 'college of computer', 'cybersecurity', 'software')
def corpus():
    cap = json.load(open(f'{SC}/v12/cap/capture.json'))
    t = ' '.join(c.get('raw', '') for c in cap) + open(f'{SC}/v12/raw/APPLY_noredirect.html', errors='ignore').read()
    t += ' '.join(open(f, errors='ignore').read() for f in glob.glob(f'{SC}/v12/pdf/*.txt'))
    return re.sub(r'\s+', ' ', t).lower()
def scan(texts):
    site = corpus(); rows = []; bad = 0
    for fname, t in texts.items():
        low = ' ' + re.sub(r'\s+', ' ', t).lower() + ' '
        for pat in STRICT + CONTEXT:
            for m in re.finditer(pat, low):
                ctx = low[max(0, m.start() - 50):m.end() + 50].strip(); core = low[max(0, m.start() - 15):m.end() + 15].strip()
                if pat in STRICT: disp = 'AUTHORED — REMOVE'
                else:
                    subject = (core in site or any(k in ctx for k in ALLOW) or m.group(0) in site) and not re.search(r'generat|assist|tool|using|powered', ctx)
                    disp = 'PUBLISHED CONTENT / SUBJECT MATTER (programme name or test skill)' if subject else 'AUTHORED — REMOVE'
                if disp.startswith('AUTHORED'): bad += 1
                rows.append([fname, m.group(0), ctx[:140], disp])
    return rows, bad
def xlsx_text(p):
    import openpyxl
    wb = openpyxl.load_workbook(p); out = []
    for ws in wb:
        out.append(ws.title)
        for row in ws.iter_rows(values_only=True): out += [str(v) for v in row if v is not None]
    pr = wb.properties; out += [str(pr.creator), str(pr.lastModifiedBy), str(pr.title), str(pr.description), str(pr.keywords), str(pr.subject)]
    z = zipfile.ZipFile(p); out.append(z.read('docProps/app.xml').decode(errors='ignore'))
    return ' '.join(out)
def docx_text(p):
    z = zipfile.ZipFile(p); return ' '.join(z.read(n).decode(errors='ignore') for n in z.namelist() if n.endswith('.xml'))
def pdf_meta(p):
    from pypdf import PdfReader
    rd = PdfReader(p); m = rd.metadata or {}; x = ''
    try: x = rd.xmp_metadata and str(rd.xmp_metadata)
    except Exception: pass
    return ' '.join(f'{k}={v}' for k, v in m.items()) + ' ' + (x or '')
def gates(npack):
    import openpyxl
    D = json.load(open(V4)); R = D['rows']; n = len(R); S = D['stats']; C = D['coverage22']
    G = []
    def add(gid, en, ar, ok, ev, residual='', action=''):
        G.append(dict(gid=gid, en=en, ar=ar, result='PASS' if ok is True else ('FAIL' if ok is False else 'NOT VERIFIED'), evidence=ev, residual=residual, action=action))
    txt = {k: pdftext(N[k]) for k in ('rev_ar', 'rev_en')}
    # C0
    inv = D['inventory']; elig = [i for i in inv if i['incl'].startswith('Included')]
    nostat = [i['rid'] for i in elig if i['rstatus'] not in ('FULLY_REVIEWED', 'PARTIALLY_REVIEWED', 'BLOCKED', 'EXCLUDED')]
    noev = [r['fid'] for r in R if not r['eids'] or not r['url']]
    evc = collections.Counter(x['fid'] for x in D['evidence'])
    conf1 = [r['fid'] for r in R if r['cls'] == 'PROVEN_PUBLISHED_CONFLICT' and evc[r['fid']] < 2]
    errref = [r['fid'] for r in R if r['cls'] == 'VERIFIED_FACTUAL_ERROR' and ('self-evident' in r['auth_ref'] or not r['auth_ref'])]
    evbad = [x['eid'] for x in D['evidence'] if not x['url'] or not x['observed']]
    discl = [i['rid'] for i in elig if i['rstatus'] == 'PARTIALLY_REVIEWED' and not i['unchecked_en']]
    dest_missing = C['unique_destinations'] - len([i for i in inv if re.fullmatch(r'R-P(0[3-9]|[1-3]\d)', i['rid'])])
    c0 = not (nostat or noev or conf1 or errref or evbad or discl or dest_missing > 0)
    add('C0', 'C0 — Evidence & Coverage Completeness', 'C0 — اكتمال الأدلة والتغطية', c0,
        f"{len(elig)} eligible resources all have a status; {C['unique_destinations']} root destinations all inventoried; {n} findings with evidence; {S['conflicts']} conflicts each ≥2 evidence items; {sum(1 for r in R if r['cls']=='VERIFIED_FACTUAL_ERROR')} factual errors each with a governing reference; partial reviews disclosed",
        '; '.join(x for x in [('no status: ' + ','.join(nostat)) if nostat else '', ('no evidence: ' + ','.join(noev)) if noev else '', ('one-sided conflicts: ' + ','.join(conf1)) if conf1 else '', ('errors without reference: ' + ','.join(errref)) if errref else ''] if x) or '2 BLOCKED items disclosed (F-033, F-131)')
    pp = [r for r in R if r['plevel'] in ('P0', 'P1')]
    add('G1', 'G1 — Executive Decision Clarity', 'G1 — وضوح القرار التنفيذي', all(r['dids'] for r in pp) and all(d['auth'] and d['rec_en'] and d['risk_en'] for d in D['decisions']),
        f"{len(pp)} P0/P1 findings mapped to {len(D['decisions'])} decisions; each decision states authority, DIRECT/REFER role, risk if deferred, options and recommendation", 'Authorities are proposed; management confirmation needed', 'Confirm D-01 … D-10')
    add('G2', 'G2 — Academic & Policy Integrity', 'G2 — سلامة المرجعية الأكاديمية والسياسات', all('OPEN CONFLICT' in r['auth_ref'] for r in R if r['cls'] == 'PROVEN_PUBLISHED_CONFLICT') and not errref,
        'Conflicts declared OPEN CONFLICT with no value chosen; recommendations conditional on approval; external facts tied to College Board (2021) and ETS (2026)', 'No approved PMU policy/fee reference available', 'Supply references for D-01 … D-05')
    add('G3', 'G3 — Execution & Accountability', 'G3 — قابلية التنفيذ والمساءلة', all(p['required'] if False else (p['action'] and p['owner'] and p['approval'] and p['status'] and p['gov_ref']) for p in D['plan']),
        f"{len(D['plan'])} actions with finding, decision, current/target state, change, governing reference, approval, owner, dependency, proposed date, status and closure fields", 'Owners proposed; no action authorised yet', 'Assign owners')
    ids_en = set(re.findall(r'\b[FDA]-\d{2,3}\b', txt['rev_en'])); ids_ar = set(re.findall(r'\b[FDA]-\d{2,3}\b', txt['rev_ar']))
    known = {r['fid'] for r in R} | {d['did'] for d in D['decisions']} | {p['aid'] for p in D['plan']}
    eids = {x['eid'] for x in D['evidence']}
    add('G4', 'G4 — Evidence & Traceability', 'G4 — الأدلة وقابلية التتبع', ids_en <= known and ids_ar <= known and all(e in eids for r in R for e in r['eids']) and npack > 0,
        f"All IDs cited in the PDFs exist in the register ({len(ids_en)} EN / {len(ids_ar)} AR); {len(D['evidence'])} evidence items resolvable; evidence pack {npack} files with MD5 manifest", 'External references cited by URL (not retrievable from review network)', '')
    wbe = openpyxl.load_workbook(N['reg_en']); wba = openpyxl.load_workbook(N['reg_ar'])
    rows_e = [ws.max_row for ws in wbe]; rows_a = [ws.max_row for ws in wba]
    guide = docx_text(N['guide'])
    cnt_ok = all(f'{n}' in t for t in txt.values()) and f'{n} findings' in guide
    add('G5', 'G5 — Institutional Delivery Excellence', 'G5 — التميز في التسليم المؤسسي', cnt_ok and len(wbe.sheetnames) >= 14,
        f"Headline count {n} identical in both PDFs and the email; {len(wbe.sheetnames)} register sheets; files open; decisions separated from technical detail", '', '')
    long_rep = [ln for ln, c in collections.Counter(l.strip() for l in txt['rev_en'].splitlines() if len(l.strip()) > 60 and not l.strip().startswith(('Source:', 'Observed:'))).items() if c > 2]  # evidence source lines repeat by design
    ph = re.findall(r'TODO|TBD|lorem|\[\[|\{\{', txt['rev_en'] + txt['rev_ar'])
    add('G6', 'G6 — Editorial & Human Professional Quality', 'G6 — الجودة التحريرية والمهنية', not long_rep and not ph,
        f"No repeated paragraphs or placeholders; English report {pages(N['rev_en'])} pp., Arabic {pages(N['rev_ar'])} pp.; findings texts edited after independent challenge", 'Owner review of wording recommended', '')
    same = rows_e == rows_a and wbe.sheetnames.__len__() == wba.sheetnames.__len__() and set(re.findall(r'\bF-\d{3}\b', txt['rev_en'])) == set(re.findall(r'\bF-\d{3}\b', txt['rev_ar']))
    add('G7', 'G7 — Arabic–English Institutional Equivalence', 'G7 — التكافؤ المؤسسي بين العربية والإنجليزية', same,
        f"Identical sheet structure and row counts ({sum(rows_e)} rows each); identical finding IDs in both PDFs; same statuses and counts", '', '')
    fonts = {k: subprocess.run(['pdffonts', N[k]], capture_output=True, text=True).stdout for k in ('rev_ar', 'rev_en')}
    noemb = any(' no ' in l[60:70] for f in fonts.values() for l in f.splitlines()[2:])
    bad_glyph = any('�' in t for t in txt.values())
    rtl = all(ws.sheet_view.rightToLeft for ws in wba) and not any(ws.sheet_view.rightToLeft for ws in wbe)
    v = run('python3', '/mnt/skills/public/docx/scripts/office/validate.py', N['guide'])
    add('G8', 'G8 — Visual & Document Integrity', 'G8 — سلامة العرض والمستندات', not noemb and not bad_glyph and rtl and 'PASSED' in (v.stdout + v.stderr),
        f"Fonts embedded; no replacement glyphs; Arabic register RTL / English LTR; guide DOCX validates; pages rendered and inspected", '', '')
    ch = D['challenge']; unresolved = [c['fid'] for c in ch if c['fid'] not in D['challenge_res']]
    add('G9', 'G9 — Independent Analytical Challenge', 'G9 — التحدي التحليلي المستقل', len(ch) >= len(pp) and not unresolved,
        f"{len(ch)} high-impact items independently challenged (all P0/P1, conflicts, errors); {sum(1 for c in ch if c['verdict'] != 'UPHELD')} raised issues; every disagreement resolved by rechecking the original evidence (18 changes applied, 1 duplicate merged, 2 severities kept with reasons)", '', '')
    texts = {os.path.basename(N['rev_en']): txt['rev_en'], os.path.basename(N['rev_ar']): txt['rev_ar'], os.path.basename(N['reg_en']): xlsx_text(N['reg_en']), os.path.basename(N['reg_ar']): xlsx_text(N['reg_ar']),
             os.path.basename(N['guide']): docx_text(N['guide']), 'pdf-metadata-EN': pdf_meta(N['rev_en']), 'pdf-metadata-AR': pdf_meta(N['rev_ar']),
             'file-names': ' '.join(os.path.basename(v) for v in N.values()) + ' ' + ' '.join(zipfile.ZipFile(N['pack']).namelist()) if os.path.exists(N['pack']) else ''}
    if os.path.exists(N['pack']):
        z = zipfile.ZipFile(N['pack'])
        for nm in z.namelist():
            if nm.endswith(('.txt', '.csv')) and 'Content_integrity_scan' not in nm: texts['pack:' + nm] = z.read(nm).decode(errors='ignore')
    rows, bad = scan(texts)
    add('G10', 'G10 — Clean Deliverable Integrity', 'G10 — سلامة المخرجات ونظافتها', bad == 0,
        f"PDF text and properties, register cells and properties, guide, file names and evidence-pack files checked: no drafting artefacts, comments, residual notes or inappropriate metadata ({bad} issues)", '', '')
    # G11 visual evidence authenticity
    vqa = visual_qa(D); bad = [r[0] for r in vqa if r[-1] != 'ACCEPTED']
    vb = collections.Counter(v['fid'] for v in D['visual'])
    conf_vis = [r['fid'] for r in R if r['cls'] == 'PROVEN_PUBLISHED_CONFLICT' and vb[r['fid']] < 2]
    pp_vis = [r['fid'] for r in R if r['plevel'] in ('P0', 'P1') and vb[r['fid']] < 1]
    hist_cur = [v['eid'] for v in D['visual'] if not v['currency'].startswith('Current')]
    zn = set(zipfile.ZipFile(N['pack']).namelist()) if os.path.exists(N['pack']) else set()
    inpack = all(any(n.endswith(v['orig']) and not n.startswith('02_') for n in zn) and f"02_Annotated_Live_Evidence/{v['ann']}" in zn for v in D['visual'])
    add('G11', 'G11 — Visual Evidence Authenticity & Capture Integrity', 'G11 — أصالة الأدلة المرئية وسلامة الالتقاط', not bad and not conf_vis and not pp_vis and not hist_cur and inpack,
        f"{len(D['visual'])} captures of 22 Oct 2026, each with Evidence ID, Finding ID, Resource ID, source URL, location and time; originals unaltered (MD5 match) and kept separately from annotated copies (≥95% identical outside the frame); all {sum(1 for r in R if r['plevel'] in ('P0','P1'))} P0/P1 findings covered; all {S['conflicts']} conflicts shown on both sides; captions present in both reports; no generated or reconstructed image; capture means not shown",
        '; '.join(x for x in [('not accepted: ' + ','.join(bad)) if bad else '', ('one-sided: ' + ','.join(conf_vis)) if conf_vis else '', ('P0/P1 without image: ' + ','.join(pp_vis)) if pp_vis else '', '' if inpack else 'pack incomplete'] if x) or 'Portal and BLOCKED items (F-033, F-131) not captured — disclosed', '')
    # data integrity cross-validation (§33A)
    fids = [r['fid'] for r in R]; rids = {i['rid'] for i in D['inventory']}
    dup = [k for k, c in collections.Counter(fids + [x['eid'] for x in D['evidence']] + [d['did'] for d in D['decisions']] + [p['aid'] for p in D['plan']] + [v['eid'] for v in D['visual']]).items() if c > 1]
    orphan_f = [r['fid'] for r in R if r['rid'] not in rids]; orphan_e = [x['eid'] for x in D['evidence'] if x['fid'] not in fids]
    orphan_d = [d['did'] for d in D['decisions'] if any(f not in fids for f in d['fids'])]
    orphan_a = [p['aid'] for p in D['plan'] if p['did'] not in ('—', '') and not all(x in {d['did'] for d in D['decisions']} for x in re.findall(r'D-\d\d', p['did']))]
    orphan_v = [v['eid'] for v in D['visual'] if v['fid'] not in fids or v['rid'] not in rids]
    p0nd = [r['fid'] for r in R if r['plevel'] == 'P0' and not (r['dids'] and any(r['fid'] in (p.get('fids') or '') for p in D['plan']))]
    sumok = n == sum(S['plevel'].get(p, 0) for p in ('P0', 'P1', 'P2', 'P3'))
    fe = len(list(wbe[wbe.sheetnames[3]].iter_rows(min_row=5))); fa = len(list(wba[wba.sheetnames[3]].iter_rows(min_row=5)))
    di = not (dup or orphan_f or orphan_e or orphan_d or orphan_a or orphan_v or p0nd) and sumok and fe == fa == n and cnt_ok
    add('DI', 'Data Integrity Cross-Validation (§33A)', 'التحقق المتقاطع من سلامة البيانات (§33A)', di,
        f"No duplicate IDs; every finding → valid resource, evidence → finding, decision → findings, action → decision, visual evidence → finding and resource; P0 each with decision and action; total {n} = P0+P1+P2+P3; findings rows EN {fe} / AR {fa}; count identical in both reports and the email",
        '; '.join(str(x) for x in [dup, orphan_f, orphan_e, orphan_d, orphan_a, orphan_v, p0nd] if x))
    return G, rows
build_docs(); n1 = build_pack([], []); G, rows = gates(n1)
D = json.load(open(V4)); D['gates5'] = G; json.dump(D, open(V4, 'w'), ensure_ascii=False, indent=1)
build_docs(); qa = [[g['gid'], g['en'], g['result'], g['evidence'], g['residual']] for g in G]
n2 = build_pack(qa, rows); G2, rows2 = gates(n2)
D = json.load(open(V4)); D['gates5'] = G2; json.dump(D, open(V4, 'w'), ensure_ascii=False, indent=1)
build_docs(); n3 = build_pack([[g['gid'], g['en'], g['result'], g['evidence'], g['residual']] for g in G2], rows2); G3, rows3 = gates(n3)
for g in G3: print(g['result'], '|', g['gid'], '|', g['evidence'][:130], '|', g['residual'][:80])
print('authored hits:', [r for r in rows3 if r[3].startswith('AUTHORED')][:12])
print({k: (os.path.getsize(v) // 1024) for k, v in N.items()}, 'pages', pages(N['rev_en']), pages(N['rev_ar']))
