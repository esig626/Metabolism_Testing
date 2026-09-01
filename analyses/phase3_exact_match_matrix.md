# Phase 3B exact-match matrix

## Scope and interpretation

This matrix answers the Phase 3B question by comparing inspected primary
papers with the complete direct-MID formulation. It is a bounded
exact-formulation search, not a literature-saturation or novelty claim.
`audit/phase3_screening.csv` is the row-level evidence register; the locations
given there and below are the inspected primary-source locations.
Its `P3-####` values are stable identifiers for the Phase 3B retained set,
not new canonical `P####` corpus assignments; existing corpus crosswalks are
recorded in the screening file and full corpus integration is deferred.

The required conjunction is:

1. replicate-level MIDs or raw isotope-resolved observations;
2. fluxes treated as latent nuisance parameters or downstream estimators;
3. metabolic-class testing rather than full flux recovery;
4. class testing that can survive flux non-identifiability;
5. several network-linked MIDs used as coupled parallel evidence;
6. distinct biological, batch, preparation, injection and measurement levels;
7. controlled finite-sample error or sample requirements.

`Y` means the paper contains the stated component, `P` means an explicit but
narrower analogue is present, and `N` means that the inspected source does
not provide the component. Mere absence of a fitted flux model is not enough
for `Y` in the flux column, and generic hypotheses or generic unidentified
parameters are not metabolic classes or fluxes. Likewise, deterministic
identifiability analysis and heuristic separation scores are not tests. A row
is an exact match only if the conjunction is essentially complete; no checked
row met that rule.
For the direct-application rows that receive `P` in the target column,
empirical mutant/condition/phenotype groups or proposed metabolic targets are
narrower analogues, not Phase 3 metabolic classes defined as induced sets of
observation laws.

## Exact-match matrix

| Phase 3 ID | Primary paper | Required classification | MID/raw primary observation | Flux represented as nuisance or downstream | Metabolic-class law/test target | Calibrated class test despite flux non-ID | Network-coupled multiple MIDs | Full experimental hierarchy | Finite-sample class error/sample requirement |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| P3-0001 | Schellenberger et al. 2012, DOI `10.1186/1752-0509-6-9` | PARTIAL FORMULATION | P | P | P | P | Y | N | N |
| P3-0002 | Zhang et al. 2023, DOI `10.1186/s12859-023-05211-5` | PARTIAL FORMULATION | Y | N | P | N | Y | N | N |
| P3-0003 / P0030 | Sundqvist et al. 2022, DOI `10.1371/journal.pcbi.1009999` | PARTIAL FORMULATION | Y | P | P | N | Y | N | N |
| P3-0004 | Crown et al. 2015, DOI `10.1016/j.ymben.2015.01.001` | PARTIAL FORMULATION | Y | N | N | N | Y | N | N |
| P3-0005 | Mairinger et al. 2018, DOI `10.1007/s00216-018-1017-7` | PARTIAL FORMULATION | Y | Y | N | N | P | P | N |
| P3-0006 / P0018 | Isermann & Wiechert 2003, DOI `10.1016/S0025-5564(02)00222-5` | PARTIAL FORMULATION | P | N | N | N | Y | N | N |
| P3-0007 | Rantanen et al. 2006, DOI `10.1093/bioinformatics/btl069` | PARTIAL FORMULATION | P | N | N | N | Y | N | N |
| P3-0008 | Antoniewicz et al. 2007, DOI `10.1016/j.ymben.2006.09.001` | PARTIAL FORMULATION | P | N | N | N | Y | N | N |
| P3-0009 | Zamboni & Sauer 2004, DOI `10.1186/gb-2004-5-12-r99` | APPLICATION WITHOUT THEORY | Y | P | P | N | P | N | N |
| P3-0010 | Galvis et al. 2024 (DIMet), DOI `10.1093/bioinformatics/btae282` | APPLICATION WITHOUT THEORY | Y | N | P | N | N | N | N |
| P3-0011 | Huang et al. 2014 (X13CMS), DOI `10.1021/ac403384n` | APPLICATION WITHOUT THEORY | Y | N | P | N | N | N | N |
| P3-0012 | Weindl et al. 2016, DOI `10.1186/s40170-016-0150-z` | APPLICATION WITHOUT THEORY | Y | P | P | N | N | N | N |
| P3-0013 | Frahm et al. 2020, DOI `10.1016/j.jmr.2020.106750` | APPLICATION WITHOUT THEORY | Y | N | P | N | P | N | N |
| P3-0014 | Bleuler & Zitzler 2007, DOI `10.1145/1276958.1277034` | APPLICATION WITHOUT THEORY | Y | P | P | N | P | N | N |
| P3-0015 | Cedersund 2012, DOI `10.1111/j.1742-4658.2012.08725.x` | PARTIAL FORMULATION | N | N | P | P | N | N | N |
| P3-0016 | Todem, Fine & Peng 2010, DOI `10.1111/j.1541-0420.2009.01290.x` | GENERIC THEORY ONLY | N | N | N | P | N | N | N |
| P3-0017 | Andrews & Mikusheva 2016, DOI `10.3982/ECTA12868` | GENERIC THEORY ONLY | N | N | N | P | N | N | N |
| P3-0018 / P0053 | Goldenshluger, Juditsky & Nemirovski 2015, DOI `10.1214/15-EJS1054` | GENERIC THEORY ONLY | N | N | N | P | N | N | Y |
| P3-0019 | Sieradzki et al. 2020, DOI `10.1128/mSystems.00151-20` | ADJACENT BUT NONTRANSFERABLE | N | N | P | N | N | P | P |
| P3-0020 | Wiechert & Wurzel 2001, DOI `10.1016/S0025-5564(00)00059-6` | PARTIAL FORMULATION | P | N | N | N | Y | N | N |
| P3-0021 | Suthers et al. 2007, DOI `10.1016/j.ymben.2007.05.005` | PARTIAL FORMULATION | Y | N | N | N | Y | N | N |
| P3-0022 | Dudek et al. 2020 (MIAMI), DOI `10.1093/bioinformatics/btaa251` | APPLICATION WITHOUT THEORY | Y | N | P | N | P | N | N |
| P3-0023 | Starke et al. 2025 (IMPACT), DOI `10.1093/bioinformatics/btaf591` | APPLICATION WITHOUT THEORY | Y | N | N | N | P | N | N |

