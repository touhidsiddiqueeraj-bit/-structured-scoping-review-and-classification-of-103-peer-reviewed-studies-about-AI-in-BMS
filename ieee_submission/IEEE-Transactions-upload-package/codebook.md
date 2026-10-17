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

## Reliability plan
One author codes; co-authors correctively review. No inter-rater statistic is
claimed for the released labels. To upgrade them: pick a random 30-paper sample
(stratified by function and year), re-code blind with this codebook, report
per-field percent agreement and Krippendorff's α (nominal) or Cohen's κ per
field, and publish the conflict-resolved table as a dataset patch.

## Boundary examples (abridged)
- PSO-tuned LSTM SOC with UKF wrapper → `Filter-based hybrid` (not meta-heuristic).
- Domain-adversarial training for SOH → `Transfer learning`.
- PINN heat generation → `Physics-informed`; physics-constrained autoencoder SOH
  → `Physics-informed`; ECM+ML SOC from EIS → `Hybrid physics+ML`.
- 80/20 split within one cell's discharge curve → `within-cell split`.
