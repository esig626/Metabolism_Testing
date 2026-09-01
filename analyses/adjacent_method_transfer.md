# Phase 2A Adjacent-Method Transfer to EMU Observation Models

## Scope and interpretation

This is a transfer assessment, not a novelty claim or a grant
recommendation. The target observation family is

`Y_e ~ P(· | h, θ_h, ψ, d_e)`,

where `h` indexes a metabolic structure or mechanism, `θ_h` is
structure-specific flux or kinetic nuisance, `ψ` is nuisance shared across
conditions, and the EMU forward map determines isotope observations under
tracer, fragment, time, perturbation and allocation design `d_e`.

Each family receives exactly one of the registered classifications. A
criterion that can rank EMU experiments is not treated as a finite-sample
decision guarantee. Likewise, a posterior probability, confidence interval,
simulation study or goodness-of-fit test is not treated as a converse.

**Phase 2A.1 evidence boundary:** administrative final dispositions do not
establish that a literature family is exhausted, and title/abstract
false-positive states are not used as negative methodological evidence.
Inspected primary results affirmatively establish general fixed-sample
composite tests, uniform two-error bounds for stated classes,
heterogeneous-product constructions and finite-sample converses. The
remaining EMU-specific issue is certified representation and computation for
nonlinear induced law families. No classification establishes priority or a
grant recommendation.

## Classification summary

| Method family | Phase 2A transfer classification |
|---|---|
| T-optimal model-discrimination design | APPLICABLE WITH COMPUTATIONAL ADAPTATION |
| KL-optimal model-discrimination design | APPLICABLE WITH COMPUTATIONAL ADAPTATION |
| Robust or maximin discrimination design | APPLICABLE WITH COMPUTATIONAL ADAPTATION |
| Bayesian discrimination design | APPLICABLE WITH COMPUTATIONAL ADAPTATION |
| Active hypothesis testing | UNRESOLVED FROM CURRENT EVIDENCE |
| Controlled sensing | UNRESOLVED FROM CURRENT EVIDENCE |
| Sequential experimental design | UNRESOLVED FROM CURRENT EVIDENCE |
| Chernoff testing | UNRESOLVED FROM CURRENT EVIDENCE |
| Composite or compound hypothesis testing | APPLICABLE WITH COMPUTATIONAL ADAPTATION |
| Fixed-sample minimax composite testing | APPLICABLE WITH COMPUTATIONAL ADAPTATION |
| Error-exponent design and converses | APPLICABLE WITH COMPUTATIONAL ADAPTATION |
| Sample-complexity converses | APPLICABLE WITH COMPUTATIONAL ADAPTATION |
| Heterogeneous non-IID or adaptive evidence | APPLICABLE WITH COMPUTATIONAL ADAPTATION |
| Shared-nuisance testing | APPLICABLE WITH COMPUTATIONAL ADAPTATION |
| Nonnested or overlapping model families | APPLICABLE WITH COMPUTATIONAL ADAPTATION |
| Distributionally robust testing and design | APPLICABLE WITH COMPUTATIONAL ADAPTATION |
| Forward-model misspecification | UNRESOLVED FROM CURRENT EVIDENCE |

## T-optimal model-discrimination design

- **Classification:** APPLICABLE WITH COMPUTATIONAL ADAPTATION.
- **Exact existing result:** P0038 defines T-optimality as maximising an
  integrated squared mean separation after fitting the rival model and proves
  best-uniform-approximation and support characterisations. P0029 supplies
  Bayesian and standardized-maximin T criteria under parameter
  misspecification.
- **Proposed metabolic formulation:** replace the rival regression means by
  EMU-predicted isotope vectors and optimise tracer, fragment, time or
  perturbation choices after minimising over feasible nuisance fluxes.
- **What transfers directly:** the outer approximate-design measure, the
  inner best-fit rival calculation and the T-distance ranking objective.
- **What does not transfer:** the regression-specific support results and any
  implication that a positive T score controls mechanism-selection error or
  determines replicate sufficiency.
- **Precise obstruction:** the inner approximation is a nonlinear,
  constrained and generally nonconvex optimisation over feasible flux sets;
  different structural families can induce identical isotope means, making
  the worst-case T distance zero.
- **Evidence:** P0038, Section 2 equations (2.3) and (2.7)–(2.9), Theorems
  2.1–2.2, Section 3 Theorem 3.1 and Corollary 3.2, and Section 5; P0029,
  Sections 2–3, equations (3)–(6), Theorem 4.1 and Sections 5.3–5.4.

