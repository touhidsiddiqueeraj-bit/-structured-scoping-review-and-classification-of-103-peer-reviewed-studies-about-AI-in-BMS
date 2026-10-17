#!/usr/bin/env python3
"""Create blind coding sheets for independent coders 2 and 3 (reliability fix).

Draws a stratified random 30-paper sample (seed 20261017) from papers_final,
strips ALL released labels, and writes corpus/reliability/coder_{A,B,C}_30.csv
with only identifiers + blank coding columns. Gold labels are withheld from
the coders and written to out/gold_labels_30.csv, which ships in the deposit
and is read by the reliability script only after locks."""
import os
import csv, json, random, os
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C = json.load(open(f'{ROOT}/corpus/papers_final.json'))
OUTDIR = f'{ROOT}/corpus/reliability'
os.makedirs(OUTDIR, exist_ok=True)

random.seed(20261017)
BANDS = {2019: '<=2021', 2020: '<=2021', 2021: '<=2021', 2022: '2022-2023', 2023: '2022-2023'}
band = lambda y: BANDS.get(y, '2024-2026')

strata = defaultdict(list)
for r in C:
    strata[(r['area'], band(r['year']))].append(r)

# allocation: proportional with min 1 per non-empty stratum, largest-remainder trim to 30
sizes = {k: len(v) for k, v in strata.items()}
N = sum(sizes.values())
raw = {k: 30 * s / N for k, s in sizes.items()}
base = {k: max(1, int(v)) if sizes[k] >= 2 else min(1, sizes[k]) for k, v in raw.items()}
over = sum(base.values()) - 30
if over > 0:
    # trim from largest allocations while keeping >=1
    keys = sorted(base, key=lambda k: -(base[k] - raw[k]))
    for k in keys:
        if over <= 0:
            break
        if base[k] > 1:
            dec = min(base[k] - 1, over)
            base[k] -= dec
            over -= dec
sample = []
for (area, yr), rows in sorted(strata.items(), key=lambda kv: (-len(kv[1]), kv[0])):
    take = base.get((area, yr), 0)
    if take <= 0: continue
    take = min(take, len(rows))
    sample += random.sample(rows, take)

# exact top-up / trim at paper level
while len(sample) > 30:
    sample.pop(random.randrange(len(sample)))
have = {(area, yr) for (area, yr), rows in strata.items() for _ in rows}
present = {(r['area'], band(r['year'])) for r in sample}
missing = [k for k in have if k not in present and k in strata]
for k in missing:
    if len(sample) >= 30: break
    sample.append(random.choice(strata[k]))
while len(sample) > 30:
    sample.pop(random.randrange(len(sample)))
random.shuffle(sample)

COLS = ['area', 'method', 'chem', 'data', 'valid',
        'access', 'evidence_area', 'evidence_method', 'evidence_valid', 'comment']
for coder in 'ABC':
    with open(f'{OUTDIR}/coder_{coder}_30.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['doi', 'title', 'journal', 'year'] + COLS)
        w.writeheader()
        for r in sample:
            t = (r.get('title') or r.get('title_cr') or r.get('title_pool') or '').replace('&amp;', '&')
            w.writerow({'doi': r['doi'], 'title': t,
                        'journal': r['journal'].replace('&amp;', '&'), 'year': r['year'],
                        **{c: '' for c in COLS}})

# gold labels withheld (not in reliability dir): keep for scoring only
with open(f'{ROOT}/out/gold_labels_30.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['doi', 'area', 'method', 'chem', 'data', 'valid'])
    w.writeheader()
    for r in sample:
        w.writerow({k: r.get(k, '') for k in ['doi', 'area', 'method', 'chem', 'data', 'valid']})

from collections import Counter
print('sample =', len(sample))
print('by area:', dict(Counter(r['area'] for r in sample)))
print('by band:', dict(Counter(band(r['year']) for r in sample)))
print('sheets:', OUTDIR + '/coder_{A,B,C}_30.csv')
