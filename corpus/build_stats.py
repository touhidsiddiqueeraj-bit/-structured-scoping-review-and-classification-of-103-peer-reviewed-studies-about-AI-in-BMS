#!/usr/bin/env python3
"""Build final papers.csv, compute meta-analysis stats, save stats.json."""
import json, csv
from collections import Counter, defaultdict

ver = json.load(open('/home/touhid/Documents/reviewpaper/corpus/papers_final.json'))
ver.sort(key=lambda r: (r['area'], r['year'], r['journal']))

def pages_str(r):
    if r.get('page'):
        return r['page']
    if r.get('article_number'):
        return f"Art. {r['article_number']}"
    return ''

cols = ['doi', 'title', 'authors', 'journal', 'year', 'volume', 'issue',
        'pages', 'area', 'method', 'chem', 'data', 'valid', 'finding', 'limit', 'cites']
with open('/home/touhid/Documents/reviewpaper/corpus/papers.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    for r in ver:
        row = {c: r.get(c, '') for c in cols}
        row['title'] = row['title'].replace('fast-chaging', 'fast-charging').replace('&amp;', '&')
        row['journal'] = row['journal'].replace('&amp;', '&')
        row['finding'] = row['finding'].replace('fast-chaging', 'fast-charging')
        w.writerow(row)
print('papers.csv written:', len(ver))

def fix(s): return s.replace('fast-chaging', 'fast-charging')

stats = {}
stats['n'] = len(ver)
stats['by_year'] = dict(sorted(Counter(r['year'] for r in ver).items()))
stats['by_area'] = dict(sorted(Counter(r['area'] for r in ver).items()))
stats['by_method'] = dict(Counter(r['method'] for r in ver).most_common())
stats['by_chem'] = dict(Counter(r['chem'] for r in ver).most_common())
stats['by_data'] = dict(Counter(r['data'] for r in ver).most_common())
stats['by_valid'] = dict(Counter(r['valid'] for r in ver).most_common())
stats['by_journal'] = dict(Counter(r['journal'].replace('&amp;', '&') for r in ver).most_common(12))

# method family x year matrix (grouped families)
GROUP = {
    'Shallow ML': 'Classical ML',
    'Deep learning': 'Deep learning',
    'Physics-informed': 'Physics-informed / hybrid',
    'Hybrid physics+ML': 'Physics-informed / hybrid',
    'Filter-based hybrid': 'Physics-informed / hybrid',
    'Meta-heuristic-optimized DL': 'Optimization-augmented learning',
    'Optimization-augmented control': 'Optimization-augmented learning',
    'Bayesian optimization': 'Optimization-augmented learning',
    'Reinforcement learning': 'Reinforcement / control learning',
    'Transfer learning': 'Transfer / domain adaptation',
    'Graph neural network': 'Deep learning',
    'Foundation model / LLM': 'Foundation models / LLM',
    'Review / perspective': 'Review / perspective',
}
my = defaultdict(lambda: defaultdict(int))
for r in ver:
    my[r['year']][GROUP[r['method']]] += 1
stats['method_group_by_year'] = {str(y): dict(m) for y, m in sorted(my.items())}
stats['group_of'] = GROUP

# area x year matrix
ay = defaultdict(lambda: defaultdict(int))
for r in ver:
    ay[r['area']][r['year']] += 1
stats['area_by_year'] = {a: dict(sorted(m.items())) for a, m in sorted(ay.items())}

# total records identified (for PRISMA): raw files item counts
import glob
total_raw = 0
for f in glob.glob('/home/touhid/Documents/reviewpaper/corpus/raw/*.json'):
    try:
        d = json.load(open(f))
        items = d if isinstance(d, list) else (d.get('message', {}) or {}).get('items', [])
        total_raw += len(items)
    except Exception:
        pass
stats['records_retrieved'] = total_raw
stats['records_after_dedupe'] = 1550
stats['on_topic_after_gate'] = 883
stats['after_venue_screen'] = 107 + 9 - 3  # selection + additions - drops
stats['final_corpus'] = len(ver)
json.dump(stats, open('/home/touhid/Documents/reviewpaper/corpus/stats.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in stats.items() if not isinstance(v, dict)}, indent=1))
print('by_year:', stats['by_year'])
print('method_group_by_year:', json.dumps(stats['method_group_by_year'], indent=1))
