# Fixed-Sample Composite-Testing Foundations

## Scope and evidence rule

This analysis asks whether fixed-sample discrimination between metabolic
mechanism classes lacks general testing theory, or whether the unresolved work
is applying and computing established results for nonlinear isotope forward
models. It addresses GAP-01 and GAP-03 only. A result is treated as established
only when the primary full text was inspected and an exact theorem, section,
equation, proposition, or methodological passage is recorded in
`corpus/papers.csv`. Abstract-only and inaccessible records are not evidence
for any conclusion below.

The evidence supports a narrower conclusion than the original Phase 2A
synthesis: fixed-sample composite tests, uniform nonasymptotic error bounds,
heterogeneous-product constructions, and several converse families already
exist. The unresolved EMU work is principally representation and global
optimisation. This is neither an absence claim nor a novelty claim.

This conclusion is affirmative: it follows from inspected primary theorems
that exhibit the relevant tests and bounds. It does not depend on declaring
the search saturated, finding no additional method family, or treating
title/abstract dispositions as methodological exclusions.

## Precise EMU-induced testing problem

Let a registered design be

`d = (d_1, ..., d_K)`,

where each block design may specify tracer identity and mixture, enrichment,
intervention, condition, measured fragments, sampling times, and observation
platform. Let `n = (n_1, ..., n_K)` be a fixed replicate allocation with total
budget `N = sum_k n_k`. For mechanism `m` in `{0,1}`, define

`zeta = (v, gamma, eta_shared, eta_1, ..., eta_K, b) in Z_m(d)`,

where:

- `v` denotes mechanism-specific fluxes, commonly constrained to a continuous
  feasible-flux polytope;
- `gamma` denotes other kinetic or biological parameters;
- `eta_shared` denotes nuisance parameters constrained to be common across
  blocks;
- `eta_k` denotes condition-specific nuisance parameters;
- `b` denotes an optional, explicitly bounded forward-model discrepancy; and
- `Z_m(d)` may encode reaction, pathway, compartment, atom-map, or broader
  mechanism-class alternatives.

The EMU forward map and a declared observation model induce a block law

`nu_(m,k,zeta,d_k)`.

Under independent sampling, the complete fixed-block law is

`P^(d,n)_(m,zeta)
  = tensor_(k=1)^K [nu_(m,k,zeta,d_k)]^(tensor n_k)`.

The competing composite families are

`P_m(d,n) = {P^(d,n)_(m,zeta) : zeta in Z_m(d)}`.

This representation allows IID blocks as a special case and independent but
non-identically distributed blocks in general. It also exposes an important
distinction: shared nuisance parameters couple the block means and prevent
replacement of the joint family by an unconstrained Cartesian product of
blockwise families.

For a possibly randomised test `phi` taking values in `[0,1]`, define

`alpha_(d,n)(phi) = sup_(P in P_0(d,n)) E_P[phi]`,

`beta_(d,n)(phi)  = sup_(Q in P_1(d,n)) E_Q[1-phi]`,

and

`R*_(d,n) = inf_phi max{alpha_(d,n)(phi), beta_(d,n)(phi)}`.

A finite-sample sufficiency certificate at tolerance `epsilon` exhibits a
computable `phi` and proves both errors at most `epsilon`. A fixed-design
converse lower-bounds `R*_(d,n)` or proves a necessary `N`. A design-wide
impossibility certificate must establish that every admissible `(d,n)` fails
the registered tolerance or budget.

The following features determine which adjacent theorem applies:

1. whether all laws share a measurable observation space and a dominating
   measure required by the chosen theorem;
2. whether the induced law sets, or useful representations of them, are
   convex, compact, separated, finitely coverable, or metrically controlled;
3. whether nuisance parameters are shared across blocks;
4. whether the EMU image and its convex hull can be represented and optimised
   over with certified error;
5. whether the forward discrepancy is bounded tightly enough to preserve
   separation; and
