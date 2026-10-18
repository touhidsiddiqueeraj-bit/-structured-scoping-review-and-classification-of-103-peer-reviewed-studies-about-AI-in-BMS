# Independent Re-coding Protocol — Second and Third Coders

Purpose: this document tells coders 2 and 3 exactly what to do to produce the
independent reliability evidence that the review currently lacks (TTE review:
"the classification procedure is too subjective … without independent double
coding and an agreement measure"). Follow it literally; do not discuss codes
with other coders until your sheet is locked (Step 5).

## 0. What you will and will not see

- You receive a **blind sheet** (`corpus/reliability/coder_X_30.csv`) with:
  doi, title, journal, year, and a link column for the paper's landing page.
- You do **not** receive, and must not open, these files, which contain the
  released labels or population statistics:
  - `corpus/papers.csv`, `papers_final.json`, `stats.json`, `consistency_check.py` output
  - `out/gold_labels_30.csv` (the released labels for your sample, generated
    only when scoring)
  - any draft of the manuscript's Sections III–VIII
  - co-coders' sheets or communications about specific papers
- If you must inspect a paper's full text, take notes in your own words;
  do not transcribe the paper's phrases into the sheet cells verbatim
  (that is what `evidence` columns are for).

## 1. Sample

- Your sheet contains **30 papers**: a stratified random draw (seed 20261017)
  from the classified subset, stratified by management function × year band,
  so every stratum with ≥2 papers contributes and rare functions are still hit.
- The draw and the full stratification (released labels removed) are
  reproducible with `corpus/make_coding_sample.py` (rerun to regenerate;
  the seed pins the exact papers).

## 2. Access a paper

1. Resolve `doi`; open the publisher or repository page.
2. Read at minimum: abstract **and** (where available) methods/validation
   section. If full text is paywalled, use the arXiv/repository copy; if the
   only evidence available is the abstract, code it anyway and flag
   `access = abstract-only` (see §4 column list).
3. Note the paper's own split/protocol description (quote ≤25 words in the
   evidence column).

## 3. Code the sheet — definitions

All definitions are in `corpus/codebook.md` (Sections 3-bis: field definitions,
border rules, absorbing rule). Read the whole codebook before your first paper;
this sheet is only a checklist. Short version per field:

| Column | Terms/values | Core question |
|---|---|---|
| `area` | State estimation (SOC); Health estimation (SOH); Prognostics (RUL); Charging control; Thermal management; Fault & safety; Cell balancing & ECM; Cross-cutting | What is the headline contribution's *function*? (Border rule in codebook; a controller-embedded estimator counts as *control* only if control is the claim.) |
| `method` | Shallow ML; Deep learning; Physics-informed; Hybrid physics+ML; Filter-based hybrid; Meta-heuristic-optimized DL; Bayesian optimization; Optimization-augmented control; Reinforcement learning; Transfer learning; Graph neural network; Foundation model / LLM; Review / perspective | Which family carries the headline result? Physics-in-*loss* = Physics-informed; physics model *architecturally adjacent* = Hybrid physics+ML; physics model *inside a KF/UKF wrapper* = Filter-based hybrid. |
| `chem` | NMC; LFP; LCO; Li-metal; Li-S; mixed; various; other (state) | Which chemistry does the headline system use? |
| `data` | self-lab; Severson-MATR; NASA; CALCE; EIS-lab; real-vehicle; simulation; review; mixed | Where does the headline number come from? |
| `valid` | within-cell split; cross-validation (k-fold); cross-cell holdout; cross-chemistry holdout; cross-domain holdout; online/real-vehicle; experimental hardware; simulation plus hardware spot-check; simulation; case study; review synthesis | Which *strongest* protocol does the paper report for its headline claim (absorbing rule, codebook)? |
| `access` | full-text; preprint; abstract-only | What did you read? (Choose one.) |

`evidence_area`, `evidence_method`, `evidence_valid`: ≤25-word quotes or precise
paraphrases **from the paper**, not your inference.

Coding conventions:

- One paper ⇒ one value per field (no semi-colons except in evidence).
- If a convention seems ambiguous, do **not** guess silently: still pick your
  best reading, then write the ambiguity in `comment`. The dispute session
  uses all `comment` cells first; codebook patches come from them.
- Do not code by citation list or by related-work prose; code by what *this
  paper* does.

## 4. Sheet columns (blind sheet keeps doi/title/journal/year; you fill the rest)

`area, method, chem, data, valid, access, evidence_area, evidence_method, evidence_valid, comment`
Use exactly these column names; fill every row; csv only.

## 5. Locks and dispute resolution

1. Work alone, in one pass, in **one sitting or two halves ≤3 days apart**;
   note the completion date on your sheet's filename row (`completed,YYYY-MM-DD`).
2. Email/save your CSV as `corpus/reliability/coder_<letter>_30.csv`.
   Do not edit it after saving (a file hash is recorded in `reliability_log.md`).
3. **Only after both/three sheets are in**, the coordinators de-blind, align,
   and run `corpus/inter_rater_reliability.py`. Preserve per-field disagreement
   for the released agreement report.
4. Dispute session: the three coders plus the lead author walk through every
   disagreed cell; first try a codebook clarification, then a majority vote;
   outcomes are written into `reliability_log.md`; codebook patches are
   committed as a patch paragraph (dated), never silently.
5. Nothing in this session may retrospectively alter any locked sheet.

## 6. Milestones

| | |
|---|---|
| Read codebook + this protocol | 30 min per coder |
| Code 30 papers (full-text where possible) | 6–8 h per coder |
| Agreement computation (automatic, see below) | minutes |
| Dispute session + patch | 1–2 h all present |

Agreement statistic to be reported for each field:
percent agreement, unweighted Cohen's κ coder-pairs (3 pairs) on the 30-paper
sample, and Krippendorff's α (nominal) across coders. Agreement thresholds:
κ ≥ .66 acceptable, ≥ .80 strong; below .66 triggers codebook repair and one
re-coded subset. Coordination: the lead author runs the reliability script and
maintains `corpus/reliability/reliability_log.md`.
