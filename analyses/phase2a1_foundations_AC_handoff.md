# Phase 2A.1 foundations handoff — query families A–C

Date: 2026-07-31 UTC

Scope: testing between sets, Le Cam/Birgé/Hellinger constructions, and
Fano/Assouad/packing lower bounds.

This handoff reports evidence; it does not assign an overall GAP-01 or GAP-03
status and does not make a novelty claim.

## Bottom line

The broad statistical existence questions are not open:

- constructive fixed-sample tests with uniform Type I/II control exist for
  important composite-versus-composite families, notably convex compact
  parameter sets in tractable observation schemes;
- fixed-block independent non-identically distributed formulations are
  explicit in both modern convex-optimization and older robust-testing work;
- finite-sample lower bounds and converse reductions through finite packings,
  divergences and least-favourable pairs are established;
- exact finite-sample test construction and converse computation for arbitrary
  nonlinear, nonconvex EMU-induced law families are not supplied by these
  results.

The residual question is therefore not whether general composite tests or
general converses exist. It is whether the relevant EMU families satisfy the
tractable convex/exponential-family assumptions, or whether useful tests and
least-favourable pairs can be computed for the convex hulls of the
mechanistically induced law families.

## Verified load-bearing anchors

| Primary source | Exact existing result | Regime and criterion | Exact evidence location | Principal limitation for EMU transfer |
|---|---|---|---|---|
| Goldenshluger, Juditsky & Nemirovski (2015), DOI `10.1214/15-EJS1054` | A saddle-point/Hellinger detector tests two convex compact composite families with uniform risk bounds; direct products cover stationary and heterogeneous independent blocks; lower comparisons quantify near-optimality. | Fixed sample; nonasymptotic; worst-case Type I/II risk; convex computation. | `hypotheses-arxiv-short_corrected.tex`: §2.1 and Theorem `the1`, lines 269–376; §2.3 and Proposition `propnonstI`, 606–727; Proposition `theverylatestopt`, 995–999; proof/converse Lemmas `prop1`–`prop2`, 2933–3055. | “Good observation scheme” requires dominated positive densities with finite-dimensional log-likelihood representation and convex compact parameter sets. Exact nonlinear EMU images need not be convex in that representation. |
| Juditsky & Nemirovski (2016), DOI `10.1214/16-EJS1170` | Affine detectors give uniform exponential-moment error bounds for two and multiple composite hypotheses over prescribed repeated and conditionally heterogeneous observations. | Fixed prescribed \(K\); nonasymptotic; uniform risk upper bounds. | `main.tex`: §3 and Proposition `prop1`, lines 367–485; Propositions `prop2`, `propsubGauss`, `prop22`, 486–603; multiple hypotheses and Proposition `prop3`, 604–714. | Detector existence depends on regular detector families/moment bounds; global minimax optimality is not established for arbitrary families. |
| Guigues, Juditsky & Nemirovski (2020), DOI `10.1214/19-AIHP1022` (inspected arXiv `1705.07196`) | Euclidean separation yields constructive uniform tests for two nonintersecting convex signal sets under sub-spherical noise, including semi-stationary heterogeneous blocks; an explicit observation count is near-optimal under a cap distribution. | Fixed sample; nonasymptotic; worst-case risk; sample-complexity upper and lower comparison. | `student_revised_Nov7_2018.tex`: problem/risk, 192–240; Propositions `prop1` and `OptMajTest`, 381–491; potential tests and Proposition `prop133`, 494–719; lower-comparison proof, 1805–1857. | Observation mean is a linear image of a convex signal set with controlled additive noise. A nonlinear EMU image is not automatically such a set. |
| Wei, Wainwright & Guntuboyina (2019), DOI `10.1214/18-AOS1701` | The GLRT has a nonasymptotic constant-factor minimax testing-radius characterization for specified nested closed convex-cone pairs in Gaussian noise, with a lower bound for every test. | Fixed sample; nonasymptotic; uniform minimax radius; lower bound. | `Full_GLRT.tex`: model/definitions 674–810; Theorem `ThmGLRT`, 1079–1165; Theorem `ThmLBGen`, 1668–1738; lower-bound proof, 2268–2421. | Specialized to Gaussian sequence observations and non-oblique nested convex cones; not a generic nonlinear structural-mechanism family. |
| Birgé (1982), *Tests robustes pour des variables indépendantes et des chaînes de Markov*, Numdam `ASCFM_1982__71_20_70_0` | Constructs robust likelihood-ratio-type tests between separated Hellinger balls; extends exponential error bounds to independent non-identically distributed product laws and, under explicit assumptions, Markov chains. | Fixed sample; nonasymptotic upper bounds; uniform over stated neighbourhoods. | pp. 70–71 introduction; pp. 72–73 §II theorem/corollary; pp. 74–75 §III theorem/corollary; pp. 76–77 §IV theorem and §V conclusion. | The paper explicitly notes failure of usual convex minimax techniques for the nonconvex product-neighbourhood formulation; the construction uses specified Hellinger separation and Markov assumptions and is not a universal minimax theorem. |
| Guntuboyina (2011), DOI `10.1109/TIT.2011.2110791` | Gives finite-sample \(f\)-divergence lower bounds for finite multiple testing and derives packing/global-entropy minimax lower bounds. | Fixed sample; nonasymptotic converse; Bayes/average testing reduction and minimax estimation consequences. | `ARXIVminfdiv.tex`: Theorem `maha` and Eq. `maha.eq`, 727–800; Theorem `ybgen`, 1159–1325; Theorem `myb.thm`, 1326–1430; packing lower bound, 2112–2274. | Supplies lower bounds after selecting a finite packing; it does not construct a composite test or optimize metabolic experimental design. |
| Venkataramanan & Johnson (2018), DOI `10.1214/18-EJS1419` | A Rényi-divergence strong converse lower-bounds average error for any finite \(M\)-ary decoder; Fano is recovered as a special case. | Fixed sample; nonasymptotic lower bound. | `revised_v5_arxiv.tex`: §2, Theorem `thm:main` and Eq. `eq:main`, 180–269; comparison with Birgé/Fano/Assouad, 270–291; Fano recovery, 735–799. | Finite-hypothesis average error is not by itself a uniform test over two continuous mechanism classes; a packing and divergence calculation are required. |
| Addario-Berry et al. (2010), DOI `10.1214/10-AOS817` | Constructs mixture and maximum tests and matching lower bounds for structured finite Gaussian alternatives. | Fixed sample; finite-alternative Bayes/average risk; upper and lower bounds. | `aos817.tex`: model 151–416; upper bounds and Propositions `average`, `maxtest`, 417–670; lower bounds `universal`, `pairs`, `symmetric`, `negass`, 671–948. | Specialized Gaussian combinatorial alternatives; the risk averages over a chosen finite alternative prior rather than uniformly covering a continuous nonlinear family. |
| Comminges & Dalalyan (2013), DOI `10.1214/13-EJS766` | Constructs a composite regression test and proves a matching minimax lower separation rate. | Global asymptotic minimax separation; not an exact finite-sample guarantee. | `revision_EJS_2012.tex`: problem/framework 181–262; Theorems `thm_1`, `thm_2`, 571–674; proofs 1392–1465. | Demonstrates established composite-versus-composite theory but does not provide usable nonasymptotic constants for EMU observations. |

