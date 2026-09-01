# Phase 2A Workstream C: adjacent decision theory

> **Phase 2A.1 evidence repair (2026-07-31):** prospective records have
> auditable dispositions, but title/abstract dispositions are not treated as
> proof of irrelevance or literature saturation. GAP-01 and GAP-03 are
> `WEAKENED` affirmatively because inspected primary results exhibit general
> fixed-sample composite tests and converses. Certified EMU representation
> and nested design computation remain unresolved.

## Scope and evidence key

This workstream attempted to falsify the need for an EMU-specific
decision-theoretic contribution by asking whether established model
discrimination, active testing, robust testing and finite-sample sample
complexity results already transfer. Search provenance and all prospective
dispositions are in `audit/phase2_search_log_C.md` and
`audit/phase2_screening_C.csv`.

Load-bearing sources inspected in complete primary text:

- **C-LB01 / P0038** — Dette H, Titoff S. Optimal discrimination designs. *Annals of
  Statistics*. 2009;37:2056–2082. DOI `10.1214/08-AOS635`. Evidence:
  Section 2, equations (2.3), (2.7)–(2.9), Theorems 2.1–2.2; Section 3,
  Theorem 3.1 and Corollary 3.2; Section 4, equations (4.1)–(4.2); Section 5
  simulation. Full arXiv primary manuscript inspected.
- **C-LB02 / P0039** — Mélykúti B, August E, Papachristodoulou A, El-Samad H.
  Discriminating between rival biochemical network models: three approaches
  to optimal experiment design. *BMC Systems Biology*. 2010;4:38. DOI
  `10.1186/1752-0509-4-38`. Evidence: Background; Results and Discussion,
  “Problem formulation,” equations (1)–(3), and the three design sections;
  Conclusions. Complete PMC primary XML inspected.
- **C-LB03 / P0040** — Dette H, Melas VB, Guchenko R. Bayesian T-optimal
  discriminating designs. *Annals of Statistics*. 2015;43:1959–1985. DOI
  `10.1214/15-AOS1333`. Evidence: Section 2, equations (2.3)–(2.6) and
  Theorem 2.1; Section 3, Algorithm 3.2 and Theorem 3.3; Section 4 examples.
  Complete author manuscript in PMC inspected.
- **C-LB04 / P0041** — Gül G, Zoubir AM. Minimax Robust Hypothesis Testing. *IEEE
  Transactions on Information Theory*. 2017;63:5572–5587. DOI
  `10.1109/TIT.2017.2693198`. Evidence: primary arXiv source, Sections II–III
  (dominating measure, uncertainty classes, saddle-value formulation and
  least-favourable densities), Section IV (fixed sample size and Cramér
  asymptotics), Section V (sequential tests and counterexamples), Conclusion.
- **C-LB05 / P0042** — Garivier A, Kaufmann E. Optimal Best Arm Identification with
  Fixed Confidence. *PMLR*. 2016;49:998–1027. Evidence: Section 2.1,
  Theorem 1 and equation (1); Section 4, Theorem 10; Section 5, Theorem 14.
  Complete official PMLR PDF inspected.
- **C-LB06 / P0043** — Grünwald P, de Heide R, Koolen WM. Safe testing. *Journal of
  the Royal Statistical Society B*. 2024;86:1091–1128. DOI
  `10.1093/jrsssb/qkae011`. Evidence: equation (1); Proposition 1 and equation
  (3); Definition 1; Proposition 2; Corollary 1 and equation (7); Theorem 1
  in Sections 2–4, especially the full version in Section 4.3 and equations
  (25)–(27). Complete primary arXiv manuscript inspected.
- **C-LB07 / P0044** — Levy BC. Robust hypothesis testing with a relative entropy
  tolerance. *IEEE Transactions on Information Theory*. 2009;55:413–421.
  DOI `10.1109/TIT.2008.2008128`. Evidence: Section II, equations
  (2.2)–(2.7), including the minimax saddle point; Section III, equations
  (3.1)–(3.12); Section IV examples. Complete primary arXiv manuscript
  inspected.
- Existing Phase 1 load-bearing primary sources: **P0024** (minimax
  KL-optimal design, Sections 2–5, Theorems 1–3), **P0026** (controlled
  sensing, Proposition 1 and Theorems 1–5), **P0027** (Bayesian active
  sequential testing, Propositions 1–5), **P0028** (composite controlled
  sensing, Lemma 1, Proposition 1, Theorems 1–3), and **P0029** (Bayesian and
  standardized-maximin robust T-design, equations (3)–(6), Theorem 4.1).

