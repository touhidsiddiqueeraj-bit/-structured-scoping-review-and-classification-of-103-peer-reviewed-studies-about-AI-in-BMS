#!/usr/bin/env python3
"""Fig 2: PRISMA-style study-selection flowchart (matches Section 2.3).

Funnel (verified against screening_log.csv and selection2.json):
  3,000 retrieved -> 1,550 deduplicated (1,450 duplicates removed)
  -> 883 title-gate retained (667 excluded)
  -> 799 venue-eligible (84 excluded) = rule-based Tier-1 pool, no quotas
  -> stratified draw of 107 (functions x years, citation-ranked within strata)
     + 5 landmark seeds retrieved individually = 112 candidates
  -> full-text curation: -19 (corrigenda, misindexed, scope mismatches,
     quota trims) +10 targeted additions = 103 classified
     (= 98 drawn from the pool + 5 seeds).
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   'figures', 'fig2_prisma.png')

plt.rcParams.update({'font.family': 'serif', 'font.serif': ['DejaVu Serif'], 'font.size': 8})
fig, ax = plt.subplots(figsize=(6.4, 5.2))

def box(x, y, w, h, lines, bold_first=True, fc='#f0f4f9'):
    b = FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.008', fc=fc, ec='#3b6ea5', lw=0.9)
    ax.add_patch(b)
    n = len(lines)
    for i, t in enumerate(lines):
        weight = 'bold' if (i == 0 and bold_first) else 'normal'
        ax.text(x + w / 2, y + h - (i + 0.56) * h / (n + 0.28), t,
                ha='center', va='center', fontsize=7.2, weight=weight)

def arrow(x, y1, y2):
    ax.add_patch(FancyArrowPatch((x, y1), (x, y2), arrowstyle='-|>',
                                 mutation_scale=9, lw=0.9, color='#3b6ea5'))

W = 0.63
XL = 0.03
# (y, height, lines, facecolor) — multi-line boxes get extra height so that
# per-line spacing stays >= ~7pt at 7.2pt font (axes height ~4.2 in)
BOXES = [
    (0.945, 0.085, ['Records identified through Crossref API queries', 'n = 3,000'], '#e3ebf5'),
    (0.812, 0.085, ['Records screened after duplicate removal', 'n = 1,550'], None),
    (0.679, 0.085, ['Relevance screening (battery AND ML terms in title)', 'n = 883'], None),
    (0.546, 0.085, ['Venue and document-type screening:', 'Tier-1 eligible pool \u2014 rule-based,', 'no quotas  n = 799'], None),
    (0.368, 0.130, ['Stratified selection from the pool:', '107 drawn balancing functions and years', '(citation-ranked within strata)', '+ 5 landmark seeds retrieved individually', 'n = 112 candidates'], None),
    (0.205, 0.115, ['Full-text curation: \u2212 19 (corrigenda, misindexed,', 'scope mismatches, quota trims)', '+ 10 targeted additions', 'n = 103 classified (98 pool + 5 seeds)'], None),
    (0.072, 0.085, ['Released evidence base: Tier-1 pool (799,', 'quota-free tag baselines) + classified', 'subset (103; full-text coding)'], '#f7f7f7'),
]
for (y, h, lines, fc) in BOXES:
    box(XL, y, W, h, lines, fc=fc or '#f0f4f9')
for (y1, _, _, _), (y2, h2, _, _) in zip(BOXES[:-1], BOXES[1:]):
    arrow(XL + W / 2, y1, y2 + h2)

XR, xw = 0.71, 0.28
excl = [
    (0.812, 'Duplicates removed\nn = 1,450'),
    (0.679, 'Off-topic records excluded\nn = 667'),
    (0.546, 'Non-journal venues\nexcluded  n = 84'),
    (0.368, '701 eligible records not\ncarried into full-text coding\n(retained verbatim in the\nreleased Tier-1 pool)'),
    (0.205, '19 excluded; 10 added\nfor under-represented\nthemes (net \u2212 9)'),
]
for y, t in excl:
    ax.text(XR + xw / 2, y + 0.035, t, ha='center', va='center', fontsize=6.4, color='#7a3b3b')
    ax.add_patch(FancyArrowPatch((XL + W, y + 0.045), (XR, y + 0.037),
                                 arrowstyle='-', lw=0.7, color='#999999'))
ax.set_xlim(0, 1.02)
ax.set_ylim(0, 1.05)
ax.axis('off')
fig.tight_layout()
fig.savefig(OUT, dpi=300)
print('fig2 (PRISMA funnel) regenerated ->', OUT)
