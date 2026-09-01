# Phase 2A.1 priority-18 closure handoff

Date: 2026-07-31  
Scope: the 10 `LOAD_BEARING` and 8 `POTENTIALLY_LOAD_BEARING` records in
`audit/phase2_unresolved_triage.csv`. This handoff does not modify
`audit/phase2_screening.csv` or `corpus/papers.csv`.

**Controlling correction:** this is the evidence-review handoff produced
before root integration and before the scoped-disposition repair. The three
included papers have since been assigned P0074, P0071, and P0065. C0405 and
C0480 remain relevant adjacent asymptotic evidence and are now
`DEFERRED_RELEVANT_ADJACENT`, not false positives for the broader review.
The historical dispositions in
`audit/phase2a1_priority18_closure.csv` remain preserved; current states are
controlled by `audit/phase2_unresolved_triage.csv` and
`audit/phase2a1_deferred_records.csv`.

## Closure result

All 18 records have a final screening disposition in
`audit/phase2a1_priority18_closure.csv`. None remains in an included,
awaiting-verification, or unresolved screening state.

| Final disposition | Count | Records |
|---|---:|---|
| `FULL_TEXT_INCLUDED` | 3 | C0650, C0652, C0656 |
| `FULL_TEXT_EXCLUDED` | 2 | C0492, C0664 |
| `DEFERRED_RELEVANT_ADJACENT` | 2 | C0405, C0480 |
| `FULL_TEXT_UNAVAILABLE` | 11 | C0136, C0231, C0235, C0241, C0242, C0283, C0285, C0286, C0402, C0483, C0653 |
| `DUPLICATE` | 0 | — |

`UNRESOLVED FROM CURRENT EVIDENCE` appears only as a transfer
classification for inaccessible papers. It is not a screening disposition.
Those papers have the final disposition `FULL_TEXT_UNAVAILABLE` and cannot
support a substantive synthesis claim.

## Exact dispositions and evidence locations

### Full-text inclusions

- **C0650 — Gül and Zoubir (2013), DOI
  10.1109/ICASSP.2013.6638718.** `FULL_TEXT_INCLUDED`. Primary proceedings
  copy inspected at the University of Zaragoza ICASSP archive. Evidence:
  pp. 5514–5518; Section 2.1, equations (1)–(6), defines the two
  squared-Hellinger neighbourhoods, false-alarm and miss probabilities, and
  minimax Bayes-error problem; Sections 2.2–2.3 derive the least-favourable
  laws and robust likelihood-ratio rule; Section 4 concludes. The result is
  an exact one-observation minimax construction for a special dominated
  distributional-uncertainty class, not an EMU experiment-design or
  sample-complexity result.

- **C0652 — Gül and Zoubir (2014), DOI 10.5281/zenodo.54502.**
  `FULL_TEXT_INCLUDED`. Official EURASIP proceedings PDF inspected.
  Evidence: Section 2.1, equations (1)–(6), defines the Hellinger classes and
  minimax problem; Sections 2.2–3 derive and computationally reduce the
  least-favourable construction; Section 4, equations (23)–(36), derives
  maximum robustness radii; Figure 1 and Section 5 identify parameter regions
  in which the least-favourable laws overlap and a minimax robust test cannot
  be designed; Section 6 concludes. This is exact finite-sample minimax and
  exact-overlap evidence, but not a sample-size or tracer-design converse.

- **C0656 — Gül and Zoubir (2016), DOI
  10.1109/TSP.2016.2569405.** `FULL_TEXT_INCLUDED`. Complete arXiv v3 author
  manuscript linked to the published DOI inspected. Evidence: Section II-A,
  equations (1)–(7), defines dominated alpha-divergence balls and three error
  criteria; Section II-B, equations (8)–(10), establishes the saddle
  formulation; Theorem III.1 and equations (15)–(20) provide the unique
  least-favourable laws and robust rule; Section III-C derives the
  maximum-robustness/overlap boundary; Figure 10 and Section V state
  nonexistence beyond that boundary. Theorem III.1 is valid for a fixed finite
  observation vector through its joint law; it does not exploit an
  independent-replicate structure or optimise the number or composition of
  observations.

