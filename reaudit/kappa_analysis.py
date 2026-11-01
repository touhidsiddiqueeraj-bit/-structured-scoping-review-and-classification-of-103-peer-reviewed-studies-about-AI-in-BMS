#!/usr/bin/env python3
"""kappa_analysis.py — agreement statistics for the BMS validation-audit re-coding.

Reads the two coder sheets from Coding_Workbook_v2.xlsx (or two CSVs with the
same layout: first column Study ID, then columns V1..V14), aligns them on
study ID, and reports per variable:

  * N double-coded studies
  * raw percent agreement
  * Cohen's kappa (unweighted, all categories incl. NR)
  * PABAK  = (K * Po - 1) / (K - 1), K = number of admissible categories
  * linearly and quadratically weighted kappa (ordinal variables; numeric
    codes only, exclusions counted)
  * bootstrap 95% confidence intervals (percentile method)
  * confusion matrix (CSV per variable)
  * the pre-declared collapse rule: if a single pair of adjacent categories
    accounts for > 50% of disagreements, report the collapsed kappa too
  * an auto-filled version of the manuscript reporting sentence
    (codebook section 6.3)

Optionally computes Fleiss's kappa for a three-coder design (--fleiss with a
third sheet/CSV whose codes are treated as the third rater).

Usage:
  python kappa_analysis.py --workbook Coding_Workbook_v2.xlsx [--out outdir]
      [--bootstrap 10000] [--seed 42] [--fleiss Coder3] [--heatmap]
  python kappa_analysis.py --csv1 coder1.csv --csv2 coder2.csv [--out outdir]
  python kappa_analysis.py --selftest          # known-answer assertions
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from collections import Counter

import numpy as np

VARS = [
    ("V1", "Estimation target", "nominal",
     ["SOC", "SOH", "SOP", "RUL", "capacity-fade", "fault-anomaly", "temperature", "charging-strategy", "multi-target"]),
    ("V2", "ML paradigm", "nominal",
     ["supervised-regression", "supervised-classification", "unsupervised", "semi-supervised", "reinforcement-learning", "physics-informed-hybrid", "ensemble-of-learned-models"]),
    ("V3", "Data source", "nominal", ["public-dataset", "own-lab", "industry-provided", "synthetic-simulated", "mixed"]),
    ("V4", "Cell chemistry", "nominal",
     ["LFP", "NMC", "NCA", "LTO", "LCO", "other", "not-specified", "mixed", "pack-level-unspecified"]),
    ("V5", "Validation split design", "nominal",
     ["random-split", "temporal-split", "k-fold-CV", "nested-CV", "leave-one-cell-out", "leave-one-chemistry-out", "leave-one-dataset-out", "train-test-only", "NR"]),
    ("V6", "Test-set independence", "ordinal", ["4", "3", "2", "1", "0", "NR"]),
    ("V7", "Ground-truth quality", "ordinal", ["3", "2", "1", "0", "NR"]),
    ("V8", "Baseline comparison", "nominal",
     ["none", "heuristics-or-trivial", "physics-based-model", "other-ML-only", "physics-and-ML-baselines"]),
    ("V9", "Error reporting", "nominal",
     ["point-metrics-only", "metrics-plus-distribution", "metrics-distribution-significance"]),
    ("V10", "Robustness stress (count)", "ordinal", ["4", "3", "2", "1", "0"]),
    ("V11", "Deployment readiness", "ordinal", ["4", "3", "2", "1", "0"]),
    ("V12", "Onboard feasibility", "ordinal", ["3", "2", "1", "none"]),
    ("V13", "Reproducibility (count)", "ordinal", ["4", "3", "2", "1", "0"]),
    ("V14", "Transportation relevance", "nominal", ["generic-battery", "EV-or-HEV-oriented", "other-transport"]),
]
VAR_IDS = [v[0] for v in VARS]
ORDINAL = {v[0] for v in VARS if v[2] == "ordinal"}
CODES = {v[0]: v[3] for v in VARS}
GATE = 0.70
BELOW_DICHOT = 0.60
LANDIS_KOCH = [(0.81, "almost perfect"), (0.61, "substantial"), (0.41, "moderate"),
               (0.21, "fair"), (0.00, "slight"), (-1.01, "poor")]


# ---------------------------------------------------------------- statistics
def cohen_kappa(a, b, categories=None):
    """Unweighted Cohen's kappa. a, b: lists of hashable codes, equal length."""
    n = len(a)
    if n == 0:
        return None
    cats = list(categories) if categories else sorted(set(a) | set(b), key=str)
    idx = {c: i for i, c in enumerate(cats)}
    obs = np.zeros((len(cats), len(cats)))
    for x, y in zip(a, b):
        obs[idx[x], idx[y]] += 1
    po = np.trace(obs) / n
    p1 = obs.sum(axis=1) / n
    p2 = obs.sum(axis=0) / n
    pe = float((p1 * p2).sum())
    if pe == 1.0:
        return 1.0
    return (po - pe) / (1 - pe)


