#!/usr/bin/env python3
"""Label-noise scenario sensitivity for the headline validation counts.

Model: the released labels are treated as one plausible coding. The two blind
re-coders (coder_B, coder_C) disagree with the released bucket labels on some
of the 30 reliability papers; that observed per-coder disagreement rate defines
the plausible label-error rate. Each scenario draw (a) resamples the error
rate around the two-coder empirical estimate, (b) flips strong/non-strong
bucket labels accordingly across the 88 primary-application papers, and
(c) recomputes (i) the overall strong-protocol share and (ii) the
physics-informed versus other Fisher exact test for the method-family
contrast. Seeded and reproducible.

Outputs corpus/sensitivity_label_noise.json. Run from repo root:
    python3 corpus/sensitivity_label_noise.py
"""
import csv, json, random
from scipy.stats import fisher_exact

ROOT = '/home/touhid/Documents/reviewpaper'
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
rates = []
for coder in ('coder_B_30.csv', 'coder_C_30.csv'):
    rows = {r['doi'].lower(): r for r in csv.DictReader(open(f'{ROOT}/corpus/reliability/{coder}'))}
    n_err = sum(int(bucket_of(rows[d]) != int(gold[d]['valid'] in PROTO)) for d in gold)
    rates.append(n_err / len(gold))
e = sum(rates) / len(rates)  # observed coder-vs-label error rate

random.seed(7)
N = 4000
shares, strong_counts, pvals = [], [], []
pi_strong, other_strong = [], []
for _ in range(N):
    fr = max(0.0, random.gauss(e, 0.02))
    s = list(buckets)
    for i in range(len(s)):
        if random.random() < fr:
            s[i] = 1 - s[i]
    strong_counts.append(sum(s))
    shares.append(sum(s) / len(s))
    a = sum(1 for i in range(len(s)) if s[i] and in_pi[i])
    b = sum(in_pi) - a
    c = sum(1 for i in range(len(s)) if s[i] and not in_pi[i])
    d = (len(prim) - sum(in_pi)) - c
    pvals.append(fisher_exact([[a, b], [c, d]])[1])
    pi_strong.append(a)
    other_strong.append(c)

shares.sort(); pvals.sort(); strong_counts.sort()
out = {
    'model': ('label-noise scenarios: flip rate drawn as Normal(mean=observed '
              'coder-vs-label bucket error rate, sd=0.02), clipped at 0; 4000 draws; seed 7'),
    'n_primary': len(prim),
    'observed_coder_vs_label_error_rates': rates,
    'point_estimate_strong': sum(buckets),
    'strong_count_range_95pct': [strong_counts[int(0.025 * N)], strong_counts[int(0.975 * N)]],
    'strong_share_range_95pct': [round(shares[int(0.025 * N)], 3), round(shares[int(0.975 * N)], 3)],
    'strong_share_median': round(shares[N // 2], 3),
    'fisher_p_range': [round(pvals[0], 4), round(pvals[-1], 4)],
    'fisher_p_below_0.05_frac': round(sum(1 for p in pvals if p < 0.05) / N, 3),
}
json.dump(out, open(f'{ROOT}/corpus/sensitivity_label_noise.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
