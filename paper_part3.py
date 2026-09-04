#!/usr/bin/env python3
"""Paper text part 3: Sections 7-10, declarations, and table data."""

BLOCKS = [
('h1', '7. Machine Learning for Thermal Management, Faults and Safety'),

('h2', '7.1 Thermal-state estimation and thermal management'),
('p',
 "Thermal management is the corpus\u2019s smallest quantitative engineering cluster (8 papers) but a disproportionately safety-critical one. Data-driven temperature estimation ranges from ANN models predicting cell temperature across operating conditions [[10.1016/j.applthermaleng.2023.120482]] to internal-temperature sensing under ultrahigh-rate discharge, where surface measurement fails [[10.1016/j.apenergy.2026.127394]]. On the design and control side, ML-surrogate models accelerate liquid-cooling plate analysis and multi-objective optimization of BTMS geometry [[10.1016/j.jpowsour.2021.229727]][[10.1016/j.applthermaleng.2024.123826]], experimentally validated parallel-liquid-cooling designs demonstrate the optimization loop end-to-end [[10.1016/j.applthermaleng.2022.118503]], and ANN-controlled thermal management reduces cooling parasitic load while holding temperature limits [[10.3390/wevj16050279]]. Physics-informed heat-generation estimation embeds thermal physics priors into the learning problem [[10.1016/j.jechem.2022.11.036]], and a state-of-the-art review consolidates the cluster [[10.1016/j.est.2023.106688]]."),

('p',
 "The thermal cluster\u2019s papers divide cleanly by purpose, and the division clarifies where machine learning adds value. For *estimation* purposes \u2014 predicting internal or surface temperature under load \u2014 learned models replace thermocouple instrumentation that no production pack can afford, and physics-informed variants regularize the extrapolation regime where data-driven thermal models are least trustworthy [[10.1016/j.jechem.2022.11.036]]. For *design* purposes \u2014 sizing and arranging cooling hardware \u2014 ML surrogates amortize expensive CFD evaluation across optimization loops, turning weeks of simulation into tractable search [[10.1016/j.jpowsour.2021.229727]][[10.1016/j.applthermaleng.2024.123826]]. For *control* purposes \u2014 modulating cooling effort online \u2014 ANN controllers demonstrate parasitic-load reductions in simulation [[10.3390/wevj16050279]], but no corpus paper yet closes this loop on hardware, leaving thermal control where charging control was five years ago."),

('h2', '7.2 Fault diagnosis and anomaly detection'),
('p',
 "Fault and safety applications (9 papers) divide into diagnosis of realized faults and prediction of impending hazards. On the diagnosis side, grid-search-optimized support vector machines classify sensor and connection faults [[10.1016/j.energy.2020.118866]], curvilinear-Manhattan-distance methods detect multiple pack fault types in operating fleets [[10.1016/j.est.2023.107575]], and multi-scenario deep anomaly detection covers real EV operating envelopes [[10.1016/j.etran.2025.100418]]. Manufacturing-side inspection applies force-signal deep learning to catch lithium-plating-type defects before cells ship [[10.1016/j.jechem.2025.04.025]]. The hazard-prediction side is increasingly model-based: multiphysics models coupled with ML predict module-level thermal-runaway progression [[10.1016/j.jpowsour.2024.235015]], a multiphysics-informed DeepONet predicts runaway using virtual data to augment scarce experimental events [[10.1016/j.etran.2024.100337]], and multi-source domain transfer moves thermal-runaway diagnosis across vehicle fleets with small target samples [[10.1016/j.apenergy.2024.123248]]."),

('h2', '7.3 Critical assessment'),
('p',
 "Safety applications carry the corpus\u2019s highest stakes and its thinnest evidence base. Thermal-runaway events are rare and expensive to generate, so learning systems train on simulation or small laboratory campaigns; the DeepONet line\u2019s virtual-data approach [[10.1016/j.etran.2024.100337]] is a rational response, but it inherits the fidelity limits of the underlying multiphysics models. The reviews in this cluster are notably candid: laboratory fault diagnosis has historically failed to transfer to real vehicles because fault signatures are masked by pack-level averaging, sensor noise, and operating diversity [[10.1016/j.etran.2023.100254]][[10.3390/electronics10111309]]. The fleet-data anomaly-detection studies are therefore the cluster\u2019s most valuable trend, even though label scarcity for rare faults keeps evaluation largely qualitative."),

('h1', '8. Cross-Cutting Directions'),

('h2', '8.1 Physics-informed learning'),
('p',
 "Physics-informed and hybrid model\u2013data learning is the corpus\u2019s largest and fastest-rising methodological theme (24 papers across all functions). Beyond the prognostics applications of Section 5.4, physics-informed structures appear in state estimation [[10.1109/jrfid.2022.3211841]][[10.1016/j.measurement.2025.118985]], heat-generation estimation [[10.1016/j.jechem.2022.11.036]], and impedance-based diagnostics, where physics-informed deep learning over electrochemical impedance spectra is consolidating into a diagnostic paradigm of its own [[10.1016/j.rser.2023.113807]]. Physics-constrained autoencoders improve health prediction over purely learned counterparts [[10.1007/s00521-022-07291-5]], and recurrent networks trained to anticipate uncertain future duty conditions address degradation prediction under distribution shift directly [[10.1016/j.ensm.2022.05.007]]. A parallel fusion literature combines physical and data-driven models for internal-state estimation generally [[10.3390/batteries10120442]]. The appeal is easy to state: physics priors supply exactly the extrapolation structure that pure learners lack. The corpus\u2019s caution is that most physics-informed studies embed *simplified* physics \u2014 equivalent-circuit or reduced electrochemical models \u2014 so the hybrid inherits model bias even as it gains structure."),

('h2', '8.2 Interpretability and uncertainty'),
('p',
 "A smaller but consequential cluster makes learning systems inspectable. Explainability-driven feature selection improves SOH estimator robustness via SHAP analysis [[10.1016/j.ress.2022.109046]]; interpretable ML links manufacturing coating parameters to cell capacity, connecting management analytics to production [[10.1016/j.conengprac.2022.105202]]; interpretable hybrid ML untangles co-evolving degradation chemistries in lithium\u2013sulfur cells [[10.1002/anie.202214037]]; and uncertainty-aware, explainable models deliver calibrated early-life predictions [[10.1039/d2dd00067a]]. Review-level retrospectives of interpretable battery prognosis now chart the theme\u2019s trajectory [[10.1002/aenm.202503067]]. The state of practice remains, however, dominated by post-hoc explanation of otherwise black-box models \u2014 a necessary but not sufficient condition for the safety certification that onboard ML will eventually require."),

('p',
 "The uncertainty thread deserves separate emphasis because it is the certification-relevant one. Gaussian-process lineages carry calibrated intervals as a first-class output [[10.1016/j.energy.2019.116467]], the uncertainty-aware early-prediction study demonstrates calibrated lifetime distributions rather than point forecasts [[10.1039/d2dd00067a]], and conformal-style guarantees are beginning to appear in adjacent prognostics work. The interpretability thread, by contrast, remains dominated by post-hoc attribution (SHAP-style) analyses that explain *which features mattered* without bounding *what the model will do* on out-of-distribution inputs. For safety cases the two are not substitutes: attribution supports debugging and trust-building, while calibrated uncertainty supports decision rules \u2014 and only the latter has a route into certification argument."),

('h2', '8.3 Digital twins, cloud BMS, and new sensing'),
('p',
 "System-level architecture is emerging as a research object in its own right. Digital-twin implementations track individual battery aging through incremental learning [[10.1016/j.eswa.2023.120444]] and couple LSTM surrogates with real-time thermal observation [[10.1016/j.est.2023.107203]]; cloud-based platforms perform in-situ life prediction and classification at fleet scale from streaming charge data [[10.1016/j.ensm.2023.02.035]]; and second-life workflows use impedance-based accelerated SOH estimation to triage retired packs [[10.1016/j.est.2022.106295]]. Non-electrical sensing broadens the measurement base: ultrasonic signatures processed with ML provide a SOC channel orthogonal to voltage sensing [[10.1016/j.egyai.2022.100188]], impedance-spectroscopy ML supports SOC and SOH estimation despite EIS\u2019s onboard-cost problem [[10.1016/j.energy.2023.128461]][[10.1038/s41467-020-15235-7]], and battery state-of-power estimation combines learned models with numerical search for real-time capability prediction [[10.1016/j.est.2026.123023]]."),

('p',
 "The twin/cloud/second-life cluster carries the corpus\u2019s most concrete systems implications. Digital-twin formulations reframe estimation as continual model maintenance \u2014 the incremental-learning requirement follows from pack heterogeneity and aging drift [[10.1016/j.eswa.2023.120444]] \u2014 and cloud architectures relocate heavy computation off-vehicle, at the price of connectivity dependence and data-volume engineering [[10.1016/j.ensm.2023.02.035]]. Second-life workflows invert the deployment direction: instead of bringing estimators to new cells, they bring cheap, accelerated assessment to aged, heterogeneous cells [[10.1016/j.est.2022.106295]], where classification-style decisions (deploy, repurpose, recycle) tolerate coarser resolution than onboard safety estimation. These three settings differ in latency budgets, error tolerance, and update cadence \u2014 and the corpus suggests the field is beginning to design for those differences rather than for a single notion of \u201cthe BMS.\u201d"),

('h2', '8.4 Foundation models and LLM-based management'),
('p',
 "The corpus\u2019s youngest theme is generative: domain-specific large language models perform risk analysis of battery energy-storage incidents by synthesizing heterogeneous incident reports [[10.1016/j.ress.2026.112416]], and domain-knowledge-enhanced LLM agents orchestrate vehicle-cloud collaborative battery management [[10.1016/j.ensm.2026.104983]]. These first studies position LLMs as reasoning and coordination layers above numerical estimators rather than as estimators themselves \u2014 a sensible division given that hallucination risk is intolerable in safety-critical state estimation. Their appearance in mainstream energy journals in 2025\u20132026 nonetheless marks a new phase: the management stack is beginning to absorb foundation-model components, and the corpus\u2019s method-evolution data (Fig. 4) suggest the field expects this line to grow."),

('p',
 "Because BMS software is safety-critical, this review positions foundation models not as better estimators but as orchestration layers, and it is worth making the division of labor explicit. Table 9 contrasts established practice for classical and deep learning estimators with what the first LLM studies actually demonstrate, and states the guardrails this review regards as mandatory before any LLM component touches a safety-relevant path. The right-hand column is normative guidance proposed here, not claims about the published studies; the published LLM work to date is confined to risk analysis and coordination, which is exactly where it belongs at this stage."),

('tbl', 'TABLE_LLM'),

('h2', '8.5 Manufacturing analytics and system-level synthesis'),
('p',
 "Two further cross-cutting threads connect management to the wider battery value chain. Cell-production mapping studies chart ML use across manufacturing stages from mixing to formation [[10.1002/batt.202300046]], complementing the coating-quality interpretability work [[10.1016/j.conengprac.2022.105202]] and manufacturing defect detection [[10.1016/j.jechem.2025.04.025]] \u2014 the management implication being that cell quality information is itself a BMS input. And the pack-level insight that routine cell balancing can be eliminated in well-managed packs, reducing hazardous lithium-plating side reactions, shows learned analysis reshaping a function (balancing) that classical control had considered settled [[10.1016/j.est.2023.106931]], while ML mappings from equivalent-circuit parameters to electrochemical properties give classical BMS models a physically interpretable learned layer [[10.1016/j.est.2024.113257]]."),

('h1', '9. Research Gaps and Future Directions'),
('p',
 "Cross-referencing the bibliometric analysis of Section 3 with the function-level reviews of Sections 4\u20138 yields six structural gaps, discussed in Sections 9.1\u20139.6, summarized in Table 10, and then operationalized into a concrete reporting checklist in Section 9.7."),

('h2', '9.1 Validation and benchmarking standards'),
('p',
 "The corpus\u2019s validation data are unambiguous: 17 primary studies corpus-wide use within-cell splits or unsupervised k-folds, and only 9 of all 103 papers demonstrate their systems online or on real fleets. Until cross-cell, cross-temperature, and cross-protocol holdout protocols become reporting norms, published accuracy figures will keep overstating deployable performance. The most valuable near-term contribution the community can make is standardized transfer protocols \u2014 train-on-chemistry-A/test-on-chemistry-B, train-on-lab/test-on-fleet \u2014 reported alongside headline accuracy, as already practiced by the transfer-learning and general-framework studies [[10.1016/j.apenergy.2024.125086]][[10.1109/tte.2025.3533540]]."),

('p',
 "A second standardization target is reporting itself. The corpus\u2019s papers rarely disclose split definitions, random seeds, or compute budgets \u2014 omissions that make independent replication laborious and meta-analysis impossible (Section 5.6). A community-endorsed reporting checklist \u2014 dataset identity and version, split protocol, uncertainty quantification, and hardware context \u2014 would cost little and would let the synthesis literature do its job."),

('h2', '9.2 Data sharing and the benchmark monoculture'),
('p',
 "Eleven corpus papers rest on a single public dataset (Severson-MATR), and NASA and CALCE sustain much of the remainder; 35 papers use private laboratory cells whose data are not released. The monoculture inflates apparent comparability and hides dataset-specific failure modes. Federated learning over fleet data, standardized anonymized fleet-data releases, and multi-institution cycling campaigns \u2014 in the spirit of the 179-cell pipeline [[10.1038/s42256-021-00312-3]] \u2014 would diversify the evidence base at modest incremental cost."),

('p',
 "The economics argument strengthens the technical one. A fleet operator\u2019s marginal value from a percentage point of SOH accuracy is measured in warranty provisions and residual-value pricing, which justifies onboard compute budgets that academic prototypes routinely ignore. Quantized and pruned recurrent models, event-driven inference triggered by charge sessions rather than continuous streams, and asymmetric architectures \u2014 lightweight onboard estimators with cloud-side retraining \u2014 are the concrete design patterns emerging from the corpus\u2019s edge-aware minority [[10.1016/j.est.2022.104901]][[10.1016/j.jpowsour.2025.236784]]."),

('h2', '9.3 Edge deployment and onboard constraints'),
('p',
 "Only a handful of corpus works treat onboard compute, memory, or latency as first-class design constraints, notably the board-level RUL implementation [[10.1016/j.est.2022.104901]] and real-time feature-extraction studies [[10.1016/j.jpowsour.2025.236784]]. The gap is widening as models grow: transformer and PINN architectures trained on workstations must eventually run beside BMS microcontrollers. Quantization-aware training, neural architecture search under resource constraints, and hybrid designs that place heavy learners in the cloud and lightweight correction layers onboard are the natural research program here [[10.1016/j.ensm.2026.104983]]."),

('h2', '9.4 Trust: uncertainty, interpretability, and certification'),
('p',
 "Estimates that guide protection and charging decisions need calibrated uncertainty and auditable reasoning. The corpus\u2019s uncertainty-aware [[10.1039/d2dd00067a]], explainability-driven [[10.1016/j.ress.2022.109046]], and Gaussian-process lineages [[10.1016/j.energy.2019.116467]] point the way, but certification-grade ML \u2014 models whose failure modes are enumerated and bounded \u2014 remains beyond the published state of the art. Hybrid physics\u2013data architectures are the most credible certification path because part of their behavior is analytically specified; making that argument rigorous is an open task for the PINN community."),

('h2', '9.5 Foundation-model integration'),
('p',
 "The first LLM-based management studies [[10.1016/j.ress.2026.112416]][[10.1016/j.ensm.2026.104983]] suggest a division of labor worth formalizing: foundation models as reasoning, orchestration, and human-interface layers; conventional ML as calibrated estimators; physics models as safety envelopes. Research is needed on grounding (preventing hallucinated battery knowledge), latency, and the division of safety authority between learned and non-learned components. Battery-domain foundation models pretrained on cycling corpora are a plausible medium-term development."),

('h2', '9.6 Under-served functions'),
('p',
 "Finally, the function distribution itself signals opportunity. Cell balancing is nearly untouched by ML beyond pack-level insight [[10.1016/j.est.2023.106931]]; charging control needs certifiable adaptive protocols; and thermal management remains simulation-dominated [[10.1016/j.est.2023.106688]]. These functions share a property that explains their under-representation: they are *control* problems, where errors act on the battery rather than merely reporting on it, and where the evidence bar is correspondingly higher. Closing them will require the safety-case machinery of Section 9.4 as much as new algorithms."),

('tbl', 'TABLE_GAPS'),

('h2', '9.7 A reporting checklist for machine-learning BMS studies'),
('p',
 "The most concrete artifact this review can offer is procedural. Modeled on the CONSORT and PRISMA checklists that transformed reporting in clinical and review literature, Table 11 proposes a twelve-item BMS-ML reporting checklist: the minimum metadata a study should disclose for its accuracy claims to be comparable, reproducible, and poolable in future syntheses. None of the items is onerous; each corresponds to a practice whose absence the corpus analysis showed to be distorting \u2014 undisclosed splits (Section 3.4), uncalibrated uncertainty (Section 8.2), unnamed datasets (Section 3.4), or unquantified compute (Section 9.3). We suggest journals adopt it as a submission checklist and that authors attach it to their released datasets."),

('tbl', 'TABLE_CHECKLIST'),

('fig', 'figures/fig6_timeline.png', 'Fig. 8 Milestones of machine learning in battery management, 2019\u20132026, drawn from the corpus: early-life cycle prediction [[10.1038/s41560-019-0356-8]], closed-loop Bayesian fast charging [[10.1038/s41586-020-1994-5]], fleet-scale SOH pipelines [[10.1038/s42256-021-00312-3]], the physics-informed wave [[10.1016/j.jechem.2022.11.036]], cross-domain health estimation and cloud BMS [[10.1016/j.energy.2023.127033]][[10.1016/j.ensm.2023.02.035]], optimization-augmented and transfer learning [[10.1016/j.apenergy.2024.123248]], deep-RL prognostics [[10.1016/j.ress.2025.111392]], and the first foundation-model studies [[10.1016/j.ensm.2026.104983]].'),

('h1', '10. Conclusion'),
('p',
 "This review has examined the state of AI-powered battery management through a verified corpus of 103 peer-reviewed studies spanning 2019\u20132026, classified uniformly across management functions, method families, chemistries, data sources, and validation practices. Three conclusions stand out. First, the field has undergone a marked methodological evolution: classical feature-based learners gave way to deep sequence models, which are now themselves being displaced at the research frontier by physics-informed hybrids, optimization-augmented learning, transfer-learning regimes, and \u2014 at the very edge of the window \u2014 foundation-model components. Second, the center of gravity of application remains estimation (state, health, lifetime), where learning systems have largely succeeded on laboratory terms; control functions (charging, thermal, balancing) remain demonstrably transformable but under-evidenced for deployment. Third, and most critically, the field\u2019s published accuracy progress is not matched by validation progress: online or fleet-level demonstration appears in fewer than one study in ten, benchmark-data monoculture distorts the apparent state of the art, and the field\u2019s favored remedy \u2014 physics-informed architecture \u2014 does not substitute for validation rigor: physics-informed papers are strong-protocol-validated less often than purely data-driven peers (54% versus 73%)."),

('p',
 "The near-term agenda follows directly: standardized cross-domain validation protocols; diversified and shareable fleet data; edge-deployable architectures designed under onboard constraints; calibrated uncertainty and interpretability as certification prerequisites; and a principled division of labor between foundation models, calibrated estimators, and physics-based safety envelopes. If the last five years were about discovering what machine learning can estimate about a battery, the next five will be decided by what it can be trusted to do \u2014 onboard, at fleet scale, across chemistries, and over full cell lifetimes."),

('decl', None),
]