6. whether the design set is finite or requires continuous global
   optimisation.

For any fixed test, error is linear in the observation law, so its supremum
over a family equals its supremum over that family’s convex hull.
Consequently, taking both convex hulls leaves every test’s worst-case risk,
and hence the infimum of those risks, unchanged. Passing additionally to a
closure requires the corresponding continuity assumptions. Intersection of
the convex hulls is therefore a valid least-favourable-mixture obstruction,
but it is not proof that one physical parameterisation belongs to both
original mechanism families. This interpretive distinction matters even when
convexification is decision-theoretically exact.

## Verified primary-source anchor register

The following sources are all linked to stable corpus IDs. The location after
each citation is the inspected primary-source location that supports the
stated result.

- **P0053 — Goldenshluger A, Juditsky A, Nemirovski A. “Hypothesis testing
  by convex optimization.” Electronic Journal of Statistics.
  2015;9(2):1645–1712. DOI `10.1214/15-EJS1054`.** Theorem 2.1 and
  equations (3)–(6) construct a
  least-favourable-pair detector and uniformly bound both errors; the same
  theorem gives a near-optimal risk comparison. The repeated/nonstationary
  observation section and Proposition 3.2, equations (24)–(25), give
  multiplicative risk bounds for heterogeneous products. The arXiv source
  locations are lines 269–376, 606–727, 995–999, and 2933–3055.
- **P0060 — Birgé L. “Tests robustes pour des variables indépendantes et des
  chaînes de Markov.” Annales scientifiques de l’Université de Clermont.
  Mathématiques. 1982;71(20):70–77. Numdam
  `ASCFM_1982__71_20_70_0`.** Section II, theorem and corollary on pp. 72–73,
  construct tests between separated Hellinger balls with simultaneous
  exponential error bounds; Section III, theorem and corollary on pp. 74–75,
  treat independent non-identically distributed product laws.
- **P0059 — Guntuboyina A. “Lower Bounds for the Minimax Risk Using
  f-Divergences, and Applications.” IEEE Transactions on Information Theory.
  2011;57(4):2386–2399. DOI `10.1109/TIT.2011.2110791`.** Section II,
  Theorem II.1 and Corollaries II.2–II.3, give finite-sample
  `f`-divergence and sharp two-law total-variation lower bounds; Example II.4
  recovers Fano’s inequality; Theorem III.1 and Theorem IV.1 give
  covering/packing and global metric-entropy reductions.
- **P0058 — Juditsky A, Nemirovski A. “Hypothesis testing via affine
  detectors.” Electronic Journal of Statistics.
  2016;10(2):2204–2242. DOI `10.1214/16-EJS1170`.** Section 3,
  Propositions 1–2 and the sub-Gaussian
  propositions, give fixed-prescribed-sample affine detectors and uniform
  exponential-risk bounds; Proposition 3 constructs tests for multiple
  hypotheses, including conditionally heterogeneous observations. Primary
  source lines 367–714 contain the relevant results.
- **P0057 — Guigues V, Juditsky A, Nemirovski A. “Hypothesis testing via
  Euclidean separation.” Annales de l’Institut Henri Poincaré, Probabilités
  et Statistiques. 2020;56(3). DOI `10.1214/19-AIHP1022`.** The inspected
  arXiv:1705.07196 author source defines the stationary and semi-stationary
  problem at lines 192–240; Propositions 1 and `OptMajTest` at lines 381–491
  and Proposition `prop133` at lines 494–719 give constructive uniform tests
  for separated convex signal sets under sub-spherical noise; lines
  1805–1857 give the sample-count comparison.
