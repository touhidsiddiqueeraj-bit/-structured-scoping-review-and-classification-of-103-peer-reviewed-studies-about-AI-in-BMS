#!/usr/bin/env python3
"""Codes and summary for the abstract-level probes (reviewer round-3, M3 + M6).

The codes below were assigned by the review team from the staged abstracts in
abstract_probe_raw.json (single-coder, abstract level, rubric in
abstract_probe.py's docstring). Re-running this script recomputes every
reported number from the raw file plus these codes.

Probe A rubric values: isolation_stated / evaluation_stated / none_stated
Probe A record types:  primary_ml / primary_model_based / review / other
Probe B rubric values: none / mentioned / stated_samedata
"""
import io, json, os

from scipy.stats import fisher_exact

HERE = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------ codes
# Probe A - pool sample (n=40; 23 codable, 17 without retrievable abstract)
PROBE_A = {
 '10.3390/su16167180':      ('evaluation_stated', 'primary_ml'),
 '10.3390/drones10070549':  ('evaluation_stated', 'primary_ml'),
 '10.3390/forecast5030032': ('none_stated', 'review'),
 '10.1002/est2.218':        ('evaluation_stated', 'primary_model_based'),
 '10.3390/electronics14112201': ('evaluation_stated', 'primary_ml'),
 '10.1002/bte2.70149':      ('none_stated', 'review'),
 '10.62441/nano-ntp.v20is5.21': ('evaluation_stated', 'primary_ml'),
 '10.54097/9ervp336':       ('evaluation_stated', 'primary_ml'),
 '10.3390/app14146240':     ('evaluation_stated', 'primary_ml'),
 '10.3390/app131810547':    ('evaluation_stated', 'primary_ml'),
 '10.1016/j.xcrp.2023.101720': ('evaluation_stated', 'primary_ml'),
 '10.1016/j.enconman.2021.114103': ('evaluation_stated', 'other'),
 '10.3390/app12052305':     ('evaluation_stated', 'primary_ml'),
 '10.1149/1945-7111/ad9cc9': ('evaluation_stated', 'primary_ml'),
 '10.1177/01423312261466331': ('evaluation_stated', 'primary_ml'),
 '10.1002/batt.202300046':  ('none_stated', 'review'),
 '10.1016/j.est.2021.102372': ('evaluation_stated', 'primary_ml'),
 '10.62441/nano-ntp.v20is7.7': ('evaluation_stated', 'primary_ml'),
 '10.3389/fenrg.2022.1032660': ('evaluation_stated', 'primary_ml'),
 '10.1002/adts.202100350':  ('evaluation_stated', 'other'),
 '10.3390/en15165829':      ('evaluation_stated', 'primary_model_based'),
 '10.1109/tte.2021.3109636': ('evaluation_stated', 'primary_ml'),
 '10.3390/en14248492':      ('evaluation_stated', 'primary_ml'),
}

