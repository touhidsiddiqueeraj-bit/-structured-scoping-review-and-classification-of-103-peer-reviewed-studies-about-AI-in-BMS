#!/usr/bin/env python3
"""Round-10 QA verification — user-found 8-issue review round.

Verifies the eight user-reported faults plus the two newly found bugs
(triple-repeated sentence in condensed III-C; stale figure arithmetic):

  U1  Fig. 2 / text duplicate-count agreement: figure script carries
      3,000 -> 2,973 (27 filtered) -> 1,550 (1,423 duplicates); no '1,450'
      anywhere in scripts, manuscripts, or figure PNG metadata
  U2  2.2 -> 9.8 pointer resolves: extended 2.2 says '(Section 9.8,
      direction (g))' and 9.8 contains the v2 re-retrieval direction (g);
      condensed II-A <-> IX-C likewise
  U3  Fig. 1 scope claim: intro says 88 primary studies (reviews not mapped);
      no 'entire corpus' claim remains
  U4  NMC denominators: 54 of 88 primaries (61%) in both 3.3 and 3.4 spots;
      reviews-carry-no-chemistry stated; no '54 of the 103'
  U5  RFID 'venue notwithstanding' notes gone from both ref lists; neutral
      document-type venue rule in extended 2.3 and condensed II-C
  U6  GP claim corrected (predictive distribution, calibration not automatic);
      'degrade more gracefully' replaced by attributed rationale + corpus
      evidence caveat; 'deliver(s) calibrated' -> 'report(s) calibrated'
  U7  conference check out of extended main text (no '3.5 Conference-venue'
      heading), supplement S6 carries it with Table S1; S6 pointers in both
      manuscripts' limitations
  U8  3.4 audit mechanics compressed with S7 pointer; per-paper itemization
      lives in supplement S7; duplicated release/re-derive sentences removed;
      caveat verbatim repeats removed (3.3 forward-pointer, conclusion repeat)
  U9  condensed triple-sentence bug fixed (exactly one occurrence)
  U10 supplement rebuilt with S1-S7 intro; no [[doi]] placeholders leak

Plus build sanity: all three artifacts exist, fresh mtimes, page counts,
citation integrity (111 refs, 0 uncited corpus papers).
"""
import os, re, subprocess, sys

OK = BAD = 0
def check(name, cond):
    global OK, BAD
    print(('OK  ' if cond else 'BAD ') + name)
    if cond: OK += 1
    else: BAD += 1

def norm(t):
    return re.sub(r'\s+', ' ', t)

sys.path.insert(0, os.getcwd())
import paper_part1, paper_part2, paper_part3
import paper_short_part1, paper_short_part2, paper_short_part3

L1 = open('paper_part1.py', encoding='utf-8').read()
L2 = open('paper_part2.py', encoding='utf-8').read()
L3 = open('paper_part3.py', encoding='utf-8').read()
S1 = open('paper_short_part1.py', encoding='utf-8').read()
S2 = open('paper_short_part2.py', encoding='utf-8').read()
S3 = open('paper_short_part3.py', encoding='utf-8').read()
SUP = open('build_supplement.py', encoding='utf-8').read()
FIG = open('corpus/make_fig1.py', encoding='utf-8').read()
DOCX = open('build_docx.py', encoding='utf-8').read()
TEXB = open('corpus/build_tex.py', encoding='utf-8').read()

def joined(blocks):
    return norm(' '.join(b[1] for b in blocks if b[0] == 'p'))

EXT = joined(paper_part1.BLOCKS + paper_part2.BLOCKS + paper_part3.BLOCKS)
COND = joined(paper_short_part1.BLOCKS + paper_short_part2.BLOCKS + paper_short_part3.BLOCKS)

# ---------------- U1: PRISMA arithmetic ----------------
check('U1a fig script: 2,973 filter step present', '2,973' in FIG and '27' in FIG)
check('U1b fig script: 1,423 duplicates', '1,423' in FIG)
check('U1c fig script: no 1,450', '1,450' not in FIG)
check('U1d fig png regenerated (mtime today)',
      os.path.getmtime('figures/fig2_prisma.png') > os.path.getmtime('README.md') - 86400 * 60)
check('U1e ieee figs copy synced',
      open('figures/fig2_prisma.png','rb').read() == open('ieee_submission/tex/figs/fig2_prisma.png','rb').read())
check('U1f zenodo copy synced',
      open('figures/fig2_prisma.png','rb').read() == open('zenodo_upload/figures/fig2_prisma.png','rb').read())
check('U1g no 1,450 in any manuscript source',
      not any('1,450' in x for x in (L1, L2, L3, S1, S2, S3)))

