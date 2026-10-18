#!/usr/bin/env python3
"""Label-noise scenario sensitivity for the headline validation counts.

Scenarios (both seeded, 4000 draws each, seed 7):
  symmetric      - a drawn flip rate is applied to strong/non-strong bucket
                   labels at random, in either direction. This is a scenario
                   envelope, not an error model: symmetric random flipping
                   mechanically attenuates contrasts toward the null. The
                   rate is centered on the coders' OVERALL bucket error rate
                   against the released labels.
  strong_to_weak - the drawn rate flips strong labels to weak only, centered
                   on the STRONG-LABEL-SPECIFIC recode rate: the share of
                   strong-labelled sample papers that each coder recoded
                   weak. Because the coders worked from abstracts under a
                   declared "weak if unreported" fallback, that rate is an
                   upper bound on plausible label error, so this scenario is
                   reported as a worst-case bound, not an estimate.

The flip rate is drawn as Normal(mean, sd=0.02), clipped at zero, with the
mean set per scenario as described above.

Outputs corpus/sensitivity_label_noise.json. Run from repo root:
    python3 corpus/sensitivity_label_noise.py
"""
import os
import csv, json, random
from scipy.stats import fisher_exact

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROTO = ('cross-cell holdout', 'cross-chemistry holdout', 'cross-domain holdout', 'online/real-vehicle')

C = json.load(open(f'{ROOT}/corpus/papers_final.json'))
prim = [r for r in C if r['method'] != 'Review / perspective' and r['valid'] != 'review synthesis']
pi = [r for r in prim if r['method'] in ('Physics-informed', 'Hybrid physics+ML', 'Filter-based hybrid')]
other = [r for r in prim if r not in pi]
buckets = [1 if r['valid'] in PROTO else 0 for r in prim]
in_pi = [r in pi for r in prim]

def bucket_of(row):
    return 1 if (row.get('valid') or '').strip() in PROTO else 0

gold = {r['doi'].lower(): r for r in csv.DictReader(open(f'{ROOT}/out/gold_labels_30.csv'))}
n_strong_sample = sum(1 for r in gold.values() if r['valid'] in PROTO)
rates = []            # per-coder overall bucket error rate (symmetric scenario)
strong_rates = []     # per-coder strong->weak rate among strong-labelled rows
direction = {'strong_label_weak_coder': 0, 'weak_label_strong_coder': 0}
for coder in ('coder_B_30.csv', 'coder_C_30.csv'):
    rows = {r['doi'].lower(): r for r in csv.DictReader(open(f'{ROOT}/corpus/reliability/{coder}'))}
    n_err = 0
    s2w = 0
    for d in gold:
        gb = int(gold[d]['valid'] in PROTO)
        cb = bucket_of(rows[d])
        if gb != cb:
            n_err += 1
            if gb == 1:
                s2w += 1
                direction['strong_label_weak_coder'] += 1
            else:
                direction['weak_label_strong_coder'] += 1
    rates.append(n_err / len(gold))
    strong_rates.append(s2w / n_strong_sample)
e = sum(rates) / len(rates)                    # overall coder-vs-label error rate
e_dir = sum(strong_rates) / len(strong_rates)  # strong-label-specific recode rate

def fisher(labels):
    a = sum(1 for i in range(len(labels)) if labels[i] and in_pi[i])
    b = sum(in_pi) - a
    c = sum(1 for i in range(len(labels)) if labels[i] and not in_pi[i])
    d = (len(prim) - sum(in_pi)) - c
    return fisher_exact([[a, b], [c, d]])[1]

random.seed(7)
N = 4000

# ---- scenario 1: symmetric random flips (either direction) ----
shares, strong_counts, pvals = [], [], []
for _ in range(N):
    fr = max(0.0, random.gauss(e, 0.02))
    s = list(buckets)
    for i in range(len(s)):
        if random.random() < fr:
            s[i] = 1 - s[i]
    strong_counts.append(sum(s))
    shares.append(sum(s) / len(s))
    pvals.append(fisher(s))
shares.sort(); pvals.sort(); strong_counts.sort()

# ---- scenario 2: strong -> weak only (worst-case bound at the strong-specific rate) ----
shares2, strong_counts2, pvals2 = [], [], []
for _ in range(N):
    fr = max(0.0, random.gauss(e_dir, 0.02))
    s = list(buckets)
    for i in range(len(s)):
        if s[i] == 1 and random.random() < fr:
            s[i] = 0
    strong_counts2.append(sum(s))
    shares2.append(sum(s) / len(s))
    pvals2.append(fisher(s))
shares2.sort(); pvals2.sort(); strong_counts2.sort()

out = {
    'model': ('label-noise scenario envelope, not an error model: flip rate drawn as '
              'Normal(mean, sd=0.02), clipped at 0; 4000 draws per scenario; seed 7. '
              'Scenario "symmetric" flips strong/non-strong labels at random in either '
              'direction (null-attenuating), with the rate centered on the coders\' '
              'overall bucket error rate vs the released labels. Scenario '
              '"strong_to_weak" flips strong labels to weak only, with the rate '
              'centered on the strong-label-specific recode rate (each coder recoded '
              '8 of the 13 strong-labelled sample papers weak). Because the coders '
              'worked from abstracts under a declared "weak if unreported" fallback, '
              'that rate is an upper bound on plausible label error, so '
              '"strong_to_weak" is a worst-case bound, not an estimate.'),
    'n_primary': len(prim),
    'observed_coder_vs_label_error_rates': [round(r, 4) for r in rates],
    'strong_labelled_sample_rows': n_strong_sample,
    'strong_specific_recode_rates': [round(r, 4) for r in strong_rates],
    'observed_disagreement_direction': direction,
    'point_estimate_strong': sum(buckets),
    'symmetric': {
        'strong_count_range_95pct': [strong_counts[int(0.025 * N)], strong_counts[int(0.975 * N)]],
        'strong_share_range_95pct': [round(shares[int(0.025 * N)], 3), round(shares[int(0.975 * N)], 3)],
        'fisher_p_below_0.05_frac': round(sum(1 for p in pvals if p < 0.05) / N, 3),
    },
    'strong_to_weak_worst_case_bound': {
        'point_estimate_strong_at_observed_rate': round(sum(buckets) * (1 - e_dir), 1),
        'point_estimate_share_at_observed_rate': round(sum(buckets) * (1 - e_dir) / len(prim), 3),
        'strong_count_range_95pct': [strong_counts2[int(0.025 * N)], strong_counts2[int(0.975 * N)]],
        'strong_share_range_95pct': [round(shares2[int(0.025 * N)], 3), round(shares2[int(0.975 * N)], 3)],
        'fisher_p_below_0.05_frac': round(sum(1 for p in pvals2 if p < 0.05) / N, 3),
    },
}
json.dump(out, open(f'{ROOT}/corpus/sensitivity_label_noise.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