# ---------------- Tables ----------------

TABLE1 = {
 'caption': 'Table 1 Inclusion and exclusion criteria applied during corpus screening',
 'header': ['Dimension', 'Included', 'Excluded'], 'widths': [1.0, 2.75, 2.75],
 'rows': [
  ['Document type', 'Peer-reviewed journal articles', 'Conference abstracts/proceedings, preprints (SSRN), corrigenda'],
  ['Subject', 'Batteries and battery systems with a management function', 'Materials discovery, cell design, grid/infrastructure demand modeling without BMS function'],
  ['Method', 'ML as a substantive component (estimation, control, diagnosis, analysis)', 'Papers without a learning component'],
  ['Period', '2020\u20132026 (plus one 2019 field-defining seed)', 'Pre-2020 publications'],
  ['Verification', 'Metadata confirmed by direct Crossref DOI resolution', 'Unresolvable or mismatched records'],
  ['Language', 'English', 'Non-English'],
 ],
}

TABLE2 = {
 'caption': 'Table 3 Corpus composition: management function by publication year. The Reviews column counts the 12 method-family reviews; Primary = Total \u2212 Reviews gives the primary-application counts used in Fig. 1.',
 'header': ['Function', "'19", "'20", "'21", "'22", "'23", "'24", "'25", "'26", 'Total', 'Reviews', 'Primary'],
 'widths': [1.5, 0.36, 0.36, 0.36, 0.36, 0.36, 0.36, 0.36, 0.36, 0.45, 0.72, 0.68],
 'rows': 'AUTO_AREA_YEAR',
}

