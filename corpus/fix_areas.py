#!/usr/bin/env python3
"""Re-classify selection entries by title rules, drop misfits, backfill from pool."""
import csv, json, re
from collections import defaultdict

POOL = '/home/touhid/Documents/reviewpaper/corpus/pool.csv'
SEL = '/home/touhid/Documents/reviewpaper/corpus/selection.json'
OUT = '/home/touhid/Documents/reviewpaper/corpus/selection2.json'

QUOTA = {
    'State estimation (SOC)': 14,
    'Health estimation (SOH)': 18,
    'Prognostics (RUL)': 13,
    'Charging control': 9,
    'Thermal management': 8,
    'Fault & safety': 8,
    'Cell balancing & ECM': 3,
    'Cross-cutting': 27,
}
VENUE_EXCL = ['ECS Meeting Abstracts', 'SSRN', 'Conference Series', 'IET Conference',
              'IFAC-PapersOnLine', 'Procedia', 'ECS Transactions', 'Franklin Open',
              'Electric and Hybrid Vehicle Technology International']
YEAR_CAP = {2019: 1, 2020: 9, 2021: 13, 2022: 15, 2023: 17, 2024: 19, 2025: 18, 2026: 12}

DROP_PAT = re.compile(r'corrigendum|erratum|publisher.s note|lifecycle assessment|'
                      r'life cycle assessment|charging session|charging infrastructure|'
                      r'transit bus|smart furniture', re.I)

def classify(title):
    t = title.lower()
    if DROP_PAT.search(t):
        return None
    if re.search(r'thermal runaway|thermal safety', t):
        return 'Fault & safety'
    if re.search(r'\bfault\b|anomaly|defect|short circuit|internal short', t):
        return 'Fault & safety'
    if re.search(r'state of charge|\bsoc\b estimation|\bsoc\b predict', t):
        return 'State estimation (SOC)'
    if re.search(r'state of health|\bsoh\b|health estimation|capacity estimation|'
                 r'capacity fade|health prognos|health state', t):
        return 'Health estimation (SOH)'
    if re.search(r'remaining useful life|\brul\b|cycle life|lifetime prediction|'
                 r'life prediction|prognos', t):
        return 'Prognostics (RUL)'
    if re.search(r'charg', t) and re.search(r'reinforcement|optimiz|optimis|strategy|'
                                            r'protocol|fast charg|bayesian|control', t):
        return 'Charging control'
    if re.search(r'thermal management|cooling|temperature|heat generation|'
                 r'thermal behavior|thermal model', t):
        return 'Thermal management'
    if re.search(r'cell balancing|equaliz', t):
        return 'Cell balancing & ECM'
    if re.search(r'equivalent circuit|parameter identif', t):
        return 'Cell balancing & ECM'
    return 'Cross-cutting'

def venue_ok(j):
    return not any(x.lower() in j.lower() for x in VENUE_EXCL) and len(j) > 3

def norm_title(t):
    t = re.sub(r'[^a-z0-9 ]', ' ', t.lower())
    return re.sub(r'\s+', ' ', t).strip()

sel = json.load(open(SEL))
kept, seen_titles = [], {}
for r in sel:
    area = classify(r['title'])
    if area is None or not venue_ok(r['journal']):
        print(f"DROP [{r['area']}] {r['title'][:70]}")
        continue
    r['area'] = area
    kept.append(r)
    seen_titles[norm_title(r['title'])] = True

count = defaultdict(int)
for r in kept:
    count[r['area']] += 1
print('after reclassify+drop:', dict(count))

# Backfill deficient areas from pool
rows = [r for r in csv.DictReader(open(POOL))]
for r in rows:
    r['year'] = int(r['year']); r['cites'] = int(r['cites'])
    r['journal'] = r['journal'].replace('&amp;', '&')
rows = [r for r in rows if venue_ok(r['journal'])]
year_count = defaultdict(int)
for r in kept:
    year_count[r['year']] += 1

for area, quota in QUOTA.items():
    deficit = quota - count[area]
    if deficit <= 0:
        continue
    cand = []
    for r in rows:
        a2 = classify(r['title'])
        if a2 != area:
            continue
        nt = norm_title(r['title'])
        if nt in seen_titles or any(norm_title(x['title']) == nt for x in kept):
            continue
        if r['doi'] in {k['doi'] for k in kept}:
            continue
        cand.append(r)
    cand.sort(key=lambda r: -r['cites'])
    for r in cand:
        if deficit <= 0:
            break
        if year_count[r['year']] >= YEAR_CAP.get(r['year'], 5):
            continue
        r['area'] = area
        kept.append(r)
        year_count[r['year']] += 1
        deficit -= 1
    count[area] = sum(1 for k in kept if k['area'] == area)

print('final:', dict(count), 'total', len(kept))
print('years:', dict(sorted(defaultdict(int, {y: sum(1 for k in kept if k['year']==y) for y in set(k['year'] for k in kept)}).items())))
json.dump(kept, open(OUT, 'w'), indent=1)
