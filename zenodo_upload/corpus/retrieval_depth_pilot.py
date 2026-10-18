#!/usr/bin/env python3
"""Round-6 P6: retrieval-depth pilot — does cursor paging lift the recall cap?

Re-runs the original 30-query Crossref retrieval design for a 6-family
representative subset, but pages each pass with a cursor to depth 200
(the original design took its top ~20 per pass). Windows and sort orders
replicate the original passes; until-pub-date is pinned to the original
retrieval date (2026-09-05) so no post-retrieval registry drift enters.

For each family/pass:
  - fetch depth-200 records (cursor, rows=200)
  - apply the original pool.py filters (journal-article, title>=25 chars,
    pass year window) and title relevance gate
  - compare against (a) the original raw/*.json items for that pass
    (replication check) and (b) the 1,550-record retrieval (marginal yield)

Output: corpus/retrieval_depth_pilot.json
"""
import json, os, time, urllib.request, urllib.parse, csv, re

REPO = ''
HERE = os.path.join(REPO, 'corpus')
OUT = os.path.join(HERE, 'retrieval_depth_pilot.json')
MAILTO = 'touhidsiddiqueeraj-bit@users.noreply.github.com'
SELECT = 'DOI,title,container-title,issued,is-referenced-by-count,type'

FAMILIES = ['soc_ml', 'soh_ml', 'rul_dl', 'pinn', 'flt_diag', 'llm']
QUERIES = {
    'soc_ml': 'state of charge estimation lithium-ion battery machine learning',
    'soh_ml': 'state of health estimation lithium-ion battery machine learning',
    'rul_dl': 'battery remaining useful life prediction deep learning',
    'pinn': 'physics-informed neural network lithium-ion battery',
    'flt_diag': 'lithium-ion battery fault diagnosis machine learning',
    'llm': 'large language model battery',
}
# original pass design (windows from manuscript 2.2; sorts verified against the
# citation-count signature of the cached raw/*.json responses: 'cited' and 'mid'
# are citation-sorted — monotonic descending is-referenced-by-count; the other
# three are relevance-sorted)
PASSES = {
    'cited': {'sort': 'is-referenced-by-count', 'from': '2020-01-01', 'until': '2026-09-05'},
    'recent': {'sort': 'relevance', 'from': '2024-06-01', 'until': '2026-09-05'},
    'mid': {'sort': 'is-referenced-by-count', 'from': '2021-01-01', 'until': '2023-12-31'},
    'old': {'sort': 'relevance', 'from': '2020-01-01', 'until': '2022-12-31'},
    'y2023': {'sort': 'relevance', 'from': '2023-01-01', 'until': '2023-12-31'},
}
DEPTH = 200

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
EXCLUDE_VENUES = [
    'ECS Meeting Abstracts', 'SSRN', 'Journal of Physics: Conference Series',
    'IET Conference Proceedings', 'IFAC-PapersOnLine', 'Procedia',
    'ECS Transactions', 'MRS Advances', 'Conference', 'Abstracts',
    'Journal of Mechanical Engineering',
    'Electric and Hybrid Vehicle Technology International', 'Franklin Open',
]

def gate(title):
    t = ' ' + title.lower() + ' '
    return any(x in t for x in BATTERY_TERMS) and any(x in t for x in ML_TERMS)

def venue_ok(j):
    return not any(x.lower() in (j or '').lower() for x in EXCLUDE_VENUES) and len(j or '') > 3

def fetch_pass(qstr, pdef):
    q = urllib.parse.quote(qstr)
    filt = f'type:journal-article,from-pub-date:{pdef["from"]},until-pub-date:{pdef["until"]}'
    url = (f'https://api.crossref.org/works?query.bibliographic={q}'
           f'&filter={filt}&rows={DEPTH}&select={SELECT}'
           f'&sort={pdef["sort"]}&order=desc&mailto={MAILTO}')
    req = urllib.request.Request(url, headers={'User-Agent': f'mlbms-pilot/1.0 (mailto:{MAILTO})'})
    with urllib.request.urlopen(req, timeout=60) as r:
        d = json.loads(r.read().decode('utf-8'))
    return d.get('message', {}).get('items', []), d.get('message', {}).get('total-results')

