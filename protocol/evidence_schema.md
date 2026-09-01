# Evidence Schema

## General completion rules

`corpus/papers.csv` uses UTF-8, RFC 4180-compatible CSV with one header row.
Fields containing commas, quotes, or newlines must be quoted. Do not invent
missing information. Use `NR` only when the inspected source does not report
an item, `NA` only when the field does not apply, and `unclear` only when the
available evidence is ambiguous. Explain consequential `NR`, `NA`, or
`unclear` values in `notes`.

Boolean fields use `yes`, `no`, `partial`, or `unclear`; use `NA` only where
logically inapplicable. Multi-valued fields use semicolon-separated controlled
terms. Free text must be concise and attributable. Every synthesis claim must
cite one or more `record_id` values.

## Paper fields

| Field | Allowed values / format | Completion rule |
|---|---|---|
| `record_id` | Stable unique ID `P####` | Required; never reuse or silently renumber. |
| `full_citation` | Verified full citation | Required at full-text verification; identify version. |
| `doi` | Canonical DOI without resolver prefix; `NR` | Verify against primary source and authoritative metadata. |
| `url` | Stable primary-source or authoritative landing-page URL | Required when available; do not use a search-result URL. |
| `publication_type` | `journal_article`; `conference_paper`; `book`; `book_chapter`; `thesis`; `preprint`; `technical_report`; `software_paper`; `software_documentation`; `review`; `perspective`; `tutorial`; `other` | Required; clarify `other`. |
| `publication_status` | `peer_reviewed`; `preprint`; `accepted`; `published_not_peer_reviewed`; `thesis_examined`; `retracted`; `withdrawn`; `superseded`; `unclear` | Required; check for later/corrected versions. |
| `primary_or_secondary_source` | `primary`; `secondary`; `mixed`; `unclear` | Required; assess for the contribution extracted, not the venue label. |
| `scientific_objective` | Free text | State the decision or inferential objective, not only the topic. |
| `biological_domain` | `13C_MFA`; `stable_isotope_tracing_other`; `metabolic_modelling`; `systems_biology`; `general_statistics`; `information_theory`; `optimal_design`; `controlled_sensing`; `scientific_software`; `other` | One or more terms; clarify `other`. |
| `model_type` | `steady_state_MFA`; `INST_MFA`; `EMU`; `isotopomer`; `cumomer`; `kinetic`; `stoichiometric`; `hierarchical`; `general_nonlinear`; `other`; `NR` | One or more; record both EMU and inferential model where applicable. |
| `observation_type` | `MID`; `mass_isotopomer`; `NMR`; `MS`; `MSMS`; `time_course`; `flux_measurement`; `concentration`; `multi_omics`; `synthetic`; `general`; `other`; `NR` | One or more; distinguish platform from data structure when known. |
| `estimated_or_decided_object` | `flux`; `parameter`; `tracer`; `measurement_panel`; `sample_size`; `replicate_allocation`; `model_structure`; `mechanism`; `hypothesis`; `experiment_sequence`; `model_adequacy`; `other` | Required; one or more. |
| `experimental_variables_optimised` | `none`; `tracer_identity`; `tracer_mixture`; `enrichment`; `measurement_panel`; `time_points`; `perturbation`; `condition`; `sample_size`; `replicate_allocation`; `experiment_sequence`; `other`; `NR` | Record only variables actually optimised, not merely varied. |
| `uncertainty_represented` | `none`; `flux`; `kinetic_parameter`; `nuisance_parameter`; `structure`; `measurement_noise`; `biological_heterogeneity`; `condition`; `tracer_implementation`; `forward_model_misspecification`; `other`; `NR` | One or more; state formulation in notes if needed. |
| `uncertainty_formulation` | `none`; `probabilistic_frequentist`; `Bayesian`; `set_valued`; `empirical`; `sensitivity_based`; `adversarial`; `distributionally_robust`; `other`; `NR`; `unclear` | One or more; record how uncertainty is mathematically represented, not merely which object is uncertain. Clarify `other` and mixed formulations in notes. |
| `uncertainty_dependencies` | `not_modelled`; `independent`; `correlated`; `hierarchical`; `shared_nuisance`; `dependent_other`; `NR`; `unclear` | One or more; state whether dependence among observations, experiments, uncertainty sources, or nuisance parameters is modelled. Clarify the dependent objects in notes. |
| `statistical_criterion` | `likelihood`; `least_squares`; `Fisher_information`; `optimality_A`; `optimality_D`; `optimality_E`; `variance`; `confidence_region`; `posterior_risk`; `expected_information_gain`; `mutual_information`; `KL_divergence`; `power`; `type_I_error`; `type_II_error`; `classification_error`; `minimax_risk`; `goodness_of_fit`; `information_criterion`; `other`; `NR` | Record the actual criterion computed or optimised. |
| `criterion_family` | `D_optimality`; `T_optimality`; `KL_optimality`; `Bayesian_discrimination`; `Chernoff`; `Fisher_information`; `likelihood`; `posterior`; `other`; `NR`; `unclear` | Higher-level decision/design family. Multi-values are allowed when the source explicitly combines families. |
| `statistical_guarantee` | `none`; `local`; `asymptotic`; `Bayesian_posterior`; `simulation_based`; `finite_sample`; `uniform`; `worst_case`; `minimax`; `converse_impossibility`; `empirical_only`; `unclear` | One or more; do not strengthen the source's claim. |
| `guarantee_regime` | `none`; `heuristic`; `simulation_based`; `local_asymptotic`; `global_asymptotic`; `non_asymptotic`; `exact_finite_sample`; `unclear` | Separate the mathematical regime from criterion and robustness. `non_asymptotic` requires an explicit bound/result valid without an asymptotic limit; `exact_finite_sample` requires exact calibration or computation. |
| `robustness_scope` | `none`; `local_neighbourhood`; `sampled_flux_maps`; `finite_scenario_set`; `continuous_parameter_set`; `structural_uncertainty_set`; `distributional_uncertainty`; `model_misspecification`; `unclear` | Record the set over which robustness is evaluated or guaranteed. Sampling is never coded as continuous-set uniformity. |
| `converse_type` | `none`; `identifiability_obstruction`; `rank_obstruction`; `lower_bound`; `error_exponent_converse`; `sample_complexity_converse`; `other`; `unclear` | Requires primary full-text inspection and an exact evidence location for any non-`none` value. |
| `stopping_rule` | `fixed_sample`; `sequential`; `adaptive`; `unspecified`; `NA` | Record the sampling/stopping regime actually formulated. Multi-values are allowed for papers treating separate regimes. |
| `structural_alternative_subtype` | `reaction_presence_absence`; `pathway_alternative`; `compartment_structure`; `atom_mapping`; `kinetic_mechanism`; `mechanism_class`; `other`; `NA`; `unclear` | Record the structural difference, not merely that several numerical parameter values are compared. |
| `parameter_sharing` | `shared_across_conditions`; `condition_specific`; `partially_shared`; `unspecified`; `NA` | State how parameters are related across experiments or conditions. |
| `finite_sample` | Boolean vocabulary | `yes` only for an explicit nonasymptotic finite-sample result or exact computation; explain simulation-only evidence. |
| `uniform_or_worst_case` | Boolean vocabulary | `yes` only if guarantee/criterion is uniform over a stated set or worst case. |
| `minimax` | Boolean vocabulary | `yes` only when a minimax optimisation or guarantee is explicit. |
| `converse_or_impossibility` | Boolean vocabulary | `yes` for a lower bound, impossibility, necessary condition, or converse. |
| `structural_alternatives` | Boolean vocabulary | Does the method explicitly compare differing network/mechanism structures? |
| `multiple_experiments` | Boolean vocabulary | Does inference/design combine more than one tracer, condition, perturbation, time series, or experiment? |
| `non_iid` | Boolean vocabulary | Does the formulation explicitly allow non-identically distributed or dependent observations? |
| `sample_size_design` | Boolean vocabulary | Is sample size or replication an output/design variable rather than fixed input? |
| `replicate_type` | `none`; `biological`; `technical`; `both`; `unspecified`; `NA`; `unclear` | Required when sample size or replicate allocation is discussed; distinguish the kind of replicate designed or analysed. |
| `model_misspecification` | Boolean vocabulary | Is departure from the assumed forward/statistical model explicitly treated? |
| `software` | Package/repository names; `none`; `NR` | Name software used or supplied; capability belongs in the software table. |
| `principal_result` | Attributable free text | State the main result relevant to the review without novelty inflation. |
| `authors_stated_limitations` | Attributable free text; `NR` | Record limitations explicitly stated by authors with location. |
| `reviewer_assessed_limitations` | Reviewer analysis | Separate reviewer inference from author statements and give rationale. |
| `novelty_claim_affected` | Candidate-gap or rejected-claim ID(s); `none`; `unclear` | Use stable IDs defined in synthesis registers. |
| `relevance` | `direct`; `adjacent`; `peripheral` | Apply `inclusion_exclusion.md`; excluded works do not receive evidence rows. |
| `verification_status` | `lead_only`; `metadata_only`; `abstract_only`; `full_text_checked`; `methods_checked`; `result_checked`; `fully_verified`; `conflicted` | Required; use the strongest completed stage, with conflicts overriding. |
| `evidence_location` | Page, section, theorem, figure, table, supplement, repository path/version, or timestamp | Required for substantive extraction; multiple locations separated by semicolons. |
| `notes` | Free text | Version links, ambiguities, provenance, access limits, and controlled-vocabulary explanations. |
| `retrieval_status` | `not_attempted`; `metadata_retrieved`; `abstract_retrieved`; `retrieved_full_text`; `retrieval_failed`; `unclear` | State what material was actually obtained. |
| `access_status` | `open_access`; `author_manuscript`; `user_supplied`; `paywalled_or_inaccessible`; `not_retrieved`; `unclear` | Record the access route/status without treating access as quality evidence. |
| `full_text_inspected` | Boolean vocabulary | `yes` only after the complete primary text or complete authoritative HTML has been inspected. |
| `screening_disposition` | `retained`; `excluded`; `duplicate`; `pending`; `unclear` | Required for screening records and retained corpus rows. |
| `exclusion_reason` | `NA`; `duplicate`; `purely_biological`; `insufficient_method_detail`; `unrelated_transfer`; `inadequate_provenance`; `secondary_only`; `not_selected_original_pilot_reason_unrecoverable`; `other`; `unclear` | Required when excluded; explain `other` or `unclear`. |

