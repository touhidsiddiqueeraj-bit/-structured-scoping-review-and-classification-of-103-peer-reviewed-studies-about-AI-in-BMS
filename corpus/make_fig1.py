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
                ha='center', va='center', fontsize=7.3, weight=weight)

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
    (['Venue and document-type screening', '(journal articles only; conference', 'abstracts, preprints excluded) n = 799'], None),
    (['Function-quota candidate selection, plus 6 landmark seed', 'studies (1 already captured by the searches, 5 injected)', 'n = 107 + 6 = 113 candidates'], None),
    (['Full-text assessment and corpus curation', '19 exclusions offset by 15 targeted additions from', 'the screened pool (net \u22124) \u2192 n = 103 studies included'], '#e3ebf5'),
    (['Integrated bibliometric synthesis and', 'qualitative critical review'], '#f7f7f7'),
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
    (0.345, 'Not selected under function quotas\nn = 692'),
    (0.195, 'Excluded during curation n = 19;\ntargeted additions from the\nscreened pool n = +15 (net \u22124)'),
]
for y, t in excl:
    ax.text(XR + xw / 2, y + 0.035, t, ha='center', va='center', fontsize=7.0, color='#7a3b3b')
    ax.add_patch(FancyArrowPatch((XL + W, y + 0.045), (XR, y + 0.035),
                                 arrowstyle='-', lw=0.7, color='#999999'))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')
fig.tight_layout()
fig.savefig('/home/touhid/Documents/reviewpaper/figures/fig2_prisma.png', dpi=300)
print('fig2 regenerated')
