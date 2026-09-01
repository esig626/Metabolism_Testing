# Phase 3B search log

Search date: 2026-08-01 UTC

Searcher: Codex

Review type: bounded exact-formulation search

Default filters: no date, language or publication-type restriction unless a
row says otherwise. PubMed `retmax=100`; OpenAlex windows are stated. Result
counts are provider-reported and may change. Retained counts are unique
primary papers retained from the row, not all overlapping occurrences.

## A. Direct MID-level inference

| ID | Source | Exact query / endpoint parameters | Total / returned | Retained | Raw capture / notes |
|---|---|---|---:|---:|---|
| P3-SEARCH-0001 | PubMed | `((mass isotopomer distribution[Title/Abstract] OR isotopologue distribution[Title/Abstract] OR isotope-resolved metabolomics[Title/Abstract]) AND (hypothesis testing[Title/Abstract] OR statistical testing[Title/Abstract] OR multivariate[Title/Abstract] OR discrimination[Title/Abstract] OR model-independent[Title/Abstract] OR flux-free[Title/Abstract]))` | 3 / 3 | 2 | `A/P3-SEARCH-0001_pubmed*.json`; Zhang and Frahm retained |
| P3-SEARCH-0002 | OpenAlex | full-text search `direct statistical testing mass isotopomer distributions isotope resolved metabolomics model independent flux free metabolic tracing`; `per-page=100` | 150 / 100 | 4 | `A/P3-SEARCH-0002_openalex.json`; broad discovery, many biological false positives |
| P3-SEARCH-0017 | PubMed | `("mass isotopomer distribution"[Title/Abstract] OR "mass isotopomer distributions"[Title/Abstract] OR "isotopologue pattern"[Title/Abstract]) AND (differential[Title/Abstract] OR comparison[Title/Abstract] OR hypothesis[Title/Abstract]) AND (metabolic[Title/Abstract] OR metabolomics[Title/Abstract])` | 9 / 9 | 1 | `A/P3-SEARCH-0017_pubmed*.json`; overlapping direct-analysis application |
| P3-SEARCH-0018 | OpenAlex | `filter=title.search:isotope labeled metabolomics differential analysis`; `per-page=100` | 1 / 1 | 1 | `A/P3-SEARCH-0018_openalex.json`; DIMet |
| P3-A-PM-01 | PubMed | `("stable isotope resolved metabolomics"[Title/Abstract] OR SIRM[Title/Abstract] OR isotopomer*[Title/Abstract]) AND (hypothesis test*[Title/Abstract] OR "differential labeling"[Title/Abstract] OR "group comparison"[Title/Abstract] OR "comparison between experimental groups"[Title/Abstract])` | 3 / 3 | 1 | discovery cross-check; IDs `36949395,14673819,10631271` |
| P3-A-PM-03 | PubMed | `("stable isotope-resolved metabolomics"[Title/Abstract] OR "isotope-labeled metabolomics"[Title/Abstract]) AND (statistical test*[Title/Abstract] OR differential analys*[Title/Abstract] OR multivariate[Title/Abstract])` | 2 / 2 | 1 | discovery cross-check; IDs `39872723,38656970` |
| P3-A-OA-02 | OpenAlex | `filter=title.search:mass isotopomer distribution`; `per-page=100` | 60 / 60 | 0 additional | MIDA review used only for orientation |

## B. Testing without parameter identification

