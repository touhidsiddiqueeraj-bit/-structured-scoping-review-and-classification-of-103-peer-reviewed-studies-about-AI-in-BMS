#!/usr/bin/env python3
"""Record-level screening provenance: one row per record retrieved (883+ refs),
with stage statuses, function tags, and exclusion reasons. Reviewer fix:
makes the selection process verifiable (TTE R3: 'record-level screening table')."""
import csv, json
import pool

POOL = '/home/touhid/Documents/reviewpaper/corpus/pool.csv'
FINAL = '/home/touhid/Documents/reviewpaper/corpus/eligible_corpus.json'
SUBSET = '/home/touhid/Documents/reviewpaper/corpus/papers_final.json'
OUT = '/home/touhid/Documents/reviewpaper/corpus/screening_log.csv'

EXCLUDE_VENUES = [
    'ECS Meeting Abstracts', 'SSRN', 'Journal of Physics: Conference Series',
    'IET Conference Proceedings', 'IFAC-PapersOnLine', 'Procedia',
    'ECS Transactions', 'MRS Advances', 'Conference', 'Abstracts',
    'Journal of Mechanical Engineering',
    'Electric and Hybrid Vehicle Technology International', 'Franklin Open',
]

def venue_reason(j):
    jlo = j.lower().replace('&amp;', '&')
    for x in EXCLUDE_VENUES:
        if x.lower() in jlo:
            return f'venue screening: {x}'
    return None

rows = list(pool.dedup().values())
# title-gate decision for every deduplicated record (retained or excluded)
RETAIN = {}
for r in rows:
    RETAIN[r['doi'].lower()] = pool.is_battery_related(r['title'])
all_rows = rows
rows = [r for r in rows if RETAIN[r['doi']]]
elig = {r['doi'].lower() for r in json.load(open(FINAL))['records']}
subset = {r['doi'].lower() for r in json.load(open(SUBSET))}

def row_meta(r):
    doi = r['doi'].lower()
    if doi in subset:
        return 'Tier2-classified (103)', ''
    if doi in elig:
        return 'Tier1-eligible (799)', ''
    reason = venue_reason(r['journal']) or 'venue screening: other'
    return 'excluded', reason

# title-gate exclusions (667): reasons must name the gate, not look venue-driven
def title_gate_row(r):
    t = ' ' + r['title'].lower() + ' '
    has_b = any(x in t for x in pool.BATTERY_TERMS)
    has_m = any(x in t for x in pool.ML_TERMS)
    miss = 'battery term' if not has_b else 'ML term'
    return {'doi': r['doi'].lower(), 'title': r['title'], 'journal': r['journal'],
            'year': r['year'], 'cites': r['cites'],
            'function_tags': ';'.join(sorted(r['areas'])),
            'status': 'excluded', 'reason_or_note': f'title gate: no {miss} in title'}

# prefer the variant pair that keeps a record eligible (duplicates vary in venue metadata)
best = {}
for r in rows:
    doi = r['doi'].lower()
    status, reason = row_meta(r)
    rank = {'Tier2-classified (103)': 0, 'Tier1-eligible (799)': 1, 'excluded': 2}[status]
    old = best.get(doi)
    if old is None or rank < old[0]:
        best[doi] = (rank, r, status, reason)

LOG = []
for doi, (rank, r, status, reason) in best.items():
    LOG.append({'doi': doi, 'title': r['title'], 'journal': r['journal'],
                'year': r['year'], 'cites': r['cites'], 'function_tags': r['areas'],
                'status': status, 'reason_or_note': reason})

# add every title-gate-excluded record not covered by best (dedup was over all raw records)
covered = {r['doi'] for r in LOG}
for r in all_rows:
    d = r['doi']
    if d in covered:
        continue
    if RETAIN[d]:
        print('WARN: retained record missing from log:', d)
        continue
    LOG.append(title_gate_row(r))

# forced seeds / individually retrieved subset papers absent from the query pool
sub = json.load(open(SUBSET)) if isinstance(SUBSET, str) else SUBSET
for doi in sorted(subset - covered):
    rec = [x for x in (sub if isinstance(sub, list) else sub['records']) if x['doi'].lower() == doi]
    if rec:
        x = rec[0]
        LOG.append({'doi': doi, 'title': (x.get('title_cr') or x.get('title_pool') or ''),
                    'journal': (x.get('venue_cr') or x.get('journal') or ''),
                    'year': x.get('year'), 'cites': x.get('citations', ''),
                    'function_tags': x.get('area', ''), 'status': 'Tier2-classified (103)',
                    'reason_or_note': 'forced-seed subset paper, retrieved individually (outside query pool)'})
print('log rows:', len(LOG))

LOG.sort(key=lambda r: (r['status'], r['journal'], r['year']))
with open(OUT, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['doi', 'title', 'journal', 'year', 'cites',
                                      'function_tags', 'status', 'reason_or_note'])
    w.writeheader()
    w.writerows(LOG)
print('screening_log.csv:', len(LOG), 'rows;',
      sum(1 for r in LOG if r['status'] == 'Tier2-classified (103)'), 'classified;',
      sum(1 for r in LOG if r['status'] == 'Tier1-eligible (799)'), 'eligible;',
      sum(1 for r in LOG if r['status'] == 'excluded'), 'excluded')

# released term lists for the title gate and function tagging
json.dump({'battery_terms': pool.BATTERY_TERMS, 'ml_terms': pool.ML_TERMS,
           'gate_rule': 'title lowercased; must contain >=1 battery term and >=1 ML term',
           'function_tag_source': 'function tags come from the Crossref query-key prefix map (AREA_OF_KEY in pool.py), i.e. the queries a record matched; they are not derived from the title-gate term lists',
           'function_tag_map': {k: v for k, v in pool.AREA_OF_KEY.items()}},
          open('/home/touhid/Documents/reviewpaper/corpus/tagging_terms.json', 'w'), indent=1)
print('tagging_terms.json written')