## KL-optimal model-discrimination design

- **Classification:** APPLICABLE WITH COMPUTATIONAL ADAPTATION.
- **Exact existing result:** P0024 formulates a continuous-set maximin
  KL-optimal design and proves continuity and algorithmic convergence under
  its assumptions. P0038 supplies the corresponding rival-model KL
  criterion. P0049 implements a semi-infinite worst-case KL-separation
  criterion for bounded biochemical ODE parameter sets.
- **Proposed metabolic formulation:** maximise over isotope-experiment
  designs the minimum KL divergence between dominated EMU-induced
  observation laws across structural alternatives and their nuisance
  parameters.
- **What transfers directly:** KL divergence, approximate-design weighting
  and the nested outer-design/inner-rival formulation when a common
  dominating observation law and a declared uncertainty set are available.
- **What does not transfer:** global tractability for nonlinear EMU families,
  finite-sample two-error calibration, or a guarantee that the minimum
  divergence is positive.
- **Precise obstruction:** continuous feasible-flux sets make the inner
  minimisation computationally inaccessible in general; overlapping induced
  law families force the worst-case KL divergence to zero.
- **Evidence:** P0024, Sections 2–5 and Theorems 1–3; P0038, Section 4
  equations (4.1)–(4.2); P0049, Methods equation 1 and robust-design
  equations 4–5.

## Robust or maximin discrimination design

- **Classification:** APPLICABLE WITH COMPUTATIONAL ADAPTATION.
- **Exact existing result:** P0029 robustifies T-design over bounded
  parameter misspecification; P0024 treats a continuous maximin KL
  criterion; P0049 performs max–min biochemical mechanism design over
  bounded kinetic parameters; P0009 aggregates flux-precision criteria over
  sampled feasible flux maps.
- **Proposed metabolic formulation:** jointly choose an EMU experiment and a
  test to control the worst-case mechanism-decision risk over continuous
  flux, structural and declared discrepancy classes.
- **What transfers directly:** finite-scenario aggregation and criterion-level
  Bayesian, standardized-maximin or KL inner extrema over a specified
  parameter set.
- **What does not transfer:** a global solution certificate or protection
  outside the declared uncertainty class. P0049's criterion is not a
  decision-error guarantee, but P0053, P0065, P0071 and P0072 establish that
  fixed-sample minimax/composite risk bounds exist for represented classes.
- **Precise obstruction:** computing the nested
  `inf_design sup_structure,flux,discrepancy` risk for nonlinear nonconvex EMU
  images can be intractable. Overlap can make the target risk non-vanishing;
  sampled maps or a local inner solution cannot certify the continuous
  supremum.
- **Evidence:** P0009, Methods 2.2–2.5 and Figure 3; P0024, Theorems 1–3;
  P0029, equations (3)–(6) and Theorem 4.1; P0049, robust-design equations
  4–5; P0053 Theorem 2.1; P0065 Theorem III.1; P0071 Sections 2–5; P0072
  Theorems 1–2.

## Bayesian discrimination design

- **Classification:** APPLICABLE WITH COMPUTATIONAL ADAPTATION.
- **Exact existing result:** P0040 proves an equivalence theorem and
  algorithmic convergence for prior-averaged T discrimination. P0050 ranks
  biochemical observables, times and conditions using posterior-predictive
  distributions and Jensen–Shannon divergence. Direct isotope studies P0031,
  P0032 and P0047 infer structural probabilities or average fluxes over
  specified structural families.
- **Proposed metabolic formulation:** put priors on mechanisms and
  structure-specific/shared nuisance, propagate each design through the EMU
  model, and optimise expected posterior decision loss or information gain.
- **What transfers directly:** prior averaging, posterior model probability,
  posterior-predictive utility and multi-model evidence calculation.
- **What does not transfer:** uniform frequentist error control,
  prior-insensitive conclusions or tractable exact marginalisation over large
  trans-dimensional EMU families.
- **Precise obstruction:** evidence and utility integrals are
  high-dimensional and prior-sensitive, and shared nuisance couples
  model-specific integrations; these are computational obstacles, not an
  absence of a Bayesian formulation.
- **Evidence:** P0040, Section 2 equations (2.3)–(2.6) and Theorem 2.1,
  Section 3 Algorithm 3.2 and Theorem 3.3; P0050, Methods “Predictive
  Distributions,” “Model selection” and “Experimental design”; P0031,
  Section 2.2 and Algorithms 1–2; P0032, Sections 2.2–2.4 and Algorithm 1;
  P0047, Results equation 1/Figure 2 and Methods “Flux inference with
  Bayesian Model Averaging.”