| ID | Source | Exact query / endpoint parameters | Total / returned | Retained | Raw capture / notes |
|---|---|---|---:|---:|---|
| P3-SEARCH-0004 | PubMed | `((nonidentifiability[Title/Abstract] OR non-identifiability[Title/Abstract] OR partial identification[Title/Abstract] OR testability without estimability[Title/Abstract] OR ill-posed inverse[Title/Abstract]) AND (hypothesis testing[Title/Abstract] OR class testing[Title/Abstract] OR mechanism testing[Title/Abstract] OR metabolic flux[Title/Abstract] OR isotope[Title/Abstract]))` | 7 / 7 | 0 | `B/P3-SEARCH-0004_pubmed*.json`; false positives illustrate terminology sensitivity |
| P3-SEARCH-0005 | OpenAlex | search `hypothesis testing under nonidentifiability testability without estimability partial identification nonlinear inverse models metabolic mechanism`; `per-page=100` | 4 / 4 | 0 | `B/P3-SEARCH-0005_openalex.json`; false positives |
| P3-B-PB0 | PubMed | `((stable isotope[Title/Abstract] OR isotopomer[Title/Abstract] OR isotopologue[Title/Abstract]) AND (nonidentifiability[Title/Abstract] OR non-identifiability[Title/Abstract]) AND (testing[Title/Abstract] OR discrimination[Title/Abstract] OR selection[Title/Abstract]))`; `retmax=20` | 0 / 0 | 0 | exact conjunction query |
| P3-B-PBEX | PubMed | `((13C metabolic flux analysis[Title/Abstract] OR 13C-MFA[Title/Abstract]) AND (model discrimination[Title/Abstract] OR model selection[Title/Abstract]) AND (identifiability[Title/Abstract] OR identifiable[Title/Abstract]))` | 0 / 0 | 0 | exact conjunction variant |
| P3-B-PB1 | PubMed | `(("metabolic flux analysis"[Title/Abstract] OR "stable isotope resolved metabolomics"[Title/Abstract]) AND ("model selection"[Title/Abstract] OR "model discrimination"[Title/Abstract] OR identifiability[Title/Abstract]))` | 18 / 18 | 4 | isotope identifiability/model-selection papers; IDs recorded in screening notes |
| P3-B-PB2 | PubMed | `(("non-identifiable models"[Title/Abstract] OR nonidentifiability[Title/Abstract] OR "non-identifiable"[Title/Abstract]) AND ("hypothesis testing"[Title/Abstract] OR "statistical hypotheses"[Title/Abstract] OR test[Title/Abstract]))` | 47 / 47 | 1 | Todem et al.; remaining records unrelated domains or different non-ID problems |
| P3-B-EPMC1 | Europe PMC | `(TITLE_ABS:"metabolic flux analysis" OR TITLE_ABS:"stable isotope resolved metabolomics") AND (TITLE_ABS:"model selection" OR TITLE_ABS:"model discrimination" OR TITLE_ABS:identifiability)`; `pageSize=100` | 18 / 18 | 4 overlapping | PubMed/preprint duplicates screened separately |
| P3-B-EPMC2 | Europe PMC | `(TITLE_ABS:"non-identifiable models" OR TITLE_ABS:nonidentifiability OR TITLE_ABS:"non-identifiable") AND (TITLE_ABS:"hypothesis testing" OR TITLE_ABS:"statistical hypotheses" OR TITLE_ABS:test)`; `pageSize=100` | 29 / 29 | 1 | Todem et al. |
| P3-B-OA0 | OpenAlex | search `"stable isotope" nonidentifiability hypothesis testing model discrimination`; `per-page=25` | 3 / 3 | 0 | one unrelated ERK article and two dissertations; article filter gave 1/1 unrelated |
| P3-B-OAEX | OpenAlex | search `"13C metabolic flux analysis" model selection identifiability`; article-filtered cross-check | 41 / 41; article filter 25 / 25 | 4 overlapping | estimation/design/model-selection results |
| P3-B-OA1 | OpenAlex | search `stable isotope metabolic flux model selection identifiability`; `filter=type:article`, `per-page=50` | 354 / 50 | 4 overlapping | discovery window; count is not negative evidence |
| P3-B-OA2 | OpenAlex | search `hypothesis testing nonidentifiable model partial identification inverse problem`; `filter=type:article`, `per-page=50` | 55 / 50 | 2 | Todem and Andrews–Mikusheva anchors |

## C. Network-coupled parallel observations

| ID | Source | Exact query / endpoint parameters | Total / returned | Retained | Raw capture / notes |
|---|---|---|---:|---:|---|
| P3-SEARCH-0009 | PubMed | `((13C metabolic flux analysis[Title/Abstract]) OR (isotope labeling[Title/Abstract] AND metabolic[Title/Abstract])) AND (parallel[Title/Abstract] OR joint[Title/Abstract] OR multi-experiment[Title/Abstract]) AND (model[Title/Abstract] OR testing[Title/Abstract] OR validation[Title/Abstract])` | 12 / 12 | 3 | `C/P3-SEARCH-0009_pubmed*.json`; includes Crown and network validation |
| P3-SEARCH-0010 | OpenAlex | full-text search `network coupled parallel observations shared latent flux isotope labeling metabolic network testing`; `per-page=50` | 236 / 50 | 1 | `C/P3-SEARCH-0010_openalex.json`; noisy broad window |
| P3-SEARCH-0011 | OpenAlex | full-text search `parallel labeling experiments 13C metabolic flux analysis joint fitting shared flux model`; `per-page=50` | 98 / 50 | 5 | `C/P3-SEARCH-0011_openalex.json`; strongest C-family query |
| P3-SEARCH-0012 | Crossref | bibliographic query `network constrained joint testing parallel composite shared latent metabolic isotope`; `rows=50` | 72,077 / 50 | 0 additional | `C/P3-SEARCH-0012_crossref.json`; high-noise discovery check only |

