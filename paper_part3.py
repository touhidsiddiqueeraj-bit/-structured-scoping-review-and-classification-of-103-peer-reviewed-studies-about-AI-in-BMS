#!/usr/bin/env python3
"""Paper text part 3: Sections 7-10, declarations, and table data."""

BLOCKS = [
('h1', '7. Machine Learning for Thermal Management, Faults and Safety'),

('h2', '7.1 Thermal-state estimation and thermal management'),
('p',
 "Thermal management is the corpus\u2019s smallest quantitative engineering cluster (7 primary papers; 8 including a review) but a disproportionately safety-critical one. Data-driven temperature estimation ranges from ANN models predicting cell temperature across operating conditions [[10.1016/j.applthermaleng.2023.120482]] to internal-temperature sensing under ultrahigh-rate discharge, where surface measurement fails [[10.1016/j.apenergy.2026.127394]]. On the design and control side, ML-surrogate models accelerate liquid-cooling plate analysis and multi-objective optimization of BTMS geometry [[10.1016/j.jpowsour.2021.229727]][[10.1016/j.applthermaleng.2024.123826]], experimentally validated parallel-liquid-cooling designs demonstrate the optimization loop end-to-end [[10.1016/j.applthermaleng.2022.118503]], and ANN-controlled thermal management reduces cooling parasitic load while holding temperature limits [[10.3390/wevj16050279]]. Physics-informed heat-generation estimation embeds thermal physics priors into the learning problem [[10.1016/j.jechem.2022.11.036]], and a state-of-the-art review consolidates the cluster [[10.1016/j.est.2023.106688]]."),

('p',
 "The thermal cluster\u2019s papers divide cleanly by purpose, and the division clarifies where machine learning adds value. For *estimation* purposes \u2014 predicting internal or surface temperature under load \u2014 learned models replace thermocouple instrumentation that no production pack can afford, and physics-informed variants regularize the extrapolation regime where data-driven thermal models are least trustworthy [[10.1016/j.jechem.2022.11.036]]. For *design* purposes \u2014 sizing and arranging cooling hardware \u2014 ML surrogates amortize expensive CFD evaluation across optimization loops, turning weeks of simulation into tractable search [[10.1016/j.jpowsour.2021.229727]][[10.1016/j.applthermaleng.2024.123826]]. For *control* purposes \u2014 modulating cooling effort online \u2014 ANN controllers demonstrate parasitic-load reductions in simulation [[10.3390/wevj16050279]], but no subset paper yet closes this loop on hardware, leaving thermal control where charging control was five years ago."),

('h2', '7.2 Fault diagnosis and anomaly detection'),
('p',
 "Fault and safety applications (7 primary papers; 9 including reviews) divide into diagnosis of realized faults and prediction of impending hazards. On the diagnosis side, grid-search-optimized support vector machines classify sensor and connection faults [[10.1016/j.energy.2020.118866]], curvilinear-Manhattan-distance methods detect multiple pack fault types in operating fleets [[10.1016/j.est.2023.107575]], and multi-scenario deep anomaly detection covers real EV operating envelopes [[10.1016/j.etran.2025.100418]]. Manufacturing-side inspection applies force-signal deep learning to catch lithium-plating-type defects before cells ship [[10.1016/j.jechem.2025.04.025]]. The hazard-prediction side is increasingly model-based: multiphysics models coupled with ML predict module-level thermal-runaway progression [[10.1016/j.jpowsour.2024.235015]], a multiphysics-informed DeepONet predicts runaway using virtual data to augment scarce experimental events [[10.1016/j.etran.2024.100337]], and multi-source domain transfer moves thermal-runaway diagnosis across vehicle fleets with small target samples [[10.1016/j.apenergy.2024.123248]]."),

('h2', '7.3 Critical assessment'),
('p',
 "Safety applications carry the corpus\u2019s highest stakes and its thinnest evidence base. Thermal-runaway events are rare and expensive to generate, so learning systems train on simulation or small laboratory campaigns; the DeepONet line\u2019s virtual-data approach [[10.1016/j.etran.2024.100337]] is a rational response, but it inherits the fidelity limits of the underlying multiphysics models. The reviews in this cluster are notably candid: laboratory fault diagnosis has historically failed to transfer to real vehicles because fault signatures are masked by pack-level averaging, sensor noise, and operating diversity [[10.1016/j.etran.2023.100254]][[10.3390/electronics10111309]]. The fleet-data anomaly-detection studies are therefore the cluster\u2019s most valuable trend, even though label scarcity for rare faults keeps evaluation largely qualitative."),

('h1', '8. Cross-Cutting Directions'),

('h2', '8.1 Physics-informed learning'),
('p',
 "Within the classified subset, physics-informed and hybrid model\u2013data learning is the most consistently rising methodological theme (24 family-coded papers across all functions; 22 of them primary applications; the only family with a monotonically non-decreasing primary trajectory within the subset \u2014 a pattern the eligible pool\u2019s query-theme tags do not mirror, Section 3.2). Beyond the prognostics applications of Section 5.4, physics-informed structures appear in state estimation [[10.1109/jrfid.2022.3211841]][[10.1016/j.measurement.2025.118985]], heat-generation estimation [[10.1016/j.jechem.2022.11.036]], and impedance-based diagnostics, where physics-informed deep learning over electrochemical impedance spectra is consolidating into a diagnostic paradigm of its own [[10.1016/j.rser.2023.113807]]. Physics-constrained autoencoders improve health prediction over purely learned counterparts [[10.1007/s00521-022-07291-5]], and recurrent networks trained to anticipate uncertain future duty conditions address degradation prediction under distribution shift directly [[10.1016/j.ensm.2022.05.007]]. A parallel fusion literature combines physical and data-driven models for internal-state estimation generally [[10.3390/batteries10120442]]. The appeal is easy to state: physics priors supply exactly the extrapolation structure that pure learners lack. The corpus\u2019s caution is that most physics-informed studies embed *simplified* physics \u2014 equivalent-circuit or reduced electrochemical models \u2014 so the hybrid inherits model bias even as it gains structure."),

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
 "The classified subset’s youngest theme is generative, and its two studies divide the labor differently. Domain-specific large language models perform risk analysis of battery energy-storage incidents by synthesizing heterogeneous incident reports [[10.1016/j.ress.2026.112416]] — a reasoning-and-synthesis role. The second study, HA-LLM [[10.1016/j.ensm.2026.104983]], is an LLM-based SOH estimator: it aligns resampled charging-current sequences with the LLM embedding space, injects battery degradation priors through prefix adaptation, and — most notably for safety — wraps the LLM in an uncertainty-aware module that estimates predictive uncertainty by Monte Carlo sampling and selectively substitutes a physics-consistent estimator when uncertainty is high. It is validated on one year of field data from 100 production vehicles on a vehicle-cloud platform, with an independent teardown and bench capacity calibration on an unseen vehicle model, and it remains robust in few-shot and zero-shot cross-vehicle evaluations. The published work therefore already spans both the orchestration seat and the estimator seat, and the estimator-seat study is instructive precisely because its authors treated hallucination risk as a design constraint: uncertainty-triggered fallback to a physics-consistent estimator is exactly the guardrail this review argues should be mandatory (Table 9). The appearance of both roles in mainstream energy journals in 2025–2026 marks a new phase: the management stack is beginning to absorb foundation-model components. Earliest-here claims are bounded by retrieval: a GPT-4-based health estimator by Poh et al. [[10.1109/tec.2025.3548400]] appeared in IEEE Transactions on Energy Conversion in 2025, predating both studies, and it appears nowhere in the released 1,550-record retrieval — a recall miss of the query design, not a venue exclusion. The recall audit of Section 2.2 shows such misses are structural rather than exceptional: the capped queries contain only 16–17% of the in-scope, 2020-onward literature cited by this review’s own included reviews, and the missed TEC paper is cited by none of those reviews either, so even a reference-list-driven search would not have surfaced it. Studies in this subset are therefore described as the earliest in the classified subset, not the first in the field."),

