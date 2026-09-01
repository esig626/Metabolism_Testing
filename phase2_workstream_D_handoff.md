# Phase 2A Workstream D — Bounded Closure Handoff

Date: 2026-07-31 UTC  
Searcher/screener: Codex `/root/workstream_d_close`

## Scope and provenance

This closure used only the already-preserved Phase 2 raw records for
PHASE2-SEARCH-0104–0106 and the legally accessible primary full text at
`audit/phase2_raw_search_results/D/P0045-PMC5020535-fulltext.xml`. No new web
search or retrieval was performed.

The prospective occurrence ledger is
`audit/phase2_screening_D_closure.csv`; its deterministic generator is
`audit/phase2_raw_search_results/D/build_screening_closure.pl`.

## Exact screening counts

| Query | Metadata-resolved occurrences | Unresolved identifiers | Full text included | Duplicates | Title/abstract included | Title/abstract excluded | Awaiting verification |
|---|---:|---:|---:|---:|---:|---:|---:|
| PHASE2-SEARCH-0104 | 50 | 0 | 1 | 10 | 7 | 32 | 0 |
| PHASE2-SEARCH-0105 | 34 | 0 | 0 | 3 | 11 | 20 | 0 |
| PHASE2-SEARCH-0106 | 30 | 1 | 0 | 2 | 9 | 19 | 1 |
| **Total** | **114** | **1** | **1** | **15** | **27** | **71** | **1** |

All 71 prospective exclusions have an explicit reason. All 27
title/abstract inclusions remain `LEVEL_3_DISCOVERY_ONLY`; they support no
substantive synthesis claim. The one `LEVEL_1_LOAD_BEARING` record is the
complete primary text proposed as P0045.
The closure ledger contains 106 ledger-local deduplication groups; this is
not a global unique-work count.

OpenAlex identifier `W6604903323` appears in P0035's reference list but did
not resolve in the preserved metadata batch. It is recorded as
`AWAITING_VERIFICATION`; its title, authors, year and eligibility were not
inferred.

## P0045 exact primary evidence

**Citation:** Sokolenko S, Quattrociocchi M, Aucoin MG. Identifying model
error in metabolic flux analysis—a generalized least squares approach. *BMC
Systems Biology*. 2016;10:91. DOI:
`10.1186/s12918-016-0335-7`. PMCID: `PMC5020535`.

The inspected paper is about traditional, overdetermined stoichiometric MFA,
not an EMU or isotope-label forward model.

Exact evidence locations:

- `Methods`, “Theoretical principles,” BioC offsets 9,303–12,860: formulates
  steady-state stoichiometric MFA as a linear/GLS regression; explicitly says
  the IID assumption in Equation 7 is unlikely and introduces covariance
  rescaling.
- `Methods`, same subsection, offsets 12,860–14,067: contrasts the residual
  chi-square check with t-tests for calculated-flux significance.
- `Methods`, same subsection, offsets 14,067–16,008, especially Equation 19:
  proposes sampling feasible balanced fluxes and perturbing them with
  measurement error to distinguish measurement uncertainty from lack of
  model fit.
- `Methods`, “Flux estimation,” offsets 19,513–20,514: obtains flux inputs
  from simulated concentration trajectories and analyses a single
  mid-exponential time point.
- `Methods`, “Implementation,” offsets 20,514–21,048: identifies the
  `omfapy` implementation and analysis-code route.
- `Results`, “Identification of model error,” offsets 23,604–26,937; Figure
  2: chi-square `p = 0.93`, but only 15/47 fluxes significant; 100 balanced
  profiles × 100 measurement-noise perturbations; model correction explicitly
  outside scope.
- `Results`, “Effect of measurement noise,” offsets 27,544–30,082; Figure 3:
  simulation-based comparison over 5%, 10%, 15% and 20% coefficients of
  variation.
- `Results`, “Effect of model structure,” offsets 30,820–33,701; Figures
  4–6: adding NADH/NADPH balances reduces non-significant fluxes from 32 to
  16 and changes simulated significance patterns.
- `Conclusion`, offsets 39,449–40,312: limits the demonstrated analysis to
  traditional MFA and says transfer to alternative MFA formulations is
  likely, rather than demonstrating that transfer.

Evidence interpretation:

- **Established:** a covariance-aware GLS formulation, conventional
  regression tests, and a simulation diagnostic can reveal poor traditional
  MFA fit that a chi-square residual check misses.
- **Not established:** EMU transfer, calibrated structural/mechanism
  selection, prospective experiment design, a bounded discrepancy class,
  uniform/minimax protection, a finite-sample guarantee, or a converse.