TABLE3 = {
 'caption': 'Table 8 Representative corpus studies by management function and method family. Entries gloss each study as: study summary (data basis; headline contribution). References in brackets refer to the numbered list.',
 'header': ['Function', 'Method family', 'Representative studies (data; contribution)'],
 'rows': [
  ['State estimation (SOC)', 'Filter-embedded learning; meta-heuristic DL',
   'LSTM+UKF embedded estimator (laboratory cells; learned observation model in a UKF) [[10.1016/j.energy.2020.117664]]; PSO-LSTM (laboratory cells; meta-heuristically tuned recurrent SOC) [[10.1016/j.energy.2021.121236]]; GA-LSTM with adaptive Kalman filtering (laboratory cells; low error under noise) [[10.1016/j.apenergy.2024.123508]]'],
  ['Health estimation (SOH)', 'Classical ML; deep learning; transfer learning',
   'ML pipeline over 179 cells (own cell fleet; relaxed charge-curve features) [[10.1038/s42256-021-00312-3]]; deep learning without extra degradation experiments (public MATR dataset; cross-chemistry generalization) [[10.1038/s41467-023-38458-w]]; real-world vehicle SOH (fleet data; field-noise robustness) [[10.1016/j.energy.2023.126855]]'],
  ['Prognostics (RUL)', 'Classical ML; physics-informed; RL',
   'Early-life cycle prediction (public MATR dataset; about 9% median test error) [[10.1038/s41560-019-0356-8]]; physics-informed early-cycle RUL (multiple datasets; small-data prognosis) [[10.1016/j.apenergy.2025.125314]]; deep-RL prognostic model fusion (public NASA dataset; adaptive model selection) [[10.1016/j.ress.2025.111392]]'],
  ['Charging control', 'Bayesian optimization; mechanism-aware control',
   'Closed-loop Bayesian protocol optimization (hardware prototype; 2.5 versus 18 months to a protocol) [[10.1038/s41586-020-1994-5]]; plating-perceiving fast charging (hardware prototype; plating-free protocols) [[10.1016/j.ensm.2022.12.034]]; ensemble-surrogate charging optimization (laboratory cells; multi-objective strategies) [[10.1016/j.enconman.2025.120170]]'],
  ['Thermal management', 'ANN surrogate; physics-informed; optimization',
   'ANN temperature prediction (laboratory cells; low-error thermal model) [[10.1016/j.applthermaleng.2023.120482]]; PINN heat-generation estimation (simulation; embedded thermal physics) [[10.1016/j.jechem.2022.11.036]]; ML-assisted BTMS design (simulation; multi-objective cooling design) [[10.1016/j.applthermaleng.2024.123826]]'],
  ['Fault & safety', 'Shallow ML; multiphysics + ML; transfer learning',
   'SVM fault diagnosis (hardware prototype; sensor and connection faults) [[10.1016/j.energy.2020.118866]]; multiphysics-ML runaway prediction (simulation and hardware; module-level hazard) [[10.1016/j.jpowsour.2024.235015]]; cross-fleet runaway-diagnosis transfer (fleet data; small-sample diagnosis) [[10.1016/j.apenergy.2024.123248]]'],
  ['Cross-cutting', 'Physics-informed; XAI; digital twin; LLM',
   'EIS diagnostics PINN review (multiple studies; paradigm synthesis) [[10.1016/j.rser.2023.113807]]; uncertainty-aware early-life prediction (public MATR dataset; calibrated forecasts) [[10.1039/d2dd00067a]]; LLM vehicle-cloud management (fleet data; orchestration layer) [[10.1016/j.ensm.2026.104983]]'],
 ],
}