Discovery-only and abstract-level records do not support the conclusions
below.

### Phase 2A.1 fixed-sample anchors

The following full-text-verified primary results supersede the provisional
fixed-sample transfer judgments in the original Workstream C analysis:

- **P0053** constructs uniform nonasymptotic tests between convex compact
  composite classes, including nonstationary product observations
  (Theorem 2.1, equations (3)–(6); Section 2.4.2; Proposition 3.2,
  equations (24)–(25)).
- **P0060** constructs robust Hellinger-separated tests and explicitly treats
  independent non-identically distributed product laws (Sections II–III,
  pp. 72–75).
- **P0065 and P0071** construct exact fixed-sample minimax tests for
  alpha-divergence and squared-Hellinger neighbourhoods and calculate
  overlap/maximum-robustness obstructions at the locations recorded in the
  corpus.
- **P0062, P0064 and P0070** give finite-sample Type-I constructions with
  continuous nuisance parameters or composite likelihoods; they do not by
  themselves give uniform Type-II power.
- **P0056, P0059, P0063, P0066, P0068–P0069 and P0072** supply
  finite-sample divergence, packing, metric/geometric and fixed-block upper
  or lower bounds.

Together these sources establish the existence of fixed-sample composite
tests, simultaneous two-error guarantees for stated classes,
heterogeneous-product constructions and finite-sample converses in general
statistics. Exact transfer to an EMU-induced family depends on representing
or certifiably covering its nonlinear law set and solving the resulting
least-favourable/design problems.

This is positive existence evidence, not an inference from a search stopping
rule. The verified theory does not by itself establish a biological EMU
application, a globally certified nonlinear computation, or an integrated
software implementation; inaccessible and discovery-level records remain
deferred.

### Evidence-regime audit note

The exact T/KL design characterisations in C-LB01 and the equivalence and
algorithm-convergence theorems in C-LB03 are not statistical asymptotic
guarantees. C-LB01's Section 5 power evidence is simulation-based; C-LB03's
Bayesian label describes prior-averaged criterion construction, not posterior
error calibration. These distinctions are carried into the row proposals in
`audit/phase2_workstream_C_handoff.md`.

Likewise, C-LB04 and C-LB07 compare distributional hypotheses and uncertainty
neighbourhoods; that alone is not evidence of structural-model alternatives.
C-LB06 treats general composite hypotheses and nuisance parameters, but does
not specifically instantiate reaction/pathway/mechanism structures.

## What the strongest adjacent results actually establish

### Discrimination-design criteria rank/separate; they do not by themselves certify decision error

C-LB01 defines T-optimality by maximising, over designs, the minimum
integrated squared difference between a fixed rival regression and a
parameterised alternative (equation (2.3)). Theorems 2.1–2.2 connect this to
best uniform approximation and characterise optimal support. Theorem 3.1
relates the criterion to a local `D1` problem in a nested regression model.
Section 4 supplies the analogous KL-distance criterion. These are exact
design-characterisation results under their assumptions, but Section 5
evaluates likelihood-ratio rejection probabilities by simulation. No
finite-sample type-I/type-II certificate or sample-complexity converse is
proved. Corollary 3.2 also shows a design can have at most `m2+1` support
points; the authors explicitly warn that this can be too few to estimate all
parameters in the extended model.

P0024 strengthens the criterion side: its maximin KL objective is uniform
over a stated continuous parameter set and has continuity/convergence
theorems. It still does not turn a discrimination distance into a
finite-sample error guarantee.

C-LB03 integrates T-distance over a parameter prior and proves an
equivalence theorem plus algorithmic convergence. Thus parameter
uncertainty and many pairwise comparisons are not, by themselves, missing
from discrimination design. The result is Bayesian criterion optimisation,
not a frequentist uniform decision-error certificate.

### Biological-network model discrimination already optimises perturbations

C-LB02 considers finite rival nonlinear ODE network structures and maximises
the `L2` distance between model outputs. Its design variables include initial
conditions, time-dependent inputs, and bounded structural/parameter changes
representing interventions such as gene knock-outs. This directly weakens
any broad claim that perturbation selection for mechanism discrimination is
absent in systems biology. The authors state that measurement noise is not
modelled directly; distance is used so that noisy measurements have a
“good chance” of discriminating. Therefore it does not certify error,
replicate number, or impossibility, and it is not an isotope/EMU forward
model.