## Completion gates

- A discovery lead may contain minimal metadata but cannot support synthesis.
- `full_text_checked` requires access to and inspection of the complete source.
- `fully_verified` requires verified metadata plus direct checking of the
  objective, relevant method/result, guarantee, limitations, and evidence
  locations.
- Any claim about finite-sample, uniform, minimax, or impossibility guarantees
  must have an exact evidence location.
- Any non-`none` `converse_type`, yes-level `structural_alternatives`,
  `non_iid`, or `sample_size_design` claim requires inspected primary full
  text and an exact methodological location.
- Conflicting metadata or interpretations require `conflicted` and an
  explanation; do not resolve them silently.

## Software fields

Capability fields use `yes`, `no`, `partial`, `unclear`, or `NA`. A `yes`
requires direct evidence of implemented functionality; plans and issue
requests do not count.

| Field | Allowed values / format | Completion rule |
|---|---|---|
| `record_id` | Stable unique ID `S####` | Required; never reuse or silently renumber. |
| `package` | Verified package/project name and version where applicable | Required; distinguish forks or renamed projects. |
| `citation` | Preferred verified software citation; `NR` | Cite a software paper, archived release, or project-requested citation where available. |
| `url` | Official repository, archive, registry, or project URL | Required; record the inspected version/commit in notes. |
| `licence` | SPDX identifier; exact stated licence; `none_stated`; `unclear` | Verify from the inspected repository/release, not a third-party list alone. |
| `maintained_status` | `active`; `inactive`; `archived`; `superseded`; `unclear` | Required; give assessment date and evidence in notes; activity alone does not establish quality. |
| `forward_EMU_simulation` | Capability vocabulary | Does it implement an EMU forward model, not merely consume simulated values? |
| `inverse_flux_estimation` | Capability vocabulary | Does it estimate fluxes from isotope observations? |
| `steady_state_support` | Capability vocabulary | Does it support metabolic and isotopic steady-state analysis? |
| `isotopically_nonstationary_support` | Capability vocabulary | Does it support isotopically nonstationary/time-course isotope analysis? |
| `tracer_design` | Capability vocabulary | Does it optimise or systematically rank tracer identity, mixture, or enrichment? |
| `measurement_design` | Capability vocabulary | Does it optimise or rank measured metabolites, fragments, platforms, or time points? |
| `replicate_allocation` | Capability vocabulary | Does it design replicate counts or allocate replicates under constraints? |
| `multi_experiment_support` | Capability vocabulary | Can a single analysis/design combine multiple tracers, conditions, or experiments? |
| `model_comparison` | Capability vocabulary | Does it implement validation, structural comparison, selection, or mechanism discrimination? Explain which. |
| `uncertainty_quantification` | Capability vocabulary | Does it compute uncertainty summaries? State object and method in notes. |
| `finite_sample_certification` | Capability vocabulary | Does it implement certified finite-sample error, sufficiency, power, or impossibility results? Simulation alone is not `yes`. |
| `graphical_interface` | Capability vocabulary | Is an operational graphical user interface documented or verified? |
| `command_line_interface` | Capability vocabulary | Is a documented or verified CLI available? A programming API alone is not `yes`. |
| `reproducibility_features` | Concise free text; `none`; `NR` | Record versioning, scripted workflows, environments, tests, examples, seeds, containers, or provenance features actually evidenced. |
| `limitations` | Attributable or reviewer-assessed free text; `NR` | Distinguish documented limitations from reviewer assessment in wording. |
| `verification_status` | `lead_only`; `metadata_only`; `documentation_checked`; `repository_checked`; `execution_checked`; `fully_verified`; `conflicted` | Required; record the strongest completed check, with conflicts overriding. |
| `notes` | Free text | Required for inspected version/date and evidence locations; include ambiguity and provenance. |
| `retrieval_status` | `not_attempted`; `documentation_retrieved`; `repository_retrieved`; `release_retrieved`; `retrieval_failed`; `unclear` | Record the strongest material retrieved. |
| `access_status` | `open_documentation`; `open_repository`; `restricted`; `not_retrieved`; `unclear` | Record the inspected access route. |
| `full_text_inspected` | Boolean vocabulary | For software, means the cited documentation/software paper or relevant repository files were inspected; it does not mean execution. |
| `screening_disposition` | `retained`; `excluded`; `duplicate`; `pending`; `unclear` | Required. |
| `exclusion_reason` | Paper exclusion vocabulary plus `NA` | Required when excluded. |

