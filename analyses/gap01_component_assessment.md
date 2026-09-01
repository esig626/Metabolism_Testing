# GAP-01 Component Assessment

## Precise registered proposition

For a fixed design and replicate allocation, competing metabolic mechanisms
induce the two law families `P_0(d,n)` and `P_1(d,n)` defined in
`analyses/fixed_sample_composite_testing_foundations.md`. GAP-01 is assessed as
five distinct propositions:

1. whether fixed-sample tests for composite mechanism classes exist;
2. whether uniform finite-sample error guarantees exist;
3. whether such tests are computable for nonlinear EMU-induced families;
4. whether tracers and interventions can be optimised against the decision
   error; and
5. whether multiple independent heterogeneous conditions require new testing
   theory.

The propositions are not merged. In particular, existence of a test or
inequality does not imply a tractable EMU implementation, and ranking designs
does not imply a certified error or replicate requirement.

## Component outcomes

| Component | Outcome | Reason |
|---|---|---|
| A. Existence of fixed-sample tests for composite mechanism classes | **ESTABLISHED** | Composite-versus-composite fixed-sample tests are explicitly constructed for convex and metric-separated law classes (P0053, P0060) and for specified divergence neighbourhoods (P0065, P0071). |
| B. Uniform finite-sample error guarantees | **ESTABLISHED under stated classes; DIRECT APPLICATION at the level of general risk inequalities** | P0053 and P0060 uniformly bound both errors; P0065/P0071 give exact minimax robust constructions for their stated classes; P0059 supplies finite-sample lower inequalities for arbitrary selected laws or finite packings. None licenses extrapolation from a sampled flux grid. |
| C. Computable tests for nonlinear EMU-induced families | **COMPUTATIONAL GAP** | The probability results apply to represented law sets, but an exact nonlinear EMU image, its convex hull, a certified metric cover, or a least-favourable pair may be computationally inaccessible. |
| D. Design optimisation over tracers and interventions | **COMPUTATIONAL GAP** | A bound can be evaluated design by design when its inner problem is solved, but a certified optimum nests mixed experimental choices around least-favourable-pair, cover/packing, or minimax-risk computations. |
| E. Multi-condition non-IID extensions | **ESTABLISHED for independent heterogeneous products; COMPUTATIONAL GAP for exact shared-nuisance representation** | P0060 and P0053 explicitly cover independent non-identical products. Shared nuisance constraints couple the joint parameter image and create the remaining representation/optimisation problem. |

## A. Existence of fixed-sample composite tests — ESTABLISHED

P0053 defines the two worst-case error probabilities and constructs an
affinity/least-favourable-pair detector for convex compact parameter sets.
Theorem 2.1 and equations (3)–(6) give the detector and simultaneous error
bounds; the repeated and nonstationary sections extend the construction to
product observations. P0060 Section II, theorem and corollary on pp. 72–73,
construct tests between separated Hellinger neighbourhoods. P0065
Theorem III.1 and P0071 Sections 2.2–4 give further exact fixed-vector
minimax tests for specified divergence-ball composites.

These sources destroy the broad proposition that a composite-versus-composite
mechanism problem needs a new kind of fixed-sample statistical test merely
because each mechanism contains continuously many parameter values.

The established result has boundaries:

- a nontrivial test still requires separation in the selected experiment;
- an exact physical overlap makes both errors below one-half impossible;
- the constructive source assumptions—convexity, metric separation,
  domination, or a specified divergence neighbourhood—must be checked; and
- none of these results computes an arbitrary nonlinear EMU law family
  automatically.

## B. Uniform finite-sample guarantees — ESTABLISHED under stated classes

The relevant positive and negative guarantees are already finite-sample:

- P0053 Theorem 2.1 uniformly bounds both composite errors, and its
  nonstationary-product result compounds detector risks across independent
  heterogeneous blocks.
- P0060 pp. 72–75 gives simultaneous exponential error bounds for separated
  Hellinger classes, including independent non-identically distributed
  products.
- P0065 Theorem III.1 and P0071 Sections 2–5 give exact one-vector minimax
  robust tests over their stated alpha-divergence and Hellinger balls.
- P0072 Theorems 1–2 give a fixed-sample robust-testing upper bound and a
  matching-order lower obstruction for its Hellinger-margin problem.
