# Phase 2A.1 search log — workstreams D–F

Searcher: Codex subagent `/root/phase2a1_foundations_def`  
Execution date: 2026-07-31 UTC  
Scope: nuisance-parameter/fixed-design testing (D), nonparametric and
high-dimensional minimax testing (E), and fixed-sample/fixed-budget
information-theoretic converses (F). No Phase 1 search provenance was changed.

The API searches below used no date, language, publication-type, or
open-access filter. Crossref used `rows=15`; OpenAlex used `per-page=15`,
relevance order. Raw responses are preserved under
`audit/phase2a1_raw_search_results/DEF/`. Counts are source occurrences, not
unique papers. All 515 occurrences, including citation-pass occurrences, have
a final prospective disposition in `audit/phase2a1_screening_DEF.csv`.

## Direct searches

| Search ID | Family | Source | Exact query | API limit | Returned occurrences | Raw export |
|---|---|---|---|---:|---:|---|
| PHASE2A1-SEARCH-0021 | D | Crossref | `composite hypothesis testing nuisance parameter fixed sample finite sample` | 15 | 15 | `PHASE2A1-SEARCH-0021_crossref.json` |
| PHASE2A1-SEARCH-0022 | D | OpenAlex | `composite hypothesis testing nuisance parameter fixed sample finite sample` | 15 | 15 | `PHASE2A1-SEARCH-0022_openalex.json` |
| PHASE2A1-SEARCH-0023 | D | Crossref | `independent non-identically distributed composite hypothesis testing fixed design` | 15 | 15 | `PHASE2A1-SEARCH-0023_crossref.json` |
| PHASE2A1-SEARCH-0024 | D | OpenAlex | `independent non-identically distributed composite hypothesis testing fixed design` | 15 | 15 | `PHASE2A1-SEARCH-0024_openalex.json` |
| PHASE2A1-SEARCH-0025 | D | Crossref | `exact finite sample test nuisance parameter confidence set maximized p value` | 15 | 15 | `PHASE2A1-SEARCH-0025_crossref.json` |
| PHASE2A1-SEARCH-0026 | D | OpenAlex | `exact finite sample test nuisance parameter confidence set maximized p value` | 15 | 15 | `PHASE2A1-SEARCH-0026_openalex.json` |
| PHASE2A1-SEARCH-0027 | E | Crossref | `nonasymptotic minimax hypothesis testing nonparametric separation rate` | 15 | 15 | `PHASE2A1-SEARCH-0027_crossref.json` |
| PHASE2A1-SEARCH-0028 | E | OpenAlex | `nonasymptotic minimax hypothesis testing nonparametric separation rate` | 15 | 15 | `PHASE2A1-SEARCH-0028_openalex.json` |
| PHASE2A1-SEARCH-0029 | E | Crossref | `high dimensional hypothesis testing minimax lower bound finite sample` | 15 | 15 | `PHASE2A1-SEARCH-0029_crossref.json` |
| PHASE2A1-SEARCH-0030 | E | OpenAlex | `high dimensional hypothesis testing minimax lower bound finite sample` | 15 | 15 | `PHASE2A1-SEARCH-0030_openalex.json` |
| PHASE2A1-SEARCH-0031 | E | Crossref | `metric entropy composite hypothesis testing finite sample` | 15 | 15 | `PHASE2A1-SEARCH-0031_crossref.json` |
| PHASE2A1-SEARCH-0032 | E | OpenAlex | `metric entropy composite hypothesis testing finite sample` | 15 | 15 | `PHASE2A1-SEARCH-0032_openalex.json` |
| PHASE2A1-SEARCH-0033 | F | Crossref | `finite blocklength composite hypothesis testing converse` | 15 | 15 | `PHASE2A1-SEARCH-0033_crossref.json` |
| PHASE2A1-SEARCH-0034 | F | OpenAlex | `finite blocklength composite hypothesis testing converse` | 15 | 15 | `PHASE2A1-SEARCH-0034_openalex.json` |
| PHASE2A1-SEARCH-0035 | F | Crossref | `fixed budget hypothesis testing controlled sensing nonadaptive sample complexity` | 15 | 15 | `PHASE2A1-SEARCH-0035_crossref.json` |
| PHASE2A1-SEARCH-0036 | F | OpenAlex | `fixed budget hypothesis testing controlled sensing nonadaptive sample complexity` | 15 | 15 | `PHASE2A1-SEARCH-0036_openalex.json` |

