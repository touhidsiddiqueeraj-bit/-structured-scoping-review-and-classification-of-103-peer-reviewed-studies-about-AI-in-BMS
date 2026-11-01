#!/usr/bin/env python3
"""Inter-rater reliability for the 30-paper re-coding (run AFTER all locks).

Round 1 (2026-10-17): reads corpus/reliability/coder_{A,B,C}_30.csv (locked sheets)
plus out/gold_labels_30.csv (withheld released labels) and writes
corpus/reliability/agreement_report.csv.

Round 2 (2026-11-01, full-text re-coding under codebook v1.1): if
corpus/reliability/coder_{B,C}_30_fulltext.csv exist, the same statistics are
computed for the round-2 sheets and written to
corpus/reliability/agreement_report_fulltext.csv (round-1 output untouched),
including the strong/non-strong validation-bucket agreement that the corpus
counts rest on.

Reports per coder vs gold: percent agreement + Cohen's kappa per field;
cross-coder pair agreement; Krippendorff's alpha (nominal) across coders.
No scipy required."""
import os
import csv, json, itertools, os, sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIELDS = ['area', 'method', 'chem', 'data', 'valid']
OUTDIR = f'{ROOT}/corpus/reliability'
GOLD = f'{ROOT}/out/gold_labels_30.csv'
STRONG = {'cross-cell holdout', 'cross-chemistry holdout', 'cross-domain holdout',
          'online/real-vehicle'}

dois = []
gold = {}
with open(GOLD) as f:
    for r in csv.DictReader(f):
        gold[r['doi'].lower()] = r
        dois.append(r['doi'].lower())
dois = sorted(gold)

def load_sheets(suffix):
    coders = {}
    for c in 'ABC':
        p = f'{OUTDIR}/coder_{c}_30{suffix}.csv'
        if os.path.exists(p):
            with open(p) as f:
                coders[c] = {r['doi'].lower(): r for r in csv.DictReader(f) if r['doi'] and r['doi'] != 'completed'}
    return coders

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

def alpha_field_across(sheets, f):
    """Krippendorff's alpha, nominal, across coders (units = papers with >=2 votes)."""
    units = []
    for d in dois:
        vs = [getv(s, d, f) for s in sheets.values()]
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
        pe = 1 - sum(fc * (fc - 1) for fc in freq.values()) / (n * (n - 1))
        D_e += m * (m - 1) / 2 * pe
    return 1 - D_o / D_e if D_e > 0 else float('nan')

def score_round(coders, label, report_path, bucket_pair=None):
    gold_map = {f: {d: gold[d].get(f, '') for d in dois} for f in FIELDS}
    report = []
    print(f'\n[{label}] papers: {len(dois)} | coders found: {", ".join(coders) or "NONE"}')
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
        a = alpha_field_across(coders, f)
        stat = '' if a != a else round(a, 3)
        report.append(dict(coder='all', comparison='alpha', field=f,
                           pct_agreement='', statistic='krippendorff_alpha', value=stat))
        print(f'  {f:<7} alpha = {a:.3f}' if a == a else f'  {f:<7} n/a (need >=2 coders)')
    if bucket_pair:
        c1, c2 = bucket_pair
        s1 = {d: coders[c1].get(d, {}) for d in dois}
        s2 = {d: coders[c2].get(d, {}) for d in dois}
        agree = sum((getv(s1, d, 'valid') in STRONG) == (getv(s2, d, 'valid') in STRONG) for d in dois)
        report.append(dict(coder=c1 + c2, comparison='pair', field='valid_strong_bucket',
                           pct_agreement=round(agree / len(dois) * 100, 1),
                           statistic='bucket_agreement', value=f'{agree}/{len(dois)}'))
        print(f'\nstrong/non-strong valid bucket ({c1}-{c2}): {agree}/{len(dois)} '
              f'({agree/len(dois)*100:.1f}%)')
    with open(report_path, 'w', newline='') as fp:
        w = csv.DictWriter(fp, fieldnames=['coder', 'comparison', 'field', 'pct_agreement', 'statistic', 'value'])
        w.writeheader()
        w.writerows(report)
    print(f'-> {report_path}')
    return report

# ---- round 1 (locked abstract-access sheets; output byte-identical to 2026-10-17 run) ----
r1 = load_sheets('')
score_round(r1, 'round 1 (locked sheets, 2026-10-17)', f'{OUTDIR}/agreement_report.csv',
            bucket_pair=('B', 'C') if {'B', 'C'} <= r1.keys() else None)

# ---- round 2 (full-text re-coding under codebook v1.1, 2026-11-01) ----
r2 = load_sheets('_fulltext')
if r2:
    score_round(r2, 'round 2 (full-text re-coding, 2026-11-01)', f'{OUTDIR}/agreement_report_fulltext.csv',
                bucket_pair=('B', 'C') if {'B', 'C'} <= r2.keys() else None)
else:
    print('\n(round-2 sheets not found - skipped)')


def _selftest():
    global dois
    # Cohen's kappa, known answer: obs=0.8, pe=0.36, k=0.6875
    m1 = {'d1': 'a', 'd2': 'a', 'd3': 'b', 'd4': 'b', 'd5': 'c'}
    m2 = {'d1': 'a', 'd2': 'b', 'd3': 'b', 'd4': 'b', 'd5': 'c'}
    old = dois
    dois = sorted(m1)
    obs, k = kappa_field('f', m1, m2)
    assert abs(k - 0.6875) < 1e-9 and abs(obs - 0.8) < 1e-9, (obs, k)
    # Krippendorff alpha, known answer: units [a,a],[a,b],[b,b] -> alpha = 4/9
    old_coders = coders = {'X': {'u1': {'f': 'a'}, 'u2': {'f': 'a'}, 'u3': {'f': 'b'}},
                           'Y': {'u1': {'f': 'a'}, 'u2': {'f': 'b'}, 'u3': {'f': 'b'}}}
    dois = ['u1', 'u2', 'u3']
    a = alpha_field_across(coders, 'f')
    assert abs(a - 4 / 9) < 1e-9, a
    dois = old
    print('selftest OK (kappa 0.6875 case; alpha 0.4444 case)')


if '--selftest' in sys.argv:
    _selftest()
