#!/usr/bin/env python3
"""Final corpus curation: explicit DOI-level reassignments, SOH trim, additions."""
import csv, json
from collections import defaultdict

SEL2 = '/home/touhid/Documents/reviewpaper/corpus/selection2.json'
POOL = '/home/touhid/Documents/reviewpaper/corpus/pool.csv'
OUT = '/home/touhid/Documents/reviewpaper/corpus/final_papers.json'

sel = json.load(open(SEL2))
by_doi = {r['doi']: r for r in sel}

# --- Explicit reassignments (title says more than the query tag did) ---
MOVES = {
    # Cross-cutting entries that are really core-area papers
    '10.1016/j.energy.2020.117664': 'State estimation (SOC)',   # LSTM+UKF SOC
    '10.1016/j.energy.2021.121236': 'State estimation (SOC)',   # PSO-LSTM SOC
    '10.1016/j.jpowsour.2020.229108': 'State estimation (SOC)', # automotive-informed SOC
    '10.1016/j.energy.2021.120205': 'Prognostics (RUL)',        # early lifetime prediction
    '10.1016/j.apenergy.2021.116897': 'Prognostics (RUL)',      # charge-process life pred
    '10.1016/j.applthermaleng.2022.118503': 'Thermal management', # parallel BTMS design
    '10.1016/j.est.2023.106931': 'Cell balancing & ECM',        # eliminating cell balancing
}
for doi, area in MOVES.items():
    if doi in by_doi:
        by_doi[doi]['area'] = area

# --- SOH trim: drop the weakest/duplicative of the 36 ---
SOH_DROPS = {
    '10.1016/j.est.2020.101741',   # generic novel DL SOH (superseded by better DL SOH)
    '10.1016/j.apenergy.2020.115074',  # ICA adaptive capacity (better ICA kept)
    '10.3390/en13020375',          # GPR SOH+RUL (deep GPR kept)
    '10.1016/j.est.2022.104215',   # ant lion (meta-heuristic dupe)
    '10.1016/j.energy.2024.132723',# dung beetle KELM (meta-heuristic dupe)
    '10.1016/j.energy.2025.135772',# snow ablation (meta-heuristic dupe)
    '10.3390/app15020516',         # generic MDPI SOH prediction
    '10.3390/batteries10090324',   # partial ICA (partial-charging entries kept)
    '10.1016/j.egyr.2023.01.108',  # SOC+SOH review (dedicated reviews kept)
    '10.1016/j.rser.2021.111903',  # theory review (non-probabilistic review kept)
    '10.1016/j.ress.2022.108818',  # multi-indicator fusion (fusion covered elsewhere)
    '10.3390/batteries12040115',   # grey wolf PINN (PINN SOH covered)
    '10.1016/j.isci.2025.114518',  # iScience SOH eval (lower value)
    '10.3390/batteries12050149',   # explainable PINN (keep other XAI entries)
    '10.1038/s41467-023-38458-w',  # Nature Comms DL SOH -- KEEP, see keep-set below
    '10.1016/j.est.2025.119450',   # CNN-LSTM transfer (transfer entries kept)
    '10.1016/j.energy.2025.139417',# LLM-MSIformer (keep HA-LLM + risk LLM)
}
# keep the Nature Comms one despite being in the dict above
SOH_DROPS.discard('10.1038/s41467-023-38458-w')

for doi in SOH_DROPS:
    r = by_doi.get(doi)
    if r and r['area'] == 'Health estimation (SOH)':
        r['_drop'] = True

# --- Additions from pool (balancing/ECM, thermal) ---
ADD_DOIS = {
    '10.1016/j.est.2024.113257': 'Cell balancing & ECM',
    '10.1016/j.applthermaleng.2024.123826': 'Thermal management',
}
pool_rows = {r['doi'].lower(): r for r in csv.DictReader(open(POOL))}
for doi, area in ADD_DOIS.items():
    r = pool_rows.get(doi)
    if r and doi not in by_doi:
        by_doi[doi] = {'doi': doi, 'title': r['title'], 'journal': r['journal'],
                       'year': int(r['year']), 'cites': int(r['cites']),
                       'areas': r['areas'], 'area': area, 'added': True}
    elif doi in by_doi:
        by_doi[doi]['area'] = area

final = [r for r in by_doi.values() if not r.get('_drop')]
for r in final:
    r.pop('_drop', None)

count = defaultdict(int)
years = defaultdict(int)
for r in final:
    count[r['area']] += 1
    years[r['year']] += 1
print('FINAL', len(final))
print('areas:', dict(sorted(count.items())))
print('years:', dict(sorted(years.items())))
json.dump(final, open(OUT, 'w'), indent=1)