def pabak(po, k):
    if k <= 1:
        return None
    return (k * po - 1) / (k - 1)


def weighted_kappa(a, b, categories, weight="linear"):
    """Weighted kappa on ordinal categories (numeric strings, ascending order).
    Returns (kappa, n_used, n_excluded)."""
    num = [c for c in categories if str(c).lstrip("-").isdigit()]
    pairs = [(x, y) for x, y in zip(a, b) if x in num and y in num]
    excluded = len(a) - len(pairs)
    if not pairs:
        return None, 0, excluded
    lev = {c: i for i, c in enumerate(num)}
    K = len(num)
    if K < 2:
        return None, len(pairs), excluded
    obs = np.zeros((K, K))
    for x, y in pairs:
        obs[lev[x], lev[y]] += 1
    n = obs.sum()
    if weight == "linear":
        w = np.array([[1 - abs(i - j) / (K - 1) for j in range(K)] for i in range(K)])
    else:  # quadratic
        w = np.array([[1 - ((i - j) / (K - 1)) ** 2 for j in range(K)] for i in range(K)])
    p1 = obs.sum(axis=1) / n
    p2 = obs.sum(axis=0) / n
    pe = float((p1[:, None] * p2[None, :] * w).sum())
    po = float((obs / n * w).sum())
    if pe == 1.0:
        return 1.0, len(pairs), excluded
    return (po - pe) / (1 - pe), len(pairs), excluded


def fleiss_kappa(ratings):
    """ratings: list per item of a list of codes (n raters, same raters per item)."""
    n_raters = len(ratings[0])
    if n_raters < 2:
        return None
    cats = sorted({c for item in ratings for c in item}, key=str)
    p_j = Counter(c for item in ratings for c in item)
    total = sum(p_j.values())
    pe = sum((v / total) ** 2 for v in p_j.values())
    P_i = []
    for item in ratings:
        cnt = Counter(item)
        P_i.append(sum(v * (v - 1) for v in cnt.values()) / (n_raters * (n_raters - 1)))
    Pbar = float(np.mean(P_i))
    if pe == 1.0:
        return 1.0
    return (Pbar - pe) / (1 - pe)


def bootstrap_ci(fn, a, b, n_boot, seed, categories=None):
    """Percentile bootstrap CI for any two-rater statistic fn(a, b)."""
    if len(a) < 2:
        return (None, None)
    rng = np.random.default_rng(seed)
    n = len(a)
    vals = []
    a_arr, b_arr = np.array(a, dtype=object), np.array(b, dtype=object)
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        v = fn(a_arr[idx].tolist(), b_arr[idx].tolist(), categories=categories) \
            if categories else fn(a_arr[idx].tolist(), b_arr[idx].tolist())
        if v is not None:
            vals.append(v)
    if not vals:
        return (None, None)
    return (float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5)))


def lk_label(k):
    for lo, lab in LANDIS_KOCH:
        if k >= lo:
            return lab
    return "poor"


def confusion(a, b, categories):
    idx = {c: i for i, c in enumerate(categories)}
    m = np.zeros((len(categories), len(categories)), dtype=int)
    for x, y in zip(a, b):
        if x in idx and y in idx:
            m[idx[x], idx[y]] += 1
    return m


