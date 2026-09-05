#!/usr/bin/env python3
"""Generate all paper figures (template-matched: Times-like serif, 300 dpi)."""
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
OUT = '/home/touhid/Documents/reviewpaper/figures/'
stats = json.load(open('/home/touhid/Documents/reviewpaper/corpus/stats.json'))

# ---------- Fig 2: publications per year ----------
years = list(range(2020, 2027))
counts = [stats['by_year'].get(str(y), 0) for y in years]
cum = np.cumsum(counts)
fig, ax = plt.subplots(figsize=(4.6, 2.6))
ax.bar(years, counts, color='#3b6ea5', label='papers per year')
ax2 = ax.twinx()
ax2.plot(years, cum, color='#c44e52', marker='o', ms=3, lw=1.2, label='cumulative')
ax.set_xlabel('Publication year')
ax.set_ylabel('Papers per year')
ax2.set_ylabel('Cumulative')
ax.set_xticks(years)
h1, l1 = ax.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, loc='upper left', fontsize=7.5, frameon=False)
fig.tight_layout()
fig.savefig(OUT + 'fig2_year_trend.png', dpi=300)
plt.close(fig)

# ---------- Fig 3: method-family evolution (stacked area share) ----------
groups = ['Classical ML', 'Deep learning', 'Physics-informed / hybrid',
          'Optimization-augmented learning', 'Transfer / domain adaptation',
          'Reinforcement / control learning', 'Foundation models / LLM']
colors = ['#7f9fc4', '#3b6ea5', '#c44e52', '#ddae57', '#55a868', '#8172b2', '#333333']
mgy = stats['method_group_by_year']
data = np.zeros((len(groups), len(years)))
for gi, g in enumerate(groups):
    for yi, y in enumerate(years):
        data[gi, yi] = mgy.get(str(y), {}).get(g, 0)
share = data / data.sum(axis=0) * 100
fig, ax = plt.subplots(figsize=(5.2, 2.9))
ax.stackplot(years, share, labels=groups, colors=colors, alpha=0.92)
ax.set_ylabel('Share of corpus (%)')
ax.set_xlabel('Publication year')
ax.set_ylim(0, 100)
ax.set_xticks(years)
ax.legend(loc='lower left', fontsize=6.4, frameon=True, framealpha=0.85, facecolor='white', edgecolor='#cccccc', ncol=2)
fig.tight_layout()
fig.savefig(OUT + 'fig3_method_evolution.png', dpi=300)
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