## D. Hierarchical experimental pipeline

| ID | Source | Exact query / endpoint parameters | Total / returned | Retained | Raw capture / notes |
|---|---|---|---:|---:|---|
| P3-SEARCH-0013 | PubMed | `(stable isotope tracing[Title/Abstract] OR isotope-resolved metabolomics[Title/Abstract] OR 13C metabolic flux analysis[Title/Abstract]) AND (biological variation[Title/Abstract] OR technical variation[Title/Abstract] OR variance components[Title/Abstract] OR batch effect[Title/Abstract] OR sample size[Title/Abstract] OR power[Title/Abstract] OR replicate[Title/Abstract])` | 19 / 19 | 2 | `D/P3-SEARCH-0013_pubmed*.json` |
| P3-SEARCH-0014 | OpenAlex | full-text search `hierarchical statistical model variance components biological technical batch extraction injection stable isotope tracing metabolomics MID`; `per-page=50` | 8 / 8 | 0 additional | `D/P3-SEARCH-0014_openalex.json` |
| P3-SEARCH-0015 | PubMed | `(mass isotopomer distribution[Title/Abstract] OR isotopologue distribution[Title/Abstract]) AND (measurement uncertainty[Title/Abstract] OR covariance[Title/Abstract] OR biological variability[Title/Abstract] OR technical variability[Title/Abstract] OR replicate[Title/Abstract]) AND (metabolic[Title/Abstract] OR metabolomics[Title/Abstract])` | 4 / 4 | 1 | `D/P3-SEARCH-0015_pubmed*.json`; Mairinger retained |
| P3-SEARCH-0016 | OpenAlex | full-text search `measurement uncertainty isotope labeling mass isotopologue biological technical variance replicate metabolic flux`; `per-page=50` | 35 / 35 | 2 | `D/P3-SEARCH-0016_openalex.json` |

## E. Geometry of induced families

| ID | Source | Exact query / endpoint parameters | Total / returned | Retained | Raw capture / notes |
|---|---|---|---:|---:|---|
| P3-SEARCH-0007 | PubMed | `((mass isotopomer distribution[Title/Abstract] OR isotopomer model[Title/Abstract] OR isotope labeling map[Title/Abstract]) AND (geometry[Title/Abstract] OR convexity[Title/Abstract] OR nonconvexity[Title/Abstract] OR identifiability[Title/Abstract] OR feasible flux space[Title/Abstract] OR probability simplex[Title/Abstract]))` | 2 / 2 | 1 | `E/P3-SEARCH-0007_pubmed*.json` |
| P3-SEARCH-0008 | OpenAlex | search `geometry image flux polytopes isotope labeling maps mass isotopomer distributions nonlinear forward induced families identifiability simplex`; `per-page=100` | 0 / 0 | 0 | `E/P3-SEARCH-0008_openalex.json`; zero is not absence evidence |
| P3-SEARCH-0019 | PubMed | `(isotopomer[Title/Abstract] OR isotopologue[Title/Abstract] OR "mass distribution vector"[Title/Abstract]) AND (identifiability[Title/Abstract] OR "feasible flux"[Title/Abstract] OR "Monte Carlo sampling"[Title/Abstract] OR nonconvex[Title/Abstract])` | 11 / 11 | 3 | `E/P3-SEARCH-0019_pubmed*.json` |
| P3-SEARCH-0020 | OpenAlex | `filter=title.search:predicting outcomes steady-state 13C isotope tracing Monte Carlo sampling`; `per-page=100` | 1 / 1 | 1 | `E/P3-SEARCH-0020_openalex.json`; Schellenberger |
| P3-E-PM-02 | PubMed | `(isotopomer[Title/Abstract] OR isotopologue[Title/Abstract] OR "13C metabolic flux"[Title/Abstract]) AND (geometry[Title/Abstract] OR geometric[Title/Abstract] OR polytope[Title/Abstract] OR convexity[Title/Abstract] OR nonconvexity[Title/Abstract])` | 53 / 53 | 0 additional | geometry terminology was largely unrelated to induced-law images |
| P3-E-OA-01 | OpenAlex | `filter=title.search:metabolic isotopomer identifiability` | 1 / 1 | 1 | Isermann |
| P3-E-OA-03 | OpenAlex | search `geometry isotopomer flux polytope metabolic` | 3 / 3 | 0 additional | no additional structural coverage category |
| P3-SEARCH-0021 | OpenAlex | search `least favourable distributions nonlinear forward model induced families inverse image isotope metabolic network probability simplex`; `filter=type:article`, `per-page=50` | 1 / 1 | 0 | `E/P3-SEARCH-0021_openalex.json`; unrelated acoustic-signal false positive |