## Active hypothesis testing

- **Classification:** UNRESOLVED FROM CURRENT EVIDENCE.
- **Exact existing result:** P0027 gives nonasymptotic Bayesian-cost bounds
  and asymptotic policy results for finite simple hypotheses under adaptive
  action choice.
- **Proposed metabolic formulation:** update mechanism beliefs after each
  experimental block, adaptively select the next tracer, condition or
  perturbation, and stop with a mechanism decision.
- **What transfers directly:** the action-dependent likelihood, posterior
  state, adaptive policy, stopping rule and sampling-cost architecture.
- **What does not transfer:** known simple observation laws and
  observation-by-observation action changes.
- **Precise obstruction:** EMU alternatives are continuous composite
  families with fitted and sometimes shared nuisance; biological experiments
  arrive in costly heterogeneous blocks, and different alternatives may
  overlap observationally. The inspected finite-simple anchor does not settle
  whether existing composite/blockwise active-testing theory covers that
  formulation, so this mismatch cannot yet be called a necessary new theorem.
- **Evidence:** P0027, Section 2 and Sections 4–6, Propositions 1–5.

## Controlled sensing

- **Classification:** UNRESOLVED FROM CURRENT EVIDENCE.
- **Exact existing result:** P0026 derives fixed-sample error-exponent bounds
  and sequential asymptotic optimality for finite simple hypotheses with
  control-dependent known observation kernels.
- **Proposed metabolic formulation:** controls are tracer, fragment,
  condition or perturbation choices and hypotheses are metabolic structures
  inducing EMU likelihood families.
- **What transfers directly:** control-dependent KL information and the
  allocation of observations among a finite action set.
- **What does not transfer:** the finite-simple-hypothesis assumption, known
  kernels and free observation-level control switching.
- **Precise obstruction:** nuisance optimisation changes the information
  rate, shared parameters couple action blocks, and some controls can have
  zero worst-case pairwise information for overlapping composite families.
  These are assumption mismatches with P0026, not proof that no existing
  controlled-sensing result applies.
- **Evidence:** P0026, Section II, Proposition 1 and Theorems 1–5.

## Sequential experimental design

- **Classification:** UNRESOLVED FROM CURRENT EVIDENCE.
- **Exact existing result:** P0027 supplies Bayesian active sequential
  policies; P0028 supplies sequential composite controlled sensing under
  disjoint exponential-family classes; P0042 supplies a fixed-confidence
  stopping threshold, expected-stopping lower bound and asymptotic
  optimality for finite one-parameter exponential-family arms.
- **Proposed metabolic formulation:** make blockwise isotope-experiment
  choices and stop when accumulated evidence certifies a mechanism decision.
- **What transfers directly:** sequential likelihood accumulation,
  information-directed allocation and data-dependent stopping for a fully
  specified finite hypothesis/action reduction.
- **What does not transfer:** fixed biological-batch costs, continuous EMU
  composites and partially shared nuisance across completed and future
  conditions.
- **Precise obstruction:** action-dependent parameter fitting destroys the
  verified simple/exponential-family geometry, while a block can contain
  correlated, non-identically distributed observations that cannot be
  replaced by one sequential draw without changing the risk and cost model.
  Current verified anchors do not determine whether this needs a theorem or
  only a different existing formulation plus computation.
- **Evidence:** P0027, Sections 2 and 4–6; P0028, Sections 2–3 and Theorems
  1–3; P0042, Section 2.1 Theorem 1, Section 4 Theorem 10 and Section 5
  Theorem 14.

## Chernoff testing

- **Classification:** UNRESOLVED FROM CURRENT EVIDENCE.
- **Exact existing result:** P0026 gives Chernoff/KL action-allocation
  exponents and converses for controlled finite simple hypotheses; P0027 and
  P0042 give related information-directed sequential policies and bounds.
- **Proposed metabolic formulation:** choose isotope actions according to
  their worst pairwise fitted KL information and stop when a likelihood
  threshold is crossed.
- **What transfers directly:** information-directed action selection for a
  finite set of fully specified EMU distributions.
- **What does not transfer:** continuous composite mechanisms, joint
  estimation of shared nuisance and fixed/batched sampling.
- **Precise obstruction:** the relevant information number becomes a nested
  infimum over nuisance and can equal zero at family overlap; the classical
  exponent and stopping analysis inspected here does not cover that geometry.
  The bounded search does not establish that all composite Chernoff results
  share this limitation.
