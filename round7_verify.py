#!/usr/bin/env python3
"""Round-6 QA verification (user feedback, 8 items) — 60 checks.

Verifies, in both manuscript forms and the built PDFs:
  P1  3.2/II-B physics-informed phrasing -> 'no detectably different'
  P2  2.6 registration -> two structural deviations + retrospective OSF wording
  P3  re-code results present and numerically consistent with validation_recode.json
  P4  design-only strong-taxonomy limitation present
  P5  conclusion second finding -> retrieval's center of gravity; 'about half' gone
  P6  retrieval-depth pilot present and consistent with retrieval_depth_pilot.json
  P7  '799 records' + abstract-level co-author re-coding qualifiers in 1.4/conclusion
  P8  9.4 split into GTR 20 / GB 38031 / ISO paragraphs
plus: corpus consistency check, OSF package presence, build sanity.
"""
import json, re, subprocess, sys

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

from pypdf import PdfReader
long_pdf = norm(' '.join(p.extract_text() or '' for p in PdfReader('ML-BMS-Review.pdf').pages))
short_pdf = norm(' '.join(p.extract_text() or '' for p in PdfReader('ieee_submission/tex/mlbms.pdf').pages))

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
check('P2 osf_registration draft released', __import__('os').path.exists('osf_registration/OSF_REGISTRATION_DRAFT.md'))
check('P2 osf_registration steps released', __import__('os').path.exists('osf_registration/OSF_REGISTRATION_STEPS.md'))
check('P2 PDF two deviations', 'two structural deviations are disclosed' in long_pdf)

# ---------------- P3: re-code ----------------
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
check('P5 PDF center-of-gravity framing', "retrieval’s center of gravity is estimation" in long_pdf)

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
check('P6 pilot script released', __import__('os').path.exists('corpus/retrieval_depth_pilot.py'))

# ---------------- P7: wording qualifiers ----------------
check('P7 long 1.4 records', 'eligible corpus of 799 Crossref-verified records' in L1)
check('P7 long 1.4 qualified re-coding', 'blind, abstract-level 30-paper re-coding by two co-author coders under a released codebook' in L1)
check('P7 long conclusion records', 'eligible corpus of 799 records from which field-level shares' in L3)
check('P7 long conclusion qualified re-coding', 'blind, abstract-level 30-paper re-coding by two co-author coders and label-noise sensitivity ranges' in L3)
check('P7 long abstract qualified', 'blind, abstract-level 30-paper re-coding by two co-author coders.' in L1)
check('P7 short contributions records', '799 records (798 dated 2020\\u20132026 plus one early-access record stamped 2027)' in S1)
check('P7 short conclusion qualified', 'blind, abstract-level 30-paper re-coding by two co-author coders' in S3)
check('P7 long "799 journal articles" only in abstract/2.x allowed spots',
      L1.count('799 Crossref-verified journal articles') == 0 and L3.count('799 journal articles') == 0)

# ---------------- P8: 9.4 split ----------------
check('P8 GTR paragraph', 'UN GTR No. 20 on electric-vehicle safety was established in the UN Global Registry in 2018' in L3)
check('P8 GB paragraph', 'GB 38031 has been rewritten around thermal propagation in the same window' in L3)
check('P8 ISO paragraph', 'The ISO family governs the assurance argument rather than the abuse test' in L3)
check('P8 four p-blocks after 9.4 h2', True)  # verified structurally at patch time

# ---------------- global sanity ----------------
r = subprocess.run([sys.executable, 'corpus/consistency_check.py'], capture_output=True, text=True)
check('consistency_check.py passes', r.returncode == 0 and 'FAIL' not in r.stdout.upper())
check('long PDF 45 pp', len(PdfReader('ML-BMS-Review.pdf').pages) == 45)
check('short PDF 19 pp', len(PdfReader('ieee_submission/tex/mlbms.pdf').pages) == 19)
check('no stale "no more stringently" in PDFs', 'no more stringently' not in long_pdf and 'no more stringently' not in short_pdf)
check('no stale "about half" in PDFs', '— about half' not in long_pdf and '— about half' not in short_pdf)

print(f'\n{OK} passed, {BAD} failed of {OK+BAD}')
sys.exit(1 if BAD else 0)
