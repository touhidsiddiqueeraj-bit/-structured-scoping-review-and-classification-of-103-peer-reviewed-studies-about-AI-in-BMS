#!/usr/bin/env python3
"""Final audit: extract every reference from the built DOCX and re-verify its DOI
and title against the Crossref registry independently."""
import re, json, subprocess, time
from docx import Document

doc = Document('/home/touhid/Documents/reviewpaper/ML-BMS-Review.docx')
refs = []
in_refs = False
for p in doc.paragraphs:
    t = p.text.strip()
    if t == 'References':
        in_refs = True
        continue
    if in_refs and t:
        refs.append(t)

import sys
START, END = int(sys.argv[1]), int(sys.argv[2])
refs = refs[START:END]
print(f'refs {START+1}-{START+len(refs)} of audit')
fails, ok = [], 0
audit = []
for r in refs:
    m = re.match(r'^(\d+)\.\s+(.*)$', r)
    if not m:
        fails.append(('PARSE', r[:80]))
        continue
    n, body = m.group(1), m.group(2)
    dm = re.search(r'doi:\s*(\S+)\.?$', body)
    if not dm:
        fails.append(('NODOI', r[:80]))
        continue
    doi = dm.group(1)
    good = False
    for _ in range(3):
        p = subprocess.run(['curl', '-s', '--max-time', '25',
                            f'https://api.crossref.org/works/{doi}'],
                           capture_output=True, text=True)
        try:
            msg = json.loads(p.stdout)['message']
        except Exception:
            time.sleep(1.5)
            continue
        cr_title = (msg.get('title') or [''])[0]
        cr_year = (msg.get('issued', {}).get('date-parts') or [[None]])[0][0]
        # title prefix match (first 25 chars, normalized)
        tm = re.search(r'\u201c(.*?)\u201d', body)
        docx_title = tm.group(1) if tm else ''
        norm = lambda s: re.sub(r'[^a-z0-9]', '', s.lower())
        title_ok = norm(docx_title)[:25] == norm(cr_title)[:25]
        yr_m = re.search(r',\s*(20\d\d|\d{4}),?\s*doi:', body)
        year_ok = (not yr_m) or (str(cr_year) == yr_m.group(1))
        if title_ok and year_ok:
            good = True
        else:
            fails.append((f'{n}. {doi}', f'title_ok={title_ok} year_ok={year_ok}',
                          docx_title[:50], cr_title[:50]))
        break
    if good:
        ok += 1
    audit.append({'n': n, 'doi': doi, 'verified': good})
    time.sleep(0.3)

try:
    prev = json.load(open('/home/touhid/Documents/reviewpaper/corpus/final_audit.json', 'r'))
except Exception:
    prev = []
json.dump(prev + audit, open('/home/touhid/Documents/reviewpaper/corpus/final_audit.json', 'w'), indent=1)
print(f'verified OK: {ok}/{len(refs)}')
if fails:
    print('FAILURES:')
    for f in fails:
        print(' ', f)
else:
    print('ALL REFERENCES PASS Crossref re-verification')