- **P0055 — Wei Y, Wainwright MJ, Guntuboyina A. “The geometry of hypothesis
  testing over convex cones: Generalized likelihood ratio tests and minimax
  radii.” Annals of Statistics. 2019;47(2). DOI
  `10.1214/18-AOS1701`.** The fixed Gaussian model and uniform-error/minimax
  radius are defined at source lines 674–810; Theorem `ThmGLRT` at
  lines 1079–1165 is constructive; Theorem `ThmLBGen` at lines 1668–1738
  and its proof at lines 2268–2421 give the matching information-theoretic
  lower-bound side for the stated cone classes.
- **P0065 — Gül G, Zoubir AM. “Robust Hypothesis Testing with
  α-Divergence.” IEEE Transactions on Signal Processing.
  2016;64(18):4737–4750. DOI `10.1109/TSP.2016.2569405`.** Section II-A,
  equations (1)–(7), defines
  dominated divergence-ball alternatives and three error criteria;
  Section II-B, equations (8)–(10), states the saddle problem;
  Theorem III.1 and equations (15)–(20) construct the unique
  least-favourable laws and test. Section III-C gives the
  maximum-robustness/overlap boundary.
- **P0074 — Gül G, Zoubir AM. “Robust hypothesis testing for modeling
  errors.” 2013 IEEE International Conference on Acoustics, Speech and
  Signal Processing. 2013:5514–5518. DOI
  `10.1109/ICASSP.2013.6638718`.** Section 2.1, equations (1)–(6), defines
  the two squared-Hellinger neighbourhoods, false-alarm and miss
  probabilities, and minimax Bayes-error problem; Sections 2.2–2.3 derive
  the least-favourable laws and robust likelihood-ratio rule. This is an
  exact one-observation construction for that special dominated
  uncertainty class, not a replicate or experiment-design theorem.
- **P0071 — Gül G, Zoubir AM. “Robust hypothesis testing with squared
  Hellinger distance.” Proceedings of the 22nd European Signal Processing
  Conference (EUSIPCO). 2014:844–848. DOI
  `10.5281/zenodo.54502`.** Sections 2.1–3, equations (1)–(6), define
  squared-Hellinger balls and the minimax problem; Sections 2.2–4 derive the
  least-favourable test; Section 4, equations (23)–(36), Figure 1, and
  Section 5 identify radii at which the least-favourable laws overlap.
- **P0072 — Suresh AT. “Robust hypothesis testing and distribution
  estimation in Hellinger distance.” Proceedings of AISTATS, PMLR 130.
  2021. Identifier `PMLR:v130:theertha-suresh21a`.** The problem definition
  and `HellingerTest` are on pp. 1–2; Theorem 1 gives a constructive
  fixed-sample upper/sample-complexity bound and Theorem 2 gives a lower
  obstruction for the stated Hellinger-margin neighbourhoods.
- **P0062 — Berger RL, Boos DD. “P Values Maximized Over a Confidence Set
  for the Nuisance Parameter.” Journal of the American Statistical
  Association. 1994;89(427):1012–1016. DOI
  `10.1080/01621459.1994.10476836`.** Journal pp. 1012–1013 define
  `p_beta = sup_(eta in C_beta) p(eta) + beta` and prove finite-sample
  conservative Type-I validity. No Type-II or sample-size result is claimed.
- **P0064 — Dufour J-M. “Monte Carlo tests with nuisance parameters: A
  general approach to finite-sample inference and nonstandard asymptotics.”
  Journal of Econometrics. 2006;133(2):443–477. DOI
  `10.1016/j.jeconom.2005.06.007`.** Section 4, equations (4.1)–(4.20),
  Propositions 4.1–4.2 on pp. 18–20 of the inspected manuscript, give
  exact/conservative finite-sample Type-I control after nuisance
  maximisation. Propositions 5.1–5.2 are asymptotic and are not used as
  finite-sample evidence.
- **P0070 — Wasserman L, Ramdas A, Balakrishnan S. “Universal Inference.”
  Proceedings of the National Academy of Sciences.
  2020;117(29):16880–16890. DOI `10.1073/PNAS.1922664117`.** Theorem 1
  gives a finite-sample confidence
  set; the universal hypothesis-test construction and Theorem 3 give
  split/cross-fit likelihood-ratio Type-I control for dominated IID
  composite nulls. The profile-likelihood nuisance discussion is in Methods
  and the supplement. Uniform Type-II or sample-complexity control is not
  proved.