## Supplementary browser discovery

The browser interface did not expose stable total counts, so counts are
recorded as `NOT EXPOSED`. These searches were used for discovery/full-text
location only, never as absence evidence. Retained papers were subsequently
checked in primary full text.

| ID | Exact query | Count | Retained / use |
|---|---|---:|---|
| P3-WEB-01 | `"parallel labeling experiments" 13C metabolic flux analysis shared flux MID` | NOT EXPOSED | Crown/parallel-MFA discovery |
| P3-WEB-02 | `"hierarchical" "stable isotope" tracing statistical model MID` | NOT EXPOSED | no additional category |
| P3-WEB-03 | `"biological variation" "mass isotopomer distribution" technical variation` | NOT EXPOSED | measurement-uncertainty discovery |
| P3-WEB-04 | `"sample size" "stable isotope tracing" metabolomics` | NOT EXPOSED | adjacent power literature |
| P3-WEB-05 | `"mass isotopomer distribution" covariance measurement error 13C MFA` | NOT EXPOSED | Mairinger/analytical-error discovery |
| P3-WEB-06 | `"mass isotopomer distributions" biological replicates statistics` | NOT EXPOSED | no additional category |
| P3-WEB-07 | `"stable isotope tracing" "technical replicates" variance` | NOT EXPOSED | no additional category |
| P3-WEB-08 | `"13C-MFA" replicate "sample size"` | NOT EXPOSED | no direct biological-power method |
| P3-WEB-09 | `site:pmc.ncbi.nlm.nih.gov 13C metabolic flux analysis parallel labeling experiments shared flux model multiple MIDs` | NOT EXPOSED | Crown and PLE orientation |
| P3-WEB-10 | `site:pmc.ncbi.nlm.nih.gov stable isotope tracing mass isotopologue distribution statistical biological technical variation uncertainty` | NOT EXPOSED | analytical/direct methods |
| P3-WEB-11 | `site:pmc.ncbi.nlm.nih.gov mass isotopomer distribution direct hypothesis testing biological replicates` | NOT EXPOSED | no exact match |
| P3-WEB-12 | `site:pmc.ncbi.nlm.nih.gov isotope resolved metabolomics power sample size replicate design` | NOT EXPOSED | adjacent qSIP/power work |
| P3-WEB-13 | `"Measurement uncertainty of isotopologue fractions in fluxomics" full text` | NOT EXPOSED | repository record; full text not used substantively |
| P3-WEB-14 | `"Effect of Error Propagation in Stable Isotope Tracer Studies" full text` | NOT EXPOSED | abstract/preview only; not retained |
| P3-WEB-15 | `"Stable isotope resolved metabolomics classification" prostate cancer hyperpolarized NMR full text` | NOT EXPOSED | Frahm full manuscript located |
| P3-WEB-16 | `"model-independent fluxome profiling" citations isotope profile discrimination` | NOT EXPOSED | Zamboni and Bleuler |
| P3-WEB-17 | `Schellenberger 2012 13C experimental hypotheses PMC feasible flux space` | NOT EXPOSED | Schellenberger full text |
| P3-WEB-18 | `Rantanen Mielikäinen Rousu 2006 isotopomer measurement selection full text` | NOT EXPOSED | Rantanen official full text |
| P3-WEB-19 | `Bayesian kinetic modeling tracer based metabolomic data PMC 36949395` | NOT EXPOSED | Zhang full text |
| P3-WEB-20 | `DIMet Differential Analysis labeled metabolomics PMC` | NOT EXPOSED | DIMet full text |
| P3-WEB-21 | `Cedersund 2012 Conclusions via unique predictions non-identifiable models core predictions full text` | NOT EXPOSED | Cedersund full text |
| P3-WEB-22 | `Todem Fine Peng 2010 nonidentifiable hypothesis testing full text` | NOT EXPOSED | Todem full text |
| P3-WEB-23 | `Andrews Mikusheva 2016 nonidentification hypothesis test nuisance full text` | NOT EXPOSED | accepted manuscript |
| P3-WEB-24 | `"testability without identifiability"` | NOT EXPOSED | generic terminology discovery |
| P3-WEB-25 | `"hypothesis testing" nonidentifiable inverse problem` | NOT EXPOSED | generic testing discovery |
| P3-WEB-26 | `"class identification without parameter identification"` | NOT EXPOSED | Cedersund/generic discovery |
| P3-WEB-27 | `"metabolic mechanism testing" without flux estimation` | NOT EXPOSED | no additional structural coverage category |
| P3-WEB-28 | `"stable isotope" prediction despite nonidentifiability` | NOT EXPOSED | no exact match |
| P3-WEB-29 | `"13C MFA" model discrimination identifiability` | NOT EXPOSED | isotope model-selection/ID papers |
| P3-WEB-30 | `"Conclusions via unique predictions obtained despite unidentifiability" PDF` | NOT EXPOSED | Cedersund full text |
| P3-WEB-31 | `"Conditional Inference With a Functional Nuisance Parameter" pdf` | NOT EXPOSED | Andrews–Mikusheva manuscript |
| P3-WEB-32 | `"A global sensitivity test" "2.3 Global sensitivity testing"` | NOT EXPOSED | Todem exact section |
| P3-WEB-33 | `"10.1016/S0025-5564(00)00059-6"` | NOT EXPOSED | Wiechert–Wurzel title/metadata verification |
| P3-WEB-34 | `"10.1016/j.ymben.2007.05.005" title` | NOT EXPOSED | Suthers title/metadata verification |
| P3-WEB-35 | `Antoniewicz Kelleher Stephanopoulos 2007 EMU PMC1994654 full text` | NOT EXPOSED | official PMC full text located after BioC failure |
| P3-WEB-36 | `"Elementary metabolite units" 2007 full text pdf` | NOT EXPOSED | author/PMC full-text cross-check |
| P3-WEB-37 | `Suthers Burgard Dasika 2007 PMC2121621 full text` | NOT EXPOSED | official PMC full text located after BioC failure |
| P3-WEB-38 | `"A global sensitivity test for evaluating statistical hypotheses with nonidentifiable models" DOI` | NOT EXPOSED | Todem DOI verification |
| P3-WEB-39 | `"Planning optimal measurements of isotopomer distributions" DOI` | NOT EXPOSED | Rantanen title/DOI verification |
| P3-WEB-40 | `"Conclusions via unique predictions obtained despite unidentifiability" DOI` | NOT EXPOSED | Cedersund title/DOI verification |
| P3-WEB-41 | `"Discrimination of metabolic flux profiles using a hybrid evolutionary algorithm" DOI` | NOT EXPOSED | Bleuler primary PDF/metadata verification |
| P3-WEB-42 | `site:sciencedirect.com/science/article/pii/S0025556402002225 Isermann Wiechert structural flux identifiability Theorem 4 global local` | NOT EXPOSED | delegated hostile-QC check; existing P3-0006/P0018 only; confirmed full-information global versus partial-information local scope, with no new record |
| P3-WEB-43 | `10.1093/bioinformatics/btaa251 MIAMI full text` | NOT EXPOSED | MIAMI primary full text; direct MID-threshold/network application found by citation chaining |
| P3-WEB-44 | `10.1093/bioinformatics/btw317 MIA non-targeted mass isotopolome analysis full text` | NOT EXPOSED | MIA primary application note; same direct-profile/network-visualisation category |
| P3-WEB-45 | `10.1007/s00216-019-01773-7 validation scheme 13C metabolite tracer studies full text` | NOT EXPOSED | primary analytical-validation paper; technical-replicate/reference-material QC, no hierarchy/class test |
| P3-WEB-46 | `site:journals.plos.org/ploscompbiol 10.1371/journal.pcbi.1013098 conformal prediction dynamic biological systems full text` | NOT EXPOSED | official PLOS full text subsequently checked; prediction coverage, not MID class testing |
| P3-WEB-47 | `site:academic.oup.com/bioinformatics btaf591 IMPACT full text methods MID network` | NOT EXPOSED | IMPACT full-text routing; official article initially returned a minimal page |
| P3-WEB-48 | `"Integrative Metabolic-Flux Platform" IMPACT btaf591 PMC` | NOT EXPOSED | IMPACT PMC full text located and checked |
| P3-WEB-49 | `"Integrative Metabolic-Flux Platform" btaf591 PDF` | NOT EXPOSED | IMPACT primary/authoritative PDF and metadata routes; no added formulation category |
| P3-WEB-50 | `10.1016/j.ymben.2018.10.005 full text alternative steady state kinetic models metabolism` | NOT EXPOSED | primary kinetic-model paper; alternative steady states affect prediction, but observations are not isotope-resolved class data |
| P3-WEB-51 | `10.3390/metabo14010024 full text Bayesian parallel tracer granulocytes` | NOT EXPOSED | parallel-tracer Bayesian MFA application; flux remains inferential target |
| P3-WEB-52 | `10.3390/psf2025012005 full text trans-dimensional diffusive nested sampling metabolic network inference` | NOT EXPOSED | primary technical report checked; synthetic `13C`-MFA model evidence/flux posterior, same structural Bayesian-inference category as P0031–P0032 |