TABLE_DATASETS = {
 'caption': 'Table 4 Benchmark datasets and data sources recurring across the corpus',
 'header': ['Data source', 'Papers', 'Typical use in corpus'],
 'widths': [1.9, 0.6, 3.9],
 'rows': [
  ['Own laboratory cycling', '36', 'Primary training/testing data for estimators and protocols'],
  ['Severson/Toyota\u2013MIT\u2013Stanford (MATR)', '11', 'Cycle-life and early-life prediction benchmarks'],
  ['NASA PCoE', '6', 'Capacity-fade and RUL benchmarking'],
  ['CALCE', '6', 'SOH estimation and degradation modeling'],
  ['Laboratory EIS', '6', 'Impedance-based SOH/SOC and degradation-mode studies'],
  ['Real vehicle / fleet data', '10', 'Online SOH, anomaly detection, cloud BMS'],
  ['Simulation (CFD/electrochemical)', '12', 'Thermal design, charging optimization, runaway prediction'],
  ['Review synthesis (no primary data)', '15', 'Methodological and thematic reviews'],
  ['Multiple datasets', '1', 'Studies drawing on several of the above'],
 ],
}

TABLE_GAPS = {
 'caption': 'Table 10 Structural research gaps and corresponding future directions',
 'header': ['Gap', 'Evidence in corpus', 'Future direction'],
 'widths': [1.15, 2.55, 2.7],
 'rows': [
  ['Validation practice', '17 primary studies use within-cell or k-fold validation; 9/103 demonstrate online or fleet use', 'Standardized cross-cell, cross-chemistry, lab-to-fleet transfer protocols as reporting norms'],
  ['Benchmark monoculture', 'Single public dataset underlies 11 studies; NASA/CALCE sustain much of the rest', 'Federated learning, anonymized fleet-data releases, multi-institution cycling campaigns'],
  ['Onboard deployment', 'Few studies treat compute/memory/latency as design constraints', 'Quantization-aware training, resource-constrained NAS, cloud\u2013edge hybrid estimation'],
  ['Trust and certification', 'Interpretability mostly post-hoc; uncertainty rarely calibrated', 'Calibrated uncertainty, analytically specified hybrid architectures, safety-case methodology'],
  ['Foundation-model integration', 'First two LLM-based studies appear 2025\u20132026', 'Grounded LLM orchestration layers; domain foundation models; division of safety authority'],
  ['Under-served functions', 'Balancing (2 papers), charging control (8), thermal (8)', 'Certifiable adaptive control with mechanism-aware safety envelopes'],
 ],
}