## Foundational-family map

| Family | Strongest verified fixed-sample result in this workstream | Constructive? | Minimax / uniform? | Heterogeneous blocks? | EMU transfer |
|---|---|---:|---|---:|---|
| Finite parametric or finite multiple hypotheses | Guntuboyina and Venkataramanan–Johnson finite-sample divergence lower bounds; Addario-Berry et al. tests for structured Gaussian alternatives. | Upper tests only in specialized models; lower bounds general after a finite reduction. | Lower bounds support minimax reductions; average-error formulations are not automatically uniform. | Product divergences can be evaluated for heterogeneous laws, but the cited theorems do not optimize a metabolic block design. | **DIRECTLY APPLICABLE** for converse bounds on any selected finite subset of EMU laws once pairwise/product divergences are available. |
| Convex distribution/parameter classes | Goldenshluger–Juditsky–Nemirovski saddle-point detector and lower comparison. | Yes, by convex optimization. | Uniform; near-optimal/minimax comparison under stated observation-scheme assumptions. | Yes, independent non-identical direct products. | **APPLICABLE WITH COMPUTATIONAL ADAPTATION** when an EMU law family or a justified outer approximation is convex in a compatible natural parameter. |
| Convex signal sets with robust noise | Euclidean-separation and affine-detector constructions. | Yes. | Uniform risk; special-case minimax and near-optimal sample count. | Yes, semi-stationary/conditional formulations. | **APPLICABLE WITH COMPUTATIONAL ADAPTATION** for linearized or convex-outer EMU observation sets with verified noise moment/tail bounds. |
| Hellinger balls and robust neighbourhoods | Birgé 1982 robust separated-ball tests, non-IID products and Markov extension. | Yes. | Uniform upper bounds; the nonconvex case is not asserted to be globally minimax. | Yes. | **APPLICABLE WITH COMPUTATIONAL ADAPTATION** if scientifically defensible Hellinger neighbourhoods and separation can be computed around EMU-induced laws. |
| Nested convex cones in Gaussian noise | Wei–Wainwright–Guntuboyina constant-factor minimax testing radius and converse. | Yes, GLRT. | Uniform minimax up to constants under theorem conditions. | No explicit metabolic multi-condition design. | **NOT APPLICABLE** to a generic EMU family as stated; useful only after proving a Gaussian-cone reduction. |
| Metric/entropy-controlled nonparametric classes | Comminges–Dalalyan and the screened Ingster/Gayraud line give asymptotic minimax separation results. | Yes in their specific regression/white-noise models. | Minimax rate-level, generally asymptotic. | Model-specific. | **UNRESOLVED FROM CURRENT EVIDENCE** for finite-sample EMU constants; the family does refute a broad absence of composite-testing theory. |
| Fano/Assouad/packing converses | Guntuboyina and Venkataramanan–Johnson give explicit finite-sample divergence/packing lower bounds. | Converse, not an upper test. | Minimax lower bounds after reduction; finite constants. | Compatible with product laws when divergences can be computed. | **DIRECTLY APPLICABLE** to finite packings/subsets; **APPLICABLE WITH COMPUTATIONAL ADAPTATION** to optimize the strongest design-specific packing/bound. |

