#!/usr/bin/env python3
"""Add cross-cutting round-out papers, then verify every final DOI against CrossRef,
saving full metadata as the verification audit trail."""
import csv, json, subprocess, time, sys

SEL = '/home/touhid/Documents/reviewpaper/corpus/final_papers.json'
POOL = '/home/touhid/Documents/reviewpaper/corpus/pool.csv'
VER = '/home/touhid/Documents/reviewpaper/corpus/verified.json'

ADD = {
    '10.1016/j.ress.2022.109046': ('Cross-cutting', 'XAI/interpretability'),
    '10.1016/j.ensm.2023.02.035': ('Cross-cutting', 'Cloud BMS'),
    '10.1016/j.est.2022.106295': ('Cross-cutting', 'Second-life batteries'),
    '10.1016/j.eswa.2023.120444': ('Cross-cutting', 'Digital twins'),
    '10.1016/j.est.2024.113502': ('Cross-cutting', 'Graph networks'),
    '10.1016/j.rser.2023.113807': ('Cross-cutting', 'Physics-informed'),
    '10.1109/tte.2025.3533540': ('Cross-cutting', 'Transfer learning'),
    '10.1039/d2dd00067a': ('Cross-cutting', 'Uncertainty quantification'),
    '10.1002/aenm.202503067': ('Cross-cutting', 'XAI/interpretability'),
}

sel = json.load(open(SEL))
have = {r['doi'] for r in sel}
pool_rows = {r['doi'].lower(): r for r in csv.DictReader(open(POOL))}
for doi, (area, tag) in ADD.items():
    if doi in have:
        continue
    r = pool_rows.get(doi)
    if not r:
        print(f'NOT IN POOL: {doi}')
        continue
    sel.append({'doi': doi, 'title': r['title'], 'journal': r['journal'],
                'year': int(r['year']), 'cites': int(r['cites']),
                'areas': r['areas'], 'area': area, 'tag': tag})
print('total selected:', len(sel))

# --- Verify every DOI against CrossRef; pull full reference metadata ---
def author_str(authors):
    if not authors:
        return ''
    parts = []
    for a in authors[:6]:
        fam = a.get('family', '')
        giv = a.get('given', '')
        initials = ' '.join(g[0] + '.' for g in giv.replace('-', ' ').split() if g)
        parts.append(f'{fam}, {initials}'.strip())
    s = '; '.join(parts)
    if len(authors) > 6:
        s += '; et al.'
    return s

verified, failures = [], []
for i, r in enumerate(sel, 1):
    doi = r['doi']
    ok = False
    for attempt in range(3):
        p = subprocess.run(['curl', '-s', '--max-time', '30',
                            f'https://api.crossref.org/works/{doi}'],
                           capture_output=True, text=True)
        try:
            m = json.loads(p.stdout)['message']
        except Exception:
            time.sleep(2)
            continue
        title_cr = (m.get('title') or [''])[0]
        jr = (m.get('container-title') or [''])[0] or r['journal']
        year = (m.get('issued', {}).get('date-parts') or [[None]])[0][0] or r['year']
        vol = m.get('volume', '')
        issue = m.get('issue', '')
        page = m.get('page', '')
        art = m.get('article-number', '')
        rec = {
            'doi': doi, 'title_cr': title_cr, 'title_pool': r['title'],
            'journal': jr, 'year': year, 'volume': vol, 'issue': issue,
            'page': page, 'article_number': art,
            'authors': author_str(m.get('author', [])),
            'n_authors': len(m.get('author', [])),
            'area': r['area'], 'tag': r.get('tag', ''),
            'cites': r.get('cites', m.get('is-referenced-by-count', 0)),
        }
        # title agreement check (first 30 chars, casefold)
        if title_cr and title_cr[:30].lower().replace('&amp;', '&') == r['title'][:30].lower().replace('&amp;', '&'):
            rec['match'] = True
        else:
            rec['match'] = False
            print(f"MISMATCH {doi}\n  pool: {r['title'][:70]}\n  cr:   {title_cr[:70]}")
        verified.append(rec)
        ok = True
        break
    if not ok:
        failures.append(doi)
        print(f'FAILED {doi}')
    if i % 20 == 0:
        print(f'  ...{i}/{len(sel)} verified')
    time.sleep(0.4)

json.dump(verified, open(VER, 'w'), indent=1)
print(f'verified: {len(verified)}, failures: {len(failures)}')
if failures:
    print('FAILURES:', failures)
