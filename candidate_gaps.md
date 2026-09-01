# Candidate-Gap Register — Phase 2A.1

These are falsification hypotheses, not novelty claims or grant
recommendations. Statuses reflect the primary evidence currently verified.

## GAP-01 — Finite-sample EMU mechanism discrimination

- **Precise hypothesis tested:** fixed-sample composite-versus-composite
  testing with uniform two-error control is missing in general, so continuous
  EMU mechanism classes require new testing theory.
- **Nearest prior work:** P0053 gives constructive uniform nonasymptotic tests
  for convex compact composite classes and heterogeneous product
  observations; P0060 gives robust fixed-sample tests for Hellinger-separated
  classes, including independent non-identically distributed products;
  P0065 and P0071 give exact minimax tests for divergence-neighbourhood
  composites; P0072 gives a constructive fixed-sample Hellinger-margin test
  with upper and lower sample-complexity bounds. Direct isotope selection and
  model averaging remain represented by P0030–P0032 and P0047.
- **Strongest evidence against:** constructive composite tests, simultaneous
  finite-sample error bounds, least-favourable-pair tests and heterogeneous
  product constructions already exist. The broad theoretical absence
  proposition is therefore false.
- **Transfers directly:** the set-of-laws formulation, minimax two-error
  risk, exact-overlap obstruction, product-law construction and general
  divergence bounds.
- **Adjacent-method transfer:** **APPLICABLE WITH COMPUTATIONAL
  ADAPTATION**.
- **Exact residual distinction:** compute a useful test and certified risk
  for nonlinear, generally nonconvex EMU-induced law families while
  respecting feasible flux sets and shared nuisance, then optimise the
  tracer/intervention/allocation design.
- **Residual type:** computational. A theoretical subproblem would require a
  narrower registered approximation or tractability theorem, not a new
  generic composite-testing formalism.
- **Boundary classification:**
  - **Generic theory already established:** P0053/P0060 provide constructive
    fixed-sample composite tests, and P0059 provides general finite-sample
    converse machinery.
  - **Verified computational limitation:** the constructive results require
    convex, separated, regular, or otherwise represented law classes; P0049
    verifies a nested local nonlinear design computation rather than a global
    certificate. This does not prove that every EMU instance is intractable.
  - **Biological/application issue:** the mechanism classes, observation
    noise, feasible flux sets, replicate meaning, and experimental costs must
    be declared for a concrete isotope problem.
  - **Software-integration issue:** connecting an EMU simulator to a
    certified detector and design optimiser is implementation work, not
    evidence for a new generic testing theorem.
  - **Unresolved/deferred-evidence boundary:** inaccessible and
    discovery-level records cannot support an absence claim. GAP-01 is
    weakened by positive verified existence results, not by treating the
    remaining ledger as exhaustive.
- **Precise obstruction:** nonlinear EMU images need not satisfy the convex
  representations used by tractable saddle-point tests. Convexification is
  decision-theoretically exact for worst-case testing because error is linear
  in the law, but computing the hull can be difficult and a hull intersection
  may represent least-favourable mixtures rather than one physical metabolic
  parameterisation. A finite grid is not uniform without a certified
  covering error; shared nuisance couples heterogeneous blocks.
- **Missing evidence:** execution on a declared EMU observation model,
  certified approximation error for discretisation/relaxation, and a global
  or auditable least-favourable/design computation.
- **Status:** **WEAKENED**. Phase 2A.1 rejects the broad theoretical claim and
  retains only the narrower computational adaptation. This is not a novelty
  claim.

## GAP-02 — Uniform guarantees over flux and structural uncertainty

- **Hypothesis:** sampled-map isotope robustness has not been extended to
  uniform decision guarantees over continuous flux and structure classes.
- **Nearest prior work:** P0009 sampled-flux robust tracer design; P0024
  continuous maximin KL design; P0029 robust T-design; P0041/P0044
  distributionally robust testing; P0032 structural BMA; P0048
  response-distribution design; P0049 continuous-parameter max-min
  biochemical design; P0050 Bayesian predictive design.