## Exact EMU formulation and the remaining obstruction

For design \(d\), let

\[
\mathcal P_0(d)=\{P_{d,\theta,\eta}:(\theta,\eta)\in\Theta_0\},\qquad
\mathcal P_1(d)=\{P_{d,\theta,\eta}:(\theta,\eta)\in\Theta_1\},
\]

where \(\theta\) contains feasible fluxes and condition-specific parameters and
\(\eta\) contains shared or condition-specific nuisance quantities. The
observation mean or full law is induced by the nonlinear EMU map and chosen
tracer/intervention. Fixed blocks may be independent but non-identically
distributed across conditions.

Against this formulation:

1. **Existence of a mathematical minimax test is not the residual issue.**
   General decision theory and the verified special constructions already
   establish testing and lower-bound formalisms.
2. **Finite-sample lower bounds transfer to finite subsets immediately.**
   Choose laws from the two EMU families, form product laws for the fixed
   block design, and evaluate an \(f\)-divergence/Rényi/Fano/Birgé bound.
3. **The constructive obstruction is exact and computational/geometric.**
   The image of a flux polytope under a nonlinear EMU map can be a nonconvex
   subset of the probability simplex or mean space. The convex saddle-point
   and Euclidean-separation algorithms require convex compatible images.
4. **Convexification is decision-theoretically exact but needs careful
   interpretation.** For every fixed randomised test, worst-case error over a
   law family equals worst-case error over its convex hull, so convexifying
   both families leaves the minimax testing risk unchanged. A convex-hull
   intersection is therefore a valid least-favourable-mixture obstruction,
   but it does not prove that one physical parameterisation in each mechanism
   induces the same law. Computing the hulls of nonlinear EMU images can also
   remain difficult.
5. **Non-IID blocks alone are not a new theoretical obstruction.** GJN 2015,
   Juditsky–Nemirovski 2016, Guigues et al. 2020 and Birgé 1982 all formulate
   heterogeneous or non-identical observations under explicit assumptions.
6. **Design optimization remains separate.** Existing tests/bounds can be
   evaluated at fixed \(d\); optimizing tracer, intervention and replicate
   allocation over \(d\), while jointly solving least-favourable-pair or
   packing problems, may be computationally inaccessible. The reviewed A–C
   papers do not prove that this nested optimization requires new statistical
   theory.

## Consequences for GAP-01 components

These are evidence recommendations for root synthesis, not an overall status:

- Existence of fixed-sample tests for composite classes:
  **ESTABLISHED** for broad convex/robust classes and specific nonparametric
  models.
- Uniform finite-sample error guarantees:
  **ESTABLISHED** under explicit class/separation/observation assumptions; not
  established universally for arbitrary overlapping EMU families.
- Computable tests for exact nonlinear EMU-induced families:
  **UNRESOLVED**. The precise issue is nonconvex induced law geometry and
  computation of least-favourable distributions, not absence of composite
  testing theory.
- Tracer/intervention design optimization:
  **COMPUTATIONAL GAP** on current A–C evidence unless another workstream finds
  a general tractable nested design theorem.
