# Method Taxonomy

## Phase 2A extensions

- **Validation-based structural selection (P0030):** fit fluxes on one tracer
  and rank candidate reaction networks on an independent tracer.
- **Bayesian multi-model 13C-MFA (P0031–P0032):** posterior model
  probabilities and model-averaged fluxes over bidirectionality, reaction and
  pathway alternatives. P0047 verifies application of this family to
  biological carbon/nitrogen co-labelling data.
- **Biochemical model-discrimination design (P0048–P0051):**
  response-distribution overlap, continuous-set max-min KL design,
  posterior-predictive measurement design and fixed-parameter perturbation
  design are established adjacent baselines. None supplies calibrated
  finite-sample EMU mechanism error.
- **Conditional safe testing (P0043):** products of conditionally valid
  e-values give exact anytime Type-I control across heterogeneous batches;
  Type-II power and sample sufficiency remain separate.
- **Fixed-sample composite testing and converses (P0053–P0060,
  P0062–P0072):** constructive uniform tests exist for convex, separated,
  nuisance-indexed, robust-neighbourhood and selected nonparametric classes.
  Independent non-identically distributed products are explicitly covered
  by P0053, P0060 and P0068. Finite-sample two-point, packing,
  metric-entropy, Rényi and fixed-block converse tools are represented by
  P0056, P0059, P0063, P0066, P0068–P0069 and P0072. These results eliminate
  a broad absence claim; applying them to exact nonlinear EMU images remains
  a representation and global-computation problem.
- **Misspecification analysis (P0034–P0035, P0045):** empirical atom-map
  sensitivity, linear omitted-reaction specification tests and
  covariance-aware traditional-MFA diagnostics are distinct from uniform
  robust testing.
- **Dynamic parameter-information analysis (P0046):** fixed-time-course
  simulation and local Fisher/covariance comparison estimate kinetic
  parameter information; they do not optimise replicate count or mechanism
  error.
- **Software generation:** 13CFLUX(v3) (S0009) is an open, versioned
  EMU/inference/UQ/tracer-design platform. Isodyn, FluxPyt, FiatFlux and
  WUFlux (S0013–S0016) add kinetic model checking, stationary EMU analysis,
  local flux-ratio analysis and GUI workflows. ModelDiscriminationToolkitGUI
  (S0017) verifies adjacent max-min biochemical model-discrimination and
  measurement-time design software; it is not an isotope platform and
  integration is not a statistical guarantee.

This is an evidence-linked structure, not a statement that every category is
populated or that any gap exists. Add claims only with paper/software record
IDs and retain contrary evidence.

## Forward simulation

### Definitions and scope

### Established methods

Full isotopomer and EMU decomposition are distinct computational
representations of isotope propagation. EMU decomposition reduces forward
simulation burden; it does not itself change the inferential decision
(P0001-P0002). Dynamic EMU systems extend forward simulation to transient
labelling (P0013-P0014). Verified implementations include 13CFLUX2, INCA,
mfapy, FreeFlux, 13CFLUX(v3), BayFlux, FluxPyt and WUFlux (S0001–S0002,
S0004–S0005, S0009, S0012, S0014, S0016). `unclear` software fields are not
treated as implemented capabilities.

### Limitations and open questions

## Direct MID and isotope-resolved decision methods (Phase 3B)

### Definitions and scope

This category starts from replicate-level MIDs or raw isotope-resolved
measurements. It is distinct from MFA estimation even when both use the same
mass-spectral coordinates.

- **Direct marginal comparison:** test isotopologues/metabolites separately
  across conditions.
- **Flux-free multivariate discrimination:** concatenate isotope features for
  PCA, ICA, clustering or classification.
- **Network-coupled direct class testing:** define a joint class-specific law
  for several fragments under one latent metabolic state and experimental
  lineage, with flux treated as nuisance or downstream.

