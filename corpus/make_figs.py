#!/usr/bin/env python3
"""Generate all paper figures (template-matched: Times-like serif, 300 dpi)."""
import os
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['DejaVu Serif', 'Liberation Serif', 'Times New Roman'],
    'font.size': 9,
    'axes.titlesize': 10,
    'axes.labelsize': 9,
    'figure.dpi': 300,
})
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'figures/')
stats = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'corpus/stats.json')))

# ---------- Fig 3: two-panel — measured eligible-corpus trend + classified-subset method families ----------
elig = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'corpus/eligible_corpus.json')))
fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.2, 3.1), constrained_layout=True)
# 2027 is a single Crossref early-access metadata stamp; shown years are 2020-2026
ey = sorted(int(y) for y in elig['by_year'] if 2020 <= int(y) <= 2026)
ec = [elig['by_year'].get(str(y), 0) for y in ey]
axL.bar(ey, ec, color='#3b6ea5', width=0.72)
axL.set_ylabel('Eligible records per year')
axL.set_xlabel('Publication year')
axL.set_title('Tier 1: eligible corpus, 2020\u20132026 (n = 799)', fontsize=9)
for x, c in zip(ey, ec):
    axL.text(x, c + max(ec) * 0.015, str(c), ha='center', fontsize=7.2, color='#37352F')
axL.text(0.035, 0.97, 'one further record is\ndate-stamped 2027 by\nCrossref (not shown)',
         transform=axL.transAxes, ha='left', va='top', fontsize=6.4, color='#666666',
         bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='#cccccc', lw=0.5))
groups = ['Classical ML', 'Deep learning', 'Physics-informed / hybrid',
          'Optimization-augmented learning', 'Transfer / domain adaptation',
          'Reinforcement / control learning', 'Foundation models / LLM',
          'Review / perspective']
colors = ['#7f9fc4', '#3b6ea5', '#c44e52', '#ddae57', '#55a868', '#8172b2', '#333333', '#b0b0b0']
mgy = stats['method_group_by_year']
years2 = list(range(2019, 2027))
data = np.zeros((len(groups), len(years2)))
for gi, g in enumerate(groups):
    for yi, y in enumerate(years2):
        data[gi, yi] = mgy.get(str(y), {}).get(g, 0)
axR.stackplot(years2, data, labels=groups, colors=colors, alpha=0.92)
axR.set_ylabel('Classified-subset papers')
axR.set_xlabel('Publication year')
axR.set_ylim(0, data.sum(axis=0).max() * 1.25)
axR.set_xticks(years2)
axR.set_xticklabels([str(y) for y in years2], fontsize=6.8)
axR.set_title('Tier 2: classified subset (n = 103)', fontsize=9)
axR.legend(loc='upper left', bbox_to_anchor=(0, -0.22), fontsize=6, frameon=False, ncol=2)
fig.savefig(OUT + 'fig3_method_evolution.png', dpi=300)
plt.close(fig)

# ---------- Fig 2b (extended Fig 3): subset composition by year + cumulative ----------
years3 = list(range(2019, 2027))
by_year = stats['by_year']
counts3 = [by_year.get(str(y), by_year.get(y, 0)) for y in years3]
cum = np.cumsum(counts3)
fig, ax = plt.subplots(figsize=(4.4, 2.7), constrained_layout=True)
ax.bar(years3, counts3, color='#3b6ea5', width=0.7, label='Papers per year')
for x, c in zip(years3, counts3):
    ax.text(x, c + max(counts3) * 0.02, str(c), ha='center', fontsize=7.2, color='#37352F')
ax.set_ylabel('Classified-subset papers')
ax.set_xlabel('Publication year')
ax.set_ylim(0, max(counts3) * 1.3)
ax2 = ax.twinx()
ax2.plot(years3, cum, color='#c44e52', marker='o', ms=3.5, lw=1.3, label='Cumulative')
ax2.set_ylabel('Cumulative total')
ax2.set_ylim(0, max(cum) * 1.12)
h1, l1 = ax.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, loc='upper left', fontsize=7, frameon=False)
fig.savefig(OUT + 'fig2_year_trend.png', dpi=300)
plt.close(fig)

