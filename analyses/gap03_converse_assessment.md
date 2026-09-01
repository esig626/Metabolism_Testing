# GAP-03 Converse Assessment

## Precise registered proposition

For design `d` and fixed replicate allocation `n`, let

`R*_(d,n) = inf_phi max{
  sup_(P in P_0(d,n)) E_P[phi],
  sup_(Q in P_1(d,n)) E_Q[1-phi] }`.

GAP-03 asks whether proving that an isotope experiment is insufficient
requires new converse theory, or whether established lower bounds only need to
be computed for the EMU-induced families. Four different converse statements
are assessed separately:

1. exact overlap or identifiability obstruction;
2. information-divergence lower bound;
3. minimax sample-complexity lower bound; and
4. design-specific impossibility certificate.

A failure to compute a useful lower bound is not itself an impossibility
result. Conversely, a lower bound below the target does not prove that the
target is achievable.

## Outcome summary

| Converse form | General-theory outcome | EMU-specific outcome |
|---|---|---|
| 1. Exact overlap / identifiability | **ESTABLISHED; DIRECT APPLICATION** | proving intersection of the original induced families is a nonlinear feasibility problem; convex-hull intersection is a valid minimax-mixture obstruction but not physical parameter overlap |
| 2. Information-divergence lower bound | **ESTABLISHED; DIRECT APPLICATION** | evaluating or globally minimising TV, Hellinger, KL, Rényi, or another divergence over opposing EMU families is computational |
| 3. Minimax sample-complexity lower bound | **ESTABLISHED in general; DIRECT APPLICATION of the inequality** | constructing a useful pair/packing and solving its product-law bound for replicates is a computational adaptation |
| 4. Design-specific impossibility | **ESTABLISHED for a fixed represented design via forms 1–3** | certifying insufficiency uniformly over all admissible designs is a nested global optimisation problem |

## 1. Identifiability or exact-overlap obstruction

**Outcome: ESTABLISHED; DIRECT APPLICATION.**

If `P` belongs to both `P_0(d,n)` and `P_1(d,n)`, then every possibly
randomised test satisfies

`alpha(phi) >= E_P[phi]`,

`beta(phi) >= E_P[1-phi]`,

and therefore

`max{alpha(phi), beta(phi)} >= 1/2`.

This is an exact finite-sample obstruction, not an asymptotic statement.
P0053 makes the same boundary explicit in its Gaussian-scheme discussion:
when the convex hypothesis sets intersect, no nontrivial test with both errors
below one-half exists. P0071 Section 4, equations (23)–(36), Figure 1, and
Section 5, and P0065 Section III-C, compute overlap/maximum-robustness
boundaries for their Hellinger and alpha-divergence neighbourhoods.

Two different intersections must not be conflated:

- `P_0(d,n) intersect P_1(d,n) != empty` proves exact physical-law
  nonidentifiability for the stated mechanism parameterisations.
- `conv(P_0(d,n)) intersect conv(P_1(d,n)) != empty` gives a valid
  least-favourable-mixture obstruction for worst-case randomised testing,
  because test risk is linear in the law. It need not identify one physical
  parameter value in each mechanism producing the same law.

For an EMU application, the theorem is direct. The unresolved task is proving
one of these intersections, or a sufficiently small separation, over two
nonlinear constrained images. A plot of close simulated means or failure of a
local optimiser is not such a proof.

## 2. Information-divergence lower bound

**Outcome: ESTABLISHED; DIRECT APPLICATION.**

P0059 supplies the primary finite-sample foundation:

- Section II, Theorem II.1, gives an `f`-divergence lower bound for the
  multiple-testing/decision risk.
- Corollaries II.2–II.3 include sharp two-law total-variation forms.
- Example II.4 recovers Fano’s inequality.

For any selected `P in P_0(d,n)` and `Q in P_1(d,n)`, the minimum sum of the
two simple-hypothesis errors is `1-TV(P,Q)`. Hence