Only the third object is the complete GAP-08 target. Ordinary multiple testing
and generic multivariate classification do not become network-coupled merely
because the features come from a metabolic pathway.

### Established methods

P3-0009 directly discriminates mutants/conditions from corrected GC-MS
fragment mass distributions without a network or full flux fit. P3-0010
(DIMet) and P3-0011 (X13CMS) provide sample-table differential analysis of
isotope-resolved data; P3-0012 constructs MID-similarity networks; P3-0013
classifies cell phenotypes from isotope-resolved NMR signals; and P3-0014
groups isotope profiles by an evolutionary objective. P3-0022 (MIAMI) carries
raw GC-MS data through MID-threshold calls to mode-of-action/reference-network
contextualization, while P3-0023 (IMPACT) adds an LC-MS preprocessing-to-MID
pipeline and similarity/reference networks. These are classified
`APPLICATION WITHOUT THEORY` because none supplies the relevant
network-induced probability family or finite-sample class guarantee.

P3-0001 is a `PARTIAL FORMULATION`: it maps high/low feasible-flux classes to
multiple fragment-MDV clouds and scores their separation. P3-0002 supplies a
replicate-level kinetic isotope likelihood. Neither contains the complete
hierarchical direct-class decision.

### Limitations and open questions

The direct-analysis applications do not establish flux-state-uniform class
error, primary-unit sample requirements, or the culture/preparation/injection
dependence structure. Cross-validated classification accuracy and ordinary
p-values or user-defined MID thresholds are empirical/application results,
not guarantees over induced metabolic-class families.

## Identification-robust target decisions (Phase 3B)

### Definitions and scope

Parameter non-identifiability, functional or class identifiability, and
hypothesis testing with a nuisance unidentified under a null are different
structures. Phase 3 requires a class decision that is well defined over every
flux state consistent with that class; it does not require selecting one flux
representative.

### Established methods

P3-0006/P0018 gives deterministic structural-flux identifiability conditions
for isotope-labeling systems. P3-0015 formalises core predictions shared by an
acceptable nonunique parameter set in a generic systems-biology model.
P3-0016 and P3-0017 give generic non-identification-robust tests under stated
models, and P3-0018/P0053 supplies finite-sample composite tests when the
probability families already have the required representation. P3-0001 is the
closest isotope-specific class analogue.

### Limitations and open questions

No retained source combines those results into a test over experiment-induced
MID law families. The first unresolved question is law-family construction and
overlap/separation, not selection of a generic theorem by name.

## Network-coupled parallel MID evidence (Phase 3B)

### Definitions and scope

Fragments, MIDs, isotopologues and ions are coordinates below the biological
sampling unit. A coupled parallel model preserves one shared flux/metabolic
state across those coordinates; an uncoupled marginal analysis implicitly
allows incompatible latent states and answers a different question.

### Established methods

P3-0004 jointly fits 14 parallel tracer datasets to a shared flux map;
P3-0003/P0030 shares fluxes across estimation and validation tracer data;
P3-0008 constructs the common EMU forward dependence; and P3-0001 generates
multiple fragment MDVs from one sampled flux state. These are positive prior
art for network coupling in simulation, estimation and validation.

### Limitations and open questions

The inspected methods do not use the coupled object as a direct
metabolic-class composite test with finite-sample errors. Direct MID tools
instead use marginal tests, concatenated features or similarity networks.

## Hierarchical isotope measurement models (Phase 3B)

### Definitions and scope

The relevant lineage is batch → culture → collected fraction → preparation →
injection → fragment/MID → isotope-resolved ion. Sibling fractions and all
measurement coordinates remain linked to their culture; none are additional
biological replicates.

### Established methods

P3-0005 propagates ion-count, integration, ionisation/transmission and
isotope-correction uncertainty to isotope fractions and downstream fluxes.
P3-0002 uses a single-level replicate likelihood for isotope time courses.
P3-0010–P3-0011 retain sample rows for ordinary differential analysis. The
adjacent qSIP paper P3-0019 studies measurement error and power for DNA
density-gradient isotope incorporation but is nontransferable to metabolite
MIDs.