('p',
 "Because BMS software is safety-critical, this review argues for an explicit division of labor before that absorption goes further, and Table 9 makes it concrete. The table contrasts established practice for classical and deep learning estimators with what the corpus’s two LLM studies actually demonstrate, and states the guardrails this review regards as mandatory before any LLM component touches a safety-relevant path. The right-hand column is normative guidance proposed here, not claims about the published studies. The notable point is that the subset’s earliest LLM estimator study [[10.1016/j.ensm.2026.104983]] already implements two of those guardrails — Monte-Carlo uncertainty gating and substitution by a physics-consistent estimator — while leaving direct cell-level safety authority undefined, which is where the line should stay for now."),

('tbl', 'TABLE_LLM'),

('h2', '8.5 Manufacturing analytics and system-level synthesis'),
('p',
 "Two further cross-cutting threads connect management to the wider battery value chain. Cell-production mapping studies chart ML use across manufacturing stages from mixing to formation [[10.1002/batt.202300046]], complementing the coating-quality interpretability work [[10.1016/j.conengprac.2022.105202]] and manufacturing defect detection [[10.1016/j.jechem.2025.04.025]] \u2014 the management implication being that cell quality information is itself a BMS input. And the pack-level insight that routine cell balancing can be eliminated in well-managed packs, reducing hazardous lithium-plating side reactions, shows learned analysis reshaping a function (balancing) that classical control had considered settled [[10.1016/j.est.2023.106931]], while ML mappings from equivalent-circuit parameters to electrochemical properties give classical BMS models a physically interpretable learned layer [[10.1016/j.est.2024.113257]]."),

('h1', '9. Research Gaps and Future Directions'),
('p',
 "Cross-referencing the bibliometric analysis of Section 3 with the function-level reviews of Sections 4\u20138 yields six structural gaps, discussed in Sections 9.1\u20139.6, summarized in Table 11, previewed against the field's milestones in Fig. 8, and then operationalized into a concrete reporting checklist in Section 9.9."),

('h2', '9.1 Validation and benchmarking standards'),
('p',
 "The corpus\u2019s validation data are unambiguous: 17 of the 88 primary papers use within-cell splits or unsupervised k-folds, and only 8 of the 88 demonstrate their systems online or on real fleets. Until cross-cell, cross-temperature, and cross-protocol holdout protocols become reporting norms, published accuracy figures will continue to carry a systematic risk of overstating deployable performance. The most valuable near-term contribution the community can make is standardized transfer protocols \u2014 train-on-chemistry-A/test-on-chemistry-B, train-on-lab/test-on-fleet \u2014 reported alongside headline accuracy, as already practiced by the transfer-learning and general-framework studies [[10.1016/j.apenergy.2024.125086]][[10.1109/tte.2025.3533540]]."),

('p',
 "A second standardization target is reporting itself. In our full-text reading of the corpus we did not routinely encounter disclosed split definitions, random seeds, or compute budgets; only the validation, data-source, and artifact items were systematically score-counted (Section 9.9), so this is a qualitative observation rather than a measured rate. Either way, such omissions make independent replication laborious and meta-analysis impossible (Section 5.6). A community-endorsed reporting checklist \u2014 dataset identity and version, split protocol, uncertainty quantification, and hardware context \u2014 would cost little and would let the synthesis literature do its job."),

('h2', '9.2 Data sharing and benchmark concentration'),
('p',
 "Twenty-three primary papers rest on the same three public benchmarks (Severson-MATR 11, NASA 6, CALCE 6), and 36 use private laboratory cells whose data are not released. This two-pole fragmentation inflates apparent comparability on the shared benchmarks and hides dataset-specific failure modes, while precluding audit altogether on the private pole. Federated learning over fleet data, standardized anonymized fleet-data releases, and multi-institution cycling campaigns \u2014 in the spirit of the 179-cell pipeline [[10.1038/s42256-021-00312-3]] \u2014 would diversify the evidence base at modest incremental cost."),

