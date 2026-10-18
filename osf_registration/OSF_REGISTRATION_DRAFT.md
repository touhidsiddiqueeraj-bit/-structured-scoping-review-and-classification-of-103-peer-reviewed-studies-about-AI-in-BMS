# Retrospective registration draft — OSF Registries

> **Status of this document.** This is the complete, ready-to-paste content for a
> **retrospective** registration of this scoping review on OSF Registries. It was
> prepared after the review was completed (October 2026) and describes the protocol
> **as conducted**, not as a prospective plan. When filed, the registration must be
> disclosed as retrospective (OSF's registration form asks "Why are you registering
> this research?" — answer: "Registration after data collection was complete; the
> review's a-priori decisions are documented in the released pipeline files and their
> version history, and this registration preserves the as-conducted protocol").
> Nothing in this document may be edited to describe a different protocol than the
> one actually executed; where the executed review deviated from common practice,
> the deviation is stated in the registration itself.

---

## Registration form content (paste field by field)

**Title.**
Machine learning in battery management systems: a two-tier scoping review of 799
eligible studies with in-depth classification and validation audit

**Registration reason.**
Retrospective registration (post-completion), disclosed as such. The protocol was
not registered prospectively because PROSPERO does not accept scoping-review
registrations and no alternative registry was used before screening began. This
registration documents the as-conducted protocol for citation and auditability; it
cannot serve the pre-emption function of prospective registration.

**Research questions.**
(1) What is the composition of the recent peer-reviewed literature on machine
learning for lithium-ion battery management, by management function, method family,
chemistry, data source, and validation protocol? (2) How stringently do published
accuracy claims validate generalization — specifically, how often do studies
isolate their generalization claim (cross-cell, cross-chemistry, or cross-domain
holdout, or online/real-vehicle demonstration) rather than evaluate on
information-leaking splits? (3) Which BMS functions are under-served relative to
the requirements posed by UN GTR 20, GB 38031, ISO 26262, ISO/PAS 8800, and
ISO 21448, and what reporting practices would make future claims checkable?

**Eligibility criteria (as executed).**
Records eligible for the pool: Crossref-registered journal articles, dated 2020
through the retrieval date (plus early-access records date-stamped by Crossref
metadata), passing a released mechanical title-relevance rule (a battery/EV term
AND a machine-learning/data-driven term) and a released venue screen (excluding
conference abstracts and proceedings series, preprint servers, and non-scholarly
venues). Studies eligible for the classified subset: all pool records were
candidates; 98 were selected by a released rule (function quotas with year caps,
citation-ordering within strata, venue quality floor) plus five landmark seed
studies retrieved and verified individually (one dated 2019). Exclusions:
non-journal document types, records failing the title rule or venue screen,
duplicates by DOI, and (at full-text) papers outside the machine-learning /
battery-management scope.

**Information sources and search strategy (as executed).**
Crossref REST API only, queried 4–5 September 2026, 30 bibliographic query strings
(released verbatim in `corpus/queries.txt`) spanning SOC/SOH/RUL estimation,
charging control, thermal management, fault and safety, cell balancing/ECM, and
cross-cutting themes (physics-informed, transfer learning, digital twins, LLMs,
graph networks, benchmarks, interpretability, cloud/fleet, second life). Five
passes per query (top-cited 2020–2026; relevance-sorted recency from 2024-06;
citation-sorted mid-window 2021–2023; relevance-sorted 2020–2022; relevance-sorted
2023), each capped at its top ~20 records: 3,000 fetched rows, 2,973 after
document-type/year/title-completeness filters, 1,423 duplicates removed, 1,550
unique records. No cross-database triangulation (Scopus/Web of Science not
searched): the design goal was that every included record be verifiable by direct
DOI resolution.

**Screening and selection (as executed).**
Single-reviewer, rule-first: the title gate and venue screen are deterministic
applications of released term lists; all 1,555 per-record decisions (1,550
retrieved + 5 forced seeds) with reasons are in the released screening log.
Full-text curation (19 exclusions, 10 additions) and all classification were
single-reviewer. Dual coding exists only as the 30-paper reliability study.

**Charting / data items (as executed).**
Six fields per paper: management function (8 values), method family, chemistry,
primary data source, validation approach (11 values aggregated into
strong/weak/environment-only tiers under a released absorbing rule), and a coded
finding/limitation summary; plus a seventh abstract-level baseline-comparison
screen added during the review. Codebook and coding protocol released
(`corpus/codebook.md`, `corpus/coding_protocol.md`).

**Synthesis and analysis (as executed).**
Quantitative cross-tabulations generated programmatically from the released
dataset (function/method/chemistry/data/validation, by year where meaningful),
with Wilson confidence intervals, Fisher exact tests for the physics-informed
contrast, a label-noise sensitivity analysis, a minimum-detectable-effect (power)
analysis, a retrieval recall audit against the included reviews' reference lists,
a retrieval-depth (cursor-paging) pilot, abstract-level representativeness and
baseline-comparison probes, and an independent post-freeze re-code of the
validation field from retrievable evidence. Qualitative critical synthesis per
management function and a requirement-level mapping onto automotive safety
standards.

**Reliability (as executed).**
Two co-author coders blind-re-coded a 30-paper stratified random sample
(seed-pinned) under the released codebook; agreement and kappas released with
coder sheets, itemized disagreements, and a hash-tracked log.

**Deviations declared within this registration.**
Screening and classification were single-reviewer rather than dual independent;
no per-record time-on-task logs were kept; retrieval was capped at the top ~20
records per query pass (the recall and depth analyses quantify what the cap
withholds); the registration itself is retrospective.

**Contributors.**
Hussain Touhid Siddiquee (lead; retrieval, screening, verification,
classification, analysis, drafting); Syeda Salsabil Islam Ariya (coder B;
reliability study, verification, revision); Jasimul Islam Chowdhury (coder C;
reliability study, verification, revision).

**Conflicts of interest.**
None declared.

**Version of the review at registration.**
Completed manuscript, repository commit corresponding to the submitted version;
the released pipeline files and their version history (screening log, term lists,
quota rules, seeds register) constitute the primary audit trail for a-priori
decisions.

**Data and code availability.**
Complete evidence base and analysis pipeline deposited (Zenodo DOI
10.5281/zenodo.23436202; GitHub development mirror under the same name).
