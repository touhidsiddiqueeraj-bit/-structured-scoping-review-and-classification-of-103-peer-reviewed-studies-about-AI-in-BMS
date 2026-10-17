#!/usr/bin/env python3
"""Inter-rater reliability for the 30-paper re-coding (run AFTER all locks).

Reads: corpus/reliability/coder_{A,B,C}_30.csv  (locked sheets)
       out/gold_labels_30.csv                   (withheld released labels)
Writes: corpus/reliability/agreement_report.csv
Reports per coder vs gold: percent agreement + Cohen's kappa per field;
cross-coder pair agreement; Krippendorff's alpha (nominal) across coders.
No scipy required."""
import csv, json, itertools, os, sys
from collections import Counter, defaultdict

ROOT = '/home/touhid/Documents/reviewpaper'
FIELDS = ['area', 'method', 'chem', 'data', 'valid']
OUTDIR = f'{ROOT}/corpus/reliability'

coders = {}
for c in 'ABC':
    p = f'{OUTDIR}/coder_{c}_30.csv'
    if os.path.exists(p):
        with open(p) as f:
            coders[c] = {r['doi'].lower(): r for r in csv.DictReader(f)}
gold = {}
with open(f'{ROOT}/out/gold_labels_30.csv') as f:
    for r in csv.DictReader(f):
        gold[r['doi'].lower()] = r

dois = sorted(gold)
print('papers:', len(dois), '| coders found:', ', '.join(coders) or 'NONE')

def getv(mapping, d, f):
    """mapping values are either raw strings (gold) or row dicts (coder sheets)."""
    v = mapping.get(d, '')
    if isinstance(v, dict):
        v = v.get(f, '')
    return str(v).strip()

def kappa_field(f, m1, m2):
    """Cohen's kappa treating empty strings as a distinct category (missing)."""
    n = len(dois)
    x1 = [getv(m1, d, f) for d in dois]
    x2 = [getv(m2, d, f) for d in dois]
    obs = sum(a == b for a, b in zip(x1, x2)) / n
    pair = list(zip(x1, x2))
    joint = Counter(pair)
    p1 = {k: sum(v for (a, b), v in joint.items() if a == k) / n for k in {a for a, b in pair}}
    p2 = {k: sum(v for (a, b), v in joint.items() if b == k) / n for k in {b for a, b in pair}}
    pe = sum(p1.get(k, 0.0) * p2.get(k, 0.0) for k in set(p1) | set(p2))
    k = 0.0 if pe == 1 else (obs - pe) / (1 - pe)
    return obs, k

def alpha_field(f):
    """Krippendorff's alpha, nominal, across coders (units = papers with >=2 votes)."""
    units = []
    for d in dois:
        vs = [getv(s, d, f) for s in coders.values()]
        vs = [v for v in vs if v]
        if len(vs) >= 2:
            units.append(vs)
    n = sum(len(v) for v in units)
    if n <= 1:
        return float('nan')
    freq = Counter(x for v in units for x in v)
    D_o = 0.0
    D_e = 0.0
    for v in units:
        m = len(v)
        if m < 2:
            continue
        D_o += sum(1 for i, j in itertools.combinations(range(m), 2) if v[i] != v[j])
        # expected disagreement prob for a random pair drawn from the whole pool
        pe = 1 - sum(fc * (fc - 1) for fc in freq.values()) / (n * (n - 1))
        D_e += m * (m - 1) / 2 * pe
    return 1 - D_o / D_e if D_e > 0 else float('nan')

gold_map = {f: {d: gold[d].get(f, '') for d in dois} for f in FIELDS}
report = []
print('\nper-coder agreement with released labels:')
for c in sorted(coders):
    sheet = {d: coders[c].get(d, {}) for d in dois}
    for f in FIELDS:
        obs, k = kappa_field(f, gold_map[f], sheet)
        report.append(dict(coder=c, comparison='vs_gold', field=f,
                           pct_agreement=round(obs * 100, 1), statistic='kappa', value=round(k, 3)))
        print(f'  {c} vs gold  {f:<7} {obs*100:5.1f}%  k={k:+.3f}')

print('\ncoder-pair agreement:')
for c1, c2 in itertools.combinations(sorted(coders), 2):
    s1 = {d: coders[c1].get(d, {}) for d in dois}
    s2 = {d: coders[c2].get(d, {}) for d in dois}
    for f in FIELDS:
        obs, k = kappa_field(f, s1, s2)
        report.append(dict(coder=c1 + c2, comparison='pair', field=f,
                           pct_agreement=round(obs * 100, 1), statistic='kappa', value=round(k, 3)))
        print(f'  {c1}-{c2}  {f:<7} {obs*100:5.1f}%  k={k:+.3f}')

print('\nKrippendorff alpha (across coders):')
for f in FIELDS:
    a = alpha_field(f)
    stat = '' if a != a else round(a, 3)
    report.append(dict(coder='all', comparison='alpha', field=f,
                       pct_agreement='', statistic='krippendorff_alpha', value=stat))
    print(f'  {f:<7} alpha = {a:.3f}' if a == a else f'  {f:<7} n/a (need >=2 coders)')

with open(f'{OUTDIR}/agreement_report.csv', 'w', newline='') as fp:
    w = csv.DictWriter(fp, fieldnames=['coder', 'comparison', 'field', 'pct_agreement', 'statistic', 'value'])
    w.writeheader()
    w.writerows(report)
print('\n-> corpus/reliability/agreement_report.csv')


def _selftest():
    global dois, coders
    # Cohen's kappa, known answer: obs=0.8, pe=0.36, k=0.6875
    m1 = {'d1': 'a', 'd2': 'a', 'd3': 'b', 'd4': 'b', 'd5': 'c'}
    m2 = {'d1': 'a', 'd2': 'b', 'd3': 'b', 'd4': 'b', 'd5': 'c'}
    old = dois
    dois = sorted(m1)
    obs, k = kappa_field('f', m1, m2)
    assert abs(k - 0.6875) < 1e-9 and abs(obs - 0.8) < 1e-9, (obs, k)
    # Krippendorff alpha, known answer: units [a,a],[a,b],[b,b] -> alpha = 4/9
    old_coders = coders
    coders = {'X': {'u1': {}, 'u3': {}}, 'Y': {'u2': {}, 'u3': {}}}
    # build manually: coder X gives u1=a, u2=a, u3=b; coder Y gives u1=a, u2=b, u3=b
    coders = {
        'X': {'u1': {'f': 'a'}, 'u2': {'f': 'a'}, 'u3': {'f': 'b'}},
        'Y': {'u1': {'f': 'a'}, 'u2': {'f': 'b'}, 'u3': {'f': 'b'}},
    }
    old_dois = dois
    dois = ['u1', 'u2', 'u3']
    a = alpha_field('f')
    assert abs(a - 4 / 9) < 1e-9, a
    dois = old_dois
    coders = old_coders
    dois = old
    print('selftest OK (kappa 0.6875 case; alpha 0.4444 case)')


if '--selftest' in sys.argv:
    _selftest()
