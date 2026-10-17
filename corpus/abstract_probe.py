#!/usr/bin/env python3
"""Abstract-level probes (reviewer round-3, M3 + M6).

Probe A (M3, representativeness): a seed-pinned uniform random sample of n=40
from the 799 Tier-1 eligible records, coded at abstract level for (i) record
type and (ii) whether the abstract STATES any validation-protocol evidence
(isolation or deployment). Purpose: test whether the classified subset's
selection distorted stated validation evidence relative to the pool it was
drawn from. Abstract-level statement is NOT full-text protocol coding; the
probe bounds and bridges, it does not replace Section 3.4's full-text counts.

Probe B (M6, baseline-comparison screen): the 88 primary-application papers,
coded at abstract level for whether the study compares its estimator against a
model-based baseline (EKF/UKF/Kalman filter, observer, equivalent-circuit
model, physics-based model, Gaussian-process or other classical regressor).

This script only FETCHES and stages the abstracts (Crossref, cached under
raw_cache/) and writes empty coding sheets; the codes themselves are filled in
by the review team in abstract_probe.json (single-coder, rubric below), and
summarized by summarize() once codes exist.

Rubric (Probe A 'validation_evidence_in_abstract'):
  isolation_stated     - abstract names an unseen-data protocol (test on unseen
                         cells/vehicles/chemistries, held-out fleet, online or
                         onboard demonstration)
  evaluation_stated    - abstract reports errors/experiments on data without an
                         isolation or deployment claim
  none_stated          - no evaluation statement at all (incl. reviews)
Rubric (Probe B 'baseline_comparison'):
  none                 - no model-based baseline mentioned
  mentioned            - a model-based baseline is named as comparison
  stated_samedata      - abstract states the comparison on the same data with a
                         quantitative result
"""
import csv, io, json, os, random, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, 'raw_cache')
os.makedirs(CACHE, exist_ok=True)
MAILTO = 'mlbms-review@example.org'
SEED = 42
N_SAMPLE = 40


def crossref_get(doi):
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
                print(f'  WARN: cannot fetch {doi}: {e}')
                return None
            time.sleep(2 * (attempt + 1))


def clean_abstract(msg):
    """Crossref abstracts are JATS-flavored XML; strip to plain text."""
    import re
    a = msg.get('abstract')
    if not a:
        return ''
    t = re.sub(r'<[^>]+>', ' ', a)
    t = re.sub(r'\s+', ' ', t).strip()
    return t


OACACHE = os.path.join(HERE, 'raw_cache', 'openalex')
os.makedirs(OACACHE, exist_ok=True)
S2CACHE = os.path.join(HERE, 'raw_cache', 'semanticscholar')
os.makedirs(S2CACHE, exist_ok=True)


def s2_abstract(doi):
    """Semantic Scholar Graph API backfill (Elsevier-withheld abstracts often present)."""
    import re
    safe = doi.replace('/', '_')
    cf = os.path.join(S2CACHE, safe + '.json')
    if os.path.exists(cf):
        return json.load(io.open(cf, encoding='utf-8')).get('abstract') or ''
    url = (f'https://api.semanticscholar.org/graph/v1/paper/DOI:{urllib.request.quote(doi)}'
           f'?fields=abstract')
    ab = ''
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'mlbms-scoping-review/1.0'})
            with urllib.request.urlopen(req, timeout=40) as r:
                ab = json.load(r).get('abstract') or ''
            break
        except urllib.error.HTTPError as e:
            if e.code == 429:  # rate limited: back off
                time.sleep(6 * (attempt + 1))
                continue
            break
        except Exception as e:
            time.sleep(3)
    json.dump({'abstract': ab}, io.open(cf, 'w', encoding='utf-8'))
    if ab:
        time.sleep(1.05)  # stay under the unauthenticated rate limit
    return re.sub(r'\s+', ' ', ab).strip()