- Multi-condition non-IID extension:
  **ESTABLISHED** as a statistical observation structure under the verified
  assumptions; biological parameter-sharing constraints may still change the
  feasible family.

## Consequences for GAP-03 converse forms

- Identifiability/exact overlap: the obstruction is immediate—if
  \(\mathcal P_0(d)\cap\mathcal P_1(d)\ne\varnothing\), no uniform test can
  separate the shared law. No EMU-specific converse theory is needed to state
  this.
- Information-divergence lower bounds: **ESTABLISHED** in general finite-sample
  theory and directly usable on selected EMU laws/product laws.
- Minimax sample-complexity lower bounds: **ESTABLISHED** via finite packings,
  multiple-testing reductions and least-favourable pairs, subject to computing
  informative EMU-specific divergences/separations.
- Design-specific impossibility certificate: the theory supplies valid bound
  templates, while finding the tightest least-favourable pair/packing for every
  candidate \(d\) is an **APPLICABLE WITH COMPUTATIONAL ADAPTATION** problem on
  current evidence. No reviewed result provides an integrated EMU design
  certificate.

## Corpus-ready field proposals

Root should assign the next stable `P####` IDs after deduplication. The
following are proposals only; the corpus was not edited.

| Source | `criterion_family` | `guarantee_regime` | `robustness_scope` | `converse_type` | `stopping_rule` | `finite_sample` | `uniform_or_worst_case` | `minimax` | `converse_or_impossibility` | `non_iid` | `sample_size_design` |
|---|---|---|---|---|---|---|---|---|---|---|---|
| GJN 2015 | `likelihood;other` | `non_asymptotic` | `continuous_parameter_set` | `lower_bound` | `fixed_sample` | `yes` | `yes` | `partial` | `yes` | `yes` | `yes` |
| Juditsky–Nemirovski 2016 | `other` | `non_asymptotic` | `continuous_parameter_set;distributional_uncertainty` | `none` | `fixed_sample` | `yes` | `yes` | `no` | `no` | `yes` | `no` |
| Guigues et al. 2020 | `other` | `non_asymptotic` | `continuous_parameter_set;distributional_uncertainty` | `sample_complexity_converse` | `fixed_sample` | `yes` | `yes` | `partial` | `yes` | `yes` | `yes` |
| Wei et al. 2019 | `likelihood` | `non_asymptotic` | `continuous_parameter_set` | `lower_bound` | `fixed_sample` | `yes` | `yes` | `yes` | `yes` | `no` | `no` |
| Birgé 1982 | `likelihood;other` | `non_asymptotic` | `distributional_uncertainty` | `none` | `fixed_sample` | `yes` | `yes` | `no` | `no` | `yes` | `no` |
| Guntuboyina 2011 | `other` | `non_asymptotic` | `finite_scenario_set;continuous_parameter_set` | `lower_bound` | `fixed_sample` | `yes` | `partial` | `yes` | `yes` | `no` | `no` |
| Venkataramanan–Johnson 2018 | `other` | `non_asymptotic` | `finite_scenario_set` | `lower_bound` | `fixed_sample` | `yes` | `no` | `partial` | `yes` | `no` | `no` |
| Addario-Berry et al. 2010 | `likelihood;other` | `non_asymptotic` | `finite_scenario_set` | `lower_bound` | `fixed_sample` | `yes` | `no` | `no` | `yes` | `no` | `no` |
| Comminges–Dalalyan 2013 | `other` | `global_asymptotic` | `continuous_parameter_set` | `lower_bound` | `fixed_sample` | `no` | `yes` | `yes` | `yes` | `no` | `no` |

For every row, `full_text_inspected=yes`,
`screening_disposition=retained`, and the exact `evidence_location` should be
copied from the verified-anchor table above. No source in this handoff directly
tests metabolic structural alternatives; `structural_alternatives=no` is the
conservative coding.

## Corrected search-closure interpretation

The earlier handoff interpretation that query families A–C had reached
method-family saturation is withdrawn. Each family is now
`ANCHOR_FAMILIES_VERIFIED`: OpenAlex and Crossref searches and bounded
citation passes found and verified the principal positive method families
listed above. The exported result windows and citation passes were truncated,
so they do not establish exhaustive coverage or the absence of another
load-bearing family.

All 444 occurrences retain final scoped screening states, and the nearest
primary anchors used for the affirmative existence conclusions are inspected
in full. Inaccessible or deferred records remain prohibited from supporting
theorem-specific, absence, converse, guarantee, or novelty statements. The
controlling search-closure assessment is
`audit/phase2_saturation_log.md`.