- **P0066 — Baraud Y. “Non-asymptotic minimax rates of testing in signal
  detection.” Bernoulli. 2002;8(5):577–606.** Section 1, equations (1)–(2),
  specifies the Gaussian sequence problem; Proposition 1 and Theorem 1 on
  pp. 4–5 give lower bounds; Proposition 2 on pp. 5–6 constructs a
  chi-square test with upper bounds; Propositions 3–4 give additional
  structured-class cases.
- **P0067 — Baraud Y, Huet S, Laurent B. “Adaptive tests of linear
  hypotheses by model selection.” Annals of Statistics.
  2003;31(1):225–251. DOI `10.1214/AOS/1046294463`.** Section 2,
  equations (2)–(5), gives exact
  level; Theorem 1 on pp. 230–231 gives a finite-sample power set;
  Proposition 1 and Corollaries 1–2 on pp. 231–236 treat the composite
  linear-subspace null with unknown common variance. The model assumes IID
  Gaussian errors (p. 227).
- **P0068 — Laurent B, Loubès J-M, Marteau C. “Non asymptotic minimax rates
  of testing in signal detection with heterogeneous variances.” Electronic
  Journal of Statistics. 2012;6:91–122. DOI
  `10.1214/12-EJS667`.** Section 2,
  Proposition 1 and Theorem 1, give lower bounds; Section 3, Proposition 2
  and Theorem 2, and Section 4, Proposition 3 and Theorem 3, give
  constructive upper bounds for independent heterogeneous Gaussian
  coordinates.
- **P0063 — Balakrishnan S, Wasserman L. “Hypothesis testing for densities
  and high-dimensional multinomials: Sharp local minimax rates.” Annals of
  Statistics. 2019;47(4). DOI `10.1214/18-AOS1729`.** The level, worst
  Type-II error, and local minimax critical radius are defined before Theorem 1;
  Theorem 1 constructs the truncated chi-square test; the main
  Lipschitz-class theorem supplies a matching lower bound for the stated
  density class.
- **P0056 — Venkataramanan R, Johnson O. “A strong converse bound for
  multiple hypothesis testing, with applications to high-dimensional
  estimation.” Electronic Journal of Statistics. 2018;12(1). DOI
  `10.1214/18-EJS1419`.** Section 2, Theorem 1 and equation (main), give a
  finite-sample Rényi-divergence lower bound on average error for finite
  multiple hypotheses; Section 2.1 compares Birgé/Fano/Assouad forms.
- **P0069 — Polyanskiy Y, Poor HV, Verdú S. “Channel Coding Rate in the
  Finite Blocklength Regime.” IEEE Transactions on Information Theory.
  2010;56(5):2307–2359. DOI `10.1109/TIT.2010.2043769`.** Section III-E,
  equations (100)–(105), gives the beta-alpha formulation; Theorems 26–27
  and 30–31 give exact nonasymptotic fixed-block converse bounds for finite
  message sets. Transfer to a composite mechanism problem requires a finite
  packing or prior reduction.
- **P0054 — Addario-Berry L, Broutin N, Devroye L, Lugosi G. “On
  combinatorial testing problems.” Annals of Statistics.
  2010;38(5):3063–3092. DOI `10.1214/10-AOS817`.** Section 1 defines a
  specialised finite Gaussian
  alternative family; Section 2 propositions give constructive upper bounds;
  Section 3 propositions give finite-sample lower bounds. The principal risk
  averages over a finite alternative prior and is not uniform control of an
  arbitrary continuous composite family.
