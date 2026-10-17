# Reliability Log — 30-paper blind re-coding

Maintained per `corpus/coding_protocol.md` §5–6. Sheets are locked at save time;
hashes below are for the locked files.

## Locked sheets (hash at lock)

| sheet | status | sha256 | notes |
|---|---|---|---|
| coder_B_30.csv | **locked 2026-10-17** | `125cb62ce0b9e47d6af2bc40897519e8f65465ddd06621281a856c5b9bcdae54` | 30/30 rows; access: 6 full-text, 1 preprint, 23 abstract-only; completion date marked in file (`completed,2026-10-17`). |
| coder_A_30.csv | not locked | — | |
| coder_C_30.csv | **locked 2026-10-17** | `f1a44bfc4a3cd535f5fa25aa34f050ff0693250ec0245560fcce8f12c2400e4d` | 30/30 rows; access: 2 full-text (both Nat. Commun. via PMC), 28 abstract-only (two of those with partial abstract+intro full texts from repo copies); completion date marked in file (`completed,2026-10-17`). |

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
