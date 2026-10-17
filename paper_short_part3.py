#!/usr/bin/env python3
"""Condensed TTE-submission text (12-page limit): part 3."""
import paper_part3 as FULL

TABLES = {
    'TABLE_METH': FULL.TABLE_METH,
    'TABLE2': FULL.TABLE2,
    'TABLE_FLEET': FULL.TABLE_FLEET,
    'TABLE_REP': FULL.TABLE3,
    'TABLE_LLM': FULL.TABLE_LLM,
    'TABLE_STD': {
 'caption': "Mapping BMS functions to requirements in UN GTR 20 (Amendment 1 thermal-propagation provisions), GB 38031-2020/2025, ISO 26262:2018 with ISO/PAS 8800:2024, and ISO 21448 (SOTIF): what deployed ML components must be able to evidence. Regulatory statuses are stated as of the September 2026 retrieval date, and a \u2018strong protocol\u2019 in the subset-status column follows the protocol-only definition of Section II-C (cross-cell, cross-chemistry, or cross-domain holdout, or online/real-vehicle demonstration). The mapping is this review's synthesis at requirement level (not clause-level legal citation); \u201csubset status\u201d gives the corresponding classified-subset primary-paper counts from Section III-C.",
 'header': ['BMS function', 'What the standard demands of a deployed function', 'Current subset status'],
 'widths': [1.0, 2.1, 1.9],
 'rows': [
  ['SOC estimation',
   'ISO 26262:2018 treats estimation error that can enable overcharge/overdischarge as an E/E-system safety hazard to be handled through the safety lifecycle; ISO/PAS 8800:2024 extends this to learned elements (assurance argument over data, model, and known insufficiencies); UN GTR 20 / GB 38031-2025 treat overcharge as an abuse-protection requirement',
   '3 of 13 SOC primary papers use a strong isolation protocol; none validate on real-vehicle data; 12 rest on laboratory-scale data'],
  ['SOH / RUL prognosis',
   'Capacity and power fade margins underpin thermal-propagation early warning and end-of-service decisions; degradation assumptions must hold across chemistry, duty, and environment (ISO 26262 hazard analysis; ISO 21448 for performance limitations)',
   '20 of 32 SOH/RUL primary papers use a strong protocol; 4 use real-vehicle data; accuracy claims rest mostly on three public benchmarks (23 primary papers in the subset)'],
  ['Fault detection',
   'Thermal-propagation early warning must provide the escape window: GB 38031-2025 requires a thermal-propagation warning ahead of hazard and no fire or explosion of the pack beyond the triggered cell, superseding GB 38031-2020\u2019s five-minute pre-warning criterion; the GTR 20 Amendment 1 proposal (EVS-30-C01/Rev.4) carries a \u22655-min advance warning before cabin hazards, with test or risk-management compliance options; coverage must be argued and audited (ISO/PAS 8800 assurance argument)',
   '2 of 7 fault/safety primary papers validate online on fleet data; detection-latency and false-alarm distributions are rarely reported'],
  ['Charging control',
   'Overcharge, over-temperature, and thermal-cycling limits are hard constraints under GB 38031-2020/2025; adaptive strategies must be bounded by protection envelopes and argued in the safety case',
   '0 of 8 charging primary papers use a strong protocol; 4 demonstrate on laboratory hardware, none online'],
  ['Thermal management',
   'Temperature-gradient and propagation-containment requirements after fast-charge or abuse (GB 38031-2025 thermal diffusion, bottom-impact, fast-charge-cycle tests); the cooling function must be verified on hardware',
   '0 of 7 thermal primary papers use a strong protocol; 2 exercise laboratory hardware; no learned control loop is validated on hardware'],
 ],
},
 'TABLE_POSITION': {
 'caption': "Position relative to prior reviews. \u201cPrasanna 2026\u201d denotes a 2026 performance-centric ML review of EV powertrains with BMS and charging scope. The function-specific and method-specific reviews named in Sections I\u2013II cover single functions or methods, so none of them, to our knowledge, addresses the axes below; here the comparison is per axis, not per review. This review differs most in the validation measurement (within a curated subset), standards linkage, and released record-level artifacts.",
 'header': ['Axis', 'This review', 'Prior cross-functional / powertrain reviews'],
 'widths': [0.9, 1.95, 2.15],
 'rows': [
  ['Corpus', 'Two-tier: 799 rule-based eligible records + 103 classified subset', 'Fixed study lists; no record-level selection provenance in the works we examined'],
  ['Validation analysis', 'Protocol classes defined, per-paper assignments released, method-family contrast tested with sensitivity ranges; within-corpus measurement, not a field census', 'Narrative remarks on data scarcity; protocol strength not quantified, to our knowledge'],
  ['Standards linkage', 'Function-to-requirement mapping vs. UN GTR 20, GB 38031-2020/2025, ISO 26262:2018, ISO/PAS 8800:2024', 'Not addressed or addressed qualitatively'],
  ['Recommendations', 'Twelve-item reporting checklist (BMS-ML-RC) + six research directions', 'General future-work statements'],
  ['Reproducibility', 'Released papers.csv, screening provenance, codebook, and statistics scripts', 'No released record-level dataset that we could locate'],
 ],
},
    'TABLE_CHECKLIST': {
 'caption': 'Proposed BMS-ML reporting checklist (BMS-ML-RC), modeled on CONSORT/PRISMA reporting standards. Items 4, 5, and 11 derive from the validation-protocol classes defined in Section II-C and measured in the classified subset; item 12 is the artifact-availability norm this paper itself follows. The checklist as a whole has not been score-audited across all 103 classified papers \u2014 it is a proposal, not a survey result.',
 'header': ['#', 'Reporting item \u2014 what must be reported'],
 'widths': [0.35, 3.0],
 'single_col': True,
 'rows': [
  ['1', 'Dataset identity \u2014 exact name and version of every dataset (e.g., Severson-MATR, NASA, CALCE); download source'],
  ['2', 'Cell population \u2014 number of cells, chemistry, manufacturer, format, and batch for every training and test set'],
  ['3', 'Sensor and sampling context \u2014 measured channels, sampling rate, sensor class, temperature conditions'],
  ['4', 'Split protocol \u2014 split type (within-cell / cross-cell / cross-chemistry / cross-domain) and isolation argument'],
  ['5', 'Out-of-distribution evaluation \u2014 at least one protocol where test conditions differ from training'],
  ['6', 'Baselines \u2014 at least one classical baseline alongside the proposed architecture, on identical data'],
  ['7', 'Randomness control \u2014 seeds or repeated-run statistics for every stochastic result'],
  ['8', 'Uncertainty \u2014 calibrated intervals or error bars for headline claims, not point estimates alone'],
  ['9', 'Compute budget \u2014 training compute and inference latency/memory on the target platform'],
  ['10', 'Failure analysis \u2014 at least one documented failure mode and its distribution'],
  ['11', 'Validation environment \u2014 simulation, laboratory cycling, hardware prototype, or online/fleet'],
  ['12', 'Artifact availability \u2014 data and code deposit (DOI-backed) or an explicit stated exemption'],
 ],
}
}