- **P0052 — Comminges L, Dalalyan AS. “Minimax testing of a composite null
  hypothesis defined via a quadratic functional in the model of regression.”
  Electronic Journal of Statistics. 2013;7. DOI
  `10.1214/13-EJS766`.** Section 1, equations (1)–(4), defines the structured
  regression problem; Propositions 1–2 and Theorems 1–2 give constructive
  and lower-bound minimax separation results. The statements contain
  asymptotic `o(1)` terms and are rate evidence, not exact finite-sample
  calibration.

P0041 supplies additional verified minimax robust-testing evidence, but its
repeated-observation result is asymptotic. It is not used to strengthen the
exact finite-sample claims above. P0061 is a simulation-trained composite test
without a theorem establishing uniform finite-sample error and likewise does
not carry a guarantee claim. P0073 is a current non-peer-reviewed preprint and
is not needed for the conclusions.

## Primary-source family map

“Exact” below means exact finite-sample calibration or construction under the
source’s assumptions. “Nonasymptotic” means an explicit bound valid at finite
sample size, which need not be exact. “Rate” means a minimax separation or
order result rather than a usable exact constant.

| Requested family | Canonical formulation | Strongest verified fixed-sample result | Construction / guarantee | Composite and heterogeneous scope | Transfer to the EMU formulation |
|---|---|---|---|---|---|
| 1. Finite parametric composite hypotheses | test `theta in Theta_0` versus `theta in Theta_1` at a prescribed sample size | P0053 constructs least-favourable-pair tests for convex compact parameter sets in Gaussian, Poisson, categorical, and product schemes; P0055 gives GLRT upper and lower minimax radii for convex cones | constructive; uniform nonasymptotic upper bounds; minimax-related lower comparison, not universal exact minimaxity | composite versus composite; P0053 includes heterogeneous products | **APPLICABLE WITH COMPUTATIONAL ADAPTATION.** A finite-dimensional EMU parameterisation fits the abstract object, but its induced law image is generally nonconvex and computing its convex hull, least-favourable pair, or certified cover is the obstruction. |
| 2. Convex distribution classes | test one convex set of dominated laws against another | P0053 Theorem 2.1 and the discrete-scheme discussion construct an affinity detector; P0065 and P0071 solve specified convex divergence-neighbourhood saddle problems | constructive; uniform; exact one-vector minimax for the specified robust neighbourhoods, nonasymptotic near-minimax more generally | composite versus composite; domination and convexity are explicit | **APPLICABLE WITH COMPUTATIONAL ADAPTATION.** Convexification leaves fixed-test worst-case risk and the resulting minimax value unchanged, but a convex-hull intersection is a mixture obstruction, not physical EMU-parameter overlap; representing that hull remains difficult. |
| 3. Metric-separated or entropy-controlled classes | test separated metric balls, covers, or packings | P0060 constructs Hellinger-ball tests with exponential two-error bounds; P0059 gives finite-sample packing, covering, and global metric-entropy lower bounds | upper construction for separated balls; minimax converse for finite reductions; explicit finite bounds or rate bounds depending on geometry | composite versus composite for the Birgé upper test; arbitrary finite subsets for the converse | **APPLICABLE WITH COMPUTATIONAL ADAPTATION.** Transfer requires a certified Hellinger/TV separation or cover of the nonlinear EMU law image; an uncertified flux grid is insufficient. |
| 4. Robust contamination or neighbourhood models | test laws lying in uncertainty neighbourhoods around competing nominal laws | P0074, P0065, and P0071 construct exact single-vector minimax tests for squared-Hellinger or alpha-divergence balls; P0072 gives a fixed-sample test and sample-complexity upper/lower bounds for Hellinger-margin neighbourhoods | constructive; uniform/minimax for stated neighbourhoods; exact for P0074/P0065/P0071 and nonasymptotic sample-complexity for P0072 | composite versus composite; the verified anchors concern divergence/Hellinger neighbourhoods, not every contamination class | **APPLICABLE WITH COMPUTATIONAL ADAPTATION.** Transfer is direct only in the special case where forward/noise uncertainty is deliberately specified by the same neighbourhood class. A mechanistic flux family instead needs a certified outer representation; without one, the theorem answers a different uncertainty problem. |
| 5. Nuisance-parameter problems | control error uniformly while nuisance values are unknown | P0062 and P0064 give finite-sample conservative Type-I control by maximising over nuisance sets; P0070 gives finite-sample universal likelihood-ratio Type-I control; P0067 gives exact level and explicit finite-sample power sets for an IID Gaussian linear model with unknown variance | constructive; uniform Type-I control in general anchors; two-error power only in structured models | usually composite null; the generic procedures do not give uniform Type-II/sample-size guarantees | **APPLICABLE WITH COMPUTATIONAL ADAPTATION.** Type-I control transfers if exact nuisance-specific tests or likelihoods can be computed. Full two-error EMU discrimination additionally requires optimisation over both mechanism families and shared nuisance constraints. |
| 6. Semiparametric and nonparametric classes | test a null against alternatives separated in a norm, smoothness class, or high-dimensional geometry | P0066, P0063, and P0068 provide constructive nonasymptotic upper bounds and minimax lower bounds for stated Gaussian, density, multinomial, or heterogeneous-variance classes; P0052 gives asymptotic minimax rates for a quadratic-functional regression class | constructive and minimax; finite bounds for the first three, rate/asymptotic for P0052 | most are simple or structured composite nulls versus separated composite alternatives | **NOT APPLICABLE** as class-specific theorems unless the EMU laws satisfy the same Gaussian/smoothness/geometric assumptions. Their packing and separation proof devices transfer through family 11; their particular minimax rates do not establish an EMU rate. |
| 7. IID fixed-block observations | observe `N` independent copies from one class member | P0053’s repeated-observation section compounds detector risk as a power of the one-observation affinity; P0072 gives explicit fixed-`N` robust-testing sample complexity | constructive; uniform nonasymptotic; near-optimal or matching-order under stated classes | composite versus composite under represented classes | **DIRECTLY APPLICABLE** once a common IID observation law and uncertainty class are declared and the required detector/separation can be computed. |
| 8. Independent non-identically distributed observations | observe a prescribed product of block-specific laws | P0060 Section III gives robust tests for independent non-identical product laws; P0053’s nonstationary products and P0058’s conditionally heterogeneous observations give multiplicative risk constructions; P0068 supplies structured heterogeneous-coordinate minimax bounds | constructive; uniform finite-sample under stated separations/schemes | composite versus composite in P0060/P0053; explicit heterogeneous blocks | **APPLICABLE WITH COMPUTATIONAL ADAPTATION.** Independent heterogeneity itself is established. The obstruction is preserving shared nuisance constraints in the joint nonlinear EMU feasible set; freeing them blockwise enlarges the family and may erase separation. |
| 9. Multiple hypotheses | decide among more than two finite or composite alternatives | P0058 Proposition 3 gives a detector assembly for multiple hypotheses; P0056 and P0059 give finite-sample M-ary converse bounds; P0054 supplies a specialised finite combinatorial example | constructive upper tests for represented classes; minimax/average-error lower bounds for finite reductions | finite multiple hypotheses; composite extensions require pairwise class detectors or finite packings | **APPLICABLE WITH COMPUTATIONAL ADAPTATION.** A finite set of metabolic structures can use pairwise detectors or a finite packing, but continuous within-mechanism parameters retain the same representation problem. |
| 10. Upper-bound constructions | exhibit a test and prove both registered errors are small | P0053, P0060, P0057, and P0058 provide explicit detector constructions; P0066–P0068 give structured chi-square/model-selection tests; P0062/P0064/P0070 give Type-I-only constructions | constructive; uniform two-error bounds for convex/separated/structured alternatives, or Type-I-only where stated | both composite-versus-composite and structured one-sided composite problems occur | **APPLICABLE WITH COMPUTATIONAL ADAPTATION.** The probability theory transfers under source assumptions; a certified EMU set representation and computable detector are still required. |
| 11. Lower-bound and converse methods | lower-bound every test’s risk or required sample size | P0059 gives two-point `f`-divergence, Fano, packing, and entropy bounds; P0056 gives a Rényi strong converse for finite M-ary testing; P0069 gives finite-block beta-alpha/meta-converse machinery; P0066/P0068/P0072 give class-specific lower bounds | converse only; finite-sample; minimax or Bayes/average-error depending on the theorem; exact constants in some forms and rate-level in others | arbitrary selected pairs or finite packings; product-law divergences encode a fixed heterogeneous design | **DIRECTLY APPLICABLE** at the inequality level. The EMU-specific task is computational: select a valid pair/packing, evaluate joint-law divergences, and optimise the resulting bound over design. |
| 12. Computational tractability | compute the detector, least-favourable pair, cover/packing, or globally best design | P0053 and P0057 reduce supported convex cases to convex or Euclidean-separation programmes; P0065/P0071 solve special divergence-ball saddle systems. The verified sources supply certified computation for their stated representations, not for an arbitrary nonlinear nonconvex image | constructive for stated convex/special classes; no complexity result for arbitrary EMU families is inferred | depends on the represented class; heterogeneous convex products are covered | **APPLICABLE WITH COMPUTATIONAL ADAPTATION.** The precise obstruction is nested global optimisation over a nonlinear EMU image, shared constraints, and mixed discrete/continuous designs, plus certified approximation error. Current evidence does not justify calling that obstruction a missing generic testing theorem. |