- P0059 Theorem II.1 and Corollaries II.2–II.3 give finite-sample
  `f`-divergence and total-variation lower bounds; Theorems III.1 and IV.1
  give finite-packing and metric-entropy forms.

Thus a blanket absence claim about uniform finite-sample composite-testing
guarantees is false. What is direct for an arbitrary EMU application is more
limited:

1. exact overlap and pairwise lower inequalities apply once the induced laws
   are specified;
2. upper certificates apply directly only if their structural assumptions
   are met; and
3. a simulation over sampled flux maps is not a uniform class guarantee.

Nuisance-only anchors reinforce the boundary. P0062 (journal pp. 1012–1013),
P0064 (Section 4, Propositions 4.1–4.2), and P0070 (universal test and
Theorem 3) provide finite-sample Type-I control, but do not by themselves
control Type II error or certify replicate sufficiency.

## C. Computable tests for nonlinear EMU-induced families — COMPUTATIONAL GAP

For each mechanism, a nonlinear EMU map sends a constrained parameter set to
a family of observation laws. The verified constructive methods solve
particular representations:

- convex compact parameter or distribution sets (P0053);
- separated convex signal sets under sub-spherical noise (P0057);
- regular families admitting affine detectors (P0058);
- convex-cone Gaussian problems (P0055); and
- alpha-divergence or Hellinger balls around nominal laws (P0065, P0071,
  P0072).

An exact EMU image need not have one of those representations. The residual
computations are:

1. represent the exact induced family or its convex hull;
2. prove a metric cover or relaxation error;
3. compute a least-favourable pair, mixture, packing, or detector; and
4. preserve feasible-flux and shared-nuisance constraints.

Convexification needs careful interpretation. Because test error is linear in
the law, its supremum over a class equals its supremum over that class’s
convex hull; replacing both classes by their convex hulls therefore leaves
every test’s worst-case risk and the resulting minimax value unchanged. But a
convex-hull intersection may arise from least-favourable mixtures and does not
prove that two physical metabolic parameterisations induce the same law.
Moreover, constructing or optimising over the convex hull of a nonlinear EMU
image can itself be intractable.

A finite flux grid is a useful numerical surrogate only if a covering radius
and continuity bound turn pointwise detector performance into a class-wide
bound. No absence claim about all possible algorithms is made; the
classification records that the verified general theorems do not themselves
supply this EMU representation and certified computation.

## D. Tracer and intervention optimisation — COMPUTATIONAL GAP

For a finite candidate list, existing theory can be applied separately to
each design and the resulting certified risks or lower bounds compared. A
new probability inequality is not required for that operation.

The exact design problem is harder:

`min_(d,n in D_budget) R*_(d,n)`

for an achievable upper certificate, or the corresponding maximin
optimisation of a converse. The outer design may contain discrete tracer,
fragment, and intervention choices, continuous mixture/enrichment variables,
and integer replicate allocations. Each objective evaluation may itself
require a nonconvex least-favourable-pair, convex-hull, cover, or packing
calculation.

P0049 already formulates a semi-infinite max-min KL design over bounded
parameters for nonlinear biochemical mechanisms (robust-optimal-design
equations (4)–(5)), which is strong evidence against a broad absence of robust
mechanism-design methods. Its derivative-based nested optimisation and
restarts do not certify the global continuous-class optimum or a
finite-sample decision error. P0053/P0057 show how inner testing problems
become tractable for specified convex representations; they do not solve this
mixed nonlinear EMU outer problem.

The residual is therefore computational design integration. A theoretical
claim would need a separately stated result, such as a certified relaxation,
approximation ratio, oracle inequality, or complexity bound.

## E. Multiple conditions and non-IID blocks — ESTABLISHED with a computational boundary

Independent heterogeneity is directly established:

- P0060 Section III, theorem and corollary on pp. 74–75, treats independent
  non-identically distributed product laws.
- P0053’s nonstationary repeated-observation section and Proposition 3.2,
  equations (24)–(25), give a detector and multiplicative risk bound for
  independent block-specific observation schemes.
- P0058 Propositions 1–3 permit fixed prescribed and conditionally
  heterogeneous observations in its regular-family detector construction.
- P0068 Sections 2–4 supplies nonasymptotic upper and lower bounds for a
  structured independent heterogeneous-variance Gaussian problem.

Consequently, “multiple conditions are non-IID” is not a sufficient
theoretical obstruction.

