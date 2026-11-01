# Response plan — TTE-Reg-2026-10-3720 (rejected)

**Manuscript:** *Machine learning in battery management systems: a two-tier
scoping review of 799 eligible studies with in-depth classification and
validation audit of 103 studies*
**Decision:** Reject (Editor-in-Chief Prof. Fei Gao, relaying two
Associate-Editor reports).
**This branch:** `revision/tte-3720-reaudit` (based on `post-review-fixes`).

AE comments below are **paraphrased** from the decision email; each maps to a
concrete, verifiable fix. Two kinds of fixes are separated honestly:
**[DONE]** exists in this repository now, **[INSTRUMENT READY — co-author
action]** the tooling is complete but the numbers it produces require the
co-author re-coding run (5 working days of coder time).

---

## AE-1: "the review needs more technical depth… has a
statistical-analysis-of-publication-data character… transportation findings
are limited" (venue fit)

**Diagnosis.** The AE read the paper as a bibliometric analysis of publication
metadata with thin transportation content. That reading is partially fair: the
reliability evidence forced the validation audit (the paper's technical core)
to be reported as a bounded range, which pushed the transportation-relevant
findings into hedged, subset-scoped statements.

**Response.**

1. **[INSTRUMENT READY]** A dedicated *Transportation-specific synthesis*
   subsection (§4 of `reaudit/Revised_Methods_Reliability.tex`) built on three
   new coding variables that do not exist in the v1 instrument:
   - **V11 deployment-TRL ladder (0–4):** offline lab → HIL → real
     vehicle/field data → onboard demonstrated. Every study's validation is
     placed on this ladder, so "vehicle-level validation" becomes a measured
     count, not a narrative claim.
   - **V12 onboard feasibility:** none / qualitative / quantitative latency–
     memory–footprint budget / measured on target hardware — the
     BMS-MCU-constraint question TTE readers care about.
   - **V14 transportation relevance:** generic-battery vs EV/HEV vs other
     transport, coded by validation context, not title claims.
2. **[DONE]** The standards mapping (GTR 20, GB 38031-2025, ISO 26262,
   ISO-PAS 8800, ISO 21448) is already in the submitted manuscript (§9.4);
   the synthesis subsection now *uses* V10 (robustness stress) and the V11
   ladder to connect the audit findings to those safety requirements instead
   of citing them as context.
3. **[DONE]** The paper's contribution is restated as: (i) a transparent,
   reliability-measured validation audit of 103 studies — a methodological
   contribution in itself, and (ii) measured, transportation-specific
   validation-practice rates. The bibliometric tier is explicitly positioned
   as context, not contribution.

## AE-2 (item 1): "kappa = 0.48" — the validation-protocol field

**What the AE saw.** The submitted manuscript reports the blind 30-paper
re-coding (two co-author coders, abstract-level access): function κ = 0.92,
method κ = 0.88, data source κ = 0.88, chemistry κ = 0.55, **validation
protocol κ = 0.48**. The manuscript itself discloses that the coders reached
full text for only 7/30 and 2/30 papers.

**Response — full re-audit with a hardened instrument. [INSTRUMENT READY]**

The v2 protocol in `reaudit/` (see `reaudit/README.md`) replaces the
abstract-level probe:

- **Full-text coding of all 103 studies** (v1's failure mode — abstract-level
  access on a field that is rarely stated in abstracts — is designed out).
- **14 validation variables** (V1–V14) with exhaustive code sets, decision
  rules for multi-experiment/multi-target studies, and worked examples for
  every known edge case; "not reported" is an explicit admissible code, so
  coders never infer silently.
- **Ordinal ladders re-anchored to demonstrable evidence** (code the level
  that is *demonstrated with results*, not claimed); top-two levels require a
  verbatim quotation with page/section reference.
- **Calibration gate before the main run:** 12-paper stratified pilot,
  per-variable κ ≥ 0.70 required to proceed; below the gate the *codebook* is
  revised and the pilot repeated — codes are never negotiated.
- **Adjudication:** third senior author, 48-hour turnaround, every resolution
  logged with rationale + codebook clause (log published as a supplement).
- **Reporting:** per-variable raw agreement, Cohen's κ, PABAK (several
  categories are rare and prevalence-dependent), linearly/quadratically
  weighted κ for the six ordinal variables, bootstrap 95% CIs (10,000
  resamples), confusion matrices; Fleiss's κ if a third coder is added; a
  pre-declared adjacent-category collapse rule (fires only if one adjacent
  pair contributes >50% of disagreements — V6 and V11 are the predicted pairs).
