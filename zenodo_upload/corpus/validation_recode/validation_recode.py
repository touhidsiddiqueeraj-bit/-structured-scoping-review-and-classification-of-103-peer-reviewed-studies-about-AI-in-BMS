#!/usr/bin/env python3
"""Round-6 P3: analyze the independent validation-field re-code (coder D).

Coder D = the AI research assistant that maintains this repository, re-coding the
`valid` field of every primary paper for which retrievable evidence exists
(open-access full text where available, else the indexed abstract), per the
codebook rubric (strongest-protocol absorbing rule; `not reported` where the
evidence does not state a protocol). Codes were assigned from the evidence
worksheet BEFORE any comparison with the released labels.

Outputs: corpus/validation_recode/validation_recode.json + console summary.
"""
import csv, json, os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))            # corpus/validation_recode
REPO = os.path.dirname(os.path.dirname(HERE))                # repo root
CORPUS = os.path.join(REPO, 'corpus')

STRONG = {'cross-cell holdout', 'cross-chemistry holdout', 'cross-domain holdout',
          'online/real-vehicle'}

def kappa(a, b):
    if len(a) != len(b) or not a:
        return None
    labels = sorted(set(a) | set(b))
    n = len(a)
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    cnt_a, cnt_b = Counter(a), Counter(b)
    pe = sum(cnt_a[l] * cnt_b[l] for l in labels) / (n * n)
    if pe == 1:
        return None
    return (po - pe) / (1 - pe)

def wilson(p, n, z=1.96):
    if n == 0:
        return None
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    hw = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / den
    return [max(0.0, c - hw), min(1.0, c + hw)]