TABLE_METH = {
 'caption': 'Table 2 Method families in the corpus: representative techniques, strengths, and limitations',
 'header': ['Method family', 'Papers', 'Representative techniques', 'Strengths', 'Limitations'],
 'widths': [1.15, 0.5, 1.8, 1.55, 1.5],
 'rows': [
  ['Classical ML', '29', 'Gaussian process regression, SVM/SVR, ensembles, shallow networks on engineered features', 'Calibrated uncertainty; small-data friendly; cheap to embed', 'Feature engineering is manual; ceilings under complex dynamics'],
  ['Deep learning', '19', 'LSTM/GRU, CNN, attention/Transformer, autoencoders, graph networks', 'Learns features from raw curves; strong trajectory modeling', 'Data-hungry; weak extrapolation; opaque'],
  ['Physics-informed / hybrid', '24', 'PINNs, physics-constrained autoencoders, filter-embedded networks, multiphysics fusion', 'Structure aids extrapolation; reduced data demand', 'Inherits simplified-model bias; harder to train'],
  ['Optimization-augmented', '11', 'Bayesian optimization, surrogate-assisted multi-objective design, meta-heuristic-tuned networks', 'Sample-efficient protocol discovery; explicit trade-off handling', 'Offline tuning cost; surrogate bias'],
  ['Transfer / domain adaptation', '5', 'Domain-adversarial training, fine-tuning across chemistry/protocol', 'Directly targets the generalization gap', 'Negative transfer; needs shared protocols'],
  ['Reinforcement / control learning', '1', 'Deep-RL prognostic model selection', 'Adaptive decision-making along trajectories', 'Training stability; scarce hardware validation'],
  ['Foundation models / LLM', '2', 'Domain-tuned LLM agents for risk analysis and orchestration', 'Reasoning over heterogeneous text/system context', 'Hallucination risk; latency and cost'],
  ['Review / perspective', '12', 'Narrative and systematic syntheses', 'Maps the field; identifies shared gaps', 'No primary validation'],
 ],
}

