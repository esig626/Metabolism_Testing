# Phase 2A Workstream B audit handoff

Date: 2026-07-31 UTC  
Scope: metabolic model validation/discrimination and its nearest biochemical
design methods. No Phase 1 file was changed.

## Audit result

The separate B audit ledger contains 203 prospectively dispositioned
bibliographic search/retrieval occurrences plus one verified software record
discovered through the fully inspected P0049 paper. The 204 rows carry 184
ledger-local deduplication groups. States:

| Screening state | Count |
|---|---:|
| `FULL_TEXT_INCLUDED` | 6 (five papers and one software record) |
| `TITLE_ABSTRACT_INCLUDED` | 14 |
| `TITLE_ABSTRACT_EXCLUDED` | 153 |
| `DUPLICATE` | 31 |
| Total | 204 |

Evidence levels are 6 load-bearing, 1 supporting and 197 discovery-only.
Every prospective exclusion has a reason. Database/export occurrence counts
by query are:

| Query | Occurrences |
|---|---:|
| PHASE2-SEARCH-0100 | 50 |
| PHASE2-SEARCH-0101 | 64 |
| PHASE2-SEARCH-0102 | 59 |
| PHASE2-SEARCH-0110 | 10 |
| PHASE2-SEARCH-0111 | 9 |
| PHASE2-SEARCH-0112 | 5 |
| PHASE2-SEARCH-0113 | 1 |
| PHASE2-SEARCH-0114 | 3 |
| PHASE2-SEARCH-0115 | 2 (one paper retrieval and one distinct software record) |
| PHASE2-SEARCH-0116 | 1 |

The five newly verified Level-1 papers are Borah Slater et al. (2023), Liu
et al. (2026), Flassig and Sundmacher (2012), Stegmaier et al. (2013), and
Vanlier et al. (2014). Existing P0030–P0032 were also re-inspected at the
method/result level; they appear as corpus duplicates in the new occurrence
ledger.

## Corrections required in existing corpus rows

### P0030

- Change `criterion_family` from `likelihood;other` to `other`. The proposed
  held-out-tracer selection criterion is weighted validation SSR; likelihood,
  chi-square, AIC and BIC are fitting/comparator machinery.
- Remove `compartment_structure` from
  `structural_alternative_subtype`. The inspected evaluated candidates differ
  by reaction/pathway inclusion; no evaluated compartment alternative was
  found.
- Replace the principal-result phrase “simulation-robust” with wording that
  says selection was evaluated under a finite set/range of assumed
  measurement-error rescalings. The seven-model simulation selected the
  generating model only about 60–70% of the time.
- Clarify that `model_misspecification=yes` and
  `robustness_scope=model_misspecification;finite_scenario_set`, if retained,
  refer to empirical sensitivity to the *working measurement-error scale*,
  not a forward-network misspecification guarantee.
- Expand `evidence_location` to: Results §2 passage after Table 1; Results
  §§2.3–2.5; Figures 4, 6 and 8; Methods §§4.1 and 4.5; Discussion passages
  on MID error dependence, non-identically distributed tracer validation,
  and “Model selection versus model testing.”
- `non_iid=yes` is supported only with that Discussion location: the authors
  explicitly distinguish tracer blocks generated from different
  distributions. `parameter_sharing=shared_across_conditions` is supported
  by Methods §4.1 for the jointly fitted tracer datasets.

### P0031

- Keep no guarantee/converse coding. “Undecided” Figure 1 probabilities are
  posterior ambiguity, not impossibility.
- Expand `evidence_location` to Approach §2.2 equations 2–6; Algorithms 1–2;
  Results §§4.1–4.2; Figure 1.
- Clarify `structural_alternative_subtype=reaction_presence_absence` as
  presence/absence of the exchange-flux component (bidirectionality), not
  presence/absence of the underlying reaction topology.
- `parameter_sharing=partially_shared` is supported: net-flux coordinates
  persist across variants while exchange-flux coordinates are
  model-specific.

### P0032

- Expand `evidence_location` to §§2.2–2.4 equations 2–5; Algorithm 1;
  §§4.1–4.2, especially §4.2.2; Appendix §§B.2–B.4; Conclusion.
