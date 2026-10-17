#!/usr/bin/env python3
"""Single source of truth: recompute every in-text statistic from papers_final.json."""
import json
from collections import Counter, defaultdict

C = json.load(open('/home/touhid/Documents/reviewpaper/corpus/papers_final.json'))
n = len(C)
print('corpus size:', n)

# 1. reviews per area (for Fig 1 heatmap reconciliation)
rev = [r for r in C if r['valid'] == 'review synthesis']
ra = Counter(r['area'] for r in rev)
prim = Counter(r['area'] for r in C if r['valid'] != 'review synthesis')
tot = Counter(r['area'] for r in C)
print('\n-- function counts: primary (review-tagged incl syntheses) = total')
for a in sorted(tot, key=lambda a: -tot[a]):
    print(f'  {a}: {prim[a]} ({ra[a]}) = {tot[a]}')
print('  primary total:', sum(prim.values()), '| review-tagged:', sum(ra.values()))

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

# 4. physics-informed/hybrid by year (primary-application papers only)
G = json.load(open('/home/touhid/Documents/reviewpaper/corpus/stats.json'))['group_of']
P88 = [r for r in C if r['method'] != 'Review / perspective' and r['valid'] != 'review synthesis']
pi = Counter(r['year'] for r in P88 if G[r['method']] == 'Physics-informed / hybrid')
print('\nPI/hybrid by year (primary):', dict(sorted(pi.items())), 'total', sum(pi.values()))

# 5. SOC lab-only validation claim (primary SOC papers)
soc = [r for r in P88 if r['area'] == 'State estimation (SOC)']
lab = [r for r in soc if r['data'] in ('self-lab', 'simulation', 'EIS-lab', 'NASA', 'CALCE', 'Severson-MATR')]
nmc = [r for r in soc if r['chem'] == 'NMC']
print('\nSOC primary:', len(soc), '| lab-scale data:', len(lab), '| NMC:', len(nmc))

# 6. validation counts
print('\nvalid counts:', dict(Counter(r['valid'] for r in C).most_common()))
print('online/real-vehicle total:', len(onl))
print('data counts:', dict(Counter(r['data'] for r in C).most_common()))

# 7. citations source
print('\ntotal cites:', sum(r['cites'] for r in C))

# 7. TTE-revision checks: two-tier corpus, protocol audit, review labels, Fisher
import json as _json
from math import sqrt as _sqrt, exp as _exp, log as _log

E = _json.load(open('/home/touhid/Documents/reviewpaper/corpus/eligible_corpus.json'))
print('\n-- two-tier checks')
print('tier1 n:', E['n'], '| tier2 n:', n, '| subset <= eligible?')
assert E['n'] >= n

primRec = [r for r in C if r['method'] != 'Review / perspective' and r['valid'] != 'review synthesis']
PROTO = ('cross-cell holdout', 'cross-chemistry holdout', 'cross-domain holdout', 'online/real-vehicle')
ENV = PROTO + ('experimental hardware',)
pi = [r for r in primRec if r['method'] in ('Physics-informed', 'Hybrid physics+ML', 'Filter-based hybrid')]
other = [r for r in primRec if r not in pi]
a = sum(1 for r in pi if r['valid'] in PROTO); c = sum(1 for r in other if r['valid'] in PROTO)
a2 = sum(1 for r in pi if r['valid'] in ENV); c2 = sum(1 for r in other if r['valid'] in ENV)
print(f'strong protocol-only: PI {a}/{len(pi)} vs other {c}/{len(other)}')
print(f'strong incl hardware: PI {a2}/{len(pi)} vs other {c2}/{len(other)}')
strong = sum(1 for r in primRec if r['valid'] in PROTO)
weak = sum(1 for r in C if r['valid'] in ('within-cell split', 'cross-validation'))
assert strong == 42 and weak == 17 and len(primRec) == 88, 'primary/strong denominators drifted'
print(f'strong protocol papers: {strong}/88 | weak splits corpus-wide: {weak}')
reviews12 = sum(1 for r in C if r['method'] == 'Review / perspective')
data_review = sum(1 for r in C if r['data'] == 'review')
print(f'method-coded reviews: {reviews12} | data-field review-tagged: {data_review} (12 + 3 review-type syntheses = 15)')

# Fisher exact via scipy if available
try:
    from scipy.stats import fisher_exact as _fe
    print('fisher protocol-only p=%.3f' % _fe([[a, len(pi)-a], [c, len(other)-c]])[1])
    print('fisher incl-hardware p=%.3f' % _fe([[a2, len(pi)-a2], [c2, len(other)-c2]])[1])
except ImportError:
    pass
print('\nall consistency checks printed')