`R*_(d,n) >= (1 - TV(P,Q))/2`,

and maximising this valid lower bound over opposing pairs is equivalent to
searching for the closest pair in total variation. Hellinger, KL, chi-square,
Rényi, or other `f`-divergence inequalities may provide computable relaxations
under their stated absolute-continuity conditions.

For independent heterogeneous blocks, the divergence is computed on the joint
product law. KL divergence adds across blocks and replicates when the usual
domination conditions hold:

`KL(P^(d,n) || Q^(d,n))
 = sum_k n_k KL(nu_(0,k) || nu_(1,k))`

for a fixed opposing parameter pair. This already incorporates a fixed
multi-condition design; no sequential stopping theorem is needed.

The remaining EMU work is computational:

1. choose or optimise the opposing parameter pair;
2. evaluate the induced joint-law divergence accurately;
3. respect shared nuisance constraints; and
4. prove global rather than sampled/local separation.

## 3. Minimax sample-complexity lower bound

**Outcome: ESTABLISHED in general; COMPUTATIONAL APPLICATION for EMU
families.**

Several independent primary sources establish fixed-sample converse
machinery:

- **P0059:** Theorem III.1 and Theorem IV.1 convert coverings, packings, and
  global metric entropy into finite-sample minimax lower bounds. These results
  apply after selecting a finite subset of a continuous composite class.
- **P0056:** Section 2, Theorem 1 and its main equation, give a finite-sample
  Rényi-divergence strong converse for finite M-ary testing; Section 2.1
  relates it to Birgé, Fano, and Assouad forms.
- **P0069:** Section III-E, equations (100)–(105), and Theorems 26–27 and
  30–31 give exact nonasymptotic beta-alpha/meta-converse bounds for finite
  message sets. For mechanism testing these require a finite packing or prior
  reduction; they are not themselves a constructive composite test.
- **P0072:** Theorems 1–2 give a constructive sample-complexity upper bound
  and a lower obstruction for the stated Hellinger-margin robust-testing
  problem.
- **P0066, P0068, and P0063:** the cited propositions/theorems give
  class-specific nonasymptotic minimax lower bounds and matching or comparable
  constructive upper bounds for Gaussian, heterogeneous-variance, density,
  and multinomial problems.

To obtain a necessary replicate count, evaluate a finite-sample lower bound as
a function of `n` and solve the inequality needed to make the lower bound fall
below the registered tolerance. For binary mechanism discrimination, a
two-point reduction may already be decisive. A packing is useful when the
scientific decision requires resolving several alternatives or a specified
resolution within a class.

These results falsify the broad claim that only sequential or asymptotic
sample-complexity converses exist. They do not remove the EMU computation:
one must construct a biologically valid pair or packing, evaluate its
product-law divergences, and preserve the joint shared-parameter constraints.

## 4. Design-specific impossibility certificate

**Outcome: ESTABLISHED in general for a fixed design; COMPUTATIONAL GAP for
global EMU design certification.**

For a fixed `(d,n)`, forms 1–3 immediately produce design-specific
certificates:

- exact family overlap proves `R*_(d,n) >= 1/2`;
- a close opposing pair gives a TV/Hellinger/KL/Rényi lower bound; and
- a finite packing gives a multiple-testing/sample-complexity lower bound.

For example, define the strongest available pairwise bound

`L(d,n) =
  sup_(P in P_0(d,n), Q in P_1(d,n))
  [1 - TV(P,Q)]/2`.

Then `L(d,n) <= R*_(d,n)`, and `L(d,n) > epsilon` certifies that this design
cannot meet tolerance `epsilon`. An analogous construction can use a
computable divergence relaxation or packing bound.

The design-wide question is

`inf_((d,n) in D_budget) R*_(d,n) > epsilon`.

A sufficient impossibility proof can show

`inf_((d,n) in D_budget) L(d,n) > epsilon`.

Computing that expression nests:

1. mixed discrete/continuous tracer, intervention, measurement, and replicate
   choices;