- **Transparency:** the original κ = 0.48 is retained and reported as the
  initial audit; the re-audit is presented as instrument refinement, not as
  a replacement of an inconvenient number. The Methods text that does this is
  §1 of `reaudit/Revised_Methods_Reliability.tex`.

## AE-2 (item 2): recall-audit limitations

**Response.**

1. **[DONE]** Quantified recall against an external anchor (released):
   17.3%/16.4% capture of included reviews' reference lists; per-query
   design caps documented (`corpus/` recall-audit construction, Supplementary
   S4).
2. **[DONE]** Retrieval-depth pilot (released): six query families cursor-paged
   to depth 200 → 1,500 title-gated records absent from the 1,550-pool
   (1,406 venue-eligible), ~5,000 net new extrapolated — establishing the
   top-20 cap, not the registry, as the binding constraint
   (`corpus/retrieval_depth_pilot.py/.json`).
3. **[INSTRUMENT READY]** *Search recall assurance* subsection (§3 of
   `reaudit/Revised_Methods_Reliability.tex`): backward–forward citation
   chaining from all included reviews, hand-search of the five core venues
   (J. Power Sources, eTransportation, J. Energy Storage, TTE, TTEV), and a
   30-record known-must-find benchmark with a pre-declared recall target —
   executed and reported in the next submission.

## AE-2 (item 3): selection of the 103 studies needs stronger justification;
treat selection bias

**Response. [INSTRUMENT READY]**

*Selection of studies for the in-depth audit* (§2 of
`reaudit/Revised_Methods_Reliability.tex`): explicit tier-2 inclusion criteria
table (method-claim prominence, data availability, transportation relevance),
a PRISMA-ScR flow diagram with per-step reasons (799 eligible → 103
classifiable), and a **sensitivity analysis** re-running the headline rates
excluding borderline studies (review-type syntheses, the RFID-venue paper, the
single 2019 forced seed) so readers can see which conclusions survive. The
subset-scoped wording already in the submitted manuscript stays.

## AE-2 (item 4): more EV-specific BMS, vehicle-level validation, onboard
implementation, transportation-safety emphasis

**Response.** Same mechanism as AE-1: V11/V12/V14 turn each of these into a
coded, countable property of every one of the 103 studies, and the
*Transportation-specific synthesis* subsection aggregates them
(vehicle-level-validation rate, onboard-feasibility-discussion rate,
EV-share of validation contexts, robustness-to-sensor-noise rate, and the
safety-requirements linkage). **[INSTRUMENT READY]**

---

## Status board

| Fix | Status | Where |
|---|---|---|
| Codebook v2.0 (V1–V14, gates, adjudication) | DONE (instrument) | `reaudit/Validation_Audit_Codebook_v2.docx` |
| Coding workbook (locked dropdowns, live κ calculator) | DONE (instrument) | `reaudit/Coding_Workbook_v2.xlsx` |
| Scoring script (κ, PABAK, weighted, Fleiss, bootstrap, collapse rule) | DONE + self-tested | `reaudit/kappa_analysis.py` |
| Revised Methods text (4 subsections) | DONE (template; numbers pending re-coding) | `reaudit/Revised_Methods_Reliability.tex` |
| Pilot re-coding (12 studies, gate κ ≥ 0.70) | **co-author action, ~2 h per coder** | workbook `Coder1`/`Coder2` sheets |
| Full double re-coding (103 studies) | **co-author action, ~25–35 min/study** | same |
| Adjudication + scoring | **co-author + script** | `Adjudication_Log` + `kappa_analysis.py` |
| Merge Methods into manuscript, fill numbers | after scoring | `ieee_submission/tex/mlbms.tex` |
| Recall assurance run (chaining, hand-search, benchmark) | next submission cycle | per §3 template |
| Sensitivity analysis excluding borderline studies | next submission cycle | per §2 template |

## Venue note (not part of the AE response)

Both rejections (2026-09-3162 and 2026-10-3720) raised venue fit. Before the
next submission, the re-audited paper is a materially stronger fit for
battery/energy-storage venues with review sections (J. Power Sources,
eTransportation, J. Energy Storage, Renewable & Sustainable Energy Reviews)
than for TTE's transportation-electrification scope; the re-audit package is
venue-neutral and reusable as-is.