## What transfers directly

### Exact overlap and convex-mixture obstructions

If one law `P` belongs to both original families, then for every `phi`,

`alpha(phi) >= E_P[phi]`,

`beta(phi) >= E_P[1-phi]`,

so `max(alpha,beta) >= 1/2`. This is a direct identifiability obstruction.
P0059’s two-law total-variation result supplies the quantitative nearby-law
version. P0071 and P0065 explicitly identify overlap boundaries for their
robust neighbourhoods.

If only the convex hulls intersect, the same one-half lower bound applies to
the randomised minimax problem through least-favourable mixtures. That is a
valid decision-theoretic converse, but it must not be reported as an exact
physical-parameter overlap.

### Pairwise, packing, and product-law converses

Any pair `P in P_0(d,n)`, `Q in P_1(d,n)` gives a valid lower bound for the
full composite risk. A finite set of induced laws gives a Fano,
Rényi-strong-converse, or packing reduction (P0059, P0056). For independent
blocks, divergence is evaluated on the joint product law; KL divergence adds
blockwise when its usual absolute-continuity conditions hold. Solving a
finite-sample bound for `N` yields a necessary sample-size statement. None of
these steps requires sequential stopping.

### Independent heterogeneous blocks

P0060 and P0053 establish that fixed, independent, non-identically
distributed observations are already within constructive finite-sample
theory. Therefore heterogeneous condition or tracer blocks are not by
themselves a theoretical obstruction. The remaining difficulty is the
geometry of the joint parameter image, especially when nuisance components
must be shared.