The biochemical-network evidence is broader than this deterministic
example. P0048 designs stimuli, readouts and measurement times using overlap
of response distributions induced by uncertain parameters. P0049 implements
a semi-infinite max-min KL-derived design over bounded parameter regions.
P0050 ranks observables, times, conditions and measurement combinations using
posterior-predictive Jensen-Shannon divergence, and P0051 optimises a control
for separation of two fixed-parameter mechanisms. These sources establish
probabilistic, robust, Bayesian and control-design baselines, respectively.
They still rank or optimise separation criteria rather than supplying a
fixed-sample EMU two-error certificate.

### Finite-sample risk and converses exist for narrower sequential/simple problems

C-LB05 Theorem 1 gives a nonasymptotic lower bound on expected stopping time
for every `delta`-PAC strategy over one-parameter exponential-family bandits,
with the alternative set entering a maximin KL allocation. Theorem 10 gives
an explicit threshold that controls error by `delta` for every Bernoulli
bandit regardless of the sampling strategy. Theorem 14 proves asymptotic
sample-complexity optimality as `delta -> 0`. Thus “no finite-sample
certificate or sample-complexity converse exists in adjacent adaptive
design” is false. Transfer is not automatic: arms are finite, observations
come from one-parameter exponential families, the decision is the unique
best mean, and sampling is sequential.

P0026 similarly proves error-exponent bounds/converses for finite simple
hypotheses under controlled observations. P0027 has nonasymptotic Bayesian
cost bounds for finite simple hypotheses. P0028 reaches disjoint
exponential-family composite hypotheses, with finite error control and an
expected-delay lower bound, but remains sequential and assumes the
separation/regularity structure stated in its Section 2.

### Robust testing already handles distributional neighbourhoods, but not joint EMU design

C-LB04 formulates dominated binary uncertainty classes and obtains
least-favourable distributions and saddle-value tests for relative-entropy,
contamination and composite neighbourhoods. It explicitly requires a common
dominating measure and non-overlap small enough for the relevant classes.
Section IV studies fixed sample size through large-deviation asymptotics,
not an exact finite-sample certificate. Section V proves that some plausible
robustified sequential tests fail their proposed minimax properties and
records where only asymptotic robustness remains. This is strong
gap-destroying and contrary evidence for a broad “robust testing under model
uncertainty is absent” claim. It does not optimise an experiment through a
nonlinear EMU map, treat structural reaction alternatives, or accommodate
unknown deterministic forward discrepancy jointly with measurement noise.

C-LB07 supplies the earlier binary KL-neighbourhood result: equation (2.6)
minimises worst-case Bayes error over two convex compact density classes and
equation (2.7) characterises a saddle point and least-favourable pair. Its
derivation assumes dominated densities and, for the explicit solution,
monotone/symmetric nominal likelihood structure. This confirms that KL-ball
minimax testing is established; it does not supply experimental design or
continuous structural EMU alternatives.

### Heterogeneous evidence and shared nuisance do not automatically require new Type-I theory

C-LB06 Proposition 1 turns any e-variable into a level-`alpha` test uniformly
over a composite null. Definition 1 permits each study/batch to use a
conditionally valid e-variable based on the information available before
that batch. Proposition 2 proves that their running product is a test
supermartingale and remains an e-variable at any stopping time; Corollary 1
gives the anytime Type-I bound. Thus differently constructed, adaptively
continued experiment blocks can be combined without an IID assumption at the
block level, provided conditional validity is established for every null law.

The full Theorem 1 constructs growth-optimal/relative-maximin e-variables for
composite hypotheses and includes nuisance handling through coarsening and
group invariance. This directly weakens a claim that heterogeneous evidence
or shared nuisance invariably demands new testing theory. It does not
automatically yield an e-variable for an arbitrary EMU family: existence of
the required information projection, full-support/dominating-density
conditions, and conditional validity after data-dependent experiment choice
must be proved. It also controls Type-I error, not uniform Type-II error,
required replicate count, or a sample-complexity converse.

## Transfer classification to an EMU-generated observation model

An EMU formulation is taken here to induce, for design `d`, mechanism class
`m`, flux/nuisance parameter `theta_m`, and possible discrepancy `b`, an
observation law
`P_{m,theta_m,b}^{(d)}`. Multiple conditions may produce heterogeneous
blocks `P^{(d_1)} ... P^{(d_K)}` with some nuisance parameters shared and
others condition-specific.

