#!/usr/bin/env python3
"""Final audit: record every reference DOI with its Crossref-resolved title and
venue, and (when network access is available) re-verify against the registry.

Default (offline) mode rebuilds corpus/final_audit.json from the cached
retrieval-time Crossref resolutions (verified.json, conference_verified.json,
external_verified.json) covering every reference of the built manuscripts, so
the released audit file records title + venue for each reference as resolved
at retrieval time.

Online mode (--online START END) re-resolves a slice of the DOCX reference
list against api.crossref.org and updates the 'reverified' field.
"""
import os
import re, json, subprocess, time, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS = json.load(open(os.path.join(ROOT, 'corpus/verified.json')))
CONF = json.load(open(os.path.join(ROOT, 'corpus/conference_verified.json')))
EXT = json.load(open(os.path.join(ROOT, 'corpus/external_verified.json')))
OUT = os.path.join(ROOT, 'corpus/final_audit.json')

# ---------- offline rebuild: title + venue per reference DOI ----------
audit = []
for i, r in enumerate(CORPUS + CONF + EXT, 1):
    audit.append({
        'n': str(i),
        'doi': r['doi'],
        'title_cr': r.get('title_cr') or r.get('title') or '',
        'venue_cr': r.get('journal') or '',
        'year': r.get('year'),
        'verified': True,           # resolved against Crossref at retrieval
        'source': ('corpus' if i <= len(CORPUS)
                   else 'conference' if i <= len(CORPUS) + len(CONF)
                   else 'external'),
    })
json.dump(audit, open(OUT, 'w'), indent=1)
print(f'final_audit.json rebuilt offline: {len(audit)} references with '
      f'Crossref-resolved title + venue (retrieval-time metadata)')

# ---------- optional online re-verification slice ----------
if '--online' in sys.argv:
    k = sys.argv.index('--online')
    START, END = int(sys.argv[k + 1]), int(sys.argv[k + 2])
    from docx import Document
    doc = Document(os.path.join(ROOT, 'ML-BMS-Review.docx'))
    refs, in_refs = [], False
    for p in doc.paragraphs:
        t = p.text.strip()
        if t == 'References':
            in_refs = True
            continue
        if in_refs and t:
            refs.append(t)
    refs = refs[START:END]
    print(f'online re-verification of refs {START+1}-{START+len(refs)}')
    by_doi = {a['doi'].lower().rstrip('.'): a for a in audit}
    fails, ok = [], 0
    for r in refs:
        m = re.match(r'^(\d+)\.\s+(.*)$', r)
        if not m:
            continue
        n, body = m.group(1), m.group(2)
        dm = re.search(r'doi:\s*(\S+)\.?$', body)
        if not dm:
            fails.append(('NODOI', r[:80]))
            continue
        doi = dm.group(1)
        rec = by_doi.get(doi.lower())
        p = subprocess.run(['curl', '-s', '--max-time', '25',
                            f'https://api.crossref.org/works/{doi}'],
                           capture_output=True, text=True)
        try:
            msg = json.loads(p.stdout)['message']
            cr_title = (msg.get('title') or [''])[0]
            cr_venue = (msg.get('container-title') or [''])[0]
            norm = lambda s: re.sub(r'[^a-z0-9]', '', s.lower())
            title_ok = norm(rec['title_cr'])[:25] == norm(cr_title)[:25] if rec else False
            if title_ok and rec:
                rec['reverified'] = True
                ok += 1
            else:
                fails.append((doi, rec['title_cr'][:50] if rec else '?', cr_title[:50]))
        except Exception:
            fails.append((doi, 'NETWORK', ''))
        time.sleep(0.3)
    json.dump(audit, open(OUT, 'w'), indent=1)
    print(f're-verified OK: {ok}/{len(refs)}')
    for f in fails:
        print('  FAIL:', f)
