# Phase 2A Workstream A — 13C-MFA Experimental Design

## Scope and evidence boundary

This standalone workstream report assesses what direct 13C-MFA
experimental-design methods optimise. Retained evidence is integrated in the
shared corpus and gap register during cross-workstream synthesis. The
prospective search ledger is `audit/phase2_screening_A.csv`; exact
queries and bounded-result limitations are in
`audit/phase2_search_log_A.md`.

An audit of the restored ledgers corrected false-negative mechanical
screening for direct design titles (including IsoDesign, COMPLETE-MFA,
measurement-set design, plant label design and tracer evaluation). These
records remain supporting leads unless full text was inspected; the
correction does not strengthen any substantive claim below.

Six primary papers were inspected in complete open full text. Five occurred
in the prospective result pages; the commissioned Crown–Antoniewicz anchor
was also checked directly against its PMC full text and used as the
PHASE2-SEARCH-0009 forward-citation seed.

## Load-bearing primary evidence

### Crown and Antoniewicz (2012): EMU-basis tracer selection

**Citation:** Crown SB, Antoniewicz MR. Selection of tracers for
13C-metabolic flux analysis using elementary metabolite units (EMU) basis
vector methodology. *Metabolic Engineering*. 2012;14(2):150–161.
doi:10.1016/j.ymben.2011.12.005.

- **Decision problem:** choose substrate labelling that makes free fluxes
  observable/precisely estimable.
- **Design variables:** tracer identity and labelling pattern; D-optimality
  is used to choose among feasible label schemes.
- **Criterion/object:** EMU-basis-vector rank and coefficient sensitivities,
  followed by a D-optimality test; the decided scientific object remains
  flux, not mechanism.
- **Evidence location:** full-text sections “EMU coefficient sensitivities
  and tracer experiment design strategy” and “Comparison of tracers for
  mammalian network model”; §4 Conclusions. The Conclusions state the rank
  condition and describe D-optimality as correlating with simulated flux
  confidence intervals.
- **Guarantee boundary:** the EMU rank condition is an observability/rank
  obstruction within the specified network and measurements. Numerical
  confidence-interval comparisons are simulation based. Neither is a
  finite-sample mechanism-discrimination error guarantee.

### Crown, Ahn and Antoniewicz (2012): rational mammalian tracer design

**Citation:** Crown SB, Ahn WS, Antoniewicz MR. Rational design of
13C-labeling experiments for metabolic flux analysis in mammalian cells.
*BMC Systems Biology*. 2012;6:43. doi:10.1186/1752-0509-6-43.

- **Decision problem:** reduce the candidate tracer space and select tracers
  that improve resolution of oxPPP and pyruvate-carboxylase fluxes.
- **Design variables:** pure glucose/glutamine tracer identity and labelling
  pattern; mixtures are evaluated secondarily.
- **Criterion/object:** EMU coefficient sensitivities create labelling
  rules; simulated nonlinear profile confidence intervals compare retained
  candidates.
- **Evidence location:** “EMU coefficient sensitivities and tracer
  experiment design strategy” (five-step procedure); “Comparison of tracers
  for mammalian network model”; Methods “Metabolic flux analysis”;
  Conclusions.
- **Guarantee boundary:** heuristic search-space reduction plus
  simulation-based flux-precision comparison at the PYC reference flux map.
  The paper neither selects network mechanisms nor certifies sample size.

### Walther et al. (2012): tracer-mixture optimisation

**Citation:** Walther JL, Metallo CM, Zhang J, Stephanopoulos G.
Optimization of 13C isotopic tracers for metabolic flux analysis in mammalian
cells. *Metabolic Engineering*. 2012;14(2):162–171.
doi:10.1016/j.ymben.2011.12.004.

- **Decision problem:** optimise glucose/glutamine isotope mixtures for
  precise central-carbon flux inference.
- **Design variables:** mixture composition over labelled glucose and
  glutamine isotopologues.
- **Criterion/object:** a genetic algorithm maximises a weighted precision
  score derived from nonlinear profile confidence-interval widths.
- **Evidence location:** §2.1 “Genetic algorithm,” equations (1)–(5),
  including the fitness definition; §3.1 “Tracer optimization”; the
  robustness exercise described in the Introduction and Results perturbs
  selected flux values.
- **Guarantee boundary:** optimiser performance and selected perturbation
  simulations are not global optimisation, continuous-class robustness, or
  finite-sample certification.

### Nöh et al. (2018): coupled input, measurement and cost design

**Citation:** Nöh K, Niedenführ S, Beyß M, Wiechert W. A Pareto approach to
resolve the conflict between information gain and experimental costs:
Multiple-criteria design of carbon labeling experiments. *PLOS
Computational Biology*. 2018;14(10):e1006533.
doi:10.1371/journal.pcbi.1006533.

