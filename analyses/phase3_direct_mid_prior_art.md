# Phase 3B: direct MID-level prior art

## Answer to search family A

Direct analysis of isotope-resolved profiles is established in the inspected
primary literature. The closest papers use corrected fragment MIDs or raw
isotope-resolved signals for mutant/condition discrimination, differential
labeling, ranking, or machine-learning classification without first
recovering a full flux vector. They do **not** formulate the complete Phase 3
decision problem: none of the direct-analysis papers constructs metabolic-
class probability families by pushing a shared latent network state through
the culture-to-ion pipeline, and none controls finite-sample class error over
that family.

This finding falsifies any broad claim that isotope data have only been
analysed through flux estimation. It does not establish exact prior art for
GAP-08.

## Inspected direct-analysis precedents

### P3-0009 — Zamboni & Sauer (2004)

**Classification: APPLICATION WITHOUT THEORY.** This is the closest direct
observation/decision precedent.

- **Primary observation:** naturally-abundance-corrected GC-MS amino-acid
  fragment mass-distribution vectors, approximately 260 `13C` or 330 `2H`
  mass values per sample.
- **Inferential target:** unsupervised discrimination of mutants and culture
  conditions and extraction of isotope-profile “fingerprints.”
- **Flux treatment:** no biochemical network or flux vector is fitted;
  selected ICA components are only compared post hoc with analytically
  derived flux ratios.
- **Non-identifiability:** avoidance of a network model permits analysis where
  numerical flux analysis is unavailable, but the paper does not prove a
  class-testing result under flux non-identifiability.
- **Several MIDs:** fragment vectors are concatenated for PCA/ICA. This is a
  multivariate data analysis, not a probability law coupled through one
  declared latent metabolic state.
- **Sampling unit and hierarchy:** the physical candidate is a culture/sample.
  Duplicate strain-medium experiments were reported as independently started
  from stocks; no day, batch, preparation, injection or measurement hierarchy
  was modeled. The duplicates were not turned into independent coordinates
  of the PCA/ICA analysis.
- **Guarantee:** none for class error or sample size. Discussion mentions
  duplicates and bootstrap stability as possible checks on components.

Exact locations: Abstract; Background, final two paragraphs; Results “2H and
13C tracer experiments,” “Independent component analysis (ICA),” and Figure
5; Discussion; Methods “Strains and growth conditions,” “GC-MS analysis and
data preprocessing,” and “Multivariate data analysis.” DOI
`10.1186/gb-2004-5-12-r99`; PMCID `PMC545802`.

### P3-0010 — Galvis et al. (2024), DIMet

**Classification: APPLICATION WITHOUT THEORY.**

- **Primary observation:** corrected isotopologue absolute values or
  proportions, metabolite abundance and mean enrichment supplied in a sample
  table.
- **Target:** pairwise, multigroup and time-course differential labeling and
  labeling-profile comparison.
- **Flux treatment:** the paper explicitly places flux analysis outside
  DIMet's scope.
- **Several MIDs/network:** individual profiles can be compared and PCA or a
  network metabologram can be displayed, but no shared-latent joint MID law is
  fitted.
- **Sampling unit/hierarchy:** an input sample is the analysis row. Triplicates
  are reported in the use case, without establishing independence or a
  variance-component hierarchy.
- **Guarantee:** ordinary `t`, Wilcoxon, Mann–Whitney, Kruskal–Wallis and
  permutation tests plus multiple-testing adjustment are offered. There is no
  isotope-family-specific finite-sample theorem or prospective sample
  requirement.

Exact locations: §1, including the statement that DIMet does not aim to
perform flux analysis; §2.1, input quantities, tests and bivariate profile
comparison; §3.1, example triplicates; §§3.2.1–3.2.2 and Figure 1. DOI
`10.1093/bioinformatics/btae282`; PMCID `PMC11109473`.

### P3-0011 — Huang et al. (2014), X13CMS

**Classification: APPLICATION WITHOUT THEORY.**

- **Primary observation:** LC-MS ion intensities grouped into isotopologues
  and converted to relative isotope-enrichment profiles across samples.
- **Target:** condition-specific enrichment and differentially labeled
  isotopologue groups.
- **Flux:** absent from the statistical comparison.
- **Several MIDs/network:** isotopologues or groups are tested separately; a
  group-level call is constructed from component results, not from a common
  network-nuisance model.
- **Sampling:** the example reports triplicate cultures; the method does not
  infer a general sampling hierarchy from that application.
- **Guarantee:** Welch tests are used. The rule that a group is differential
  if any component passes, and the special handling of groups detected in
  only one condition, are not accompanied by a network-level error guarantee.

Exact locations: Figure 1; Experimental Section “X13CMS Analysis,” including
`getIsoLabelReport()` and `getIsoDiffReport()`; Tables 2–3. DOI
`10.1021/ac403384n`; PMCID `PMC3982964`.

### P3-0012 — Weindl et al. (2016)

**Classification: APPLICATION WITHOUT THEORY.**

- **Primary observation:** corrected metabolome-wide MIDs across conditions.
- **Target:** rank qualitative labeling/flux changes and place unknown
  compounds in a MID-similarity network.
- **Flux:** only qualitative pathway consequences are inferred; a shared flux
  state is not fitted as nuisance.
- **Non-identifiability:** the paper notes that MIDs provide relative
  information and that not every flux change alters an MID, but does not turn
  this into a class-testability theorem.