The remaining issue is shared parameter geometry. If one nuisance or flux
component must be the same in all conditions, replacing it by independent
block-specific values produces a larger family. A test constructed for that
larger family can remain conservative, but may lose all useful separation.
Keeping the equality constraints yields a coupled nonlinear joint image. The
need to represent and optimise over that image is computational; no new
non-IID probability principle is established as necessary by the evidence.

## Nearest prior work and strongest evidence against the gap

The nearest verified primary works are:

1. **P0053**, for constructive composite-versus-composite fixed-sample tests,
   uniform two-error bounds, repeated observations, and heterogeneous product
   schemes (Theorem 2.1; repeated/nonstationary sections; Proposition 3.2).
2. **P0060**, for robust Hellinger tests and independent non-identically
   distributed fixed blocks (Sections II–III, pp. 72–75).
3. **P0065/P0071/P0072**, for exact or nonasymptotic robust composite tests
   and overlap/sample-complexity boundaries under explicitly specified
   distributional neighbourhoods.
4. **P0059**, for finite-sample two-point, multiple-point, packing, and
   metric-entropy converses (Sections II–IV).
5. **P0049**, for a nonlinear biochemical max-min model-discrimination
   design whose remaining limitation is global computation rather than
   absence of a robust design formulation.

Together, they provide the strongest evidence against GAP-01 as originally
stated:

- fixed-sample composite tests exist;
- uniform finite-sample two-error bounds exist for substantial class
  families;
- independent heterogeneous blocks are covered;
- robust neighbourhood tests and sample-complexity bounds exist; and
- nonlinear biochemical robust design has already been formulated.

## Contribution-type and evidence boundary

- **Generic theory already established:** components A and B are supported
  affirmatively by the inspected constructions and bounds in P0053, P0060,
  P0065/P0071/P0072 and P0059. Component E is established for independent
  heterogeneous products by P0053/P0060. These conclusions do not depend on
  exhausting every search result.
- **Verified computational limitation:** the cited constructive methods take
  convex, separated, regular or neighbourhood representations as inputs.
  P0049 verifies a nested nonlinear biochemical design solved with local
  methods/restarts rather than a global continuous-class certificate. The
  evidence therefore supports a representation/global-computation residual,
  not a universal complexity lower bound.
- **Biological/application issue:** a metabolic instantiation must define the
  rival mechanisms, corrected observation law, feasible flux regions,
  parameter-sharing graph, replicate type and experimental cost. Those
  choices are scientific assumptions, not consequences of generic testing
  theory.
- **Software-integration issue:** connecting an EMU forward solver,
  likelihood, certified class approximation and outer design optimiser is an
  implementation contribution unless accompanied by a separately stated
  theorem.
- **Unresolved/deferred-evidence boundary:** inaccessible records and records
  resolved only at title/abstract level are not used to establish an absence
  or a residual. The `WEAKENED` outcome follows from verified positive
  results that refute the broad proposition; the review does not claim the
  fixed-sample literature is saturated.

## Exact residual, evidence needed, and overall status

- **Exact residual:** certified representation, separation, testing, and
  global design optimisation for nonlinear EMU-induced law families under
  continuous flux constraints, shared nuisance parameters, and mixed
  tracer/intervention/replicate decisions.
- **Residual type:** computational. A narrower theoretical component would
  require an explicit approximation, tractability, or complexity proposition
  not implied by the existing results.
- **Evidence for the residual:** the verified constructive sources impose
  convex, conic, separated, regular-family, or divergence-neighbourhood
  representations; P0049 reports a nested local nonlinear optimisation
  rather than a global certificate.
- **Evidence against a theoretical residual:** P0053, P0060, and P0059
  already provide the core upper, heterogeneous-product, and converse
  machinery.
- **Evidence still needed:** an execution-level EMU formulation with a
  declared observation law; certified discretisation or relaxation error;
  numerical comparison with direct P0053/P0060/P0059 baselines; and a
  global-optimality or approximation analysis for the outer design problem.
- **Overall status: WEAKENED.**

The earlier surviving status is not restored. Verified primary results
affirmatively establish the generic test and guarantee families, so the broad
theoretical hypothesis is falsified even though some literature remains
deferred. A narrower computational adaptation remains unresolved. This
assessment is not a novelty claim and does not make a grant recommendation.
