# Machine learning in battery management systems: a two-tier scoping review of 799 eligible studies with in-depth classification and validation audit

Deposit of record for the manuscript above. The layout mirrors the project
repository: every release script runs unmodified from this directory.

## Reproduce the manuscript numbers
Python 3, standard library only (scipy optional for the Fisher p-value).
```
python3 corpus/rule_selection.py         # Tier 1: eligible corpus (799)
python3 corpus/build_stats.py            # classified subset (103) + stats.json
python3 corpus/make_screening_log.py     # record-level screening provenance
python3 corpus/make_protocol_audit.py    # per-paper validation-protocol audit
python3 corpus/consistency_check.py      # re-verifies every Section III count
python3 corpus/inter_rater_reliability.py --selftest   # k = 0.92/0.88/0.88 checks
python3 corpus/inter_rater_reliability.py              # agreement (needs filled sheets)
```

## Contents
- `corpus/papers.csv` -- the 103-study classified subset (machine-readable, 16 fields).
- `corpus/eligible_corpus.json` + `corpus/pool.csv` -- the 799-record rule-based
  eligible corpus and the 883-record screened pool behind it.
- `corpus/screening_log.csv` -- record-level screening provenance (status + reason for
  every inspected record).
- `corpus/protocol_audit.csv` -- per-paper validation-protocol audit (strong flags under
  both reported definitions).
- `corpus/codebook.md`, `corpus/coding_protocol.md` -- coding definitions, border and
  absorbing rules, and the independent re-coding protocol.
- `corpus/reliability/` -- locked blind coding sheets (coders 2-3), per-field Cohen
  kappa and Krippendorff alpha (`agreement_report.csv`), itemized disagreements
  (`dispute_items.csv`), hash-tracked log.
- `corpus/final_audit.json`, `conference_*`, `external_verified.json` -- Crossref
  verification audit trail for every reference.
- `figures/` -- manuscript figures regenerated from the released data.
- `out/gold_labels_30.csv` -- withheld released labels used by the reliability script.

## Citation
Siddiquee, H. T., Islam Ariya, S. S., & Chowdhury, J. I. (2026).
Machine learning in battery management systems: a two-tier scoping review of 799 eligible studies with in-depth classification and validation audit. Zenodo. https://doi.org/10.5281/zenodo.23436202

License: CC-BY-4.0.