- **Strongest evidence against:** continuous-set maximin biochemical design,
  probabilistic and posterior-predictive design, least-favourable
  distributional testing, and isotope structural averaging are already
  established separately.
- **Transfers directly:** finite-scenario objectives, posterior-predictive
  utilities, and continuous KL/T inner extrema when computable.
- **Residual distinction:** a certified joint maximin design/test over an
  explicitly bounded EMU structural/flux/discrepancy class.
- **Residual type:** computational for a represented uncertainty class. Whether
  a narrower theorem is needed is **UNRESOLVED FROM CURRENT EVIDENCE** until
  the class, error criterion and desired certificate are registered.
- **Boundary classification:**
  - **Generic theory already established:** continuous maximin criteria,
    robust testing over declared ambiguity sets, and Bayesian structural
    averaging are established in P0024, P0029, P0041, P0044 and P0032.
  - **Verified computational limitation:** P0049 verifies a semi-infinite
    nested design solved without a global continuous-class certificate; the
    cited testing papers require explicitly represented uncertainty sets.
  - **Biological/application issue:** a structural/flux/discrepancy class must
    be scientifically bounded before “uniform” has a defined target.
  - **Software-integration issue:** combining robust criterion evaluation,
    EMU simulation and structural testing is an engineering layer unless it
    depends on a separately stated guarantee theorem.
  - **Unresolved/deferred-evidence boundary:** the verified sources establish
    the components, not the exact registered conjunction. Records not
    inspected in full cannot establish either that conjunction or its
    absence.
- **Precise obstruction:** nonlinear nonconvex inner optimisation and
  possibly overlapping ambiguity classes; the verified sources do not
  establish a global solution or finite-sample risk for their conjunction.
- **Missing evidence:** separation and global-optimisation results for a
  registered EMU uncertainty class.
- **Transfer:** **UNRESOLVED FROM CURRENT EVIDENCE**. Generic uniform
  fixed-sample testing and robust-design theory already exist for represented
  classes, so a theory requirement cannot be inferred merely from requesting
  a certificate. The transfer may be computational if the declared EMU class
  satisfies an existing theorem; a narrower extension would need a precise
  assumption or guarantee not covered by that theorem.
- **Status:** **WEAKENED**.

## GAP-03 — Converse-guided isotope design

- **Precise hypothesis tested:** a new fixed-sample converse theory is needed
  to distinguish difficult from impossible decisions between continuous
  EMU mechanism families.
- **Nearest prior work:** P0059 supplies finite-sample `f`-divergence,
  two-point, packing and global metric-entropy lower bounds; P0056 supplies a
  finite-sample Rényi strong converse for multiple testing; P0069 supplies
  fixed-block binary-testing meta-converses; P0072 supplies matching
  Hellinger-margin upper/lower sample-complexity results; P0065 and P0071
  calculate exact ambiguity-set overlap obstructions. P0018 remains the
  direct isotope rank obstruction.
- **Strongest evidence against:** exact-overlap, two-point divergence,
  finite-packing/Fano and metric-entropy converse templates already apply to
  any chosen finite subset of EMU-induced joint laws. Product divergences
  incorporate a fixed heterogeneous replicate allocation.
- **Transfers directly:** exact intersection implies minimax error at least
  one half; two-point and finite-packing lower bounds apply to selected
  induced laws without new probability theory.
- **Adjacent-method transfer:** **APPLICABLE WITH COMPUTATIONAL
  ADAPTATION** for the strongest design-specific bound.
- **Exact residual distinction:** find and globally certify informative
  least-favourable pairs or packings inside continuous nonlinear EMU families
  and optimise the resulting lower bound over mixed experimental designs and
  block costs.