# ---------- Fig 4: application-area distribution ----------
areas = sorted(stats['by_area'].items(), key=lambda kv: kv[1])
names = [a[0] for a in areas]
vals = [a[1] for a in areas]
fig, ax = plt.subplots(figsize=(5.6, 2.9), constrained_layout=True)
bars = ax.barh(names, vals, color='#3b6ea5', height=0.62)
for b, v in zip(bars, vals):
    inside = v > max(vals) * 0.82
    ax.text(v - 0.45 if inside else v + 0.35, b.get_y() + b.get_height() / 2, str(v),
            va='center', ha='right' if inside else 'left', fontsize=8.5,
            color='white' if inside else '#37352F')
ax.set_xlim(0, max(vals) * 1.04)
ax.tick_params(axis='y', labelsize=9)
ax.set_xlabel('Papers in corpus')
fig.savefig(OUT + 'fig4_area_distribution.png', dpi=300)
plt.close(fig)

# ---------- Fig 5: data sources + validation ----------
fig, (axa, axb) = plt.subplots(1, 2, figsize=(6.8, 2.8))
data_map = {
    'self-lab': 'Own lab cycling', 'review': 'Review / none',
    'simulation': 'Simulation only', 'Severson-MATR': 'Public cycle-life (MATR)',
    'real-vehicle': 'Real vehicle / fleet', 'CALCE': 'Public (CALCE)',
    'EIS-lab': 'Lab EIS', 'NASA': 'Public (NASA)', 'mixed': 'Multiple datasets',
}
dd = sorted(((data_map[k], v) for k, v in stats['by_data'].items()), key=lambda kv: -kv[1])
axa.barh([d[0] for d in dd][::-1], [d[1] for d in dd][::-1], color='#55a868')
axa.set_xlabel('Papers')
axa.tick_params(axis='y', labelsize=8.5)
valid_map = {
    'cross-cell holdout': 'Cross-cell holdout', 'within-cell split': 'Within-cell split',
    'experimental hardware': 'Experimental hardware', 'cross-chemistry holdout': 'Cross-chemistry holdout',
    'online/real-vehicle': 'Online / fleet', 'cross-domain holdout': 'Cross-domain',
    'simulation': 'Simulation only', 'review synthesis': 'Review synthesis',
    'simulation plus hardware spot-check': 'Sim + hardware', 'cross-validation': 'k-fold CV',
    'case study': 'Case study',
}
vv = sorted(((valid_map.get(k, k), v) for k, v in stats['by_valid'].items()), key=lambda kv: -kv[1])
axb.barh([v[0] for v in vv][::-1], [v[1] for v in vv][::-1], color='#c44e52')
axb.set_xlabel('Papers')
axb.tick_params(axis='y', labelsize=8.5)
fig.tight_layout()
fig.savefig(OUT + 'fig5_data_validation.png', dpi=300)
plt.close(fig)

# ---------- Fig 6: five-year capability timeline (conceptual roadmap) ----------
fig, ax = plt.subplots(figsize=(6.5, 2.9))
milestones = [
    (2019.3, 2.95, 'Severson et al.\nearly-life cycle prediction'),
    (2020.3, 2.2, 'Attia et al.\nBayesian closed-loop\nfast charging'),
    (2021.2, 1.45, 'SOH pipelines at\nfleet scale'),
    (2022.2, 2.4, 'PINN & physics-\nhybrid wave'),
    (2023.2, 1.6, 'Cross-domain SOH &\ncloud BMS'),
    (2024.3, 2.3, 'Optimization-augmented\n& transfer learning'),
    (2025.3, 1.5, 'Deep-RL prognostics\n& transfer at scale'),
    (2026.2, 2.4, 'Foundation models\n& LLM agents'),
]
ax.hlines(1.0, 2018.9, 2026.75, color='#666666', lw=1.4)
for x, y, txt in milestones:
    ax.plot(x, 1.0, 'o', ms=5, color='#c44e52', zorder=3)
    ax.annotate(txt, (x, 1.0), xytext=(x, y), ha='center', fontsize=7.8,
                arrowprops=dict(arrowstyle='-', lw=0.6, color='#999999'))
ax.set_ylim(0.4, 3.6)
ax.set_xlim(2018.9, 2026.75)
ax.set_yticks([])
ax.set_xticks(list(range(2019, 2027)))
ax.set_xlabel('Year', fontsize=10)
ax.tick_params(axis='x', labelsize=9.5)
ax.spines[['top', 'right', 'left']].set_visible(False)
fig.tight_layout()
fig.savefig(OUT + 'fig6_timeline.png', dpi=300)
plt.close(fig)

print('figures 2-6 done')