## What does not transfer automatically

- **Representation of nonlinear families.** A continuous flux polytope mapped
  through a nonlinear EMU solver generally does not arrive in the convex,
  conic, divergence-ball, or smoothness-class representation required by the
  constructive anchors.
- **Certified approximation.** A simulation grid controls only its sampled
  points. Extending its guarantee to the continuous class requires a proved
  covering radius and a continuity bound for the chosen law metric or
  detector risk.
- **Shared nuisance constraints.** Treating a common nuisance value as
  independently variable in each condition enlarges the family. Although the
  resulting test may remain valid, it can be needlessly powerless; preserving
  the shared constraint creates a coupled, commonly nonconvex programme.
- **Mechanistic interpretation of convexification.** Convexification can be
  exact for minimax test risk, but a least-favourable mixture need not
  correspond to any feasible metabolic state. A report must distinguish a
  mixture-risk converse from physical nonidentifiability.
- **Continuous design optimisation.** Applying a certified bound to each
  member of a finite design list is direct. Proving a global result over
  tracer mixtures, interventions, measurement panels, and replicate
  allocations requires a nested mixed discrete/continuous optimisation that
  the verified testing theorems do not solve.
- **Forward-model discrepancy.** If the declared discrepancy class is so
  broad that the two induced families overlap, impossibility follows from
  that modelling choice. If it is unspecified, no uniform robustness claim
  can be made.