Software capability values must be supported by official documentation,
repository code/tests, an executed check, or a primary software paper, with
the source and version recorded in `notes`. Interface availability does not
establish methodological novelty or statistical guarantees.

## Pilot screening-ledger fields

`audit/pilot_screening.csv` is a discovery/provenance ledger. It does not
imply that every discovered record received an eligibility decision.

| Field | Controlled values / rule |
|---|---|
| `screening_state` | `RETAINED`; `EXCLUDED_WITH_RECORDED_REASON`; `DISCOVERED_NOT_SCREENED`; `SCREENED_DECISION_UNRECOVERABLE`; `DUPLICATE`; `UNRESOLVED` |
| `original_eligibility_disposition` | `retained`; `excluded`; `duplicate`; `not_screened`; `unrecoverable`; `unresolved` |
| `historical_discovery_provenance_state` | `EXACT_HISTORICAL_PROVENANCE`; `PARTIAL_HISTORICAL_PROVENANCE`; `HISTORICAL_PROVENANCE_UNRECOVERABLE`; `MANUAL_CITATION_DISCOVERY`; `BACKWARD_CITATION_DISCOVERY`; `FORWARD_CITATION_DISCOVERY` |
| `historical_query_ids` | Original query IDs only when demonstrated by a preserved original export; blank when unrecoverable. |
| `repair_retrieval_provenance_state` | `EXACT_REPAIR_RERUN_MATCH`; `PARTIAL_REPAIR_RERUN_MATCH`; `NOT_FOUND_IN_REPAIR_RERUN`; `NOT_APPLICABLE` |
| `repair_query_ids` | Demonstrated `REPAIR-SEARCH-####` IDs only; never original `SEARCH-####` IDs inferred from equivalent query text. |
| `repair_rerun_date` | ISO date of the repair rerun; blank when not applicable. |
| `provenance_notes` | Explain the basis and limits of both provenance states. |
| `exclusion_reason` | `NA` unless `screening_state=EXCLUDED_WITH_RECORDED_REASON`; an unrecoverable decision is not an exclusion reason. |

