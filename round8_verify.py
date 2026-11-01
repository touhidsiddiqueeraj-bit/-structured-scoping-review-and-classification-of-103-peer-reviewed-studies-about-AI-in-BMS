#!/usr/bin/env python3
"""Round-8 QA verification — reliability round 2 propagated into the manuscripts.

Carries forward the round-7 checks (P1-P8; the P7 re-coding qualifiers and the
page-count check updated for the two-round language and the 46-pp extended
PDF) and adds the round-2 section:

  R2-A  round-2 agreement artifacts: B-C kappas, alphas (0.92-1.00), bucket
        28/30, vs-gold mechanically capped (10 v1.1-only-code papers,
        16 broader-chem), 4 residual dispute cells, locked-sheet hashes
  R2-B  byte-identical regeneration of both agreement reports
  R2-C  gold-state reconciliation (deposited corrected gold is canonical)
  R2-D  extended manuscript: abstract, contributions, 2.5 round-2 paragraph,
        limitations, 3.4 additions, conclusion
  R2-E  condensed manuscript: contributions, II-C round-2 passage, III,
        conclusion; round-1 bucket kappa 0.51 -> 0.52
  R2-F  PDFs: both manuscripts + supplement carry the round-2 numbers
  R2-G  README headline + contents + AI disclosure
plus: corpus consistency check, build sanity.
"""
import csv, hashlib, json, os, re, subprocess, sys

OK = BAD = 0
def check(name, cond):
    global OK, BAD
    print(('OK  ' if cond else 'BAD ') + name)
    if cond: OK += 1
    else: BAD += 1

def norm(t):
    return re.sub(r'\s+', ' ', t)

L1 = open('paper_part1.py', encoding='utf-8').read()
L3 = open('paper_part3.py', encoding='utf-8').read()
S1 = open('paper_short_part1.py', encoding='utf-8').read()
S2 = open('paper_short_part2.py', encoding='utf-8').read()
S3 = open('paper_short_part3.py', encoding='utf-8').read()

# joined block text (interprets \uXXXX escapes, concatenates line splits)
sys.path.insert(0, os.getcwd())
import paper_part1, paper_part2, paper_part3
import paper_short_part1, paper_short_part2, paper_short_part3
def joined(blocks):
    out = []
    for b in blocks:
        if isinstance(b, tuple) and len(b) >= 2 and isinstance(b[1], str):
            out.append(b[1])
    return norm(' '.join(out))
LJ = joined(paper_part1.BLOCKS + paper_part2.BLOCKS + paper_part3.BLOCKS)
SJ = joined(paper_short_part1.BLOCKS + paper_short_part2.BLOCKS + paper_short_part3.BLOCKS)

from pypdf import PdfReader
long_pdf = norm(' '.join(p.extract_text() or '' for p in PdfReader('ML-BMS-Review.pdf').pages))
short_pdf = norm(' '.join(p.extract_text() or '' for p in PdfReader('ieee_submission/tex/mlbms.pdf').pages))
supp_pdf = norm(' '.join(p.extract_text() or '' for p in PdfReader('Supplementary_Material.pdf').pages))

# ---------------- P1: physics-informed phrasing ----------------
check('P1 long 3.2 new phrasing', 'show no detectably different validation stringency from the others' in L1)
check('P1 long 3.2 old phrasing gone', 'validated no more stringently than others' not in L1)
check('P1 short II-B new phrasing', 'show no detectably different validation stringency from the others' in S2)
check('P1 short old phrasing gone', 'validated no more stringently than others' not in S2)
check('P1 long PDF carries new phrasing', 'no detectably different validation stringency' in long_pdf)

# ---------------- P2: registration ----------------
check('P2 long two structural deviations', 'and two structural deviations are disclosed here rather than footnoted' in L1)
check('P2 long three deviations gone', 'and three deviations are disclosed' not in L1)
check('P2 long retrospective wording', 'The protocol is registered retrospectively rather than prospectively' in L1)
check('P2 long OSF named', 'OSF Registries' in L1)
check('P2 osf_registration draft released', os.path.exists('osf_registration/OSF_REGISTRATION_DRAFT.md'))
check('P2 osf_registration steps released', os.path.exists('osf_registration/OSF_REGISTRATION_STEPS.md'))
check('P2 PDF two deviations', 'two structural deviations are disclosed' in long_pdf)