## Backward and forward citation searches

OpenAlex `cites:` result counts and landing-page citation counts can differ
because of indexing/deduplication. Both are recorded when observed. Backward
checks used the primary paper's reference list and/or the OpenAlex
`referenced_works` list.

For the stopping rule, a **structural formulation category** means one of the
following kinds of mathematical coverage, not one of the five screening
labels: (i) direct multivariate isotope-profile discrimination, (ii)
network-induced MID-family construction or geometry, (iii) joint MID fitting
through a shared flux/network state, (iv) target-level inference under
parameter non-identification, (v) biological/technical measurement-error or
hierarchical modeling, or (vi) calibrated testing for already represented
probability families. Citation chaining was stopped only after it produced
papers within these six categories, or ordinary applications/estimation
papers, but no seventh structural category and no paper joining previously
separate coverage cells into the requested formulation. This is a bounded
category-stability rule, not evidence of literature saturation.

| ID | Anchor | Backward result count | Forward source/count | Outcome | Raw capture |
|---|---|---:|---:|---|---|
| P3-CITE-01 | Zamboni 2004, `W2101413453` | 41 OpenAlex references; 38 references represented in PMC full text | OpenAlex landing/filter 32/32 | direct profile discrimination and later applications only; no added structural category or joined coverage cell | `citation_checks/P3-CITE-ZAMBONI-*` |
| P3-CITE-02 | Schellenberger 2012, `W2120900694` | 38 PMC references | OpenAlex 34 | induced-family/design, joint fitting and flux-estimation papers; no added structural category or joined coverage cell | `citation_checks/P3-CITE-SCHELLENBERGER-*` |
| P3-CITE-03 | Cedersund 2012, `W1585358837` | 44 | OpenAlex landing/filter 93/91 | non-identification, prediction/profile-likelihood and applications; no isotope-induced-family combination | `citation_checks/P3-CITE-CEDERSUND-*` |
| P3-CITE-04 | Isermann 2003, `W2091963605` | 38 | OpenAlex 46 | identifiability, estimation and design; no direct class-test category | `citation_checks/P3-CITE-ISERMANN-*` |
| P3-CITE-05 | Sundqvist 2022, `W4223583835` | 54 | OpenAlex 13 | model validation, BMA and MFA extensions; no added structural category or joined coverage cell | `citation_checks/P3-CITE-P0030-*` |
| P3-CITE-06 | Crown 2015, `W1981299471` | 40 | OpenAlex 100 | parallel-MFA estimation/design/application extensions; no direct-test category | `citation_checks/P3-CITE-CROWN14-*` |
| P3-CITE-07 | Mairinger 2018, `W2797301123` | 41 | OpenAlex 15 | correction, analytical validation and Bayesian flux work; no hierarchy/class-test category | `citation_checks/P3-CITE-MAIRINGER-*` |
| P3-CITE-08 | Zhang 2023, `W4353061640` | 104 PMC references | OpenAlex 6 | shared-state likelihood, correction and Bayesian kinetic extensions; no added hierarchy or direct class-test category | `citation_checks/P3-CITE-ZHANG-*` |
| P3-CITE-09 | DIMet 2024, `W4395069938` | 25 PMC references | OpenAlex 3 | protocol and raw-processing extensions; application category unchanged | `citation_checks/P3-CITE-DIMET-*` |
| P3-CITE-10 | Weindl 2016, `W2337048129` | 75 PMC references | OpenAlex 43 | MIA/MIAMI and tracing workflows; application category unchanged | `citation_checks/P3-CITE-WEINDL-*` |
| P3-CITE-11 | Bleuler 2007, `W2056889431` | 15 | OpenAlex 0 | backward path returns to Zamboni/cluster methods | `citation_checks/P3-CITE-BLEULER-*` |
| P3-CITE-12 | Todem 2010, `W2036649935` | 26 | OpenAlex 11 | missing-data/sensitivity tests, no isotope construction | `citation_checks/P3-CITE-TODEM-*` |
| P3-CITE-13 | Andrews–Mikusheva 2016, `W2145246306` | 21 | OpenAlex landing/filter 59/58 | generic identification-robust inference; no isotope application category | `citation_checks/P3-CITE-ANDREWS-MIKUSHEVA-*` |
| P3-CITE-14 | MIAMI 2020, `W3020193235` | 15 references in PMC XML | OpenAlex 7 | IMPACT plus reviews/applications; no added structural category or joined coverage cell | `verification/P3-MIAMI-PMC7320603.xml`; `citation_checks/P3-CITE-MIAMI-forward.json` |
| P3-CITE-15 | IMPACT 2025, `W4416225799` | 19 references in PMC XML | OpenAlex 0 | direct isotope-processing and metabolomics-platform references only; no added structural category or joined coverage cell | `verification/P3-IMPACT-PMC12684724.xml`; `citation_checks/P3-CITE-IMPACT-forward.json` |