`SCREENED_DECISION_UNRECOVERABLE` must not be counted as a genuine exclusion
or a prospectively repeated screening decision.

An exact repair-rerun match establishes only that the record was returned on
the repair date. It does not establish its original historical discovery
query.

## Phase 2 prospective screening fields

`audit/phase2_screening.csv` is independent of the Phase 1 ledger.
It is the authoritative current disposition ledger. Workstream-specific
screening CSVs are preserved pre-closure inputs and may retain their original
interim states; those states are not current dispositions after the
corresponding occurrence has a final state in the consolidated ledger.

| Field | Rule |
|---|---|
| `phase2_record_id` | Stable occurrence ID within its workstream. |
| `workstream` | `A`; `B`; `C`; `D`; `E`. |
| `query_id` | Demonstrated `PHASE2-SEARCH-####` identifier only. |
| `screening_state` | `DISCOVERED_NOT_SCREENED`; `TITLE_ABSTRACT_INCLUDED`; `TITLE_ABSTRACT_EXCLUDED`; `FULL_TEXT_INCLUDED`; `FULL_TEXT_EXCLUDED`; `DUPLICATE`; `FULL_TEXT_UNAVAILABLE`; `AWAITING_VERIFICATION`; `FALSE_POSITIVE`; `DEFERRED_RELEVANT_SUPPORTING`; `DEFERRED_RELEVANT_ADJACENT`; `OUT_OF_SCOPE_FOR_PHASE2A1`; `FALSE_POSITIVE_CONFIRMED`. The last four are scoped Phase 2A.1 repair states and do not alter the preserved workstream-source ledgers. |
| `exclusion_reason` | Required and nonblank for every genuine final non-inclusion (`TITLE_ABSTRACT_EXCLUDED`; `FULL_TEXT_EXCLUDED`; `FULL_TEXT_UNAVAILABLE`; `DUPLICATE`; `FALSE_POSITIVE`; `FALSE_POSITIVE_CONFIRMED`). For the three deferred/scoped states, this field stores the explicit *deferral or scope reason*, not a broader-review exclusion. It may be `NA` or blank for an inclusion or unresolved discovery state. |
| `evidence_level` | `LEVEL_1_LOAD_BEARING`; `LEVEL_2_SUPPORTING`; `LEVEL_3_DISCOVERY_ONLY`. |
| `final_record_id` | Stable paper/software corpus ID when retained; blank for discovery-only and excluded occurrences. |

