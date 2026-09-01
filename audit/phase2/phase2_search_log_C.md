# Phase 2A search log — Workstream C

Searcher: Codex Workstream C  
Execution date: 2026-07-31 UTC  
Scope: adjacent model-discrimination design, controlled sensing, composite
testing, converses, non-IID observations, nuisance parameters, and robust
testing. No Phase 1 provenance was reused. API result order and metadata are
preserved in `audit/phase2_raw_search_results/C/`.

All OpenAlex searches used `per-page=25` and no date filter. All Crossref
searches used `rows=25` and no date filter. Counts below are API records,
not database-wide hit counts. “New” means not a duplicate of an earlier
Workstream C record by canonical DOI or, when DOI was absent, normalized
title.

| ID | Source | Exact query | Results | New | Duplicates | Raw export |
|---|---|---|---:|---:|---:|---|
| PHASE2-SEARCH-0021 | OpenAlex | `T-optimal discriminating design robust model discrimination` | 25 | 25 | 0 | `PHASE2-SEARCH-0021_openalex.json` |
| PHASE2-SEARCH-0022 | Crossref | `KL optimal model discrimination experimental design` | 25 | 25 | 0 | `PHASE2-SEARCH-0022_crossref.json` |
| PHASE2-SEARCH-0023 | OpenAlex | `maximin robust model discrimination experimental design` | 25 | 23 | 2 | `PHASE2-SEARCH-0023_openalex.json` |
| PHASE2-SEARCH-0024 | Crossref | `Bayesian optimal design model discrimination` | 25 | 13 | 12 | `PHASE2-SEARCH-0024_crossref.json` |
| PHASE2-SEARCH-0025 | OpenAlex | `finite sample composite hypothesis testing minimax lower bound` | 25 | 25 | 0 | `PHASE2-SEARCH-0025_openalex.json` |
| PHASE2-SEARCH-0026 | Crossref | `active hypothesis testing composite hypotheses controlled sensing` | 25 | 25 | 0 | `PHASE2-SEARCH-0026_crossref.json` |
| PHASE2-SEARCH-0027 | OpenAlex | `sequential controlled sensing composite multihypothesis testing` | 25 | 24 | 1 | `PHASE2-SEARCH-0027_openalex.json` |
| PHASE2-SEARCH-0028 | Crossref | `Chernoff sequential design experiments composite hypothesis` | 25 | 25 | 0 | `PHASE2-SEARCH-0028_crossref.json` |
| PHASE2-SEARCH-0029 | OpenAlex | `non iid experimental design hypothesis testing heterogeneous observations` | 25 | 24 | 1 | `PHASE2-SEARCH-0029_openalex.json` |
| PHASE2-SEARCH-0030 | Crossref | `shared nuisance parameters model discrimination experimental design` | 25 | 21 | 4 | `PHASE2-SEARCH-0030_crossref.json` |
| PHASE2-SEARCH-0031 | OpenAlex | `overlapping nonnested models likelihood ratio test Vuong` | 25 | 25 | 0 | `PHASE2-SEARCH-0031_openalex.json` |
| PHASE2-SEARCH-0032 | Crossref | `robust hypothesis testing contamination neighborhoods minimax` | 25 | 24 | 1 | `PHASE2-SEARCH-0032_crossref.json` |
| PHASE2-SEARCH-0033 | OpenAlex | `distributionally robust hypothesis testing model uncertainty finite sample` | 25 | 25 | 0 | `PHASE2-SEARCH-0033_openalex.json` |
| PHASE2-SEARCH-0034 | Crossref | `best arm identification fixed confidence lower bound sample complexity` | 25 | 25 | 0 | `PHASE2-SEARCH-0034_crossref.json` |
| PHASE2-SEARCH-0035 | OpenAlex | `optimal experimental design model discrimination common parameters nuisance` | 25 | 24 | 1 | `PHASE2-SEARCH-0035_openalex.json` |

Supplementary primary-source discovery within PHASE2-SEARCH-0024 identified
Dette, Melas and Guchenko (2015) on PMC; its complete BioC XML is preserved as
`PMC4793413_fulltext.xml`. Supplementary discovery within
PHASE2-SEARCH-0034 identified Garivier and Kaufmann (2016); the official PMLR
landing page is preserved as
`PHASE2-SEARCH-0034_pmlr_supplementary.html`. These records are separately
identified in the screening ledger and are not represented as Crossref hits.