TABLE_VALID = {
 'caption': 'Table 5 Validation practices across the corpus',
 'header': ['Validation approach', 'Papers', 'Interpretation'],
 'widths': [1.9, 0.6, 3.9],
 'rows': [
  ['Cross-cell holdout', '24', 'Strongest common laboratory protocol; unseen sibling cells'],
  ['Experimental hardware', '19', 'Physical validation of estimator or controller behavior'],
  ['Review synthesis', '15', 'No primary validation applicable'],
  ['Within-cell split', '12', 'Optimistic; trajectory leakage between train and test'],
  ['Online / real-vehicle', '9', 'Deployment-relevant evidence; rarest strong protocol'],
  ['Cross-chemistry holdout', '7', 'Strictest generalization demand in corpus'],
  ['k-fold cross-validation', '5', 'Optimistic without cell-level isolation'],
  ['Simulation (+ hardware spot-check)', '8', 'Model-fidelity dependent; strongest when hardware-checked'],
  ['Cross-domain holdout', '3', 'Transfer-specific evidence'],
  ['Case study', '1', 'Single-system demonstration'],
 ],
}


TABLE_FLEET = {
 'caption': 'Table 7 Cross-tabulation of fleet-data use against online validation (103 papers). Fleet-data use describes the primary data source; online validation describes the validation protocol; their overlap is 8 of 10 fleet-data papers. The right-hand column pools the validation categories of Table 5.',
 'header': ['', 'Online / real-vehicle validation', 'All other validation protocols (Table 5)', 'Total papers'],
 'rows': [
  ['Real-vehicle / fleet data', '8', '2 (transfer; case study)', '10'],
  ['Other data sources', '1 (laboratory-data demonstration)', '92', '93'],
  ['Total', '9', '94', '103'],
 ],
}


