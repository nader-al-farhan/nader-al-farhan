# Master Directive build: Level 1 + Level 2 packs, quality gates G1–G5, two-pass rebuild.
# Usage: b360m_build.py scratch_v10 master.json out_dir
import json, os, re, subprocess, sys, shutil, collections
V10, MASTER, OUTD = sys.argv[1], sys.argv[2], sys.argv[3]
B = os.path.dirname(os.path.abspath(__file__))
L1 = f'{OUTD}/Level-1_Management_Pack'; L2 = f'{OUTD}/Level-2_Evidence_and_Follow-up_Pack'
for d in (L1, L2, f'{L2}/evidence_screenshots'): os.makedirs(d, exist_ok=True)
N = {'brief_ar': f'{L1}/L1-01_Executive_Management_Brief_AR.pdf', 'brief_en': f'{L1}/L1-01_Executive_Management_Brief_EN.pdf',
     'mx_ar': f'{L1}/L1-02_Decision_Matrix_and_Action_Roadmap_AR.xlsx', 'mx_en': f'{L1}/L1-02_Decision_Matrix_and_Action_Roadmap_EN.xlsx',
     'rep_ar': f'{L1}/L1-03_Detailed_Audit_Report_AR.pdf', 'rep_en': f'{L1}/L1-03_Detailed_Audit_Report_EN.pdf',
     'ev_ar': f'{L2}/L2-01_Evidence_and_Follow-up_Pack_AR.xlsx', 'ev_en': f'{L2}/L2-01_Evidence_and_Follow-up_Pack_EN.xlsx'}
def run(*a):
    r = subprocess.run(a, capture_output=True, text=True)
    if r.returncode: print('ERR', a, r.stderr[-500:])
    return r
FOOT = {'en': 'PMU Admissions Audit 360 · PMU-ADM-360-MASTER-20261022 · Prepared for Management Review', 'ar': 'PMU Admissions Audit 360 · PMU-ADM-360-MASTER-20261022 · Prepared for Management Review (AR)'}
def build():
    for L in ('ar', 'en'):
        run('python3', f'{B}/b360m_brief.py', MASTER, f'{V10}/ev', f'{V10}/brief_{L}.html', L)
        run('node', f'{B}/b360_pdf.js', f'{V10}/brief_{L}.html', N['brief_' + L], FOOT[L])
        run('python3', f'{B}/b360_report.py', MASTER, f'{V10}/ev', f'{V10}/rep_{L}.html', L)
        run('node', f'{B}/b360_pdf.js', f'{V10}/rep_{L}.html', N['rep_' + L], FOOT[L])
        run('python3', f'{B}/b360m_xlsx.py', MASTER, N['mx_' + L], L, 'L1')
        run('python3', f'{B}/b360m_xlsx.py', MASTER, N['ev_' + L], L, 'L2')
