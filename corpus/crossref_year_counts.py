#!/usr/bin/env python3
"""Per-year Crossref result counts (denominators) for the same 30 bibliographic
queries used by fetch_crossref.sh. Writes per_year_denominators.json."""
import json, urllib.parse, urllib.request, time, os

QUERIES = {
 "soc_ml": "state of charge estimation lithium-ion battery machine learning",
 "soc_dl": "state of charge estimation deep learning lithium-ion battery LSTM",
 "soc_hybrid": "state of charge estimation neural network battery filter",
 "soh_ml": "state of health estimation lithium-ion battery machine learning",
 "soh_feat": "battery state of health estimation charging curve health features",
 "soh_gp": "battery state of health Gaussian process regression lithium-ion",
 "rul_ml": "remaining useful life prediction lithium-ion battery machine learning",
 "rul_dl": "battery remaining useful life prediction deep learning",
 "rul_early": "early prediction battery cycle life machine learning data",
 "rev_bms": "machine learning battery management system review",
 "pinn": "physics-informed neural network lithium-ion battery",
 "tl": "transfer learning battery state of health lithium-ion",
 "twin": "digital twin lithium-ion battery machine learning",
 "llm": "large language model battery",
 "gnn": "graph neural network battery degradation",
 "bmk": "battery degradation dataset benchmark machine learning",
 "interp": "interpretable machine learning battery degradation mechanism",
 "cloud": "cloud battery management electric vehicle fleet data",
 "second": "second-life battery state of estimation machine learning",
 "bal": "battery cell balancing machine learning",
 "chg_ml": "machine learning charging strategy lithium-ion battery",
 "chg_bayes": "bayesian optimization battery charging protocols",
 "chg_rl": "reinforcement learning battery charging control",
 "thermal_ml": "machine learning thermal management lithium-ion battery",
 "fault_ml": "machine learning fault diagnosis lithium-ion battery",
 "soc_filter": "sigma point kalman filter battery state of charge estimation",
 "eis_ml": "impedance spectroscopy machine learning lithium-ion battery",
 "soctemp": "battery internal temperature estimation machine learning",
 "soc_pubdata": "public dataset battery degradation machine learning",
 "aging_ml": "battery aging model machine learning prediction",
}

BASE = "https://api.crossref.org/works"
MAILTO = "review.study%40example.org"
years = list(range(2020, 2027))
out = {q: {} for q in QUERIES}
totals = {y: 0 for y in years}
ok = 0
for q, full in QUERIES.items():
    qq = urllib.parse.quote(full)
    for y in years:
        url = (f"{BASE}?query.bibliographic={qq}"
               f"&filter=type:journal-article,from-pub-date:{y}-01-01,until-pub-date:{y}-12-31&rows=0&mailto={MAILTO}")
        try:
            with urllib.request.urlopen(url, timeout=40) as r:
                n = json.load(r)["message"]["total-results"]
            out[q][y] = n
            totals[y] += n
            ok += 1
        except Exception as e:
            print("FAIL", q, y, e)
            out[q][y] = None
        time.sleep(0.4)

json.dump({"queries": out, "totals_per_year": totals, "ok": ok},
          open("corpus/per_year_denominators.json", "w"), indent=1)
print("OK queries:", ok, "/", len(QUERIES) * len(years))
print("totals:", totals)