## Deduplication and screening outcome

- API records: 375.
- Supplementary records: 2.
- Total prospective records: 377.
- Duplicate records: 22.
- Full-text included: 6.
- Title/abstract included for discovery or later verification: 71.
- Title/abstract excluded with a recorded reason: 278.

## Corrected search-family assessment

| Family | Assessment | Evidence |
|---|---|---|
| Classical T/KL/Bayesian discrimination design | `ANCHOR_FAMILIES_VERIFIED` | OpenAlex and Crossref searches recovered established T, KL, Bayesian and robust/maximin families. Backward references in the inspected full texts support the Atkinson–Fedorov/T/KL lineage already present in Phase 1. The bounded windows do not establish exhaustiveness. |
| Active testing and controlled sensing | `ANCHOR_FAMILIES_VERIFIED` | Crossref and OpenAlex recovered controlled sensing, Chernoff/sequential design and composite sequential testing. The verified P0026–P0028 results retain their finite-simple or disjoint-exponential-family assumptions. |
| Fixed-confidence sample complexity | `ANCHOR_FAMILIES_VERIFIED` | PHASE2-SEARCH-0034 plus the official PMLR paper established a nonasymptotic converse, exact risk control for a stopping rule, and asymptotic sample-complexity optimality for its stated subfamily. It does not establish transfer to continuous overlapping EMU mechanism classes. |
| Non-IID/shared nuisance/overlap | `INCOMPLETELY_SEARCHED` | PHASE2-SEARCH-0029, 0030, 0031 and 0035 were noisy. Vuong-type nonnested testing addresses overlap asymptotically, while fixed-sample designed non-IID results with shared EMU nuisance remain deferred or unverified. |
| Distributional robustness/misspecification | `INCOMPLETELY_SEARCHED` | PHASE2-SEARCH-0032 recovered a load-bearing minimax robust testing paper. The verified result assumes dominated binary uncertainty classes and does not jointly optimise EMU experiments; the bounded search does not establish that no other family exists. |

## Bounded closure: PHASE2-SEARCH-0061–0068

Executed prospectively on 2026-07-31 after the initial assessment identified
two incompletely searched families. Crossref returned poorly ranked results when the
generic `query` parameter was used for 0062, 0064 and 0066, so a single
bounded retry used `query.bibliographic` plus a metadata `select`. Both
responses are preserved; retry records are deduplicated rather than hidden.

| ID | Source / route | Exact query or anchor operation | Raw records |
|---|---|---|---:|
| PHASE2-SEARCH-0061 | OpenAlex | `independent non identically distributed composite hypothesis testing error exponent` | 25 |
| PHASE2-SEARCH-0062 | Crossref | `query=independent non identically distributed composite hypothesis testing error exponent`; bounded retry: `query.bibliographic=independent non-identically distributed composite hypothesis testing error exponent` | 25 + 25 |
| PHASE2-SEARCH-0063 | OpenAlex | `shared nuisance parameters multiple experiments composite hypothesis testing` | 25 |
| PHASE2-SEARCH-0064 | Crossref | `query=overlapping composite hypotheses common nuisance parameters nonnested likelihood test`; bounded retry: same text in `query.bibliographic` | 25 + 25 |
| PHASE2-SEARCH-0065 | OpenAlex | `distributionally robust hypothesis testing Wasserstein f divergence finite sample` | 25 |
| PHASE2-SEARCH-0066 | Crossref | `query=distributionally robust hypothesis testing Wasserstein ambiguity finite sample minimax`; bounded retry: same text in `query.bibliographic` | 25 + 25 |
| PHASE2-SEARCH-0067 | OpenAlex citation network | DOI anchor `10.1080/07474946.2021.1912525`; retrieve anchor, 28 referenced works, and works with `cites:W2982216380` | 1 anchor; 27 resolved backward; 5 forward |
| PHASE2-SEARCH-0068 | OpenAlex citation network | DOI anchor `10.1109/TIT.2017.2693198`; retrieve anchor, 24 referenced works, and works with `cites:W1585342122` | 1 anchor; 23 resolved backward; 1 forward |

The closure added 281 raw API result rows and two explicit anchor-verification
rows to the prospective ledger. Across the complete Workstream C ledger:

- Prospective records: 660.
- Duplicates: 104.
- Full-text included: 8.
- Title/abstract included for discovery or later verification: 122.
- Title/abstract excluded with a recorded reason: 426.

### Closure decision

| Precise family | Closure decision | Reason |
|---|---|---|
| Heterogeneous studies with prospective Type-I control | `ANCHOR_FAMILIES_VERIFIED` | Grünwald, de Heide and Koolen (2024), Proposition 1, Proposition 2 and Corollary 1 give finite-sample Type-I control for products of conditionally valid e-variables over adaptively continued, potentially differently constructed study batches. |
| Shared nuisance parameters | `INCOMPLETELY_SEARCHED` | The same paper gives general composite-null constructions and a full Theorem 1 including nuisance handled through coarsening/group invariance. It does not show that arbitrary EMU shared-nuisance families meet the information-projection/existence conditions, nor give uniform Type-II/sample-size guarantees. |
| Exactly overlapping induced hypothesis families | `ANCHOR_FAMILIES_VERIFIED` | If the same observation law lies in both mechanism classes, any level-`alpha` test has power at most `alpha` at that shared law. This positive obstruction transfers directly; quantitative near-overlap over the full EMU design set remains computationally unresolved. |
| Dominated binary distributional-neighbourhood testing | `ANCHOR_FAMILIES_VERIFIED` | Levy (2009) and Gül–Zoubir (2017) verify KL, contamination, composite-distance, least-favourable-distribution and saddle-point methods at their recorded strength. |
| Joint distributionally robust EMU experiment design | `INCOMPLETELY_SEARCHED` | The verified records do not supply the registered conjunction of a nonlinear EMU design map, structural composite alternatives, ambiguity over forward/noise laws, finite-sample two-error guarantees and a converse. Deferred records prevent an absence inference. |

## Restored-backup audit closure: PHASE2-SEARCH-0080–0083

Executed prospectively on 2026-07-31 after restoration. These searches test
the two residual stopping rules after C-LB06 and C-LB07 became load-bearing.
No date filters were used. OpenAlex used `per-page=25`; Crossref used
`rows=25`, `query.bibliographic`, and the metadata `select` recorded in the
raw request response.

| ID | Source | Exact query | Results | New load-bearing method |
|---|---|---|---:|---|
| PHASE2-SEARCH-0080 | OpenAlex | `e-values composite hypothesis nuisance experimental design power sample size` | 25 | none |
| PHASE2-SEARCH-0081 | Crossref | `e-values composite hypothesis nuisance experimental design power sample size` | 25 | none |
| PHASE2-SEARCH-0082 | OpenAlex | `distributionally robust experiment design hypothesis testing least favorable structural model` | 25 | none |
| PHASE2-SEARCH-0083 | Crossref | `distributionally robust experiment design hypothesis testing least favorable structural model` | 25 | none |

Within their exported windows, the first distinct-source pair added no
method beyond C-LB06's conditional e-value/composite-nuisance family, and the
second added no method beyond the C-LB04/C-LB07 dominated
least-favourable-distribution family. Together with the bounded backward and
forward networks in PHASE2-SEARCH-0067–0068, these operations are
`BOUNDED_SEARCH_COMPLETE`. They do not establish exhaustive coverage or that
the joint EMU formulation is absent.

Current prospective Workstream C ledger:

- Records: 760.
- `FULL_TEXT_INCLUDED`: 8.
- `TITLE_ABSTRACT_INCLUDED`: 124.
- `TITLE_ABSTRACT_EXCLUDED`: 501.
- `DUPLICATE`: 127.
- Prospective exclusions without a reason: 0.

Final corrected search-closure statement:

- T/KL/Bayesian, robust/maximin, active-testing, controlled-sensing,
  fixed-confidence-converse, conditional-e-value, and dominated
  distributional-neighbourhood anchor families are
  `ANCHOR_FAMILIES_VERIFIED` at the strength of the inspected papers.
- The exported result and citation windows do not establish exhaustive
  coverage of those families.
- Uniform Type-II/sample-size certification for overlapping continuous EMU
  structural classes with shared nuisance, and joint distributionally robust
  EMU experiment design, remain `INCOMPLETELY_SEARCHED`; deferred evidence
  cannot support an absence claim.
