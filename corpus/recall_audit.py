#!/usr/bin/env python3
"""Recall audit (reviewer round-3, M2): how much of the literature that our own
included reviews cite did the 30-query Crossref retrieval actually capture?

Method
------
1. Take the 15 review-labelled papers of the classified subset (12 method-family
   reviews + 3 review-type syntheses) -- the papers whose job is to survey this
   literature -- plus the 6 seed studies.
2. Pull each one's deposited reference list from the Crossref REST API.
3. Match every DOI-bearing reference against the 1,550-record query retrieval
   (screening_log.csv minus the 5 forced seeds).
4. Restrict to "in-scope-looking" references by applying the SAME title gate as
   the screening pipeline (>=1 battery term AND >=1 ML term in the title), so
   the capture rate is estimated on references that would plausibly have been
   eligible, not on unrelated electrochemistry.
5. Also record per-query yields (records retrieved per query family, after the
   same journal-article / year / title-length filters used to build the pool).

Outputs: corpus/recall_audit.json (all numbers used in the manuscript).
Cached API responses in corpus/raw_cache/ so the audit re-runs offline.
"""
import csv, glob, io, json, os, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CACHE = os.path.join(HERE, 'raw_cache')
os.makedirs(CACHE, exist_ok=True)
MAILTO = 'mlbms-review@example.org'  # polite-pool identifier

# ---------------------------------------------------------------- helpers
def crossref_get(doi):
    """GET a Crossref work record, with a local cache."""
    safe = doi.replace('/', '_')
    cf = os.path.join(CACHE, safe + '.json')
    if os.path.exists(cf):
        return json.load(io.open(cf, encoding='utf-8'))
    url = f'https://api.crossref.org/works/{urllib.request.quote(doi)}?mailto={MAILTO}'
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=40) as r:
                msg = json.load(r)['message']
            json.dump(msg, io.open(cf, 'w', encoding='utf-8'))
            return msg
        except Exception as e:
            if attempt == 2:
                print(f'  WARN: could not fetch {doi}: {e}')
                return None
            time.sleep(2 * (attempt + 1))

def norm_doi(d):
    return (d or '').strip().lower()

# ---------------------------------------------------------------- inputs
srows = list(csv.DictReader(io.open(os.path.join(HERE, 'screening_log.csv'), encoding='utf-8')))
FORCED = {r['doi'] for r in srows if 'forced-seed' in (r['reason_or_note'] or '')}
RETRIEVED = {r['doi'] for r in srows} - FORCED           # the 1,550 query-retrieved
ELIGIBLE = ({r['doi'] for r in srows if r['status'].startswith('Tier')}
            - FORCED)  # the 799 Tier-1 eligible records

papers = json.load(io.open(os.path.join(HERE, 'papers_final.json'), encoding='utf-8'))
reviews = [p for p in papers if p.get('data') == 'review']           # 15 review-labelled
seeds = json.load(io.open(os.path.join(HERE, 'seeds.json'), encoding='utf-8'))

# title gate (identical to pool.py)
import pool
def gate(title):
    return title is not None and len(title) >= 25 and pool.is_battery_related(title)

# ---------------------------------------------------------------- audit
# Restriction: the retrieval itself only ever contained records dated >= 2020
# (pool.py year filter), so the capture-rate denominator is restricted to
# references that (a) carry a deposited title, (b) pass the same title gate as
# the screening pipeline, (c) are dated >= 2020 in the deposited reference
# metadata, and (d) carry a DOI that can be matched. Refs failing (a), (c) or
# (d) are counted separately, not silently dropped.
def ref_year(r):
    try:
        return int(str(r.get('year') or '')[:4])
    except (ValueError, TypeError):
        return None

# Some publishers deposit reference lists as DOI-only records (no title, no
# year). For those, resolve the referenced DOI once (cached) so the same title
# gate and year window can be applied. Resolution failures are counted, not
# silently dropped.
_resolved = {}

def resolve_ref(r):
    """Return (title, year, resolved_flag) for a reference entry."""
    title = r.get('article-title') or r.get('unstructured')
    y = ref_year(r)
    d = norm_doi(r.get('DOI') or '')
    if (title and len(title) >= 25 and y is not None) or not d:
        return title, y, False
    if d in _resolved:
        return _resolved[d]
    msg = crossref_get(d)
    if not msg:
        _resolved[d] = (title, y, False)
        return title, y, False
    t2 = (msg.get('title') or [''])[0] or title
    dp = (msg.get('issued', {}).get('date-parts') or [[None]])[0]
    y2 = dp[0] if dp and dp[0] else y
    _resolved[d] = (t2, y2, True)
    time.sleep(0.22)
    return t2, y2, True