# ---------------- P3: post-freeze re-code (round-6 QA artifact) ----------------
rc = json.load(open('corpus/validation_recode/validation_recode.json'))
sr = rc['strong_labels']; ba = rc['bucket_agreement_determinable']
check('P3 re-code 46 covered', rc['n_coded'] == 46)
check('P3 re-code 23 determinable', rc['n_determinable'] == 23)
check('P3 10 of 14 confirmed', sr['confirmed_strong'] == 10 and sr['determinable'] == 14)
check('P3 4 contradicted', sr['contradicted'] == 4)
check('P3 2 upgrades', len(rc['nonstrong_upgrades']['upgrades']) == 2)
check('P3 17/23 = 74% kappa 0.47', ba['agree'] == 17 and ba['n'] == 23 and abs(ba['kappa'] - 0.47) < 0.005)
check('P3 long 2.5 coder D description', 'coder D) re-coded the validation field of all 88 primary papers' in L1)
check('P3 long 3.4 results numbers', '10 of the 14 determinable strong labels are confirmed' in L1 and '17 of 23 (74%' in L1)
check('P3 long 3.4 no-label-altered', 'No released label was altered' in L1)
check('P3 short III-C results', '10 of the 14 determinable strong labels are confirmed' in S2)
check('P3 conclusion audit clause', 'confirms ten of fourteen determinable strong labels' in L3)
check('P3 AI declaration extended', 'after the labels were frozen, an AI-assisted re-code of the validation field was run as a released robustness audit' in open('build_docx.py', encoding='utf-8').read())
check('P3 PDF re-code present', 'coder D' in long_pdf and '74%' in long_pdf)
check('P3 coder sheet rows', sum(1 for _ in open('corpus/validation_recode/coder_D_validation.csv')) - 1 == 46)

# ---------------- P4: design-only taxonomy ----------------
check('P4 long limitation present', 'The strong/weak taxonomy itself is design-only' in L1)
check('P4 long covers three misses', all(k in L1 for k in ('how many cells', 'hyper-parameter tuning touched the test set', 'preprocessing such as feature scaling')))
check('P4 short limitation present', 'the strong/weak taxonomy is itself design-only' in S1)
check('P4 PDF limitation', 'taxonomy itself is design-only' in long_pdf)

# ---------------- P5: conclusion center of gravity ----------------
check('P5 long conclusion new', "the retrieval\\u2019s center of gravity is estimation (state, health, lifetime)" in L3)
check('P5 long conclusion about-half gone', '45.8% \\u2014 about half' not in L3)
check('P5 long 3.3 reframed', "the retrieval\\u2019s center of gravity: a property of what the capped retrieval" in L1)
check('P5 short conclusion new', "the retrieval\\u2019s center of gravity is estimation at cell level" in S3)
check('P5 short about-half gone', '46% \\u2014 about half' not in S3)
check('P5 PDF center-of-gravity framing', "retrieval\u2019s center of gravity is estimation" in long_pdf)

# ---------------- P6: retrieval-depth pilot ----------------
dp = json.load(open('corpus/retrieval_depth_pilot.json'))
sm = dp['summary']
check('P6 pilot json keys', sm['families_piloted'] == 6 and sm['per_pass_depth'] == 200)
check('P6 pilot numbers', sm['gated_unique_all_families'] == 2319 and sm['new_gated_not_in_1550_all_families'] in (1498, 1500) and sm['new_gated_venueok_all_families'] in (1404, 1406))
check('P6 pilot overlap factor', abs(sm['orig_30family_overlap_factor'] - 1.46) < 0.005)
check('P6 long 2.2 pilot text', 'retrieval_depth_pilot.py/.json' in L1 and 'yield 2,319 at depth 200' in L1)
check('P6 long binding-constraint statement', 'the 16\\u201317% recall figure measures a sampling decision, not a property of the registry' in L1)
check('P6 short pilot text', 'A released retrieval-depth pilot quantifies what the cap withholds' in S1)
check('P6 PDF pilot present', 'retrieval-depth pilot' in long_pdf)
check('P6 pilot script released', os.path.exists('corpus/retrieval_depth_pilot.py'))

