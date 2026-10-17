#!/usr/bin/env python3
"""Minimum-detectable-effect (MDE) analysis for the physics-informed vs other
validation-stringency contrast (reviewer round-3, M4).

Facts being qualified (Section 3.4): strong protocol 8/22 physics-informed vs
34/66 others, Fisher exact two-sided p = 0.32, OR 0.54 (95% CI 0.21-1.46);
broad definition 13/22 vs 49/66, p = 0.19.

Question answered: with 22 vs 66 papers and a two-sided test at alpha = 0.05,
what true difference in strong-protocol share would be detected with 80% power?

Method: analytic power of the two-proportion z-test (unpooled-variance form,
which closely tracks the Fisher exact test at these margins), scanned over the
alternative; the analytic curve is validated against a 4,000-draw Monte Carlo of
the actual Fisher exact test at the observed and MDE points.
"""
import json, math, os

import numpy as np
from scipy.stats import fisher_exact, norm

RNG = np.random.default_rng(7)
ALPHA = 0.05
Z = norm.ppf(1 - ALPHA / 2)


def power_z(p1, p2, n1, n2):
    """Analytic power of the two-sided two-proportion z test (unpooled SE)."""
    se = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    if se == 0:
        return 1.0
    d = abs(p1 - p2)
    return float(norm.cdf(d / se - Z) + norm.cdf(-d / se - Z))


def power_fisher_mc(p1, p2, n1, n2, nsim=4000):
    """Monte Carlo power of the two-sided Fisher exact test (validation)."""
    k1 = RNG.binomial(n1, p1, size=nsim)
    k2 = RNG.binomial(n2, p2, size=nsim)
    rej = 0
    for a, c in zip(k1, k2):
        if fisher_exact([[a, n1 - a], [c, n2 - c]])[1] < ALPHA:
            rej += 1
    return rej / nsim


def mde(p_base, n_small, n_big):
    """Smallest |p_small - p_base| with analytic power >= 0.8, both directions."""
    out = {}
    for direction in ('lower', 'upper'):
        grid = np.arange(0.02, 0.981, 0.005)
        cand = [p for p in grid if (p < p_base - 0.001 if direction == 'lower'
                                    else p > p_base + 0.001)]
        cand.sort(key=lambda x: abs(x - p_base))
        hit = None
        for p1 in cand:
            if power_z(p1, p_base, n_small, n_big) >= 0.8:
                hit = p1
                break
        out[direction] = hit
    return out


def or_of(p1, p2):
    return (p1 / (1 - p1)) / (p2 / (1 - p2))


def wilson(k, n, z=1.959964):
    ph = k / n
    d = 1 + z * z / n
    c = (ph + z * z / (2 * n)) / d
    h = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / d
    return round(100 * (c - h), 1), round(100 * (c + h), 1)


def main():
    out = {'alpha_two_sided': ALPHA, 'method': (
        'analytic two-proportion z-test power (validated against 4,000-draw '
        'Fisher-exact Monte Carlo at the reported points)'), 'contrasts': {}}

    for name, (k1, n1, k2, n2) in {
        'protocol_only': (8, 22, 34, 66),
        'broad': (13, 22, 49, 66),
    }.items():
        p1, p2 = k1 / n1, k2 / n2
        m = mde(p2, n1, n2)
        entry = {
            'observed': {'strong_physics': k1, 'n_physics': n1, 'strong_other': k2, 'n_other': n2,
                         'p_physics': round(p1, 4), 'p_other': round(p2, 4),
                         'diff_pp': round(100 * (p1 - p2), 1)},
            'analytic_power_at_observed_difference': round(power_z(p1, p2, n1, n2), 3),
        }
        for direction in ('lower', 'upper'):
            pp = m[direction]
            entry[f'mde_{direction}'] = None if pp is None else {
                'p_physics': round(pp, 3), 'diff_pp': round(100 * (pp - p2), 1),
                'odds_ratio': round(or_of(pp, p2), 2),
                'analytic_power': round(power_z(pp, p2, n1, n2), 3)}
        # validation of the analytic curve at the observed point and both MDE points
        entry['fisher_mc_power_at_observed'] = round(power_fisher_mc(p1, p2, n1, n2), 3)
        for direction in ('lower', 'upper'):
            pp = m[direction]
            if pp is not None:
                entry[f'fisher_mc_power_at_mde_{direction}'] = round(
                    power_fisher_mc(pp, p2, n1, n2), 3)
        out['contrasts'][name] = entry

    out['wilson_cis'] = {
        'physics_strong_8_of_22': wilson(8, 22),
        'other_strong_34_of_66': wilson(34, 66),
        'overall_strong_42_of_88': wilson(42, 88),
        'online_8_of_88': wilson(8, 88),
    }

    here = os.path.dirname(os.path.abspath(__file__))
    json.dump(out, open(os.path.join(here, 'power_analysis.json'), 'w'), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
