#!/usr/bin/env python3
"""Assemble the Zenodo upload package for the review's released artifacts.

Deposit mirrors the repository layout (corpus/, figures/, out/) so every
released script runs unmodified from the extracted zip: absolute paths are
rewritten to CWD-relative ones. Includes Zenodo API metadata, deposit README,
license, and zip. The only manual step afterwards: upload + get DOI.
"""
import os
import json, os, shutil, zipfile, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = f'{ROOT}/zenodo_upload'
ZIP = f'{ROOT}/zenodo_upload.zip'
ABS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TITLE = ('Machine learning in battery management systems: a two-tier scoping '
         'review of 799 eligible studies with in-depth classification and validation audit')

CREATORS = [
    {'name': 'Siddiquee, Hussain Touhid', 'affiliation': 'Leading University, Sylhet, Bangladesh'},
    {'name': 'Islam Ariya, Syeda Salsabil', 'affiliation': 'Leading University, Sylhet, Bangladesh'},
    {'name': 'Chowdhury, Jasimul Islam', 'affiliation': 'Leading University, Sylhet, Bangladesh'},
]

DATA = [
    'corpus/papers.csv',
    'corpus/papers_final.json',
    'corpus/eligible_corpus.json',
    'corpus/pool.csv',
    'corpus/screening_log.csv',
    'corpus/tagging_terms.json',
    'corpus/per_year_denominators.json',
    'corpus/sensitivity_label_noise.json',
    'corpus/protocol_audit.csv',
    'corpus/conference_sensitivity.csv',
    'corpus/conference_verified.json',
    'corpus/external_verified.json',
    'corpus/standards_refs.json',
    'corpus/final_audit.json',
    'corpus/stats.json',
    'corpus/seeds.json',
    'corpus/recall_audit.json',
    'corpus/power_analysis.json',
    'corpus/abstract_probe_raw.json',
    'corpus/abstract_probe.json',
    'corpus/codebook.md',
    'corpus/coding_protocol.md',
    'corpus/reliability/coder_A_30.csv',
    'corpus/reliability/coder_B_30.csv',
    'corpus/reliability/coder_C_30.csv',
    'corpus/reliability/agreement_report.csv',
    'corpus/reliability/dispute_items.csv',
    'corpus/reliability/reliability_log.md',
    'out/gold_labels_30.csv',
]

CODE = [
    'corpus/rule_selection.py',
    'corpus/build_stats.py',
    'corpus/consistency_check.py',
    'corpus/pool.py',
    'corpus/crossref_year_counts.py',
    'corpus/sensitivity_label_noise.py',
    'corpus/make_screening_log.py',
    'corpus/make_protocol_audit.py',
    'corpus/make_coding_sample.py',
    'corpus/inter_rater_reliability.py',
    'corpus/make_figs.py',
    'corpus/make_fig1.py',
    'corpus/make_fig1_heatmap.py',
    'corpus/make_fig7_saturation.py',
    'corpus/recall_audit.py',
    'corpus/power_analysis.py',
    'corpus/abstract_probe.py',
    'corpus/abstract_probe_codes.py',
]

FIGURES = ['fig1_function_method_map.png', 'fig2_prisma.png',
           'fig3_method_evolution.png', 'fig7_dataset_saturation.png']


def localize(src_text):
    """Rewrite absolute repo paths to CWD-relative so the zip runs standalone."""
    return src_text.replace(ABS, '')