### Full-text exclusions

- **C0492 — Rois, Basak and Majumder (2012), DOI
  10.5539/ijsp.v1n2p69.** `FULL_TEXT_EXCLUDED`. Official CCSE full text
  inspected. Section 2 defines the Gaussian regression/AR(p) problem;
  Section 3.1 assumes asymptotic normality; equations (3.2.4) and (3.3.1) use
  asymptotic chi-square or weighted-mixture null distributions; Section 5
  reports 5,000-run Monte Carlo power at n=50. Exclusion reason: the result is
  narrow, asymptotically calibrated, and simulation-supported rather than a
  foundational nonasymptotic composite test.

- **C0664 — Demortier (2008), DOI 10.5170/CERN-2008-001.23.**
  `FULL_TEXT_EXCLUDED`. CERN proceedings text inspected. The abstract and
  Section 1 identify a review; Section 3 reviews supremum/confidence-set,
  bootstrap, and predictive treatments of nuisance parameters; Section 4,
  equation (29), is explicitly asymptotic; Section 5 summarizes. Exclusion
  reason: expository/secondary review, not an original load-bearing theorem.

### Deferred adjacent asymptotic records

- **C0405 — Wefelmeyer (1987), DOI
  10.1007/978-94-009-3963-9_20.** `DEFERRED_RELEVANT_ADJACENT`. The
  publisher-supplied abstract explicitly states asymptotic smoothness and an
  asymptotic power bound under contiguous alternatives. The full chapter is
  paywalled. It is relevant to non-IID asymptotic theory, but not to the
  registered fixed-sample nonasymptotic question.

- **C0480 — Li (2001), DOI 10.1016/S0378-3758(00)00345-1.**
  `DEFERRED_RELEVANT_ADJACENT`. The official ScienceDirect abstract/preview
  describes local sensitivity using Edgeworth expansions and order-n^-1
  terms under local alternatives. The full paper is paywalled. It cannot
  support a finite-sample guarantee or converse.

### Full text unavailable

- **C0402 — Birgé (1983), DOI 10.1007/978-1-4612-5503-1_9.**
  Springer and recognised repository/author routes yielded no legal open
  copy. No theorem was inspected. This is the one inaccessible record most
  likely to bear on heterogeneous independent non-identically distributed
  robust tests. Request manual/library retrieval only if the other
  foundational full-text anchors do not close that family.

- **C0483 — Bernshtein (1981), DOI 10.1137/1125037.** SIAM is
  paywalled; Math-Net/original-language bibliographic routes did not yield
  inspectable primary text. Its references and neighbouring author
  bibliography are heavily asymptotic, but that is not enough to classify
  the paper's actual result. No fixed-sample or converse field may be coded.

- **C0283, C0285 and C0286 — Gül (2017) book chapters.** Springer and
  author/dissertation routes yielded no open chapter text. P0041 and the
  verified primary papers C0650/C0652/C0656 cover much of the underlying
  method family, so these chapters are supporting rather than necessary.
  Their table-of-contents section titles are not theorem evidence.

- **C0653 — Gül and Zoubir (2014), DOI
  10.1109/SSP.2014.6884668.** IEEE/proceedings and recognised repository
  routes yielded only metadata and abstract. The abstract's least-favourable
  distribution claim remains unverified. P0041 and C0656 establish the broad
  robust-composite family but not this exact two-distance construction.

- **C0235 — Jurečková and Navrátil (2013), DOI
  10.1007/s00184-013-0447-7.** Springer and author/repository routes
  yielded the abstract but no full text. It describes ancillary-statistic
  nuisance handling in a heteroscedastic regression model, with simulations;
  no exact uniform-error theorem was verified.