('p',
 "The economics argument strengthens the technical one. A fleet operator\u2019s marginal value from a percentage point of SOH accuracy is measured in warranty provisions and residual-value pricing, which justifies onboard compute budgets that academic prototypes routinely ignore. Quantized and pruned recurrent models, event-driven inference triggered by charge sessions rather than continuous streams, and asymmetric architectures \u2014 lightweight onboard estimators with cloud-side retraining \u2014 are the concrete design patterns emerging from the corpus\u2019s edge-aware minority [[10.1016/j.est.2022.104901]][[10.1016/j.jpowsour.2025.236784]]."),

('h2', '9.3 Edge deployment and onboard constraints'),
('p',
 "Only a handful of corpus works treat onboard compute, memory, or latency as first-class design constraints, notably the board-level RUL implementation [[10.1016/j.est.2022.104901]] and real-time feature-extraction studies [[10.1016/j.jpowsour.2025.236784]]. The gap is widening as models grow: transformer and PINN architectures trained on workstations must eventually run beside BMS microcontrollers. Quantization-aware training, neural architecture search under resource constraints, and hybrid designs that place heavy learners in the cloud and lightweight correction layers onboard are the natural research program here [[10.1016/j.ensm.2026.104983]]."),

('h2', '9.4 Trust, uncertainty, and safety standards'),
('p',
 "Estimates that guide protection and charging decisions need calibrated uncertainty and auditable reasoning. The corpus\u2019s uncertainty-aware [[10.1039/d2dd00067a]], explainability-driven [[10.1016/j.ress.2022.109046]], and Gaussian-process lineages [[10.1016/j.energy.2019.116467]] point the way, but certification-grade ML \u2014 models whose failure modes are enumerated and bounded \u2014 remains beyond the published state of the art. Hybrid physics\u2013data architectures are the most credible certification path because part of their behavior is analytically specified; making that argument rigorous is an open task for the PINN community."),
('p',
 "The safety standards invoked in the introduction \u2014 UN GTR No. 20 on electric-vehicle safety (established in the UN Global Registry in 2018 [[std:unece-gtr20]]; its Amendment 1, adding thermal-propagation requirements with two compliance options \u2014 a physical propagation test or a documented risk-management approach \u2014 was submitted by the European Commission on behalf of the Informal Working Group on Electric Vehicle Safety as formal document ECE/TRANS/WP.29/GRSP/2026/4, alongside the working group\u2019s status report ECE/TRANS/WP.29/GRSP/2026/3 [[std:unece-gtr20-amd1]]; it was considered at the 79th session of the Working Party on Passive Safety (GRSP, June 2026) and stood, at this review\u2019s 18 October 2026 finalization date, pending before WP.29 with adoption listed for its 17\u201320 November 2026 session), GB 38031 (GB 38031-2020, superseded for new type approvals by GB 38031-2025 from July 2026, with existing models transitioning through July 2027; GB 38031-2025 requires that, once single-cell thermal runaway is triggered, the pack or system neither fire nor explode throughout a two-hour observation window, that a thermal-event alarm still be issued, and that smoke not harm occupants \u2014 superseding GB 38031-2020\u2019s criterion of an alarm at least five minutes before any fire or explosion \u2014 and adds bottom-impact and 300-cycle fast-charge safety tests [[std:gb38031-2025]]), ISO 26262:2018 (functional safety of road-vehicle E/E systems [[std:iso26262]]), ISO/PAS 8800:2024 (safety and artificial intelligence \u2014 the road-vehicle extension of ISO 26262 and ISO 21448 to learned components [[std:isopas8800]]), and ISO 21448 (SOTIF [[std:iso21448]]) \u2014 do not prescribe estimation algorithms, but they define what a deployed estimator or controller must be able to evidence, and Table 10 translates the subset\u2019s gaps into those terms. The mapping is this review\u2019s synthesis at requirement level rather than clause level, and it is stated so that it can be checked against the standards texts themselves: the point is not legal advice but that a validation protocol reported in a paper corresponds, or does not, to evidence a safety case can use. The inference rule behind every \u2018supports a standards argument\u2019 statement in this section is explicit: a paper\u2019s evidence can support such an argument only if it demonstrates performance on at least one held-out integration unit (a cross-cell holdout or stronger isolation protocol, Section 2.5) and reports the environment in which that evidence was obtained; by construction, within-cell and k-fold evidence cannot support the argument, because the safety case is about unseen cells and unseen duty. Three consequences stand out for automotive deployment. Within-cell and k-fold validation (17 primary papers) cannot support an ISO 26262 argument, because the safety case is about unseen cells and unseen duty and the protocol never tests an unseen unit; a standards argument must therefore be *argued* from the isolation evidence, not *asserted* from headline accuracy. Thermal-propagation early-warning latency is a timing requirement, so fault-detection papers evaluated on curated laboratory windows under-report both the false-alarm rate and the detection-delay distribution that the GB 38031-2025 / GTR-20 escape window needs. And charging or thermal control strategies validated only in simulation lack the hardware-in-the-loop evidence base an automotive release process expects. The reporting checklist of Section 9.9 is deliberately aligned with this mapping \u2014 reporting an isolation argument and a validation environment is the minimum on which any standards conversation can start."),

('tbl', 'TABLE_STD'),

('h2', '9.5 Foundation-model integration'),
('p',
 "The corpus's first LLM-based management studies (2025\u20132026, with LLM-based estimation prior art that this review\u2019s retrieval missed \u2014 Section 8.4) [[10.1016/j.ress.2026.112416]][[10.1016/j.ensm.2026.104983]] suggest a division of labor worth formalizing — with the caveat that HA-LLM [[10.1016/j.ensm.2026.104983]] already occupies the estimator seat under exactly the guardrails proposed here: foundation models as reasoning, orchestration, and human-interface layers, and as estimators only where uncertainty-gated and protected by physics-fallback substitution; conventional ML as calibrated estimators; physics models as safety envelopes. Research is needed on grounding (preventing hallucinated battery knowledge), latency, and the division of safety authority between learned and non-learned components. Battery-domain foundation models pretrained on cycling corpora are a plausible medium-term development."),

