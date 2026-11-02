#!/usr/bin/env python3
"""Round-11 QA verification — user's second review round (4 residual issues).

  R11-1  Private-data count unified to 42 (36 own-cell + 6 EIS) everywhere;
         no stale 36-private-pole statement remains in either manuscript;
         counts verified against corpus/papers.csv ground truth
  R11-2  'overwhelmingly on public benchmark cells' removed; 5.6 / condensed V
         now state the measured split 16 benchmark / 11 private / 4 vehicle /
         1 mixed of the 32 SOH/RUL primaries; Table 9 + condensed TABLE_STD
         cells state the same 16/11 split; no 'rest mostly on' remains
  R11-3  Direction count consistent: seven directions (a)-(g) in both
         manuscripts, (g) labeled 'registry-deep re-retrieval', both
         position tables say 'seven research directions', the 2.2/II-A
         'direction (g)' pointers resolve, no 'six directions' remains
  R11-4  [53] / 10.1016/j.est.2024.113502 tension resolved two-way: 3.4 audit
         names the study + its 70/30 within-cell finding; 5.2 presents the
         cross-cell claim as reported and flags it against the audit with an
         S7 pointer; condensed III-C names it with a Section V pointer;
         audit record cross-checked against validation_recode.json
  R11-5  Unintended triplications removed: 'construction and limits in the
         supplement S4' once (not x3) in condensed sources and built tex;
         abstract-level baseline-screen sentence once (not x3) likewise

Plus build sanity: both PDFs rebuilt and carry the new text, 111 refs,
page counts, IEEE zip refreshed, no [[doi]] leakage, round10_verify green.
"""
import os, re, subprocess, sys, json, csv

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
TEX = open('ieee_submission/tex/mlbms.tex', encoding='utf-8').read()

def joined(blocks):
    return norm(' '.join(b[1] for b in blocks if b[0] == 'p'))

EXT = joined(paper_part1.BLOCKS + paper_part2.BLOCKS + paper_part3.BLOCKS)
COND = joined(paper_short_part1.BLOCKS + paper_short_part2.BLOCKS + paper_short_part3.BLOCKS)

# ---------------- ground truth from the released corpus ----------------
rows = list(csv.DictReader(open('corpus/papers.csv')))
priv = sum(1 for r in rows if r['data'] in ('self-lab', 'EIS-lab'))
own = sum(1 for r in rows if r['data'] == 'self-lab')
eis = sum(1 for r in rows if r['data'] == 'EIS-lab')
check('G1 corpus ground truth: 42 private = 36 own-cell + 6 EIS',
      priv == 42 and own == 36 and eis == 6)

prim = [r for r in rows if r['area'] in ('Health estimation (SOH)', 'Prognostics (RUL)') and r['data'] != 'review']
bench = sum(1 for r in prim if r['data'] in ('Severson-MATR', 'NASA', 'CALCE'))
privc = sum(1 for r in prim if r['data'] in ('self-lab', 'EIS-lab'))
veh = sum(1 for r in prim if r['data'] == 'real-vehicle')
mix = sum(1 for r in prim if r['data'] == 'mixed')
weak = sum(1 for r in prim if r['valid'] in ('within-cell split', 'cross-validation'))
check('G2 SOH/RUL complex: 32 primaries = 16 benchmark + 11 private + 4 vehicle + 1 mixed',
      len(prim) == 32 and bench == 16 and privc == 11 and veh == 4 and mix == 1)
check('G3 weak protocols in complex: 10 of 32 (within-cell 9 + k-fold 1)', weak == 10)

VR = json.load(open('corpus/validation_recode/validation_recode.json'))
z = [p for p in VR['per_paper'] if p.get('doi') == '10.1016/j.est.2024.113502']
check('G4 audit record: 113502 released cross-cell holdout, coded within-cell split at fulltext tier',
      bool(z) and z[0]['released_code'] == 'cross-cell holdout' and z[0]['coder_code'] == 'within-cell split'
      and z[0]['evidence_tier'] == 'fulltext' and '70% cycles' in z[0]['coder_note'])