- **Residual type:** computational.
- **Boundary classification:**
  - **Generic theory already established:** exact-overlap, two-point,
    packing, entropy and fixed-block converse forms are verified in
    P0059, P0056, P0069, P0065/P0071 and P0072.
  - **Verified computational limitation:** those results take a pair,
    packing, distance or represented family as input; they do not themselves
    compute the globally strongest witness in a nonlinear EMU image.
  - **Biological/application issue:** a mixture witness in a convex hull must
    not be reported as one physically feasible metabolic state, and the
    error tolerance, cost and mechanism resolution must be declared.
  - **Software-integration issue:** evaluating and reporting a certified
    bound from an EMU forward model is implementation work unless a new
    approximation or tractability statement is proved.
  - **Unresolved/deferred-evidence boundary:** inaccessible foundational
    records remain non-evidence. GAP-03 is weakened by verified converse
    constructions already in hand, not by a claim that every converse family
    has been exhaustively searched.
- **Precise obstruction:** the tight pair/packing and the outer design
  optimum require global optimisation over nonconvex forward images with
  shared constraints. Convex-hull bounds remain valid minimax certificates
  but may be witnessed by mixtures rather than physical parameter points; an
  uncertified grid can miss the true least-favourable configuration.
- **Missing evidence:** a certified numerical least-favourable/packing
  procedure for a realistic EMU model and finite-precision/global-optimality
  analysis.
- **Status:** **WEAKENED**. Identifiability, divergence and sample-complexity
  converse forms are established generally; only EMU-specific certified
  computation remains unresolved.

## GAP-04 — Joint tracer, perturbation, measurement and replication design

- **Hypothesis:** no framework jointly chooses all four variable classes for
  a decision objective.
- **Nearest prior work:** P0036 couples tracer, platform, measurement groups,
  technical repetition and cost; P0037 optimises parallel tracers; P0039 and
  P0048–P0049 optimise biochemical perturbations and measurement times;
  P0050 combines measurement, time and condition choices; P0051 optimises a
  discrimination control; P0007 optimises tracer mixtures.
- **Strongest evidence against:** most component combinations,
  multi-objective optimisation, robust biochemical mechanism design and
  Bayesian measurement/condition design already exist.
- **Transfers directly:** combine finite candidate variables in a common
  utility/cost optimiser.
- **Residual distinction:** biological replicate allocation and perturbation
  selection tied to calibrated mechanism error, not merely flux covariance.
- **Residual type:** computational/integration; theoretical only through
  a separately registered guarantee result, not through the rejected broad
  version of GAP-01.
- **Boundary classification:**
  - **Generic theory already established:** multi-variable optimal design,
    robust biochemical discrimination design and Bayesian
    measurement/condition design are established in P0036–P0039 and
    P0048–P0051.
  - **Verified computational limitation:** the cited applications solve
    selected combinations and criteria; P0049 records nested local
    optimisation rather than a global certificate for the four-way target.
  - **Biological/application issue:** biological versus technical replication,
    perturbation feasibility, batch effects and the scientific mechanism
    decision must be specified.
  - **Software-integration issue:** joining existing tracer, perturbation,
    panel and cost components is principally workflow engineering until a
    calibrated decision objective is supplied.
  - **Unresolved/deferred-evidence boundary:** the current verified direct
    13C-MFA evidence does not establish a prospective biological-replicate
    power calculation for this exact target. That is a deferred evidence
    need, not a universal absence conclusion.
- **Precise obstruction:** mixed discrete/continuous nested optimisation and
  lack of a verified, computationally evaluated EMU mechanism-risk
  objective.
- **Missing evidence:** load-bearing biological power/replicate design in
  direct 13C-MFA.
- **Transfer:** APPLICABLE WITH COMPUTATIONAL ADAPTATION.
- **Status:** **WEAKENED**.

## GAP-05 — Multi-condition non-IID mechanism discrimination

- **Hypothesis:** heterogeneous isotope blocks with partially shared nuisance
  cannot be combined with calibrated mechanism decisions.
- **Nearest prior work:** P0037 parallel-tracer joint precision; P0030
  held-out non-identically distributed tracer validation; P0032 three-ILE
  Bayesian structural inference; P0050 combined condition/measurement
  design; P0043 heterogeneous conditional e-values; P0028 sequential
  composite sensing.
- **Strongest evidence against:** heterogeneity alone is not a theoretical
  gap. P0053 and P0060 give fixed-sample heterogeneous-product
  constructions, exact Type-I control can multiply conditionally valid
  e-values, and held-out non-IID validation, multi-ILE structural posterior
  inference and multi-condition predictive design are implemented.