('h2', '9.6 Under-served functions'),
('p',
 "Finally, the function distribution itself signals opportunity — read at both levels of the evidence base. Cell balancing is the smallest core function both in the curated subset (2 papers) and in the quota-free eligible pool (38 of 799 tagged records, Section 3.3), so its under-representation is a property of the retrieved literature rather than of the quotas; ML has so far contributed mainly at the level of pack-level insight rather than as a balancing controller [[10.1016/j.est.2023.106931]]. Thermal management is not scarce as a theme in the pool (99 tagged records), but closed-loop thermal control has not yet been demonstrated on hardware in the subset, and the cluster remains simulation-dominated [[10.1016/j.est.2023.106688]] — the deficit is evidential, not topical. Charging control needs certifiable adaptive protocols. These functions share a property that explains the pattern: they are *control* problems, where errors act on the battery rather than merely reporting on it, and where the evidence bar is correspondingly higher. Closing them will require the safety-case machinery of Section 9.4 as much as new algorithms."),

('tbl', 'TABLE_GAPS'),

('h2', '9.7 Position relative to prior reviews'),
('p',
 "Section 1.3 situated this review against the function-specific and method-specific reviews that dominate the field; the positioning deserves its own statement because reviewers and readers routinely ask what a new review adds when several exist. The closest in scope among recent cross-functional reviews is the performance-centric review of Prasanna et al. [[10.1007/s44163-025-00721-y]] (240 studies, included from 361 screened records, across the EV powertrain, aggregating reported RMSE and R\u00b2); adjacent cross-functional surveys exist for degradation and estimation methods. This review is distinguished by what those studies do not attempt, and Table 12 states the comparison axis by axis: a two-tier corpus with record-level screening provenance (799 eligible records released in full, 103 classified in depth); a within-corpus measurement of validation-protocol strength across functions, with per-paper assignments released and method-family contrasts tested rather than asserted; a requirement-level mapping onto UN GTR 20, GB 38031, and ISO 26262; and a released, re-runnable analysis pipeline behind every count and figure. Where prior reviews ask *which method works best for function X*, this review asks *which claims can actually be checked \u2014 and what it would cost the reader to trust them* \u2014 which is the question a scoping review with a curated classified subset is positioned to answer, and the question that performance-centric aggregation cannot ask of itself."),

('tbl', 'TABLE_POSITION'),

('h2', '9.8 Outlook: what the next revision cycle of this literature should produce'),
('p',
 "Concretely, and tied to the gaps above, the highest-value near-term work falls in six directions. (a) *Duty-cycle-aware validation*: public cross-cell benchmarks that pair cycling data with recorded EV drive profiles, so that cross-chemistry and cross-domain generalization can be tested against transportation duty rather than laboratory schedules. (b) *Federated fleet evidence*: privacy-preserving SOH/SOC studies over live fleets (about 2% of the eligible corpus today), with the 179-cell pipeline [[10.1038/s42256-021-00312-3]] as the template. (c) *Benchmark diversification*: multi-institution cycling campaigns two orders of magnitude larger than MATR/NASA/CALCE and released with DOI-backed artifacts, addressing the two-pole fragmentation of Section 3.4. (d) *Pack- and vehicle-level ML*: estimation validated at the integration level where UN GTR 20 and GB 38031 requirements bite, instead of cell-level evidence transplanted upward. (e) *Functionally safe learning*: ML estimators whose uncertainty handling and assurance arguments are specified against ISO 26262 safety goals and ISO/PAS 8800, with ISO 21448/SOTIF reasoning for capability limitations, making certifiable charging and thermal control reachable. And (f) *honest foundation-model integration*: retrieval-grounded LLM agents with published latency and calibration budgets, capable of the coordination role while estimation authority stays with calibrated numeric models \u2014 extending, not contradicting, the corpus\u2019s LLM estimator [[10.1016/j.ensm.2026.104983]]. A guardrail on all six directions: the BMS-ML-RC checklist of Section 9.9 is designed to be attached to a paper at submission, so that the next revision cycle of this literature arrives auditable by construction."),

('h2', '9.9 A reporting checklist for machine-learning BMS studies'),
('p',
 "The most concrete artifact this review can offer is procedural. Modeled on the CONSORT and PRISMA checklists that transformed reporting in clinical and review literature, Table 13 proposes a twelve-item BMS-ML reporting checklist: the minimum metadata a study should disclose for its accuracy claims to be comparable, reproducible, and poolable in future syntheses. None of the items is onerous. Items 4, 5, and 11 operationalize the validation-protocol classes that the corpus analysis measured directly (Section 3.4); the remaining items respond to reporting omissions observed qualitatively across Sections 3\u20138 \u2014 undisclosed splits, uncalibrated uncertainty, unnamed datasets, unquantified compute \u2014 but only the validation, data-source, and artifact items are score-measured in this corpus, and the checklist has not been applied as an audit to all 103 studies. We suggest journals adopt it as a submission checklist and that authors attach it to their released datasets."),

('tbl', 'TABLE_CHECKLIST'),

('fig', 'figures/fig6_timeline.png', 'Fig. 8 Milestones of machine learning in battery management, 2019\u20132026, drawn from the corpus; dating follows the cited studies\u2019 publication years and is therefore citation- and retrieval-conditioned (Sections 2.2 and 3.1): early-life cycle prediction [[10.1038/s41560-019-0356-8]], closed-loop Bayesian fast charging [[10.1038/s41586-020-1994-5]], fleet-scale SOH pipelines [[10.1038/s42256-021-00312-3]], the physics-informed wave [[10.1016/j.jechem.2022.11.036]], cross-domain health estimation and cloud BMS [[10.1016/j.energy.2023.127033]][[10.1016/j.ensm.2023.02.035]], optimization-augmented and transfer learning [[10.1109/tte.2023.3311813]][[10.1016/j.apenergy.2024.123248]], deep-RL prognostics [[10.1016/j.ress.2025.111392]], and the first corpus foundation-model studies [[10.1016/j.ensm.2026.104983]].', 6.4),