### Limitations and open questions

The complete biological/technical variance hierarchy and primary sampling
unit remain unreported for the Phase 3 manuscripts. No retained isotope paper
places that hierarchy inside a finite-sample metabolic-class guarantee.

## Geometry of induced MID families (Phase 3B)

### Definitions and scope

Feasible flux-set geometry, deterministic forward-image geometry, corrected
MID support and full probability-law geometry are separate objects.

### Established methods

P3-0020 establishes stability/state prerequisites; P3-0008 constructs an EMU
forward map; P3-0006 provides structural injectivity/rank analysis; P3-0007
proves exact fragment-equivalence and measurement-order results; P3-0001
samples flux-to-MDV class images and approximates dimension; and P3-0015
studies target images of broad acceptable parameter sets in a generic ODE
model.

### Limitations and open questions

The checked evidence does not characterize support, boundaries, global
convexity, ordering, separation or least-favourable distributions of the full
culture-induced MID law families. A nonlinear/nonconvex optimisation reported
for flux fitting is not proof of nonconvexity of those statistical families.

## Flux estimation

### Definitions and scope

### Established methods

PROVISIONAL: nonlinear least-squares flux estimation with goodness-of-fit and
confidence analysis is represented by abstract-level P0001 and P0003.
ABSTRACT-LEVEL ONLY: shared-flux fitting of parallel experiments is reported
by P0008 and P0015. Phase 2 full-text evidence verifies parallel-tracer
precision analysis (P0037), Bayesian structural/flux inference across
specified model families (P0031–P0032), its application to biological
co-labelling data (P0047), and local dynamic
parameter-information analysis (P0046). P0010 remains abstract-level.

### Limitations and open questions

## Identifiability and observability

### Definitions and scope

### Established methods

EMU-basis rank limits (P0005) and structural flux-identifiability criteria
(P0018, Theorem 4) are verified and operate at different levels.
ABSTRACT-LEVEL ONLY: the topology-specific conclusion in P0019 remains
unverified beyond its abstract.

### Limitations and open questions

## Uncertainty quantification

### Definitions and scope

### Established methods

Profile/nonlinear confidence regions and Bayesian posterior uncertainty are
both represented (P0003, P0010–P0011, P0031–P0032). P0036–P0037 use
covariance/profile-CI quantities for experimental ranking. These do not,
without a separate theorem, imply controlled error for selecting a mechanism.

### Limitations and open questions

## Tracer design

### Definitions and scope

### Established methods

ABSTRACT-LEVEL ONLY: P0004 reports covariance-based input and measurement
design but its full method was not obtained. EMU basis-vector sensitivity
(P0005–P0006), mixture optimisation (P0007), sampled-flux robustification
(P0009), Pareto input/measurement/cost design (P0036), and parallel-tracer
precision scoring (P0037) are full-text checked. P0046 compares a fixed
dynamic design but does not optimise its sampling schedule.

### Limitations and open questions

## Measurement design

### Definitions and scope

### Established methods

P0036 directly optimises analytical platform and measurement groups together
with tracer and cost using local covariance information. ABSTRACT-LEVEL
ONLY: P0004 reports an earlier measurement-panel method and P0016 reports a
pool-size/misspecification trade-off.

### Limitations and open questions

## Perturbation design

### Definitions and scope

### Established methods

P0039 directly optimises initial conditions, time-dependent inputs and
interventions to separate rival biochemical-network outputs. Its objective
is deterministic output separation, not calibrated decision error.
ABSTRACT-LEVEL ONLY: P0019 reports topology-dependent identifiability under
deletions; its proof and scope remain unverified.

### Limitations and open questions

## Model validation

### Definitions and scope

### Established methods