An occurrence marked `FULL_TEXT_INCLUDED` establishes access only when its
corpus evidence row also records an exact methodological location.

`FALSE_POSITIVE` is a final disposition in the independently prospective
Phase 2A.1 search ledger for a record that, after record-level
title/abstract/citation-context assessment, does not address that search
question. `FALSE_POSITIVE_CONFIRMED` is the corresponding controlled state
used when correcting the 264 inherited Phase 2 occurrences, and it requires
an explicit record-level reason showing that the paper addresses no review
question. Neither state may be inferred from priority, workstream, failure
to retrieve a full text, or non-selection for a narrow repair.

`DEFERRED_RELEVANT_SUPPORTING`, `DEFERRED_RELEVANT_ADJACENT`, and
`OUT_OF_SCOPE_FOR_PHASE2A1` preserve the original prospective
title/abstract relevance judgement. They mean, respectively, relevant
supporting evidence deferred from the narrow repair, adjacent evidence
deferred from the narrow repair, and evidence outside the narrow
GAP-01/GAP-03 repair but not excluded from the broader Phase 2 review. These
records remain eligible only for qualified family-level synthesis until
their full text is verified.

Neither false-positive state is a full-text exclusion or evidence for a
substantive synthesis or absence claim.

## Phase 2A.1 prospective screening and triage

`audit/phase2a1_screening.csv` records the new foundational searches
separately from Phase 2 and Phase 1 provenance.