| Method family | Classification | What transfers | What does not transfer / precise obstruction | Evidence |
|---|---|---|---|---|
| T-optimal model-discrimination design | **APPLICABLE WITH COMPUTATIONAL ADAPTATION** | Replace the rival regression means in the integrated squared-distance criterion by EMU-predicted MIDs; tracer, fragment, time point or perturbation can be the design variable. | Nonlinear constrained flux spaces make the inner best-approximation problem nonconvex. T-optimality supplies a ranking/characterisation, not finite-sample error control. Degenerate designs may not estimate all nuisance parameters. | C-LB01, equations (2.3), (2.7)–(2.9), Theorems 2.1–2.2, Corollary 3.2; P0029. |
| KL-optimal design | **APPLICABLE WITH COMPUTATIONAL ADAPTATION** | Given dominated likelihoods, compute KL separation between EMU-induced laws and optimise a tracer/measurement/condition design; maximin optimisation over a specified continuous flux set is already formulated. | Computing nested extrema over nonlinear feasible-flux sets may be intractable. If induced families overlap, the worst-case KL is zero; the criterion then reports no separation but does not itself provide an experiment-level finite-sample certificate or a general impossibility theorem. Unknown noise/forward discrepancy must first define a valid law. | C-LB01 Section 4; P0024 Theorems 1–3. |
| Robust/maximin discrimination design | **APPLICABLE WITH COMPUTATIONAL ADAPTATION** | Bayesian and standardized-maximin criteria, continuous maximin KL design, fixed-sample minimax tests over represented ambiguity classes, and P0049's biochemical max-min design all transfer once the uncertainty set is explicit. | The general risk formalism exists, but a nonlinear EMU `inf_design sup_family` computation can be globally inaccessible. Overlap must be certified and sampled maps cannot establish a continuous supremum. | P0024; P0029; P0041; P0049; P0053; P0065; P0071–P0072. |
| Bayesian discrimination design | **APPLICABLE WITH COMPUTATIONAL ADAPTATION** | Put priors on mechanism and continuous flux/nuisance parameters; integrate T-distance or posterior-predictive risk; use EMU simulation in the utility calculation. P0050 verifies this workflow in biochemical networks. | Conclusions are prior-dependent. A Bayesian average criterion does not provide uniform frequentist control, and high-dimensional posterior/evidence/utility integrals may be computationally inaccessible. | P0040 Theorem 2.1 and Algorithm 3.2; P0027; P0050 Methods Predictive Distributions and Experimental design. |
| Active hypothesis testing | **UNRESOLVED FROM CURRENT EVIDENCE** | Sequential posterior updating, action-dependent observation kernels and adaptive action selection map conceptually to choosing successive tracers/conditions. | P0027 treats finite simple hypotheses. EMU mechanisms are continuous composite families; flux/nuisance estimates influence action choice, and physical isotope experiments usually arrive in costly fixed blocks rather than one observation/action at a time. The inspected anchor does not establish that a new theorem is necessary. | P0027, Sections 2 and 4–6. |
| Controlled sensing | **UNRESOLVED FROM CURRENT EVIDENCE** | KL-based action allocation and error-exponent converses directly motivate choosing among finite tracer/measurement actions. | P0026 assumes finite simple hypotheses and controlled observations with specified kernels. Uniform guarantees under overlapping composite EMU families, nuisance sharing and blockwise non-IID observations are outside that result, but incomplete adjacent coverage precludes a theory-necessity claim. | P0026, Section II, Proposition 1, Theorems 1–5. |
| Sequential experimental design / Chernoff tests | **UNRESOLVED FROM CURRENT EVIDENCE** | Likelihood-ratio stopping and information-directed allocation transfer for a finite, sequentially sampled, fully specified EMU hypothesis set. | Typical metabolic designs commit biological replicates in batches; tracer changes cannot generally occur after every observation. Fixed-sample/batched cost and composite parameter fitting alter both the stopping rule and converse; current evidence does not determine whether the remaining step is theoretical or computational. | P0026; C-LB05 Theorems 1, 10 and 14. |
| Composite hypothesis testing | **APPLICABLE WITH COMPUTATIONAL ADAPTATION** | Set-valued hypotheses, uniform two-error risk, convex/metric-separated tests and general converse inequalities transfer at the level of induced observation laws. | EMU images may be nonconvex, singular or overlapping, and shared nuisance couples blocks; computing a useful least-favourable test or certified cover is the residual. | P0053; P0060; P0065; P0071–P0072; P0028. |
| Fixed-sample minimax testing | **APPLICABLE WITH COMPUTATIONAL ADAPTATION** | P0053/P0060/P0065/P0071–P0072 supply constructive uniform fixed-sample tests for stated composite classes; P0056/P0059/P0069 supply finite-sample converses. | None of these algorithms automatically represents an exact nonlinear EMU law family or globally optimises tracer/allocation choices. Convexification preserves worst-case testing risk but computing the hull/least-favourable mixture can be hard; a finite grid requires a certified covering error. | P0053; P0056; P0059–P0060; P0065; P0069; P0071–P0072. |
| Nonnested/overlapping-model testing | **APPLICABLE WITH COMPUTATIONAL ADAPTATION** | P0065/P0071 verify exact robust-class overlap obstructions and P0059 supplies general divergence/packing converses; exact intersection is a direct testing obstruction. | Calculating intersection or the nearest pair for fitted nonlinear EMU families and optimising it over design remains nonconvex. Vuong-family asymptotic records remain discovery-only and are not needed for this classification. | P0059; P0065 Section III-C; P0071 Section 4; P0018. |
| Heterogeneous non-IID blocks with shared nuisance | **APPLICABLE WITH COMPUTATIONAL ADAPTATION** | P0053 and P0060 already give fixed-sample heterogeneous-product constructions; conditional e-values add anytime Type-I aggregation. | Shared nuisance makes the joint feasible law set coupled and often nonconvex. Treating nuisance independently by block is conservative and can destroy separation; exact computation, not non-IID probability theory, is the residual. | P0053 Theorem 2.1/Proposition 3.2; P0060 Sections II–III; P0043. |
| Distributionally robust testing | **APPLICABLE WITH COMPUTATIONAL ADAPTATION** | Dominated ambiguity sets, least-favourable distributions, saddle tests and overlap-radius obstructions transfer when the declared EMU uncertainty genuinely has that form. | A feasible-flux image is not automatically a divergence ball, and replacing it by one can add nonmechanistic laws. The design-dependent least-favourable problem remains a nested nonconvex computation. | P0041; P0044; P0065; P0071–P0073. |