# Probe A codes applied to the SAME rubric on the subset's primary papers
# (the probe-B sheet) so the two tiers are comparable at abstract level.
PROBE_A_ON_SUBSET = {
 '10.1038/s42256-021-00312-3': 'evaluation_stated',
 '10.1016/j.energy.2020.117664': 'evaluation_stated',
 '10.1016/j.heliyon.2024.e35183': 'evaluation_stated',
 '10.3390/wevj12010038': 'evaluation_stated',
 '10.1016/j.apenergy.2021.116897': 'evaluation_stated',
 '10.1109/access.2021.3068776': 'none_stated',          # abstract reads as a survey
 '10.1016/j.energy.2019.116467': 'evaluation_stated',
 '10.1016/j.energy.2020.118000': 'evaluation_stated',
 '10.1016/j.geits.2024.100169': 'evaluation_stated',
 '10.1109/tpel.2021.3134701': 'evaluation_stated',
 '10.1016/j.apenergy.2024.125086': 'evaluation_stated',
 '10.1016/j.jpowsour.2019.227281': 'evaluation_stated',
 '10.1109/tte.2020.3028784': 'evaluation_stated',
 '10.1016/j.energy.2021.120205': 'evaluation_stated',
 '10.1016/j.apenergy.2025.125314': 'isolation_stated',  # "completely new data ... different operation conditions and life spans"
 '10.1038/s41598-025-92262-8': 'evaluation_stated',
 '10.1002/advs.202402608': 'isolation_stated',          # "6.6% test error on unseen data"
 '10.1016/j.renene.2019.08.077': 'evaluation_stated',
 '10.1109/tte.2023.3311813': 'evaluation_stated',
 '10.1038/s41598-025-30602-4': 'evaluation_stated',
 '10.1016/j.jpowsour.2021.229727': 'evaluation_stated',
 '10.1016/j.energy.2020.118866': 'evaluation_stated',
 '10.1016/j.jpowsour.2020.229108': 'evaluation_stated',
 '10.1038/s41467-023-38458-w': 'isolation_stated',      # "in the absence of target battery labels"
 '10.1016/j.ensm.2022.05.007': 'evaluation_stated',
 '10.1016/j.energy.2023.128461': 'evaluation_stated',
 '10.1109/tpel.2021.3117788': 'evaluation_stated',
 '10.1016/j.conengprac.2022.105202': 'evaluation_stated',
 '10.1016/j.egyai.2022.100188': 'evaluation_stated',
 '10.1002/anie.202214037': 'evaluation_stated',
 '10.1016/j.est.2026.123023': 'isolation_stated',       # Jetson Nano deployment + HIL testing
 '10.1109/jrfid.2022.3211841': 'evaluation_stated',
 '10.1038/s41467-020-15235-7': 'evaluation_stated',
 '10.3390/wevj16050279': 'evaluation_stated',
 '10.1016/j.est.2024.113257': 'evaluation_stated',
 '10.1016/j.est.2024.113502': 'evaluation_stated',
 '10.1109/tte.2025.3533540': 'isolation_stated',        # target-cell transfer across temperatures/cell types
 '10.1039/d2dd00067a': 'evaluation_stated',
}

# Probe B - baseline-comparison screen on the 88 primary papers
PROBE_B = {
 '10.3390/wevj12010038': 'mentioned',        # GPR among the six compared algorithms
 '10.1016/j.geits.2024.100169': 'mentioned',  # "compared to ... GPR and SVR" (no baseline numbers)
 '10.1016/j.renene.2019.08.077': 'stated_samedata',   # vs 0.5C CCCV, +3.60%
 '10.1016/j.jpowsour.2021.229727': 'stated_samedata', # vs SVR, R +2.1%, MSE -87.8%
 '10.1016/j.est.2026.123023': 'stated_samedata',      # vs ECM/EM, >=3x improvement
 '10.3390/wevj16050279': 'stated_samedata',           # vs rule-based controller, energy savings quantified
}
# every other codable record codes 'none'; B18 (isci.2025.112235) is an
# uncodable fragment and is excluded from the screen.

# ------------------------------------------------------------------ summary
raw = json.load(io.open(os.path.join(HERE, 'abstract_probe_raw.json'), encoding='utf-8'))
A, B = raw['probeA_pool_sample'], raw['probeB_primary_papers']


def wilson(k, n, z=1.959964):
    import math
    if n == 0:
        return None
    ph = k / n
    d = 1 + z * z / n
    c = (ph + z * z / (2 * n)) / d
    h = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / d
    return [max(0.0, round(100 * (c - h), 1)), round(100 * (c + h), 1)]


out = {'seed': raw['seed'], 'probeA': {}, 'probeB': {}, 'notes': []}

# --- Probe A
codedA = [r for r in A if r['doi'] in PROBE_A]
missingA = [r for r in A if len(r['abstract']) < 150]
assert len(codedA) + len(missingA) == len(A), (len(codedA), len(missingA), len(A))
ev = {'isolation_stated': 0, 'evaluation_stated': 0, 'none_stated': 0}
ty = {'primary_ml': 0, 'primary_model_based': 0, 'review': 0, 'other': 0}
for r in codedA:
    e, t = PROBE_A[r['doi']]
    ev[e] += 1
    ty[t] += 1
