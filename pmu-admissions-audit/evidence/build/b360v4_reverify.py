# Re-verify every finding's verbatim text against a fresh capture (+ raw HTML + PDF text).
# Usage: b360v4_reverify.py master.json capdir rawdir pdfdir bundle.js out.json
import json, re, sys, glob, html, unicodedata
M, CAP, RAW, PDF, BUNDLE, OUT = sys.argv[1:7]
D = json.load(open(M)); C = json.load(open(f'{CAP}/capture.json'))
def n(s):
    s = html.unescape(unicodedata.normalize('NFKC', s)).replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"').replace('–', '-').replace('—', '-')
    s = re.sub(r'[/\t|*]', ' ', s); return re.sub(r'\s+', ' ', s).strip().lower()
corp = ' '.join(c.get('raw', '') + ' ' + c.get('title', '') + ' ' + ' '.join(l['t'] + ' ' + l['h'] for l in c.get('links', [])) for c in C)
for f in glob.glob(f'{RAW}/*.html'): corp += ' ' + open(f, errors='ignore').read()
for f in glob.glob(f'{PDF}/*.txt'): corp += ' ' + open(f, errors='ignore').read()
corp += ' ' + open(BUNDLE, errors='ignore').read()
ALL = n(corp)
NP = lambda x: re.sub(r'\s+', ' ', re.sub(r'\([^)]*\)', ' ', x)).strip()
ALLNP = NP(ALL)
res = {}
for r in D['rows']:
    t = r['current_text']
    t = re.sub(r'\[[^\]]*\]', '|', t); t = re.sub(r'\([^)]*(فحص|عرض)[^)]*\)', '|', t)
    t = re.sub(r'(?:^|\|)\s*[A-Za-z/ ]{2,25}:\s*"', '|', t)       # strip 'SAT: "' style labels
    frags = [f.strip(' "\'.:;،') for f in re.split(r'…|\||;|\.\.\.|→|other pages:|College of Medicine:', t)]
    frags = [re.sub(r'\s—.*$', '', f).strip() for f in frags]
    frags = [f for f in frags if len(f) >= 8]
    hit = [f for f in frags if n(f) in ALL or (NP(n(f)) and NP(n(f)) in ALLNP)]
    st = 'MATCH' if frags and len(hit) == len(frags) else ('PARTIAL' if hit else ('NO_TEXT' if not frags else 'NOT_FOUND'))
    res[r['fid']] = dict(status=st, frags=len(frags), hits=len(hit), missing=[f[:80] for f in frags if f not in hit])
json.dump(res, open(OUT, 'w'), ensure_ascii=False, indent=1)
import collections; print(collections.Counter(v['status'] for v in res.values()))
for k, v in res.items():
    if v['status'] != 'MATCH': print(k, v['status'], v['missing'][:2])
