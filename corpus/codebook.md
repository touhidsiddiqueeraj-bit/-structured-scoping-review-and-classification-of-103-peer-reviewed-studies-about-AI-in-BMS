# BMS-ML Classification Codebook

This codebook defines every field of `corpus/papers.csv` with the threshold rules
used for coding, so independent coders can reproduce or challenge the released
labels. It exists because the review's conclusions are cross-tabulations of these
codes: reproducible codes are the floor for reproducible counts.

## Field definitions and decision rules

### `area` — management function (one primary value, eight values)
Assign the function of the paper's **headline contribution** (the system or result
the paper claims as its novelty), not auxiliary uses. Priority order when several
apply and the claim is genuinely cross-functional: `Cross-cutting`.
Values: `State estimation (SOC)`, `Health estimation (SOH)`, `Prognostics (RUL)`,
`Charging control`, `Thermal management`, `Fault & safety`,
`Cell balancing & ECM`, `Cross-cutting`.
*Border rule:* an estimator used *by* a controller (e.g., SOC as charging input)
is coded to the controller only if control is the headline claim.
*Review handling:* a paper that synthesizes only a single function's literature
keeps that function with method family `Review / perspective`; a paper whose
contribution is a cross-function classification framework is coded to its
dominant technique family (and is flagged as review-type in the data table).

### `method` — dominant method family
Assign the family of the model that carries the headline claim.
`Shallow ML` (GPR/SVR/ensembles/shallow nets on engineered features) |
`Deep learning` (LSTM/GRU/CNN/transformer/graph/autoencoder) |
`Physics-informed` (physics in training objective) |
`Hybrid physics+ML` (physics model sequentially or architecturally coupled, not
in the loss) | `Filter-based hybrid` (learned model embedded in a Kalman-family
filter or observer) | `Meta-heuristic-optimized DL` (evolutionary/SWA/hyper-
heuristic tuning of networks) | `Bayesian optimization` |
`Optimization-augmented control` (MPC/surrogate co-design) |
`Reinforcement learning` | `Transfer learning` (method family only if the
headline is a transfer architecture; a transfer *result* keeps the base family) |
`Graph neural network` | `Foundation model / LLM` (pretrained or LLM components
in the headline system) | `Review / perspective`.
*Border rule (physics-informed vs hybrid):* physics enters the loss ⇒
`Physics-informed`; physics model runs alongside/embedded but no loss term ⇒
`Hybrid physics+ML`; physics model inside a KF/UKF/EKF wrapper ⇒
`Filter-based hybrid`.

### `chem` — electrochemistry of the headline system
Single chemistry (e.g. `NMC`, `LFP`, `LCO`, `Li-metal`, `Li-S`) if the headline
system uses one; `mixed` if results pool several; `various` if unspecified.