- Make the limitation explicit: §2.4 assumes a sufficiently comprehensive
  candidate space; posterior support is relative and does not guarantee that
  one enumerated structure is correct. The three-ILE result is synthetic and
  computationally expensive.
- Keep finite-sample, minimax, uniform and converse fields `no`; keep preprint
  status.

### P0033 and consolidated screening

P0033 remains abstract-only. Its originating root occurrence is now
`TITLE_ABSTRACT_INCLUDED`/`LEVEL_2_SUPPORTING`; no correction-only row is
counted as a new discovery. P0033 must not support a definitive structural or
guarantee statement.

### Verified software record

`B-AUDIT-SOFTWARE-0001` records ModelDiscriminationToolkitGUI as a distinct
software item discovered in and verified against the P0049 primary paper and
official SourceForge project. It maps to S0017 and is not counted as a second
bibliographic paper occurrence.

## Integrated new corpus evidence rows

Cross-workstream synthesis allocated stable IDs P0047–P0051. The descriptions
below preserve the workstream extraction supporting those curated rows.

### P0047 — Borah Slater et al. 2023 — direct isotope application

- Citation: Borah Slater K, Beyß M, Xu Y, et al. One-shot
  ^13C^15N-metabolic flux analysis for simultaneous quantification of carbon
  and nitrogen flux. *Molecular Systems Biology*. 2023;19:e11099.
- DOI/URL: `10.15252/msb.202211099`;
  `https://pmc.ncbi.nlm.nih.gov/articles/PMC9996240/`.
- Decision: infer fluxes and posterior reaction-bidirectionality/model
  probabilities from biological carbon/nitrogen co-labeling data.
- Suggested core coding:
  `13C_MFA`; `steady_state_MFA;general_nonlinear`; `MID;MS`;
  object `flux;model_structure`; design `none`; uncertainty
  `flux;structure;measurement_noise`; formulation `Bayesian`;
  criterion `posterior_risk;likelihood`; family
  `Bayesian_discrimination;posterior`; guarantee
  `Bayesian_posterior`; regime `none`; robustness
  `structural_uncertainty_set`; structural alternatives `yes`;
  subtype `reaction_presence_absence` with a bidirectionality note;
  finite-sample/uniform/minimax/converse/sample-size `no`;
  `multiple_experiments=no`; `non_iid=no`; relevance `direct`.
- Result: Bayesian model averaging is applied to real BCG co-labeling data
  and reports model-averaged flux posteriors and reaction-bidirectionality
  probabilities.
- Exact evidence: Results “Roadmap for Bayesian multi-model
  13C15N-metabolic flux analysis,” equation 1 and Figure 2; Results Figures
  3–6 and Appendix Figure S7; Materials and Methods “Flux inference with
  Bayesian Model Averaging”; Discussion and network-scope limitation.
- Limit: one specified structural family and condition; no decision-error,
  power, replicate-allocation, minimax or converse result.

### P0048 — Flassig and Sundmacher 2012 — probabilistic robust discrimination design

- Citation: Flassig RJ, Sundmacher K. Optimal design of stimulus experiments
  for robust discrimination of biochemical reaction networks.
  *Bioinformatics*. 2012;28:3089–3096.
- DOI/URL: `10.1093/bioinformatics/bts585`;
  `https://pmc.ncbi.nlm.nih.gov/articles/PMC3516143/`.
- Decision/design: distinguish nonlinear biochemical ODE mechanisms by
  optimizing stimulus, measurement times and readouts under parameter
  distributions.
- Suggested core coding:
  domain `systems_biology;optimal_design`; model
  `kinetic;general_nonlinear`; observation `time_course;synthetic`; object
  `model_structure;mechanism`; design
  `time_points;measurement_panel;perturbation`; uncertainty
  `kinetic_parameter;measurement_noise;biological_heterogeneity`;
  formulation `probabilistic_frequentist`; dependencies `correlated`;
  criterion `other`; family `other`; guarantee
  `simulation_based`; regime `simulation_based`; robustness
  `distributional_uncertainty`; structural alternatives `yes`; subtype
  `kinetic_mechanism`; finite-sample/uniform/minimax/converse/sample-size
  `no`; relevance `adjacent`.