# ---------------- P7: wording qualifiers (updated for the two-round re-coding) ----------------
check('P7 long 1.4 records', 'eligible corpus of 799 Crossref-verified records' in L1)
check('P7 long 1.4 two-round re-coding', 'blind, two-round 30-paper re-coding by two co-author coders under released codebooks' in L1)
check('P7 long conclusion records', 'eligible corpus of 799 records from which field-level shares' in L3)
check('P7 long conclusion two-round', 'blind, two-round 30-paper re-coding by two co-author coders (all five fields at strong agreement in the revised-codebook round' in L3)
check('P7 long abstract two-round', 'after the pre-declared codebook revision, passes all five fields at strong agreement (validation \u03ba = 0.92)' in L1)
check('P7 short contributions records', '799 records (798 dated 2020\\u20132026 plus one early-access record stamped 2027)' in S1)
check('P7 short conclusion two-round', 'blind, two-round 30-paper re-coding by two co-author coders' in S3)
check('P7 no stale abstract-level qualifiers at old spots',
      'blind, abstract-level 30-paper re-coding by two co-author coders.' not in L1
      and 'abstract-level 30-paper re-coding by two co-author coders and label-noise' not in L3
      and 'blind, abstract-level 30-paper re-coding by two co-author coders and label-noise sensitivity ranges' not in S3)

# ---------------- P8: 9.4 split ----------------
check('P8 GTR paragraph', 'UN GTR No. 20 on electric-vehicle safety was established in the UN Global Registry in 2018' in L3)
check('P8 GB paragraph', 'GB 38031 has been rewritten around thermal propagation in the same window' in L3)
check('P8 ISO paragraph', 'The ISO family governs the assurance argument rather than the abuse test' in L3)

# ---------------- R2-A: round-2 agreement artifacts ----------------
rep = {}
for row in csv.DictReader(open('corpus/reliability/agreement_report_fulltext.csv')):
    rep[(row['coder'], row['comparison'], row['field'], row['statistic'])] = row['value']
check('R2A B-C area kappa 0.961', rep[('BC', 'pair', 'area', 'kappa')] == '0.961')
check('R2A B-C method kappa 1.0', float(rep[('BC', 'pair', 'method', 'kappa')]) == 1.0)
check('R2A B-C chem kappa 1.0', float(rep[('BC', 'pair', 'chem', 'kappa')]) == 1.0)
check('R2A B-C data kappa 0.96', rep[('BC', 'pair', 'data', 'kappa')] == '0.96')
check('R2A B-C valid kappa 0.92', rep[('BC', 'pair', 'valid', 'kappa')] == '0.92')
alphas = [float(rep[('all', 'alpha', f, 'krippendorff_alpha')]) for f in ('area', 'method', 'chem', 'data', 'valid')]
check('R2A alphas span 0.92-1.00 (valid 0.922 is the min)', min(alphas) >= 0.92 and max(alphas) <= 1.0 and abs(alphas[4] - 0.922) < 0.001)
check('R2A bucket 28/30', rep[('BC', 'pair', 'valid_strong_bucket', 'bucket_agreement')] == '28/30')
check('R2A vs-gold valid recomputed (B 0.284, C 0.318)', rep[('B', 'vs_gold', 'valid', 'kappa')] == '0.284' and rep[('C', 'vs_gold', 'valid', 'kappa')] == '0.318')
r1 = {}
for row in csv.DictReader(open('corpus/reliability/agreement_report.csv')):
    r1[(row['coder'], row['comparison'], row['field'], row['statistic'])] = row['value']
