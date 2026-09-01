# Phase 3B: testing and target decisions under non-identifiability

## Answer to search family B

The inspected evidence establishes three separate facts:

1. isotope forward models can be structurally non-identifiable;
2. a function, prediction or class-relevant property can remain determined
   when the full parameter vector is not; and
3. tests can be constructed generically with nonidentified nuisance
   parameters under stated model assumptions.

Those facts do not by themselves yield a direct MID metabolic-class test.
No inspected source constructs the isotope experiment's observation-law
families and then proves controlled class testing uniformly over
nonidentifiable flux states and pipeline nuisance variation.

## Isotope-specific and systems-model partial formulations

### P3-0006 / P0018 — Isermann & Wiechert (2003)

**Classification: PARTIAL FORMULATION.** The paper constructs an isotope-
labeling-system measurement map and studies structural flux identifiability.
Its full-information rank criterion and non-identifiable examples are
deterministic: flux is the parameter to be recovered, measurements are exact,
and there is no replicated sampling law or class error. Exact locations:
Introduction; “Measurement models for CLEs”; “Structural identifiability
problem”; the non-identifiable example; Theorem 4 in “Identifiability criterion
for full information”; “Partial information analysis”; Conclusions. DOI
`10.1016/S0025-5564(02)00222-5`.

This source establishes a real obstruction to full flux recovery. It does not
show that a declared metabolic class is or is not testable at a given sample
size.

### P3-0001 — Schellenberger et al. (2012)

**Classification: PARTIAL FORMULATION.** Feasible flux points are partitioned
by a high/low reaction-flux or flux-ratio objective and mapped through an
isotopomer model to multiple fragment MDVs. The paper explicitly motivates
questions that can be resolved even if the full flux vector cannot. This is
the closest isotope-specific construction of a class-relevant target surviving
incomplete flux resolution.

The within-class distribution is induced by a uniform Monte Carlo sample of
feasible flux points, and separation is summarized by marginal `Z_i` scores
and their sum. It is not a worst-case composite test, does not include a
replicate law, and does not calibrate Type-I/II errors or sample size. Exact
locations: Background and Figure 1; Results “Monte Carlo Sampling Approach”
and Figure 2; “Generating and Evaluating 13C Experimental Hypotheses,” the
`Z_i` and `Z` equations; “Dimensionality of Isotopomer Data”; Methods “Monte
Carlo Sampling” and isotopomer calculation. DOI
`10.1186/1752-0509-6-9`.

### P3-0015 — Cedersund (2012)

**Classification: PARTIAL FORMULATION.** This systems-biology paper formally
separates parameter identification from identification of a “core prediction”:
a model property shared by all parameter values acceptable under a model and
data cutoff. It proves a set-logical equivalence between such a property and
rejection of its complement and searches the acceptable parameter set in the
direction relevant to the prediction.

This is a substantive target-without-parameter-identification precedent, but
its observations are generic ODE time courses, not MIDs. The selected
cost/rejection cutoff is not a finite-sample two-error guarantee over an
isotope-induced class, and the experimental hierarchy is absent. Exact
locations: Abstract; Introduction; “Basic notations”; “New definitions and
analysis of their basic properties,” Definitions 1–8 and Lemmas 1–2;
“Modified optimization,” Steps 1–3; “Approaches not equivalent to the
identification of core predictions”; Summary. DOI
`10.1111/j.1742-4658.2012.08725.x`.

### P3-0002 and P3-0003 — nonunique fits and model decisions

Zhang et al. (2023) motivate Bayesian priors partly by multiple parameter
vectors that fit tracer time courses, but compare kinetic parameters and
derived fluxes rather than test metabolic classes without identification
(Methods “A Bayesian kinetic model” and “Comparison of kinetic model
parameters between experimental groups”; Discussion; DOI
`10.1186/s12859-023-05211-5`). Sundqvist et al. (2022) use held-out tracer
MIDs to select a reaction-network candidate while fitting fluxes, and
explicitly distinguish model selection from a final model test (Results after
Table 1 and §§2.3–2.5; Discussion; DOI
`10.1371/journal.pcbi.1009999`). Both are `PARTIAL FORMULATION`, not direct
class tests under nonidentifiable flux.

## Generic testing results

### P3-0016 — Todem, Fine & Peng (2010)

**Classification: GENERIC THEORY ONLY.** The paper tests a hypothesis about
identifiable parameters uniformly over a nonidentified sensitivity parameter.
It constructs an infimum/global-sensitivity statistic, simultaneous bands and
a nonparametric-bootstrap implementation for a prespecified missing-data/
longitudinal family. The guarantees are asymptotic; simulations assess small
samples. Exact locations: Abstract; §§2.1–2.3, especially the infimum test and
simultaneous bands; §3 and Table 1. DOI
`10.1111/j.1541-0420.2009.01290.x`; PMCID `PMC3076640`.

### P3-0017 — Andrews & Mikusheva (2016)

**Classification: GENERIC THEORY ONLY.** The paper recasts moment-condition
testing without identification assumptions as conditioning with an
infinite-dimensional nuisance mean function. It gives uniformly correct
asymptotic size for stated model/test classes; exact conditioning belongs to
the Gaussian limit experiment. Exact locations: Abstract p. 1571; §1
pp. 1571–1576; §2 and equations (1)–(2); §3, equation (5) and Lemma 1;
§4.1 and Theorem 1; §7. DOI `10.3982/ECTA12868`.

### Existing Phase 2A.1 anchor P3-0018 / P0053

Goldenshluger, Juditsky & Nemirovski (2015) give constructive, uniform
finite-sample tests for specified convex composite families and independent
heterogeneous products. The exact theorem locations and transfer boundary are
already recorded in
`analyses/fixed_sample_composite_testing_foundations.md`; they are not
re-reviewed here. **Classification: GENERIC THEORY ONLY.** The theorem assumes
a suitable family representation and detector computation; it does not
construct that representation from isotope cultures, fragments, correction
and latent network states. DOI `10.1214/15-EJS1054`.

## Distinctions needed for Phase 3

| Statement | Evidence status | Consequence |
|---|---|---|
| Full flux is structurally identifiable | can fail in isotope models (P3-0006) | failure of flux recovery is not automatically failure of every class decision |
| A functional or output property is identified | possible in generic mechanistic models (P3-0015) | the desired metabolic-class property must be defined and checked over the entire acceptable flux set |
| A test is valid with a nonidentified nuisance | established for prespecified generic models (P3-0016–P3-0018) | validity cannot be imported until the actual MID law and nuisance set meet the source assumptions |
| Empirical profiles discriminate groups without flux fitting | demonstrated in isotope applications (P3-0009, P3-0013–P3-0014) | observed separation is not a uniform class-test guarantee |
| The Phase 3 metabolic classes are testable despite flux non-ID | not determined by the inspected sources | requires induced-family overlap/separation and an experimental sampling law |

“Partial identification” also must not be used as a synonym for all these
cases. A set-valued flux region, a uniquely determined functional, a nuisance
unidentified only under a null, and a completely overlapping observation-law
image lead to different testability questions.

## Family-B conclusion

GAP-08C is **PARTIALLY ADDRESSED**. Positive prior art shows that target-level
decisions may remain meaningful without point identification and that generic
tests can handle specified nonidentification structures. What is unresolved
from the checked evidence is the experiment-specific step: construct the two
network-coupled MID law families, retain every flux state consistent with each
metabolic class, and determine their finite-sample separation after the
biological and technical hierarchy is included.
