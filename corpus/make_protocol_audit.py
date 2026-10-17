#!/usr/bin/env python3
"""Per-paper validation-protocol audit table (TTE R1 #2 fix):
every classified paper mapped to its protocol class and strong flags,
so the 43-of-91 strong-protocol arithmetic is checkable row by row."""
import csv, json

C = json.load(open('/home/touhid/Documents/reviewpaper/corpus/papers_final.json'))
OUT = '/home/touhid/Documents/reviewpaper/corpus/protocol_audit.csv'

PROTO_STRONG = ('cross-cell holdout', 'cross-chemistry holdout',
                'cross-domain holdout', 'online/real-vehicle')
ENV_STRONG = PROTO_STRONG + ('experimental hardware',)

rows = []
for r in sorted(C, key=lambda r: (r['area'], r['year'], r['journal'])):
    v = r['valid']
    primary = '--' if r['method'] == 'Review / perspective' else 'primary'
    rows.append({
        'doi': r['doi'], 'area': r['area'], 'method_family': r['method'],
        'data_source': r['data'], 'validation_coded': v,
        'strong_protocol_only': 'yes' if v in PROTO_STRONG else 'no',
        'strong_incl_hardware': 'yes' if v in ENV_STRONG else 'no',
        'primary_or_review': primary,
    })
with open(OUT, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)
print('protocol_audit.csv:', len(rows), 'rows; strong>',
      sum(1 for r in rows if r['strong_protocol_only'] == 'yes' and r['primary_or_review'] == 'primary'), '/',
      sum(1 for r in rows if r['primary_or_review'] == 'primary'))
