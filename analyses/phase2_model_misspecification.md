# Phase 2A — Model Misspecification

## Question

Does existing work already protect EMU-based isotope inference or design
against incorrect observation noise, omitted reactions, structural
alternatives, atom mappings, or discrepancies outside the assumed forward
model?

## Verified evidence

### Uncertain measurement-error magnitude (P0030)

Validation-based selection uses a held-out tracer and, in simulations,
selects the generating candidate structure across a range of believed noise
scales where chi-square, AIC, and BIC choices change (Results §§2.1–2.3,
Figures 4, 6, and 8). This is simulation-based robustness to noise-scale
miscalibration. It is not uniform protection over arbitrary noise laws; the
authors also note that MID normality is questionable and that validation
selection still requires a final adequacy test.

### Atom-mapping error (P0034)

MetAMDB evaluates a deliberate aldolase atom-mapping error in an *E. coli*
13C-MFA model. A single mapping error changes predicted labeling, inflates
the pyruvate-dehydrogenase estimate, broadens confidence intervals, and
increases SSR roughly tenfold (Results, Figure 3 and Supplementary Tables
S4, S7, and S8). This is a concrete sensitivity demonstration and motivates
curated mappings. It neither identifies an unknown wrong mapping from a
general class nor gives a robust-design guarantee.

### Omitted reactions in stoichiometric MFA (P0035)

Gunawan, Hutter, and Feng derive omitted-variable bias for overdetermined
stoichiometric MFA:

`bias = (S_I' S_I)^(-1) S_I' S_O v_O`

(Methods §2.2.1, equations 11–15). They evaluate RESET, F, and
Lagrange-multiplier specification tests and an iterative candidate-reaction
addition procedure (Methods §§2.2.2–2.3; Results §§3.1–3.3, Tables 1–4).
This primary result directly establishes that good regression fit need not
imply small flux bias and that omitted reactions may be detectable when a
candidate set is supplied.

Transfer to EMU-generated nonlinear isotope models requires a nontrivial
extension: the linear projection formula and nested regression tests do not
directly cover nonlinear isotope balances, unknown atom mappings, or
alternatives whose induced distributions overlap.

### GLS validation and simulated model-error diagnosis in traditional MFA (P0045)

Sokolenko, Quattrociocchi, and Aucoin formulate **traditional,
overdetermined stoichiometric MFA** as generalized least squares. The
complete primary text explicitly says that Equation 7's IID error assumption
is unlikely and rescales the balances using an estimated covariance matrix
(`Methods`, “Theoretical principles,” BioC offsets 10,627–12,860). They then
use regression t-tests for calculated-flux significance and contrast these
with the usual chi-square residual check (`Methods`, same subsection, offsets
12,860–14,067).

The model-error diagnosis is empirical and simulation-based. Feasible fluxes
are sampled from a stoichiometric null-space region bounded by observed-flux
intervals, then perturbed with measurement error (`Methods`, “Theoretical
principles,” offsets 14,067–16,008, especially Equation 19). In the CHO case,
the chi-square test gave `p = 0.93`, while only 15 of 47 calculated fluxes
were significant; the authors compared the observed fit with 100 balanced
profiles, each perturbed 100 times (`Results`, “Identification of model
error,” offsets 23,604–25,682; Figure 2). A deliberately modified structure
that added NADH/NADPH balances reduced the number of non-significant fluxes
from 32 to 16 (`Results`, “Effect of model structure,” offsets
30,820–33,701; Figures 4–6).

This paper therefore strengthens the evidence that a conventional
goodness-of-fit result can miss practically important model inadequacy and
that simulation can diagnose it. It does **not** provide:

- an EMU or isotope-label forward model;
- a calibrated choice among mechanism classes;
- a prospective tracer, condition, sample-size, or replicate design;
- a uniform/minimax result over a misspecification class; or
- a finite-sample guarantee or converse.

The authors state that model correction is outside their scope (`Results`,
“Identification of model error,” offsets 25,682–26,937) and conclude only
that their traditional-MFA framework is *likely* to transfer to other
regression or MFA formulations (`Conclusion`, offsets 39,449–40,312).
Accordingly, the transfer to EMU-generated observations remains an
unverified extension rather than a result of this paper.

### Specified structural uncertainty (P0031–P0032)

Bayesian model averaging incorporates bidirectionality uncertainty (P0031)
and prespecified reaction/pathway sets (P0032). This manages uncertainty
inside the enumerated family. It does not protect against omitted mechanisms
outside that family, likelihood discrepancy, or adversarial forward error.

### Probabilistic and max-min biochemical discrimination (P0048–P0049)

Flassig and Sundmacher propagate specified kinetic-parameter distributions
through rival biochemical ODE models and optimise stimulus, observation time
and readout using overlap of the resulting response distributions (P0048,
Sections 2.2–2.5, equations 5 and 8–11). Stegmaier, Skanda and Lebiedz
instead maximise the worst-case KL-derived separation over bounded
continuous parameter regions (P0049, Methods equation 1 and Robust optimal
designs equations 4–5). These are strong evidence that uncertainty-aware
biochemical mechanism design is established.

Both can use an EMU simulator in place of an ODE response map with
computational adaptation. They do not address an erroneous forward
structure outside the candidate models: P0048 assumes specified parameter
laws, while P0049 assumes specified bounded parameter sets. Neither provides
a calibrated finite-sample test or a globally certified solution of the
non-convex continuous design problem.

## Classification

The broad hypothesis that metabolic-model misspecification is untreated is
rejected. The narrower EMU problem is application-specific, while its
computational or theoretical status depends on the discrepancy class:

- detection and sensitivity studies are already direct applications;
- enumeration and averaging over known structural alternatives are
  computational problems with working methods;
- probabilistic or max-min parameter robustness can be transferred from
  P0048–P0049 computationally once a distribution or bounded set is specified;
- uniform decision/design protection against unknown nonlinear forward error
  first requires a precise discrepancy or uncertainty class; the inspected
  papers do not determine whether the declared class would need new theory or
  only representation and computation;
- without such a bounded class, the proposed problem is too broad to support
  a guarantee.

## Transfer classification

**UNRESOLVED FROM CURRENT EVIDENCE** for uniform or minimax mechanism
discrimination under EMU forward-model error. The classification cannot be
made more specific until the discrepancy class is declared and checked
against established robust-testing assumptions.

What transfers directly: held-out validation, posterior averaging over
enumerated structures, sensitivity analysis, candidate-reaction testing
logic, P0045's covariance-aware GLS/simulation diagnostic at the level of a
chosen regression formulation, and the P0048–P0049 probabilistic/max-min
design criteria for a declared parameter uncertainty set.

What does not transfer: the linear omitted-variable formula and regression
tests of P0035, P0045's traditional stoichiometric-GLS construction, or the
within-family Bayesian interpretation of P0031–P0032, to an unenumerated
nonlinear discrepancy class.

Precise obstruction: one must specify a set or probability law for
forward-model discrepancies and characterize separation between the induced
composite observation families. If those sets overlap, uniform
discrimination can be impossible. The inspected P0030–P0035 and
P0045/P0048–P0049 results do not themselves supply an EMU-specific
separation theorem, finite-sample test, or converse, but the bounded review
does not establish that no other applicable result exists. P0045 adds a
direct metabolic model-error diagnostic and P0048–P0049 add
uncertainty-aware design baselines.