- **Transfers directly:** additive likelihood/KL information and conditional
  e-value products when blockwise validity is established.
- **Residual distinction:** compute uniform two-error risk and replicate
  sufficiency while enforcing coupled shared and condition-specific nuisance
  in a nonlinear EMU family.
- **Residual type:** computational and application-specific.
- **Boundary classification:**
  - **Generic theory already established:** independent heterogeneous-product
    tests and conditional evidence aggregation are established by
    P0053/P0060 and P0043.
  - **Verified computational limitation:** the verified product constructions
    assume a represented joint family; enforcing partially shared nuisance in
    a nonlinear EMU image leaves a coupled optimisation.
  - **Biological/application issue:** the parameter-sharing graph, condition
    effects, batch structure and biological versus technical replication
    must be justified for the intended experiment.
  - **Software-integration issue:** existing multi-experiment inference can be
    connected to calibrated testing only after the joint likelihood and
    sharing constraints are implemented.
  - **Unresolved/deferred-evidence boundary:** no conclusion is drawn from
    title-level heterogeneous-testing records. What remains unverified is a
    declared EMU application with certified shared-nuisance computation, not
    generic non-IID theory.
- **Precise obstruction:** treating nuisance independently by block enlarges
  the family and can erase separation; enforcing the shared constraint gives
  a coupled nonconvex feasible set.
- **Missing evidence:** certified computation for a declared partially
  shared EMU likelihood, not another generic heterogeneous-product theorem.
- **Transfer:** APPLICABLE WITH COMPUTATIONAL ADAPTATION.
- **Status:** **WEAKENED**.

## GAP-06 — Robustness to forward-model misspecification

- **Hypothesis:** EMU inference/design lacks protection against omitted
  reactions, atom maps and unknown discrepancy.
- **Nearest prior work:** P0030 noise-scale-robust validation; P0034 atom-map
  sensitivity; P0035 omitted-reaction tests; P0045 covariance-aware
  traditional-MFA model-error diagnosis; P0031–P0032 structural BMA; P0048
  distributional parameter-robust design; P0049 max-min continuous-parameter
  design; P0041/P0044 robust testing.
- **Strongest evidence against:** model-error detection, candidate-reaction
  repair, structural averaging, probabilistic/max-min biochemical design and
  distributional minimax testing all exist.
- **Transfers directly:** held-out validation, specified-model averaging,
  sensitivity analysis, parameter-distribution/max-min design and
  ambiguity-set testing.
- **Residual distinction:** uniform design/error control against a declared
  nonlinear EMU discrepancy class outside an enumerated model family.
- **Residual type:** unresolved until a bounded discrepancy class is
  specified. Depending on that class, the residual may be a direct
  application, a computational representation problem or a narrower
  theoretical extension; an unspecified-error target is too broad.
- **Boundary classification:**
  - **Generic theory already established:** ambiguity-set robust tests,
    held-out validation, atom-map sensitivity, omitted-reaction diagnostics
    and specified-model averaging are established in P0041/P0044 and
    P0030–P0035/P0045.
  - **Verified computational limitation:** the verified robust methods require
    a stated uncertainty class, and the EMU applications diagnose or compare
    specified errors rather than optimise a general discrepancy family.
  - **Biological/application issue:** the allowed omissions, mapping errors,
    compartment errors or discrepancy magnitude must be scientifically
    interpretable and distinguishable from flux variation.
  - **Software-integration issue:** combining diagnostics, alternative-model
    generation and robust design is a workflow contribution unless a
    separately stated separation result is needed.
  - **Unresolved/deferred-evidence boundary:** “unknown misspecification” is
    not a defined uncertainty class. The review neither infers protection nor
    infers absence beyond the specified classes verified in primary sources.
- **Precise obstruction:** unknown forward error lacks an identifiable
  uncertainty class. For a specified class, overlapping induced ambiguity
  sets defeat uniform discrimination; separated, represented classes may
  instead admit existing robust tests with computational adaptation.
