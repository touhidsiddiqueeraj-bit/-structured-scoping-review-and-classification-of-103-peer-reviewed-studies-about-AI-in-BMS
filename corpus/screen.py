#!/usr/bin/env python3
"""Screen candidate pool to ~100 corpus papers with area quotas, year balance,
reputable-journal constraint, and duplicate rejection."""
import csv, json, re
from collections import defaultdict

POOL = '/home/touhid/Documents/reviewpaper/corpus/pool.csv'
SEEDS = '/home/touhid/Documents/reviewpaper/corpus/seeds.json'
OUT = '/home/touhid/Documents/reviewpaper/corpus/selection.json'

# Journals excluded: abstract/preview venues, preprint servers, conference series
EXCLUDE_VENUES = [
    'ECS Meeting Abstracts', 'SSRN', 'Journal of Physics: Conference Series',
    'IET Conference Proceedings', 'IFAC-PapersOnLine', 'Procedia',
    'ECS Transactions', 'MRS Advances', 'Conference', 'Abstracts',
    'Journal of Mechanical Engineering',  # obscure non-English venue noise
    'Electric and Hybrid Vehicle Technology International', 'Franklin Open',
]

# Corpus quotas per BMS function area
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
CROSS_PREFIXES = ['Physics-informed', 'Transfer learning', 'Digital twins',
                  'Foundation models', 'Graph networks', 'Benchmarks & data',
                  'Interpretability', 'Cloud & fleet', 'Second life',
                  'Cross-cutting']
YEAR_CAP = {2020: 8, 2021: 13, 2022: 15, 2023: 17, 2024: 19, 2025: 18, 2026: 12}
# Landmark seeds always included (background, cited but counted within areas)
FORCE_DOIS = {
    '10.1038/s41586-020-1994-5': 'Charging control',      # Attia 2020
    '10.1038/s42256-021-00312-3': 'Health estimation (SOH)',  # Roman 2021
    '10.1038/s41467-020-15235-7': 'Health estimation (SOH)',  # Zhang 2020 EIS
    '10.1038/s42256-020-0156-7': 'Cross-cutting',          # Ng 2020 perspective
    '10.1016/j.joule.2019.11.018': 'Cross-cutting',        # Hu 2020 prognostics review
    '10.1038/s41560-019-0356-8': 'Prognostics (RUL)',      # Severson 2019 (background)
}

def clean_journal(j):
    return j.replace('&amp;', '&').strip()

def venue_ok(j):
    return not any(x.lower() in j.lower() for x in EXCLUDE_VENUES) and len(j) > 3

rows = list(csv.DictReader(open(POOL)))
for r in rows:
    r['year'] = int(r['year'])
    r['cites'] = int(r['cites'])
    r['journal'] = clean_journal(r['journal'])

# index by doi, keep max-cites variant
bydoi = {}
for r in rows:
    if not venue_ok(r['journal']):
        continue
    d = r['doi']
    if d not in bydoi or r['cites'] > bydoi[d]['cites']:
        bydoi[d] = r

def primary_area(r):
    areas = r['areas'].split(';')
    for a in ['State estimation (SOC)', 'Health estimation (SOH)', 'Prognostics (RUL)',
              'Charging control', 'Thermal management', 'Fault & safety',
              'Cell balancing & ECM']:
        if a in areas:
            return a
    for a in areas:
        if a in CROSS_PREFIXES:
            return 'Cross-cutting'
    return None

def normalize_title(t):
    t = t.lower()
    t = re.sub(r'[^a-z0-9 ]', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

selected = {}
title_seen = {}
year_count = defaultdict(int)

def try_add(r, area, cite_floor=0):
    if area is None or r['doi'] in selected:
        return False
    if year_count[r['year']] >= YEAR_CAP.get(r['year'], 6):
        return False
    nt = normalize_title(r['title'])
    if nt in title_seen:
        return False
    selected[r['doi']] = dict(r)
    selected[r['doi']]['area'] = area
    title_seen[nt] = r['doi']
    year_count[r['year']] += 1
    return True

# 1. Force landmarks (ignore year caps)
for doi, area in FORCE_DOIS.items():
    if doi in bydoi:
        r = bydoi[doi]
        r2 = dict(r); r2['area'] = area
        selected[doi] = r2
        title_seen[normalize_title(r['title'])] = doi
        year_count[r['year']] += 1
    else:
        print(f'WARN: force DOI missing from pool: {doi}')

# 2. Per-area greedy fill: interleave top-cited with recent for balance
for area, quota in QUOTA.items():
    cand = [r for r in bydoi.values() if primary_area(r) == area]
    recent = [r for r in cand if r['year'] >= 2024]
    older = [r for r in cand if r['year'] < 2024]
    recent.sort(key=lambda r: -r['cites'])
    older.sort(key=lambda r: -r['cites'])
    got = sum(1 for r in selected.values() if r.get('area') == area)
    # alternate older (citations) / recent (recency-aware) while quota remains
    oi, ri = 0, 0
    while got < quota and (oi < len(older) or ri < len(recent)):
        added = False
        if oi < len(older):
            added = try_add(older[oi], area) or False
            oi += 1
        if got >= quota:
            break
        if ri < len(recent):
            added = try_add(recent[ri], area) or added
            ri += 1
        got = sum(1 for r in selected.values() if r.get('area') == area)

print(f'selected: {len(selected)}')
area_count = defaultdict(int)
year_sel = defaultdict(int)
for r in selected.values():
    area_count[r['area']] += 1
    year_sel[r['year']] += 1
print('by area:', dict(sorted(area_count.items())))
print('by year:', dict(sorted(year_sel.items())))

json.dump(list(selected.values()), open(OUT, 'w'), indent=1)
print('wrote', OUT)
