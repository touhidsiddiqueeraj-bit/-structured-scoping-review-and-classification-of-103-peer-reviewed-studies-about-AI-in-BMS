#!/usr/bin/env python3
"""Rule-based selection applied to ALL venue-screened eligible records.

Reviewer fix (TTE rejection, R1#1/R2#1/R3): the original function-quota step
partly wrote the corpus distributions. This script applies rule-based
inclusion criteria uniformly to the full venue-screened pool:

  Rule R1 (venue): not in EXCLUDE_VENUES (same list as screen.py).
  Rule R2 (relevance): every pool record already passed the title-level
      relevance gate (battery AND ML terms) in pool.py.
  Rule R3 (function tag): the record carries at least one management-function
      tag from the tagging pass; the function label is the primary tag.

No quotas, no year caps, no citation thresholds. Everything below is measured
from the eligible set, not selected into it.
Output: corpus/eligible_corpus.json with one row per study.
"""
import os
import csv, json
from collections import Counter, defaultdict

POOL = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'corpus/pool.csv')
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'corpus/eligible_corpus.json')

EXCLUDE_VENUES = [
    'ECS Meeting Abstracts', 'SSRN', 'Journal of Physics: Conference Series',
    'IET Conference Proceedings', 'IFAC-PapersOnLine', 'Procedia',
    'ECS Transactions', 'MRS Advances', 'Conference', 'Abstracts',
    'Journal of Mechanical Engineering',
    'Electric and Hybrid Vehicle Technology International', 'Franklin Open',
]

def venue_ok(j):
    return not any(x.lower() in j.lower() for x in EXCLUDE_VENUES) and len(j) > 3

rows = list(csv.DictReader(open(POOL)))
for r in rows:
    r['year'] = int(r['year'])
    r['cites'] = int(r['cites'])
    r['journal'] = r['journal'].replace('&amp;', '&').strip()

# dedupe by DOI keeping max-cites variant
bydoi = {}
for r in rows:
    d = r['doi'].lower()
    if not venue_ok(r['journal']):
        continue
    if d not in bydoi or r['cites'] > bydoi[d]['cites']:
        bydoi[d] = r

area_counts = Counter()
years = Counter()
area_year = defaultdict(Counter)
for r in bydoi.values():
    areas = r['areas'].split(';')
    area_counts.update(areas)
    years[r['year']] += 1
    for a in areas:
        area_year[a][r['year']] += 1

print('eligible records (rule-based, no quotas):', len(bydoi))
print('by year:', dict(sorted(years.items())))
print('\nby tag count (records can carry tags from >1 area):')
for a, c in area_counts.most_common():
    print(f'  {a}: {c}')

para = {a: area_year[a] for a in ['State estimation (SOC)', 'Health estimation (SOH)',
        'Prognostics (RUL)', 'Charging control', 'Thermal management',
        'Fault & safety', 'Cell balancing & ECM']}
print('\nprimary-area totals:')
for a, yc in para.items():
    print(f'  {a}: {sum(yc.values())}')

out = {
    'n': len(bydoi),
    'records': sorted(bydoi.values(), key=lambda r: (r['year'], r['journal'])),
    'by_year': dict(sorted(years.items())),
    'tag_counts': dict(area_counts.most_common()),
    'primary_area_years': {a: dict(sorted(yc.items())) for a, yc in para.items()},
}
json.dump(out, open(OUT, 'w'), indent=1, default=lambda o: dict(o))
print('\n->', OUT)
