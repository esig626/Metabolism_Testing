# Phase 2A Workstream C handoff

## Audit outcome

Workstream C is internally reproducible and ready for central synthesis with
the row corrections below. No Phase 1 file, corpus file, or shared synthesis
file was modified by this audit.

- Prospective records: **760**.
- Ledger-local deduplication groups: **633**.
- Full-text included: **8**.
- Title/abstract included for discovery: **124**.
- Title/abstract excluded with reasons: **501**.
- Duplicates: **127**.
- Missing reasons among prospective exclusions: **0**.
- Raw JSON snapshots parsed successfully: **34**.
- Screening ledger reproduced byte-for-byte from
  `audit/phase2_raw_search_results/C/build_screening.pl`.

## Load-bearing evidence

| Evidence key / proposed row | Primary result used | Exact location | Guarantee interpretation |
|---|---|---|---|
| C-LB01 / P0038 | T-optimal design as best uniform approximation; support characterisation; analogous KL criterion | Section 2 equation (2.3), Theorems 2.1–2.2 and equations (2.7)–(2.9); Section 3 Theorem 3.1 and Corollary 3.2; Section 4 equations (4.1)–(4.2); Section 5 | Exact design characterisation; simulated rejection probabilities. Not a local-asymptotic error guarantee. |
| C-LB02 / P0039 | Initial condition, input profile and structural/intervention design maximise rival biochemical-network output distance | Results and Discussion, “Problem formulation,” equations (1)–(3), and the three design subsections; Conclusions | Deterministic optimisation plus numerical examples; no direct noise model, error control, replication certificate or converse. |
| C-LB03 / P0040 | Prior-averaged Bayesian T criterion, equivalence theorem and convergent construction algorithm | Section 2 equations (2.3)–(2.6), Theorem 2.1; Section 3 Algorithm 3.2 and Theorem 3.3; Section 4 | Exact criterion/equivalence and algorithmic convergence. Not posterior calibration or statistical asymptotics. |
| C-LB04 / P0041 | Least-favourable laws and minimax tests over dominated distributional neighbourhoods; analytic failures of proposed sequential robustifications | Sections II–III, especially the uncertainty classes and saddle equations; Section IV Cramér fixed-sample asymptotics; Section V minimax conditions/counterexamples; Conclusion | Minimax/worst-case with fixed-sample large-deviation and sequential asymptotic statements. No exact finite-sample certification. |
| C-LB05 / P0042 | Nonasymptotic expected-stopping lower bound; finite-sample delta-risk threshold; asymptotic sample-complexity optimality | Section 2.1 Theorem 1 and equation (1); Section 4 Theorem 10; Section 5 Theorem 14 | Nonasymptotic converse and risk control plus global asymptotics, for finite one-parameter exponential-family arms and sequential sampling. |
| C-LB06 / P0043 | Composite-null e-values, heterogeneous conditional batches and anytime Type-I control; nuisance-aware growth optimality | Equation (1); Proposition 1 and equation (3); Definition 1; Proposition 2; Corollary 1 and equation (7); full Theorem 1 in Section 4.3, equations (25)–(27) | Exact finite-sample Type-I control conditional on e-validity. No uniform Type-II, replicate sufficiency or converse. |
| C-LB07 / P0044 | Binary KL-neighbourhood minimax saddle and least-favourable laws | Section II equations (2.2)–(2.7); Section III equations (3.1)–(3.12); Section IV | Exact single-observation minimax saddle under stated dominated/symmetry conditions; no experimental design or finite-replicate two-error certificate. |
| P0024 | Continuous-parameter minimax KL design; continuity and algorithm convergence | Equations (1)–(5); Theorem 1; Assumptions 1–2 and Theorem 2; Sections 4–5 | Worst-case criterion over a continuous alternative-parameter set and algorithmic convergence, not finite-sample decision error. |
| P0026 | Fixed-sample controlled-sensing error exponents and sequential results for finite simple hypotheses | Section II; Proposition 1 equations (6)–(8); Theorems 1–2 equations (9)–(11); sequential Section IV and Theorems 3–5 | Error-exponent/converse and sequential asymptotic results; finite simple hypotheses with known action kernels. |
| P0027 | Bayesian active sequential testing cost bounds | Sections 2–3; Proposition 1; Propositions 2–5 and assumptions stated with each | Nonasymptotic Bayesian cost bounds and asymptotic policy comparisons for finite simple hypotheses. |
| P0028 | Sequential controlled sensing for disjoint composite exponential-family hypotheses | Section II assumptions; Lemma 1 equations (17)–(18); Proposition 1; Theorems 1–3 equations (20)–(22) | Nonasymptotic expected-delay lower bound and error correctness plus asymptotic optimality, under disjoint regular composite classes. |
| P0029 | Bayesian and standardized-maximin robust T criteria | Sections 2–3 equations (3)–(6); Theorem 4.1; Section 5.3–5.4 simulation | Exact robust criterion/design solutions for specified regression parameter uncertainty; power evidence is simulation-based. |

## Corpus row proposals

These are proposals only; this workstream did not edit `corpus/papers.csv`.

