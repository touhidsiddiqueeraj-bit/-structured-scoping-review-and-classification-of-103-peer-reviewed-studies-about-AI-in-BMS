#!/usr/bin/env python3
"""New Fig 1: corpus heatmap — management function x method family."""
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['DejaVu Serif', 'Liberation Serif'],
    'font.size': 9,
    'figure.dpi': 300,
})

corpus = json.load(open('/home/touhid/Documents/reviewpaper/corpus/papers_final.json'))
stats = json.load(open('/home/touhid/Documents/reviewpaper/corpus/stats.json'))
GROUP = stats['group_of']

FUNCS = ['State estimation (SOC)', 'Health estimation (SOH)', 'Prognostics (RUL)',
         'Charging control', 'Thermal management', 'Fault & safety',
         'Cell balancing & ECM', 'Cross-cutting']
COLS = ['Classical ML', 'Deep learning', 'Physics-informed / hybrid',
        'Optimization-augmented learning', 'Transfer / domain adaptation',
        'Reinforcement / control learning', 'Foundation models / LLM']
SHORT = {'Classical ML': 'Classical ML', 'Deep learning': 'Deep learning',
         'Physics-informed / hybrid': 'Physics-informed / hybrid',
         'Optimization-augmented learning': 'Optimization-augmented',
         'Transfer / domain adaptation': 'Transfer learning',
         'Reinforcement / control learning': 'RL / control',
         'Foundation models / LLM': 'Foundation / LLM'}
FSHORT = {'State estimation (SOC)': 'State estimation (SOC)',
          'Health estimation (SOH)': 'Health estimation (SOH)',
          'Prognostics (RUL)': 'Prognostics (RUL)',
          'Charging control': 'Charging control',
          'Thermal management': 'Thermal management',
          'Fault & safety': 'Fault & safety',
          'Cell balancing & ECM': 'Cell balancing & ECM',
          'Cross-cutting': 'Cross-cutting'}

M = np.zeros((len(FUNCS), len(COLS)))
for r in corpus:
    if r['method'] == 'Review / perspective':
        continue
    M[FUNCS.index(r['area']), COLS.index(GROUP[r['method']])] += 1

fig, ax = plt.subplots(figsize=(7.2, 3.0))
im = ax.imshow(M, cmap='Blues', aspect='auto', vmin=0, vmax=M.max())
ax.set_xticks(range(len(COLS)))
ax.set_xticklabels([SHORT[c] for c in COLS], fontsize=7.5, rotation=20, ha='right')
ax.set_yticks(range(len(FUNCS)))
ax.set_yticklabels([FSHORT[f] for f in FUNCS], fontsize=7.5)
for i in range(len(FUNCS)):
    for j in range(len(COLS)):
        v = int(M[i, j])
        if v:
            ax.text(j, i, str(v), ha='center', va='center', fontsize=7.5,
                    color='white' if v > M.max() * 0.55 else '#1a3a5c',
                    fontweight='bold' if v >= 8 else 'normal')
# row totals on the right
for i, f in enumerate(FUNCS):
    ax.text(len(COLS) - 0.35, i, f'={int(M[i].sum())}', ha='left', va='center',
            fontsize=7, color='#555555')
ax.set_xlim(-0.5, len(COLS) + 0.35)
cb = fig.colorbar(im, ax=ax, shrink=0.85, pad=0.06)
cb.set_label('Papers', fontsize=7.5)
cb.ax.tick_params(labelsize=7)
ax.set_xticks(np.arange(-0.5, len(COLS), 1), minor=True)
ax.set_yticks(np.arange(-0.5, len(FUNCS), 1), minor=True)
ax.grid(which='minor', color='white', linewidth=1.2)
ax.tick_params(which='minor', length=0)
fig.tight_layout()
fig.savefig('/home/touhid/Documents/reviewpaper/figures/fig1_function_method_map.png', dpi=300)
print('heatmap done; totals:', {f: int(M[i].sum()) for i, f in enumerate(FUNCS)},
      '| primary papers:', int(M.sum()))
