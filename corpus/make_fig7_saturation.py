#!/usr/bin/env python3
"""Fig 7: benchmark-dataset saturation — reuse of the three dominant public
benchmarks per year against total corpus output per year."""
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

plt.rcParams.update({
    'font.family': 'serif', 'font.serif': ['DejaVu Serif', 'Liberation Serif'],
    'font.size': 9, 'figure.dpi': 300,
})
C = json.load(open('/home/touhid/Documents/reviewpaper/corpus/papers_final.json'))
years = list(range(2019, 2027))
BENCH = [('Severson-MATR', '#3b6ea5', 'Severson/Toyota (MATR)'),
         ('NASA', '#c44e52', 'NASA PCoE'),
         ('CALCE', '#ddae57', 'CALCE')]
per = {k: Counter(r['year'] for r in C if r['data'] == k) for k, _, _ in BENCH}
tot = Counter(r['year'] for r in C)

fig, ax = plt.subplots(figsize=(5.2, 2.9))
bottom = np.zeros(len(years))
for k, color, label in BENCH:
    vals = np.array([per[k].get(y, 0) for y in years], dtype=float)
    ax.bar(years, vals, bottom=bottom, color=color, label=label, width=0.62)
    bottom += vals
ax2 = ax.twinx()
tot_line = [tot.get(y, 0) for y in years]
ax2.plot(years, tot_line, color='#37352F', marker='o', ms=3.5, lw=1.2,
         label='All corpus papers (right axis)')
ax.set_ylabel('Papers using the three dominant benchmarks')
ax2.set_ylabel('All corpus papers')
ax.set_xticks(years)
ax.set_ylim(0, 8)
ax2.set_ylim(0, max(tot_line) * 1.18)
h1, l1 = ax.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, loc='upper left', fontsize=6.8, frameon=True,
          framealpha=0.9, facecolor='white', edgecolor='#cccccc')
fig.tight_layout()
fig.savefig('/home/touhid/Documents/reviewpaper/figures/fig7_dataset_saturation.png', dpi=300)
print('fig7 done; benchmark papers/year:', {y: int(bottom[i]) for i, y in enumerate(years)})
print('totals/year:', tot_line)
print('benchmark total:', sum(int(bottom[i]) for i in range(len(years))))