- **Missing evidence:** a scientifically defensible EMU discrepancy class,
  its relation to the verified ambiguity-set results, and an executable
  separation or robust-objective calculation.
- **Transfer:** **UNRESOLVED FROM CURRENT EVIDENCE**. The currently verified
  sources do not determine whether the eventual declared discrepancy class
  is covered directly, requires only computation, or needs a new theorem.
- **Status:** **WEAKENED**.

## GAP-07 — Decision-oriented open scientific software

- **Hypothesis:** no open platform integrates simulation, inference, design,
  structural decisions, power and certification.
- **Nearest platforms:** S0009 13CFLUX(v3), S0002 INCA, S0004 mfapy, S0010
  OpenMebius2, S0012 BayFlux, S0013 Isodyn, S0014 FluxPyt, S0015 FiatFlux,
  S0016 WUFlux and adjacent S0017 ModelDiscriminationToolkitGUI.
- **Strongest evidence against:** verified platforms already implement open
  EMU simulation, inverse inference, UQ and tracer-design APIs; GUI, Bayesian
  isotope tools and GPL robust biochemical model-discrimination software are
  also verified separately.
- **Exact missing integration:** within the capabilities directly verified
  for S0001–S0017, the evidence does not establish one platform combining
  calibrated structural/mechanism error, biological power/replicate design,
  finite-sample certification and insufficiency reporting. This is a bounded
  corpus statement, not a universal software-absence claim.
- **Does it require new science?** integration alone does not; it inherits
  only the narrower computational or application-specific work remaining
  after GAP-01/GAP-03/GAP-05 falsification.
- **Residual type:** software engineering and usability.
- **Boundary classification:**
  - **Generic theory already established:** component methods for simulation,
    inverse estimation, uncertainty, design, structural inference and robust
    discrimination are established in the cited paper evidence.
  - **Verified computational limitation:** the component methods retain the
    representation and global-optimisation boundaries recorded for
    GAP-01/GAP-03/GAP-05; software integration does not remove them.
  - **Biological/application issue:** a usable workflow still needs
    experiment-specific mechanism definitions, replicate semantics, noise
    models and validation data.
  - **Software-integration issue:** the residual identified here is
    integration, provenance, usability and maintenance; by itself it is not
    a methodological contribution.
  - **Unresolved/deferred-evidence boundary:** undocumented or unexecuted
    capabilities remain `unclear`/`partial`. Their absence is not inferred,
    and further execution-level comparison is deferred.
- **Missing evidence:** execution-level comparison; unresolved versions or
  maintenance for FluxPyt, FiatFlux, WUFlux, Metran and
  ModelDiscriminationToolkitGUI affect product comparison but not the bounded
  capability conclusion.
- **Transfer:** APPLICABLE WITH COMPUTATIONAL ADAPTATION.
- **Status:** **WEAKENED**.

## Phase 3B boundary note

Phase 3B does not revise the positive Phase 2/2A.1 evidence for generic
composite-testing theorems. It narrows what can be inferred from that evidence
for a direct-MID formulation. In particular, the earlier phrase
“computational adaptation” must not be read as proof that a theorem's
representation, convexity, domination, separation or independence assumptions
hold for a culture-to-ion induced family. For GAP-08, constructing the family
and proving applicability are unresolved before any residual can be labelled
purely computational. This is a prospective synthesis clarification, not an
alteration of the Phase 1/2 audit history.

## GAP-08 — Construction, geometry and operational testing of experimentally induced network-coupled MID families

- **Registered question:** has stable-isotope tracing been formulated as a
  hierarchical decision problem whose primary data are replicate-level MIDs
  or raw isotope-resolved measurements; whose fluxes are nuisance or
  downstream; whose target is a metabolic class that may remain testable
  under flux non-identifiability; whose several fragment MIDs share one latent
  state; and whose finite-sample errors or sample requirements distinguish
  biological and technical levels?
- **Closest direct observation/target precedent:** P3-0009 analyses corrected
  multi-fragment GC-MS isotope profiles to discriminate mutants/conditions
  without fitting a network or flux. P3-0010–P3-0014 add direct differential
  analysis, MID-distance networks and isotope-signal classification;
  P3-0022–P3-0023 add raw-to-MID processing and mode-of-action/pathway
  contextualization. They are
  `APPLICATION WITHOUT THEORY`, not calibrated network-class tests.