def openalex_abstract(doi):
    """Fetch the OpenAlex record and rebuild the abstract from its inverted index."""
    safe = doi.replace('/', '_')
    cf = os.path.join(OACACHE, safe + '.json')
    if os.path.exists(cf):
        inv = json.load(io.open(cf, encoding='utf-8'))
    else:
        url = f'https://api.openalex.org/works/doi:{urllib.request.quote(doi)}?mailto={MAILTO}'
        try:
            with urllib.request.urlopen(url, timeout=40) as r:
                inv = json.load(r).get('abstract_inverted_index')
        except Exception as e:
            print(f'  WARN openalex miss {doi}: {e}')
            inv = None
        json.dump(inv, io.open(cf, 'w', encoding='utf-8'))
        time.sleep(0.12)
    if not inv:
        return ''
    pos = {}
    for word, idxs in inv.items():
        for i in idxs:
            pos[i] = word
    return ' '.join(pos[i] for i in sorted(pos))


def get_abstract(doi, crossref_msg):
    """Crossref abstract first, OpenAlex and Semantic Scholar backfill second."""
    a = clean_abstract(crossref_msg) if crossref_msg else ''
    src = 'crossref' if a else 'none'
    if len(a) >= 200:
        return a, src
    b = openalex_abstract(doi)
    if len(b) > len(a):
        a, src = b, 'openalex'
    if len(a) >= 200:
        return a, src
    c = s2_abstract(doi)
    if len(c) > len(a):
        return c, 'semanticscholar'
    return a, src


srows = list(csv.DictReader(io.open(os.path.join(HERE, 'screening_log.csv'), encoding='utf-8')))
FORCED = {r['doi'] for r in srows if 'forced-seed' in (r['reason_or_note'] or '')}
ELIGIBLE = [r for r in srows if r['status'].startswith('Tier') and r['doi'] not in FORCED]
assert len(ELIGIBLE) == 799, len(ELIGIBLE)
SUBSET = {r['doi'] for r in srows if r['status'].startswith('Tier2')}

# ---------------- Probe A: uniform seed-pinned sample of the 799
rng = random.Random(SEED)
sample = rng.sample(ELIGIBLE, N_SAMPLE)

probeA = []
for r in sample:
    msg = crossref_get(r['doi'])
    ab, src = get_abstract(r['doi'], msg)
    probeA.append({
        'doi': r['doi'], 'title': r['title'], 'journal': r['journal'],
        'year': r['year'], 'in_classified_subset': r['doi'] in SUBSET,
        'abstract': ab, 'abstract_source': src, 'fetch_ok': msg is not None,
    })

# ---------------- Probe B: the 88 primary papers
papers = json.load(io.open(os.path.join(HERE, 'papers_final.json'), encoding='utf-8'))
primary = [p for p in papers if p.get('data') != 'review']
assert len(primary) == 88, len(primary)

probeB = []
for p in primary:
    msg = crossref_get(p['doi'])
    ab, src = get_abstract(p['doi'], msg)
    probeB.append({
        'doi': p['doi'], 'title': p.get('title_pool') or p.get('title_cr'),
        'journal': p.get('journal'), 'year': p.get('year'),
        'function': p.get('area'), 'method_family': p.get('method'),
        'abstract': ab, 'abstract_source': src, 'fetch_ok': msg is not None,
    })

json.dump({'seed': SEED, 'n_sample': N_SAMPLE,
           'probeA_pool_sample': probeA, 'probeB_primary_papers': probeB},
          io.open(os.path.join(HERE, 'abstract_probe_raw.json'), 'w', encoding='utf-8'), indent=1)

nA = sum(1 for x in probeA if x['abstract'])
nB = sum(1 for x in probeB if x['abstract'])
print(f'Probe A: {len(probeA)} sampled, {nA} with Crossref abstract '
      f'({100*nA//len(probeA)}%); subset members in sample: '
      f'{sum(1 for x in probeA if x["in_classified_subset"])}')
print(f'Probe B: {len(probeB)} primary papers, {nB} with Crossref abstract ({100*nB//len(probeB)}%)')
print('wrote abstract_probe_raw.json - now code the sheets')
