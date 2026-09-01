# Phase 3B: network-coupled parallel observations

## Answer to search family C

Joint use of multiple tracer experiments, fragments and MIDs through a shared
network/flux model is established in the inspected `13C`-MFA literature.
Those papers use the coupling for flux estimation, precision, tracer design
or network-model validation. Ordinary differential tests and pathway displays
also combine many isotope variables, but do not enforce a common latent
metabolic state. No checked source formulates the fragment MIDs as parallel
composite observations for a direct metabolic-class test with controlled
finite-sample error.

## Shared-state coupling that is established

### P3-0004 — Crown et al. (2015)

**Classification: PARTIAL FORMULATION.**

- **Primary observation:** GC-MS mass isotopomer distributions from 14
  parallel tracer experiments. The eight new experiments yielded 14
  amino-acid fragments per experiment and 1,246 mass-isotopomer-abundance
  measurements; after combination with six earlier experiments, the
  integrated fit used 811 nonzero mass-isotopomer measurements plus two
  external constraints.
- **Target:** one central-carbon flux map with experiment-specific dilution
  parameters and improved flux precision.
- **Latent flux:** flux is the estimation target, not nuisance for a direct
  metabolic-class decision.
- **Coupling:** all 14 tracer datasets are concurrently fit to a single flux
  model; experiment-specific `G` parameters remain separate. This is genuine
  common-latent coupling, not ordinary multiple testing.
- **Sampling:** tracer cultures/experiments are the experimental blocks
  described by the source. The paper does not supply a culture/batch/
  preparation/injection random-effects hierarchy, and fragments and
  isotopologues are not biological replicates.
- **Guarantee:** SSR/chi-square goodness of fit and flux confidence analysis,
  not a finite-sample metabolic-class error or sample requirement.

Exact locations: Methods §§2.3 “Analytical methods,” 2.4 “Gas chromatography
mass spectrometry,” 2.5 “Metabolic network model and flux analysis,” and 2.6
“Goodness-of-fit analysis”; Results §§3.1–3.2, including the integrated
analysis of 14 labeling experiments, measurement/parameter counts,
goodness-of-fit and flux-confidence results. DOI
`10.1016/j.ymben.2015.01.001`; PMCID `PMC5845449`.

### P3-0003 / P0030 — Sundqvist et al. (2022)

**Classification: PARTIAL FORMULATION.** Candidate reaction networks share
flux parameters across tracer datasets. One tracer can be reserved for
validation, and validation SSR ranks models after flux fitting. The paper
states that choosing the lowest validation error does not show that the chosen
model is acceptable and calls for a final model test. Thus it supplies a
network-coupled estimation/validation architecture, not the direct class test
asked here.

Exact locations: Introduction, MID observations and replicate-derived error
discussion; Results after Table 1; §§2.3–2.5 and Figures 4, 6 and 8; Methods
§§4.1 and 4.5; Discussion on model selection versus model testing. DOI
`10.1371/journal.pcbi.1009999`; PMCID `PMC9022838`.

### P3-0001 — Schellenberger et al. (2012)

**Classification: PARTIAL FORMULATION.** A common sampled flux state is
forward-mapped to all selected fragment MDVs, so the simulated evidence is
network-coupled. The final score adds marginal `Z_i` values and does not use
the induced cross-fragment covariance or a joint likelihood. It therefore
shows coupled signal generation but not a parallel composite test.

Exact locations: Results “Monte Carlo Sampling Approach,” Figure 2;
“Generating and Evaluating 13C Experimental Hypotheses,” equations defining
`Z_i` and `Z`; “Dimensionality of Isotopomer Data”; Methods. DOI
`10.1186/1752-0509-6-9`; PMCID `PMC3323462`.

### P3-0008 — Antoniewicz et al. (2007), EMU

**Classification: PARTIAL FORMULATION.** The EMU construction identifies the
minimal network states required to calculate the measured fragment MIDs and
preserves their common atom-map/flux dependence. This establishes the
deterministic network-coupled forward map. It does not place a sampling law on
replicate cultures or ions and does not define class risks.

Exact locations: Methods §§2.1–2.6, including EMU decomposition and the
algorithms relating measured fragments to required EMUs; computation and
equivalence comparisons. DOI `10.1016/j.ymben.2006.09.001`; PMCID
`PMC1994654`.

### P3-0021 — Suthers et al. (2007)

**Classification: PARTIAL FORMULATION.** Multiple MDVs and extracellular rates
enter one nonlinear isotope mapping and flux-range calculation. Unresolved
flux ranges acknowledge partial resolution, but the target remains flux
elucidation. Repeated injections described by the source are analytical depth,
not biological units. Exact locations: §2.2, large-scale isotopomer mapping;
§2.5, `FluxCalc` and `FluxRange`. DOI
`10.1016/j.ymben.2007.05.005`.

## Multivariate use without shared-state coupling

P3-0009 concatenates many corrected fragment profiles for PCA/ICA;
P3-0013 uses several NMR isotope signals in one classifier; P3-0010 applies
ordinary tests and PCA to labeling tables; and P3-0012, P3-0022 and P3-0023
construct MID-similarity/reference networks. These are multivariate or
multi-feature analyses, but the dependence is learned/described from the
observed feature table rather than induced by one constrained latent network
state.

## Ordinary multiple testing is a different object

Suppose fragment `f` has an MID `Y_f`. Three procedures must be kept separate:

1. **Marginal screening:** test one null for each isotopologue or metabolite
   and adjust the resulting p-values. DIMet and X13CMS are examples.
2. **Generic multivariate classification:** concatenate the `Y_f` values and
   fit PCA, ICA, SVM or a clustering objective. Zamboni, Frahm and Bleuler are
   examples.
3. **Network-coupled parallel composite testing:** define one class-specific
   set of joint laws
   `P_c = {Law(Y_1,...,Y_F | v, eta): v in V_c, eta in E}`, preserving the
   fact that the same latent state and experimental lineage constrain every
   fragment. This is the Phase 3 target.

Neither (1) nor (2) is equivalent to (3). Treating each MID independently
enlarges the feasible family by allowing a different latent state for each
fragment; treating isotopologues or ions as repeated observations creates
pseudoreplication. Conversely, a jointly fitted MFA model contains coupling
but still answers a flux-estimation or model-fit question unless a class
decision and its errors are separately defined.

## What remains unknown for the source manuscripts

The Phase 3A event maps establish sibling fractions and fragments, but the
source manuscripts do not report the replicate-level joint MID arrays, the
preparation/injection lineage, raw ion counts, or the covariance structure.
Consequently the empirical dependence between sibling fractions and the
conditional dependence among fragments cannot yet be estimated. The model
must keep those relations symbolic rather than assert independence.

## Family-C conclusion

GAP-08D is **PARTIALLY ADDRESSED**. Network-coupled multiple-MID forward
simulation and joint fitting are established. The unresolved conjunction is
a direct class target, a joint observation law at the primary sampling unit,
and controlled risk while the common flux is nuisance rather than the object
reported as the result.