def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    for src in DATA:
        dst = os.path.join(OUT, src)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(os.path.join(ROOT, src), dst)
    for c in CODE:
        text = localize(open(os.path.join(ROOT, c)).read())
        p = os.path.join(OUT, c)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'w').write(text)
    # cached Crossref/OpenAlex/SemanticScholar responses so the recall audit and
    # abstract probes re-run offline, exactly as published
    for sub in ('corpus/raw_cache', 'corpus/raw_cache/openalex', 'corpus/raw_cache/semanticscholar'):
        src_dir = os.path.join(ROOT, sub)
        if os.path.isdir(src_dir):
            os.makedirs(os.path.join(OUT, sub), exist_ok=True)
            for f in os.listdir(src_dir):
                if f.endswith('.json'):
                    shutil.copy2(os.path.join(src_dir, f), os.path.join(OUT, sub, f))
    os.makedirs(f'{OUT}/figures', exist_ok=True)
    for f in FIGURES:
        shutil.copy2(f'{ROOT}/figures/{f}', f'{OUT}/figures/{f}')
    shutil.copy2(f'{ROOT}/zenodo_asset/LICENSE', f'{OUT}/LICENSE')

    abstract = (
        'Machine learning (ML) has become a load-bearing component of modern battery '
        'management systems (BMS), yet the validation practices behind the literature\'s '
        'accuracy claims are rarely examined at corpus scale. This deposit contains '
        'the complete evidence base and analysis pipeline of a two-tier structured scoping '
        'review: a rule-based eligible corpus of 799 peer-reviewed journal articles '
        '(798 dated 2020-2026 plus one early-access record stamped 2027; the classified '
        'subset of 103 adds five individually verified seed studies, one dated 2019) '
        'with record-level screening provenance (corpus/screening_log.csv, '
        'all 1,550 title-gate decisions plus 5 forced-seed entries), an in-depth classified subset of 103 studies '
        '(corpus/papers.csv) with a per-paper validation-protocol audit '
        '(corpus/protocol_audit.csv), a conference descriptive set, the classification '
        'codebook (corpus/codebook.md), and a blind 30-paper inter-coder reliability '
        'study (locked coding sheets, per-field Cohen\'s kappa and Krippendorff\'s alpha, '
        'itemized disagreement table, corpus/reliability/), a recall audit against the '
        'included reviews\' reference lists with cached API responses (corpus/recall_audit.py/.json, '
        'corpus/raw_cache/), a minimum-detectable-effect analysis (corpus/power_analysis.py/.json), '
        'and abstract-level representativeness and baseline-comparison probes '
        '(corpus/abstract_probe*.py/.json). Every count, figure, and '
        'cross-tabulation in the manuscript regenerates from this deposit: extract it, '
        'enter the top directory, and run the commands in README.md. CC-BY-4.0.')
    meta = {
        'title': TITLE,
        'upload_type': {'main_type': 'dataset'},
        'publication_date': time.strftime('%Y-%m-%d'),
        'creators': CREATORS,
        'description': abstract,
        'access_right': 'open',
        'license': 'cc-by-4.0',
        'keywords': ['battery management systems', 'machine learning', 'scoping review',
                     'validation practice', 'electric vehicles', 'reliability study'],
        'doi': '10.5281/zenodo.23436202',
        'notes': 'Companion GitHub repository hosts the same artifacts in development form.',
        'related_identifiers': [{
            'identifier': 'https://github.com/touhidsiddiqueeraj-bit/'
                          '-structured-scoping-review-and-classification-of-103-peer-reviewed-'
                          'studies-about-AI-in-BMS',
            'relation': 'isSupplementingBy', 'resource_type': None,
        }],
    }
    # Zenodo relation vocab: our deposit supplements the repo? The deposit IS the
    # dataset for the paper; repo relation is 'isIdenticalTo'-free, keep simple:
    meta['related_identifiers'][0]['relation'] = 'isSupplementedBy'
    json.dump(meta, open(f'{OUT}/zenodo_metadata.json', 'w'), indent=2)

    lines = [
        '# ' + TITLE,
        '',
        'Deposit of record for the manuscript above. The layout mirrors the project',
        'repository: every release script runs unmodified from this directory.',
        '',
        '## Reproduce the manuscript numbers',
        'Python 3, standard library only (scipy optional for the Fisher p-value).',
        '```',
        'python3 corpus/rule_selection.py         # Tier 1: eligible corpus (799)',
        'python3 corpus/build_stats.py            # classified subset (103) + stats.json',
        'python3 corpus/make_screening_log.py     # record-level screening provenance',
        'python3 corpus/make_protocol_audit.py    # per-paper validation-protocol audit',
        'python3 corpus/consistency_check.py      # re-verifies every Section III count',
        'python3 corpus/inter_rater_reliability.py --selftest   # k = 0.92/0.88/0.88 checks',
        'python3 corpus/inter_rater_reliability.py              # agreement (needs filled sheets)',
        '```',
        '',
        '## Contents',
        '- `corpus/papers.csv` -- the 103-study classified subset (machine-readable, 16 fields).',
        '- `corpus/eligible_corpus.json` + `corpus/pool.csv` -- the 799-record rule-based',
        '  eligible corpus and the 883-record screened pool behind it.',
        '- `corpus/screening_log.csv` -- record-level screening provenance (status + reason for',
        '  every inspected record).',
        '- `corpus/protocol_audit.csv` -- per-paper validation-protocol audit (strong flags under',
        '  both reported definitions).',
        '- `corpus/codebook.md`, `corpus/coding_protocol.md` -- coding definitions, border and',
        '  absorbing rules, and the independent re-coding protocol.',
        '- `corpus/reliability/` -- locked blind coding sheets (coders 2-3), per-field Cohen',
        '  kappa and Krippendorff alpha (`agreement_report.csv`), itemized disagreements',
        '  (`dispute_items.csv`), hash-tracked log.',
        '- `corpus/final_audit.json`, `conference_*`, `external_verified.json` -- Crossref',
        '  verification audit trail for every reference.',
        '- `corpus/recall_audit.py/.json` + `corpus/raw_cache/` -- retrieval recall audit against',
        '  the included reviews\' reference lists, with cached API responses.',
        '- `corpus/power_analysis.py/.json` -- minimum-detectable-effect analysis for the',
        '  physics-informed validation contrast.',
        '- `corpus/abstract_probe*.py/.json` -- seed-pinned 40-record pool sample and the',
        '  88-paper baseline-comparison screen, with released codes.',
        '- `figures/` -- manuscript figures regenerated from the released data.',
        '- `out/gold_labels_30.csv` -- withheld released labels used by the reliability script.',
        '',
        '## Citation',
        'Siddiquee, H. T., Islam Ariya, S. S., & Chowdhury, J. I. (' + time.strftime('%Y') + ').',
        TITLE + '. Zenodo. https://doi.org/10.5281/zenodo.23436202',
        '',
        'License: CC-BY-4.0.',
    ]
    open(f'{OUT}/README.md', 'w').write('\n'.join(lines) + '\n')

    if os.path.exists(ZIP):
        os.remove(ZIP)
    with zipfile.ZipFile(ZIP, 'w', zipfile.ZIP_DEFLATED) as z:
        for base, _, files in os.walk(OUT):
            for f in sorted(files):
                p = os.path.join(base, f)
                z.write(p, os.path.relpath(p, OUT))
    print('package:', OUT, '| files:', sum(len(fs) for _, _, fs in os.walk(OUT)))
    print('zip:', ZIP)


if __name__ == '__main__':
    main()