check('R2A round-1 report corrected vs-gold valid (0.303/0.295)', r1[('B', 'vs_gold', 'valid', 'kappa')] == '0.303' and r1[('C', 'vs_gold', 'valid', 'kappa')] == '0.295')
check('R2A round-1 bucket row 25/30', r1[('BC', 'pair', 'valid_strong_bucket', 'bucket_agreement')] == '25/30')
dis = [r for r in csv.DictReader(open('corpus/reliability/dispute_items_fulltext.csv')) if r['doi'].startswith('10.')]
check('R2A dispute table 30 rows', len(dis) == 30)
check('R2A 10 papers carry v1.1-only codes', sum(1 for r in dis if r['method_coderB'] == 'Not ML (physics/classical)' or r['area_coderB'] == 'Production & quality' or r['data_coderB'] == 'field-stationary' or r['valid_coderB'] == 'not reported') == 10)
check('R2A 16 broader-chem vs gold specifics', sum(1 for r in dis if r['chem_gold'] not in ('various', 'mixed') and r['chem_coderB'] in ('various', 'mixed')) == 16)
check('R2A 4 residual B-C dispute cells', sum(1 for r in dis if r['area_status'] == 'dispute' or r['method_status'] == 'dispute' or r['chem_status'] == 'dispute' or r['data_status'] == 'dispute' or r['valid_status'] == 'dispute') == 4)
for f, h in (('corpus/reliability/coder_B_30_fulltext.csv', 'f1b93b60f4f67e506671a33502b7828695ca7f3dff09f87589c8ea07f89eb3b3'),
             ('corpus/reliability/coder_C_30_fulltext.csv', '33c28849ad8b03463875bd9283b1d280d8d95f31ebab7e0cf46f0938b6511844')):
    check(f'R2A sheet hash {os.path.basename(f)}', hashlib.sha256(open(f, 'rb').read()).hexdigest() == h)

# ---------------- R2-B: byte-identical regeneration ----------------
before = {f: hashlib.md5(open(f, 'rb').read()).hexdigest()
          for f in ('corpus/reliability/agreement_report.csv', 'corpus/reliability/agreement_report_fulltext.csv')}
subprocess.run([sys.executable, 'corpus/inter_rater_reliability.py'], capture_output=True, text=True)
after = {f: hashlib.md5(open(f, 'rb').read()).hexdigest() for f in before}
check('R2B both agreement reports regenerate byte-identically', before == after)

# ---------------- R2-C: gold-state reconciliation ----------------
log = open('corpus/reliability/reliability_log.md', encoding='utf-8').read()
gold = open('out/gold_labels_30.csv', encoding='utf-8').read()
check('R2C log reconciliation note', 'Gold-state reconciliation at merge (2026-11-01' in log)
check('R2C log gold-state item marked resolved', 'Resolved at merge' in log)
check('R2C deposited gold carries corrected jpowsour valid', 'experimental hardware' in [l for l in gold.splitlines() if '235609' in l][0])
check('R2C codebook v1.1 patch section', '## Codebook v1.1 patch (2026-11-01)' in open('corpus/codebook.md', encoding='utf-8').read())