BLOCKS = [
('h1', '8. Cross-Cutting Directions'),

('h2', '8.1 Physics-informed learning, interpretability, and uncertainty'),
('p',
 "Physics-informed and hybrid model\u2013data learning is the classified subset's fastest-growing methodological theme (22 primary-application "
 "papers across all functions; Table I) \u2014 in state estimation [[10.1109/jrfid.2022.3211841]][[10.1016/j.measurement.2025.118985]], heat-generation estimation "
 "[[10.1016/j.jechem.2022.11.036]], prognostics [[10.1016/j.ymssp.2022.109347]], and impedance-based diagnostics \u2014 consolidated by a physics-informed EIS-diagnostics review "
 "[[10.1016/j.rser.2023.113807]] \u2014 with physics-constrained autoencoders improving health prediction over purely learned counterparts "
 "[[10.1007/s00521-022-07291-5]] and a reviewed physical-plus-data-driven fusion literature for internal-state estimation "
 "[[10.3390/batteries10120442]]. "
 "The caution is that most physics-informed studies embed simplified physics \u2014 equivalent-circuit or reduced electrochemical models \u2014 so the "
 "hybrid inherits model bias even as it gains structure, and its validation is no stronger than that of purely data-driven peers (Section III-C). "
 "A smaller but consequential cluster makes learning systems inspectable: explainability-driven feature selection improves estimator robustness "
 "[[10.1016/j.ress.2022.109046]], interpretable ML links manufacturing coating parameters to cell capacity "
 "[[10.1016/j.conengprac.2022.105202]], interpretable hybrid ML untangles degradation chemistries in lithium\u2013sulfur cells "
 "[[10.1002/anie.202214037]], and uncertainty-aware models deliver calibrated early-life predictions [[10.1039/d2dd00067a]]. For safety cases "
 "only calibrated uncertainty has a route into certification; attribution supports debugging."),

('h2', '8.2 Digital twins, cloud BMS, and new sensing'),
('p',
 "System-level architecture is emerging as a research object: digital twins track individual battery aging through incremental learning "
 "[[10.1016/j.eswa.2023.120444]] and couple LSTM surrogates with real-time thermal observation [[10.1016/j.est.2023.107203]]; cloud platforms "
 "perform in-situ life prediction at fleet scale [[10.1016/j.ensm.2023.02.035]]; second-life workflows use impedance-based accelerated SOH "
 "estimation to triage retired packs [[10.1016/j.est.2022.106295]], and learned battery models with numerical search estimate real-time "
 "state-of-power [[10.1016/j.est.2026.123023]]. Non-electrical sensing broadens the measurement base \u2014 ultrasonic signatures provide a SOC "
 "channel orthogonal to voltage sensing [[10.1016/j.egyai.2022.100188]] \u2014 and ML mappings from equivalent-circuit parameters to "
 "electrochemical properties give classical BMS models a physically interpretable learned layer [[10.1016/j.est.2024.113257]]. These settings "
 "differ in latency budgets, error tolerance, and update cadence, and the field is beginning to design for those differences. Production-side "
 "mapping review [[10.1002/batt.202300046]], coating interpretability [[10.1016/j.conengprac.2022.105202]], and defect detection "
 "[[10.1016/j.jechem.2025.04.025]] complete the picture: cell quality is itself a BMS input."),

('h2', '8.3 Foundation models and LLM-based management'),
('p',
 "The classified subset's youngest theme is generative, and it arrives with a prior-art caveat: LLM-based battery state estimation already exists beyond this corpus: "
 "a 2025 IEEE Transactions on Energy Conversion letter [[10.1109/tec.2025.3548400]] that this review's Crossref retrieval failed to "
 "return \u2014 a recall miss, not a venue exclusion \u2014 so no study in this corpus can claim to be the first of its kind. Within the subset the published studies are of two distinct kinds: a domain-specific LLM "
 "for risk analysis of battery *energy-storage-system* incidents \u2014 station-side rather than onboard technology \u2014 "
 "[[10.1016/j.ress.2026.112416]], and HA-LLM, which crosses the estimation boundary by using field vehicle data to estimate SOH with "
 "uncertainty-aware control, coordinating vehicle and cloud [[10.1016/j.ensm.2026.104983]]. The honest framing of [[10.1016/j.ensm.2026.104983]] "
 "matters for everything that follows: LLM-based estimation is no longer hypothetical \u2014 what remains normative is the claim that before any "
 "LLM-based estimator feeds actuation, it must publish calibrated intervals, structured outputs, and a latency budget, and it must not hold "
 "direct cell-level protection authority; that role belongs to physics-based envelopes and calibrated numeric estimators. Table V makes this "
 "division of labor explicit; its right-hand column is guidance proposed here, not claims about the published studies."),

('tbl', 'TABLE_LLM'),

('h1', '9. Research Gaps, Reporting Standards, and Future Directions'),
('p',
 "Cross-referencing the bibliometric analysis of Section III with the function-level reviews yields six structural gaps. (1) Validation "
 "practice: 17 of the 88 primary papers use within-cell or unsupervised k-fold validation, and only 8 of the 88 primary papers (every online "
 "demonstration in the subset is a primary application) evaluate online or on fleets; standardized cross-cell, cross-chemistry, and lab-to-fleet transfer protocols should become reporting norms, as already practiced by the "
 "transfer-learning and general-framework studies [[10.1016/j.apenergy.2024.125086]][[10.1109/tte.2025.3533540]]. (2) Two-pole data "
 "fragmentation: the three public benchmarks sustain 23 primary papers and 36 rest on private laboratory cells that are rarely released; "
 "federated learning over fleets, anonymized fleet-data releases, and multi-institution cycling campaigns \u2014 in the spirit of the 179-cell "
 "pipeline [[10.1038/s42256-021-00312-3]] \u2014 would diversify the evidence base, and papers should at minimum disclose split definitions, "
 "seeds, and compute budgets. (3) Edge deployment: only isolated works treat onboard compute, memory, and latency as first-class constraints "
 "[[10.1016/j.est.2022.104901]][[10.1016/j.jpowsour.2025.236784]]; quantization-aware training, resource-constrained architecture search, and "
 "cloud\u2013edge hybrid designs are the natural research program. (4) Trust: uncertainty must be calibrated rather than post-hoc "
 "[[10.1039/d2dd00067a]], interpretability must bound behavior rather than merely attribute it, and hybrid physics\u2013data architectures are "
 "the most credible certification path because part of their behavior is analytically specified. (5) Foundation-model integration: an "
 "LLM-based estimator [[10.1016/j.ensm.2026.104983]] and the risk-analysis LLM [[10.1016/j.ress.2026.112416]] suggest a division of labor \u2014 "
 "foundation models for reasoning and orchestration, conventional ML for calibrated estimation, physics models for safety envelopes \u2014 that "
 "should be formalized with grounding and latency guarantees. (6) Under-served functions: balancing is nearly untouched beyond pack-level "
 "insight [[10.1016/j.est.2023.106931]], charging needs certifiable adaptive protocols, and thermal management remains simulation-dominated "
 "[[10.1016/j.est.2023.106688]]; these are control problems where errors act on the battery, so closing them requires the safety-case machinery "
 "of gap 4 as much as new algorithms. Two follow-on subsections turn these gaps outward \u2014 first to what the automotive safety standards "
 "actually demand of these functions, then to how the emerging 2027\u20132030 research directions map onto them."),

('h2', '9.1 From corpus gaps to safety-standard requirements'),  # heading kept; body text uses subset wording
('p',
 "The standards invoked in Section I \u2014 UN GTR No. 20 (electric-vehicle safety, established in the Global Registry in 2018 [[std:unece-gtr20]]; Amendment 1, proposed as document EVS-30-C01/Rev.4 in September 2025 [[std:unece-gtr20-amd1]] and listed for adoption at the November 2026 WP.29 session at this "
 "review's retrieval date, adds thermal-propagation provisions with two compliance options: a physical propagation test or a documented risk-management approach "
 "), GB 38031 (GB 38031-2020, now superseded, and the strengthened GB 38031-2025 [[std:gb38031-2025]], effective "
 "July 2026, which replaces the fire/explosion-warning criterion with no-fire/no-explosion thermal-diffusion requirements and adds bottom-"
 "impact and fast-charge-cycle tests), ISO 26262:2018 (functional safety of road-vehicle E/E systems [[std:iso26262]]), ISO/PAS 8800:2024 (safety and "
 "artificial intelligence \u2014 the road-vehicle extension of ISO 26262 and ISO 21448 to learned components [[std:isopas8800]]), and ISO 21448 (SOTIF [[std:iso21448]]) \u2014 do "
 "not prescribe estimation algorithms, but they define what a deployed estimator or controller must be able to evidence, and Table VI "
 "translates the subset's gaps into those terms. The mapping is this review's synthesis at requirement level rather than clause level, and it "
 "is stated so that it can be checked against the standards texts themselves: the point is not legal advice but that a validation protocol "
 "reported in a paper corresponds, or does not, to evidence a safety case can use. The inference rule behind every ``supports a standards "
 "argument'' statement in this section is explicit: a paper's evidence can support such an argument only if it demonstrates performance on "
 "at least one held-out integration unit (a cross-cell holdout or stronger isolation protocol) and reports the environment in which that "
 "evidence was obtained; by construction, within-cell and k-fold evidence cannot support the argument, because the safety case is about "
 "unseen cells and unseen duty. Three consequences stand out for automotive deployment. "
 "Within-cell and k-fold validation (17 primary papers) cannot support an ISO 26262 argument, because the safety case is about unseen cells "
 "and unseen duty and the protocol never tests an unseen unit; a standards argument must therefore be *argued* from the isolation evidence, "
 "not *asserted* from headline accuracy. Thermal-propagation early-warning latency is a timing requirement, so fault-detection papers "
 "evaluated on curated laboratory windows under-report both the false-alarm rate and the detection-delay distribution the GB 38031-2025 / "
 "GTR-20 escape window needs. And charging or thermal control strategies validated only in simulation lack the hardware-in-the-loop evidence "
 "base an automotive release process expects. The reporting checklist below (Table VIII) is deliberately aligned with this mapping \u2014 "
 "reporting an isolation argument and a validation environment is the minimum on which any standards conversation can start."),

('tbl', 'TABLE_STD'),

('h2', '9.2 Position relative to prior reviews'),
('p',
 "The closest in scope among recent reviews is the performance-centric review of Prasanna et al. [[10.1007/s44163-025-00721-y]], which "
 "examines 240 peer-reviewed publications (from 361 initially retrieved records) spanning the whole EV powertrain \u2014 battery management alongside charging systems, "
 "motor control, and energy-consumption prediction \u2014 and aggregates reported performance metrics (RMSE, R\u00b2) into a quantitative "
 "benchmarking of algorithm families, concluding that hybrid deep-learning architectures (LSTM-DDQN, CNN-BiGRU, transformer-based frameworks) "
 "consistently achieve superior accuracy (R\u00b2 > 0.95, RMSE < 0.05). This review differs from that work in scope, unit of analysis, and "
 "question asked. In scope, it is narrower and deeper \u2014 battery-management functions only \u2014 which permits function-level cuts such as the "
 "standards mapping of Section IX-A and the per-function validation audit. In unit of analysis, it is protocol-centric rather than "
 "performance-centric: instead of pooling reported accuracy figures, it codes how each study\u2019s validation protocol isolates (or fails to "
 "isolate) its generalization claim. The two approaches are complementary, and the complementarity is pointed: an aggregation of self-reported "
 "RMSE and R\u00b2 may inherit, unmeasured, the validation weaknesses this review quantifies within its own subset \u2014 there, 17 of 88 primary papers validate on "
 "information-leaking splits, and headline accuracies concentrate on three shared benchmarks \u2014 so where Prasanna et al. answer *which "
 "algorithm family performs best as reported*, this review asks *how much the reports can be trusted, and what a study must disclose for its "
 "claims to be checkable*. Adjacent cross-functional surveys exist for degradation and estimation methods; Table VII states the comparison "
 "axis by axis across all of them: a two-tier corpus with record-level screening provenance, a within-corpus measurement of validation "
 "protocol strength across functions, a standards-grounded gap analysis, and a released, re-run-able analysis pipeline. Where prior reviews "
 "ask \u201cwhich method works best for function X,\u201d this review asks \u201cwhich claims can actually be "
 "checked \u2014 and what would it cost the reader to trust them,\u201d which is the question a scoping review with a curated classified subset is "
 "positioned to answer, and the question that performance-centric aggregation cannot ask of itself."),

('tbl', 'TABLE_POSITION'),

('h2', '9.3 Outlook: what the next revision cycle of this literature should produce'),
('p',
 "Concretely, and tied to the gaps above, the highest-value near-term work falls in six directions. (a) *Duty-cycle-aware validation*: public "
 "cross-cell benchmarks that pair cycling data with recorded EV drive profiles, so that cross-chemistry and cross-domain generalization can be "
 "tested against transportation duty rather than laboratory schedules; (b) *federated fleet evidence*: privacy-preserving SOH/SOC studies over "
 "live fleets (\u22482% of the eligible corpus today), with the 179-cell pipeline as the template; (c) *benchmark diversification*: "
 "multi-institution cycling campaigns two orders of magnitude larger than MATR/NASA/CALCE and released with DOI-backed artifacts, addressing "
 "the two-pole fragmentation of Section III-C; (d) *pack- and vehicle-level ML*: estimation validated at the integration level where UN GTR 20 "
 "and GB 38031 requirements bite, instead of cell-level evidence transplanted upward; (e) *functionally safe learning*: ML estimators whose "
 "uncertainty handling and assurance arguments are specified against ISO 26262 safety goals and ISO/PAS 8800, with ISO 21448/SOTIF reasoning for "
 "capability limitations, making certifiable charging and thermal control reachable; and (f) *honest foundation-model integration*: "
 "retrieval-grounded LLM agents with published latency and calibration budgets, capable of the coordination role while estimation authority "
 "stays with calibrated numeric models \u2014 extending, not contradicting, the corpus's LLM estimator [[10.1016/j.ensm.2026.104983]]. A "
 "guardrail on all six directions: the BMS-ML-RC checklist below is designed to be attached to a paper at submission, so the next revision "
 "cycle of this literature arrives auditable by construction."),

('h2', '9.4 A reporting checklist for machine-learning BMS studies'),
('p',
 "The most concrete artifact this review can offer is procedural. Modeled on the CONSORT and PRISMA checklists, Table VIII proposes a "
 "twelve-item BMS-ML reporting checklist (BMS-ML-RC): the minimum metadata a study should disclose for its accuracy claims to be comparable, "
 "reproducible, and poolable \u2014 and, per Section IX-A, admissible in a safety discussion. Its derivation is explicit: items 4, 5, and 11 "
 "operationalize the validation-protocol classes defined in Section II-C and measured in the classified subset; items 1\u20133 and 6\u201310 "
 "respond to the reporting omissions observed across Sections III\u2013VIII; item 12 is the artifact-availability norm this paper itself "
 "follows. What the checklist is and is not: it is a proposal grounded in the classified subset's measured weaknesses, not a community-"
 "validated instrument \u2014 no Delphi or expert-consensus process was run for it, only three items are score-measured in this corpus, and it "
 "has not been applied as an audit to all 103 studies. The review's own reporting follows the PRISMA-ScR flow structure (Fig. 2), but the "
 "protocol was not prospectively registered; where this section says a practice *should* be reported, that is a recommendation supported by "
 "the evidence above, and we suggest journals consider it as a submission checklist."),
('tbl', 'TABLE_CHECKLIST'),


('h1', '10. Conclusion'),
('p',
 "This review has examined machine learning in battery management on a two-tier evidence base: a rule-based eligible corpus of 799 journal "
 "articles from which field-level shares are measured within a documented capped retrieval, and an in-depth classified subset of 103 studies "
 "through which method, data, and validation practice are examined with a 30-paper blind reliability check and label-noise sensitivity "
 "ranges. Three conclusions stand out. First, within the classified subset, method families have shifted from classical feature-based "
 "learners to deep sequence models and now physics-informed hybrids, with LLM-based studies appearing from 2025\u20132026 \u2014 though "
 "LLM-based battery estimation began in other venues. Second, the center of gravity is estimation at cell level: measured as shares of the "
 "eligible corpus, the SOC\u2013SOH\u2013prognostics union covers about half of eligible records, whereas vehicle- and pack-level "
 "practice remains thin \u2014 precisely the level at which UN GTR 20, GB 38031, and ISO 26262 pose their requirements. Third, the "
 "proliferation of published accuracy claims is not matched by validation progress: only 8 of the 88 primary papers (8 of the 103 "
 "classified studies) demonstrate online or fleet operation, 17 of 88 "
 "primary papers use isolation-weakened splits, and 23 rest on three public benchmarks while 36 rest on private laboratory cells; the "
 "physics-informed validation contrast is directionally consistent under both reported definitions, statistically unestablished and underpowered "
 "(protocol-only 36% versus 52%, p = 0.32; including-hardware 59% versus 74%, p = 0.19), so it is reported as no detectable difference, with meaningful differences in either direction not excluded \u2014 an open hypothesis "
 "rather than a settled result. The near-term agenda follows directly: standardized cross-domain validation, diversified fleet data, pack- "
 "and vehicle-level ML aligned with the standards mapping of Section IX, calibrated uncertainty, and a strict division of labor between "
 "foundation models, calibrated estimators, and physics-based safety envelopes. If the last five years were about discovering what machine "
 "learning can estimate about a battery, the next five will be decided by what it can be trusted to do \u2014 onboard, at fleet scale, across "
 "chemistries, and over full cell lifetimes."),

('decl', None),
]