- **Evidence:** P0026, Proposition 1 and Theorems 1–5; P0027, Propositions
  1–5; P0042, Theorems 1, 10 and 14.

## Composite or compound hypothesis testing

- **Classification:** APPLICABLE WITH COMPUTATIONAL ADAPTATION.
- **Exact existing result:** P0053 constructs uniform nonasymptotic tests
  between convex compact composite classes; P0060 constructs robust tests
  between Hellinger-separated classes; P0065/P0071 give exact minimax tests
  for divergence-neighbourhood composites. P0028 gives sequential composite
  error/delay results and P0043 supplies exact composite-null Type-I control.
- **Proposed metabolic formulation:** each mechanism is the set of
  observation laws obtained as structure-specific and shared flux/nuisance
  parameters vary.
- **What transfers directly:** set-valued hypotheses, minimax two-error risk,
  least-favourable information calculations, product-law construction and
  composite-null testing logic.
- **What does not transfer:** a tractable representation of an arbitrary
  nonlinear EMU image, or a certified cover when convex/separation
  assumptions fail.
- **Precise obstruction:** EMU-induced families can be curved, singular or
  overlapping and shared nuisance couples blocks. Convexification preserves
  worst-case testing risk, but its hull and least-favourable mixtures may be
  difficult to compute and need not correspond to one physical parameter
  point; finite gridding is not uniform without an approximation bound.
- **Evidence:** P0053 Theorem 2.1 and Proposition 3.2; P0060 Sections II–III;
  P0065 Theorem III.1; P0071 Sections 2–5; P0028; P0043.

## Fixed-sample minimax composite testing

- **Classification:** APPLICABLE WITH COMPUTATIONAL ADAPTATION.
- **Exact existing result:** P0053 gives constructive uniform
  nonasymptotic two-error tests and near-optimality comparisons for convex
  composite classes; P0060 covers separated Hellinger classes and non-IID
  products; P0065/P0071 give exact minimax divergence-neighbourhood tests;
  P0072 gives constructive sample-complexity upper and lower bounds under a
  Hellinger-margin condition.
- **Proposed metabolic formulation:** precommit a biological replicate
  allocation and control both mechanism-selection errors uniformly over
  continuous EMU structural/nuisance classes.
- **What transfers directly:** the minimax risk definition, uniform
  two-error bounds, least-favourable-law construction and product-law
  extension for represented or separated classes.
- **What does not transfer:** certified representation of the exact nonlinear
  EMU law sets and globally optimised tracer/intervention/allocation choices.
- **Precise obstruction:** the tractable primary results rely on convex,
  separated or structured ambiguity classes. Nonconvex EMU images require a
  global least-favourable calculation or certified cover. Convex-hull
  intersection is a valid minimax mixture obstruction, but its witness need
  not be a single physical metabolic parameterisation.
- **Evidence:** P0053; P0060; P0065; P0071–P0072; supported by P0041/P0044.

## Error-exponent design and converses

- **Classification:** APPLICABLE WITH COMPUTATIONAL ADAPTATION.
- **Exact existing result:** P0026 proves fixed-sample controlled-sensing
  exponent bounds/converses and sequential asymptotic optimality for finite
  simple hypotheses. P0041 provides Cramér-type fixed-sample asymptotics for
  specified robust binary tests.
- **Proposed metabolic formulation:** optimise the asymptotic exponential
  decay of worst-case mechanism error over isotope actions and composite EMU
  alternatives.
- **What transfers directly:** pairwise KL/Rényi calculations and
  finite-hypothesis lower bounds for selected induced joint laws.
- **What does not transfer:** a positive exponent under continuous nuisance
  or overlapping families, and automatic optimisation over heterogeneous
  block designs.
- **Precise obstruction:** the exponent becomes a design-dependent max–min
  over composite families and is zero when their closures intersect.
  General lower-bound templates exist, but computing the tight EMU pair or
  packing is a nested nonconvex problem.
- **Evidence:** P0026; P0041 Section IV; P0056 Theorem 1; P0059 Theorems
  II.1, III.1 and IV.1.

## Sample-complexity converses

- **Classification:** APPLICABLE WITH COMPUTATIONAL ADAPTATION.
- **Exact existing result:** P0059 gives finite-sample two-point,
  multiple-testing, packing and metric-entropy lower bounds; P0056 gives a
  Rényi strong converse; P0069 gives fixed-block binary-testing
  meta-converses; P0072 supplies matching Hellinger-margin upper/lower sample
  complexity. P0042/P0028 provide narrower sequential bounds and P0018 an
  isotope rank obstruction.