P0030 verifies held-out-tracer validation and model ranking. P0034–P0035 and
P0045 verify atom-map sensitivity, omitted-reaction specification tests and
covariance-aware traditional-MFA diagnostics. ABSTRACT-LEVEL ONLY: P0001 and
P0015 report other goodness-of-fit and cross-experiment checks.

### Limitations and open questions

## Model selection

### Definitions and scope

### Established methods

P0030 selects among finite reaction-network candidates using held-out tracer
data. P0031–P0032 estimate posterior structural probabilities and average
fluxes over specified bidirectionality/reaction/pathway families; P0047
applies Bayesian model averaging to biological co-labelling data. P0038 and
P0040 verify T-, KL- and Bayesian T-design criteria in adjacent regression
models; P0024 verifies continuous maximin KL design. P0050 uses
posterior-predictive Jensen-Shannon separation to rank biochemical
measurement/time/condition combinations. These criteria are not
finite-sample mechanism-error certificates.

### Limitations and open questions

## Mechanism discrimination

### Definitions and scope

### Established methods

P0039 verifies perturbation/input design for rival biochemical-network
mechanisms. P0048 propagates parameter distributions into rival response
laws; P0049 implements a continuous-parameter max-min KL design; P0050
optimises posterior-predictive model separation; P0051 separates
fixed-parameter mechanisms by perturbation control. Verified adjacent work
also includes T/KL/Bayesian discrimination criteria (P0024, P0029, P0038,
P0040), controlled sensing and active composite testing (P0026–P0028),
exact heterogeneous-batch Type-I control (P0043), and distributionally
robust tests (P0041, P0044). Phase 2A.1 adds fixed-sample composite tests with
uniform two-error bounds (P0053, P0060, P0065, P0071–P0072), exact
nuisance-null Type-I constructions (P0062, P0064, P0070), and constructive
nonparametric minimax tests (P0063, P0066–P0068). P0025 remains UNVERIFIED.
The generic testing theory is established; a calibrated EMU implementation
still requires certified representation and optimisation of the induced law
families.

### Limitations and open questions

## Sample-size design

### Definitions and scope

### Established methods

No fully inspected isotope paper made biological replicate number an
optimised output. P0036 prices technical repetition inside a local
measurement-error/cost model, which is not biological power design.
P0026–P0028 and P0042 make stopping/sample count part of narrower verified
sequential decision problems. P0057 and P0072 give explicit fixed-sample
sufficiency/lower comparisons in adjacent composite models, while P0059,
P0063, P0066, P0068 and P0069 provide nonasymptotic lower-bound machinery.
These are not prospective biological-replicate designs for EMU mechanisms.
P0025 is UNVERIFIED.

### Limitations and open questions

## Adaptive design

### Definitions and scope

### Established methods

Adaptive/sequential experiment choice and lower-bound or error-exponent
results are verified in P0026-P0028 at the exact locations recorded in the
corpus. P0025 is UNVERIFIED. Transfer to EMU models requires the qualifications
in `analyses/adjacent_method_transfer.md`.

### Limitations and open questions

## Software and reproducibility

### Definitions and scope

### Established capabilities

Seventeen retained platforms cover forward simulation, inverse estimation,
stationary and transient analysis, UQ, tracer ranking/design, GUIs and
scripted workflows unevenly (S0001–S0017). Isodyn (S0013) verifies
chi-square acceptance/rejection among supplied kinetic schemes, but not
calibrated composite mechanism discrimination. ModelDiscriminationToolkitGUI
(S0017) verifies adjacent robust kinetic-model discrimination and
measurement-time design; its inspected evidence does not establish an EMU
capability. Within the currently curated S0001–S0017 evidence, no platform
is verified as documenting biological replicate/power optimisation, a
finite-sample mechanism-decision certificate, or impossibility reporting.
This is a bounded capability statement, not a universal software-absence
claim.

### Limitations and open questions