# ---------------- R2-D: extended manuscript (joined text) ----------------
check('R2D 2.5 round-2 paragraph present', 'a second round was designed to measure, on the second stage the protocol pre-declares' in LJ)
check('R2D 2.5 all five fields numbers', 'management function \u03ba = 0.96, method family 1.00, chemistry 1.00, primary data source 0.96, and validation protocol 0.92' in LJ)
check('R2D 2.5 alpha range correct (0.92-1.00)', 'Krippendorff \u03b1 0.92\u20131.00 across the five fields' in LJ and '\u03b1 0.96\u20131.00' not in LJ)
check('R2D 2.5 bucket rise', 'rising from 25 of 30 papers (83%, \u03ba = 0.52) to 28 of 30 (93%, \u03ba = 0.83)' in LJ)
check('R2D 2.5 shared-evidence caveat', 'independence at the judgment level, not the evidence level' in LJ and 'complementary, not interchangeable' in LJ)
check('R2D 2.5 v1.1 patch items', all(k in LJ for k in ('not-ML method code', 'production-and-quality function code', 'field-stationary data code', "dedicated 'not reported' validation code", 'fixed reading for cross-function reviews')))
check('R2D 2.5 evidence counts', '10 full texts' in LJ and '1 accepted-manuscript preprint' in LJ and '19 papers that remain abstract-only' in LJ)
check('R2D 2.5 residual cells classified', 'one is an evidence gap' in LJ and 'v1.2 candidate' in LJ)
check('R2D 2.5 vs-gold capping', 'ten papers carry v1.1-only codes' in LJ and 'sixteen are coded to broader chemistry classes' in LJ)
check('R2D 2.5 five candidate corrections', 'five candidate label corrections' in LJ and 'Severson-dataset papers whose released chemistry records NMC where the dataset itself is LFP' in LJ and 'differ from its own released code repository on all five fields' in LJ)
check('R2D 2.5 no-independent-dual-coding reworded', 'No fully independent full-text dual coding proved achievable' in LJ and 'No full-text dual coding was performed' not in LJ)
check('R2D 2.5 post-freeze clause reworded', 'audits the frozen labels from the evidence side rather than measuring coder agreement' in LJ)
check('R2D limitations two-round', 'round 1 (independent evidence, mostly abstract-level access) passed three of five fields, and round 2 (revised codebook, shared evidence base, 19 of 30 papers still abstract-only) passed all five at the strong level' in LJ)
check('R2D 3.4 round-2 bucket clause', 'lifts the coders\u2019 mutual bucket agreement to 28 of 30 papers (93%, \u03ba = 0.83)' in LJ)
check('R2D 3.4 four further corrections', 'four further candidate label corrections' in LJ and 'dispute_items_fulltext.csv' in LJ)
check('R2D conclusion cross-checked clause', 'cross-checked by a revised-codebook re-coding round in which the two coders agree on the strong/non-strong bucket for 28 of 30 papers' in LJ)

# ---------------- R2-E: condensed manuscript (joined text) ----------------
check('R2E contributions two-round', 'blind, two-round 30-paper re-coding by two co-author coders (all five fields at strong agreement in the revised-codebook round)' in SJ)
check('R2E II-C round-2 passage', 'codebook revision, then one re-coded subset' in SJ and 'was then executed as pre-declared' in SJ)
check('R2E II-C all five numbers', 'management function \u03ba = 0.96, method family 1.00, chemistry 1.00, primary data source 0.96, validation protocol 0.92' in SJ)
check('R2E II-C bucket rise', 'rising from 25 of 30 papers (83%, \u03ba = 0.52) to 28 of 30 (93%, \u03ba = 0.83)' in SJ)
check('R2E II-C shared-evidence caveat', 'independence at the judgment level, not the evidence level' in SJ)
check('R2E II-C chemistry rule candidate kept', 'chemistry inference-rule candidate remains logged but not codified' in SJ)
check('R2E II-C five corrections', 'five candidate label corrections' in SJ and 'queued for author adjudication' in SJ)
check('R2E round-1 bucket kappa corrected to 0.52', '\u03ba = 0.52 at the sample\'s prevalence' in SJ and '\u03ba = 0.51' not in SJ)
check('R2E limitations two-round', 'three of five fields above threshold in round 1, all five at the strong level in the revised-codebook round 2' in SJ)
check('R2E III lifts clause', 'lifts the coders\' mutual bucket agreement to 28 of 30 papers, \u03ba = 0.83' in SJ)
check('R2E conclusion two-round', 'blind, two-round 30-paper re-coding by two co-author coders' in SJ and '(all five fields at strong agreement in the revised-codebook round)' in SJ)

# ---------------- R2-F: PDFs ----------------
check('R2F long PDF round-2 paragraph', 'second round was designed to measure' in long_pdf)
check('R2F long PDF five-field numbers', 'method family 1.00, chemistry 1.00' in long_pdf)
check('R2F long PDF bucket rise', 'to 28 of 30 (93%, \u03ba = 0.83)' in long_pdf)
check('R2F long PDF adjudication queue', 'queued for author adjudication' in long_pdf)
check('R2F long PDF abstract two-round', 'after the pre-declared codebook revision, passes all five fields at strong agreement' in long_pdf)
check('R2F long PDF alpha range', '0.92\u20131.00 across the five fields' in long_pdf)
check('R2F short PDF round-2 passage', ('codebook revision, then one re-coded subset' in short_pdf) or ('codebook revision, then one re-coded sub- set' in short_pdf) or ('codebook revision, then one re- coded subset' in short_pdf))
check('R2F short PDF five-field numbers', 'validation protocol 0.92' in short_pdf)
check('R2F short PDF bucket rise', '28 of 30 (93%, \u03ba = 0.83)' in short_pdf)
check('R2F supplement round-2 note', 'Why round 2 does not move this envelope' in supp_pdf)

