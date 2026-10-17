#!/usr/bin/env python3
"""Condensed TTE-submission text (12-page limit): part 2."""

BLOCKS = [
('h1', '3. Corpus Overview and Five-Year Evolution'),

('h2', '3.1 Publication trend and method-family evolution'),
('p',
 "Two layers of trend evidence are reported. On the *measured* tier (eligible corpus, 799 records), the capped retrieval captures 55, 85, 139, and "
 "223 journal articles for 2020\u20132023, 56 for 2024 \u2014 an observed count inside the capped retrieval, not an estimate of missing volume; the January\u2013May 2024 window is only partially covered (Section II-A) \u2014 then 126 in 2025 and \u2014 partial "
 "year, retrieval date September 2026 \u2014 114 in 2026, plus one further early-access record date-stamped 2027 by Crossref metadata and omitted "
 "from the year chart (Fig. 3, left panel). These are counts within a capped retrieval, not census totals, and "
 "they do not support absolute-growth claims (``the literature quadrupled'' would require an uncapped retrieval). A per-year external denominator "
 "was tested and discarded: Crossref's reported result totals for the same 30 queries (a published script and its output ship with the deposit) "
 "rely on a loose token-level bibliographic match whose totals run into the hundreds of thousands and vary strongly with query phrasing, so they "
 "are not interpretable as field denominators. What remains defensible is direction within the sample: the eligible-corpus counts rise through "
 "2020\u20132023, dip at the retrieval hole, and remain high in 2025\u20132026, and the tagged composition of those records shifts toward estimation "
 "and hybrid methods (next paragraph)." ),
('p',
 "On the *classified subset*, the defining finding is the compositional shift in method families (Fig. 3, right panel; Table I). Classical "
 "ML \u2014 Gaussian process regression, support vector machines, ensembles, shallow networks on engineered features \u2014 contributes 12 of the 23 "
 "subset papers published from 2019 through 2021, while physics-informed and hybrid model\u2013data learning rises year by year (1, 2, 3, 3, 4, 4, and 5 "
 "primary papers in 2020\u20132026) \u2014 the only family with a monotonically non-decreasing trajectory within the subset \u2014 so that 13 of its 22 primary papers "
 "fall in 2024\u20132026 and it is the largest single family in 2026 (Table II gives the subset totals by year). Optimization-"
 "augmented learning (Bayesian optimization, surrogate-assisted and meta-heuristic schemes) peaks in 2024 (5 of its 11 papers); transfer learning "
 "accelerates in 2024\u20132025 (3 of its 5 papers); reinforcement learning appears as the dominant family in 1 paper and as an embedded component in at least "
 "one more [[10.1016/j.ress.2025.111392]][[10.1038/s41598-025-30602-4]]; the subset\u2019s first foundation-model and LLM-based studies appear in 2025\u20132026 "
 "(2 papers) [[10.1016/j.ress.2026.112416]][[10.1016/j.ensm.2026.104983]], with journal-published LLM-based battery estimation beginning "
 "earlier still, as a retrieval miss rather than a venue exclusion [[10.1109/tec.2025.3548400]]. These family shares describe the subset "
 "only; the subset is curated, small-denominator years carry wide sampling error, and the eligible pool's method-theme tags show no "
 "monotonic physics-informed trend. Two qualifications matter: the families are not mutually exclusive (a PSO-tuned LSTM is both deep learning and optimization-"
 "augmented), so the composition understates method mixing; and physics-informed papers are, on average, validated no more stringently than others "
 "even under the most permissive definition of stringency \u2014 a point quantified, with its sensitivity ranges, in Section III-C."),

('fig', 'figures/fig3_method_evolution.png', 'Fig. 3 Two-tier trend evidence. Left: Tier 1 eligible-corpus records per year across the capped retrieval '
 '(the 2024 dip is the documented January\u2013May 2024 retrieval hole, not a decline in the field; one further record is date-stamped 2027 by '
 'Crossref and not shown). Right: Tier 2 classified-subset papers by year and method family, with reviews shown as their own band; the yearly '
 'totals match Table II, and the three review-type syntheses sit inside their dominant family bands (two of them physics-informed), so the '
 'physics-informed band exceeds the primary-only trajectory stated in the text (curated subset; wide sampling error in small years).'),

('tbl', 'TABLE_METH'),

('h2', '3.2 Measured application areas, the transportation-electrification cut, and venues'),
('p',
 "Because function tags were applied mechanically to all 799 eligible records, the application-area distribution is *measured* rather than quoted "
 "from a curated sample. Tags are inherited from the retrieving queries (a record carries every area whose query returned it); 597 records "
 "(75%) carry at least one management-function tag, while the remaining 202 are method-, second-life-, digital-twin-, benchmark-level, or "
 "unmapped records without a specific BMS function, and the tags match the subset's full-text function labels for 53 of the 75 core-area "
 "papers found in the pool (71%, any-tag match \u2014 a lenient criterion, so shares are read for ordering, not for exact rates). Of all eligible records, health estimation (SOH) leads at 20% (158 records; 27% of those function-tagged), followed by state estimation "
 "(SOC) at 17% (133), prognostics (RUL) at 13% (103), thermal management at 12% (99), fault and safety at 12% (96), charging control at 8% (64), and "
 "cell balancing at 5% (38). These per-tag percentages must not be summed \u2014 a record can carry several tags; the union of SOC, SOH, and RUL "
 "covers 46% of eligible records, and adding the four control-and-safety functions brings management-function coverage to 75%. The estimation "
 "concentration is a measured pattern consistent with the commercial pull of lifetime prediction for warranties and second-life markets, and is "
 "mirrored (with a heavier cross-cutting share) in the classified subset (Fig. 1; Table II gives subset composition by year; Table IV maps "
 "representative studies). Two measured concentrations matter specifically for transportation electrification. First, the electrification cut: only \u22482% "
 "of eligible records (n = 17) are tagged fleet- or cloud-orchestration-adjacent, and in the "
 "classified subset only 10 of 88 primary papers use real vehicle or fleet data as their primary source against 36 resting on laboratory cells \u2014 "
 "the classified literature is predominantly cell-level and laboratory-scale, one integration level below the pack- and vehicle-level questions that "
 "UN GTR 20, GB 38031, and ISO 26262 pose. Second, venue concentration is marked: in the eligible corpus the Journal of Energy Storage (103 records), "
 "Energy (61), and Batteries (45) lead, and the same two energy-storage journals head the classified subset (Journal of Energy Storage with 15 papers and Energy with 13, Applied Energy "
 "third at 9) \u2014 energy-storage venues, not transportation-electrification venues, absorb the field's output. The thin representation of cell "
 "balancing is also telling: balancing remains dominated by classical control practice, and the subset's most-cited balancing-related result is the "
 "demonstration that routine balancing can be dispensed with in well-managed packs, reducing hazardous lithium-plating side reactions "
 "[[10.1016/j.est.2023.106931]]."),

('tbl', 'TABLE2'),

('h2', '3.3 Data landscape and validation practice'),
('p',
 "The data underpinning the classified subset are strikingly concentrated: 36 of the 88 primary-application papers rest on laboratory cycling of "
 "the authors' own cells; the public Severson/Toyota\u2013MIT\u2013Stanford (MATR) dataset alone supports 11, NASA and CALCE 6 each, and laboratory "
 "impedance spectroscopy 6; 12 are simulation-based. Only 10 papers use real vehicle or fleet data as their primary source, and *data use* is a "
 "distinct measure from *validation protocol*: 8 of the 10 fleet-data papers are validated online or on real vehicles, and the other two through "
 "cross-domain holdout or case-study protocols (Table III). Validation practice is arguably the classified subset's most consequential weakness, and "
 "it is now defined and audited explicitly. Per the definitions of Section II-C, cross-cell holdout \u2014 the strongest common laboratory protocol "
 "\u2014 accounts for 24 primary-application papers, cross-chemistry holdout for 7, cross-domain holdout for 3, and online or fleet validation for "
 "8; together these *strong protocols* cover 42 of the 88 primary-application papers (48%). Within-cell splits (12 papers) and unsupervised k-fold "
 "cross-validation (5) leak trajectory information between train and test, producing optimistic errors that do not survive cell-to-cell variability; "
 "the remaining 29 studies establish hardware operation (20), simulation- or case-level evidence without a generalization protocol (9) \u2014 "
 "42+17+29 = 88. The complete per-paper protocol assignment is released in papers.csv (valid field) and tabulated as a supplement "
 "(protocol_audit.csv), so the 42-of-88 arithmetic above can be verified row by row, and the 30-paper blind re-coding of Section II-C re-derived 25 of these "
 "primary-paper assignments (plus 5 review-labelled papers) independently."),
('p',
 "Crossing validation practice with method family, the cautious reading is: 8 of the 22 physics-informed/hybrid primary papers (36%) use a strong "
 "protocol, against 34 of the 66 other primary papers (52%) \u2014 Fisher's exact p = 0.32, odds ratio 0.54 (95% CI 0.21\u20131.46). Under the "
 "earlier, broader definition that also counted experimental-hardware demonstration as strong validation, the contrast is 13 of 22 (59%) versus "
 "49 of 66 (74%), OR 0.50 (95% CI 0.19\u20131.36, p = 0.19). We report both and claim neither as a model-family effect: the difference is not "
 "statistically significant under either definition, confounding is unadjusted (physics-informed work skews toward early-stage and simulation-heavy "
 "studies), and n = 22 is small. A minimum-detectable-effect analysis (released with the corpus) shows that 80% power at \u03b1 = 0.05 would require a gap of roughly 30\u201335 percentage points between the two families, while the observed 15-point gap is detectable with only about 20\u201325% power \u2014 so no detected difference does not mean no difference: meaningful effects in either direction remain compatible with these counts. A label-noise scenario envelope built from the observed blind coder-versus-label disagreement (Section II-C) "
 "moves the overall strong-protocol share across 35\u201352 of the 88 papers (40\u201359% of the primary papers) under symmetric random flipping and "
 "leaves the method-family contrast non-significant in 94% of scenario draws; because the observed disagreements are directional (16 of 19 "
 "have the coder defaulting to weak), a strong-to-weak-only scenario spans 22\u201335 papers (25\u201340%) with the contrast non-significant in 96% "
 "of draws, so the subset's qualitative conclusions survive plausible coding error in either direction. The noise model is explicit and released "
 "(sensitivity_label_noise.py): in each of 4,000 seeded Monte Carlo draws, a strong/non-strong label-flip rate is drawn from a Normal "
 "distribution centered on the observed coder-versus-label bucket error rate (0.37 and 0.27 for the two coders; mean 0.32) with standard "
 "deviation 0.02, truncated at zero, and the drawn rate then flips bucket labels across the 88 primary papers before both the "
 "overall share and the Fisher test are recomputed. The honest reading remains: a physics "
 "prior does not *demonstrably* buy validation rigor \u2014 and settling the question requires the standardized protocols proposed in Section IX, "
 "not more subset cross-tabs."),

('tbl', 'TABLE_FLEET'),

('p',
 "The data concentration can be stated as a two-pole fragmentation metric (Fig. 4). Across 2019\u20132026, 23 primary papers \u2014 26% of the "
 "88 primary-application papers \u2014 rest on the same three public benchmarks (Severson/MATR, NASA, CALCE), whose combined cell count is on the order of a few hundred; "
 "meanwhile, the single largest source overall is private laboratory cycling (36 papers) whose data are rarely released. The empirical base is "
 "therefore not one benchmark monoculture but two poles: a small set of shared benchmarks onto which comparative claims crowd, and many unshared "
 "laboratory datasets over which accuracy claims cannot be audited at all. On the shared benchmarks, dataset-specific failure modes and implicit "
 "test-set familiarity inflate apparent comparability; on the private datasets, reproducibility is unavailable in principle. Both faces of this "
 "pattern \u2014 a small, slowly broadening empirical base under a multiplying literature, and unauditable private data beside it \u2014 make "
 "two-pole data fragmentation the most reproducibility-relevant feature of the classified subset's data landscape; benchmark reuse itself is "
 "erratic year to year (1\u20137 papers) rather than tracking output, so no saturation trend is claimed."),
('fig', 'figures/fig7_dataset_saturation.png', 'Fig. 4 Benchmark reuse versus classified-subset output. Papers in the classified subset using the three '
 'dominant public benchmarks per year (stacked bars) against classified-subset papers per year (line). Both quantities describe the curated 103-study '
 'subset, not the eligible corpus.'),

('h1', '4. Machine Learning for Battery State Estimation'),
('p',
 "SOC estimation is the most mature BMS function, and the classified subset shows how machine learning entered it. The early pattern pairs learning with "
 "classical estimation: Gaussian process regression for pack-level SOC with native uncertainty quantification [[10.1016/j.energy.2020.118000]], and "
 "\u2014 most influentially \u2014 recurrent networks embedded in unscented Kalman filters, where the LSTM supplies a learned observation model and "
 "the filter recursive correction [[10.1016/j.energy.2020.117664]]. A second generation tuned network structure itself: particle-swarm-optimized LSTM "
 "improved accuracy and noise robustness [[10.1016/j.energy.2021.121236]], and evolutionary-assisted CNN\u2013BiLSTM hybrids report sub-1% drive-cycle "
 "errors [[10.1016/j.heliyon.2024.e35183]]. Simulation-informed training pipelines substitute automotive-accurate simulated data for exhaustive cell "
 "testing [[10.1016/j.jpowsour.2020.229108]], comparative benchmarks on standard drive cycles weigh ML regression families [[10.3390/wevj12010038]], "
 "pack heterogeneity is surveyed in a joint review of pack-SOC, cell-inconsistency, and balancing estimation "
 "[[10.1109/access.2021.3068776]], unified frameworks estimate SOH and SOC jointly from partial charging data [[10.1016/j.ensm.2022.06.053]], "
 "large-format applications extend estimation to containerized storage strings [[10.1016/j.jpowsour.2024.235609]], and a review of cutting-edge "
 "SOC algorithms weighs accuracy against embedded compute budgets [[10.1016/j.est.2024.114281]] alongside primary comparative benchmarks "
 "[[10.1016/j.est.2024.111877]]."),
('p',
 "The most substantive recent shift is toward hybrid schemes in which a filter, an equivalent-circuit model, or a physics prior constrains the "
 "learner: GA-optimized LSTM coupled with improved adaptive Kalman filtering reaches low error under measurement noise that breaks pure-network "
 "estimators [[10.1016/j.apenergy.2024.123508]]; equivalent-circuit-informed ML on impedance features estimates SOC across temperatures "
 "[[10.1016/j.energy.2023.128461]]; and physics-informed recurrent structures embed battery dynamics directly into the training objective "
 "[[10.1109/jrfid.2022.3211841]]. These schemes trade engineering complexity for extrapolation behavior \u2014 the property that matters most onboard. "
 "Yet 11 of the 13 subset SOC primary papers rest on the authors' own laboratory cells and one on laboratory impedance measurements, 9 of the 13 on a "
 "single cathode chemistry (NMC), and the thirteenth \u2014 the cluster's only operation-scale demonstration, a simulated stationary containerized "
 "storage system rather than a vehicle \u2014 is [[10.1016/j.jpowsour.2024.235609]]; benchmark heterogeneity makes cross-paper comparison nearly "
 "meaningless "
 "[[10.1016/j.egyai.2025.100585]][[10.20517/jmi.2024.84]]. Within the subset's own reporting, accuracy on laboratory cells no longer appears to be the binding constraint in this cluster; "
 "guaranteed accuracy on arbitrary packs over full cell aging, which the onboard estimator would need, is not demonstrated anywhere in the subset."),

('h1', '5. Machine Learning for Health Estimation and Prognostics'),
('p',
 "SOH estimation and RUL prediction form the largest functional block of the classified subset (32 primary papers: 19 SOH, 13 RUL). The founding pattern is "
 "classical: extract health-sensitive features from partial charge or discharge curves, then regress with Gaussian process or similar shallow models "
 "\u2014 incremental-capacity analysis with explicit uncertainty bounds [[10.1016/j.energy.2019.116467]], differential thermal voltammetry "
 "[[10.1109/tte.2020.3028784]], and Gaussian-process classification of impedance spectra that identifies degradation modes "
 "[[10.1038/s41467-020-15235-7]], and deep Gaussian processes coupling prognosis with degradation-mode identification "
 "[[10.1016/j.jpowsour.2019.227281]]. Measurement relaxations followed: random partial charging data proved sufficient for accurate SOH "
 "[[10.1109/tpel.2021.3134701]], and charging-segment adjustment refined features for vehicle-level use [[10.1016/j.apenergy.2024.124077]]. The "
 "landmark systematization is Roman et al.'s 179-cell pipeline showing that relaxed charge-curve features support accurate SOH estimation across a "
 "heterogeneous commercial fleet [[10.1038/s42256-021-00312-3]]."),
('p',
 "Deep architectures entered as sequence models over capacity-fade trajectories and representation learners over raw curves: graph convolutional "
 "networks fusing multiple health indicators [[10.1016/j.ress.2022.108947]], graph networks over partial discharge curves "
 "[[10.1016/j.est.2024.113502]], BiLSTM\u2013Transformer hybrids under fast-charging stress [[10.1016/j.energy.2024.133418]], hybrid-fusion networks "
 "for real-time prediction streams [[10.1016/j.energy.2025.136618]], and interpretable deep learning with transparency mechanisms "
 "[[10.1016/j.apenergy.2024.124713]]. Field-data studies absorb real-vehicle noise [[10.1016/j.energy.2023.126855]] and estimate pack-level SOH from "
 "fleet streams [[10.1016/j.geits.2024.100169]], while deep models estimate SOH without additional degradation experiments by learning trajectory "
 "features that generalize across chemistries [[10.1038/s41467-023-38458-w]]. Early-life prediction \u2014 forecasting lifetime from the first cycles "
 "\u2014 compresses test times from months to days [[10.1038/s41560-019-0356-8]][[10.1016/j.apenergy.2021.116897]][[10.1016/j.energy.2021.120205]], "
 "hybrid physics-plus-learned models give early RUL from limited cycles [[10.1016/j.jclepro.2021.128265]], the approach extends to lithium-metal "
 "chemistries [[10.1002/advs.202402608]], and it now runs on embedded boards in real time [[10.1016/j.est.2022.104901]]."),
('p',
 "The prognostics cluster shows the clearest physics-informed turn: physics-informed online degradation models [[10.1016/j.ymssp.2022.109347]], hybrid "
 "reinforcement learning that reduces the data demand of SOH estimation [[10.1038/s41598-025-30602-4]], a generalizable PINN from limited early-cycle "
 "data [[10.1016/j.jechem.2025.08.093]], EIS-informed physics-constrained networks [[10.1016/j.energy.2025.139753]], a generic physics-informed RUL "
 "framework for small early-life samples [[10.1016/j.apenergy.2025.125314]], multi-feature hybrids across datasets [[10.1016/j.est.2025.118415]], "
 "recurrent networks anticipating uncertain duty [[10.1016/j.ensm.2022.05.007]], and signal-decomposition hybrids on noisy capacity series "
 "[[10.1038/s41598-025-92262-8]]. Transfer learning attacks generalization directly: domain-adversarial training across operating conditions "
 "[[10.1109/tpel.2021.3117788]], deep transfer with partial charging curves across cell types [[10.1016/j.energy.2023.127033]], transfer under fast-"
 "charging protocols [[10.1016/j.isci.2025.112235]], cross-chemistry EIS estimation [[10.1109/tte.2025.3533540]], and a general framework quantifying "
 "the laboratory-to-fleet domain gap [[10.1016/j.apenergy.2024.125086]]. The critical assessment: the cluster's accuracy claims are established overwhelmingly on public benchmark cells \u2014 10 of the 32 primary "
 "studies in this complex use within-cell or k-fold validation (17 of the 88 primary papers in total) \u2014 and the transfer-learning papers, the "
 "honest exception, reveal how much shift remains unaddressed. SOH estimation under "
 "controlled conditions shows signs of approaching incremental returns within this subset; calibrated lifetime and safety margins for arbitrary packs in the field remain open "
 "[[10.1016/j.joule.2019.11.018]][[10.1016/j.jechem.2023.03.026]]."),

('tbl', 'TABLE_REP'),

('h1', '6. Machine Learning for Charging Control and Optimization'),
('p',
 "Charging control is the function where machine learning has changed experimental practice most directly. The defining result is Attia et al.: a "
 "Bayesian optimization loop identified high-cycle-life protocols among 224 candidates in 16 days of closed-loop cycling, against more than 500 days "
 "for an exhaustive search without early prediction [[10.1038/s41586-020-1994-5]]. Ensemble surrogates make multi-objective strategy optimization "
 "tractable [[10.1016/j.enconman.2025.120170]], and Bayesian fast-charging optimization reduces charge time under degradation constraints "
 "[[10.1109/tte.2023.3311813]]. A second line embeds degradation mechanisms into the decision itself: machine-learning fast charging that perceives "
 "and regulates internal lithium-plating onset enables plating-free rapid protocols [[10.1016/j.ensm.2022.12.034]], adaptive multistage schemes "
 "adjust stage boundaries against measured degradation [[10.1016/j.renene.2019.08.077]], module-level optimization manages temperature gradients "
 "[[10.1016/j.energy.2022.126331]], and pack-level extensions coordinate balance-aware charging "
 "[[10.1016/j.est.2024.111755]][[10.1016/j.est.2024.112046]]."),
('p',
 "The deployment gap is most concrete here: of the eight charging papers, four demonstrate on laboratory hardware \u2014 including the 224-cell "
 "closed-loop campaign above \u2014 and the remaining four rest on simulation-level evidence (three simulation-only, one with hardware spot-checks). "
 "No subset charging paper demonstrates a learned strategy validated online on a vehicle. The unsolved problem is certifiable learning-based "
 "charging \u2014 which is why mechanism-aware schemes such as plating-perception control [[10.1016/j.ensm.2022.12.034]] are the cluster's most "
 "deployment-relevant results."),

('h1', '7. Machine Learning for Thermal Management, Faults and Safety'),
('p',
 "Thermal management (7 primary papers) divides by purpose. For estimation, ANN models predict cell temperature across operating conditions "
 "[[10.1016/j.applthermaleng.2023.120482]] and internal-temperature sensing extends to ultrahigh-rate discharge where surface measurement fails "
 "[[10.1016/j.apenergy.2026.127394]]. For design, ML surrogates amortize expensive CFD evaluation across optimization loops "
 "[[10.1016/j.jpowsour.2021.229727]][[10.1016/j.applthermaleng.2024.123826]], with experimentally validated parallel-liquid-cooling designs closing "
 "the loop [[10.1016/j.applthermaleng.2022.118503]]. For control, ANN controllers demonstrate parasitic-load reductions in simulation "
 "[[10.3390/wevj16050279]] \u2014 but no subset paper closes this loop on hardware, leaving thermal control where charging control was five years ago. "
 "Physics-informed heat-generation estimation embeds thermal priors into the learning problem [[10.1016/j.jechem.2022.11.036]], and the cluster is "
 "consolidated by a state-of-the-art review [[10.1016/j.est.2023.106688]]."),
('p',
 "Fault and safety applications (7 primary papers) divide into diagnosis of realized faults and prediction of impending hazards: grid-search-optimized SVMs "
 "classify sensor and connection faults [[10.1016/j.energy.2020.118866]], curvilinear-distance methods detect multiple pack fault types in operating "
 "fleets [[10.1016/j.est.2023.107575]], and multi-scenario deep anomaly detection covers real EV operating envelopes [[10.1016/j.etran.2025.100418]]; "
 "force-signal deep learning catches lithium-plating-type defects at manufacturing [[10.1016/j.jechem.2025.04.025]]. The hazard-prediction side is "
 "increasingly model-based: multiphysics models coupled with ML predict module-level thermal-runaway progression [[10.1016/j.jpowsour.2024.235015]], a "
 "multiphysics-informed DeepONet augments scarce experimental events with virtual data [[10.1016/j.etran.2024.100337]], and multi-source domain "
 "transfer moves thermal-runaway diagnosis across fleets with small target samples [[10.1016/j.apenergy.2024.123248]]. The reviews in this cluster are "
 "candid that laboratory fault diagnosis has historically failed to transfer to real vehicles "
 "[[10.1016/j.etran.2023.100254]][[10.3390/electronics10111309]]; the fleet-data anomaly-detection studies are therefore the cluster's most valuable "
 "trend, even though label scarcity for rare faults keeps evaluation largely qualitative."),

]