## Bounded anchor and citation passes

### PHASE2A1-SEARCH-0037 — D and robust-composite anchors

- OpenAlex anchor lookup, backward-reference resolution, and forward-citation
  retrieval for Berger and Boos (1994), OpenAlex `W2055708265`; backward
  references were bounded to 21 resolvable records and forward citations to
  the first 25 of 318.
- The same pass for Dufour (2006), OpenAlex `W2149862193`; backward and
  forward records were bounded to 25 each (80 references and 264 citations
  reported by OpenAlex).
- Targeted Crossref metadata/access passes for Gül and Zoubir's minimax and
  alpha-divergence papers; official author, PMLR, proceedings, arXiv,
  publisher, and repository access checks for the full texts named in the
  screening ledger.
- Bounded publisher/repository access checks for Wefelmeyer (1987) and
  Bernshtein (1981). Full texts remained unavailable.
- Total ledger occurrences: 104. Raw exports and retrieved primary
  manuscripts have the `PHASE2A1-SEARCH-0037_` prefix.

### PHASE2A1-SEARCH-0038 — E anchors

- OpenAlex anchor lookup, backward-reference resolution, and forward-citation
  retrieval for Baraud (2002), OpenAlex `W1591122161`; all 13 resolvable
  references and the first 25 of 152 citations were requested.
- The same pass for Laurent, Loubès and Marteau (2012), OpenAlex
  `W2060233947`; all 24 references and the first 25 of 35 citations were
  requested.
- Targeted Crossref/official-repository access for Comminges and Dalalyan
  (2013), Baraud, Huet and Laurent (2003), Balakrishnan and Wasserman (2019),
  and the two primary anchors.
- Total ledger occurrences: 88. Raw exports and retrieved primary manuscripts
  have the `PHASE2A1-SEARCH-0038_` prefix.

### PHASE2A1-SEARCH-0039 — F anchors

- OpenAlex anchor lookup, backward-reference resolution, and forward-citation
  retrieval for Polyanskiy, Poor and Verdú (2010), OpenAlex `W2106864314`;
  reference and citation results were bounded to 25 each (57 references and
  3,885 citations reported).
- The same pass for Venkataramanan and Johnson (2018), OpenAlex
  `W2790620458`; 25 of 38 references and all five reported citations were
  requested.
- An official institutional-repository access check for the 2024 POMDP
  fixed-budget paper retrieved metadata but no accessible primary full text.
- Total ledger occurrences: 83. Raw exports and retrieved primary manuscripts
  have the `PHASE2A1-SEARCH-0039_` prefix.

## Closure assessment

- Exact nuisance-parameter Type-I control has two-source discovery plus
  verified primary anchors (Berger–Boos, Dufour, Universal Inference).
- Structured nonasymptotic minimax testing has two-source discovery and
  verified constructive and converse anchors (Baraud; Laurent et al.;
  Baraud–Huet–Laurent; Balakrishnan–Wasserman).
- Finite-message/fixed-block converse machinery has two-source discovery and
  verified primary anchors (Polyanskiy et al.; Venkataramanan–Johnson).
- The D–F workstream as a whole is **NOT SATURATED**: the primary texts for
  Birgé's robust independent-nonidentical/Markov result, Wefelmeyer's
  heterogeneous-observation result, Bernshtein's multivariate
  composite/nuisance result, and the 2024 POMDP fixed-budget result were
  unavailable. These papers cannot support either a definitive claim or an
  absence conclusion.
