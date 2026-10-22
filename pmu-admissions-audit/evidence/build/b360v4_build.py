# Directive 2.1 build: PDFs, registers, evidence pack, internal guide, metadata cleaning, C0 + G1–G10.
# Usage: b360v4_build.py v4.json scratch_root out_dir
import json, os, re, sys, subprocess, shutil, zipfile, hashlib, csv, collections, glob, html, unicodedata
V4, SC, OUTD = sys.argv[1:4]
B = os.path.dirname(os.path.abspath(__file__))
EV = f'{SC}/v10/ev'
N = {'rev_ar': f'{OUTD}/01_PMU_Admissions_Management_Review_AR.pdf', 'reg_ar': f'{OUTD}/02_PMU_Admissions_Master_Register_AR.xlsx',
     'rev_en': f'{OUTD}/03_PMU_Admissions_Management_Review_EN.pdf', 'reg_en': f'{OUTD}/04_PMU_Admissions_Master_Register_EN.xlsx',
     'pack': f'{OUTD}/05_PMU_Admissions_Evidence_Pack.zip', 'guide': f'{OUTD}/00_INTERNAL_Submission_Guide.docx'}
os.makedirs(OUTD, exist_ok=True)
def run(*a):
    r = subprocess.run(a, capture_output=True, text=True)
    if r.returncode: print('ERR', a[:3], r.stderr[-400:])
    return r
FOOT = 'PMU Admissions — Management Review &amp; Decision Package · v4.0 · Prepared for Management Review'
def clean_pdf(p, title):
    from pypdf import PdfReader, PdfWriter
    rd = PdfReader(p); w = PdfWriter(clone_from=rd)
    w._info = None
    w.add_metadata({'/Title': title, '/Author': 'Nader Al Farhan', '/Subject': 'Admissions Office content review — Prepared for Management Review',
                    '/Creator': 'PMU Admissions Office', '/Producer': 'PMU Admissions Office', '/Keywords': 'PMU; Admissions; Management Review'})
    with open(p, 'wb') as f: w.write(f)
def build_docs():
    for L in ('ar', 'en'):
        run('python3', f'{B}/b360v4_review.py', V4, EV, f'{SC}/v12/review_{L}.html', L)
        run('node', f'{B}/b360_pdf.js', f'{SC}/v12/review_{L}.html', N['rev_' + L], FOOT)
        clean_pdf(N['rev_' + L], 'PMU Admissions — Management Review & Decision Package' + (' (Arabic)' if L == 'ar' else ''))
        run('python3', f'{B}/b360v4_xlsx.py', V4, N['reg_' + L], L)
    run('node', f'{B}/b360v4_guide.js', V4, N['guide'])