primA = sum(1 for r in codedA if PROBE_A[r['doi']][1] in ('primary_ml', 'primary_model_based'))
out['probeA'] = {
    'n_sample': len(A), 'n_coded': len(codedA), 'n_no_abstract': len(missingA),
    'availability_rate': round(len(codedA) / len(A), 3),
    'validation_evidence_codes': ev,
    'record_types': ty,
    'primary_like_records': primA,
    'isolation_stated_share_of_primary_like': wilson(ev['isolation_stated'], primA),
    'missingness_note': ('Elsevier-withheld abstracts dominate the missing 17; '
                         'missingness is publisher-driven, not topic-driven'),
}

# --- same rubric on subset primary papers
codedS = [r for r in B if r['doi'] in PROBE_A_ON_SUBSET]
missingS = [r for r in B if len(r['abstract']) < 150]
frag = [r['doi'] for r in B if len(r['abstract']) >= 150 and r['doi'] not in PROBE_A_ON_SUBSET]
assert frag == ['10.1016/j.isci.2025.112235'], frag  # uncodable fragment (openalex tail-only)
evS = {'isolation_stated': 0, 'evaluation_stated': 0, 'none_stated': 0}
for r in codedS:
    evS[PROBE_A_ON_SUBSET[r['doi']]] += 1
out['probeA_on_subset'] = {
    'n_primary': len(B), 'n_coded': len(codedS), 'n_no_abstract': len(missingS),
    'n_uncodable_fragment': len(frag),
    'availability_rate': round(len(codedS) / len(B), 3),
    'validation_evidence_codes': evS,
    'isolation_stated_share': wilson(evS['isolation_stated'], len(codedS)),
}
tab = [[ev['isolation_stated'], primA - ev['isolation_stated']],
       [evS['isolation_stated'], len(codedS) - evS['isolation_stated']]]
out['probeA_contrast'] = {
    'table_isolation_vs_rest': tab,
    'fisher_p_two_sided': round(fisher_exact(tab)[1], 3),
}

# --- Probe B
codedB = [r for r in B if r['doi'] in PROBE_B or r['doi'] in PROBE_A_ON_SUBSET]
none_ct = sum(1 for r in codedB if r['doi'] not in PROBE_B or PROBE_B[r['doi']] == 'none')
men_ct = sum(1 for r in codedB if PROBE_B.get(r['doi']) == 'mentioned')
sd_ct = sum(1 for r in codedB if PROBE_B.get(r['doi']) == 'stated_samedata')
out['probeB'] = {
    'n_primary': len(B), 'n_screenable': len(codedB), 'n_no_abstract': len(missingS),
    'n_uncodable_fragment': len(frag),
    'availability_rate': round(len(codedB) / len(B), 3),
    'baseline_none': none_ct, 'baseline_mentioned': men_ct, 'baseline_stated_samedata': sd_ct,
    'any_baseline_share': wilson(men_ct + sd_ct, len(codedB)),
    'stated_samedata_share': wilson(sd_ct, len(codedB)),
    'named_baselines_examples': ['GPR/SVR (wevj 2021; geits 2024)', '0.5C CCCV (renene 2020)',
                                  'SVR (jpowsour 2021)', 'ECM/electrochemical model (est 2026)',
                                  'rule-based controller (wevj 2025)'],
    'bounds_note': ('abstract-level screen: a full text may compare baselines the abstract does '
                    'not mention, so these are lower bounds on comparison PRACTICE and exact '
                    'measures of comparison VISIBILITY; ScienceDirect abstracts are withheld '
                    'from Crossref/OpenAlex/Semantic Scholar, so 48 of 88 papers (55%) cannot '
                    'be screened at all'),
}

json.dump(out, io.open(os.path.join(HERE, 'abstract_probe.json'), 'w', encoding='utf-8'), indent=1)
print(json.dumps(out, indent=1))
