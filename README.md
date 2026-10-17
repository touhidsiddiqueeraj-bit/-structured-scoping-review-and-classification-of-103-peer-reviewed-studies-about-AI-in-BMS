# Machine learning in battery management systems: a two-tier scoping review of 799 eligible studies with in-depth classification and validation audit

[![Paper](https://img.shields.io/badge/manuscript-ML--BMS--Review.pdf-blue)](ML-BMS-Review.pdf)
[![Corpus](https://img.shields.io/badge/dataset-799%20eligible%20%2B%20103%20classified-green)](ML-BMS-Corpus.xlsx)
[![Verification](https://img.shields.io/badge/metadata-Crossref%20DOI--resolved-orange)](#verification-methodology)

This repository is the complete, reproducible companion to the scoping review

> **Hussain Touhid Siddiquee, Syeda Salsabil Islam Ariya, Jasimul Islam Chowdhury**
> *Machine learning in battery management systems: a structured scoping review and classification of 103 peer-reviewed studies, 2019–2026.*
> Leading University, Sylhet, Bangladesh.

Every DOI in the **103-study classified subset** and the **conference descriptive set** was resolved directly against the [Crossref registry](https://api.crossref.org); the **799-record eligible corpus** is assembled entirely from Crossref-registered records with the mapping listed per record in `screening_log.csv`. Every number, figure, and table in the paper can be regenerated from the released datasets with the released code.

---

## Contents

| Artifact | Description |
|---|---|
| [`ML-BMS-Review.pdf`](ML-BMS-Review.pdf) / [`.docx`](ML-BMS-Review.docx) | The manuscript (32 pp., 10 sections, 8 figures, 11 tables, 117 Crossref-verified references) |
| [`ML-BMS-Corpus.xlsx`](ML-BMS-Corpus.xlsx) | Human-readable workbook: **Papers** (103, clickable DOI links), **Summary** (corpus counts), **Conference sensitivity** (14, clickable DOI links) |
| [`corpus/papers.csv`](corpus/papers.csv) | The 103-paper classified corpus (machine-readable; one row per study, 16 fields) |
| [`corpus/eligible_corpus.json`](corpus/eligible_corpus.json) | The 799-record rule-based eligible corpus (Tier 1; measured bibliometrics source) |
| [`corpus/screening_log.csv`](corpus/screening_log.csv) | Record-level screening provenance: status + reason for every decision — 1,550 pool records (883 retained at the title gate, 667 gate exclusions, 84 venue exclusions) plus 5 forced-seed entries |
| [`corpus/tagging_terms.json`](corpus/tagging_terms.json) | Released title-gate term lists (battery terms, ML terms) and the query-key → function-tag map |
| [`corpus/sensitivity_label_noise.json`](corpus/sensitivity_label_noise.json) | Label-noise scenario sensitivity of the headline validation counts (`sensitivity_label_noise.py`, seeded) |
| [`corpus/per_year_denominators.json`](corpus/per_year_denominators.json) | Crossref per-year result totals for the 30 queries (tested as trend denominators; documented as unusable — see manuscript §III-A) |
| [`corpus/protocol_audit.csv`](corpus/protocol_audit.csv) | Per-paper validation-protocol audit (strong flags under both definitions) |
| [`corpus/codebook.md`](corpus/codebook.md) | Classification codebook: field definitions, thresholds, absorbing rules |
| [`corpus/coding_protocol.md`](corpus/coding_protocol.md) | Independent re-coding protocol for coders 2–3 (blinding, dispute resolution, agreement thresholds) |
| [`corpus/reliability/coder_*_30.csv`](corpus/reliability) | Blind 30-paper coding sheets (stratified random draw, seed 20261017) |
| [`zenodo_upload.zip`](zenodo_upload.zip) | Ready-to-upload Zenodo deposit (data + codebook + reliability evidence + regeneration scripts; run from the extracted zip, verified) |
| [`corpus/conference_sensitivity.csv`](corpus/conference_sensitivity.csv) | The 14-paper conference set behind the 11-paper ML descriptive set |
| [`corpus/`](corpus) | Full pipeline: search, screening, verification, statistics, figures, document build |
| [`figures/`](figures) | All manuscript figures as 300-dpi PNGs |

## The corpus in one figure

![Method-family evolution](figures/fig3_method_evolution.png)

*Tier trend figure (Fig. 3 of the paper).* Left: measured eligible-corpus publications per year (capped retrieval; the 2024 dip is the documented retrieval hole). Right: classified-subset method-family papers by year — classical ML gives way to deep learning, then to physics-informed/hybrid approaches, with LLM-based studies appearing in 2025–2026.

## Headline findings

- **Two-tier evidence base.** Field-level bibliometrics are *measured* on a rule-based eligible corpus (799 records, no function quotas); in-depth classification and the validation audit live on the curated 103-study subset, with reconciliation checks between tiers (`consistency_check.py`).
- **Validation gap, quantified and tested.** Strong protocols (cross-cell / cross-chemistry / cross-domain holdout, online or fleet) cover 42 of 88 primary-application papers (48%; label-noise scenarios span 40–59%); 17 use within-cell or unsupervised k-fold splits that leak trajectory information; 23 papers rest on three public benchmarks (MATR/NASA/CALCE) and 36 on private laboratory cells.
- **Inter-coder reliability, measured.** Two independent coders blind-re-coded a 30-paper stratified sample: κ = 0.92 (function), 0.88 (method), 0.88 (data) pass; chemistry κ = 0.55 and validation κ = 0.48 fail the ≥ 0.66 threshold — traced to abstract-only evidence access (both resolved unreported splits toward weak codes); on the count-bearing strong/non-strong bucket the two coders agree 25/30 (83%). Sheets, `dispute_items.csv`, and the hash-tracked log are released; the two failing fields trigger v1.1 codebook patch candidates.
- **Physics-informed validation gap is exploratory, not settled.** 36% vs 52% strong-protocol share (Fisher p = 0.32); under the broader definition 59% vs 74%, OR 0.50, 95% CI 0.19–1.36, p = 0.19 — non-significant under both definitions, unadjusted confounding declared, and the family contrast stays non-significant in 95% of label-noise scenario draws.
- **Transportation-electrification cut + standards mapping.** Measured shares for vehicle/fleet-level work (≈2% of eligible records), a BMS-function-to-requirement map for UN GTR 20 / GB 38031 / ISO 26262, and a positioning table against prior reviews.
- **Foundation-model guardrails.** An LLM-based SOH **estimator** among the corpus's 2025–2026 entries is analyzed with its prior-art caveat stated (LLM-based battery estimation exists earlier outside the screened venues); Table 9 maps grounding, hallucination, uncertainty, latency, and safety-authority requirements — LLM components must never hold direct cell-level protection authority.
- **A reporting checklist.** Section 9.7 proposes **BMS-ML-RC**, a 12-item CONSORT/PRISMA-style reporting checklist (Table 11) for future machine-learning BMS studies.

## Figures

| Figure | Content |
|---|---|
| Fig. 1 | Corpus map: management function × method family (88 primary-application papers) |
| Fig. 2 | Study-selection flowchart with the two-tier design (3,000 → 1,550 → 883 → 799 Tier-1 eligible → 103 classified subset) |
| Fig. 3 | Two-panel: eligible-corpus publications per year + classified-subset method families (`fig3_method_evolution.png`) |
| Fig. 4 | Benchmark saturation: reuse of MATR/NASA/CALCE vs total output (`fig7_dataset_saturation.png`) |
| Fig. 5 | Milestones timeline (`fig6_timeline.png`) |

## Verification methodology

1. **Retrieval.** 30 bibliographic query strings × 4 date/sort passes against the Crossref REST API on **4–5 September 2026** → 3,000 records.
2. **Deduplication.** DOI-based → 1,550 unique records (1,450 duplicates removed).
3. **Relevance screening.** Title must contain battery-related **and** ML-related terms → 883 (−667); all 1,550 title-gate decisions are logged in `screening_log.csv`, and the term lists are released in `tagging_terms.json`.
4. **Venue/document-type screening.** Journal articles only; conference abstracts, preprints, non-scholarly venues excluded → 799 (−84).
5. **Rule-based two-tier selection.** Tier 1: venue-screened 799 eligible records, included in full without function quotas (`corpus/eligible_corpus.json`); Tier 2: curated full-text-classified 103-study subset (quota-era design replaced after the TTE review; record-level provenance in `corpus/screening_log.csv`, per-paper protocol audit in `corpus/protocol_audit.csv`, coding definitions in `corpus/codebook.md`).
6. **Verification.** Every DOI resolved directly against `api.crossref.org`; registry metadata compared to the record; per-paper citation counts (is-referenced-by-count, retrieved 5 September 2026) shipped in the dataset. External citations verified separately (`corpus/verify_external.py` → `corpus/external_verified.json`).

Full details: manuscript Section 2; screening funnel in `figures/fig2_prisma.png`.

## Reproducibility

### Requirements

- Python ≥ 3.10 with `openpyxl`, `matplotlib`, `python-docx`, `pandas`
- `curl` (network access to `api.crossref.org` and `api.semanticscholar.org`)
- LibreOffice (only for DOCX → PDF rendering)

### Pipeline

All commands run from the repository root. Every stage is cached/skipped-safe; outputs land in `corpus/` and `figures/`.

```bash
# 1. Search: 30 queries x 4 passes from Crossref (~3,000 records -> corpus/raw/*.json)
bash corpus/fetch_crossref.sh

# 2. Pool + dedupe + relevance gate + venue gate (-> corpus/pool.csv)
python3 corpus/pool.py

# 3. Screening: function quotas, landmark seeds, reclassification, curation
python3 corpus/screen.py
python3 corpus/fix_areas.py
python3 corpus/final_selection.py

# 4. Verification: resolve every DOI against Crossref, pull registry metadata
python3 corpus/verify_seeds.py
python3 corpus/verify_final.py

# 5. Statistics + consistency (every in-text number regenerates from here)
python3 corpus/build_stats.py
python3 corpus/consistency_check.py
python3 corpus/sensitivity_label_noise.py   # label-noise scenarios -> sensitivity_label_noise.json
python3 corpus/make_screening_log.py        # screening_log.csv (1,550 pool decisions) + tagging_terms.json

# 6. Figures (Figs. 1-8 as PNG, 300 dpi)
python3 corpus/make_fig1_heatmap.py   # Fig. 1 heatmap
python3 corpus/make_fig1.py           # Fig. 2 PRISMA funnel
python3 corpus/make_figs.py           # Figs. 3-6 + Fig. 8 timeline
python3 corpus/make_fig7_saturation.py# Fig. 7 benchmark saturation

# 7. Manuscript (citations [[doi]] -> numbered [n], tables, references)
python3 build_docx.py                 # -> ML-BMS-Review.docx
soffice --headless --convert-to pdf ML-BMS-Review.docx   # -> ML-BMS-Review.pdf

# 8. Spreadsheet companion (Papers / Summary / Conference sensitivity)
python3 corpus/make_xlsx.py           # -> ML-BMS-Corpus.xlsx

# 9. Reference audit: re-resolve every reference DOI and compare titles
python3 corpus/final_audit.py
```

`corpus/raw/` ships the 150 cached Crossref responses from the original run, so stages 1–2 can be replayed offline; the released `corpus/papers_final.json`, `corpus/verified.json`, and `corpus/stats.json` pin the exact state behind the published figures.

### Single source of truth

`corpus/consistency_check.py` recomputes the paper's key statistics (function totals, review reconciliation, fleet/online overlap, validation breakdowns, method-family year counts) from `papers_final.json`. If any future edit changes the corpus, re-run it before touching the text.

## Repository structure

```
.
├── ML-BMS-Review.docx / .pdf      # manuscript
├── ML-BMS-Corpus.xlsx             # Papers + Summary + Conference sensitivity
├── figures/                       # Figs. 1-8 (300 dpi PNG)
├── paper_part1.py / _2 / _3       # manuscript text as structured blocks ([[doi]] citations)
├── build_docx.py                  # DOCX builder: citation resolution, tables, references
├── corpus/
│   ├── fetch_crossref.sh, queries.txt, raw/     # search stage (cached responses)
│   ├── pool.py, screen.py, fix_areas.py, final_selection.py   # screening
│   ├── verify_seeds.py, verify_final.py, final_audit.py       # Crossref verification + audit
│   ├── papers.csv, papers_final.json, verified.json, stats.json
│   ├── conference_sensitivity.csv, conference_verified.json   # Section 3.5 sensitivity set
│   ├── make_figs.py, make_fig1.py, make_fig1_heatmap.py, make_fig7_saturation.py
│   ├── make_xlsx.py, consistency_check.py, build_stats.py
│   └── ...
└── README.md
```

## Dataset schema (papers.csv)

| Field | Meaning |
|---|---|
| `doi` / `title` / `authors` / `journal` / `year` / `volume` / `issue` / `pages` | Crossref-verified bibliographic metadata |
| `area` | Management function (8 values, incl. cross-cutting) |
| `method` | Dominant method family (13 values) |
| `chem` | Electrochemistry (NMC, LFP, LCO, Li-metal, Li-S, mixed, various) |
| `data` | Primary data source (own lab, public benchmark, EIS lab, fleet, simulation, …) |
| `valid` | Validation approach (cross-cell holdout, within-cell split, hardware, online/fleet, …) |
| `finding` / `limit` | Coded headline finding and principal limitation |
| `cites` | Crossref is-referenced-by-count at retrieval (5 September 2026) |

## Citation

If this corpus or checklist is useful, please cite the manuscript:

```bibtex
@article{siddiquee2026mlbms,
  title  = {Machine learning in battery management systems: a structured scoping review
            and classification of 103 peer-reviewed studies, 2019--2026},
  author = {Siddiquee, Hussain Touhid and Ariya, Syeda Salsabil Islam and
            Chowdhury, Jasimul Islam},
  year   = {2026},
  note   = {Manuscript and verified corpus; this repository}
}
```

## Provenance and AI disclosure

The bibliographic corpus is machine-curated and human-verified: classification fields were coded by the lead author from Crossref-verified metadata and reviewed by the co-author team (corrective pass; no formal inter-rater statistic is claimed — see manuscript §2.5). Writing-support and language-enhancement tools (ChatGPT, Grammarly, QuillBot) were used for grammar, readability, and restructuring; all technical content, analysis, interpretations, and research contributions are the authors' own (see the Acknowledgment section of the manuscript).