### `data` — primary data source of the headline result (one value)
`self-lab` (authors' own cycling) | `Severson-MATR` | `NASA` | `CALCE` |
`EIS-lab` (impedance datasets) | `real-vehicle` (vehicle/fleet-derived field
data) | `simulation` | `review` | `mixed` (≥2 sources, no dominant one).
*Border rule:* public dataset "plus a small self-collected validation set" is
coded to the public dataset if headline metrics are reported on it.

### `valid` — validation protocol of the headline claim (four definitions)
1. `within-cell split` — train/test segments drawn from the same cycling
   trajectory (any fractions, any resampling).
2. `cross-validation` (k-fold/unsupervised) — folds over samples of the same
   trajectories without cell-level isolation.
3. Strong protocols:
   - `cross-cell holdout` — every test cell is entirely absent from training.
   - `cross-chemistry holdout` — test chemistry absent from training.
   - `cross-domain holdout` — test domain (duty cycle, temperature regime,
     application, lab) absent from training.
   - `online/real-vehicle` — deployed system evaluated on live vehicle fleet use.
4. Environment-only codes (say nothing about isolation; never counted as
   strong protocols):
   - `experimental hardware` — physical test stand / hardware-in-the-loop,
     isolation unspecified.
   - `simulation plus hardware spot-check` — headline validation simulation
     with limited hardware checks.
   - `simulation` — headline validation in simulation only.
   - `case study` — single-system narrative demonstration.
   - `review synthesis` — no primary validation.

**Absorbing rule:** a paper is credited with the *strongest* protocol it reports
for its headline claim (strongest among the four strong protocols, then
environment codes). Protocol *and* environment both reported (e.g. cross-cell
holdout plus hardware-in-the-loop checks) → the protocol is coded; SaH honesty
requires checking protocol results are the headline numbers.

**Strong-protocol grouping used in Section III:** {`cross-cell holdout`,
`cross-chemistry holdout`, `cross-domain holdout`, `online/real-vehicle`} =
`strong_protocol_only`; the historical broader grouping additionally counts
`experimental hardware` and is reported alongside (not mixed).

### `finding` / `limit`
One sentence each, from the abstract + full text: the headline quantitative or
binary finding; the principal stated or evident limitation. Coded verbatim from
the paper, no editorializing.

## Reliability plan -> executed outcome

**Executed 2026** (coder 2 + coder 3, blind, per `coding_protocol.md`): the
30-paper stratified sample was independently re-coded. Blind inter-coder
agreement: `area` κ = 0.92 / α = 0.92, `method` κ = 0.88 / α = 0.88, `data`
κ = 0.88 / α = 0.88 (pass); `chem` κ = 0.55, `valid` κ = 0.48 (fail — both
below the 0.66 threshold). The `chem`/`valid` failures trace to evidence
access (23 and 28 of 30 sample papers coded from abstracts only; split
protocols and chemistry are rarely stated there) rather than random
disagreement: on the strong-protocol/non-strong bucket that corpus counts
rest on, the two coders agree 25/30 (83%). Per the protocol, both
below-threshold fields trigger these v1.1 patch candidates (not applied to
released labels):

1. `method`: explicit not-ML code for physics-only estimators.
2. `area`: production/quality function for manufacturing-QC papers.
3. `data`: vehicle vs stationary field split; self-lab/EIS-lab tie-break.
4. `valid`: a dedicated `not reported` code instead of weak-code fallback.
5. Reviews: fixed reading for cross-function reviews before κ on
   `area`/`method` is interpreted for review-type papers.

Full sheets, the itemized disagreement table (`dispute_items.csv`), and the
hash-tracked log are released in `corpus/reliability/`.

**Round 2 executed 2026-11-01** (full-text re-coding of the same 30-paper
sample under the v1.1 patch below, per `coding_protocol.md` §6; shared
evidence base, see `reliability_log.md`): B-C κ = 0.96 (`area`), 1.00
(`method`), 1.00 (`chem`), 0.96 (`data`), 0.92 (`valid`) — all five fields
pass the 0.66 threshold at the 0.80 strong level; strong/non-strong
validation bucket 28/30 (93%). Released labels unchanged; vs-gold deltas are
itemized in `corpus/reliability/dispute_items_fulltext.csv` as candidate
corrections for the lead author.

## Codebook v1.1 patch (2026-11-01)

Applied per the 2026-10-17 dispute-session outcomes (reliability_log.md,
"Dispute session", item 2) ahead of the round-2 re-coding, as prescribed by
`coding_protocol.md` §6 ("below .66 triggers codebook repair and one re-coded
subset"). The v1.0 vocabulary above remains the vocabulary of the released
labels (unchanged); v1.1 governs re-coding rounds only and adds:

1. `method` — new code `Not ML (physics/classical)`: the headline method
   contains no learned component (round-2 scope: est.2023.106931,
   est.2023.107575).
2. `area` — new code `Production & quality`: manufacturing/quality functions
   (coating, formation, grading QC) that are not in-battery management
   functions (conengprac.2022.105202, jechem.2025.04.025, batt.202300046).
3. `data` — `real-vehicle` is restricted to vehicle/fleet-derived field data;
   new code `field-stationary` for stationary-storage field data
   (jpowsour.2024.235609). Tie-break: a study that creates its own EIS
   dataset is coded `EIS-lab` (impedance is the defining observation);
   `self-lab` is reserved for own non-EIS cycling (s41467-020-15235-7).
4. `valid` — new code `not reported`: no train/test protocol described in the
   accessible text. Unreported protocols are no longer forced into
   `within-cell split` / `cross-validation (k-fold)` weak-code fallbacks (the
   two coders' divergent fallbacks drove the round-1 κ_valid = 0.48 failure).
   `not reported` counts as non-strong in the strong/non-strong bucket.
   Review-type papers keep `review synthesis`.
5. Reviews — fixed reading for cross-function reviews: `area` = the single
   domain function if the review synthesizes one function's literature, else
   the domain function under rule 2 for production reviews, else
   `Cross-cutting`; `method` = `Review / perspective` (the contribution is the
   synthesis; the dominant reviewed technique family is recorded in the sheet
   comment). κ on `area`/`method` for review-type papers is interpreted with
   this rule.

## Boundary examples (abridged)
- PSO-tuned LSTM SOC with UKF wrapper → `Filter-based hybrid` (not meta-heuristic).
- Domain-adversarial training for SOH → `Transfer learning`.
- PINN heat generation → `Physics-informed`; physics-constrained autoencoder SOH
  → `Physics-informed`; ECM+ML SOC from EIS → `Hybrid physics+ML`.
- 80/20 split within one cell's discharge curve → `within-cell split`.


## Baseline-comparison screen (added in revision; field 7)

Motivation: BMS-ML-RC item 6 demands a classical baseline on identical data, but the
original six coding fields never recorded whether studies actually provide one.

Abstract-level values (coded from indexed abstracts; released codes in
abstract_probe_codes.py):
- `none` - no model-based or classical reference method named as a comparator
- `mentioned` - such a baseline is named (EKF/UKF/Kalman family, observer,
  equivalent-circuit or physics-based model, coulomb counting, or a classical
  regressor such as GPR/SVR), without a stated same-data quantitative result
- `stated_samedata` - the abstract states the comparison on the same data with a
  quantitative result

Bounds: a full text may compare baselines its abstract omits, so abstract-level
codes are lower bounds on comparison practice and exact measures of comparison
visibility. ScienceDirect-withheld abstracts cannot be screened (49 of the 88
primary papers at the September 2026 retrieval).

Full-text rubric for future work:
- `none` - no model-based baseline
- `weak` - baseline named, but comparison not on identical data or not quantitative
- `fair` - same data, quantitative comparison against a model-based baseline

## Recall audit and power analysis (added in revision)

- `recall_audit.py` / `recall_audit.json`: capture rate of the 1,550-record
  retrieval against the deposited reference lists of the 15 included reviews and
  6 seeds; denominators restricted to title-gate-positive, DOI-bearing references
  dated >= 2020; titles/years resolved by DOI where publishers deposit neither.
- `power_analysis.py` / `power_analysis.json`: minimum-detectable-effect analysis
  for the physics-informed vs other validation-stringency contrast (analytic
  two-proportion power, validated against Fisher-exact Monte Carlo).
- `abstract_probe.py` / `abstract_probe_raw.json`: seed-pinned 40-record sample of
  the 799-record eligible pool plus the 88 primary papers, with abstracts fetched
  from Crossref, OpenAlex, and Semantic Scholar (cached under raw_cache/).
