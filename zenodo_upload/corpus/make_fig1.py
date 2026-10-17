#!/usr/bin/env python3
"""Fig 2: PRISMA-style study-selection flowchart (true funnel arithmetic)."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams.update({'font.family': 'serif', 'font.serif': ['DejaVu Serif'], 'font.size': 8})
fig, ax = plt.subplots(figsize=(5.8, 4.6))

def box(x, y, w, h, lines, bold_first=True, fc='#f0f4f9'):
    b = FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.012', fc=fc, ec='#3b6ea5', lw=0.9)
    ax.add_patch(b)
    n = len(lines)
    for i, t in enumerate(lines):
        weight = 'bold' if (i == 0 and bold_first) else 'normal'
        ax.text(x + w / 2, y + h - (i + 0.55) * h / (n + 0.35), t,
                ha='center', va='center', fontsize=8.0, weight=weight)

def arrow(x, y1, y2):
    ax.add_patch(FancyArrowPatch((x, y1), (x, y2), arrowstyle='-|>',
                                 mutation_scale=9, lw=0.9, color='#3b6ea5'))

W, H = 0.64, 0.098
XL = 0.04
YS = [0.945, 0.795, 0.645, 0.495, 0.345, 0.195, 0.045]
B = [
    (['Records identified through CrossRef API queries', 'n = 3,000'], '#e3ebf5'),
    (['Records screened after duplicate removal', 'n = 1,550'], None),
    (['Relevance screening (battery AND ML terms in title)', 'n = 883'], None),
    (['Venue and document-type screening \u2192 TIER 1: eligible corpus,', 'rule-based, no quotas (every record included)', 'n = 799'], None),
    (['TIER 2: full-text classification of a curated subset', 'with landmark studies deliberately force-included', 'n = 103 classified'], None),
    (['Two-tier synthesis: measured bibliometrics (Tier 1) and', 'in-depth validation audit (Tier 2)'], '#f7f7f7'),
]
for (y, (lines, fc)) in zip(YS, B):
    box(XL, y, W, H, lines, fc=fc or '#f0f4f9')
for y_top, y_bot in zip(YS[:-1], YS[1:]):
    arrow(XL + W / 2, y_top, y_bot + H)

XR, xw = 0.73, 0.26
excl = [
    (0.795, 'Duplicates removed\nn = 1,450'),
    (0.645, 'Off-topic records excluded\nn = 667'),
    (0.495, 'Non-journal venues excluded\nn = 84'),
    (0.345, 'Not carried into full-text coding\n(screened pool retained verbatim;\n6 landmark studies force-included;\nsee screening_log.csv)'),
]
for y, t in excl:
    ax.text(XR + xw / 2, y + 0.035, t, ha='center', va='center', fontsize=7.6, color='#7a3b3b')
    ax.add_patch(FancyArrowPatch((XL + W, y + 0.045), (XR, y + 0.035),
                                 arrowstyle='-', lw=0.7, color='#999999'))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')
fig.tight_layout()
fig.savefig('figures/fig2_prisma.png', dpi=300)
print('fig2 regenerated')