('h1', '10. Conclusion'),
('p',
 "This review has examined machine learning in battery management on a two-tier evidence base: a rule-based eligible corpus of 799 journal articles from which field-level shares are measured within a documented capped retrieval, and an in-depth classified subset of 103 studies through which method, data, and validation practice are examined with a blind 30-paper reliability check and label-noise sensitivity ranges. Three conclusions stand out. First, and most critically, the subset\u2019s published accuracy claims have outpaced the validation evidence behind them: online or fleet-level demonstration appears in fewer than one primary study in ten, 17 of 88 primary papers use isolation-weakened splits, benchmark concentration and private-data fragmentation distort the apparent state of the art, and the favored remedy \u2014 physics-informed architecture \u2014 shows no detectable substitution for validation rigor in these counts: physics-informed papers use strong protocols at rates statistically indistinguishable from data-driven peers (36% versus 52% under the protocol-only definition, p = 0.32; 59% versus 74% under the broader definition, p = 0.19), a contrast too underpowered to rule out meaningful differences in either direction (Section 3.4), and therefore retained as an open hypothesis rather than a settled result. Second, the center of gravity of application remains estimation (state, health, lifetime): measured as shares of the eligible corpus, the SOC\u2013SOH\u2013prognostics union tags 366 of 799 records (45.8% \u2014 about half), where learning systems report laboratory-regime success \u2014 on metrics that this review argues cannot be pooled across papers (Section 5.6) \u2014 while control functions (charging, thermal, balancing) remain demonstrably transformable but under-evidenced for deployment, and vehicle- and pack-level practice stays thin relative to the level at which UN GTR 20, GB 38031, and ISO 26262 pose their requirements (Section 9.4). Third, within the classified subset the method families stratify by period \u2014 classical feature-based learners gave way to deep sequence models, which are now themselves being displaced at the research frontier by physics-informed hybrids, optimization-augmented learning, transfer-learning regimes, and, at the very edge of the window, foundation-model components \u2014 a within-subset sequence that the eligible pool\u2019s method-theme tags do not mirror, so no field-level family rise is measurable at either tier (Section 3.2)."),

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
  ['Period', 'Crossref date-stamps 2020\u20132027 at retrieval (798 records dated 2020\u20132026, one early-access record stamped 2027)', 'Pre-2020 publications, except the individually verified 2019 seed study admitted to the classified subset'],
  ['Verification', 'Metadata confirmed by direct Crossref DOI resolution', 'Unresolvable or mismatched records'],
  ['Language', 'English', 'Non-English'],
 ],
}

TABLE2 = {
 'caption': 'Table 3 Corpus composition: management function by publication year. The Reviews column counts the 12 method-family reviews plus the 3 review-type syntheses coded under their dominant method family; Primary = Total \u2212 Reviews is the 88-paper primary-application count used in Fig. 1.',
 'header': ['Function', "'19", "'20", "'21", "'22", "'23", "'24", "'25", "'26", 'Total', 'Reviews', 'Primary'],
 'widths': [1.5, 0.36, 0.36, 0.36, 0.36, 0.36, 0.36, 0.36, 0.36, 0.45, 0.72, 0.68],
 'rows': 'AUTO_AREA_YEAR',
}

