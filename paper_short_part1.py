#!/usr/bin/env python3
"""Condensed TTE-submission text (12-page limit): part 1.
Citation coverage mirrors the full manuscript; prose tightened."""

TITLE = "Machine learning in battery management systems: a two-tier scoping review of 799 eligible studies with in-depth classification and validation audit"

AUTHOR_LINES = [("Hussain Touhid Siddiquee", "Leading University, Sylhet, Bangladesh"),
                ("Syeda Salsabil Islam Ariya", "Leading University, Sylhet, Bangladesh"),
                ("Jasimul Islam Chowdhury", "Leading University, Sylhet, Bangladesh")]

ABSTRACT = [
 "Machine learning (ML) has moved from a promising addition to battery research to a load-bearing component of battery management systems (BMS), but the validation practices behind the accuracy claims are rarely examined. A structured scoping review with a two-tier evidence base is presented: an *eligible corpus* of 799 peer-reviewed journal articles admitted by uniform rule-based criteria from a capped 30-query Crossref retrieval (798 dated 2020\u20132026 plus one early-access record stamped 2027), and an in-depth *classified subset* of 103 studies \u2014 98 from that pool plus five individually verified seed studies, one dated 2019 \u2014 coded by function, method family, chemistry, data source, and validation practice. Union-share bibliometrics across the eligible corpus locate the center of gravity of the screened literature in health estimation (SOH), state estimation (SOC), and prognostics (RUL) \u2014 query-tag shares, read for ordering rather than exact rates, with their union share reported in Section III-B \u2014 with charging, thermal management, balancing, and vehicle- or fleet-level work relatively under-served for a transportation-electrification readership. Within the classified subset, three weaknesses recur. Only 8 of 88 primary-application papers evaluate online or on real vehicles; 17 of 88 rely on within-cell or k-fold splits that can leak trajectory information; and the largest single data source is private laboratory cells (36 of 88), a reproducibility constraint at least as limiting as the benchmark concentration (23 papers on three datasets). Validation practice shows no detectable difference between physics-informed/hybrid and purely data-driven papers under either definition of stringency \u2014 an underpowered contrast in which meaningful differences in either direction cannot be excluded \u2014 and symmetric and strong-to-weak label-noise scenarios bracket the strong-protocol share between 11% and 59%, the strong-to-weak floor a worst-case bound rather than an estimate. A post-hoc recall audit against the included reviews\u2019 reference lists bounds what the capped retrieval misses. The paper closes with a requirement-level mapping of BMS functions onto UN GTR 20, GB 38031, and ISO 26262, a positioning against prior reviews, and a twelve-item reporting checklist; all data and code are released.",
]

KEYWORDS = ("machine learning; battery management systems; lithium-ion batteries; state of charge; "
            "state of health; remaining useful life; deep learning; physics-informed neural networks; "
            "transfer learning; battery safety")