- **Observation-law compatibility.** Detector constructions that assume a
  common dominated “good observation scheme” cannot be invoked until the
  corrected MID/count/noise law satisfies those conditions. General
  total-variation and `f`-divergence lower bounds are less restrictive, but
  their numerical evaluation can still fail without a well-defined common
  sample space.

## Access limits not used as evidence

The following records remain unavailable and support no theorem-level claim:

- Birgé’s 1983 English chapter (C0402) is inaccessible, but the legally
  accessible 1982 French primary article P0060 supplies the consequential
  Hellinger and independent-nonidentical results.
- Bernshtein (1981; C0483) could not be inspected, so no nuisance,
  finite-sample, or converse result is attributed to it.
- The Gül book chapters C0283, C0285, and C0286 and the composite-distance
  proceedings record C0653 remain inaccessible; P0041 and P0065/P0071/P0074
  cover the verified parts of the robust-testing family.
- The Lapidoth chapters C0241/C0242, Linnik chapter C0231, Jurečková and
  Navrátil C0235, and Zarrin and Lim C0136 remain unavailable and carry no
  guarantee claim.
- Wefelmeyer C0405 and Li C0480 are not used for a substantive conclusion
  here. Their available evidence did not supply an inspected load-bearing
  fixed-sample theorem for this synthesis. Their ledger dispositions are
  administrative screening records, not proof that the papers are
  methodologically irrelevant.
- The inaccessible 2024 fixed-budget POMDP record was not used. Fixed-block
  converse conclusions instead rely on verified P0059, P0056, and P0069.
- Huber and Strassen (1973) could not be accessed through the attempted
  official route and are not used to establish the robust-neighbourhood row.

## Conclusion for the bounded repair

The primary evidence falsifies the broad claim that statistics lacks
fixed-sample tests for composite classes, uniform nonasymptotic two-error
bounds under useful structural assumptions, independent heterogeneous-block
constructions, or finite-sample converse machinery. The exact EMU residual is
to represent or cover the nonlinear induced families with certified error,
compute tests and least-favourable pairs or packings, and optimise the
experiment globally while respecting shared constraints and mechanistic
interpretation. On current evidence that residual is computational, with any
future theoretical claim requiring a separately stated approximation,
complexity, or tractability theorem.

The evidence boundary is:

- **generic theory already established:** the positive upper- and lower-bound
  results cited above are enough to weaken the broad GAP-01 and GAP-03 theory
  propositions;
- **verified computational limitation:** the constructive anchors require
  represented convex, separated, regular or neighbourhood classes, while
  P0049 verifies a nested local biochemical design computation rather than a
  global continuous-class certificate;
- **biological/application issue:** a concrete EMU problem must declare its
  mechanisms, observation law, sharing constraints, replicate semantics,
  costs and any discrepancy class;
- **software-integration issue:** wiring an EMU simulator to a detector,
  converse calculation and design optimiser is implementation work unless it
  carries a separately proved approximation or tractability result; and
- **unresolved/deferred evidence:** inaccessible or discovery-level records
  support no absence conclusion. They are not needed for the affirmative
  finding that general tests and converses already exist, and this bounded
  repair does not claim literature-family saturation.