- Exact evidence: §§2.2–2.3 equations 5 and 8–11; §2.4 sigma-point
  approximation; §2.5 local non-convex optimal-control solutions; §3 Table 1
  and Figures 2–3; Conclusion.
- Limit: specified parameter PDFs and moment approximation; global design
  optimality not ensured; no calibrated decision rule.

### P0049 — Stegmaier, Skanda and Lebiedz 2013 — max–min biochemical design

- Citation: Stegmaier J, Skanda D, Lebiedz D. Robust Optimal Design of
  Experiments for Model Discrimination Using an Interactive Software Tool.
  *PLOS ONE*. 2013;8:e55723.
- DOI/URL: `10.1371/journal.pone.0055723`;
  `https://pmc.ncbi.nlm.nih.gov/articles/PMC3563641/`.
- Decision/design: maximize the worst-case separation of competing
  biochemical ODE mechanisms over bounded kinetic-parameter regions by
  selecting initial concentrations, perturbations and measurement times.
- Suggested core coding:
  domain `systems_biology;optimal_design;scientific_software`; model
  `kinetic;general_nonlinear`; observation `time_course;synthetic`; object
  `model_structure;mechanism`; design `time_points;perturbation;condition`;
  uncertainty `kinetic_parameter;structure;measurement_noise`; formulation
  `set_valued;adversarial`; criterion `KL_divergence;minimax_risk`; family
  `KL_optimality`; guarantee `simulation_based;worst_case;minimax`; regime
  `simulation_based`; robustness `continuous_parameter_set`;
  `uniform_or_worst_case=yes`; `minimax=yes`; structural alternatives `yes`;
  subtype `kinetic_mechanism`; finite-sample/converse/sample-size `no`;
  software `ModelDiscriminationToolkitGUI`; relevance `adjacent`.
- Exact evidence: Methods equation 1; “Robust optimal designs,” equations
  4–5; full semi-infinite formulation; Results KL histograms and F-test
  examples; Conclusion.
- Limit: nested derivative-based optimization and restarts do not certify a
  global continuous-class optimum; simulated F-tests do not turn the design
  objective into controlled finite-sample error. Authors state that no
  general recipe follows from the examples.

### P0050 — Vanlier et al. 2014 — Bayesian posterior-predictive measurement design

- Citation: Vanlier J, Tiemann CA, Hilbers PAJ, van Riel NAW. Optimal
  experiment design for model selection in biochemical networks. *BMC
  Systems Biology*. 2014;8:20.
- DOI/URL: `10.1186/1752-0509-8-20`;
  `https://pmc.ncbi.nlm.nih.gov/articles/PMC3946009/`.
- Decision/design: rank observable, time, condition and small measurement
  combinations for Bayesian selection among biochemical mechanisms.
- Suggested core coding:
  domain `systems_biology;optimal_design`; model
  `kinetic;general_nonlinear`; observation `time_course;synthetic`; object
  `model_structure;mechanism;measurement_panel`; design
  `measurement_panel;time_points;condition`; uncertainty
  `kinetic_parameter;structure;measurement_noise`; formulation `Bayesian`;
  dependencies `independent;shared_nuisance`; criterion
  `mutual_information;KL_divergence;posterior_risk`; family
  `Bayesian_discrimination`; guarantee
  `Bayesian_posterior;simulation_based`; regime `simulation_based`;
  robustness `distributional_uncertainty`; structural alternatives `yes`;
  subtype `kinetic_mechanism`; multiple experiments `yes`;
  finite-sample/uniform/minimax/converse/sample-size `no`; relevance
  `adjacent`.
- Exact evidence: Methods “Predictive Distributions,” “Model selection,”
  “Experimental design,” and JSD equations; Results Figures 6–9 and Table 1;
  Conclusion limitations.
- Limit: MCMC and density-estimation burden; degradation with dimension and
  exponential growth of experiment combinations; ranking rather than a
  frequentist sufficiency/impossibility certificate.

### P0051 — Liu, Maini and Baker 2026 — fixed-parameter perturbation design

- Citation: Liu Y, Maini PK, Baker RE. Optimal experiment design for
  practical parameter identifiability and model discrimination.
  *Mathematical Biosciences*. 2026;399:109710.