The `Y` entries in the last column for P3-0018 concern generic represented
probability families. They do not establish a detector, least-favourable
pair, or sample requirement for a culture-induced MID family.

## Closest formulations by axis

There is no single dominating prior formulation.

- **Closest direct observation/decision precedent:** P3-0009 uses corrected
  GC-MS mass-isotope fragment vectors to discriminate mutants and conditions
  without fitting a biochemical network or fluxes. It is classified
  `APPLICATION WITHOUT THEORY` because PCA/ICA discrimination is not a
  probabilistic class test with controlled risk. See Background; Results
  “2H and 13C tracer experiments” and “Independent component analysis”; and
  Methods “GC-MS analysis and data preprocessing” and “Multivariate data
  analysis.”
- **Closest direct mode-of-action application:** P3-0022 carries raw GC-MS
  data through MID construction, condition-threshold calls and similarity/
  reference-network contextualization to propose metabolic targets. The
  threshold is user-defined and the network is an annotation/display object,
  not a shared-latent class law. See Abstract and §§1–2 and 4.
- **Closest induced-class/network-geometry precedent:** P3-0001 partitions a
  feasible flux set into high/low flux or flux-ratio classes, maps every
  sampled state to several fragment MDVs, and scores separation even where
  the full flux vector is not resolved. See Results “Monte Carlo Sampling
  Approach,” Figure 2, “Generating and Evaluating 13C Experimental
  Hypotheses,” and the `Z_i` and `Z` equations. Its score is a sampled
  separation heuristic, not a calibrated test.
- **Closest replicate-level probabilistic network model:** P3-0002 places an
  explicit likelihood on repeated isotopomer-concentration vectors generated
  by a nonlinear kinetic network. Its target is kinetic-parameter comparison,
  and its one residual level does not encode the experimental hierarchy. See
  Methods “A Bayesian kinetic model,” Equation 1 and the likelihood, and
  “Comparison of kinetic model parameters between experimental groups.”
- **Closest coupled parallel-MID estimation workflow:** P3-0004 jointly fits
  14 tracer experiments and 14 amino-acid fragments to one flux model; P3-0003
  shares fluxes across estimation and held-out tracer-validation datasets.
  Both decide or estimate through fitted flux/network models, not through a
  direct metabolic-class test.
- **Closest measurement-pipeline uncertainty model:** P3-0005 propagates raw
  ion counting, peak integration, ionisation/transmission and isotope-
  correction uncertainty to isotope fractions and then to fitted fluxes. Its
  three biological replicates provide an aggregate empirical precision term,
  not separately identifiable biological, culture, preparation and injection
  variance components.

## Classification result

- `EXACT FORMULATION`: **0 verified in this bounded search**.
- `PARTIAL FORMULATION`: P3-0001–P3-0008, P3-0015, P3-0020 and P3-0021.
- `GENERIC THEORY ONLY`: P3-0016–P3-0018.
- `APPLICATION WITHOUT THEORY`: P3-0009–P3-0014 and P3-0022–P3-0023.
- `ADJACENT BUT NONTRANSFERABLE`: P3-0019.

This zero count is confined to the executed searches and checked citation
neighbourhoods. It is not evidence of universal absence.