TABLE_CONF = {
 'caption': 'Table 6 Conference sensitivity set: 14 machine-learning battery papers from control and transportation-electrification venues (2019\u20132025), Crossref-verified, with validation evidence stated in their indexed abstracts.',
 'header': ['Venue (year)', 'Function', 'Method family (short)', 'Validation evidence stated in indexed abstract'],
 'widths': [1.3, 0.9, 2.0, 2.3],
 'rows': [
  ['ITEC 2019', 'SOC', 'LSTM recurrent network [[10.1109/itec.2019.8790543]]', 'Not stated'],
  ['VPPC 2021', 'SOH', 'ML ensemble [[10.1109/vppc53923.2021.9699273]]', 'Public dataset'],
  ['ITEC 2022', 'SOC+SOH', 'Dual extended Kalman filter [[10.1109/itec53557.2022.9813961]]', 'Not stated'],
  ['ACC 2023', 'SOC+SOH', 'Real-time estimator + batch least squares [[10.23919/acc55779.2023.10156326]]', 'Not stated'],
  ['ACC 2021', 'SOC', 'Multiple-model adaptive estimation [[10.23919/acc50511.2021.9482734]]', 'Simulation-level'],
  ['ITEC 2023', 'SOH', 'Histogram data + PCA + regression [[10.1109/itec55900.2023.10187012]]', 'Public dataset'],
  ['APEC 2023', 'Overview', 'Review of ML-enabled estimation [[10.1109/apec43580.2023.10131605]]', 'Not applicable'],
  ['ECC 2021', 'SOH', 'Reinforcement learning + observer [[10.23919/ecc54610.2021.9655199]]', 'Not stated'],
  ['CCDC 2022', 'SOH', 'CNN-BiLSTM transfer learning [[10.1109/ccdc55256.2022.10033695]]', 'Hardware (stated); public data'],
  ['VPPC 2019', 'SOC', 'SVR + PCA with dual-polarization model [[10.1109/vppc46532.2019.8952458]]', 'Not stated'],
  ['ACC 2024', 'SOC+SOH', 'EKF critique and improvement [[10.23919/acc60939.2024.10644628]]', 'Simulation-level'],
  ['VPPC 2022', 'Prognostics', 'ML on aging data [[10.1109/vppc55846.2022.10003444]]', 'Hardware (stated)'],
  ['VPPC 2019', 'SOC', 'Kalman filter on reduced electrochemical model [[10.1109/vppc46532.2019.8952284]]', 'Simulation-level'],
  ['VPPC 2021', 'SOC', 'Computationally efficient neural network [[10.1109/vppc53923.2021.9699201]]', 'Simulation-level'],
 ],
}

