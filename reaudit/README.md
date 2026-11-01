# Re-audit package (codebook v2.0) — TTE-Reg-2026-10-3720 rejection response

This directory contains the complete instrument for re-running the validation
audit with measured inter-coder reliability, built in response to the
TTE-Reg-2026-10-3720 decision (Associate Editor: *"kappa = 0.48"* on the
validation-protocol field, selection of the 103 studies needs stronger
justification, recall-audit limitations, more EV-specific / vehicle-level /
onboard / transportation-safety emphasis).

It **supersedes**, for the validation-audit dimensions:

| Superseded artifact | Why superseded |
|---|---|
| `corpus/coding_protocol.md` (v1, 30-paper abstract-level sheets) | v1 coders reached full text for only 7/30 and 2/30 sample papers; the two fields that failed (chemistry κ = 0.55, validation protocol κ = 0.48) are exactly those least often stated at abstract level. v2 mandates full-text coding. |
| `corpus/reliability/` (coder A/B/C 30-paper sheets + agreement report) | Retained as the historical v1 evidence; not deleted, but no longer the instrument of record. |
| `corpus/validation_recode/` (coder D post-freeze re-code, bucket κ = 0.47) | Single-coder AI-assisted audit; v2 replaces it with blinded two-coder full re-coding plus adjudication. |

## Files

| File | What it is |
|---|---|
| `Validation_Audit_Codebook_v2.docx` | The coding instrument (25 pp): unit and evidence rules, 8 ground rules, 4-stage workflow with gates, variables V1–V14 (construct, exhaustive code sets, decision rules, worked examples, pitfalls), adjudication protocol, agreement-statistics plan, pre-declared category-collapse rule, reporting template, quick-reference appendix. |
| `Coding_Workbook_v2.xlsx` | The coding workbook (10 sheets): `README` (steps), `Study_IDs` (S001–S103 with 12 pilot flags), `Code_Lists` (+14 locked named ranges), `Coder1` / `Coder2` / `Adjudicated` sheets with locked dropdowns, live `Kappa_Calculator` (pilot gate: Po, Pe, Cohen's κ, PABAK per variable), `Demo_Data` (12 synthetic studies × 2 synthetic coders, with a mini live calculator), `Worked_Examples` (20 tricky cases), `Adjudication_Log`. |
| `kappa_analysis.py` | Standalone scoring script: Cohen's κ, PABAK, linear/quadratic weighted κ (ordinal variables, NR-excluded with counts), Fleiss's κ (3-rater mode), bootstrap 95% CIs (percentile, default 10,000 resamples), per-variable confusion matrices (CSV + optional PNG heatmaps), the pre-declared adjacent-category collapse rule (>50% of disagreements in one adjacent pair), and an auto-filled manuscript reporting sentence. `--selftest` runs built-in cross-checks against scikit-learn. |
| `Revised_Methods_Reliability.tex` | Drop-in LaTeX for the revised manuscript: (1) *Reliability of the validation audit* (replaces the paragraph that reported κ = 0.48), (2) *Selection of studies for the in-depth audit* (tier-2 criteria + PRISMA-ScR flow + sensitivity analysis), (3) *Search recall assurance* (citation chaining, hand-search, known-must-find benchmark), (4) *Transportation-specific synthesis* (V11/V12/V14-driven: vehicle-level validation, onboard constraints, safety framing). Results-dependent numbers are marked for completion from the `kappa_analysis.py` output after the re-coding. |

## Workflow (co-authors: ~5 working days)

1. **Sign-off** — both coders read `Validation_Audit_Codebook_v2.docx` end-to-end
   and confirm by reply (the codebook is the contract; do not negotiate codes).
2. **Pilot** — each coder independently codes the 12 flagged pilot studies in
   their own copy of the workbook (`Study_IDs` column flags them; S001–S103 map
   to the 103 DOIs in `corpus/papers.csv`). Full text + supplement only;
   silence = "NR"; no inference.
3. **Gate** — paste both pilots into `Coder1` / `Coder2`, read the
   `Kappa_Calculator` sheet. Gate: per-variable κ ≥ 0.70. Below gate ⇒
   discrepancy meeting ⇒ codebook edit ⇒ re-pilot (the codebook changes, not
   the codes). The gate can also be computed with
   `python3 kappa_analysis.py --workbook Coding_Workbook_v2.xlsx`.
4. **Full double-coding** — all 103 studies, both coders, blinded
   (~25–35 min/study; comment with page/section for every non-obvious code).
5. **Adjudication** — remaining disagreements go to the adjudicator (senior
   author; name/email to be filled in codebook §7); every resolution is logged
   in `Adjudication_Log` with rationale + codebook clause.
6. **Scoring** — `python3 kappa_analysis.py --workbook Coding_Workbook_v2.xlsx
   --bootstrap 10000 --heatmap` produces the per-variable table (raw agreement,
   κ, PABAK, weighted κ, 95% CIs), confusion matrices, and the reporting
   sentence for the manuscript.
7. **Merge** — fill the marked numbers into `Revised_Methods_Reliability.tex`
   and merge into `ieee_submission/tex/mlbms.tex`.

## Verification already performed

- `kappa_analysis.py --selftest`: all pass, including 5/5 cross-checks against
  `sklearn.metrics.cohen_kappa_score` and hand-computed Cohen / weighted /
  Fleiss examples.
- End-to-end test on 103 synthetic coded studies: all 14 variable κ values
  match sklearn to 4 decimal places; the pre-declared collapse rule fires on
  the predicted adjacent pairs (V6 levels 1+0, V11 levels 2+1); bootstrap CIs
  bracket the estimates; 28 output files produced.
- `Coding_Workbook_v2.xlsx`: LibreOffice recalculation clean (302 formulas,
  0 errors); the live calculator matches an independent numpy computation to
  1e-9 on all 14 demo variables.

## Provenance and AI disclosure

The instrument was drafted with declared AI assistance (instrument design,
workbook formulas, and the scoring script), consistent with the repository's
standing AI-use declaration; all coding decisions, codebook sign-off, pilot
gate judgments, and adjudications are the co-authors'. One deliberate
placeholder remains: the adjudicator's name and email in codebook §7.