# ---------------- R2-G: README ----------------
rd = open('README.md', encoding='utf-8').read()
check('R2G README two-round headline', 'Inter-coder reliability, measured in two rounds' in rd and '28/30 (93%, \u03ba = 0.83)' in rd)
check('R2G README contents row updated', 'round 2 full-text re-coding under codebook v1.1' in rd)
check('R2G README AI disclosure two-round', 'two-round 30-paper blind inter-coder re-coding study' in rd)
check('R2G README round-1 kappa 0.51 gone', '\u03ba = 0.51)' not in rd)


# ---------------- R2-H: fresh-submission cleanup + technical depth ----------------
check('R2H no earlier-draft reference (short)', 'an earlier draft' not in SJ and 'an earlier draft' not in S1)
check('R2H no repair language (short)', all(k not in SJ for k in ('repair path', 'codebook repair', 'repaired', 'it must be reported straight', 'The honest reading remains', 'The honest framing of', 'the short version is that')))
check('R2H no repair language (long)', all(k not in LJ for k in ('repair path', 'codebook repair', 'repaired', 'next revision cycle')))
check('R2H abstract section self-reference removed', 'Section III-B' not in paper_short_part1.ABSTRACT[0])
check('R2H short 9.1 GTR garble fixed', "review's retrieval date" not in SJ and 'November 2026 session; it adds' in SJ)
check('R2H outlook de-versioned', 'what the next research cycle should produce' in S3 and 'what the next research cycle should produce' in L3)
check('R2H two-culture split (short)', 'two-culture split in validation practice' in SJ and 'at 0 of 11' in SJ)
check('R2H two-culture split (long)', 'two-culture split in validation practice' in LJ and 'at 0 of 11' in LJ)
check('R2H family-class matrix numbers (short)', 'uses a strong isolation protocol in 19 of them (68%)' in SJ and 'all five of its papers validate on isolation protocols' in SJ)
check('R2H function-data stratification (short)', 'fault and safety is the only cluster whose modal primary source is real-vehicle data (3 of 7)' in SJ and 'NMC cells dominate 54 of the 88 primary papers (61%)' in SJ)
check('R2H function-data stratification (long)', 'NMC cells dominate 54 of the 88 primary papers (61%)' in LJ)
check('R2H leakage mechanism sentence (short)', 'Both leaking definitions share one mechanism' in SJ)
check('R2H misattribution fix (short)', 'so that misattributions of this kind are not hidden' in SJ)
check('R2H PDF two-culture present', 'two-culture split' in short_pdf and 'two-culture split' in long_pdf)

# ---------------- global sanity ----------------
r = subprocess.run([sys.executable, 'corpus/consistency_check.py'], capture_output=True, text=True)
check('consistency_check.py passes', r.returncode == 0 and 'FAIL' not in r.stdout.upper())
check('long PDF 46 pp', len(PdfReader('ML-BMS-Review.pdf').pages) == 46)
check('short PDF 20 pp', len(PdfReader('ieee_submission/tex/mlbms.pdf').pages) == 20)
check('supplement PDF 4 pp', len(PdfReader('Supplementary_Material.pdf').pages) == 4)
check('no stale "abstract-level 30-paper re-coding by two co-author coders" as sole descriptor in PDFs',
      'blind, abstract-level 30-paper re-coding by two co-author coders' not in long_pdf
      and 'blind, abstract-level 30-paper re-coding by two co-author coders' not in short_pdf)
from docx import Document
check('build sanity: docx opens, 14 tables', len(Document('ML-BMS-Review.docx').tables) == 14)

print(f'\n{OK} passed, {BAD} failed of {OK+BAD}')
sys.exit(1 if BAD else 0)
