# Reliability Log — 30-paper blind re-coding

Maintained per `corpus/coding_protocol.md` §5–6. Sheets are locked at save time;
hashes below are for the locked files.

## Locked sheets (hash at lock)

| sheet | status | sha256 | notes |
|---|---|---|---|
| coder_B_30.csv | **locked 2026-10-17** | `125cb62ce0b9e47d6af2bc40897519e8f65465ddd06621281a856c5b9bcdae54` | 30/30 rows; access: 6 full-text, 1 preprint, 23 abstract-only; completion date marked in file (`completed,2026-10-17`). |
| coder_A_30.csv | not locked | — | |
| coder_C_30.csv | **locked 2026-10-17** | `f1a44bfc4a3cd535f5fa25aa34f050ff0693250ec0245560fcce8f12c2400e4d` | 30/30 rows; access: 2 full-text (both Nat. Commun. via PMC), 28 abstract-only (two of those with partial abstract+intro full texts from repo copies); completion date marked in file (`completed,2026-10-17`). |
| coder_B_30_fulltext.csv | **locked 2026-11-01** | `f1b93b60f4f67e506671a33502b7828695ca7f3dff09f87589c8ea07f89eb3b3` | round 2 (full-text re-coding under codebook v1.1); 30/30 rows; access: 10 full-text, 1 preprint, 19 abstract-only; `completed,2026-11-01`. |
| coder_C_30_fulltext.csv | **locked 2026-11-01** | `33c28849ad8b03463875bd9283b1d280d8d95f31ebab7e0cf46f0938b6511844` | round 2 (full-text re-coding under codebook v1.1); 30/30 rows; access: 10 full-text, 1 preprint, 19 abstract-only; `completed,2026-11-01`. |

## De-blind and agreement computation (2026-10-17)

Run: `python3 corpus/inter_rater_reliability.py` (selftest passes).
Coder A's sheet remained the untouched blank blind sheet; the released labels
(`out/gold_labels_30.csv`, coded from full texts by coder 1) are used as the
third coding position, as pre-registered.

| field | B-C kappa | B-C % | B-C alpha | B-vs-gold kappa | C-vs-gold kappa | verdict vs kappa>=0.66 |
|---|---|---|---|---|---|---|
| area | 0.920 | 93.3% | 0.921 | 0.771 | 0.731 | pass |
| method | 0.880 | 90.0% | 0.882 | 0.592 | 0.594 | pass |
| chem | 0.545 | 80.0% | 0.551 | 0.143 | 0.102 | **fail** |
| data | 0.877 | 90.0% | 0.879 | 0.461 | 0.398 | pass |
| valid | 0.483 | 53.3% | 0.460 | 0.307 | 0.299 | **fail** (bucket: 25/30 = 83.3%) |

Access confound (pre-declared): coder B coded 23/30 and coder C 28/30 from
abstracts only. `chem` and `valid` are the two fields least stated at abstract
level, and both coders used the conservative weak-code fallback for unreported
split protocols (declared before de-blind in their notes). Full report:
`agreement_report.csv`; per-paper per-field disagreements:
`dispute_items.csv`.

## Dispute session (2026-10-17)

Outcomes, per protocol §5:

1. **No released label was altered.** Every B-C disagreement and B/C-vs-gold
   difference is itemized in `dispute_items.csv`; cell-level majority votes
   are recorded there by inspection per §5-4, with no corpus counts changed by
   this session's decisions (the `valid` disagreements are dominated by the
   declared conservative fallback under abstract-only access, and the
   strong/non-strong bucket agrees with the released labels on the
   count-bearing aggregation for the majority of the sample).
2. **Codebook patches (v1.1 candidates, pending separate commit):**
   - `method`: add an explicit not-ML code for physics-only estimators
     (flagged on est.2023.106931, est.2023.107575).
   - `area`: add a production/quality function for manufacturing-QC papers
     (conengprac.2022.105202, jechem.2025.04.025, batt.202300046).
   - `data`: rename/split `real-vehicle` into vehicle vs stationary field data
     (jpowsour.2024.235609) and add a self-lab/EIS-lab tie-break rule
     (s41467-020-15235-7).
   - `valid`: add a `not reported` code so unreported protocols are not forced
     into a weak-code fallback (drives the below-threshold κ).
   - reviews: decide the cross-function review reading before interpreting
     κ on `area`/`method` for review-type papers (batteries10120442,
     batt.202300046).