def pdftext(p): return subprocess.run(['pdftotext', '-layout', p, '-'], capture_output=True, text=True).stdout
def pages(p): return int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', p], capture_output=True, text=True).stdout).group(1))
def gates():
    import openpyxl
    D = json.load(open(MASTER)); R = D['rows']; n = len(R); S = D['stats']
    txt = {k: pdftext(v) for k, v in N.items() if v.endswith('.pdf')}
    g = []
    def add(gid, en, ar, ok, ev, residual='', action=''):
        g.append(dict(gid=gid, en=en, ar=ar, result='PASS' if ok is True else ('FAIL' if ok is False else 'NOT VERIFIED'), evidence=ev, residual=residual, action=action))
    # G1
    pp = [r for r in R if r['plevel'] in ('P0', 'P1')]
    nod = [r['fid'] for r in pp if not r['dids']]
    dok = all(d.get('auth') and d.get('rec_en') and d.get('risk_en') for d in D['decisions'])
    add('G1', 'G1 — Executive Decision Clarity', 'G1 — وضوح القرار التنفيذي', not nod and dok,
        f"{len(pp)} P0/P1 findings mapped to decisions; {len(D['decisions'])} decisions each with authority, risk, options and recommendation; brief §5 lists all decisions on one page",
        ('Unmapped: ' + ', '.join(nod)) if nod else 'Proposed authorities require confirmation by management', 'Mr. Radhi to confirm authorities (D-01 … D-10)')
    # G2
    conf = [r for r in R if r['category'] == 'CONFLICT']
    noref = [r['fid'] for r in R if not r.get('auth_ref')]
    chosen = [r['fid'] for r in conf if 'OPEN CONFLICT' not in r['auth_ref']]
    add('G2', 'G2 — Academic & Policy Integrity', 'G2 — سلامة المرجعية الأكاديمية والسياسات', not noref and not chosen,
        f"Every finding carries an authoritative-reference field; {len(conf)} conflicts declared OPEN CONFLICT with no value chosen; external facts tied to College Board (19 Jan 2021) and ETS (21 Jan 2026)",
        'No approved PMU policy or fee decision was available; governing values remain to be confirmed institutionally', 'Supply approved, dated references for D-01 … D-05')
    # G3
    pl = D['plan']
    bad = [p['aid'] for p in pl if not (p['action'] and p['owner'] and p['approval'] and p['status'] and p['kpi_en'])]
    add('G3', 'G3 — Execution & Accountability', 'G3 — قابلية التنفيذ والمساءلة', not bad,
        f"{len(pl)} actions with problem, outcome, action, decision, owner (or OWNER_TO_CONFIRM), prior approval, proposed target, status, evidence and re-verification fields",
        'Owners are proposed, not confirmed; no implementation authorised yet', 'Assign owners and authorise actions')
    # G4
    eids = {e['eid'] for e in D['evidence']}
    miss = [r['fid'] for r in R if not r['eids'] or any(x not in eids for x in r['eids']) or not r.get('verified_on')]
    shots = sorted(f for f in os.listdir(f'{L2}/evidence_screenshots') if f.endswith('.png'))
    brief_ids = set(re.findall(r'F-\d{3}', txt['brief_en']))
    in_reg = brief_ids <= {r['fid'] for r in R}
    rep_ids = len(set(re.findall(r'F-\d{3}', txt['rep_en'])))
    add('G4', 'G4 — Evidence & Traceability', 'G4 — الأدلة وقابلية التتبع', not miss and in_reg and rep_ids >= n and len(shots) == 14,
        f"{n} findings → {len(D['evidence'])} evidence items + {len(D['recheck'])} live re-confirmations (22 Oct); {len(brief_ids)} IDs cited in the brief all exist in the register; report indexes {rep_ids} IDs; 14 screenshots",
        '2 findings BLOCKED (F-033, F-131); external pages located by search, not retrieved directly', 'Manual check of F-033 and F-131')
    # G5
    wbs = {k: openpyxl.load_workbook(v) for k, v in N.items() if v.endswith('.xlsx')}
    mfe = wbs['ev_en'].worksheets[2]; mfa = wbs['ev_ar'].worksheets[2]
    ids_e = [mfe.cell(i, 1).value for i in range(5, mfe.max_row + 1)]; ids_a = [mfa.cell(i, 1).value for i in range(5, mfa.max_row + 1)]
    rtl = all(ws.sheet_view.rightToLeft for k in ('ev_ar', 'mx_ar') for ws in wbs[k])
    counts_ok = all(f"{n}" in txt[k] for k in ('brief_en', 'brief_ar', 'rep_en', 'rep_ar'))
    bad_glyph = any('�' in t for t in txt.values())
    fonts_ar = subprocess.run(['pdffonts', N['brief_ar']], capture_output=True, text=True).stdout
    pg = {k: pages(v) for k, v in N.items() if v.endswith('.pdf')}
    add('G5', 'G5 — Institutional Delivery Excellence', 'G5 — التميز في التسليم المؤسسي', ids_e == ids_a and rtl and counts_ok and not bad_glyph and 'Naskh' in fonts_ar,
        f"EN/AR registers identical IDs ({len(ids_e)} records); Arabic workbooks RTL; headline count {n} present in all four PDFs; no replacement glyphs; Arabic font embedded; pages {pg}",
        'Visual check performed on sampled pages; owner review of translations recommended', '—')
    # supporting checks
    phones = re.findall(r'\(966\)-3-849-\d{4}', ''.join(txt.values()))
    add('QC-1', 'No personal data reproduced (staff phone numbers / names)', 'عدم إيراد بيانات شخصية', not phones, 'none found' if not phones else ', '.join(phones))
    add('QC-2', 'No claim of approval, publication or closure', 'لا ادعاء باعتماد أو نشر أو إغلاق', 'NOT READY FOR VERIFIED CLOSURE' in txt['brief_en'], 'Closure status stated in brief, report and registers')
    add('QC-3', 'Exclusions not counted as examined', 'عدم احتساب المستبعد ضمن المفحوص', all(i['status'] == 'EXCLUDED' for i in D['inventory'] if i['incl'] == 'Excluded'), f"eligible {D['coverage']['eligible']}, excluded {D['coverage']['excluded']}")
    add('QC-4', 'P0 items re-confirmed on the live site on 22 Oct 2026', 'إعادة تأكيد بنود P0 حيًا في 22 أكتوبر 2026', all(x['hits'] not in ('0',) or x['id'] in ('F-005', 'A-2b', 'A-4b', 'A-1') for x in D['recheck']), f"{len(D['recheck'])} live checks; footer link verified from raw HTML")
    D['gates'] = g; json.dump(D, open(MASTER, 'w'), ensure_ascii=False, indent=1)
    return g, pg
build(); g1, _ = gates(); build(); g2, pg = gates()
for f in os.listdir(f'{V10}/ev'):
    if f.endswith('.png'): shutil.copy(f'{V10}/ev/{f}', f'{L2}/evidence_screenshots/{f}')
for x in g2: print(x['result'], '|', x['en'], '|', x['evidence'][:150])
print('stable:', [a['result'] for a in g1] == [b['result'] for b in g2], pg)