2. a closest-pair or packing search over two nonlinear mechanism classes;
3. shared nuisance and structural constraints; and
4. certified evaluation of observation-law distances.

The verified general converse papers do not make this nested global
optimisation tractable. That is a computational obstruction. A new
theoretical residual would require a separately registered claim—such as an
approximation ratio, relaxation tightness theorem, or complexity lower
bound—not merely an EMU-specific notation.

## Nearest prior work and strongest contrary evidence

The closest verified primary works are:

1. **P0059**, for finite-sample two-point, `f`-divergence, Fano, packing,
   covering, and metric-entropy minimax lower bounds (Sections II–IV).
2. **P0056**, for a finite-sample Rényi strong converse over a finite
   hypothesis packing (Section 2, Theorem 1).
3. **P0069**, for exact finite-block beta-alpha/meta-converse machinery
   (Section III-E; Theorems 26–27 and 30–31).
4. **P0071/P0065**, for explicit overlap/maximum-robustness impossibility
   boundaries in specified composite uncertainty neighbourhoods.
5. **P0060**, for the complementary constructive side under independent
   heterogeneous products, showing that non-IID blocks do not invalidate
   fixed-sample theory.

This fixed-sample literature is stronger and more directly relevant to
GAP-03 than the sequential controlled-sensing chain used in the initial Phase
2A assessment. It establishes exact overlap, divergence, packing, and
finite-block converse forms without variable stopping times.

## Contribution-type and evidence boundary

- **Generic theory already established:** exact-overlap, two-point
  divergence, finite-packing/Fano, metric-entropy and fixed-block converse
  forms are positively established by P0059, P0056, P0069,
  P0065/P0071 and P0072. This is enough to weaken the registered claim that a
  new generic fixed-sample converse is required.
- **Verified computational limitation:** these sources require a law pair,
  packing, distance or represented uncertainty class as input. They do not
  compute the globally strongest witness over a nonlinear EMU image or the
  outer mixed design. This is an interface and global-optimisation boundary,
  not a proved universal intractability result.
- **Biological/application issue:** the mechanism resolution, error
  tolerance, cost, admissible design set and interpretation of a
  least-favourable mixture versus a physical metabolic state must be fixed
  for a meaningful insufficiency statement.
- **Software-integration issue:** evaluating product-law divergences,
  certified pair/packing bounds and design-wide reports from an EMU solver is
  engineering unless it includes a separately proved approximation,
  relaxation or complexity result.
- **Unresolved/deferred-evidence boundary:** inaccessible and
  discovery-level converse records are not used for an absence statement.
  The `WEAKENED` status rests on verified positive converse results, not a
  claim that every adjacent family has been located or screened in full.

## Exact residual, evidence needed, and overall status

- **Exact residual:** compute and globally certify overlap, closest-pair,
  packing, or divergence-based lower bounds for nonlinear EMU law families,
  then optimise those bounds over admissible tracer/intervention/replicate
  designs.
- **Residual type:** computational adaptation.
- **Evidence against a theoretical gap:** P0059, P0056, and P0069 already
  supply general fixed-sample converse inequalities; P0071/P0065 demonstrate
  explicit composite-overlap certificates.
- **Evidence for a computational residual:** the general results take laws,
  distances, or packings as inputs and do not provide a certified global
  solver for a nonlinear EMU image with shared nuisance and structural
  constraints.
- **Evidence still needed:** a declared EMU observation law; certified
  closest-pair or packing algorithms; finite-precision error bounds for the
  forward solver and divergence calculation; and a global or certified
  approximate solution of the outer design problem.
- **Overall status: WEAKENED.**

The broad proposition that EMU discrimination needs a new fixed-sample
converse is rejected by affirmative verified general results. The narrower
task of computing a mechanistically interpretable, design-specific converse
remains unresolved. Deferred literature does not restore the broad
proposition or support a stronger absence conclusion. This is not a novelty
claim and does not make a grant recommendation.