def year_of(it):
    for dp in (it.get('issued', {}).get('date-parts') or [[None]]):
        if dp and dp[0]:
            return dp[0]
    return None

def orig_family_gated(fams=None):
    """Original-design gated DOIs per family, from the cached raw/*.json files."""
    import glob
    per_fam = {}
    for f in glob.glob(os.path.join(HERE, 'raw', '*.json')):
        key = os.path.basename(f).rsplit('_', 1)[0]
        if fams is not None and key not in fams:
            continue
        try:
            items = json.load(open(f)).get('message', {}).get('items', [])
        except Exception:
            continue
        for it in items:
            doi = (it.get('DOI') or '').lower()
            title = re.sub(r'\s+', ' ', (it.get('title') or [''])[0]).strip()
            yr = year_of(it)
            if doi and len(title) >= 25 and it.get('type') == 'journal-article' \
               and yr and yr >= 2020 and gate(title):
                per_fam.setdefault(key, set()).add(doi)
    uniq = set().union(*per_fam.values()) if per_fam else set()
    gross = sum(len(s) for s in per_fam.values())
    return uniq, gross

def main():
    # the 1,550 original retrieval
    srows = list(csv.DictReader(open(os.path.join(HERE, 'screening_log.csv'))))
    forced = {r['doi'] for r in srows if 'forced-seed' in (r['reason_or_note'] or '')}
    retrieved = {r['doi'].lower() for r in srows} - {d.lower() for d in forced}
    print(f'original retrieval: {len(retrieved)} records')

    results = {'families': {}, 'depth': DEPTH, 'retrieval_date_pin': '2026-09-05',
               'method': ('six representative query families, five original passes each, '
                          'cursor-paged to depth 200 per pass (original design: top ~20 per pass); '
                          'pool.py filters and title gate applied identically; venue screen applied '
                          'for the eligible-level count')}

    for fam in FAMILIES:
        fam_res = {'passes': {}}
        for pname, pdef in PASSES.items():
            items, total = fetch_pass(QUERIES[fam], pdef)
            time.sleep(1.0)
            # original raw file for this pass (replication check)
            rawf = os.path.join(HERE, 'raw', f'{fam}_{pname}.json')
            orig_dois = set()
            if os.path.exists(rawf):
                try:
                    od = json.load(open(rawf))
                    orig_dois = {it.get('DOI', '').lower() for it in od.get('message', {}).get('items', [])
                                 if it.get('DOI')}
                except Exception:
                    pass
            # apply pool.py filters rank-by-rank
            ranked = []
            for rank, it in enumerate(items, 1):
                doi = (it.get('DOI') or '').lower()
                title = re.sub(r'\s+', ' ', (it.get('title') or [''])[0]).strip()
                yr = year_of(it)
                jr = (it.get('container-title') or [''])[0]
                ok = bool(doi) and len(title) >= 25 and yr is not None
                gated = ok and gate(title)
                ranked.append({'rank': rank, 'doi': doi, 'title': title, 'year': yr,
                               'venue': jr, 'filters_ok': ok, 'gated': gated,
                               'venue_ok': venue_ok(jr) if gated else None})
            def gated_upto(depth, extra=None):
                seen, out = set(), []
                for r in ranked:
                    if r['rank'] <= depth and r['gated'] and r['doi'] not in seen:
                        seen.add(r['doi'])
                        if extra is None or extra(r):
                            out.append(r)
                return out
            # replication: overlap of top-20 gated set with original pass items
            top_gated = {r['doi'] for r in gated_upto(25)}
            overlap = len(top_gated & orig_dois)
            fam_res['passes'][pname] = {
                'total_results': total,
                'fetched_items': len(items),
                'orig_items': len(orig_dois),
                'orig_overlap_in_top25_gated': overlap,
                'gated_unique_at_25': len(gated_upto(25)),
                'gated_unique_at_100': len(gated_upto(100)),
                'gated_unique_at_200': len(gated_upto(200)),
                'gated_venueok_at_200': len(gated_upto(200, extra=lambda r: r['venue_ok'])),
                'new_gated_at_100_not_in_1550': len([r for r in gated_upto(100) if r['doi'] not in retrieved]),
                'new_gated_at_200_not_in_1550': len([r for r in gated_upto(200) if r['doi'] not in retrieved]),
                'new_gated_venueok_at_200': len([r for r in gated_upto(200)
                                                 if r['doi'] not in retrieved and r['venue_ok']]),
                'ranked': [{k: r[k] for k in ('rank', 'doi', 'title', 'year', 'venue', 'gated', 'venue_ok')}
                           for r in ranked if r['gated']],
            }
            print(f'{fam}/{pname}: total={total} fetched={len(items)} '
                  f'gated@25={len(gated_upto(25))} gated@100={len(gated_upto(100))} '
                  f'gated@200={len(gated_upto(200))} new@200={fam_res["passes"][pname]["new_gated_at_200_not_in_1550"]}')
        # family-level uniques across passes
        fam_uniq = {}
        for pname, pr in fam_res['passes'].items():
            for r in pr['ranked']:
                fam_uniq.setdefault(r['doi'], r)
        new_fam = [d for d in fam_uniq if d not in retrieved]
        fam_res['family_gated_unique_at_200'] = len(fam_uniq)
        fam_res['family_new_gated_not_in_1550'] = len(new_fam)
        fam_res['family_new_gated_venueok'] = len([d for d, r in fam_uniq.items()
                                                   if d not in retrieved and r['venue_ok']])
        results['families'][fam] = fam_res
        print(f'  FAMILY {fam}: unique gated {len(fam_uniq)}, NEW (not in 1,550): {len(new_fam)}, '
              f'venue-ok new: {fam_res["family_new_gated_venueok"]}')

    # summary
    tot_new = sum(f['family_new_gated_not_in_1550'] for f in results['families'].values())
    tot_new_ok = sum(f['family_new_gated_venueok'] for f in results['families'].values())
    tot_uniq = sum(f['family_gated_unique_at_200'] for f in results['families'].values())
    # original-design reference for the same 6 families (from cached raw/*.json)
    orig6, orig6_gross = orig_family_gated(FAMILIES)
    # original 30-family overlap factor (gated per-family sum / unique)
    all_fams, all_gross = orig_family_gated(None)
    overlap_factor = all_gross / len(all_fams) if all_fams else None
    extrap = None
    if overlap_factor:
        extrap = round(tot_new * (30.0 / len(FAMILIES)) / overlap_factor)
    results['summary'] = {
        'families_piloted': len(FAMILIES),
        'per_pass_depth': DEPTH,
        'gated_unique_all_families': tot_uniq,
        'new_gated_not_in_1550_all_families': tot_new,
        'new_gated_venueok_all_families': tot_new_ok,
        'orig_6family_gated_unique': len(orig6),
        'orig_30family_gated_unique': len(all_fams),
        'orig_30family_overlap_factor': round(overlap_factor, 2) if overlap_factor else None,
        'extrapolated_net_new_gated_all_30_families': extrap,
        'note': ('marginal yield of cursor paging beyond the original top-20 design, '
                 'measured on 6 of 30 families; the extrapolation applies the original '
                 'design\'s observed 30-family cross-family overlap factor to the pilot\'s '
                 'per-family new-record yield and is indicative only'),
    }
    json.dump(results, open(OUT, 'w'), indent=1)
    print(f'\nwrote {OUT}')
    print('summary:', json.dumps(results['summary'], indent=1))

if __name__ == '__main__':
    main()
