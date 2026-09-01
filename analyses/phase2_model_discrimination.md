# Phase 2A — Metabolic Model Validation and Discrimination

## Scope and evidence rule

This workstream prospectively tested whether isotope-data methods already
perform structural or mechanism decisions, rather than merely estimating
fluxes or rejecting an inadequate fit. Definitive statements below use
inspected primary full text. Phase 1 records retain their original evidence
depth.

## Direct isotope-method evidence

### Validation on a held-out tracer (P0030)

Sundqvist et al. formulate a finite candidate sequence of metabolic network
models. Fluxes are fitted on an estimation dataset, while the structure with
the smallest weighted residual sum on an independent validation dataset is
selected. In the 13C-MFA examples, the held-out data come from a distinct
tracer (Results §2, Table 1, and the passage immediately after Table 1;
Methods §§4.1 and 4.5). The evaluated simulation and HMEC candidates differ
through reaction/pathway inclusion. An evaluated compartment-structure
alternative was not located and should not be coded from the paper's general
discussion alone.

The paper explicitly warns that selecting the lowest validation statistic
does not guarantee that the selected model is adequate; a final model test
remains necessary (Discussion, “Model selection versus model testing”). In
the seven-model simulation, validation identified the data-generating model
only about 60–70% of the time. Figures 4, 6 and 8 and Results §§2.3–2.5
therefore demonstrate empirical selection frequencies, including sensitivity
to tested rescalings of the assumed measurement error, not a finite-sample
error theorem. The authors also explain that normalized MID components are
not independent even though the working error model treats them that way,
and that validation blocks generated using different tracers need not be
identically distributed (Discussion, measurement-error and cross-validation
passages).

This is direct structural model selection among reaction-network
alternatives and defeats any broad claim that 13C-MFA only assesses goodness
of fit. It does not supply prescribed type-I/type-II error, minimax risk,
sample-size certification, or impossibility. Its primary ranking criterion is
the weighted validation residual sum, not likelihood optimality; likelihood,
chi-square, AIC and BIC appear as fitting or comparator machinery.

### Bayesian structural inference for reaction bidirectionality (P0031)

Theorell and Nöh treat model identity as random across alternative
bidirectionality configurations and use a 13C-MFA-tailored reversible-jump
MCMC algorithm to sample the joint model/flux posterior (Approach §2.2,
equations 2–6; Algorithms 1–2; Results §§4.1–4.2). Each structural variant
sets an exchange-flux component to zero or permits it to be positive while
retaining common net-flux coordinates. The method returns posterior
bidirectionality and model probabilities. Figure 1 and Results §4.2 call
intermediate probabilities “undecided”; this is posterior ambiguity in a
simulated example, not a proved impossibility.

This is genuine structural inference, not merely goodness-of-fit rejection.
Its evidence is Bayesian and simulation-based. Posterior probabilities are
not frequentist finite-sample decision-error guarantees, and the investigated
structure varies reaction bidirectionality within a fixed reaction topology.

### Bayesian model-set averaging over pathways and reactions (P0032)

Jadebeck et al. extend the preceding framework to reaction-set, pathway and
bidirectionality uncertainty. Bayesian model-set averaging partitions an
enormous discrete model family, combines reversible-jump MCMC with
trans-dimensional diffusive nested sampling, and reports posterior model and
model-set probabilities plus model-averaged flux posteriors (Problem
statement §§2.2–2.4, equations 2–5; Algorithm 1; Appendix B, especially
§§B.2–B.4). Synthetic Triangulus and *E. coli* studies include single- and
three-ILE analyses, with 46,976,204,800 candidate structures in the larger
example (Results §§4.1–4.2, especially §4.2.2).

This 2026 preprint materially weakens claims that structural uncertainty,
model averaging, or multi-tracer structural inference are absent from
13C-MFA. Section 2.4 assumes that the enumerated candidate space is
sufficiently comprehensive, and the Conclusion stresses relative support,
rather than a guarantee that one candidate is correct. The authors also
report substantial computational cost. The paper does not derive calibrated
frequentist decision errors, finite-sample sufficiency, a worst-case guarantee
over continuous misspecification, or a converse for overlapping EMU
observation families.

### Bayesian multi-model inference on biological co-labeling data (P0047)

