#!/usr/bin/env python3
"""Verify landmark seed DOIs via CrossRef and save results."""
import json, subprocess, time

SEEDS = [
    '10.1038/s41560-019-0356-8',   # Severson 2019 cycle life prediction (background)
    '10.1038/s41586-020-1994-5',   # Attia 2020 closed-loop fast charging
    '10.1038/s42256-021-00312-3',  # Roman 2021 ML pipeline SOH
    '10.1038/s41467-020-15235-7',  # Zhang 2020 EIS degradation patterns
    '10.1038/s42256-020-0156-7',   # Ng 2020 SOC/SOH ML perspective
    '10.1016/j.joule.2019.11.018', # Hu 2020 battery lifetime prognostics
    '10.1109/ACCESS.2019.2927778', # CNN-LSTM SOC (background, 2019)
]

ok = []
for doi in SEEDS:
    r = subprocess.run(['curl', '-s', '--max-time', '30',
                        f'https://api.crossref.org/works/{doi}'],
                       capture_output=True, text=True)
    try:
        m = json.loads(r.stdout)['message']
        title = (m.get('title') or [''])[0]
        jr = (m.get('container-title') or [''])[0]
        year = (m.get('issued', {}).get('date-parts') or [[None]])[0][0]
        cites = m.get('is-referenced-by-count', 0)
        print(f'{doi}  {year}  cites={cites:>5}  {jr[:45]:<45}  {title[:70]}')
        ok.append({'doi': doi.lower(), 'title': title, 'journal': jr,
                   'year': year, 'cites': cites})
    except Exception:
        print(f'{doi}  FAILED: {r.stdout[:100]}')
    time.sleep(0.5)

with open('/home/touhid/Documents/reviewpaper/corpus/seeds.json', 'w') as f:
    json.dump(ok, f, indent=1)
print(f'{len(ok)} seeds verified')