def collapse_check(a, b, categories):
    """Pre-declared collapse rule: the most-confused pair of ADJACENT categories
    (adjacent in the variable's declared order) accounting for > 50% of
    disagreements. Returns (pair or None, share)."""
    m = confusion(a, b, categories)
    dis = m.sum() - np.trace(m)
    if dis == 0:
        return None, 0.0
    best, best_n = None, 0
    for i in range(len(categories)):
        for j in range(i + 1, len(categories)):
            if j - i != 1:            # adjacent only
                continue
            n_ij = m[i, j] + m[j, i]
            if n_ij > best_n:
                best_n, best = n_ij, (categories[i], categories[j])
    if best is None:
        return None, 0.0
    return best, best_n / dis


# ---------------------------------------------------------------- data input
def read_workbook(path, sheet):
    from openpyxl import load_workbook
    wb = load_workbook(path, data_only=True)
    if sheet not in wb.sheetnames:
        sys.exit(f"error: sheet '{sheet}' not found in {path}")
    ws = wb[sheet]
    # header row 4: B=Study ID, C..P = V1..V14
    data = {}
    for r in range(5, ws.max_row + 1):
        sid = ws.cell(row=r, column=2).value
        if sid is None or str(sid).strip() == "":
            continue
        sid = str(sid).strip()
        if not sid.upper().startswith("S") and not sid.upper().startswith("D"):
            continue
        row = {}
        for i, vid in enumerate(VAR_IDS):
            v = ws.cell(row=r, column=3 + i).value
            row[vid] = None if v is None or str(v).strip() == "" else str(v).strip()
        data[sid] = row
    return data


def read_csv(path):
    data = {}
    with open(path, newline="", encoding="utf-8-sig") as f:
        rdr = csv.reader(f)
        header = [h.strip() for h in next(rdr)]
        # first column = study id, remaining columns with V# headers
        vcols = {h: i + 1 for i, h in enumerate(header[1:]) if h.strip().upper().startswith("V")}
        for row in rdr:
            if not row or not row[0].strip():
                continue
            sid = row[0].strip()
            data[sid] = {vid: (row[i].strip() or None) if i < len(row) else None
                         for vid, i in vcols.items()}
    return data


def align(d1, d2):
    common = [s for s in d1 if s in d2]
    only1 = [s for s in d1 if s not in d2]
    only2 = [s for s in d2 if s not in d1]
    return common, only1, only2


# ---------------------------------------------------------------- analysis
def analyse(c1, c2, n_boot, seed, outdir, heatmaps=False):
    rows = []
    collapse_notes = []
    per_var_pairs = {}
    for vid, name, scale, codes in VARS:
        a = [c1[s][vid] for s in c1 if c1[s].get(vid) and c2.get(s, {}).get(vid)]
        b = [c2[s][vid] for s in c1 if c1[s].get(vid) and c2.get(s, {}).get(vid)]
        # keep pair order aligned
        ids = [s for s in c1 if c1[s].get(vid) and c2.get(s, {}).get(vid)]
        a = [c1[s][vid] for s in ids]
        b = [c2[s][vid] for s in ids]
        per_var_pairs[vid] = (a, b)
        n = len(a)
        if n == 0:
            rows.append(dict(var=vid, name=name, n=0))
            continue
        po = float(np.mean([x == y for x, y in zip(a, b)]))
        k = cohen_kappa(a, b, codes)
        pk = pabak(po, len(codes))
        lo, hi = bootstrap_ci(cohen_kappa, a, b, n_boot, seed, categories=codes)
        row = dict(var=vid, name=name, n=n, agree=po, kappa=k, kappa_lo=lo, kappa_hi=hi,
                   pabak=pk, lk=lk_label(k) if k is not None else "")
        if vid in ORDINAL:
            kw_l, nu, nex = weighted_kappa(a, b, codes, "linear")
            kw_q, _, _ = weighted_kappa(a, b, codes, "quadratic")
            row.update(kw_linear=kw_l, kw_quadratic=kw_q, w_excluded=nex)
        pair, share = collapse_check(a, b, codes)
        if pair is not None and share > 0.5:
            merged = f"{pair[0]}/{pair[1]}"
            a2 = [merged if x in pair else x for x in a]
            b2 = [merged if x in pair else x for x in b]
            codes2 = [merged if c in pair else c for c in codes]
            kc = cohen_kappa(a2, b2, codes2)
            row["collapsed_pair"] = f"{pair[0]}+{pair[1]}"
            row["collapsed_share"] = round(share, 3)
            row["collapsed_kappa"] = kc
            collapse_notes.append(
                f"{vid}: {pair[0]} / {pair[1]} confusions are {share:.0%} of all disagreements "
                f"(pre-declared rule applies); kappa {k:.2f} collapsed to {kc:.2f}.")
        rows.append(row)
        # confusion matrix CSV
        m = confusion(a, b, codes)
        with open(os.path.join(outdir, f"confusion_{vid}.csv"), "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["C1 \\ C2"] + [str(c) for c in codes])
            for i, c in enumerate(codes):
                w.writerow([str(c)] + [int(x) for x in m[i]])
        if heatmaps:
            make_heatmap(m, codes, vid, outdir)
    return rows, collapse_notes, per_var_pairs


def make_heatmap(m, codes, vid, outdir):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(5, 4), constrained_layout=True)
    im = ax.imshow(m, cmap="Blues")
    ax.set_xticks(range(len(codes)), [str(c) for c in codes], rotation=45, ha="right")
    ax.set_yticks(range(len(codes)), [str(c) for c in codes])
    ax.set_xlabel("Coder 2"); ax.set_ylabel("Coder 1"); ax.set_title(f"{vid} confusion")
    for i in range(len(codes)):
        for j in range(len(codes)):
            if m[i, j] > 0:
                ax.text(j, i, int(m[i, j]), ha="center", va="center",
                        color="white" if m[i, j] > m.max() / 2 else "black", fontsize=8)
    fig.colorbar(im, shrink=0.8)
    fig.savefig(os.path.join(outdir, f"confusion_{vid}.png"), dpi=150)
    plt.close(fig)