- **Guarantee coding:** `simulation_based`; `guarantee_regime =
  simulation_based`; `finite_sample = no`; `uniform_or_worst_case = no`;
  `minimax = no`; `converse_or_impossibility = no`.

## Proposed P0045 corpus row

The parent should assign P0045 only if that stable ID remains available at
merge time. No corpus edit was made by this workstream.

| Field | Proposed value |
|---|---|
| `record_id` | `P0045` |
| `full_citation` | Sokolenko S, Quattrociocchi M, Aucoin MG. Identifying model error in metabolic flux analysis—a generalized least squares approach. BMC Systems Biology. 2016;10:91. |
| `doi` | `10.1186/s12918-016-0335-7` |
| `url` | `https://pmc.ncbi.nlm.nih.gov/articles/PMC5020535/` |
| `publication_type` | `journal_article` |
| `publication_status` | `peer_reviewed` |
| `primary_or_secondary_source` | `primary` |
| `scientific_objective` | Diagnose lack of fit in overdetermined traditional stoichiometric MFA separately from measurement uncertainty. |
| `biological_domain` | `metabolic_modelling` |
| `model_type` | `steady_state_MFA;stoichiometric` |
| `observation_type` | `flux_measurement;concentration;synthetic` |
| `estimated_or_decided_object` | `flux;model_adequacy` |
| `experimental_variables_optimised` | `none` |
| `uncertainty_represented` | `measurement_noise;forward_model_misspecification` |
| `uncertainty_formulation` | `probabilistic_frequentist;empirical` |
| `uncertainty_dependencies` | `correlated` |
| `statistical_criterion` | `least_squares;goodness_of_fit;type_I_error` |
| `statistical_guarantee` | `simulation_based` |
| `finite_sample` | `no` |
| `uniform_or_worst_case` | `no` |
| `minimax` | `no` |
| `converse_or_impossibility` | `no` |
| `structural_alternatives` | `yes` |
| `multiple_experiments` | `no` |
| `non_iid` | `yes` |
| `sample_size_design` | `no` |
| `replicate_type` | `none` |
| `model_misspecification` | `yes` |
| `software` | `omfapy` |
| `principal_result` | A covariance-aware GLS/t-test plus balanced-flux simulation diagnostic exposes poor traditional MFA fit despite an acceptable chi-square residual check; a modified balance structure improves simulated and observed flux significance. |
| `authors_stated_limitations` | Model correction is outside scope; the demonstrated analysis is traditional MFA, and applicability to other MFA formulations is stated as likely rather than shown. |
| `reviewer_assessed_limitations` | No EMU observation model, calibrated mechanism selection, prospective design, finite-sample guarantee, minimax protection or converse. |
| `novelty_claim_affected` | `GAP-06` |
| `relevance` | `adjacent` |
| `verification_status` | `fully_verified` |
| `evidence_location` | Methods “Theoretical principles” offsets 9303–16008, Equations 7 and 19; Methods “Flux estimation” offsets 19513–20514; Methods “Implementation” offsets 20514–21048; Results “Identification of model error” offsets 23604–26937, Figure 2; Results “Effect of measurement noise” offsets 27544–30082, Figure 3; Results “Effect of model structure” offsets 30820–33701, Figures 4–6; Conclusion offsets 39449–40312. |
| `notes` | Complete PMC BioC primary XML inspected 2026-07-31. Conventional t-test calibration was not recoded as a review-level finite-sample decision guarantee. |
| `criterion_family` | `other` |
| `guarantee_regime` | `simulation_based` |
| `robustness_scope` | `model_misspecification` |
| `converse_type` | `none` |
| `stopping_rule` | `fixed_sample` |
| `structural_alternative_subtype` | `other` |
| `parameter_sharing` | `unspecified` |
| `retrieval_status` | `retrieved_full_text` |
| `access_status` | `open_access` |
| `full_text_inspected` | `yes` |
| `screening_disposition` | `retained` |
| `exclusion_reason` | `NA` |

`non_iid = yes` is limited to the paper's explicit covariance-aware GLS
error formulation; it is not a claim about heterogeneous multi-condition
isotope experiments. `structural_alternatives = yes` is limited to the
reported original-versus-modified balance structure in the CHO example; it
is not mechanism-discrimination error control.

## Closure interpretation

The bounded Crossref and two anchor citation passes add one consequential
primary method, P0045. It strengthens evidence that metabolic model-error
diagnostics exist, but introduces no EMU-specific robust/minimax design,
finite-sample mechanism-discrimination guarantee, or converse. The 27
discovery-only leads are conventional specification tests, atom-mapping
curation methods, and related metabolic diagnostics; none was used to make a
definitive claim without full-text inspection.