Borah Slater et al. (2023; P0047) apply the P0031
Bayesian multi-model method to biological steady-state ^13C/^15N co-labeling
data from *Mycobacterium bovis* BCG. Every combination of uni- and
bidirectional reactions is a structural variant, and Bayesian model averaging
weights the variant-specific flux posterior by its posterior model
probability (Results, “Roadmap for Bayesian multi-model 13C15N-metabolic flux
analysis,” equation 1 and Figure 2; Materials and Methods, “Flux inference
with Bayesian Model Averaging”). The paper reports model-averaged flux
credible intervals and posterior probabilities that particular reactions
operate uni- or bidirectionally (Results, Figures 3–6 and Appendix Figure S7).

This is gap-destroying evidence because structural Bayesian inference is not
confined to P0031's simulated benchmark. It remains an application of a
specified bidirectionality model family to one co-labeling condition. The
authors' Discussion limits the carbon/nitrogen network scope, and neither
equation 1 nor the application supplies frequentist selection error, power,
replicate allocation, a minimax guarantee, or a converse.

### Parallel experiments as model checks (P0033)

Leighty and Antoniewicz compare an initial and extended *E. coli* network
across six parallel [U-13C]glucose mixtures. The primary abstract reports
that the initial network failed acceptable fits and gave inconsistent fluxes,
whereas a network including extracellular CO2 dilution fitted acceptably and
gave consistent fluxes. Complete primary text was unavailable, so this is
supporting evidence only and supplies no guarantee-level conclusion.

## Adjacent biochemical-network designs that transfer

The targeted citation audit found several primary methods closer to the
proposed decision problem than a generic T- or KL-optimality analogy. None is
an EMU paper, but all formulate model discrimination for nonlinear
biochemical systems.

### Response-distribution overlap under parameter uncertainty (P0048)

Flassig and Sundmacher (2012; P0048) propagate
parameter distributions through competing biochemical ODE models and
minimize the time-averaged overlap of the induced response distributions.
Equations 5 and 8–11 and Methods §§2.2–2.5 define the response PDFs,
probability-product-kernel overlap, measurement-time/readout/stimulus design
variables and optimal-control problem. Sigma points approximate nonlinear
propagation; the two examples are evaluated by Monte Carlo (Methods §3,
Table 1 and Figures 2–3).

This transfers to a probabilistic EMU output map with computational
adaptation: replace the ODE response simulator with the EMU observation
simulator and propagate model-specific flux/nuisance distributions. What
does not transfer is a calibrated selection rule or uniform guarantee. The
paper assumes specified parameter PDFs, approximates their induced response
laws by moments, returns local solutions to non-convex programs, and
explicitly says global optimality is not ensured (§2.5). It is neither a
worst-case design over an entire uncertainty class nor finite-sample error
control.

### Worst-case biochemical model-discrimination design (P0049)

Stegmaier, Skanda and Lebiedz (2013; P0049) formulate a semi-infinite
max–min problem over
experimental designs and feasible kinetic-parameter regions. Equation 1
gives a KL-derived response-separation objective; equation 4 chooses initial
concentrations, perturbations and measurement times to maximize the
worst-case separation; equation 5 defines the outer-approximation stopping
gap (Methods, “Robust optimal designs”). Simulated examples re-estimate both
models after the proposed experiment and use lack-of-fit/F-test checks; the
Conclusion expressly says that the examples do not provide a general design
recipe.

The max–min formulation is directly relevant to flux-map uncertainty and
transfers to a bounded EMU nuisance space with computational adaptation. The
precise obstruction is numerical: nested non-convex EMU fits and worst-case
searches can return local parameter/design solutions, so the computed
minimum is not automatically a certified infimum over a continuous class. A
positive worst-case value of this KL-derived criterion is also not a
finite-sample Type-I/Type-II guarantee.

### Bayesian posterior-predictive measurement design (P0050)

Vanlier et al. (2014; P0050) draw from model-specific
parameter posteriors, simulate posterior predictive distributions, and rank
choices of observable, measurement time, condition and small combinations of
measurements by Jensen–Shannon divergence (Methods, “Predictive
Distributions,” “Model selection,” and “Experimental design”; Figures 6–9).
The divergence is empirically compared with expected Bayes-factor changes.
The method therefore optimizes a genuine model-selection utility under
non-Gaussian parameter uncertainty rather than flux precision.

An EMU implementation can directly define the same posterior-predictive
utility, but computing it requires model-specific posterior sampling and
high-dimensional density/divergence estimation. The authors identify MCMC,
density estimation and exponential growth of experiment combinations as
limitations (Conclusion). The method ranks experiments and can identify
little predictive separation; it does not certify frequentist sufficiency or
impossibility.