- **Several MIDs:** a pairwise distance network is constructed. Edges encode
  profile similarity, not a shared-latent probability law.
- **Sampling/hierarchy/guarantee:** no experimental variance hierarchy and no
  calibrated class error. A reported `n=3` for a follow-up experiment cannot
  be generalized to every MID measurement.

Exact locations: Methods “Mass isotopomer abundance variation” and “MID
distance calculation”; Results “Locating flux changes in the metabolic
network” and Figure 1; Discussion. DOI `10.1186/s40170-016-0150-z`; PMCID
`PMC4842284`.

### P3-0013 — Frahm et al. (2020)

**Classification: APPLICATION WITHOUT THEORY.**

- **Primary observation:** isotope-resolved hyperpolarized `13C` NMR signal
  integrals from cultured prostate cell samples; these are raw
  isotope-resolved activity features rather than conventional MS MIDs.
- **Target:** multiclass cell-line classification and binary aggressive versus
  indolent classification.
- **Flux:** not recovered. Random-forest feature ranking and an SVM act
  directly on signal integrals.
- **Several observations:** multiple metabolite/positional signals enter one
  classifier, but no network forward law couples them.
- **Sampling:** 32 reported samples, eight per cell type. The source calls
  them samples; it does not justify treating cell lines, signals or repeated
  measurements as additional biological units.
- **Guarantee:** leave-one-out cross-validation and observed accuracy are
  empirical performance, not prospective finite-sample error control.

Exact locations: author manuscript pp. 2–3, Introduction and Results/sample
description; pp. 3–5, ANOVA, random-forest feature selection, SVM and
leave-one-out validation; Table 1 and Table 2; pp. 5–6, Discussion. DOI
`10.1016/j.jmr.2020.106750`.

### P3-0014 — Bleuler & Zitzler (2007)

**Classification: APPLICATION WITHOUT THEORY.**

This work clusters or partitions concatenated isotope profiles with an
evolutionary algorithm and silhouette-type objectives. It explicitly
motivates profile discrimination when exact fluxes or ratios cannot be
recovered, but the optimization repetitions are algorithm seeds, not
biological replicates, and no sampling law or decision error is provided.
Exact locations: p. 354 Abstract; §2.1 pp. 355–356; §3, equations (2)–(6),
pp. 356–357; §5.1 pp. 357–358; §5.3 and Figure 3 p. 358; §6 pp. 359–360.
DOI `10.1145/1276958.1277034`.

### P3-0022 — MIAMI (Dudek et al., 2020)

**Classification: APPLICATION WITHOUT THEORY.** This is the closest inspected
application explicitly framed as mode-of-action identification. MIAMI starts
from raw GC-MS data, calculates MIDs for labeled and unlabeled extracts,
detects condition-dependent changes with a user-defined variability threshold,
and overlays MID-similarity connections on reference pathways to propose
potential targets. Flux change is an interpretation of thresholded MID change;
there is no latent-flux law, treatment of flux non-identifiability, declared
biological sampling unit, or calibrated class error. The similarity/reference
network is contextualization, not coupling through one shared latent state.

Exact locations: Abstract; §1, especially the distinction between targeted
and non-targeted interpretation and the experimental prerequisite; §2,
raw-data processing, MID calculation, variability threshold and network
mapping; §4. DOI `10.1093/bioinformatics/btaa251`; PMCID `PMC7320603`.

### P3-0023 — IMPACT (Starke et al., 2025)

**Classification: APPLICATION WITHOUT THEORY.** IMPACT adds a fuller
raw-LC-MS-to-MID workflow: peak picking, retention-time alignment, feature
grouping/filling, isotope detection, MID calculation and similarity/reference-
pathway contextualization. It can also start from external MID tables. The
paper does not fit flux, specify a class-testing law, model biological and
technical variance levels, or provide a finite-sample error/sample
requirement. Its network is an annotation/similarity object, not an
experiment-induced joint law.

Exact locations: Abstract; §1; §2 and Figure 1, including Modules 1–3 and
the similarity-network description; §3; §4. DOI
`10.1093/bioinformatics/btaf591`; PMCID `PMC12684724`.

## Testing is not estimation, classification is not calibrated testing

| Operation in the inspected literature | What it establishes | What it does not establish |
|---|---|---|
| PCA/ICA or evolutionary grouping of corrected fragment profiles | direct flux-free discrimination can be empirically informative | a null/alternative family, uniform Type-I/II control, or sample requirement |
| Per-isotopologue or per-metabolite ordinary tests | condition differences can be screened directly at isotope level | a coupled network-class test or valid treatment of sibling fragments as biological replicates |
| Cross-validated machine-learning classification | out-of-sample performance within the reported dataset/split rule | worst-case error over latent flux and batch/preparation/injection nuisance |
| Network display of MID similarities or differential signals | visualization/localisation of related profile changes | a metabolic-network forward constraint or shared-latent composite law |
| Flux fitting followed by model selection | a candidate network can be ranked after estimation | direct metabolic-class testing without flux recovery |

## Family-A conclusion

Direct or flux-free isotope-profile analysis is established, including
multivariate use of many fragment signals. The checked papers stop at
exploratory discrimination, ordinary differential tests, empirical
classification, or network visualization. Their closest contribution to
Phase 3 is the choice of primary observation and target; the probability
family, dependence, hierarchy and finite-sample decision guarantee remain
unprovided in these sources.