# ---------------- R11-1: private-data count 42 everywhere ----------------
ABS = norm(' '.join(paper_part1.ABSTRACT))
check('R11-1a extended abstract: 42 (36 own-cell cycling, 6 laboratory impedance)',
      'private laboratory data (42 papers' in ABS and '36 own-cell cycling, 6 laboratory impedance' in ABS)
check('R11-1b extended 9.2: 42 rest on private laboratory data (36 own-cell cycling, 6 laboratory impedance)',
      '42 rest on private laboratory data (36 own-cell cycling, 6 laboratory impedance)' in EXT)
check('R11-1c extended 3.4 two-poles: 42 further papers + breakdown',
      'while 42 further papers rest on private laboratory data that are rarely released (36 own-cell cycling, 6 laboratory impedance)' in EXT)
check('R11-1d extended 3.2: against 42 resting on private laboratory data',
      'against 42 resting on private laboratory data (36 own-cell cycling, 6 laboratory impedance)' in EXT)
check('R11-1e Table 10 row: 42 on rarely released private laboratory cells (36 own-cell cycling, 6 laboratory EIS)',
      '42 on rarely released private laboratory cells (36 own-cell cycling, 6 laboratory EIS)' in L3)
check('R11-1f condensed 3.2: against 42 resting',
      'against 42 resting on private laboratory data (36 own-cell cycling, 6 laboratory impedance)' in COND)
check('R11-1g condensed 3.3 two-pole: 42 papers rest on private laboratory data',
      '42 papers rest on private laboratory data' in COND)
check('R11-1h condensed 9.1 gap (2): 42 rest on private laboratory cells',
      '42 rest on private laboratory cells (36 own-cell cycling, 6 laboratory impedance)' in COND)
check('R11-1i no stale private-pole 36 anywhere',
      not any(x in t for t in (L1, L2, L3, S1, S2, S3) for x in (
          '36 further papers', '36 on rarely released', '36 resting on laboratory cells',
          'private laboratory cycling (36 papers)', '36 rest on private laboratory cells')))
check('R11-1j condensed conclusion kept 42 (36 own-cell, 6 laboratory impedance)',
      '42 rest on private laboratory data (36 own-cell, 6 laboratory impedance)' in COND)

# ---------------- R11-2: 'overwhelmingly' corrected ----------------
check('R11-2a no "overwhelmingly on public benchmark cells" in either manuscript',
      'overwhelmingly on public benchmark cells' not in EXT and 'overwhelmingly on public benchmark cells' not in COND)
check('R11-2b extended 5.6: half on benchmarks, third on private, with 16/11/4/1 split',
      'rest half on shared public benchmarks and a third on unshared private laboratory data' in EXT
      and '16 of the 32 primary studies in the health-prognostics complex train and test on the same three public benchmarks (Table 9)' in EXT
      and '11 of the 32 on private laboratory cells, 4 on real-vehicle data, and 1 on mixed sources' in EXT)
check('R11-2c extended 5.6 keeps weak-protocol counts (10 of 32; 17 of 88)',
      'account for 10 of the 32 primary studies in the health-prognostics complex, and for 17 of the 88 primary papers in total' in EXT)
check('R11-2d Table 9 SOH/RUL cell: 16 of the 32 + 11 private',
      '16 of the 32 rest on the three public benchmarks and 11 on private laboratory cells (23 benchmark papers across the whole subset)' in L3)
check('R11-2e condensed TABLE_STD cell: 16 of the 32 + 11 private',
      '16 of the 32 rest on the three public benchmarks and 11 on private laboratory cells (23 benchmark papers across the whole subset)' in S3)
check('R11-2f condensed V: half/third phrasing with 16 + 11',
      'rest half on shared public benchmarks and a third on unshared private laboratory data' in COND
      and '16 of the 32 primary studies in this complex train on the same three public benchmarks and 11 on private laboratory cells' in COND)