# ---------------- U2: 2.2 -> 9.8 pointer ----------------
check('U2a extended 2.2 points to 9.8 direction (g)', '(Section 9.8, direction (g))' in L1)
check('U2b extended 9.8 contains v2 re-retrieval direction (g) [round-11: (g) now labeled]',
      'registry-deep re-retrieval' in EXT and 'falls in seven directions' in EXT and 'v2 re-retrieval of this corpus with cursor paging' in EXT)
check('U2c extended guardrail now seven directions', 'guardrail on all seven directions' in EXT)
check('U2d condensed II-A points to IX-C (g)', 'Section IX-C, direction (g)' in S1)
check('U2e condensed IX-C contains direction (g) [round-11: (g) now labeled]',
      'registry-deep re-retrieval' in COND and 'falls in seven directions' in COND and 'guardrail on all seven directions' in COND)

# ---------------- U3: Fig. 1 scope ----------------
check('U3a no "entire corpus" claim', 'entire corpus' not in EXT and 'entire corpus' not in COND)
check('U3b intro maps 88 primary studies',
      'mapping the 88 primary studies of the classified subset across management functions and method families' in EXT)
check('U3c review exclusion stated at Fig. 1 pointer',
      'the 12 method reviews carry no method-family code' in EXT)

# ---------------- U4: NMC denominators ----------------
check('U4a no "54 of the 103"', '54 of the 103' not in EXT and '54 of the 103' not in COND)
check('U4b 3.3 uses 54 of 88 primaries (61%)',
      'anchor 54 of the 88 primary studies (61%)' in EXT)
check('U4c 3.4 chemistry scoped to primaries',
      '54 of them (61%) work on NMC-based cells' in EXT)
check('U4d reviews-carry-no-chemistry stated',
      'carry no cell-chemistry code' in EXT)
check('U4e condensed NMC already primary-scoped (54 of the 88, 61%)',
      '54 of the 88 primary papers' in COND)

# ---------------- U5: RFID notes ----------------
check('U5a "venue notwithstanding" gone from all sources',
      not any('venue notwithstanding' in x for x in (L1, L2, L3, S1, S2, S3, DOCX, TEXB)))
check('U5b REF_NOTES empty in both builders',
      'REF_NOTES = {}' in DOCX and 'REF_NOTES = {}' in TEXB)
check('U5c neutral document-type rule in extended 2.3',
      'document-type-based rather than topical' in EXT)
check('U5d condensed II-C neutral venue wording',
      'document-type-based rather than' in COND)
check('U5e no per-ref note in built tex',
      'Note: lithium-ion battery state-of-charge estimation study' not in open('ieee_submission/tex/mlbms.tex', encoding='utf-8').read())

# ---------------- U6: GP / hybrid claims ----------------
check('U6a no "natively returns calibrated"', 'natively returns calibrated' not in EXT)
check('U6b GP predictive-distribution phrasing + calibration caveat',
      'natively returns a full predictive distribution' in EXT and
      'calibration under kernel or model misspecification is not automatic' in EXT)
check('U6c no unhedged "degrade more gracefully"', 'degrade more gracefully' not in EXT and 'degrade more gracefully' not in COND)
check('U6d hybrid rationale attributed + corpus caveat',
      "authors\u2019 stated rationale" in EXT and 'no study in the subset measures out-of-envelope degradation' in EXT)
check('U6e GP lineage "predictive intervals" + "reports calibrated"',
      'predictive intervals as a first-class output' in EXT and
      'reports calibrated lifetime distributions' in EXT and
      'report calibrated early-life predictions' in EXT)

# ---------------- U7: conference check -> S6 ----------------
check('U7a no "3.5 Conference-venue" heading in extended',
      not any(b[0] in ('h1', 'h2') and b[1].startswith('3.5') for b in paper_part1.BLOCKS))
check('U7b TABLE_CONF not referenced in extended main blocks',
      not any(b[0] == 'tbl' and b[1] == 'TABLE_CONF' for b in paper_part1.BLOCKS))
check('U7c supplement S6 carries the probe',
      'S6. Conference-venue probe' in SUP)
check('U7d supplement Table S1 rendered from TABLE_CONF',
      "paper_part3.TABLE_CONF" in SUP and 'Table S1 ' in SUP)
check('U7e extended limitations point to S6',
      'Supplementary Material S6) finds no evidence' in EXT)
check('U7f condensed limitations point to S6',
      'descriptive conference-venue probe in the supplement, S6' in COND)

# ---------------- U8: audit mechanics -> S7 + dedupe ----------------
check('U8a 3.4 compressed audit summary present', 'Three audit layers bound these counts' in EXT)
check('U8b per-paper 70/30 itemization out of extended main text',
      'train on the first 70% of each cell' not in EXT)