def main():
    # released labels
    pa = {}
    with open(os.path.join(CORPUS, "protocol_audit.csv")) as f:
        for r in csv.DictReader(f):
            pa[r['doi']] = r  # validation_coded, strong_protocol_only, primary_or_review
    # the 88 true primaries = probeB list
    probe = json.load(open(os.path.join(CORPUS, "abstract_probe_raw.json")))
    primary_dois = [e['doi'] for e in probe['probeB_primary_papers']]

    # coder D sheet
    codes = {}
    with open(os.path.join(HERE, 'coder_D_validation.csv')) as f:
        for r in csv.DictReader(f):
            codes[r['doi']] = r

    rows = []
    for doi in primary_dois:
        rel = pa.get(doi, {})
        cd = codes.get(doi)
        rows.append({
            'doi': doi,
            'released_code': rel.get('validation_coded', ''),
            'released_strong': rel.get('strong_protocol_only', ''),
            'coded': bool(cd),
            'coder_code': cd['coder_valid_code'] if cd else None,
            'evidence_tier': cd['evidence_tier'] if cd else 'none-retrievable',
            'coder_note': cd['coder_note'] if cd else '',
        })

    coded = [r for r in rows if r['coded']]
    print(f'primaries: {len(rows)} | re-coded with retrievable evidence: {len(coded)}')
    tier = Counter(r['evidence_tier'] for r in coded)
    print('evidence tiers:', dict(tier))

    determinable = [r for r in coded if r['coder_code'] != 'not reported']
    nd = [r for r in coded if r['coder_code'] == 'not reported']
    print(f'determinable codes: {len(determinable)} | not-reported: {len(nd)}')

    # strong-focused audit: the 42 released strong labels
    strong_rows = [r for r in rows if r['released_strong'] == 'yes']
    print(f'\n=== released strong labels: {len(strong_rows)} ===')
    s_coded = [r for r in strong_rows if r['coded']]
    s_det = [r for r in s_coded if r['coder_code'] != 'not reported']
    s_conf = [r for r in s_det if r['coder_code'] in STRONG]
    s_contra = [r for r in s_det if r['coder_code'] not in STRONG]
    s_nd = [r for r in s_coded if r['coder_code'] == 'not reported']
    s_noev = [r for r in strong_rows if not r['coded']]
    print(f'  evidence retrievable: {len(s_coded)} (fulltext {sum(1 for r in s_coded if r["evidence_tier"]=="fulltext")}, '
          f'abstract {sum(1 for r in s_coded if r["evidence_tier"]=="abstract")})')
    print(f'  determinable: {len(s_det)} -> confirmed strong: {len(s_conf)}, contradicted (coded non-strong): {len(s_contra)}')
    print(f'  protocol not determinable from evidence: {len(s_nd)} | no retrievable evidence: {len(s_noev)}')
    for r in s_contra:
        print(f'    CONTRADICTED: {r["doi"]} -> coder: {r["coder_code"]} ({r["coder_note"][:90]})')

    # upgrades among released non-strong
    ns_rows = [r for r in rows if r['released_strong'] == 'no' and r['coded']]
    ns_det = [r for r in ns_rows if r['coder_code'] != 'not reported']
    upgrades = [r for r in ns_det if r['coder_code'] in STRONG]
    print(f'\n=== released non-strong with evidence: {len(ns_rows)} (determinable {len(ns_det)}) ===')
    print(f'  coder-D would upgrade to strong: {len(upgrades)}')
    for r in upgrades:
        print(f'    UPGRADE: {r["doi"]} -> coder: {r["coder_code"]} ({r["coder_note"][:90]})')

    # bucket agreement (strong vs non-strong) on determinable rows
    det = [r for r in coded if r['coder_code'] != 'not reported']
    a = [1 if r['coder_code'] in STRONG else 0 for r in det]
    b = [1 if r['released_strong'] == 'yes' else 0 for r in det]
    agree = sum(1 for x, y in zip(a, b) if x == y)
    k = kappa(a, b)
    print(f'\nbucket agreement (determinable, n={len(det)}): {agree}/{len(det)} '
          f'= {agree/len(det)*100:.1f}%, kappa = {k:.2f}' if det else 'no determinable rows')
    ci = wilson(agree / len(det), len(det)) if det else None
    if ci:
        print(f'  Wilson 95% CI: {ci[0]*100:.1f}-{ci[1]*100:.1f}%')

    # full itemization: every determinable row where the code differs at class level
    diffs = [r for r in det if r['coder_code'] != r['released_code']]
    print(f'\n=== itemized class-level differences (determinable): {len(diffs)} ===')
    for r in diffs:
        print(f"  {r['doi']} [{r['evidence_tier']}]: released '{r['released_code']}' vs coder '{r['coder_code']}'")

    # abstract-only vs fulltext agreement split
    for t in ('fulltext', 'abstract'):
        sub = [r for r in det if r['evidence_tier'] == t]
        if sub:
            ag = sum(1 for r in sub if (r['coder_code'] in STRONG) == (r['released_strong'] == 'yes'))
            print(f'  {t} tier: {ag}/{len(sub)} agree')

    # fallback semantics (B/C-style: not-reported counted as non-strong)
    a2 = [1 if r['coder_code'] in STRONG else 0 for r in coded]
    b2 = [1 if r['released_strong'] == 'yes' else 0 for r in coded]
    ag2 = sum(1 for x, y in zip(a2, b2) if x == y)
    k2 = kappa(a2, b2)
    print(f'\nfallback semantics (not-reported -> non-strong, n={len(coded)}): '
          f'{ag2}/{len(coded)} = {ag2/len(coded)*100:.1f}%, kappa = {k2:.2f}')

    out = {
        'method': ('independent re-code of the validation field by coder D (AI research '
                   'assistant), from open-access full texts where retrievable (7) and '
                   'indexed abstracts otherwise; codes assigned from an evidence worksheet '
                   'before comparison with released labels; `not reported` used where the '
                   'evidence states no protocol'),
        'n_primary': len(rows),
        'n_coded': len(coded),
        'n_determinable': len(det),
        'evidence_tiers': dict(tier),
        'strong_labels': {
            'n': len(strong_rows),
            'with_evidence': len(s_coded),
            'determinable': len(s_det),
            'confirmed_strong': len(s_conf),
            'contradicted': len(s_contra),
            'contradicted_items': [r['doi'] for r in s_contra],
            'not_determinable': len(s_nd),
            'no_evidence': len(s_noev),
        },
        'nonstrong_upgrades': {
            'n_coded_nonstrong': len(ns_rows),
            'n_determinable': len(ns_det),
            'upgrades': [r['doi'] for r in upgrades],
        },
        'bucket_agreement_determinable': {
            'n': len(det), 'agree': agree,
            'pct': round(agree / len(det) * 100, 1) if det else None,
            'kappa': round(k, 3) if k is not None else None,
            'wilson_ci': [round(c * 100, 1) for c in ci] if ci else None,
        },
        'itemized_class_differences': [
            {'doi': r['doi'], 'tier': r['evidence_tier'],
             'released': r['released_code'], 'coder': r['coder_code'],
             'note': r['coder_note']} for r in diffs
        ],
        'fallback_semantics': {
            'n': len(coded), 'agree': ag2,
            'pct': round(ag2 / len(coded) * 100, 1),
            'kappa': round(k2, 3) if k2 is not None else None,
        },
        'per_paper': rows,
    }
    json.dump(out, open(os.path.join(HERE, 'validation_recode.json'), 'w'), indent=1)
    print(f'\nwrote {os.path.join(HERE, "validation_recode.json")}')

if __name__ == '__main__':
    main()