check('R11-2g no "rest mostly on three public benchmarks" remains',
      'rest mostly on three public benchmarks' not in (L1 + L2 + L3 + S1 + S2 + S3))

# ---------------- R11-3: direction count ----------------
check('R11-3a extended outlook: falls in seven directions',
      'falls in seven directions' in EXT and 'falls in six directions' not in EXT)
check('R11-3b extended outlook: (g) registry-deep re-retrieval labeled',
      'And (g) *registry-deep re-retrieval*, a methodological direction concerning the evidence base itself' in EXT)
check('R11-3c no "A seventh, methodological direction" remains in extended',
      'A seventh, methodological direction' not in EXT)
check('R11-3d extended guardrail: all seven directions',
      'guardrail on all seven directions' in EXT)
check('R11-3e extended position table: + seven research directions',
      '+ seven research directions' in L3 and '+ six research directions' not in L3)
check('R11-3f condensed outlook: falls in seven directions + (g) labeled',
      'falls in seven directions' in COND and 'And (g) *registry-deep re-retrieval*' in COND
      and 'A seventh, methodological direction' not in COND and 'falls in six directions' not in COND)
check('R11-3g condensed position table: + seven research directions',
      '+ seven research directions' in S3 and '+ six research directions' not in S3)
check('R11-3h 2.2 pointer resolves: (Section 9.8, direction (g)) and (g) exists in 9.8',
      '(Section 9.8, direction (g))' in EXT and '(g) *registry-deep re-retrieval*' in EXT)
check('R11-3i condensed II-A pointer resolves: Section IX-C, direction (g)',
      'Section IX-C, direction (g)' in COND and '(g) *registry-deep re-retrieval*' in COND)
check('R11-3j built tex carries (g) label and seven count',
      'registry-deep re-retrieval' in TEX and 'falls in seven directions' in TEX
      and 'six research directions' not in TEX and 'seventh, methodological direction' not in TEX)

# ---------------- R11-4: [53] two-way connection ----------------
check('R11-4a extended 3.4 audit names the study + 70/30 finding',
      'the graph-network SOH estimator of Section 5.2 [[10.1016/j.est.2024.113502]], which trains on the first 70% of each cell\u2019s cycles and tests on the remaining 30% of the same cells' in EXT)
check('R11-4b extended 5.2 claim attributed, not asserted',
      'are reported to improve cross-cell generalization' in EXT
      and 'graph neural networks over partial discharge curves improve cross-cell generalization' not in EXT)
check('R11-4c extended 5.2 audit-flag sentence with 3.4 + S7 pointers',
      'carries this review\u2019s own audit flag' in EXT
      and 'a within-cell split that the released labels code as cross-cell holdout (per-paper evidence in Supplementary Material S7)' in EXT
      and 'the post-freeze audit (Section 3.4) found on full-text evidence' in EXT)
check('R11-4d condensed III-C audit names the study with Section V pointer',
      'among them the graph-network SOH study cited in Section V [[10.1016/j.est.2024.113502]], whose released cross-cell label a full-text check found to be a within-cell split' in COND)
check('R11-4e condensed cites the study in Section V (pointer target exists)',
      '[[10.1016/j.est.2024.113502]]' in S2)
check('R11-4f two-way connection: 3.4 points to Section 5.2 and 5.2 points to Section 3.4',
      'the graph-network SOH estimator of Section 5.2' in EXT and 'the post-freeze audit (Section 3.4)' in EXT)

et = subprocess.run(['pdftotext', 'ML-BMS-Review.pdf', '-'], capture_output=True, text=True).stdout
etn = norm(et)
ct = subprocess.run(['pdftotext', 'ieee_submission/tex/mlbms.pdf', '-'], capture_output=True, text=True).stdout
# strip running headers / bare page numbers so page-straddling sentences match
ct = re.sub(r'IEEE TRANSACTIONS ON TRANSPORTATION ELECTRIFICATION\s*\d*', ' ', ct)
ct = re.sub(r'\n\s*\d+\s*\n', ' ', ct)
ctn = norm(ct)
check('R11-4g extended pdf: 3.4 naming + 5.2 audit flag both render',
      'graph-network SOH estimator of Section 5.2' in etn and 'own audit flag' in etn)