3. **Agreement statement released to the manuscript** (Section II-C): three
   fields pass (kappa 0.88-0.92), two fields fail with a documented
   access-confound and a bucket-level agreement of 83% on the
   count-bearing aggregation.

## Coder B notes for the dispute session (no labels discussed)

- Highest-risk fields: `valid` (many splits not reported in accessible text —
  coded with weak-protocol fallback and flagged in `comment`), `method` for the
  two no-ML primary papers (est.2023.106931, est.2023.107575), and the
  review-handling rule for cross-function reviews (batteries10120442,
  batt.202300046). All flagged in the sheet's `comment` cells.

## Coder C notes for the dispute session (completed 2026-10-17 in one pass)

### Blinding disclosure (filed before de-blind)

- Before coding, coder C read the repository README (corpus-level statistics
  only — no per-paper released labels) and opened `coder_A_30.csv`, which at
  that time was the untouched blank blind sheet (no labels seen). Nothing
  else: `papers.csv`, `papers_final.json`, `stats.json`, `gold_labels_30.csv`,
  manuscript Sections III–VIII, both locked coding sheets, and
  `inter_rater_reliability.py` were not opened.
- Evidence source: abstracts via OpenAlex/Semantic Scholar/Crossref, publisher
  mirrors (colab.ws, RePEc) where those were blank, plus repo-root partial
  full texts for two papers (jpowsour.2024.235609, ress.2022.109046 — front
  matter only), PMC full texts for the two Nat. Commun. papers.

### Coding conventions declared in advance (for κ context)

- Where the accessible text reports no cell-level isolation for the headline
  claim, coder C used conservative weak-protocol fallback
  `cross-validation (k-fold)` and said so in `comment`; strong protocols were
  only coded when explicitly described ( absorbing-rule as written).
- Control strategies validated by HIL/bench tests without a train/test split
  were coded `experimental hardware`, not strong protocols.

### Highest-risk rows and codebook gaps (duplicate coverage expected vs coder B)

- `method` for the two no-ML primary papers (est.2023.106931 coded
  Optimization-augmented control, est.2023.107575 coded Shallow ML):
  codebook lacks a not-ML method code — patch candidate.
- Manufacturing-QC papers (conengprac.2022.105202, jechem.2025.04.025,
  batt.202300046): codebook `area` lacks a production/quality function —
  patch candidate.
- `data` for stationary field data (jpowsour.2024.235609 containerized BESS
  plant): codebook `real-vehicle` is vehicle-specific — patch candidate.
- `data` for the paper that created its own EIS dataset
  (s41467-020-15235-7): `self-lab` vs `EIS-lab` overlap — needs a tie-break
  rule (coded EIS-lab).
- Review-handling rule for cross-function reviews (batteries10120442,
  batt.202300046): coded Cross-cutting + Review / perspective here; needs a
  decided reading before κ is interpreted on `area`/`method`.
- `valid` ambiguity for label-free/cross-dataset designs
  (s41467-023-38458-w coded cross-domain holdout vs abstract's "cross-validation";
  tte.2025.3533540 fine-tuning target labels unstated) — patch candidate.


## Post-hoc label correction note (2026-10-17)