def write_report(rows, collapse_notes, outdir, n_boot, fleiss=None):
    csv_path = os.path.join(outdir, "kappa_report.csv")
    fields = ["var", "name", "n", "agree", "kappa", "kappa_lo", "kappa_hi", "pabak",
              "kw_linear", "kw_quadratic", "w_excluded", "lk",
              "collapsed_pair", "collapsed_share", "collapsed_kappa"]
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()})

    ks = [r["kappa"] for r in rows if r.get("kappa") is not None]
    md = ["# Agreement report — BMS validation-audit re-coding", "",
          f"Bootstrap: {n_boot} resamples, percentile 95% CI. "
          f"Gate: kappa >= {GATE} (calibration); dichotomisation threshold: {BELOW_DICHOT}.", ""]
    md.append("| Var | Variable | N | Raw agr. | kappa | 95% CI | PABAK | wK lin | wK quad | Landis-Koch |")
    md.append("|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        if r.get("n", 0) == 0:
            md.append(f"| {r['var']} | {r['name']} | 0 | - | - | - | - | - | - | awaiting codes |")
            continue
        ci = f"[{r['kappa_lo']:.2f}, {r['kappa_hi']:.2f}]" if r.get("kappa_lo") is not None else "-"
        wl = f"{r['kw_linear']:.2f}" if r.get("kw_linear") is not None else "-"
        wq = f"{r['kw_quadratic']:.2f}" if r.get("kw_quadratic") is not None else "-"
        md.append(f"| {r['var']} | {r['name']} | {r['n']} | {r['agree']:.1%} | "
                  f"{r['kappa']:.2f} | {ci} | {r['pabak']:.2f} | {wl} | {wq} | {r['lk']} |")
    md.append("")
    if collapse_notes:
        md.append("## Pre-declared collapse rule applied")
        md.extend("- " + c for c in collapse_notes)
        md.append("")
    if fleiss is not None:
        md.append(f"## Fleiss kappa (three-coder design)\n\n{fleiss:.2f}\n")
    if ks:
        below = [r["var"] for r in rows if r.get("kappa") is not None and r["kappa"] < BELOW_DICHOT]
        passed = sum(1 for k in ks if k >= GATE)
        collapsed = [r["var"] for r in rows if r.get("collapsed_pair")]
        sentence = (
            f"The initial pilot coding achieved kappa = 0.48; following codebook revision to version 2.0, "
            f"calibration against the {GATE:.2f} gate, blinded double-coding of all 103 studies, and "
            f"adjudicated resolution, the re-audit achieved a median per-variable kappa of "
            f"{float(np.median(ks)):.2f} (range {min(ks):.2f} to {max(ks):.2f}); {passed} of {len(ks)} "
            f"variables reached the calibration gate, {len(collapsed)} required the pre-declared collapse rule"
            + (f" ({', '.join(collapsed)})" if collapsed else "")
            + f", and {len(below)} remained below {BELOW_DICHOT:.2f}"
            + (f" ({', '.join(below)}) and were dichotomised for all headline analyses." if below else "."))
        md.append("## Manuscript reporting sentence (codebook section 6.3, auto-filled)")
        md.append("")
        md.append("> " + sentence)
    with open(os.path.join(outdir, "kappa_report.md"), "w") as f:
        f.write("\n".join(md) + "\n")
    print(f"wrote {csv_path}")
    print(f"wrote {os.path.join(outdir, 'kappa_report.md')}")
    return md


# ---------------------------------------------------------------- self-test
def selftest():
    # 1. perfect agreement -> kappa 1
    a = ["0", "1", "2", "0", "1"]
    assert abs(cohen_kappa(a, a[:], ["2", "1", "0"]) - 1.0) < 1e-12
    # 2. known hand-computed example
    #    rater1: 0,0,1,1,2,2 ; rater2: 0,1,1,1,2,2
    #    po = 5/6 ; p1 = [2,2,2]/6 ; p2 = [1,3,2]/6 ; pe = (2*1 + 2*3 + 2*2)/36 = 12/36 = 1/3
    #    kappa = (5/6 - 1/3)/(1 - 1/3) = 0.75
    a = ["0", "0", "1", "1", "2", "2"]
    b = ["0", "1", "1", "1", "2", "2"]
    assert abs(cohen_kappa(a, b, ["0", "1", "2"]) - 0.75) < 1e-12, "hand-computed kappa mismatch"
    # 3. cross-check with scikit-learn if available
    try:
        from sklearn.metrics import cohen_kappa_score
        rng = np.random.default_rng(7)
        for trial in range(5):
            a = rng.choice(["0", "1", "2", "NR"], size=40, p=[0.4, 0.3, 0.2, 0.1]).tolist()
            b = rng.choice(["0", "1", "2", "NR"], size=40, p=[0.4, 0.3, 0.2, 0.1]).tolist()
            cats = ["0", "1", "2", "NR"]
            mine = cohen_kappa(a, b, cats)
            ref = cohen_kappa_score(a, b, labels=cats)
            assert abs(mine - ref) < 1e-12, f"sklearn mismatch: {mine} vs {ref}"
        print("sklearn cross-check: 5/5 OK")
    except ImportError:
        print("sklearn not available; skipped cross-check")
    # 4. weighted kappa: perfect -> 1; known example
    k, nu, nex = weighted_kappa(["0", "1", "2"], ["0", "1", "2"], ["2", "1", "0"], "linear")
    assert abs(k - 1.0) < 1e-12 and nex == 0
    # hand example: a=[0,1,2], b=[1,1,2], linear weights over {0,1,2}
    k, _, _ = weighted_kappa(["0", "1", "2"], ["1", "1", "2"], ["2", "1", "0"], "linear")
    # po = (0.5+1+1)/3 = 2.5/3 ; pe = sum p1*p2*w
    p1 = [1 / 3, 1 / 3, 1 / 3]; p2 = [0, 2 / 3, 1 / 3]
    w = [[1, .5, 0], [.5, 1, .5], [0, .5, 1]]
    pe = sum(p1[i] * p2[j] * w[i][j] for i in range(3) for j in range(3))
    po = (0.5 + 1 + 1) / 3
    assert abs(k - (po - pe) / (1 - pe)) < 1e-12, "weighted kappa hand-check failed"
    # 5. NR excluded from weighted but not unweighted
    k, nu, nex = weighted_kappa(["0", "NR", "2"], ["0", "1", "NR"], ["2", "1", "0"], "linear")
    assert nu == 1 and nex == 2
    # 6. Fleiss known example (3 raters, 2 items) vs published formula
    fl = fleiss_kappa([["0", "0", "1"], ["1", "1", "1"]])
    # P1 = (2*1 + 1*0)/(3*2) = 1/3 ; P2 = 1 ; Pbar = 2/3 ; pe = ((4/6)^2+(2/6)^2)=5/9
    # k = (2/3 - 5/9)/(1 - 5/9) = (1/9)/(4/9) = 0.25
    assert abs(fl - 0.25) < 1e-12, f"Fleiss hand-check failed: {fl}"
    # 7. collapse rule: 1/0 confusions dominate (categories in declared order 2,1,0)
    a = ["0", "0", "0", "1", "2", "2"]
    b = ["1", "0", "1", "1", "2", "2"]
    pair, share = collapse_check(a, b, ["2", "1", "0"])
    assert pair == ("1", "0") and abs(share - 1.0) < 1e-12, f"collapse check failed: {pair} {share}"
    # 8. PABAK
    assert abs(pabak(0.8, 2) - 0.6) < 1e-12
    assert abs(pabak(0.9, 4) - (4 * 0.9 - 1) / 3) < 1e-12
    # 9. bootstrap runs and brackets
    rng = np.random.default_rng(3)
    a = rng.choice(["0", "1", "2"], size=60).tolist()
    b = [x if rng.random() < 0.8 else rng.choice(["0", "1", "2"]) for x in a]
    lo, hi = bootstrap_ci(cohen_kappa, a, b, 500, 11, categories=["0", "1", "2"])
    assert lo is not None and lo <= hi
    print("ALL SELF-TESTS PASSED")


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--workbook")
    ap.add_argument("--sheet1", default="Coder1")
    ap.add_argument("--sheet2", default="Coder2")
    ap.add_argument("--fleiss", help="optional third sheet for Fleiss kappa (e.g. Coder3)")
    ap.add_argument("--csv1"); ap.add_argument("--csv2")
    ap.add_argument("--out", default="kappa_output")
    ap.add_argument("--bootstrap", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--heatmap", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        selftest()
        return
    if not ((args.workbook or (args.csv1 and args.csv2))):
        ap.error("provide --workbook or both --csv1 and --csv2 (or --selftest)")

    if args.workbook:
        d1 = read_workbook(args.workbook, args.sheet1)
        d2 = read_workbook(args.workbook, args.sheet2)
        d3 = read_workbook(args.workbook, args.fleiss) if args.fleiss else None
    else:
        d1 = read_csv(args.csv1); d2 = read_csv(args.csv2); d3 = read_csv(args.fleiss) if args.fleiss else None

    common, only1, only2 = align(d1, d2)
    if not common and not only1 and not only2:
        sys.exit("error: no coded studies found — are the sheets filled in?")
    if only1 or only2:
        print(f"warning: {len(only1)} studies only in sheet1, {len(only2)} only in sheet2 "
              f"(excluded pairwise per variable)")
    if d3 is not None:
        common3 = [s for s in common if s in d3]
        ratings = []
        for s in common3:
            for vid in VAR_IDS:
                trip = [d1[s].get(vid), d2[s].get(vid), d3[s].get(vid)]
                if all(trip):
                    ratings.append(trip)
        fl = fleiss_kappa(ratings) if ratings else None
        print(f"Fleiss kappa (3 raters, {len(ratings)} coded variable-studies): "
              f"{fl:.3f}" if fl is not None else "Fleiss: no fully-coded triples found")
    else:
        fl = None

    os.makedirs(args.out, exist_ok=True)
    rows, notes, _ = analyse(d1, d2, args.bootstrap, args.seed, args.out, args.heatmap)
    write_report(rows, notes, args.out, args.bootstrap, fl)
    # console summary
    print(f"\n{'Var':5} {'N':>4} {'kappa':>7} {'PABAK':>7}  gate")
    for r in rows:
        if r.get("n", 0) == 0:
            print(f"{r['var']:5} {0:>4}  awaiting codes")
            continue
        gate = "PASS" if r["kappa"] >= GATE else ("below gate" if r["kappa"] < GATE else "")
        print(f"{r['var']:5} {r['n']:>4} {r['kappa']:>7.2f} {r['pabak']:>7.2f}  {gate}")


if __name__ == "__main__":
    main()