| Row | Proposed action | Reason |
|---|---|---|
| P0038 | Remove `local_asymptotic` from `guarantee_regime`; retain `simulation_based` for Section 5 and describe theorems as exact criterion characterisations. | The paper does not prove a local-asymptotic decision-error guarantee. |
| P0039 | Correct URL from `PMC2864213` to `https://pmc.ncbi.nlm.nih.gov/articles/PMC2873315/`; remove `T_optimality` from `criterion_family` unless explicitly defined as an analogy; retain `other` for L2 output separation. | The current PMC identifier is inconsistent with the verified DOI/full text. The method maximises deterministic L2 output separation and does not invoke the formal T criterion. |
| P0040 | Set `statistical_guarantee=none` and `guarantee_regime=none`; do not code algorithmic convergence as `global_asymptotic` or prior averaging as `Bayesian_posterior`. | Theorem 3.3 is computational convergence; no posterior-error or statistical asymptotic result is supplied. |
| P0041 | Set `structural_alternatives=no` and `structural_alternative_subtype=NA`; retain `model_misspecification=yes`, distributional robustness and the Section V counterexample/converse coding with its exact location. | Binary distributional hypotheses under ambiguity are not necessarily structural network/mechanism alternatives. |
| P0042 | Retain finite-sample, sample-size, non-IID/action-dependent and sample-complexity-converse coding; retain DOI as `NR`. | Theorems 1 and 10 directly support the strong fields; Theorem 14 is asymptotic. PMLR supplies no DOI. |
| P0043 | Set `structural_alternatives=no`, `structural_alternative_subtype=NA`, and `parameter_sharing=unspecified`; retain exact finite-sample Type-I and multiple-experiment/non-IID conditional-batch coding. | General composite hypotheses and nuisance parameters do not establish a structural mechanism alternative or a particular cross-condition sharing scheme. |
| P0044 | Set `structural_alternatives=no`, `structural_alternative_subtype=NA`; use `criterion_family=likelihood;other` rather than `KL_optimality`. | KL defines the ambiguity neighbourhood, not a KL-optimal experimental-design criterion; the paper compares distributional hypotheses rather than structural mechanisms. |

## Transfer classifications

| Family | Classification | Precise residual obstruction |
|---|---|---|
| T-optimal design | APPLICABLE WITH COMPUTATIONAL ADAPTATION | Nonlinear constrained inner approximation over feasible flux sets; no finite-sample error certificate. |
| KL-optimal design | APPLICABLE WITH COMPUTATIONAL ADAPTATION | Nested maximin computation over nonlinear feasible sets; overlap can force worst-case KL to zero. |
| Bayesian discrimination | APPLICABLE WITH COMPUTATIONAL ADAPTATION | High-dimensional prior integration and prior dependence; no uniform frequentist guarantee. |
| Robust/maximin discrimination | REQUIRES A NONTRIVIAL THEORETICAL EXTENSION | Uniform two-error risk over continuous structural alternatives with shared nuisance and detectable-separation conditions is not implied by robust criterion ranking. |
| Active hypothesis testing | REQUIRES A NONTRIVIAL THEORETICAL EXTENSION | Existing load-bearing result uses finite simple hypotheses and observation-by-observation sequential action. |
| Controlled sensing | REQUIRES A NONTRIVIAL THEORETICAL EXTENSION | Existing exponent/converse theory assumes finite simple hypotheses with known action kernels. |
| Composite controlled sensing | REQUIRES A NONTRIVIAL THEORETICAL EXTENSION | P0028 requires disjoint regular exponential-family composite classes; EMU classes may overlap or be singular and share nuisance across blocks. |
| Heterogeneous conditional batches | REQUIRES A NONTRIVIAL THEORETICAL EXTENSION | Type-I combination transfers from C-LB06, but uniform Type-II/sample-size control and a converse under coupled shared and condition-specific nuisance do not. |
| Distributionally robust testing/design | REQUIRES A NONTRIVIAL THEORETICAL EXTENSION | Dominated binary ambiguity testing transfers; joint optimisation of EMU design and least-favourable structural/noise laws with two-error guarantees does not. |
| Fixed-sample minimax composite testing | UNRESOLVED FROM CURRENT EVIDENCE | No verified source jointly supplies fixed biological replication, continuous structural EMU alternatives, both-error uniform control and a matching converse. |
| Nonnested/overlapping likelihood testing | UNRESOLVED FROM CURRENT EVIDENCE | Vuong-family candidates remain discovery-level; exact overlap is an identifiability obstruction, while quantitative near-overlap under prospective design is unresolved. |

## Search closure and access

PHASE2-SEARCH-0080/0081 and 0082/0083 are consecutive bounded,
distinct-source query pairs; their exported windows added no load-bearing
family. PHASE2-SEARCH-0067/0068 preserve bounded backward and forward
citation networks for the composite controlled-sensing and
minimax-robust-testing anchors. Workstream C is
`ANCHOR_FAMILIES_VERIFIED` for the positive method families listed above,
but the truncated searches do not establish exhaustive coverage.

Atkinson–Fedorov (1975), Chernoff (1959), and the candidate Vuong-family
papers were not promoted to load-bearing because complete primary text was
not inspected in this workstream. Later verified primary sources support the
criterion and sequential/converse statements used here. No definitive claim
depends on those inaccessible/discovery-only records.

## Controlling evidence-boundary correction

The `REQUIRES A NONTRIVIAL THEORETICAL EXTENSION` classifications above are
preserved as the original workstream handoff but are not controlling
Phase 2A.1 conclusions. They compared the EMU target only with the selected
workstream anchors and therefore cannot establish that no existing adjacent
result covers the target. Under `protocol/phase2b_evidence_boundary.md`, the
active/controlled/sequential, composite controlled-sensing, heterogeneous
shared-nuisance and distributionally robust family-level classifications are
`UNRESOLVED FROM CURRENT EVIDENCE` unless a claim is explicitly limited to
extending one cited anchor. The controlling classifications are in
`analyses/adjacent_method_transfer.md`.