| Field | Controlled values / rule |
|---|---|
| `phase2a1_record_id` | Stable occurrence ID `A1AC-####` or `A1DEF-####`; never reuse. |
| `query_id` | Demonstrated `PHASE2A1-SEARCH-####` only. |
| `screening_state` | Final states only: `FULL_TEXT_INCLUDED`; `FULL_TEXT_EXCLUDED`; `FULL_TEXT_UNAVAILABLE`; `DUPLICATE`; `FALSE_POSITIVE`. |
| `evidence_depth` | `LEVEL_1_LOAD_BEARING`; `LEVEL_2_SUPPORTING`; `LEVEL_3_DISCOVERY_ONLY`. |
| `final_record_id` | Stable `P####` only for the representative `FULL_TEXT_INCLUDED` occurrence; blank otherwise. |
| `corpus_action` | `NONE`; `NEW_CORPUS_CANDIDATE`; `EXISTING_CORPUS_RECORD`; `DUPLICATE_OF_EXISTING_CORPUS`; `DUPLICATE_OF_NEW_CORPUS_CANDIDATE`. |
| `source_proposed_corpus_record` | Preserved source-ledger proposal or stable ID; never treated as the final mapping without corpus validation. |
| `exclusion_reason` | Required for every state other than `FULL_TEXT_INCLUDED`. |
| `evidence_location` | Exact primary-source location required for `FULL_TEXT_INCLUDED`; blank or explicitly bibliographic for inaccessible records. |
| `raw_snapshot` | Repository-relative path to the preserved query export or retrieval record. |

`audit/phase2_unresolved_triage.csv` is a paper-level normalization of the
264 Phase 2 title/abstract-included occurrences. `likely_load_bearing` is one
of `LOAD_BEARING`, `POTENTIALLY_LOAD_BEARING`, `SUPPORTING`, `PERIPHERAL`, or
`FALSE_POSITIVE`. `final_disposition` uses `FULL_TEXT_INCLUDED`,
`FULL_TEXT_EXCLUDED`, `FULL_TEXT_UNAVAILABLE`, `DUPLICATE`,
`DEFERRED_RELEVANT_SUPPORTING`, `DEFERRED_RELEVANT_ADJACENT`,
`OUT_OF_SCOPE_FOR_PHASE2A1`, `FALSE_POSITIVE_CONFIRMED`, or `UNRESOLVED`.
Multiple source occurrences never count as multiple papers.

`audit/phase2a1_deferred_records.csv` is the explicit scoped-disposition
mapping for non-included records from that normalization. It preserves the
original Phase 2 state, canonical original evidence level, title/abstract
relevance metadata, methodological family, gap association, and access
depth. Its controlled fields are:

| Field | Controlled values / rule |
|---|---|
| `phase2a1_scoped_disposition` | `DEFERRED_RELEVANT_SUPPORTING`; `DEFERRED_RELEVANT_ADJACENT`; `OUT_OF_SCOPE_FOR_PHASE2A1`; `FALSE_POSITIVE_CONFIRMED`; `FULL_TEXT_UNAVAILABLE`; `FULL_TEXT_EXCLUDED`. |
| `broader_review_relevance` | `RELEVANT_SUPPORTING`; `RELEVANT_ADJACENT`; `RELEVANT_OUTSIDE_NARROW_REPAIR`; `RELEVANT_BUT_FULL_TEXT_UNAVAILABLE`; `ASSESSED_AND_EXCLUDED_AT_FULL_TEXT`; `NOT_RELEVANT_TO_ANY_REVIEW_QUESTION`. |
| `eligible_for_later_synthesis` | `yes_qualified_only`; `conditional_on_full_text`; `no`. |
| `disposition_reason` | Required for every row. A `FALSE_POSITIVE_CONFIRMED` reason must be record-specific and explain why no review question is addressed. |
| `original_phase2_screening_state` | Preserved source state; `TITLE_ABSTRACT_INCLUDED` for this repaired cohort. |
| `original_phase2_evidence_level` | Canonical source occurrence's original controlled evidence level. |

`audit/phase2a1_false_positive_confirmations.csv` preserves the two
record-level scope decisions used to assign
`FALSE_POSITIVE_CONFIRMED`. Each row requires a stable
`unique_record_id`, an explicit `record_level_reason`, `decision_date`,
`assessment_basis`, and `status=FALSE_POSITIVE_CONFIRMED`. The confirmation
ledger is curator-supplied input; no script may infer one of these decisions
from priority, workstream, or non-selection.

The correction script consumes this explicit mapping; it never derives a
false positive from priority. Unmapped unresolved records remain unchanged,
unknown mappings or unexpected curated states abort before replacement, and
every applied transition is retained in
`audit/phase2a1_closure_change_log.csv`.