def classify_ref(r):
    """-> ('scope', doi) with scope in denom / out_of_window / no_doi / unresolvable / off_topic."""
    d = norm_doi(r.get('DOI') or '')
    title, y, resolved = resolve_ref(r)
    if not title:
        return 'unresolvable', d
    if y is not None and y < 2020:
        return 'out_of_window', d
    if not gate(title):
        return 'off_topic', d
    if not d:
        return 'no_doi', ''
    return 'denom', d

per_source = []
all_denom, all_denom_hit, all_denom_elig = set(), set(), set()
n_resolved = 0
for p in reviews + seeds:
    doi = p['doi']
    kind = 'review' if p in reviews else 'seed'
    label = (p.get('title_pool') or p.get('title') or '')[:70]
    msg = crossref_get(doi)
    if not msg:
        per_source.append({'doi': doi, 'kind': kind, 'error': 'unreachable'})
        continue
    refs = msg.get('reference', []) or []
    c = {'denom': 0, 'out_of_window': 0, 'unresolvable': 0, 'no_doi': 0, 'off_topic': 0}
    hit = elig = 0
    for r in refs:
        scope, d = classify_ref(r)
        c[scope] += 1
        if scope == 'denom':
            all_denom.add(d)
            if d in RETRIEVED:
                hit += 1
                all_denom_hit.add(d)
            if d in ELIGIBLE:
                elig += 1
                all_denom_elig.add(d)
    per_source.append({
        'doi': doi, 'kind': kind, 'label': label,
        'n_refs': len(refs), 'refs_with_doi': sum(1 for r in refs if r.get('DOI')),
        'in_scope_2020plus': c['denom'], 'captured': hit, 'of_which_eligible': elig,
        'refs_pre2020': c['out_of_window'], 'refs_unresolvable': c['unresolvable'],
        'refs_no_doi_in_scope': c['no_doi'], 'refs_off_topic': c['off_topic'],
    })
    print(f"  audited {doi} ({kind}): denom {c['denom']}, captured {hit}")
    time.sleep(0.12)

print(f'DOI resolutions performed: {sum(1 for v in _resolved.values() if v)} of {len(_resolved)} attempted')

rev = [s for s in per_source if s['kind'] == 'review' and 'error' not in s]
seed_rows = [s for s in per_source if s['kind'] == 'seed' and 'error' not in s]

def tot(rows, k):
    return sum(r.get(k, 0) for r in rows)

def block(rows):
    denom = tot(rows, 'in_scope_2020plus')
    cap = tot(rows, 'captured')
    return {
        'n_sources': len(rows),
        'refs_total': tot(rows, 'n_refs'),
        'denominator_in_scope_2020plus_doi': denom,
        'captured': cap,
        'capture_rate': round(cap / denom, 4) if denom else None,
        'captured_of_which_eligible': tot(rows, 'of_which_eligible'),
        'refs_pre2020': tot(rows, 'refs_pre2020'),
        'refs_unresolvable': tot(rows, 'refs_unresolvable'),
        'refs_no_doi_in_scope': tot(rows, 'refs_no_doi_in_scope'),
        'refs_off_topic': tot(rows, 'refs_off_topic'),
    }

summary_reviews = block(rev)
summary_seeds = block(seed_rows)
combined = {
    'n_sources': len(rev) + len(seed_rows),
    'refs_total': summary_reviews['refs_total'] + summary_seeds['refs_total'],
    'denominator_in_scope_2020plus_doi':
        summary_reviews['denominator_in_scope_2020plus_doi'] + summary_seeds['denominator_in_scope_2020plus_doi'],
    'captured': summary_reviews['captured'] + summary_seeds['captured'],
    'captured_of_which_eligible':
        summary_reviews['captured_of_which_eligible'] + summary_seeds['captured_of_which_eligible'],
    'refs_pre2020': summary_reviews['refs_pre2020'] + summary_seeds['refs_pre2020'],
    'refs_unresolvable': summary_reviews['refs_unresolvable'] + summary_seeds['refs_unresolvable'],
    'refs_no_doi_in_scope': summary_reviews['refs_no_doi_in_scope'] + summary_seeds['refs_no_doi_in_scope'],
    'refs_off_topic': summary_reviews['refs_off_topic'] + summary_seeds['refs_off_topic'],
}
combined['capture_rate'] = (round(combined['captured'] / combined['denominator_in_scope_2020plus_doi'], 4)
                            if combined['denominator_in_scope_2020plus_doi'] else None)