TABLE3 = {
 'caption': 'Table 8 Representative classified-subset studies by management function and method family. Entries gloss each study as: study summary (data basis; headline contribution). References in brackets refer to the numbered list.',
 'header': ['Function', 'Method family', 'Representative studies (data; contribution)'],
 'rows': [
  ['State estimation (SOC)', 'Filter-embedded learning; meta-heuristic DL',
   'LSTM+UKF embedded estimator (laboratory cells; learned observation model in a UKF) [[10.1016/j.energy.2020.117664]]; PSO-LSTM (laboratory cells; meta-heuristically tuned recurrent SOC) [[10.1016/j.energy.2021.121236]]; GA-LSTM with adaptive Kalman filtering (laboratory cells; low error under noise) [[10.1016/j.apenergy.2024.123508]]'],
  ['Health estimation (SOH)', 'Classical ML; deep learning; transfer learning',
   'ML pipeline over 179 cells (own cell fleet; relaxed charge-curve features) [[10.1038/s42256-021-00312-3]]; deep learning without extra degradation experiments (public MATR dataset; cross-chemistry generalization) [[10.1038/s41467-023-38458-w]]; real-world vehicle SOH (fleet data; field-noise robustness) [[10.1016/j.energy.2023.126855]]'],
  ['Prognostics (RUL)', 'Classical ML; physics-informed; RL',
   'Early-life cycle prediction (public MATR dataset; about 9% median test error) [[10.1038/s41560-019-0356-8]]; physics-informed early-cycle RUL (multiple datasets; small-data prognosis) [[10.1016/j.apenergy.2025.125314]]; deep-RL prognostic model fusion (public NASA dataset; adaptive model selection) [[10.1016/j.ress.2025.111392]]'],
  ['Charging control', 'Bayesian optimization; mechanism-aware control',
   'Closed-loop Bayesian protocol optimization (hardware prototype; 224 candidates in 16 days vs >500 days of exhaustive search) [[10.1038/s41586-020-1994-5]]; plating-perceiving fast charging (hardware prototype; plating-free protocols) [[10.1016/j.ensm.2022.12.034]]; ensemble-surrogate charging optimization (laboratory cells; multi-objective strategies) [[10.1016/j.enconman.2025.120170]]'],
  ['Thermal management', 'ANN surrogate; physics-informed; optimization',
   'ANN temperature prediction (laboratory cells; low-error thermal model) [[10.1016/j.applthermaleng.2023.120482]]; PINN heat-generation estimation (simulation; embedded thermal physics) [[10.1016/j.jechem.2022.11.036]]; ML-assisted BTMS design (simulation; multi-objective cooling design) [[10.1016/j.applthermaleng.2024.123826]]'],
  ['Fault & safety', 'Shallow ML; multiphysics + ML; transfer learning',
   'SVM fault diagnosis (hardware prototype; sensor and connection faults) [[10.1016/j.energy.2020.118866]]; multiphysics-ML runaway prediction (simulation and hardware; module-level hazard) [[10.1016/j.jpowsour.2024.235015]]; cross-fleet runaway-diagnosis transfer (fleet data; small-sample diagnosis) [[10.1016/j.apenergy.2024.123248]]'],
  ['Cross-cutting', 'Physics-informed; XAI; digital twin; LLM',
   'EIS diagnostics PINN review (multiple studies; paradigm synthesis) [[10.1016/j.rser.2023.113807]]; uncertainty-aware early-life prediction (public MATR dataset; calibrated forecasts) [[10.1039/d2dd00067a]]; LLM-based SOH estimation with uncertainty-aware fallback (field data; subset\u2019s earliest LLM estimator \u2014 an earlier journal study was missed by the retrieval, Section 8.4) [[10.1016/j.ensm.2026.104983]]'],
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

TABLE_STD = {
 'caption': 'Table 10 Mapping BMS functions to requirements in UN GTR 20 (Amendment 1 thermal-propagation provisions, ECE/TRANS/WP.29/GRSP/2026/4), GB 38031-2020/2025, ISO 26262:2018 with ISO/PAS 8800:2024, and ISO 21448 (SOTIF): what deployed ML components must be able to evidence. Regulatory statuses are stated as of 18 October 2026; throughout the table, a \u2018strong protocol\u2019 means the protocol-only definition of Section 2.5 (cross-cell, cross-chemistry, or cross-domain holdout, or online/real-vehicle demonstration). The mapping is this review\u2019s synthesis at requirement level (not clause-level legal citation); the right-hand column gives the corresponding classified-subset primary-paper counts from Section 3.4.',
 'header': ['BMS function', 'What the standard demands of a deployed function', 'Current subset status'],
 'widths': [1.0, 2.1, 1.9],
 'rows': [
  ['SOC estimation',
   'ISO 26262:2018 treats estimation error that can enable overcharge/overdischarge as an E/E-system safety hazard to be handled through the safety lifecycle; ISO/PAS 8800:2024 extends this to learned elements (assurance argument over data, model, and known insufficiencies); UN GTR 20 / GB 38031-2025 treat overcharge as an abuse-protection requirement [[std:unece-gtr20]][[std:gb38031-2025]][[std:iso26262]]',
   '3 of 13 SOC primary papers use a strong isolation protocol; none validate on real-vehicle data; 12 rest on laboratory-scale data'],
  ['SOH / RUL prognosis',
   'Capacity and power fade margins underpin thermal-propagation early warning and end-of-service decisions; degradation assumptions must hold across chemistry, duty, and environment (ISO 26262 hazard analysis; ISO 21448 for performance limitations [[std:iso21448]])',
   '20 of 32 SOH/RUL primary papers use a strong protocol; 4 use real-vehicle data; accuracy claims rest mostly on three public benchmarks (23 primary papers in the subset)'],
  ['Fault detection',
   'Thermal-propagation containment and early warning must both be evidenced: GB 38031-2025 requires that after single-cell thermal runaway the pack or system neither fire nor explode over a two-hour observation window, that a thermal-event alarm still be issued, and that smoke not harm occupants \u2014 superseding GB 38031-2020\u2019s five-minute pre-fire alarm; the GTR 20 Amendment 1 proposal (ECE/TRANS/WP.29/GRSP/2026/4) carries a \u22655-min advance-warning requirement before cabin hazards, with test or risk-management compliance options [[std:unece-gtr20-amd1]]; coverage must be argued and audited (ISO/PAS 8800 assurance argument [[std:isopas8800]])',
   '2 of 7 fault/safety primary papers validate online on fleet data; detection-latency and false-alarm distributions are rarely reported'],
  ['Charging control',
   'Overcharge, over-temperature, and thermal-cycling limits are hard constraints under GB 38031-2020/2025; adaptive strategies must be bounded by protection envelopes and argued in the safety case',
   '0 of 8 charging primary papers use a strong protocol; 4 demonstrate on laboratory hardware, none online'],
  ['Thermal management',
   'Temperature-gradient and propagation-containment requirements after fast-charge or abuse (GB 38031-2025 thermal diffusion, bottom-impact, fast-charge-cycle tests); the cooling function must be verified on hardware',
   '0 of 7 thermal primary papers use a strong protocol; 2 exercise laboratory hardware; no learned control loop is validated on hardware'],
 ],
}

TABLE_POSITION = {
 'caption': 'Table 12 Position relative to prior reviews. \u201cPrasanna 2026\u201d denotes the 2026 performance-centric ML review of EV powertrains with BMS and charging scope (240 studies, included from 361 screened records; aggregated reported RMSE/R\u00b2). The function-specific and method-specific reviews named in Section 1.3 cover single functions or methods, so none of them, to our knowledge, addresses the axes below; the comparison is per axis, not per review. This review differs most in the validation measurement (within a curated subset), standards linkage, and released record-level artifacts.',
 'header': ['Axis', 'This review', 'Prior cross-functional / powertrain reviews'],
 'widths': [0.9, 1.95, 2.15],
 'rows': [
  ['Corpus', 'Two-tier: 799 rule-based eligible records + 103 classified subset', 'Fixed study lists; no record-level selection provenance in the works we examined'],
  ['Validation analysis', 'Protocol classes defined, per-paper assignments released, method-family contrast tested with sensitivity ranges; within-corpus measurement, not a field census', 'Narrative remarks on data scarcity; protocol strength not quantified, to our knowledge'],
  ['Standards linkage', 'Function-to-requirement mapping vs. UN GTR 20, GB 38031-2020/2025, ISO 26262:2018, ISO/PAS 8800:2024', 'Not addressed or addressed qualitatively'],
  ['Recommendations', 'Twelve-item reporting checklist (BMS-ML-RC) + six research directions', 'General future-work statements'],
  ['Reproducibility', 'Released papers.csv, screening provenance, codebook, and statistics scripts', 'No released record-level dataset that we could locate'],
 ],
}

TABLE_GAPS = {
 'caption': 'Table 11 Structural research gaps and corresponding future directions',
 'header': ['Gap', 'Evidence in corpus', 'Future direction'],
 'widths': [1.15, 2.55, 2.7],
 'rows': [
  ['Validation practice', '17 of 88 primary papers use within-cell or k-fold validation; 8 of 88 primary papers demonstrate online or fleet use', 'Standardized cross-cell, cross-chemistry, lab-to-fleet transfer protocols as reporting norms'],
  ['Two-pole data fragmentation', '23 primary papers on three public benchmarks; 36 on rarely released private laboratory cells', 'Federated learning, anonymized fleet-data releases, multi-institution cycling campaigns'],
  ['Onboard deployment', 'Few studies treat compute/memory/latency as design constraints', 'Quantization-aware training, resource-constrained NAS, cloud\u2013edge hybrid estimation'],
  ['Trust and certification', 'Interpretability mostly post-hoc; uncertainty rarely calibrated', 'Calibrated uncertainty, analytically specified hybrid architectures, safety-case methodology'],
  ['Foundation-model integration', 'First two LLM-based studies appear 2025\u20132026 in the subset', 'Grounded LLM orchestration layers; domain foundation models; division of safety authority'],
  ['Under-served functions', 'Balancing: smallest core function in subset (2 papers) and pool (38 of 799 tagged); closed-loop thermal control not yet shown on hardware', 'Certifiable adaptive control with mechanism-aware safety envelopes'],
 ],
}


TABLE_METH = {
 'caption': 'Table 2 Method families: representative techniques, strengths, and limitations. Counts are the 88 primary-application papers; the three review-type syntheses coded under a method family plus the 12 method-family reviews are accounted for in the function-by-year composition table.',
 'header': ['Method family', 'Papers', 'Representative techniques', 'Strengths', 'Limitations'],
 'widths': [1.15, 0.5, 1.8, 1.55, 1.5],
 'rows': [
  ['Classical ML', '28', 'Gaussian process regression, SVM/SVR, ensembles, shallow networks on engineered features', 'Calibrated uncertainty; small-data friendly; cheap to embed', 'Feature engineering is manual; ceilings under complex dynamics'],
  ['Deep learning', '19', 'LSTM/GRU, CNN, attention/Transformer, autoencoders, graph networks', 'Learns features from raw curves; strong trajectory modeling', 'Data-hungry; weak extrapolation; opaque'],
  ['Physics-informed / hybrid', '22', 'PINNs, physics-constrained autoencoders, filter-embedded networks, multiphysics fusion', 'Structure aids extrapolation; reduced data demand', 'Inherits simplified-model bias; harder to train'],
  ['Optimization-augmented', '11', 'Bayesian optimization, surrogate-assisted multi-objective design, meta-heuristic-tuned networks', 'Sample-efficient protocol discovery; explicit trade-off handling', 'Offline tuning cost; surrogate bias'],
  ['Transfer / domain adaptation', '5', 'Domain-adversarial training, fine-tuning across chemistry/protocol', 'Directly targets the generalization gap', 'Negative transfer; needs shared protocols'],
  ['Reinforcement / control learning', '1', 'Deep-RL prognostic model selection (also an embedded component in further studies)', 'Adaptive decision-making along trajectories', 'Training stability; scarce hardware validation'],
  ['Foundation models / LLM', '2', 'LLM incident-risk analysis; LLM-based SOH estimation with uncertainty-gated physics fallback', 'Reasoning over heterogeneous text/system context; transferable priors', 'Hallucination risk; latency and cost'],
  ['Review / perspective', '12', 'Narrative and systematic syntheses', 'Maps the field; identifies shared gaps', 'No primary validation'],
 ],
}

TABLE_VALID = {
 'caption': 'Table 5 Validation practices across the corpus',
 'header': ['Validation approach', 'Papers', 'Interpretation'],
 'widths': [1.9, 0.6, 3.9],
 'rows': [
  ['Cross-cell holdout', '24', 'Strongest common laboratory protocol; unseen sibling cells'],
  ['Experimental hardware', '20', 'Physical validation of estimator or controller behavior'],
  ['Review synthesis', '15', 'No primary validation applicable'],
  ['Within-cell split', '12', 'Can be optimistic; trajectory leakage between train and test'],
  ['Online / real-vehicle', '8', 'Deployment-relevant evidence; rarest strong protocol'],
  ['Cross-chemistry holdout', '7', 'Strictest generalization demand in corpus'],
  ['k-fold cross-validation', '5', 'Can be optimistic without cell-level isolation'],
  ['Simulation (+ hardware spot-check)', '8', 'Model-fidelity dependent; strongest when hardware-checked'],
  ['Cross-domain holdout', '3', 'Transfer-specific evidence'],
  ['Case study', '1', 'Single-system demonstration'],
 ],
}


TABLE_FLEET = {
 'caption': 'Table 6 Cross-tabulation of fleet-data use against online validation (103 classified papers). Fleet-data use describes the primary data source; online validation describes the validation protocol; their overlap is 8 of 10 fleet-data papers. A laboratory-data online demonstration was recoded to experimental hardware after full-text re-check (per the codebook’s absorbing rule: each paper is credited with the strongest protocol its full text reports for its headline claim, and a stronger claim unsupported at full-text re-check absorbs into the weaker class that is evidenced — Box 2). The right-hand column pools the environment-only validation categories defined with the classification framework.',
 'header': ['', 'Online / real-vehicle validation', 'All other validation protocols', 'Total papers'],
 'rows': [
  ['Real-vehicle / fleet data', '8', '2 (cross-domain holdout; case study)', '10'],
  ['Other data sources', '0', '93', '93'],
  ['Total', '8', '95', '103'],
 ],
}


TABLE_CONF = {
 'caption': 'Table 7 Conference-path descriptive set: all 14 battery papers retrieved from control and transportation-electrification venues (2019\u20132025), Crossref-verified, with validation evidence stated in their indexed abstracts. The pre-stated inclusion rule (machine learning as a substantive component of the contribution) retains 8 of the 14 for the learning-path comparison; the remainder are conventional model-based estimators or an overview and are retained here for transparency.',
 'header': ['Venue (year)', 'Function', 'Method (short)', 'Learning-based?', 'Validation evidence stated in indexed abstract'],
 'widths': [0.95, 0.85, 2.0, 0.75, 1.85],
 'rows': [
  ['ITEC 2019', 'SOC', 'LSTM recurrent network with transfer learning [[10.1109/itec.2019.8790543]]', 'Yes', 'Not stated'],
  ['VPPC 2019', 'SOC', 'SVR + PCA with dual-polarization model [[10.1109/vppc46532.2019.8952458]]', 'Yes', 'Not stated'],
  ['VPPC 2019', 'SOC', 'Kalman filter on reduced electrochemical model [[10.1109/vppc46532.2019.8952284]]', 'No (model-based)', 'Simulation-level'],
  ['ACC 2021', 'SOC', 'Multiple-model adaptive estimation [[10.23919/acc50511.2021.9482734]]', 'No (model-based)', 'Simulation-level'],
  ['VPPC 2021', 'SOC', 'Computationally efficient neural network [[10.1109/vppc53923.2021.9699201]]', 'Yes', 'Simulation-level'],
  ['VPPC 2021', 'SOH', 'ML ensemble [[10.1109/vppc53923.2021.9699273]]', 'Yes', 'Public dataset'],
  ['ECC 2021', 'SOH', 'Reinforcement learning + observer [[10.23919/ecc54610.2021.9655199]]', 'Yes', 'Not stated'],
  ['CCDC 2022', 'SOH', 'CNN-BiLSTM transfer learning [[10.1109/ccdc55256.2022.10033695]]', 'Yes', 'Hardware (stated); public data'],
  ['VPPC 2022', 'Prognostics', 'ML on aging data [[10.1109/vppc55846.2022.10003444]]', 'Yes', 'Hardware (stated)'],
  ['ITEC 2022', 'SOC+SOH', 'Dual extended Kalman filter [[10.1109/itec53557.2022.9813961]]', 'No (model-based)', 'Not stated'],
  ['ACC 2023', 'SOC+SOH', 'Real-time estimator + batch least squares [[10.23919/acc55779.2023.10156326]]', 'No (model-based)', 'Not stated'],
  ['APEC 2023', 'Overview', 'Review of ML-enabled estimation [[10.1109/apec43580.2023.10131605]]', 'Overview', 'Not applicable'],
  ['ITEC 2023', 'SOH', 'Histogram data + PCA + regression [[10.1109/itec55900.2023.10187012]]', 'Yes', 'Public dataset'],
  ['ACC 2024', 'SOC+SOH', 'EKF critique and improvement [[10.23919/acc60939.2024.10644628]]', 'No (model-based)', 'Simulation-level'],
 ],
}

TABLE_LLM = {
 'caption': 'Table 9 Safety and verification taxonomy for foundation-model components in the BMS stack. The right-hand column is normative guidance proposed by this review, not claims about the published studies.',
 'header': ['Dimension', 'Classical / deep ML estimators (established practice)', 'Published LLM studies (2025\u20132026)', 'Required guardrail (this review)'],
 'widths': [1.0, 1.9, 1.8, 1.8],
 'rows': [
  ['Role in the stack', 'Calibrated numeric estimation and detection', 'Stationary-BESS incident risk analysis [[10.1016/j.ress.2026.112416]]; LLM-based SOH estimation with uncertainty-aware control on field vehicle data [[10.1016/j.ensm.2026.104983]]', 'Estimation should belong to calibrated ML; the LLM SOH estimator of [[10.1016/j.ensm.2026.104983]] is the earliest in the classified subset \u2014 an earlier journal-published LLM estimator, missed by this review\u2019s retrieval, is [[10.1109/tec.2025.3548400]] (Section 8.4) \u2014 and must show calibrated intervals before any actuation-adjacent role'],
  ['Grounding', 'Trained on domain cycling data', 'Domain-tuned corpora and knowledge-enhanced prompting', 'Retrieval over verified corpora with source citations; no ungrounded recall'],
  ['Dominant failure mode', 'Bounded numeric error under distribution shift', 'Open-ended hallucinated text', 'Outputs restricted to structured, checkable forms; never free text into protection logic'],
  ['Uncertainty', 'Gaussian-process / conformal intervals in a subset of studies', 'Not reported for incident risk analysis [[10.1016/j.ress.2026.112416]]; Monte-Carlo uncertainty estimates with selective physics-estimator substitution demonstrated in the SOH estimator [[10.1016/j.ensm.2026.104983]]', 'Calibrated intervals mandatory before any actuation-adjacent role'],
  ['Latency and compute', 'Millisecond-class, onboard', 'Second-class, cloud-dependent', 'Offline analysis and planning only unless real-time evidence is shown'],
  ['Safety authority', 'Bounded by physics envelopes and thresholds', 'Undefined in published studies', 'LLM components must never hold direct cell-level protection authority'],
 ],
}

TABLE_CHECKLIST = {
 'caption': 'Table 13 Proposed BMS-ML reporting checklist (BMS-ML-RC), modeled on CONSORT/PRISMA reporting standards.',
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
