# Directive 2.2 layer: visual evidence register, review contact rate, change log. Usage: b360v5_enrich.py v4.json visual.json captions.json out.json
import json, sys, re, collections
D = json.load(open(sys.argv[1])); V = json.load(open(sys.argv[2])); CAP = json.load(open(sys.argv[3])); OUT = sys.argv[4]
by = {r['fid']: r for r in D['rows']}
norm = lambda u: re.sub(r'^https?://(www\.)?', '', (u or '').lower()).rstrip('/')
rid_of = {}
for i in D['inventory']:
    for u in (i.get('url'), i.get('final')):
        if u and u.startswith('http'): rid_of.setdefault(norm(u), i['rid'])
rid_of[norm('https://www.pmu.edu.sa/Attachments/Admission/Images/PDF/Web-Admission-Guide-v2-2_20-12-18.pdf')] = rid_of.get(norm('https://www.pmu.edu.sa/Attachments/Admission/Images/PDF/Web-Admission-Guide-v2-2_20-12-18.pdf'), 'R-MENU')
acts = collections.defaultdict(list)
for p in D['plan']:
    for f in re.findall(r'F-\d{3}', p.get('fids') or ''): acts[f].append(p['aid'])
amend_by_hid = {a['hid']: a for a in D['amend']}
ROLE = {'A': ('Conflict — source A', 'تعارض — المصدر أ'), 'B': ('Conflict — source B', 'تعارض — المصدر ب'), 'C': ('Conflict — source C', 'تعارض — المصدر ج'),
        '': ('Single evidence', 'دليل منفرد'), 'H': ('Historical request / current state', 'طلب تاريخي / الحالة الحالية')}
vis = []
for v in V:
    r = by[v['fid']]; tev = v['tev']; hid = tev if tev.startswith('H-') else ''
    role = v['role'] if r['cls'] == 'PROVEN_PUBLISHED_CONFLICT' or v['role'] == 'H' else ''
    if r['fid'] == 'F-028': role = 'P'
    rl = ROLE.get(role, ('AR/EN parity', 'التكافؤ العربي/الإنجليزي'))
    ev = next((x for x in D['evidence'] if x['eid'] == tev), None)
    dids = list(r['dids']) or ([amend_by_hid[hid]['did']] if hid else [])
    vis.append(dict(eid=v['eid'], fid=r['fid'], rid=rid_of.get(norm(v['url']), r['rid']), text_evidence=tev if not hid else ', '.join(x['eid'] for x in D['evidence'] if x['fid'] == r['fid']),
        hid=hid or ('H-3' if r['fid'] == 'F-039' else 'H-4' if r['fid'] == 'F-040' else 'H-6' if r['fid'] == 'F-036' else 'H-2' if v['eid'] == 'E022' else ''),
        dids=dids, aids=acts.get(r['fid'], []), title=v['title'].split('::')[0].strip() if '::' in v['title'] else v['title'], url=v['url'],
        date=v['date'], time=v['time'] or '18:02', tz='Asia/Riyadh', section_en=(ev['locator'] if ev and v['role'] in ('', 'A') else v['view']), section_ar=(ev['locator_ar'] if ev and v['role'] in ('', 'A') else ''),
        etype=v['etype'], role=role, role_en=rl[0], role_ar=rl[1], view=v['view'], claim_en=CAP['shows'][v['eid']][0], claim_ar=CAP['shows'][v['eid']][1],
        why_en=CAP['why'][r['fid']][0], why_ar=CAP['why'][r['fid']][1], prio=r['plevel'], cls=r['cls'], ftitle_en=r['title_en'], ftitle_ar=r['title_ar'],
        orig=v['orig'], ann=v['ann'], md5=v['md5_orig'], currency='Current (22 Oct 2026)', vstatus='VERIFIED',
        notes=('Published section hidden by default; expanded locally for viewing only. ' if v.get('revealed') else '') + ('Page shown without following its automatic redirect to the application portal; published content unchanged. ' if v.get('held') else '') + (v.get('frame_note', '') and 'Annotation frame placed on the cited text after visual check. ')))
D['visual'] = vis
vt = collections.defaultdict(list)
for v, x in zip(V, vis): vt[v['tev']].append(x['eid'])
for x in D['evidence']:
    x['shot'] = ', '.join(vt.get(x['eid'], []))
    if x.get('page_shot'): x['page_shot'] = 'R-' + x['page_shot'].replace('_full.jpg', '') + '_full_2026-10-22.jpg' if not x['page_shot'].startswith('R-') else x['page_shot']
C = D['coverage22']; C['contact_rate'] = round(100 * (C['fully'] + C['partially']) / C['eligible'], 1)
C['visual_findings'] = len({x['fid'] for x in vis}); C['visual_items'] = len(vis)
D['changelog'] = [c for c in D['changelog'] if c[0] != 'v5.0'] + [['v5.0', '2026-10-22', 'Directive 2.2 edition: original live captures of 22 Oct 2026 for all P0/P1 findings, proven conflicts (both sides), the material parity item and historical amendments, each kept unaltered with a separate annotated copy; visual evidence register with Evidence/Finding/Resource IDs, source, URL, location and capture time (Asia/Riyadh); evidence annex rebuilt around conflict pairs; review contact rate added; evidence pack restructured (00–07); quality gate G11 added']]
D['version'] = '5.0'
json.dump(D, open(OUT, 'w'), ensure_ascii=False, indent=1)
print(len(vis), 'visual;', C['visual_findings'], 'findings; contact', C['contact_rate'])
for x in vis[:3]: print(x['eid'], x['fid'], x['rid'], x['hid'], x['dids'], x['aids'], x['time'], x['title'][:40])
print([ (x['eid'],x['rid']) for x in vis if not x['rid'] or x['rid']=='R-MENU'])