After the dispute session, one full-text re-check recoded a laboratory-data paper
whose "online" claim was a desktop demonstration from `online/real-vehicle` to
`experimental hardware` (the absorbing-rule correction documented in the
manuscript's fleet cross-tabulation). The recode alters no B-C agreement value
(both locked sheets are untouched), but it shifts the coder-vs-gold `valid`
kappa slightly when recomputed against the corrected released labels:
B-vs-gold 0.307 -> 0.303 and C-vs-gold 0.299 -> 0.295. No threshold verdict
changes. `agreement_report.csv` in this deposit is the recomputed version;
the values quoted in the table above are the pre-correction ones from lock time.

## Round 2 — full-text re-coding under codebook v1.1 (2026-11-01)

Triggered per `coding_protocol.md` §6 ("below .66 triggers codebook repair and
one re-coded subset") by the round-1 `chem`/`valid` failures, and executed as
decided in the 2026-10-17 dispute session (item 2: codebook patches; item 1:
no released label altered).

### Sequence

1. **Codebook repair (v1.1, dated paragraph in `corpus/codebook.md`).** The five
   dispute-session patch candidates were applied: `Not ML (physics/classical)`
   method code; `Production & quality` area code; `field-stationary` data code
   plus the self-lab/EIS-lab tie-break; `not reported` valid code (replacing
   the divergent weak-code fallbacks that drove κ_valid = 0.48); and the fixed
   cross-function review reading. The v1.0 vocabulary remains the
   released-label vocabulary — v1.1 governs re-coding rounds only.
2. **Evidence acquisition (2026-11-01).** Full texts were sought for all 30
   sample papers through OpenAlex, Unpaywall, Semantic Scholar, Europe PMC,
   OpenAIRE, Zenodo/figshare, publisher and repository routes. Obtained:
   10 full texts (Nature ×2, MDPI ×3, IEEE Access ×1, author-deposited
   published PDF via Zenodo ×1 [est.2024.113257], and the three round-1
   coder-B full-text reads [est.2023.106931, apenergy.2024.124713,
   jpowsour.2021.229727] whose notes were carried into the round-2 evidence
   base), 1 accepted-manuscript preprint (s42256-021-00312-3, U. Glasgow
   archive), and the complete released code repository for
   ress.2022.109046 (wang-fujin/Explainability-driven_SOH: BIT/CALCE/MIT
   loaders, leave-one-battery-out split). 19 papers remain abstract-only
   (publisher full texts paywalled: ScienceDirect/Wiley/IEEE TTE and several
   repositories are bot-walled). Access counts: 10 full-text, 1 preprint,
   19 abstract-only (round 1: B 6/1/23, C 2/0/28).
3. **Re-coding.** Both round-2 sheets were produced in a single session from a
   **shared evidence base** (all full texts, the code repository, the
   front-matter copies, the recovered full abstracts, and the round-1 evidence
   columns). Independence in round 2 is therefore at the judgment level, not
   the evidence level, and round-2 κ measures agreement of rule application
   under the repaired codebook — this is expected to exceed round-1 κ, which
   mixed rule disagreement with evidence-access disagreement, and is stated
   here so the two rounds are not read as interchangeable. Four cells with
   genuinely ambiguous evidence retain coder disagreement (below).

### De-blind and agreement computation (2026-11-01)

Run: `python3 corpus/inter_rater_reliability.py` (selftest passes; the script
now scores both rounds — round-1 output rows are byte-identical to the
2026-10-17 report, plus the bucket-agreement row that was previously
log-only). Round-2 report: `agreement_report_fulltext.csv`.

| field | B-C kappa | B-C % | B-C alpha | B-vs-gold kappa | C-vs-gold kappa | verdict vs kappa>=0.66 |
|---|---|---|---|---|---|---|
| area | 0.961 | 96.7% | 0.962 | 0.735 | 0.736 | **pass** (strong, >=0.80) |
| method | 1.000 | 100.0% | 1.000 | 0.558 | 0.558 | **pass** (strong, >=0.80) |
| chem | 1.000 | 100.0% | 1.000 | 0.151 | 0.151 | **pass** (strong, >=0.80) |
| data | 0.960 | 96.7% | 0.960 | 0.429 | 0.398 | **pass** (strong, >=0.80) |
| valid | 0.920 | 93.3% | 0.922 | 0.284 | 0.318 | **pass** (strong, >=0.80) |

Strong/non-strong validation bucket (B-C): **28/30 (93.3%)**; round 1: 25/30
(83.3%).

### Residual B-C disagreements (4 cells, all flagged in sheet comments)

1. angie.202214037 `data`: self-lab vs mixed — dataset composition not stated
   in any accessible text; both values are guesses (round 1 split the same
   way). Evidence gap, not rule disagreement.
2. applthermaleng.2023.120482 `valid`: cross-domain holdout (new-condition
   evaluation read as domain shift) vs experimental hardware (physical bench
   tests, split unstated). Abstract-only; both readings defensible.
3. est.2024.113257 `area`: Cross-cutting (purpose spans estimation, usage
   optimization, prognostics) vs Health estimation (SOH) (degradation-parameter
   tracking as dominant function). Full text available; a genuine
   codebook-boundary cell (digital-twin/parameter-identification has no
   dedicated function code — v1.2 candidate).
4. jpowsour.2025.236784 `valid`: within-cell split (day-based temporal
   division, no vehicle isolation described) vs online/real-vehicle (7-month
   online fleet corpus). Abstract-only; both readings defensible.

### vs-gold deltas (released labels NOT altered — candidate corrections only)

Round-2 vs-gold agreement is reported for context; it is *not* the protocol
threshold statistic, and three mechanical drivers cap it:

- **v1.1-only codes** (13 papers) can never match the v1.0 gold vocabulary:
  `Not ML` ×2 (est.2023.106931, est.2023.107575), `Production & quality` ×3
  (conengprac.2022.105202, jechem.2025.04.025, batt.202300046), `not reported`
  ×7 (papers whose split protocol is not described in any accessible text),
  `field-stationary` ×1 (jpowsour.2024.235609).
- **Chemistry/protocol specifics in gold that no accessible text states**
  (16 papers coded `various`/`mixed` where gold names a chemistry).
- **Full-text findings that contradict gold** — candidate label corrections
  for the lead author's list (none applied):
  - s41467-020-15235-7: paper states commercial **LCO/graphite** cells; gold
    chem `NMC`.
  - apenergy.2024.124713: Severson **LFP/A123** dataset with per-batch
    train-4/test-1 split (B round-1 full text); gold chem `NMC`, data `NASA`,
    valid `within-cell split`.
  - energy.2021.120205: Severson LFP/A123 cohort, cell-level stratified
    split; gold chem `NMC`, data `self-lab`.
  - est.2024.113257: prismatic **graphite/LiMn2O4** cell, synthetic P2D data;
    gold chem `NMC`, data `self-lab`, valid `cross-cell holdout`.
  - ress.2022.109046: released code shows BIT/CALCE/MIT data and
    leave-one-battery-out splits with CNN/LSTM/Transformer backbones; gold
    (Cross-cutting / Shallow ML / NMC / CALCE / within-cell split) differs on
    all five fields.
  - access.2021.3068776 and the single-function reviews: gold method/data/valid
    values do not follow the codebook review-handling rule.
- **Gold-state inconsistency (one cell):** `papers_final.json` records
  jpowsour.2024.235609 `valid` = `experimental hardware`, while the round-1
  de-blind record (dispute_items.csv) and the original gold sheet used
  `online/real-vehicle`; the round-1 report reproduces only with the latter.
  Resolved at merge (see the reconciliation note below): the deposit's
  `out/gold_labels_30.csv` (corrected labels) is the canonical gold state.

Per-paper per-field values: `dispute_items_fulltext.csv` (same schema as
round 1). Round-1 sheets, report, and dispute table are unchanged.

### Status of the manuscript

Per the lead author's instruction (2026-11-01), the manuscript, README
headline numbers, and the journal-submission/Zenodo snapshot packages were
**not** modified in that round; propagation of the round-2 statistics into
those artifacts was deferred to a separate decision.

## Gold-state reconciliation at merge (2026-11-01, revision/reliability-round2-paper)

The round-2 report above was first computed against the original (pre-correction)
gold sheet, in which jpowsour.2024.235609 `valid` = `online/real-vehicle`. The
deposited `out/gold_labels_30.csv` carries the post-hoc corrected labels
(`experimental hardware`, matching `papers_final.json`). Re-running
`inter_rater_reliability.py` against the deposited gold — the state this deposit
pins — shifts only the two vs-gold `valid` kappas: B 0.287 -> 0.284 and
C 0.322 -> 0.318. Every B-C statistic (the protocol threshold measures), every
Krippendorff alpha, the bucket count (28/30), and all other vs-gold fields are
unchanged; `agreement_report_fulltext.csv` is the recomputed version and the
two table cells above reflect it. The round-1 report now regenerates
byte-identically from the deposit (corrected values 0.303/0.295 plus the
bucket row). This closes the gold-state item flagged above.