- **Proposed metabolic formulation:** lower-bound the number and allocation
  of fixed or sequential isotope-experiment blocks needed to attain declared
  mechanism errors.
- **What transfers directly:** exact overlap, two-point divergence and any
  finite packing of EMU-induced product laws, plus rank failure as an
  insufficiency diagnostic.
- **What does not transfer:** fixed biological batches, continuous structural
  composites, shared nuisance and nonuniform per-condition cost.
- **Precise obstruction:** a useful least-favourable pair or packing must
  preserve shared nuisance and EMU feasibility. General inequalities already
  quantify near-overlap once divergence is bounded; globally finding the
  tight design-specific reduction is computational.
- **Evidence:** P0056; P0059; P0069; P0072; P0042; P0028; P0018 Theorem 4.

## Heterogeneous non-IID or adaptive evidence

- **Classification:** APPLICABLE WITH COMPUTATIONAL ADAPTATION.
- **Exact existing result:** P0053 and P0060 give uniform fixed-sample tests
  for independent non-identically distributed products under their stated
  class/separation assumptions. P0043 gives anytime Type-I control for
  conditionally valid heterogeneous/adaptive e-values; P0032 and P0050
  verify direct multi-experiment isotope/Bayesian use.
- **Proposed metabolic formulation:** combine condition-specific isotope
  blocks with shared and condition-specific nuisance and prospectively
  allocate new blocks to a mechanism decision.
- **What transfers directly:** conditional e-value multiplication for Type-I
  control once each block is valid, additive likelihood/information
  contributions and Bayesian multi-experiment integration.
- **What does not transfer:** a tractable exact law-family representation
  when nuisance is shared across blocks.
- **Precise obstruction:** blockwise independent nuisance enlargement can
  erase separation, while enforcing shared nuisance creates a coupled
  nonconvex feasible set. Adaptive validity additionally requires
  conditional control for every admitted null law.
- **Evidence:** P0053 Theorem 2.1 and Proposition 3.2; P0060 Sections II–III;
  P0043; P0032; P0050.

## Shared-nuisance testing

- **Classification:** APPLICABLE WITH COMPUTATIONAL ADAPTATION.
- **Exact existing result:** P0062 maximises valid pointwise p-values over a
  nuisance confidence set; P0064 gives exact/conservative Monte Carlo tests
  with nuisance parameters; P0070 gives finite-sample composite-null
  split-likelihood control. P0043 supplies e-value constructions, and
  P0030–P0032/P0047 verify shared-parameter isotope analyses.
- **Proposed metabolic formulation:** test structural alternatives while
  enforcing that biological or flux nuisance is common across selected
  conditions and allowing specified condition-specific components.
- **What transfers directly:** joint likelihood construction, Bayesian
  hierarchical sharing and composite-null validity when P0043's conditions
  can be verified.
- **What does not transfer:** an automatic tractable profile,
  least-favourable or covering calculation with both-error uniformity for an
  arbitrary nonlinear sharing pattern.
- **Precise obstruction:** a common nuisance value must be optimised jointly
  across hypotheses and blocks; separate per-model fits can create
  incompatible least-favourable points, boundary singularities or absent
  information projections.
- **Evidence:** P0062, journal pp. 1012–1013; P0064 Section 4,
  Propositions 4.1–4.2; P0070 Theorem 3; P0043; P0030–P0032; P0047.

## Nonnested or overlapping model families

- **Classification:** APPLICABLE WITH COMPUTATIONAL ADAPTATION.
- **Exact existing result:** P0065 and P0071 compute ambiguity radii at which
  robust composite law classes overlap and a minimax robust test ceases to be
  designable. P0059 supplies finite-sample two-point/packing lower bounds;
  P0038 exposes zero T/KL separation and P0018 gives an isotope rank
  obstruction.
- **Proposed metabolic formulation:** discriminate nonnested reaction,
  pathway, compartment or atom-map families whose induced observation-law
  sets may intersect.
- **What transfers directly:** zero fitted T/KL separation and rank failure
  as diagnostics of exact observational equivalence.
- **What does not transfer:** a certified calculation of exact or near
  intersection for nonlinear fitted EMU families and its optimisation over
  design.
- **Precise obstruction:** exact intersection makes uniform discrimination
  impossible; near-intersection is already handled by divergence bounds once
  a difficult pair is certified, but finding that pair globally is
  computationally hard.