uniq, uniq_hit, uniq_elig = all_denom, all_denom_hit, all_denom_elig  # unique across all 21 sources

# Poh check
POH = '10.1109/tec.2025.3548400'
poh_cited_by = [p['doi'] for p in reviews + seeds
                if POH in {norm_doi(r.get('DOI') or '') for r in (crossref_get(p['doi']) or {}).get('reference', [])}]

# ---------------------------------------------------------------- per-query yields
AREA_OF_KEY = pool.AREA_OF_KEY
def area_of(key):
    for prefix, area in AREA_OF_KEY.items():
        if key.startswith(prefix):
            return area
    return 'Other'

qyield = {}
for f in sorted(glob.glob(os.path.join(HERE, 'raw/*.json'))):
    key = os.path.basename(f)[:-5]
    fam = key.rsplit('_', 1)[0]
    try:
        data = json.load(io.open(f, encoding='utf-8'))
    except Exception:
        continue
    items = data.get('message', {}).get('items', []) if isinstance(data, dict) else []
    n = 0
    for it in items:
        doi = it.get('DOI', '').lower()
        if not doi or it.get('type') != 'journal-article':
            continue
        title = (it.get('title') or [''])[0]
        if not title or len(title) < 25:
            continue
        dp = (it.get('issued', {}).get('date-parts') or [[None]])[0]
        if not dp or not dp[0] or dp[0] < 2020:
            continue
        n += 1
    qyield.setdefault(fam, {'records': 0, 'files': 0, 'area': area_of(fam)})
    qyield[fam]['records'] += n
    qyield[fam]['files'] += 1

per_query = [{'query': k, 'area': v['area'], 'passes': v['files'], 'records_after_filters': v['records']}
             for k, v in sorted(qyield.items(), key=lambda kv: -kv[1]['records'])]

out = {
    'retrieved_set_size': len(RETRIEVED),
    'per_source': per_source,
    'summary_reviews': summary_reviews,
    'summary_seeds': summary_seeds,
    'summary_combined': combined,
    'unique_in_scope_2020plus_refs_with_doi': len(uniq),
    'unique_in_scope_captured': len(uniq_hit),
    'unique_in_scope_capture_rate': round(len(uniq_hit) / len(uniq), 4) if uniq else None,
    'unique_in_scope_of_which_eligible': len(uniq_elig),
    'poh_doi_in_review_reference_lists': poh_cited_by,
    'per_query_yields': per_query,
    'query_design_caps': {'rows_per_pass': 20, 'passes_per_query': 5,
                          'max_records_per_query_family': 100,
                          'query_pass_records_after_filters': sum(q['records_after_filters'] for q in per_query),
                          'unique_after_dedup': len(RETRIEVED)},
    'method_note': (
        'Capture rate = share of references cited by the 15 included reviews + 6 seeds that the '
        '1,550-record query retrieval contains. Denominator restricted to references that pass the '
        'same battery-term AND ML-term title gate as the screening pipeline and are dated 2020 or '
        'later (the retrieval window); titles and years are taken from the deposited reference '
        'metadata where present and otherwise resolved by DOI (cached in raw_cache/). References '
        'pre-2020, unresolvable, without DOIs, or failing the title gate are counted separately in '
        'the summary blocks. This estimates retrieval recall against a review-curated ground truth, '
        'not against the true literature: the denominator is itself a citation-conditioned sample.'
    ),
}
json.dump(out, io.open(os.path.join(HERE, 'recall_audit.json'), 'w', encoding='utf-8'), indent=1)

print(json.dumps({k: v for k, v in out.items() if k not in ('per_source', 'per_query_yields')}, indent=1))
print()
print('per-review:')
for r in rev:
    isc = r['in_scope_2020plus']; isc_h = r['captured']
    print(f"  {r['doi'][:38]:40} refs {r['n_refs']:4} (doi {r['refs_with_doi']:4}) "
          f"in-scope-2020+ {isc:3} captured {isc_h:3} ({(isc_h/isc*100 if isc else 0):5.1f}%)")
print()
print('per-query yields (top 12):')
for q in per_query[:12]:
    print(f"  {q['query']:12} {q['records_after_filters']:4} records / {q['passes']} passes")
print('  ...', len(per_query), 'query families total;',
      sum(q['records_after_filters'] for q in per_query), 'query-pass records after filters (pre-dedup)')
