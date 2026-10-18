# Cover letter — new submission to IEEE Transactions on Transportation Electrification

Manuscript: "Machine learning in battery management systems: a two-tier scoping review of 799 eligible studies with in-depth classification and validation audit"

Dear Editor,

We submit a substantially reworked version of the manuscript previously considered as TTE-Reg-2026-09-3162 and rejected on 17 October 2026. The associate editors and all four reviewers identified weaknesses — a curated corpus read as a field measurement, an under-defined validation taxonomy with unreconciled counts, single-coder classification without a reliability statistic, thin transportation-electrification fit, and missing positioning against prior reviews — that were real. The rework addresses them structurally rather than cosmetically, and a point-by-point response dossier accompanies this submission. Because the earlier decision was a rejection, we present this as a new manuscript and disclose up front that it differs from the version previously reviewed: it is retitled, redesigned around a two-tier evidence base, and adds a reliability study, a safety-standards mapping, a validation audit with significance testing, and an explicit comparison with the closest prior reviews.

## Why this review belongs in TTE

The manuscript links every BMS machine-learning function to the requirement an electric-vehicle safety standard actually places on it — UN GTR 20's thermal-propagation early-warning window (Amendment 1, endorsed for WP.29 adoption in late 2026), GB 38031-2025's no-fire/no-explosion thermal-diffusion tests (effective July 2026), and ISO 26262:2018 extended to learned components by ISO/PAS 8800:2024. The review's measured finding is that the classified literature rests predominantly at cell level and in the laboratory (36 of 88 primary papers on the authors' own cells; real-vehicle data in 10; online validation in 8), one integration level below the pack- and vehicle-level questions these standards pose. That gap — and the reporting checklist proposed to close it — is written for the reader deciding how ML fits into a certifiable EV traction system.

## What the evidence base is

A rule-based eligible corpus of 799 peer-reviewed journal articles (798 dated 2020–2026 plus one early-access record stamped 2027) carries the measured bibliometrics; a curated 103-study classified subset (98 from the pool plus 5 individually retrieved seeds) carries the in-depth coding, with a 30-paper blind inter-coder reliability study, a per-paper protocol audit, and a label-noise sensitivity analysis with an explicitly stated Monte Carlo noise model. All screening provenance and analysis code are released in a Zenodo deposit (DOI: 10.5281/zenodo.23436202); every count in the paper can be regenerated from the deposit.

## Statement on scope and claims

All validation-practice rates and reliability statistics are reported for the classified subset and are not generalized to the field; caveats about the capped Crossref retrieval (including a documented January–May 2024 retrieval hole and publisher-tilt toward energy-storage venues), the curated subset, and the non-significance of the physics-informed validation contrast are stated in the manuscript rather than left to the reader. The review was not prospectively registered; this is stated explicitly.

## Declaration on the use of AI tools

During the preparation of this manuscript the authors used the following tools, each for a stated purpose: an AI language model (GLM, Z.ai) assisted in drafting and adapting the literature-pooling, analysis, and figure-generation scripts; OpenAI ChatGPT, Grammarly, and QuillBot were used for language editing (grammar, readability, and sentence restructuring). No AI tool decided study inclusion, and no AI tool assigned or altered any classification label; all screening decisions and all released labels were made by the authors, and the released reliability files document the coding evidence. The authors declare no conflicts of interest and received no specific funding for this work.

Respectfully,
Hussain Touhid Siddiquee (corresponding), Syeda Salsabil Islam Ariya, Jasimul Islam Chowdhury
Leading University, Sylhet, Bangladesh
