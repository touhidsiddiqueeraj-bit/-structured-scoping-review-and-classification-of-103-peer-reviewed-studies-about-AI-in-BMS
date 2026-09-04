#!/bin/bash
# Fetch candidate papers from CrossRef bibliographic queries, one file per query.
# Polite pool: include mailto. rows=20, journal articles only, 2020+.
BASE="https://api.crossref.org/works"
MAILTO="review.study%40example.org"
SELECT="DOI,title,container-title,issued,is-referenced-by-count,author,type,published-print,published-online"
OUT=/home/touhid/Documents/reviewpaper/corpus/raw

declare -A QUERIES
QUERIES[soc_ml]="state of charge estimation lithium-ion battery machine learning"
QUERIES[soc_dl]="state of charge estimation deep learning lithium-ion battery LSTM"
QUERIES[soc_hybrid]="state of charge estimation neural network battery filter"
QUERIES[soh_ml]="state of health estimation lithium-ion battery machine learning"
QUERIES[soh_feat]="battery state of health estimation charging curve health features"
QUERIES[soh_gp]="battery state of health Gaussian process regression lithium-ion"
QUERIES[rul_ml]="remaining useful life prediction lithium-ion battery machine learning"
QUERIES[rul_dl]="battery remaining useful life prediction deep learning"
QUERIES[rul_early]="early prediction battery cycle life machine learning data-driven"
QUERIES[chg_ml]="fast charging lithium-ion battery machine learning optimization"
QUERIES[chg_rl]="reinforcement learning charging strategy lithium-ion battery"
QUERIES[chg_bayes]="Bayesian optimization battery charging protocol lithium-ion"
QUERIES[thm_est]="lithium-ion battery temperature estimation data-driven"
QUERIES[thm_mgr]="thermal management electric vehicle battery machine learning"
QUERIES[thm_run]="thermal runaway prediction lithium-ion battery machine learning"
QUERIES[flt_diag]="lithium-ion battery fault diagnosis machine learning"
QUERIES[flt_anom]="battery anomaly detection electric vehicle data-driven"
QUERIES[flt_plate]="lithium plating detection machine learning battery"
QUERIES[bal]="cell balancing lithium-ion battery machine learning"
QUERIES[ecm]="equivalent circuit model parameter identification battery machine learning"
QUERIES[rev_bms]="machine learning battery management system review"
QUERIES[pinn]="physics-informed neural network lithium-ion battery"
QUERIES[tl]="transfer learning battery state of health lithium-ion"
QUERIES[twin]="digital twin lithium-ion battery machine learning"
QUERIES[llm]="large language model battery"
QUERIES[gnn]="graph neural network battery degradation"
QUERIES[bmk]="battery degradation dataset benchmark machine learning"
QUERIES[interp]="interpretable machine learning battery degradation mechanism"
QUERIES[cloud]="cloud battery management electric vehicle fleet data"
QUERIES[second]="second-life battery state of estimation machine learning"

for key in "${!QUERIES[@]}"; do
  q=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "${QUERIES[$key]}")
  url="$BASE?query.bibliographic=$q&filter=type:journal-article,from-pub-date:2020-01-01&rows=22&select=$SELECT&sort=is-referenced-by-count&order=desc&mailto=$MAILTO"
  curl -s --max-time 40 "$url" -o "$OUT/${key}_cited.json"
  sleep 1
  url2="$BASE?query.bibliographic=$q&filter=type:journal-article,from-pub-date:2024-06-01&rows=15&select=$SELECT&sort=relevance&mailto=$MAILTO"
  curl -s --max-time 40 "$url2" -o "$OUT/${key}_recent.json"
  sleep 1
  echo "done: $key"
done
echo "ALL DONE"