BLOCKS = [
('h1', '1. Introduction'),

('h2', '1.1 The battery management problem'),
('p',
 "Lithium-ion batteries now anchor three converging transitions \u2014 electrified road transport, renewable-heavy stationary storage, and the "
 "electrification of aerospace and marine systems \u2014 and in each the battery is an actively managed asset whose usable capacity, lifetime, and "
 "safety depend on real-time operating decisions. The battery management system (BMS) is the embedded cyber-physical layer that makes those decisions "
 "\u2014 sensing, state estimation, protection, balancing, and charging negotiation [[10.1016/j.egyai.2025.100585]]. The difficulty stems from the fact that "
 "the quantities that matter most \u2014 state of charge (SOC), state of health (SOH), internal temperature, and the onset of degradation or fault "
 "mechanisms \u2014 are not directly measurable and must be inferred from noisy, partially observable terminal measurements under widely varying "
 "conditions. Model-based approaches built on equivalent-circuit or electrochemical models face a persistent fidelity-versus-tractability trade-off, "
 "and their parameters drift as cells age [[10.1016/j.joule.2019.11.018]]. It is in this inference-and-decision layer that machine learning has made "
 "its most forceful entry, and the stakes are highest in transportation electrification: electric-vehicle packs face automotive safety "
 "expectations \u2014 UN GTR 20 on board energy storage rechargeable systems, GB 38031 on traction battery safety requirements, and ISO "
 "26262 on functional safety of electric/electronic systems \u2014 that make state estimation, degradation prognosis, and fault detection safety-"
 "relevant BMS functions, not research add-ons. Section IX returns to these three standards and maps each estimation function to the property the "
 "standard actually demands (detection reliability, gradient/temperature limits, protection timing) \u2014 the mapping that turns the validation "
 "findings of this review into vehicle-level stakes."),

('p',
 "Machine learning entered battery management through estimation on hand-engineered features. Two studies then reset expectations. Severson and "
 "colleagues predicted the entire cycle life of lithium-ion cells with a median test error near 9% from the first hundred cycles alone, on a public "
 "dataset of 124 cells [[10.1038/s41560-019-0356-8]]. Attia and colleagues demonstrated closed-loop Bayesian optimization of fast-charging protocols, "
 "identifying high-cycle-life protocols among 224 candidates in 16 days of cycling rather than the more than 500 days an exhaustive search would take "
 "[[10.1038/s41586-020-1994-5]]. The five years that "
 "followed produced applications across every BMS function: recurrent and convolutional networks for SOC and SOH [[10.1016/j.energy.2020.117664]][[10.1016/j.energy.2023.126855]], "
 "graph and transformer architectures for prognostics [[10.1016/j.ress.2022.108947]][[10.1016/j.energy.2024.133418]], physics-informed neural networks "
 "embedding electrochemical and thermal priors [[10.1016/j.jechem.2022.11.036]][[10.1109/jrfid.2022.3211841]], transfer learning across chemistries "
 "and vehicles [[10.1109/tpel.2021.3117788]][[10.1016/j.energy.2023.127033]], reinforcement learning agents [[10.1016/j.ress.2025.111392]], and, most "
 "recently, LLM-based studies of station-side incident-risk analysis and vehicle-cloud management "
 "[[10.1016/j.ress.2026.112416]][[10.1016/j.ensm.2026.104983]]."),

('h2', '1.2 Existing reviews and the literature gap'),
('p',
 "The review literature has grown alongside the applications but is fragmented along the same axes as the primary studies: an early perspective on "
 "data-driven SOC and SOH prediction [[10.1038/s42256-020-0156-7]] set the agenda; function-specific reviews "
 "cover SOC estimation [[10.1016/j.est.2022.104664]][[10.20517/jmi.2024.84]], SOH estimation [[10.1016/j.apenergy.2021.117346]], and prognostics "
 "[[10.1016/j.jechem.2023.03.026]]; method-specific reviews follow deep-learning state estimation [[10.1016/j.egyai.2025.100585]], physics-informed "
 "impedance diagnostics [[10.1016/j.rser.2023.113807]], or interpretable prognosis [[10.1002/aenm.202503067]]; and domain reviews examine fault "
 "diagnosis [[10.3390/electronics10111309]][[10.1016/j.etran.2023.100254]] and thermal management [[10.1016/j.est.2023.106688]], alongside broader "
 "degradation-method surveys [[10.3390/batteries10070220]] and EV-powertrain ML reviews with BMS scope [[10.1007/s44163-025-00721-y]]. What is missing "
 "is a cross-functional account of the field's trajectory: which method families are used for which tasks, on which data, validated how \u2014 and, "
 "among existing cross-functional surveys, none to our knowledge quantifies validation practice at all. Table VII in Section IX positions this review against its "
 "closest competitors and states the added value explicitly; the short version is that prior reviews synthesize *what is claimed*, while this review "
 "additionally measures \u2014 within a 103-study classified subset \u2014 how those claims are validated, ties both to three safety standards, and "
 "releases the record-level dataset to make every count auditable."),

('h2', '1.3 Contribution of this paper'),
('p',
 "This paper makes four contributions: (i) a rule-based *eligible corpus* of 799 peer-reviewed journal articles (2020\u20132026), selected by uniform "
 "criteria applied to all screened Crossref records \u2014 no function quotas, year caps, or citation thresholds \u2014 so that field-level shares "
 "are measured, not curated, with the retrieval, screening, and tagging provenance of every record released; (ii) an in-depth *classified subset* of "
 "103 studies from that corpus, coded along the six classification fields (function, method family, chemistry, data source, validation practice, and "
 "coded finding/limitation summaries) with the "
 "classification dataset, codebook, per-paper protocol audit, and a 30-paper blind inter-coder reliability study released together with a "
 "label-noise sensitivity analysis of the headline counts; (iii) a two-tier synthesis \u2014 measured bibliometrics from the eligible corpus "
 "(Section III) plus function-by-function critical review of the classified subset (Sections IV\u2013VIII) \u2014 with a BMS-function-to-safety-"
 "standard mapping and a gap-driven research agenda including a twelve-item reporting checklist (Section IX); and (iv) a transportation-"
 "electrification cut of the corpus (Section III-B) separating cell-level laboratory evidence from pack-, vehicle-, and fleet-level practice. "
 "Fig. 1 previews the classified subset, mapping it across management functions and method families: the center of gravity sits in the "
 "health-prognostics complex, hybrid model\u2013data approaches span every function, and learning-based charging control remains a concentrated "
 "Bayesian-optimization stronghold. The remainder of the paper is organized as follows. Section II details the review methodology and its limitations. "
 "Section III presents the two-tier corpus overview, five-year bibliometrics, and the transportation-electrification cut. Sections IV\u2013VII review "
 "machine learning for state estimation, health estimation and prognostics, charging control, and thermal management, faults, and safety. "
 "Section VIII examines cross-cutting directions, and Sections IX and X give the research agenda and conclusions."),

('fig', 'figures/fig1_function_method_map.png', 'Fig. 1 The classified subset mapped across battery-management functions and method families (the 88 '
 "primary-application papers). The remaining 15 classified papers are 12 method-coded reviews (``Review / perspective'') plus 3 review-type syntheses "
 "coded under their dominant method family (two physics-informed, one classical), all 15 of which are counted in the Reviews column of Table II. Rates that "
 "use the primary denominator are 88, not 103."),

('h1', '2. Review Methodology'),

('h2', '2.1 Search strategy'),
('p',
 "All candidate records were retrieved programmatically from the Crossref REST API between 4 and 5 September 2026 using 30 bibliographic query strings "
 "spanning the application areas above. Queries were issued in five passes: a citation-sorted 2020\u20132026 pass, dedicated 2020\u20132022 and 2023 "
 "windows, a mid-window 2021\u20132023 coverage pass, and a relevance-sorted recency pass starting June 2024, yielding 3,000 records; after DOI-based "
 "deduplication (1,450 duplicates removed), 1,550 unique records remained. Six landmark studies \u2014 including [[10.1038/s41560-019-0356-8]] and "
 "[[10.1016/j.joule.2019.11.018]] \u2014 were additionally safeguarded as forced seeds: five were retrieved and verified individually because "
 "citation-sorted retrieval had crowded them out, and one was already among the top-cited hits. Four properties should be stated plainly. First, the "
 "Crossref registry is a metadata registry, not a discovery engine like Scopus or Web of Science; it was chosen so that every included record is "
 "individually verifiable by direct DOI resolution, at the cost of a recall floor. Second, citation-ordered passes favor established English-language "
 "work; all trend statements therefore describe this citation-weighted, journal-article sample rather than the field in the aggregate. Third, "
 "January\u2013May 2024 is a known retrieval hole \u2014 the citation-sorted pass returns almost nothing from those months and the recency pass starts "
 "at June 2024 \u2014 so the 2024 dip visible in year distributions is a design artifact of this retrieval, not evidence about publication volume; "
 "per-year counts in Section III-A are therefore reported as counts within the capped retrieval, with the hole documented, and no field-level "
 "per-year shares are claimed. Fourth, every query pass returned its top 20 records only, so the 30 queries are design-capped at 100 records "
 "per query family; a post-hoc recall audit against the deposited reference lists of the 15 included reviews finds that the retrieval contains "
 "112 of the 649 in-scope-looking, 2020-onward, DOI-bearing references they cite (17.3% counted per-source; 96 of 586 unique references, "
 "16.4%). Retrieval recall is therefore bounded and now quantified: theme frequencies, per-family shares, and \u2018earliest\u2019 claims in this "
 "review are scoped to this retrieval and the subset it fed, and the LLM-estimator recall miss disclosed in the cross-cutting section is cited "
 "by none of those reviews either (audit released as recall_audit.py/.json with cached responses)."),

('h2', '2.2 Screening and rule-based selection'),
('p',
 "The screening funnel is shown in Fig. 2. A title-level relevance gate requiring both battery-related and machine-learning terminology retained 883 "
 "records and excluded 667 (predominantly adjacent-field papers that surfaced through loose matching); the gate is a mechanical keyword rule, and its "
 "term lists are released (tagging_terms.json) together with all 1,550 screening decisions (screening_log.csv). Venue and document-type screening "
 "removed 84 records \u2014 conference abstracts and proceedings series, preprint servers, and non-scholarly venues \u2014 leaving 799 eligible "
 "records. Selection then proceeds in two tiers, replacing the single-quota design that an earlier draft of this review used. *Tier 1 (eligible "
 "corpus).* Every one of the 799 eligible records is included, subject only to venue screening; no function quotas, year caps, or citation thresholds "
 "are applied. Every one of the 799 eligible records carries a Crossref-registered DOI, and every record carried forward to Tier 2 full-text coding "
 "was individually DOI-resolved. Function tagging at this tier is inherited from retrieval: each record carries the area of every query theme that "
 "returned it (query list released), so a record can hold several tags; 202 of 799 records "
 "(25%) carry no management-function tag \u2014 most are method-level or cross-cutting records (physics-informed, second life, digital twins, "
 "benchmark papers) \u2014 so per-function shares below are computed over tagged records and cross-function totals are reported as union shares, "
 "never as sums of per-tag percentages. *Tier 2 (classified subset).* Because in-depth coding of chemistry, data source, and validation practice "
 "requires full-text assessment, full-text coding was applied to a classified subset of 103 studies \u2014 98 from the eligible pool plus 5 landmark seeds retrieved and verified individually \u2014 curated with the same eight-function "
 "stratification used by the tagging pass, with six landmark studies (including the 2019 field-defining seed, Severson et al.) safeguarded as forced entries \u2014 five retrieved individually from outside the query pool and one already among the top-cited hits (Section II-A). This subset is curated, not sampled: "
 "the released record-level log identifies every record at every screening stage (with the forced seeds annotated), the released selection files "
 "allow every inclusion and drop to be traced, and its function and year composition does not match "
 "the eligible corpus's measured shares exactly. Section III therefore never generalizes subset distributions to the field; where the subset is the "
 "only source (method family, validation practice), the text reports subset statistics and their selection caveats explicitly."),

('fig', 'figures/fig2_prisma.png', 'Fig. 2 Study-selection flowchart with the two-tier design. Records were retrieved from the Crossref REST API on '
 "4\u20135 September 2026 (five passes; January\u2013May 2024 retrieval hole documented in Section II-A), deduplicated, screened at title level by a "
 "released mechanical keyword rule (883 retained, 667 excluded), then at venue and document-type level. Tier 1 includes every eligible record (799, "
 "rule-based, no quotas); Tier 2 carries a curated full-text-classified subset of 103 with six landmark studies included deliberately and five "
 "force-included individually from outside the pool. Record-level provenance is released as screening_log.csv (all 1,550 decisions) and "
 "tagging_terms.json."),

('h2', '2.3 Classification framework, validation definitions, and limitations'),
('p',
 "Each paper was classified along six fields: management function (eight values, including a cross-cutting cluster); dominant method family (classical "
 "ML, deep learning, physics-informed/hybrid, optimization-augmented, reinforcement/control learning, transfer learning, foundation models/LLMs, "
 "review); chemistry; primary data source; validation approach; and a coded summary of the headline finding and principal limitation. Three terms are "
 "used consistently: an *eligible record* is one of the 799 Tier-1 studies; a *classifiable paper* is one of the 103 Tier-2 studies; and a "
 "*primary-application paper* is one of the 88 classified papers whose contribution is a primary application \u2014 the 12 method-coded reviews and "
 "3 review-type syntheses coded under their dominant method family are excluded from every rate that uses this denominator (Table II counts them "
 "per function; papers.csv identifies each one). Validation practice is coded against four definitions used throughout this paper: (1) *within-cell split* \u2014 train and test "
 "segments drawn from the same cycling trajectory; (2) *unsupervised k-fold cross-validation* \u2014 folds assigned over samples of the same "
 "trajectories without cell isolation; (3) *cross-cell holdout* \u2014 every test cell held out entirely from training (with cross-chemistry and "
 "cross-domain holdout extending this isolation across chemistry or application); and (4) *online or real-vehicle/fleet validation* \u2014 the "
 "deployed system evaluated on live vehicle data. Cross-cell, cross-chemistry, cross-domain, and online/fleet are together the *strong protocols*; "
 "the four remaining coded environments (experimental hardware, simulation plus hardware spot-check, simulation-only, case study) characterize where "
 "a study was exercised but say nothing about train\u2013test isolation, and they are reported separately \u2014 never mixed into strong-protocol "
 "percentages. Borderline assignments, the absorbing rule for ambiguous cases (a study is credited with the *strongest* protocol it reports for its "
 "headline claim), and the decision tree with examples are given in the released codebook. Classification was performed by the lead author with "
 "conservative coding from full texts; to probe the reliability of that coding, two co-author coders (the second and third authors, not involved in "
 "the primary coding) later blind-re-coded a 30-paper stratified random sample (drawn by function and year band, seed-pinned and reproducible) "
 "under the released codebook, without access to the released labels, to the population statistics, or to each other. The blinding was procedural "
 "rather than external: the coders are authors of this study \u2014 their later author-contribution roles included verification of classifications "
 "and counts \u2014 but their coding sheets were locked and hash-tracked at completion, with a filed blinding memo documenting what each coder had "
 "opened before coding. Blind agreement between the two coders is strong on three of the five classification "
 "fields: management function (\u03ba = 0.92, Krippendorff \u03b1 = 0.92), method family (\u03ba = 0.88, \u03b1 = 0.88), and primary data source "
 "(\u03ba = 0.88, \u03b1 = 0.88). Two fields fell below the \u03ba \u2265 0.66 threshold: chemistry (\u03ba = 0.55) and validation protocol "
 "(\u03ba = 0.48). Part of the shortfall is an evidence-access artifact: the two coders had full-text (or preprint) access to only 7 and 2 of the 30 sample papers, "
 "respectively, so 23 and 28 were coded from abstracts alone \u2014 and these two fields are precisely those least often stated at abstract level. But it must be reported straight that the "
 "aggregation Section III's counts rest on does not escape this: on strong-protocol versus non-strong, the two coders agree on 25 of 30 papers "
 "(raw agreement 83%, \u03ba = 0.51 at the sample's prevalence \u2014 below the 0.66 threshold the paper itself applies). The released labels are "
 "therefore treated as one plausible coding, and all headline validation counts in Section III carry a scenario sensitivity analysis built from the "
 "observed coder-versus-label disagreement in this sample: the central strong-protocol estimate (48% of the 88 primary papers) spans 40\u201359% under the symmetric scenario, and a strong-to-weak worst-case bound (Section III-C) places it as low as 18% at the observed abstract-level recode rate "
 "\u2014 so the strong-protocol level is a bounded range rather than a pinned estimate, and no qualitative conclusion below depends on where in these ranges the truth lies (Section III-C). Coder access "
 "constraints, training, and the complete per-paper, per-field disagreement table are released together with both locked coding sheets and the "
 "hash-tracked log; protocol-versioning candidates (a ``protocol not reported'' code; a chemistry inference rule) are logged as candidates and "
 "alter no released label. The synthesis proceeds on two tracks: measured bibliometrics from the eligible corpus and cross-tabulations from the "
 "classified subset, both generated programmatically from the released datasets (Section III), and qualitative function-by-function critique "
 "(Sections IV\u2013VIII). The methodology's limitations are acknowledged: Crossref coverage excludes influential conference papers; title-level "
 "screening can miss relevant work; citation-ordered retrieval privileges established English-language venues; the per-year retrieval window has one "
 "documented hole (Section II-A); the Tier-2 subset is curated rather than sampled, so validation-practice rates are subset statistics that do not "
 "automatically generalize to the eligible corpus or the field; and reliability is documented on a 30-paper blind re-coding subset rather than "
 "measured corpus-wide (three of five fields above threshold, two below, with the resulting sensitivity ranges reported). DOI resolution, moreover, "
 "verifies that a record exists, not that its venue is topically sensible: one classified-subset study (a physics-informed SOC network, "
 "[[10.1109/jrfid.2022.3211841]]) appears in an RFID-special-issue journal \u2014 we flag it here rather than dropping it, and the released audit "
 "file (final_audit.json) records each reference's Crossref-resolved title and venue at retrieval time so that misattributions of this kind are "
 "hidden. These are the reasons this paper describes itself as a scoping review with bibliometric classification rather than a meta-analysis."),
]