- **C0231 — Linnik (1968), DOI 10.1090/mmono/020/04.** AMS and
  limited-preview routes did not expose the chapter. The title cannot
  establish exact similarity, uniform nuisance control, or computation.

- **C0241 and C0242 — Lapidoth (2009/2017), textbook chapters.**
  Cambridge and the official ETH book pages expose bibliographic information
  only. The editions remain related but were not coded as duplicates because
  their mathematical identity was not verified.

- **C0136 — Zarrin and Lim (2009), DOI
  10.1109/ICC.2009.5198841.** The exact conference paper remains
  unavailable. The authors' open 2010 journal extension (DOI
  10.1109/TSP.2010.2045425) was inspected: Section III equations (8)–(21)
  explicitly use MLE consistency and an asymptotically equivalent GLRT;
  Sections IV–V use approximations and simulation. These verified properties
  must not be imputed backward to the inaccessible conference record.

## Consequences for GAP-01 and GAP-03

The three included Gül–Zoubir papers destroy a broad version of GAP-01:
exact finite-sample minimax tests do exist for composite-versus-composite
hypotheses when each class is a specified convex divergence neighbourhood of
a dominated nominal law. They also give computable least-favourable-pair
constructions for those classes.

They do not by themselves solve the exact metabolic formulation. An
EMU-induced family is generally a nonlinear parameter image rather than an
alpha-divergence or Hellinger ball. Direct use therefore requires replacing
or outer-bounding the mechanistic family by a divergence ball. That
approximation can change both the least-favourable pair and the mechanistic
interpretation. Whether the exact nonconvex family is covered is a question
for the foundational-theory synthesis, not an absence claim supported by
these papers.

The overlap boundaries in C0652 and C0656 destroy a broad version of GAP-03:
an exact identifiability/overlap obstruction already exists for these robust
distribution classes. This is not a minimax replicate-count lower bound, a
fixed-budget experimental-design converse, or an EMU-specific insufficiency
certificate.

## Corpus-ready actions

Three new primary rows are warranted; stable IDs must be allocated at
integration time:

| Workstream record | Publication type | Criterion | Guarantee | Converse | Key controlled fields |
|---|---|---|---|---|---|
| C0650 | `conference_paper` | `minimax_risk;type_I_error;type_II_error` | `finite_sample;uniform;worst_case;minimax` | `no` | `criterion_family=likelihood;other`; `guarantee_regime=exact_finite_sample`; `robustness_scope=distributional_uncertainty;model_misspecification`; `converse_type=none`; `stopping_rule=fixed_sample`; `full_text_inspected=yes` |
| C0652 | `conference_paper` | `minimax_risk;type_I_error;type_II_error` | `finite_sample;uniform;worst_case;minimax;converse_impossibility` | `yes` | same as C0650 except `converse_type=identifiability_obstruction`; exact evidence is Section 4 and Figure 1 |
| C0656 | `journal_article` | `minimax_risk;type_I_error;type_II_error` | `finite_sample;uniform;worst_case;minimax;converse_impossibility` | `yes` | `criterion_family=likelihood;other`; `guarantee_regime=exact_finite_sample`; `robustness_scope=distributional_uncertainty;model_misspecification`; `converse_type=identifiability_obstruction`; `stopping_rule=fixed_sample`; `full_text_inspected=yes` |

For all three, use `structural_alternatives=no`, `multiple_experiments=no`,
`non_iid=no`, `sample_size_design=no`, `model_misspecification=yes`,
`parameter_sharing=unspecified`, `retrieval_status=retrieved_full_text`,
`screening_disposition=retained`, and `relevance=adjacent`. Do not code their
fixed vector or single-observation statements as multi-condition or
non-identically distributed inference.

No inaccessible record should be added with a guarantee-level `yes`. C0492
and C0664 should remain excluded from the load-bearing primary corpus; C0405
and C0480 remain qualified adjacent evidence and cannot carry a definitive
fixed-sample claim.