- **Decision problem:** expose Pareto trade-offs among flux information and
  experiment costs.
- **Design variables:** tracer compositions, analytical platform,
  measurement groups, measurement-error assumptions and cost components.
  Technical repetitions enter error and cost models.
- **Criterion/object:** multi-objective optimisation of covariance-derived
  A-, D- and E-criteria, number of statistically identifiable fluxes, and
  cost.
- **Evidence location:** Methods “General framework for multi-objective
  experimental design,” equation (1); “Covariance-based information
  measures,” equations (7)–(14); “Cost model”; Results, Figures 4–8.
- **Guarantee boundary:** equations (7)–(14) are local Fisher/covariance
  approximations around an assumed flux design point. The E-criterion
  improves the least-informed covariance direction; it is not a minimax
  mechanism-error guarantee. Repetition affects an assumed measurement-error
  scaling and cost but the method does not derive prospective biological
  sample size or power.

### Crown, Long and Antoniewicz (2016): parallel-tracer scoring

**Citation:** Crown SB, Long CP, Antoniewicz MR. Optimal tracers for parallel
labeling experiments and 13C metabolic flux analysis: A new precision and
synergy scoring system. *Metabolic Engineering*. 2016;38:10–18.
doi:10.1016/j.ymben.2016.06.001.

- **Decision problem:** rank single and complementary parallel tracer
  experiments for joint flux estimation.
- **Design variables:** tracer identity and combinations of parallel tracer
  experiments.
- **Criterion/object:** the precision score is the mean squared ratio of
  reference to candidate 95% flux-confidence-interval widths; the synergy
  score compares joint-fit precision with the sum of component precision
  scores.
- **Evidence location:** §2.1 “The precision score” and its displayed
  definition; §2.2 “The synergy score” and its displayed definition;
  §4.1–4.3 simulations; §5 Conclusions.
- **Guarantee boundary:** “synergy” is a defined relative flux-precision
  score. It is not evidence for independent observations, decision power,
  controlled mechanism-selection error, or sufficiency.

### Beyß et al. (2021): sampled-flux robustification

**Citation:** Beyß M, Parra-Peña VD, Ramirez-Malule H, Nöh K. Robustifying
Experimental Tracer Design for 13C-Metabolic Flux Analysis. *Frontiers in
Bioengineering and Biotechnology*. 2021;9:685323.
doi:10.3389/fbioe.2021.685323.

- **Decision problem:** choose a tracer mixture that remains informative
  across uncertainty in the nominal flux map.
- **Design variables:** tracer-mixture composition and cost.
- **Criterion/object:** median D-criterion over sampled feasible flux maps,
  sampled “coverage” of an identifiable active-flux count, and tracer cost.
- **Evidence location:** §2.4 equations (3)–(8) and Algorithm 1; §3.2.1
  equations (9)–(11); §3.2.2 Algorithm 2; Figure 3; §4 Conclusion.
- **Guarantee boundary:** the two information criteria are aggregates over a
  finite Monte Carlo sample. The paper explicitly distinguishes median
  precision from sampled coverage. It does not establish uniformity over the
  continuous feasible flux polytope, mechanism discrimination, or
  finite-sample decision error.

## What is actually optimised

| Method family | Design variables | Optimised object/criterion | Evidence regime |
|---|---|---|---|
| Classical isotopomer/FIM design | tracer input; measurement type/panel | determinant, average variance, or eigenvalue of local covariance/FIM; flux identifiability | local/asymptotic approximation; Möllney et al. (1999) remains abstract-level in the current evidence |
| EMU-basis design | tracer identity and labelling pattern | EMU rank, coefficient sensitivity, then D-optimal flux precision | rank obstruction plus simulation/local precision |
| Mixture optimisation | glucose/glutamine mixture proportions | nonlinear profile-CI-derived flux precision score | heuristic genetic search and simulations |
| Multi-objective information/cost design | tracer, analytical platform, measurement groups, technical repetitions/cost | A-, D-, E-criteria, identifiable-flux count, cost Pareto front | local Fisher/covariance approximation |
| Parallel-tracer design | tracer identities and parallel combinations | relative nonlinear-CI precision and synergy | simulation-based ranking |
| Robustified tracer design | tracer mixture over sampled flux maps | median sampled D-score, sampled identifiability coverage, cost | simulation-based finite sampled flux set |
| INST-MFA timing/design | time points and transient labelling settings | identifiability/information in a dynamic model | discovery search recovered Nöh–Wiechert (2006), but full text was unavailable here; no load-bearing conclusion is drawn |

No inspected direct paper in this workstream uses T- or KL-optimality to
design an isotope experiment for structural-model discrimination. The A/D/E
labels in the isotope papers are covariance geometry for flux estimation,
not model-discrimination criteria bearing the same letters in adjacent
literatures.