### Citation-neighbour occurrence adjudication

The raw forward sets preserve every provider occurrence. The table below
records a paper-level disposition for every occurrence that title/abstract
screening identified as capable of adding a structural category or joining
two existing coverage cells. `RETAINED_PHASE3` means a full-text Phase 3 row;
`EXISTING_EVIDENCE_DUPLICATE` means an already verified `P####`/`S####` row;
`NOT_RETAINED_NO_NEW_CATEGORY` means primary text or sufficient primary
metadata placed the paper wholly within an already represented category;
`DEFERRED_NOT_USED` means it was not allowed to support the stopping or gap
assessment. This is a category-stability appendix, not an exhaustive
eligibility ledger for every biological application in the raw payloads.

| OpenAlex ID | Anchor(s) | Paper / year | Phase 3B disposition | Evidence-bounded reason |
|---|---|---|---|---|
| `W2056889431` | Zamboni | Bleuler & Zitzler, 2007 | `RETAINED_PHASE3` (P3-0014) | full text: direct profile grouping, no sampling law or calibrated risk |
| `W3194711869` | Zamboni | Frahm et al., 2021, DOI `10.1016/j.talanta.2021.122812` | `NOT_RETAINED_NO_NEW_CATEGORY` | isotope-feature classification application; same direct-classification category as full-text P3-0013 |
| `W2019797668` | Zamboni | automated fluxome-profiling platform, 2014 | `NOT_RETAINED_NO_NEW_CATEGORY` | isotope-profile application/platform; no direct class-test law visible in primary metadata |
| `W3020193235` | Weindl | MIAMI, 2020 | `RETAINED_PHASE3` (P3-0022) | full text: raw GC-MS to thresholded MID/reference-network targets; contextualization is not latent-network coupling |
| `W2936632334` | Weindl; Mairinger | Schwaiger-Haber et al., 2019 | `NOT_RETAINED_NO_NEW_CATEGORY` | full text: standards, blanks and technical-replicate precision/trueness validation; no biological hierarchy or class test |
| `W4283027665` | Weindl | untargeted isotopic-data extraction optimisation, 2022 | `NOT_RETAINED_NO_NEW_CATEGORY` | primary target is analytical extraction optimisation, not inference over MID families |
| `W4416225799` | DIMet | IMPACT, 2025 | `RETAINED_PHASE3` (P3-0023) | full text: raw LC-MS to MIDs and similarity/reference networks; no shared-flux law, hierarchy or test |
| `W2564510448` | Schellenberger; Crown | stable-isotope network-validation dissertation, 2024 | `DEFERRED_NOT_USED` | dissertation abstract describes parallel-tracer applications and flux estimation; exact chapter-level validation rule was not used |
| `W1981299471` | Schellenberger | Crown et al., 2015 | `RETAINED_PHASE3` (P3-0004) | full text: shared-flux fit across 14 tracer datasets, not direct class testing |
| `W2128791609` | Schellenberger | integrated MFA/tandem-MS fragment inference, 2013 | `NOT_RETAINED_NO_NEW_CATEGORY` | measurement/fragment extension with flux-estimation target |
| `W4410287397` | Cedersund | Portela et al., 2025, conformal dynamic-system prediction | `NOT_RETAINED_NO_NEW_CATEGORY` | full primary text: IID conformal prediction coverage for ODE outputs, not hypothesis/class testing or isotope-family construction |
| `W4223583835` | Cedersund | Sundqvist et al., 2022 | `EXISTING_EVIDENCE_DUPLICATE` (P0030; P3-0003) | full text already checked; held-out tracer model selection after flux fitting |
| `W4383720928` | Cedersund | predictive power of non-identifiable models, 2023 | `NOT_RETAINED_NO_NEW_CATEGORY` | generic mechanistic prediction under parameter non-identification; Cedersund already represents that component |
| `W2172187648` | Cedersund | bootstrapped mechanistic-model rejection, 2014 | `NOT_RETAINED_NO_NEW_CATEGORY` | generic parametric-bootstrap model rejection, no isotope-induced family or uniform finite-sample guarantee |
| `W3174355401` | Isermann | Beyß et al., 2021 | `EXISTING_EVIDENCE_DUPLICATE` (P0009) | full text already checked: tracer design over sampled flux maps for flux information, not class error |
| `W2135394763` | Isermann; Crown | anaplerotic-reaction identifiability, 2015 | `NOT_RETAINED_NO_NEW_CATEGORY` | isotope flux-identifiability/application component already represented by P3-0006 |
| `W2037881978` | Isermann | isotope-labeling-network topology, 2007 | `NOT_RETAINED_NO_NEW_CATEGORY` | deterministic topology/decomposition, same forward-map category as P3-0008/P3-0020 |
| `W4402391572` | Zhang | BayesianSSA, 2024 | `NOT_RETAINED_NO_NEW_CATEGORY` | enzyme-perturbation prediction without MID observations or isotope forward law |
| `W1499117579` | Todem | weakly identifiable estimating-function tests, 2012 | `NOT_RETAINED_NO_NEW_CATEGORY` | generic identification-robust testing; no isotope construction |
| `W3126064887`; `W3092280141` | Andrews–Mikusheva | finite-sample/nominal-size IV inference, 2018/2020 | `DEFERRED_NOT_USED` | generic IV guarantees could refine generic theory but cannot construct the isotope pipeline; no guarantee attributed here |
| `W2409209783` | Crown | optimal tracers for parallel labeling, 2016 | `NOT_RETAINED_NO_NEW_CATEGORY` | tracer ranking for flux precision/synergy, not direct class testing |
| `W2958256899` | Crown | reversible-jump MFA, 2019 | `EXISTING_EVIDENCE_DUPLICATE` (P0031) | full text already checked: Bayesian structural-model/flux inference |
| `W4390404716` | Crown | Bayesian parallel-tracer MFA in granulocytes, 2024 | `DEFERRED_NOT_USED` | primary metadata supports parallel-MFA estimation only; no stronger guarantee is attributed |
| `W2951480779` | Crown | alternative kinetic steady states, 2019 | `NOT_RETAINED_NO_NEW_CATEGORY` | primary article/abstract concerns kinetic-model prediction under alternative flux/concentration states, not isotope observations or class testing |
| `W4414516522` | Crown | trans-dimensional nested sampling for MFA, 2025 | `NOT_RETAINED_NO_NEW_CATEGORY` | full primary report: synthetic `13C`-MFA model evidence and flux posterior; same Bayesian structural-inference category as P0031–P0032 |
| `W2937049592` | Mairinger | IsoCor, 2019 | `NOT_RETAINED_NO_NEW_CATEGORY` | isotope-correction software in the analytical-error category |
| `W4388562984` | Mairinger | BayFlux, 2023 | `EXISTING_EVIDENCE_DUPLICATE` (S0012) | verified software/paper supports downstream Bayesian flux inference, not a pipeline hierarchy or direct class test |

The remaining forward occurrences were applications, reviews, platform
descriptions or estimation/design papers within these same categories, or
unrelated records. Their titles, identifiers and available abstracts remain
in the anchor-specific raw JSON. They are not counted as paper-level
substantive exclusions and do not support an absence claim.

## Search limitations

- Broad OpenAlex and Crossref rankings are discovery windows, not exhaustive
  exports and not evidence of absence.
- Search terminology is unstable (`MID`, `MDV`, mass isotopomer,
  isotopologue, SIRM, fluxome profiling); citation chaining was therefore
  necessary.
- Some publisher supplements or records were inaccessible. Their failed or
  empty retrieval artifacts are named as such under
  `audit/phase3_raw_search_results/verification/` and are not substantive
  evidence.
- Secondary reviews oriented parallel-MFA and tracer terminology but were not
  used as sole support for any retained methodological claim.
