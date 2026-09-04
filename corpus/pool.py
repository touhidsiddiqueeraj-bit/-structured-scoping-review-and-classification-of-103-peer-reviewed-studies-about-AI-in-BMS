#!/usr/bin/env python3
"""Pool CrossRef raw query results into a deduplicated candidate pool."""
import json, glob, csv, re

AREA_OF_KEY = {
    'soc': 'State estimation (SOC)', 'soh': 'Health estimation (SOH)',
    'rul': 'Prognostics (RUL)', 'chg': 'Charging control', 'thm': 'Thermal management',
    'flt': 'Fault & safety', 'bal': 'Cell balancing & ECM', 'rev': 'Cross-cutting',
    'pinn': 'Physics-informed', 'tl': 'Transfer learning', 'twin': 'Digital twins',
    'llm': 'Foundation models', 'gnn': 'Graph networks', 'bmk': 'Benchmarks & data',
    'interp': 'Interpretability', 'cloud': 'Cloud & fleet', 'second': 'Second life',
}

def area_of(key):
    for prefix, area in AREA_OF_KEY.items():
        if key.startswith(prefix):
            return area
    return 'Other'

rows = {}
files = sorted(glob.glob('/home/touhid/Documents/reviewpaper/corpus/raw/*.json'))
print(f'{len(files)} raw files')
for f in files:
    key = f.split('/')[-1].replace('.json', '')
    try:
        data = json.load(open(f))
    except Exception as e:
        print(f'BAD JSON {f}: {e}')
        continue
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        items = data.get('message', {}).get('items', []) if isinstance(data.get('message'), dict) else []
    else:
        items = []
    for it in items:
        doi = it.get('DOI', '').lower()
        if not doi or it.get('type') != 'journal-article':
            continue
        title = (it.get('title') or [''])[0]
        if not title or len(title) < 25:
            continue
        year = None
        for dp in (it.get('issued', {}).get('date-parts') or [[None]]):
            if dp and dp[0]:
                year = dp[0]
                break
        if not year or year < 2020:
            continue
        jr = (it.get('container-title') or [''])[0]
        cites = it.get('is-referenced-by-count', 0)
        r = rows.setdefault(doi, {
            'doi': doi, 'title': re.sub(r'\s+', ' ', title).strip(),
            'journal': jr, 'year': year, 'cites': cites, 'areas': set(),
        })
        r['areas'].add(area_of(key))
        r['cites'] = max(r['cites'], cites)

# Relevance gate: title must mention a battery/EV term AND an ML/data-driven term
BATTERY_TERMS = [
    'batter', 'lithium', 'li-ion', 'li ion', 'state of charge', 'state of health',
    'charging', 'electric vehicle', ' ev ', 'sodium-ion', 'anode', 'cathode',
    'plating', 'electrochemical impedance', 'cell balancing', 'energy storage',
    'supercapacitor', 'power source', 'solid-state electrolyte', 'electric ship',
    'electric aircraft', 'e-bike', 'scooter',
]
ML_TERMS = [
    'machine learning', 'deep learning', 'neural network', 'reinforcement learning',
    'transfer learning', 'data-driven', 'learning', 'artificial intelligence', ' ai ',
    'intelligent', 'bayesian', 'gaussian process', 'lstm', 'gru', 'transformer',
    'random forest', 'support vector', 'regression', 'classification', 'clustering',
    'predict', 'prognos', 'estimat', 'digital twin', 'physics-informed',
    'physics informed', 'optimiz', 'optimis', 'foundation model', 'large language',
    'graph neural', 'convolutional', 'feature', 'monitor', 'diagnos', 'anomaly',
    'fault', 'sensing', 'surrogate', 'generative', 'autoencoder', 'ensemble',
]
def is_battery_related(title):
    t = ' ' + title.lower() + ' '
    return any(term in t for term in BATTERY_TERMS) and any(term in t for term in ML_TERMS)

out = []
dropped = 0
for doi, r in rows.items():
    if not is_battery_related(r['title']):
        dropped += 1
        continue
    r['areas'] = ';'.join(sorted(r['areas']))
    out.append(r)
out.sort(key=lambda r: -r['cites'])
print(f'dropped as off-topic: {dropped}')
with open('/home/touhid/Documents/reviewpaper/corpus/pool.csv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=['doi', 'title', 'journal', 'year', 'cites', 'areas'])
    w.writeheader()
    w.writerows(out)
print(f'unique candidates: {len(out)}')
byyear = {}
for r in out:
    byyear[r['year']] = byyear.get(r['year'], 0) + 1
print('by year:', dict(sorted(byyear.items())))