## Gap-directed falsification findings

### Joint experimental design (relevant to GAP-04)

The broad proposition that isotope design considers only tracer identity is
false. Nöh et al. directly couples tracer, analytical platform, measurement
groups and costs, and allows technical repetition to affect error/cost.
Crown–Long–Antoniewicz treats combinations of parallel experiments. What is
not established by these papers is a single calibrated design over tracer,
biological perturbation/condition, measurement panel and biological
replicate allocation. The residual is principally computational for a
finite candidate design set; it becomes theoretical only if controlled
mechanism-decision error is required.

### Multi-condition evidence (relevant to GAP-05)

Parallel tracer papers demonstrate joint flux fitting and complementary
precision. They do not by themselves formulate heterogeneous condition
blocks, partially shared nuisance parameters, or composite mechanism
hypotheses. Thus they strongly weaken any claim that multiple isotope
experiments cannot be integrated, but do not falsify the narrower
non-IID-mechanism-discrimination distinction.

### Robust design (relevant to GAP-02/GAP-06)

Beyß et al. destroys a broad absence claim for uncertainty-aware isotope
tracer design. Its robustness scope is sampled nominal flux maps in a fixed
network and assumed noise model. Walther et al.'s perturbed-flux exercise is
still narrower. Neither addresses omitted reactions, atom-map errors,
compartment alternatives, or a uniform ambiguity class over EMU forward
models.

### Sample size and replicate allocation

The search found Blaise et al. (2016), doi:10.1021/acs.analchem.6b00188, as
an adjacent metabolic-phenotyping power method, but it is not a 13C-MFA
forward-design method. Nöh et al. includes technical repetitions in a
measurement-error/cost model. No inspected direct 13C-MFA paper makes
biological replicate count an output chosen to achieve calibrated
model-selection power. This is a bounded negative result, not an absence or
novelty claim.

## Bounded closure: dynamic/INST-MFA design

A prospective backward-reference extraction from all six verified anchors
(PHASE2-SEARCH-0056), three distinct-source dynamic-design searches
(PHASE2-SEARCH-0057–0059), and a forward-citation pass from Nöh and Wiechert
(PHASE2-SEARCH-0060) recovered no additional experimental-design family.

One newly inspected open full text was:

**Wahl SA, Nöh K, Wiechert W. 13C labeling experiments at metabolic
nonstationary conditions: an exploratory study. BMC Bioinformatics.
2008;9:152. doi:10.1186/1471-2105-9-152.**

- The paper models metabolically and isotopically nonstationary
  concentration/isotopomer observations for kinetic-parameter estimation.
- “Measurement model,” equations (4)–(5), represents observations at a
  vector of sampling times. “Statistical evaluation,” equation (10), uses
  linearised covariance/Fisher information and explicitly says the tool is
  used to compare experiments rather than precisely determine confidence
  regions.
- “Sampling and quality of the measurements” fixes a 19-time-point schedule
  and assumed measurement-error components; it does not optimise that
  schedule.
- The Conclusion reports simulation-based parameter-information improvement
  from specific labelling. It is not prospective sample-size design,
  calibrated power, or a finite-sample guarantee.

The load-bearing Nöh and Wiechert (2006) paper,
doi:10.1002/bit.20803, remains abstract-only because a legal complete primary
text was not retrieved. Consequently, its exact “almost optimal” dynamic
design algorithm, design variables and criterion cannot support definitive
synthesis here.

## Limitations and access

- Möllney et al. (1999), Nöh and Wiechert (2006), IsoDesign (2014), and
  COMPLETE-MFA (2013) remain supporting or discovery leads here because
  complete primary methods were not inspected in this workstream.
- Crossref searches were poorly specific. Their total match counts must not
  be interpreted as screened populations beyond the retained 25-result
  snapshots.
- The bounded OpenAlex, Crossref and Nöh forward-citation passes recovered
  the known dynamic/INST design lineage but do not establish exhaustive
  coverage. The family remains `INCOMPLETELY_SEARCHED` because result and
  citation windows were truncated, Nöh and Wiechert (2006) remains
  inaccessible, and COMPLETE-MFA remains abstract-only.

## Workstream conclusion

Established isotope experimental design is extensive for **flux precision,
local information geometry, tracer mixtures, measurement/platform choice,
parallel-experiment synergy, cost trade-offs, and sampled-flux
robustification**. In the inspected primary evidence, these methods rank or
optimise experiments for flux inference; they do not certify
mechanism-discrimination error, required biological replicate count, or
impossibility. The bounded dynamic-design searches verified the family but
did not exhaust it, and its principal 2006 method cannot support a
load-bearing claim until manually
retrieved. That narrower boundary is the main handoff to Workstreams B and C
and is not a novelty conclusion.