- **Closest mathematical class/geometry precedent:** P3-0001 maps sampled
  feasible high/low flux or flux-ratio classes into multiple fragment-MDV
  clouds despite incomplete flux resolution. Its separation score is
  heuristic/simulation-based rather than a composite-test guarantee.
- **Closest non-identifiability precedents:** P3-0006/P0018 establishes isotope
  structural flux non-identifiability; P3-0015 formalises a target/core
  prediction that can remain determined across nonunique parameters; and
  P3-0016–P3-0018/P0053 provide generic tests for already specified
  nonidentification/composite structures. These pieces are not combined into
  an induced MID class test.
- **Closest network-coupled precedents:** P3-0003/P0030 and P3-0004 jointly
  fit multiple tracer/fragment MIDs through shared fluxes for network
  validation or flux estimation; P3-0008 constructs the deterministic EMU
  map. Flux remains the estimator or fitting variable rather than only a
  nuisance for a direct class decision.
- **Closest hierarchy/error precedent:** P3-0005 propagates ion counting,
  integration, ionisation/transmission and isotope-correction uncertainty to
  isotope fractions and fluxes; P3-0002 supplies a one-level replicate
  isotope likelihood. Neither separates batch, culture, sibling fraction,
  preparation, injection and measurement variation in a finite-sample class
  guarantee.
- **Geometry prior art:** P3-0020 gives stability/state prerequisites;
  P3-0008 constructs the forward map; P3-0006 gives structural rank/
  injectivity results; P3-0007 gives exact fragment equivalence and
  measurement ordering; and P3-0001 gives sampled images/approximate
  dimension. The current evidence does not characterise the full law image's
  support, boundaries, global convexity, order, separation or least-favourable
  distributions.
- **Subquestion A — complete culture-to-MID probability pipeline:**
  **PARTIALLY ADDRESSED** by P3-0002 and P3-0005 at separate levels; no
  complete pipeline verified.
- **Subquestion B — class testing separated from flux estimation:**
  **PARTIALLY ADDRESSED** empirically by P3-0009–P3-0014 and P3-0022–P3-0023,
  and geometrically by P3-0001; no calibrated induced-class test verified.
- **Subquestion C — testing under flux non-identifiability:**
  **PARTIALLY ADDRESSED** by P3-0001, P3-0006 and P3-0015–P3-0018 as separate
  components.
- **Subquestion D — several MIDs as parallel composite observations with one
  latent state:** **PARTIALLY ADDRESSED** for forward simulation and joint
  fitting by P3-0001, P3-0003–P3-0004 and P3-0008; not for direct class risk.
- **Subquestion E — biological/technical levels in finite-sample guarantees:**
  **UNRESOLVED FROM CURRENT EVIDENCE**. P3-0005 distinguishes analytical
  sources but not the complete hierarchy or class guarantee.
- **Subquestion F — induced-family geometry/order/support/least-favourable
  structure:** **PARTIALLY ADDRESSED** at deterministic-map level by
  P3-0001, P3-0006–P3-0008 and P3-0020; unresolved for full probability-law
  families.
- **Precise obstruction:** the actual joint law cannot yet be instantiated
  from the source manuscripts because primary-unit lineage, preparation/
  injection structure, variance components, exact correction/atom maps, raw
  counts, missingness/censoring and replicate-level MIDs remain unreported.
  Even after declaring synthetic versions, overlap/separation and theorem
  assumptions must be certified over the shared-flux family.
- **Synthetic proof of concept:** possible if every missing hierarchy,
  correction, support and variance rule is declared as an assumption and
  varied in sensitivity analysis. It cannot yield an empirical sample size
  for either source manuscript.
- **Evidence boundary:** no `EXACT FORMULATION` was verified in the bounded
  Phase 3B set. This is not a universal absence, saturation or novelty claim.
- **GAP-08 status:** **PARTIALLY ADDRESSED**.