- DOI/URL: `10.1016/j.mbs.2026.109710`;
  `https://doi.org/10.1016/j.mbs.2026.109710`. Peer-reviewed final metadata
  was verified from the publisher and Oxford repository; the complete arXiv
  manuscript was inspected.
- Decision/design: optimize an external control either for profile-likelihood
  parameter identifiability or for separation of two known-parameter ODE
  mechanisms.
- Suggested core coding:
  domain `systems_biology;optimal_design`; model
  `kinetic;general_nonlinear`; observation `time_course;synthetic`; object
  `parameter;model_structure;mechanism`; design `perturbation`; uncertainty
  `kinetic_parameter;structure` with notes separating the two branches;
  formulation `probabilistic_frequentist;none`; criterion
  `confidence_region;other`; family `other`; guarantee `simulation_based`;
  regime `simulation_based`; robustness `none`; structural alternatives
  `yes`; subtype `kinetic_mechanism;mechanism_class`;
  finite-sample/uniform/minimax/converse/multiple-experiment/non-IID/
  sample-size `no`; relevance `adjacent`.
- Exact evidence: Introduction §§1.2–1.3; Section 3 equations 18–19 and
  examples; Discussion fixed-parameter/control limitations.
- Limit: model discrimination assumes fixed parameter sets, a known
  control-to-system action and noiseless continuous-time output for the
  optimization; sample timing is fixed; no decision-error calibration.

## Transfer and search-closure assessment

The direct MFA citation network is substantially closed for the narrow
structural-method question: saved P0030 and P0031 backward/forward passes
added the Borah Slater biological application but no new direct
EMU-specific calibrated-testing family. Four P0030 references and one P0031
reference were unresolved by OpenAlex and are documented as such.

The broader biochemical field is decisively *not* empty. The verified prior
methods already provide:

- probabilistic parameter-robust response-overlap design;
- explicit max–min parameter-robust mechanism design;
- Bayesian posterior-predictive measurement/condition design; and
- fixed-parameter perturbation/control design.

Transfer of those objectives to an EMU observation model is
`APPLICABLE WITH COMPUTATIONAL ADAPTATION`. The residual obstacles are
precise: repeated nonlinear EMU inference within non-convex nested design
optimization; potentially overlapping composite observation families with
shared nuisance fluxes; no certified global max–min solution; and no mapping
from separation criteria to finite-sample two-error/sample-size guarantees.
Those are not evidence that biochemical mechanism design itself is absent.

Workstream B is `ANCHOR_FAMILIES_VERIFIED` for the affirmative conclusion
that biochemical mechanism-design and direct isotope structural-comparison
methods exist. It is not exhaustively searched for the stronger
cross-workstream finite-sample/composite-EMU question, and P0033 remains an
access gap. The verified five-paper set is a nearest-prior-work baseline; the
conclusion does not rely on treating deferred records as negative evidence.

## Files owned by this audit

- `analyses/phase2_model_discrimination.md`
- `audit/phase2_search_log_B.md`
- `audit/phase2_screening_B_audit.csv`
- `audit/phase2_raw_search_results/B/README.md`
- `audit/phase2_raw_search_results/B/PHASE2-SEARCH-0100_crossref.json`
- `audit/phase2_raw_search_results/B/PHASE2-SEARCH-0101_*`
- `audit/phase2_raw_search_results/B/PHASE2-SEARCH-0102_*`
- `audit/phase2_raw_search_results/B/PHASE2-SEARCH-0110-0112_web_snapshot.json`
- `audit/phase2_raw_search_results/B/PHASE2-SEARCH-0112_Liu-arxiv-fulltext.html`
- `audit/phase2_raw_search_results/B/PHASE2-SEARCH-0113_*`
- `audit/phase2_raw_search_results/B/PHASE2-SEARCH-0114_*`
- `audit/phase2_raw_search_results/B/PHASE2-SEARCH-0115_*`
- `audit/phase2_raw_search_results/B/PHASE2-SEARCH-0116_*`
- `scripts/build_phase2_screening_B_audit.pl`

The shared corpus, shared synthesis, consolidated Phase 2 ledger and every
Phase 1 audit file were intentionally left for parent integration.