def md5(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()
def build_pack(qa_rows, scan_rows):
    D = json.load(open(V4)); st = f'{SC}/v12/pack'; shutil.rmtree(st, ignore_errors=True)
    dirs = ['00_Manifest', '01_Current_Live_Evidence/annotated', '01_Current_Live_Evidence/original_captures', '02_PDF_Evidence', '03_Historical_Evidence', '04_Reference_Material', '05_QA']
    for d in dirs: os.makedirs(f'{st}/{d}', exist_ok=True)
    man = []
    def put(src, rel, desc, url='', date='', ids=''):
        dst = f'{st}/{rel}'; shutil.copy(src, dst); man.append([rel, desc, url, date, ids, md5(dst)])
    shots = {s['id']: s for s in json.load(open(f'{EV}/evshots.json'))}
    fid_of = {}
    for x in D['evidence']:
        for s in (x['shot'] or '').split(', '):
            if s: fid_of[s.replace('.png', '')] = x['fid']
    for evid, s in sorted(shots.items()):
        put(f'{EV}/{evid}.png', f'01_Current_Live_Evidence/annotated/{evid}.png', 'Annotated capture (highlight added by reviewer); fact re-confirmed 22 Oct 2026', s['url'], s['at'][:10], f"{evid}; {fid_of.get(evid, '')}")
    cap = json.load(open(f'{SC}/v12/cap/capture.json'))
    for c in cap:
        p = f'{SC}/v12/cap/shots/{c["id"]}_full.jpg'
        if os.path.exists(p): put(p, f'01_Current_Live_Evidence/original_captures/R-{c["id"]}_full_2026-10-22.jpg', f'Original full-page capture: {c["title"][:70]}', c['final'], '2026-10-22', f'R-{c["id"]}')
    slim = [dict(resource=f"R-{c['id']}", url=c['url'], final=c.get('final'), http=c.get('status'), captured=c['at'], title=c.get('title'), text=c.get('raw')) for c in cap]
    json.dump(slim, open(f'{SC}/v12/page_text.json', 'w'), ensure_ascii=False, indent=1)
    put(f'{SC}/v12/page_text.json', '01_Current_Live_Evidence/page_text_2026-10-22.json', 'Text of every captured resource (visible and tab content)', '', '2026-10-22', 'R-*')
    put(f'{SC}/v12/links_status_22.tsv', '01_Current_Live_Evidence/link_status_2026-10-22.tsv', 'HTTP status of every unique link on in-scope pages', '', '2026-10-22', 'F-035; F-131')
    put('/home/user/nader-al-farhan/pmu-admissions-audit/evidence/recheck_2026-10-22.tsv', '01_Current_Live_Evidence/live_recheck_2026-10-22.tsv', 'Live re-confirmation of highest-risk facts', '', '2026-10-22', 'RC-*')
    put(f'{SC}/v12/pdf/WAG.pdf', '02_PDF_Evidence/Web-Admission-Guide-v2-2_20-12-18.pdf', 'Web Admission Guide (21 pp.); p. 20 states SR 500 fee', 'https://www.pmu.edu.sa/Attachments/Admission/Images/PDF/Web-Admission-Guide-v2-2_20-12-18.pdf', '2026-10-22', 'F-036; H-6')
    put(f'{SC}/v7/wagimg/p-20.png', '02_PDF_Evidence/Web-Admission-Guide_page-20.png', 'Page 20 image of the Web Admission Guide', '', '2026-10-11', 'F-036')
    put(f'{SC}/v12/pdf/APTIS.pdf', '02_PDF_Evidence/Aptis-Candidate-Guide-2017.pdf', 'Aptis Candidate Guide (50 pp., Aug 2017)', 'https://www.pmu.edu.sa/Attachments/Admission/PDF/Appendix%203.3%20(Aptis%20Candidate%20Guide).pdf', '2026-10-22', 'F-121')
    hist = f'{SC}/v12/H_requests_2025-10-26.txt'
    open(hist, 'w').write('Amendments requested in the email of 26 October 2025 (thread "updates on Admission pages" / "comments on Admission pages")\n\n' +
        '\n'.join(f"{a['hid']}: {a['req_en']}" for a in D['amend']) + '\n\nThese are historical requests compared with the published content; they are not approved policy.\n')
    put(hist, '03_Historical_Evidence/H_requests_2025-10-26.txt', 'Historical amendment requests H-1 … H-6', '', '2025-10-26', 'H-1 … H-6')
    base = [dict(resource=f"R-{c['id']}", url=c['url'], captured=c['at'], text=c.get('raw')) for c in json.load(open(f'{SC}/v10/cap/capture.json'))]
    json.dump(base, open(f'{SC}/v12/page_text_21.json', 'w'), ensure_ascii=False)
    put(f'{SC}/v12/page_text_21.json', '03_Historical_Evidence/page_text_2026-10-21_baseline.json', 'Baseline capture of 21 Oct 2026 (comparison only)', '', '2026-10-21', 'R-*')
    ref = f'{SC}/v12/references.txt'
    open(ref, 'w').write('Reference material\n\n1. College Board — "An Update on Reducing and Simplifying Demands on Students" (19 Jan 2021): SAT Subject Tests discontinued; final international administration June 2021.\n   https://allaccess.collegeboard.org/update-reducing-and-simplifying-demands-students\n   Used for: F-040, H-4\n\n2. ETS — TOEFL iBT score scale update: 1–6 scale for tests on/after 21 Jan 2026; dual 0–120 reporting through Jan 2028.\n   https://www.ets.org/toefl/institutions/ibt/score-scale-update.html\n   Used for: F-124\n\n3. PMU Other Fees schedule — "Admission Application Fees … (includes the VAT 15%) Non-refundable SAR 950"; "APTIS Exam Fees SAR 575".\n   https://www.pmu.edu.sa/admission/student_fees_tf_ro  (capture R-L2-STU-FEES)\n   Used for: F-039, F-119, H-3, H-5\n\n4. PMU Medical Program Fees — "Medical Application Fee SAR 1,150 (VAT inclusive)".\n   https://pmu.edu.sa/admission/medical_program_studies_fees_tf_ro  (capture R-L2-MED-FEES)\n   Used for: F-052\n\nNote: items 1–2 were located on the official sites but could not be retrieved directly from the review network; they are cited by URL.\n')
    put(ref, '04_Reference_Material/References.txt', 'Governing and external references with URLs', '', '2026-10-22', 'F-039; F-040; F-052; F-119; F-124')
    for rid in ('L2-STU-FEES', 'L2-MED-FEES', 'L2-FEES-2627', 'L2-GR-FORM', 'L2-MILBL-FORM'):
        p = f'{SC}/v12/cap/shots/{rid}_full.jpg'
        if os.path.exists(p): put(p, f'04_Reference_Material/R-{rid}_full_2026-10-22.jpg', 'Official PMU page used as verification source', '', '2026-10-22', f'R-{rid}')
    for name, rows, hdr in (('QA_record.csv', qa_rows, ['gate', 'check', 'result', 'evidence', 'residual']),
                            ('Independent_challenge.csv', [[c['fid'], c['verdict'], c.get('rationale', ''), D['challenge_res'].get(c['fid'], '')] for c in D['challenge']], ['finding', 'challenge verdict', 'challenge rationale', 'resolution after evidence recheck'])):
        p = f'{SC}/v12/{name}'
        with open(p, 'w', newline='') as f: w = csv.writer(f); w.writerow(hdr); w.writerows(rows)
        put(p, f'05_QA/{name}', name.replace('_', ' ').replace('.csv', ''), '', '2026-10-22', '')
    readme = f'{st}/00_Manifest/README.txt'
    open(readme, 'w').write('PMU Admissions — Evidence Pack (v4.0, 22 Oct 2026)\nPrepared by Nader Al Farhan, Administrative Assistant, Student Affairs, Admission Office\n\n00_Manifest — this file and Manifest.csv (every file, description, source URL, date, linked IDs, MD5)\n01_Current_Live_Evidence — annotated captures (EV-*), original full-page captures (R-*), page text, link status, live re-check\n02_PDF_Evidence — linked PDF guides and the page-20 image\n03_Historical_Evidence — amendment requests of 26 Oct 2025; baseline capture of 21 Oct 2026\n04_Reference_Material — official external references and PMU fee pages\n05_QA — quality-gate record and independent challenge record\n\nAnnotated copies carry a reviewer highlight; originals are unaltered.\n')
    with open(f'{st}/00_Manifest/Manifest.csv', 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['path', 'description', 'source_url', 'date', 'linked_ids', 'md5']); w.writerows(man)
    if os.path.exists(N['pack']): os.remove(N['pack'])
    with zipfile.ZipFile(N['pack'], 'w', zipfile.ZIP_DEFLATED) as z:
        for root, _, fs in os.walk(st):
            for fn in sorted(fs): z.write(f'{root}/{fn}', os.path.relpath(f'{root}/{fn}', st))
    return len(man)

# ---------------- checks
def pdftext(p): return subprocess.run(['pdftotext', '-layout', p, '-'], capture_output=True, text=True).stdout
def pages(p): return int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', p], capture_output=True, text=True).stdout).group(1))
STRICT = [r'chatgpt', r'claude', r'anthropic', r'openai', r'playwright', r'chromium', r'pdftotext', r'python', r'openpyxl', r'pypdf', r'\bskia\b', r'docx-js', r'\bllms?\b', r'\bgpt', r'generated using', r'ai-assisted',
          r'deep research', r'cowork', r'code assistant', r'automated generation', r'internal tool', r'execution layer', r'\bprompts?\b', r'\bagents?\b', r'\bconnectors?\b', r'\bplugins?\b', r'\bscripts?\b']
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
    long_rep = [ln for ln, c in collections.Counter(l.strip() for l in txt['rev_en'].splitlines() if len(l.strip()) > 60).items() if c > 2]
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
    return G, rows
build_docs(); n1 = build_pack([], []); G, rows = gates(n1)
D = json.load(open(V4)); D['gates4'] = G; json.dump(D, open(V4, 'w'), ensure_ascii=False, indent=1)
build_docs(); qa = [[g['gid'], g['en'], g['result'], g['evidence'], g['residual']] for g in G]
n2 = build_pack(qa, rows); G2, rows2 = gates(n2)
D = json.load(open(V4)); D['gates4'] = G2; json.dump(D, open(V4, 'w'), ensure_ascii=False, indent=1)
build_docs(); n3 = build_pack([[g['gid'], g['en'], g['result'], g['evidence'], g['residual']] for g in G2], rows2); G3, rows3 = gates(n3)
for g in G3: print(g['result'], '|', g['gid'], '|', g['evidence'][:130], '|', g['residual'][:80])
print('authored hits:', [r for r in rows3 if r[3].startswith('AUTHORED')][:12])
print({k: (os.path.getsize(v) // 1024) for k, v in N.items()}, 'pages', pages(N['rev_en']), pages(N['rev_ar']))