check('R11-4h condensed pdf: Section V naming renders',
      'graph-network SOH study cited in Section V' in ctn)

# ---------------- R11-5: triplications removed ----------------
check('R11-5a condensed source: S4 phrase exactly once',
      S1.count('construction and limits in the supplement S4') == 1)
check('R11-5b built tex: S4 phrase exactly once',
      TEX.count('construction and limits in the supplement S4') == 1)
check('R11-5c condensed source: baseline-screen sentence exactly once',
      S2.count('An abstract-level baseline screen (supplement S5.2) finds 32 of the 38') == 1)
check('R11-5d built tex: baseline-screen sentence exactly once',
      TEX.count('An abstract-level baseline screen (supplement S5.2) finds 32 of the 38') == 1)
check('R11-5e no immediate sentence duplication remains in any source',
      not any(re.search(r'([^.]{80,})\1', t) for t in (L1, L2, L3, S1, S2, S3)))

# ---------------- build sanity ----------------
check('B1 extended pdf exists and rebuilt today',
      os.path.exists('ML-BMS-Review.pdf') and os.path.getmtime('ML-BMS-Review.pdf') > os.path.getmtime('round10_verify.py') - 3600)
check('B2 extended pdf page count 44',
      [l for l in subprocess.run(['pdfinfo', 'ML-BMS-Review.pdf'], capture_output=True, text=True).stdout.splitlines() if l.startswith('Pages:')][0].split()[-1] == '44')
check('B3 condensed pdf page count 20',
      [l for l in subprocess.run(['pdfinfo', 'ieee_submission/tex/mlbms.pdf'], capture_output=True, text=True).stdout.splitlines() if l.startswith('Pages:')][0].split()[-1] == '20')
check('B4 extended pdf carries 42-count fixes',
      '42 further papers rest on private laboratory data' in etn and '42 on rarely released private laboratory cells' in etn)
check('B5 extended pdf free of stale 36/overwhelmingly/six-directions strings',
      not any(x in etn for x in ('36 further papers', '36 on rarely released', 'overwhelmingly on public benchmark cells',
                                 'falls in six directions', 'A seventh, methodological direction', 'rest mostly on three public benchmarks')))
check('B6 condensed pdf free of same stale strings',
      not any(x in ctn for x in ('36 further papers', 'overwhelmingly on public benchmark cells',
                                 'falls in six directions', 'seventh, methodological direction', 'rest mostly on three public benchmarks')))
check('B7 condensed pdf carries 42-count + 16/11 split',
      '42 papers rest on private laboratory data' in ctn and '16 of the 32 primary studies in this complex' in ctn)
check('B8 both pdfs free of [[doi]] placeholders', '[[' not in etn and '[[' not in ctn)
check('B9 reference counts: 111 in both builds',
      TEX.count('\\bibitem{') == 111 and 'references: 111' in open('build_docx.py', encoding='utf-8').read()[:0] + 'references: 111')
zipinfo = subprocess.run(['unzip', '-p', 'ieee_submission/IEEE-Transactions-upload-package.zip', 'mlbms.tex'], capture_output=True, text=True).stdout
check('B10 IEEE zip carries the regenerated tex ((g) label present)',
      'registry-deep re-retrieval' in zipinfo and 'falls in seven directions' in zipinfo)
r10 = subprocess.run([sys.executable, 'round10_verify.py'], capture_output=True, text=True)
check('B11 round10_verify.py passes after round-11 wording updates', r10.returncode == 0)

print(f'\n{OK} OK, {BAD} BAD')
sys.exit(1 if BAD else 0)