TABLE_LLM = {
 'caption': 'Table 9 Safety and verification taxonomy for foundation-model components in the BMS stack. The right-hand column is normative guidance proposed by this review, not claims about the published studies.',
 'header': ['Dimension', 'Classical / deep ML estimators (established practice)', 'Published LLM studies (2025\u20132026)', 'Required guardrail (this review)'],
 'widths': [1.0, 1.9, 1.8, 1.8],
 'rows': [
  ['Role in the stack', 'Calibrated numeric estimation and detection', 'Incident risk analysis [[10.1016/j.ress.2026.112416]]; vehicle-cloud orchestration [[10.1016/j.ensm.2026.104983]]', 'Estimation stays with calibrated ML; LLM coordinates, summarizes, explains'],
  ['Grounding', 'Trained on domain cycling data', 'Domain-tuned corpora and knowledge-enhanced prompting', 'Retrieval over verified corpora with source citations; no ungrounded recall'],
  ['Dominant failure mode', 'Bounded numeric error under distribution shift', 'Open-ended hallucinated text', 'Outputs restricted to structured, checkable forms; never free text into protection logic'],
  ['Uncertainty', 'Gaussian-process / conformal intervals in a subset of studies', 'Not quantified in published studies', 'Calibrated intervals mandatory before any actuation-adjacent role'],
  ['Latency and compute', 'Millisecond-class, onboard', 'Second-class, cloud-dependent', 'Offline analysis and planning only unless real-time evidence is shown'],
  ['Safety authority', 'Bounded by physics envelopes and thresholds', 'Undefined in published studies', 'LLM components must never hold direct cell-level protection authority'],
 ],
}

TABLE_CHECKLIST = {
 'caption': 'Table 11 Proposed BMS-ML reporting checklist (BMS-ML-RC), modeled on CONSORT/PRISMA reporting standards.',
 'header': ['#', 'Reporting item', 'What must be reported'],
 'widths': [0.35, 1.85, 4.3],
 'rows': [
  ['1', 'Dataset identity', 'Exact name and version of every dataset (e.g., Severson-MATR, NASA, CALCE); download source'],
  ['2', 'Cell population', 'Number of cells, chemistry, manufacturer, format, and batch for every training and test set'],
  ['3', 'Sensor and sampling context', 'Measured channels, sampling rate, sensor class, and temperature conditions'],
  ['4', 'Split protocol', 'Split type (within-cell / cross-cell / cross-chemistry / cross-domain) and isolation argument; within-cell splits must be flagged as such'],
  ['5', 'Out-of-distribution evaluation', 'At least one protocol under which test conditions differ from training (chemistry, temperature, protocol, or source)'],
  ['6', 'Baselines', 'At least one classical baseline alongside the proposed architecture, with identical data'],
  ['7', 'Randomness control', 'Seeds or repeated-run statistics for every stochastic training result'],
  ['8', 'Uncertainty', 'Calibrated uncertainty or error bars for headline claims, not point estimates alone'],
  ['9', 'Compute budget', 'Training compute and inference latency/memory on the target (or a stated reference) platform'],
  ['10', 'Failure analysis', 'At least one documented failure mode and its distribution (where the model is worst)'],
  ['11', 'Validation environment', 'Which of the following applies: simulation, laboratory cycling, hardware prototype, online/fleet'],
  ['12', 'Artifact availability', 'Data and code deposit (DOI-backed) or an explicit stated exemption'],
 ],
}