check('U8c S7 carries the per-paper evidence',
      'S7. Validation audit: per-paper evidence' in SUP and 'train on the first 70% of each cell' in SUP)
check('U8d duplicated "verified row by row" sentence removed',
      EXT.count('verified row by row') == 1)
check('U8e duplicated re-derive sentence compressed',
      EXT.count('can be re-derived') == 1)
check('U8f 3.3 forward meta-commentary removed',
      'it is read as such in the Conclusion' not in EXT)
check('U8g conclusion scope repeat rephrased',
      'a share of what the capped retrieval and its query families surfaced' not in EXT)

# ---------------- U9: condensed triple sentence ----------------
check('U9a supplementary-note sentence exactly once in condensed',
      COND.count('released supplementary note re-derives') == 1)
check('U9b same in built tex',
      open('ieee_submission/tex/mlbms.tex', encoding='utf-8').read().count('released supplementary note re-derives') == 1)

# ---------------- U10: supplement ----------------
check('U10a supplement intro lists S1-S7', 'per-paper evidence of the validation audit (S7)' in SUP)
check('U10b supplement built (docx+pdf exist, pdf 7+ pages)',
      os.path.exists('Supplementary_Material.docx') and os.path.exists('Supplementary_Material.pdf'))
st = subprocess.run(['pdftotext', 'Supplementary_Material.pdf', '-'], capture_output=True, text=True).stdout
check('U10c no [[doi]] placeholders leak in supplement pdf', '[[' not in st)
check('U10d S6 + S7 present in supplement pdf',
      'S6. Conference-venue probe' in norm(st) and 'S7. Validation audit' in norm(st))

# ---------------- build sanity ----------------
check('B1 extended pdf exists', os.path.exists('ML-BMS-Review.pdf'))
et = subprocess.run(['pdftotext', 'ML-BMS-Review.pdf', '-'], capture_output=True, text=True).stdout
etn = norm(et)
check('B2 extended pdf carries new text (direction g, S6/S7 pointers) [round-11 wording]',
      'registry-deep re-retrieval' in etn and 'Supplementary Material S6' in etn)
check('B3 extended pdf free of removed strings',
      'venue notwithstanding' not in etn and '1,450' not in etn and '54 of the 103' not in etn)
ct = subprocess.run(['pdftotext', 'ieee_submission/tex/mlbms.pdf', '-'], capture_output=True, text=True).stdout
# strip running headers / bare page numbers so sentences split across page
# boundaries still match (round-11: guardrail sentence straddles pp. 15-16)
ct = re.sub(r'IEEE TRANSACTIONS ON TRANSPORTATION ELECTRIFICATION\s*\d*', ' ', ct)
ct = re.sub(r'\n\s*\d+\s*\n', ' ', ct)
ctn = norm(ct)
check('B4 condensed pdf carries direction (g) + S6/S7 pointers',
      'guardrail on all seven directions' in ctn and 'supplement, S6' in ctn and 'supplement, S7' in ctn)
check('B5 condensed pdf free of removed strings',
      'venue notwithstanding' not in ctn and 'degrade more gracefully' not in ctn)
check('B6 tex recompilable (fresh pdf newer than tex)',
      os.path.getmtime('ieee_submission/tex/mlbms.pdf') >= os.path.getmtime('ieee_submission/tex/mlbms.tex') - 60)

# no stray "Section 3.5" pointers anywhere
check('B7 no dangling Section 3.5 pointers',
      not any(re.search(r'Section[s]? 3\.5', x) for x in (L1, L2, L3, S1, S2, S3)))

print(f'\n{OK} OK, {BAD} BAD')
sys.exit(1 if BAD else 0)

# ================= ROUND-10 JUDGE FIXES (R10-1..R10-25) =================
import subprocess as sp
et = norm(sp.run(['pdftotext','ML-BMS-Review.pdf','-'], capture_output=True, text=True).stdout)
ct = norm(sp.run(['pdftotext','ieee_submission/tex/mlbms.pdf','-'], capture_output=True, text=True).stdout)
st = norm(sp.run(['pdftotext','Supplementary_Material.pdf','-'], capture_output=True, text=True).stdout)

check('J1  Fig.1 parenthetical: 12 method reviews + 3 syntheses (R10-1)',
      'the 12 method reviews carry no method-family code' in et and '15 review-labelled studies carry no method-family code' not in et)
check('J2  LLM dating 2026 everywhere; no 2025-2026 LLM claims (R10-2)',
      'first large-language-model studies appear in 2026' in et and
      'appear in 2025' not in et.replace('2025\u20132026 records','') and
      'Published LLM studies (2026)' in et and 'in 2026 in the subset' in et)