## Consequences for the candidate distinctions

- Ranking designs versus certifying sufficiency remains a substantive
  distinction. C-LB01/P0024/P0029 establish optimisation criteria; C-LB05
  shows what a genuine risk guarantee and sample-complexity converse look
  like in a narrower sequential problem.
- Achievable discrimination versus impossibility is not an untouched
  distinction in adjacent theory. Error-exponent and sample-complexity
  converses exist (P0026, P0028, P0056, P0059, P0069 and P0072). Their
  mathematical inequalities transfer to selected fixed-block EMU product
  laws; what remains unresolved is the certified least-favourable/packing and
  design computation for continuous families.
- “Composite testing” alone is too broad to sustain a gap. P0028 already
  treats composite controlled sensing. A residual claim must name the
  departures: overlapping/singular induced families, shared nuisance,
  heterogeneous fixed blocks, or forward-model error.
- Robustness over sampled flux maps is weaker than a continuous-set minimax
  statement, but continuous maximin design and distributional minimax
  testing both already exist (P0024, P0029, C-LB04). Any residual
  contribution must join those theories to the EMU observation family and
  state verifiable separation and computation conditions.
- A broad “new mathematical theory is required” conclusion is not supported.
  Phase 2A.1 establishes the generic fixed-sample composite tests and
  converse templates. The registered EMU residual is computational:
  certified representation or covering of nonlinear law families,
  least-favourable-pair/packing computation and nested design optimisation.

## Access and evidence limitations

The original Atkinson–Fedorov papers and Chernoff (1959) remained
inaccessible in Phase 1 and were not repeatedly retried. Later open primary
papers supply the load-bearing criterion and guarantee evidence used here.
The Vuong-family records remain discovery-level. The heterogeneous-batch and
shared-nuisance route has load-bearing evidence from C-LB06, limited to its
conditional-e-value and stated nuisance constructions. No claim in this
analysis treats an abstract as proof of a guarantee.

PHASE2-SEARCH-0080–0083 verified selected conditional-e-value and dominated
distributional-neighbourhood anchors. Phase 2A.1 added prospective
foundational searches documented in `audit/phase2a1_search_log.md`.
Administrative final dispositions, including title-level false-positive
states, are not used to infer that a method family is absent or exhausted.
Nonnested likelihood testing remains discovery-level and supports no
definitive guarantee claim. The weaker GAP-01/GAP-03 conclusions instead rest
on the verified positive fixed-sample results listed above.

The resulting boundary is: generic fixed-sample and converse theory is
established; representation and global optimisation for nonlinear EMU
families are computational residuals; biological mechanisms, sharing
assumptions and costs are application inputs; packaging the calculation is a
software-integration issue; and uninspected records remain deferred rather
than being used as negative evidence.