### Fixed-parameter optimal-control separation (P0051)

Liu, Maini and Baker (2026; P0051) explicitly
separate parameter-identifiability design from model-discrimination design.
For two known-parameter ODE alternatives, Section 3 and equations 18–19
maximize integrated squared output separation minus a control penalty, using
Pontryagin's maximum principle. Introduction §§1.2–1.3 state that only the
external stimulus/control is optimized while sample timing and other design
features are fixed. The model-discrimination calculation assumes noiseless,
continuous-time observation for simplicity even though the paper discusses
noisy discrete data.

This establishes that perturbation design for mechanism separation is an
existing biological-modeling method. A fixed-parameter EMU analogue is a
computational adaptation. Continuous composite mechanism classes, unknown
shared nuisance parameters and an unknown perturbation-to-flux map are not
resolved by the paper; the Discussion identifies fixed ground-truth
parameter sets and known control action as limitations and proposes robust
extensions.

## Decision taxonomy

| Task | Established primary example | What is decided | Evidential limit |
|---|---|---|---|
| Reject an inadequate fitted model | P0030; P0033 supporting only | network adequacy | does not select a unique mechanism |
| Select from finite structures | P0030 | reaction-network candidate | held-out SSR ranking, simulation evaluated |
| Estimate model probabilities | P0031–P0032 | bidirectionality, reaction/pathway sets | Bayesian posterior under specified model family |
| Apply structural Bayesian inference to biological isotope data | P0047 | bidirectionality and flux | one specified model family and condition |
| Average fluxes across structures | P0031–P0032; P0047 | model-averaged flux posterior | prior/likelihood and computation dependent |
| Design a robust biochemical perturbation | P0048–P0049 | kinetic mechanism/model structure | response-separation criteria; no calibrated finite-sample error is established in these inspected papers |
| Design measurements using Bayesian predictive separation | P0050 | biochemical model | ranks measurement/time/condition combinations |
| Design a control for fixed mechanisms | P0051 | ODE mechanism | known parameters and noiseless continuous-output objective |
| Composite mechanism discrimination with controlled errors | adjacent decision theory only | hypothesis class | the current curated evidence does not verify an EMU-specific finite-sample result |
| Prove discrimination impossible | Phase 1 P0018 | structural flux identifiability | rank obstruction, not an error/sample-complexity converse |

## Falsification consequences for the registered gaps

- GAP-01's broad premise is strongly falsified: P0030–P0032 establish
  selection and posterior structural inference, P0047 applies
  multi-model inference to biological isotope data, and P0050
  design biochemical measurements for model selection. A narrower question
  about finite-sample calibrated decision error for EMU-induced composite
  mechanism classes is not answered by these papers.
- GAP-03 is narrowed to resource/error converses. Posterior ambiguity in
  P0031–P0032 is evidence of limited information in examples, not an
  impossibility theorem.
- GAP-04's broad perturbation/mechanism-design premise is contradicted by
  P0048–P0051.
  The remaining EMU issue, if retained, must be framed as transfer and
  computation or as a stricter calibrated decision requirement.
- GAP-05 is weakened by the multi-ILE Bayesian structural analysis in P0032
  and by P0050's simultaneous measurement/condition combinations.
  The remaining issue is calibrated decisions for heterogeneous blocks with
  partially shared nuisance parameters.
- GAP-06 is weakened because P0030 varies assumed measurement-error
  magnitudes, P0032 averages specified structural alternatives, P0048
  propagates parameter distributions, and P0049 solves a max–min
  parameter-robust design. None covers arbitrary unknown alternatives
  outside the enumerated structural family or supplies a certified global
  solution for nonlinear EMU classes.

## Remaining evidence limits

P0033 remains abstract-only. P0032 is a preprint dated 24 May 2026 and must
not be described as peer reviewed. The citation-network pass around P0030 and
P0031 added the fully inspected P0047 application but no new
direct EMU-specific calibrated-testing family. The adjacent audit found
substantial prior art for robust, Bayesian and perturbation-oriented
biochemical model-discrimination design; these methods must be treated as
transfer baselines, not as evidence of an absent field. No inspected direct
paper in this workstream gives exact finite-sample mechanism-error control, a
sample-size converse, or uniform robustness outside a prespecified
structural family.