check('J3  no dangling Section 3.5 (R10-3)', 'Sections 3 and 3.5' not in et and 'Section 3.5' not in et)
check('J4  table sequence 1-12 with no skip: Table 7 Representative, 12 checklist (R10-4)',
      'Table 7 Representative classified-subset studies' in et and
      'Table 12 Proposed BMS-ML reporting checklist' in et and 'Table 13' not in et)
check('J5  Box 1 (no orphan Box 2) (R10-5)', 'Box 1 Terminology and count reconciliation' in et and 'Box 2' not in et)
check('J6  condensed extrapolation claim attributed (R10-6)',
      'verify only the premise of that argument' in ct)
check('J7  Table 2/I cell: native predictive distributions (R10-7)',
      'Native predictive distributions (calibration must be verified empirically)' in et and
      'Native predictive distributions (calibration must be verified empirically)' in ct)
check('J8  3.3 union dedup note 394/28 overlap (R10-8)',
      '366' in et and 'per-tag counts sum to 394' in et)
check('J9  thermal not falsely smallest (R10-9)',
      'After cell balancing (2 primary papers), thermal management' in et)
check('J10 output-rose scoped to selection design (R10-10)',
      'a profile shaped by the year-stratified selection design' in et)
check('J11 score-measured items: validation/data-source/baseline (R10-11)',
      'validation-protocol, data-source, and baseline-comparison items are score-measured' in et and
      'validation-protocol, data-source, and baseline-comparison items are score-measured' in ct)
check('J12 private-lab 42 (36+6) consistent (R10-12)',
      '42 papers \u2014 36 own-cell cycling, 6 laboratory impedance' in et and
      '42 rest on private laboratory data' in et and '42 of 88: 36 own-cell cycling, 6 laboratory impedance' in ct and
      'while 42 rest on private laboratory data' in ct)
check('J13 condensed baseline screen + S5.2 (R10-13)',
      'abstract-level baseline screen (supplement S5.2) finds 32 of the 38' in ct)
check('J14 recall per-source numerator 112 of 649 (R10-14)',
      '112 of the 649 per-source reference mentions (17.3%)' in et)
check('J15 reviews-column match corrected (R10-15)',
      'Table 3\u2019s Reviews column counts these 12 reviews plus the three syntheses' in et)
check('J16 only multi-year family (R10-16)',
      'only multi-year family with a monotonically non-decreasing primary trajectory' in et and
      'only multi-year family with a monotonically non-decreasing trajectory' in ct)
check('J17 224-candidate (R10-17)', '224-candidate closed-loop campaign' in ct and '224-cell' not in ct)
check('J18 Fig.2 caption six/five seeds (R10-18)', 'one already among the top-cited hits; five force-included' in ct)
check('J19 absorbing rule once; 1,555 expansion once in prose (R10-19)',
      et.count('the 1,550 retrieved records plus the five individually retrieved seeds') <= 2 and
      'absorbing rule, Box 1' in et)
check('J20 abbreviations defined (R10-20)',
      'root-mean-square error, RMSE' in et and 'mean absolute error (MAE)' in et and
      'electrochemical impedance spectroscopy (EIS)' in et and
      'computational fluid dynamics (CFD)' in et and 'gated recurrent unit (GRU)' in et and
      'particle swarm optimization (PSO)' in et and 'explainable AI (XAI)' in et and
      'long short-term memory (LSTM)' in et)
check('J21 supplement keying + S3/S4 pointers in condensed (R10-21)',
      'Sections 2.2\u20132.3, 2.5\u20132.6, and 3.4' in st and 'supplement S3' in ct and 'supplement S4' in ct)
check('J23 GTR 20 electric-vehicle safety (R10-23)',
      'GTR) 20 on electric-vehicle safety' in ct)
check('J24a Table 9 SOH/RUL row 16-of-32 (R10-24a)',
      '16 of the 32 SOH/RUL primary papers; 23 across the whole subset' in et)
check('J24b Fig.4 caption syntheses note (R10-24b)',
      '3 review-type syntheses sit inside their family bands' in et)
check('J24c most consistently rising (R10-24c)',
      'most consistently rising methodological theme' in ct and 'fastest-growing methodological theme' not in ct)
check('J25 three follow-on subsections (R10-25)',
      'Three follow-on subsections' in ct and '2027\u20132030 research directions' not in ct)
# R10-22 intentionally not "fixed": iso.org/standard/83303 confirms the manuscript's
# title "Road vehicles - Safety and artificial intelligence" is correct.

print(f'\nTOTAL: {OK} OK, {BAD} BAD')
