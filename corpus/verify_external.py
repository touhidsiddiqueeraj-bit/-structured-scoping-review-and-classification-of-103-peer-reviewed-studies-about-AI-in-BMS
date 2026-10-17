#!/usr/bin/env python3
"""Verify external (non-corpus) citations against Crossref.
These are references used for positioning/standards discussion that are NOT
part of the 103-study classified subset or the 799-record eligible corpus,
so they live in a separate file to keep the dataset counts clean."""
import json, subprocess, time

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

EXTERNAL = [
    '10.1007/s44163-025-00721-y',  # Prasanna et al. 2026, Discover Artificial Intelligence (positioning)
    '10.1109/tec.2025.3548400',    # GPT-4 distilled-lifelong-learning SOH letter, IEEE TEC 2025 (LLM prior art)
]

out = []
for doi in EXTERNAL:
    p = subprocess.run(['curl', '-s', '--max-time', '30',
                        f'https://api.crossref.org/works/{doi}'],
                       capture_output=True, text=True)
    m = json.loads(p.stdout)['message']
    rec = {
        'doi': doi,
        'title_cr': (m.get('title') or [''])[0],
        'journal': (m.get('container-title') or [''])[0],
        'year': (m.get('issued', {}).get('date-parts') or [[None]])[0][0],
        'volume': m.get('volume', ''), 'issue': m.get('issue', ''),
        'page': m.get('page', ''), 'article_number': m.get('article-number', ''),
        'authors': author_str(m.get('author', [])),
        'external': True,
    }
    out.append(rec)
    print('verified', doi, '->', rec['journal'], rec['year'])
    time.sleep(0.4)
json.dump(out, open('/home/touhid/Documents/reviewpaper/corpus/external_verified.json', 'w'), indent=1)