- **Evidence:** P0065 Section III-C/Figure 10; P0071 Section 4/Figure 1;
  P0059; P0038; P0018 Theorem 4.

## Distributionally robust testing and design

- **Classification:** APPLICABLE WITH COMPUTATIONAL ADAPTATION.
- **Exact existing result:** P0044 gives an exact binary KL-neighbourhood
  saddle test; P0041 treats several dominated uncertainty classes; P0065 and
  P0071 give exact divergence/Hellinger-neighbourhood minimax tests and
  overlap boundaries; P0072 gives fixed-sample robust Hellinger upper/lower
  sample-complexity bounds.
- **Proposed metabolic formulation:** place declared ambiguity sets around
  EMU-induced laws and jointly optimise tracer/condition design and a
  least-favourable structural test.
- **What transfers directly:** dominated ambiguity sets,
  least-favourable-law construction and saddle-point testing for a fixed
  binary experiment.
- **What does not transfer:** automatic conversion of a feasible-flux or
  structural EMU image into a scientifically defensible ambiguity set, or
  global optimisation of the experiment-dependent least-favourable pair.
- **Precise obstruction:** the ambiguity sets must share a dominating measure
  and remain detectably separated for every admitted nuisance value; design
  changes the nominal laws and hence the least-favourable pair, creating a
  nested nonconvex saddle problem.
- **Evidence:** P0044 Sections II–III; P0041 Sections II–V; P0065 Theorem
  III.1; P0071 Sections 2–5; P0072 Theorems 1–2.

## Forward-model misspecification

- **Classification:** UNRESOLVED FROM CURRENT EVIDENCE.
- **Exact existing result:** P0029 handles parameter misspecification within
  specified rivals; P0034 quantifies an atom-map error; P0035 tests and
  repairs omitted reactions in linear stoichiometric MFA; P0045 diagnoses
  traditional-MFA model error with covariance-aware GLS and simulation;
  P0048 designs against response distributions induced by uncertain
  biochemical-network parameters.
- **Proposed metabolic formulation:** design and analyse isotope experiments
  under a declared ambiguity class containing specified reaction omissions,
  atom-map alternatives, compartment errors or bounded systematic EMU
  discrepancy.
- **What transfers directly:** held-out validation, candidate-reaction tests,
  atom-map sensitivity, parameter-distribution design and bounded
  within-model robust criteria.
- **What does not transfer:** protection against an unspecified unknown
  discrepancy or a uniform mechanism-error guarantee outside an enumerated
  family.
- **Precise obstruction:** without a scientifically bounded discrepancy
  class the target is unidentified; with one, discrepancy can be confounded
  with flux and can make induced ambiguity classes overlap. A declared class
  is required before deciding whether existing robust testing applies
  directly, needs computational adaptation, or leaves a narrower theorem.
- **Evidence:** P0029, Sections 2–3; P0034, Figure 3 and Supplementary Tables
  S4/S7/S8; P0035, Methods 2.2.1–2.3 and Results 3.1–3.3; P0045, Methods
  equations 7 and 19 and Results Figures 2–6; P0048, Sections 2.2–2.5.

## Phase 2A boundary

The classifications above support transfer decisions only at the evidence
depth recorded in `corpus/papers.csv`. They do not establish that a residual
is novel. Phase 2A.1 changes the fixed-sample/composite/converse families from
unresolved to computational transfer classifications; it does not imply that
their EMU implementation, approximation accuracy or global optimisation has
been demonstrated.

Across GAP-01–GAP-07, these classifications must be read in five separate
layers:

1. **Generic theory already established:** positive verified results support
   the stated T/KL, Bayesian, composite, robust, heterogeneous-product and
   converse transfers.
2. **Verified computational limitation:** the cited algorithms solve their
   declared convex, separated, regular or neighbourhood representations; the
   evidence does not supply a global solver for an arbitrary nonlinear EMU
   image.
3. **Biological/application issue:** mechanisms, feasible flux sets, nuisance
   sharing, discrepancy, replicate semantics and experimental costs must be
   specified in the metabolic application.
4. **Software-integration issue:** coupling forward simulation, inference,
   tests, bounds and design is engineering unless a separately stated
   mathematical result is proved.
5. **Unresolved/deferred evidence:** inaccessible and discovery-level records
   cannot support either an absence or a survival claim. The weakened
   GAP-01/GAP-03 judgments rest on verified existence evidence, not on
   saturation or automatic exclusion.
