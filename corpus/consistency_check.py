#!/usr/bin/env python3
"""Single source of truth: recompute every in-text statistic from papers_final.json."""
import json
from collections import Counter, defaultdict

C = json.load(open('/home/touhid/Documents/reviewpaper/corpus/papers_final.json'))
n = len(C)
print('corpus size:', n)

# 1. reviews per area (for Fig 1 heatmap reconciliation)
rev = [r for r in C if r['method'] == 'Review / perspective']
ra = Counter(r['area'] for r in rev)
prim = Counter(r['area'] for r in C if r['method'] != 'Review / perspective')
tot = Counter(r['area'] for r in C)
print('\n-- function counts: primary (reviews) = total')
for a in sorted(tot, key=lambda a: -tot[a]):
    print(f'  {a}: {prim[a]} ({ra[a]}) = {tot[a]}')
print('  primary total:', sum(prim.values()), '| reviews:', sum(ra.values()))

# 2. health-prognostics validation weakness
hp = [r for r in C if r['area'] in ('Health estimation (SOH)', 'Prognostics (RUL)')]
weak = [r for r in hp if r['valid'] in ('within-cell split', 'cross-validation')]
weak_all = [r for r in C if r['valid'] in ('within-cell split', 'cross-validation')]
print('\nweak validation: corpus-wide', len(weak_all), '| within SOH+RUL', len(weak), '| SOH+RUL size', len(hp))

# 3. real-vehicle data vs online validation overlap
rv = [r for r in C if r['data'] == 'real-vehicle']
onl = [r for r in C if r['valid'] == 'online/real-vehicle']
both = [r for r in C if r['data'] == 'real-vehicle' and r['valid'] == 'online/real-vehicle']
print('real-vehicle data:', len(rv), '| online validation:', len(onl), '| overlap:', len(both))
onl_not_rv = [r for r in onl if r['data'] != 'real-vehicle']
rv_not_onl = [r for r in rv if r['valid'] != 'online/real-vehicle']
print('  online-validated but data not real-vehicle:', [(r['doi'], r['data']) for r in onl_not_rv])
print('  real-vehicle data but not online-validated:', [(r['doi'], r['valid']) for r in rv_not_onl])

# 4. physics-informed/hybrid by year
G = json.load(open('/home/touhid/Documents/reviewpaper/corpus/stats.json'))['group_of']
pi = Counter(r['year'] for r in C if G[r['method']] == 'Physics-informed / hybrid')
print('\nPI/hybrid by year:', dict(sorted(pi.items())), 'total', sum(pi.values()))

# 5. SOC lab-only validation claim
soc = [r for r in C if r['area'] == 'State estimation (SOC)']
lab = [r for r in soc if r['data'] in ('self-lab', 'simulation', 'EIS-lab', 'NASA', 'CALCE', 'Severson-MATR')]
onechem = [r for r in soc if r['chem'] in ('NMC', 'LFP', 'LCO')]
print('\nSOC:', len(soc), '| lab-scale data:', len(lab), '| single chemistry:', len(onechem))

# 6. validation counts
print('\nvalid counts:', dict(Counter(r['valid'] for r in C).most_common()))
print('online/real-vehicle total:', len(onl))
print('data counts:', dict(Counter(r['data'] for r in C).most_common()))

# 7. citations source
print('\ntotal cites:', sum(r['cites'] for r in C))
