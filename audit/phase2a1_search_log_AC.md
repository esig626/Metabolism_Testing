# Phase 2A.1 search log — workstream AC

Date: 2026-07-31 UTC

Searcher: Codex subagent `/root/phase2a1_foundations_ac`

Scope: query families A–C only (testing between sets, Le Cam/Birgé/Hellinger
families, and Fano/Assouad/packing converses), plus bounded citation closure.

This is a prospective Phase 2A.1 log. It does not modify or reinterpret Phase
1 provenance. Counts below distinguish the database-reported universe from the
bounded result window actually exported and screened. Very large Crossref
totals reflect its broad relevance ranking; only the preserved returned window
is a screening occurrence.

## Query-family A — testing between sets of distributions

| ID | Source | Exact query or operation | Filters / ordering | Source total | Exported |
|---|---|---|---|---:|---:|
| PHASE2A1-SEARCH-0001 | OpenAlex | `fixed-sample composite hypothesis testing nonasymptotic` | `per-page=15`; default relevance | 358 | 15 |
| PHASE2A1-SEARCH-0002 | Crossref | `fixed-sample composite hypothesis testing nonasymptotic` | `query.bibliographic`; `rows=15` | 1,535,092 | 15 |
| PHASE2A1-SEARCH-0003 | OpenAlex | `testing between convex sets of distributions minimax hypothesis test` | `per-page=15`; default relevance | 4,988 | 15 |
| PHASE2A1-SEARCH-0004 | Crossref | `testing between convex sets of distributions minimax hypothesis test` | `query.bibliographic`; `rows=15` | 3,993,493 | 15 |
| PHASE2A1-SEARCH-0005 | OpenAlex | `minimax robust hypothesis testing distribution uncertainty finite sample` | `per-page=15`; default relevance | 2,631 | 15 |
| PHASE2A1-SEARCH-0006 | Crossref | `minimax robust hypothesis testing distribution uncertainty finite sample` | `query.bibliographic`; `rows=15` | 2,606,888 | 15 |

Raw exports are the correspondingly numbered JSON files under
`audit/phase2a1_raw_search_results/AC/`.

## Query-family B — Le Cam, Birgé, Hellinger and metric separation

| ID | Source | Exact query or operation | Filters / ordering | Source total | Exported |
|---|---|---|---|---:|---:|
| PHASE2A1-SEARCH-0007 | OpenAlex | `Le Cam test composite hypotheses Hellinger distance finite sample` | `per-page=15`; default relevance | 34 | 15 |
| PHASE2A1-SEARCH-0008 | Crossref | `Le Cam test composite hypotheses Hellinger distance finite sample` | `query.bibliographic`; `rows=15` | 3,329,700 | 15 |
| PHASE2A1-SEARCH-0009 | OpenAlex | `Birge tests metric balls Hellinger robust test` | `per-page=15`; default relevance | 4 | 4 |
| PHASE2A1-SEARCH-0010 | Crossref | `Birge tests metric balls Hellinger robust test` | `query.bibliographic`; `rows=15` | 1,374,627 | 15 |
| PHASE2A1-SEARCH-0011 | OpenAlex | `hypothesis testing metric entropy separated classes nonasymptotic` | `per-page=15`; default relevance | 320 | 15 |
| PHASE2A1-SEARCH-0012 | Crossref | `hypothesis testing metric entropy separated classes nonasymptotic` | `query.bibliographic`; `rows=15` | 1,008,145 | 15 |

The OpenAlex Birgé query returned only four records. Crossref's much larger
reported total was poorly specific; the preserved top 15 were screened rather
than treating the reported universe as reviewed.

## Query-family C — Fano, Assouad, packing and finite-sample lower bounds

| ID | Source | Exact query or operation | Filters / ordering | Source total | Exported |
|---|---|---|---|---:|---:|
| PHASE2A1-SEARCH-0013 | OpenAlex | `Fano inequality Assouad lemma Le Cam minimax lower bound hypothesis testing` | `per-page=15`; default relevance | 158 | 15 |
| PHASE2A1-SEARCH-0014 | Crossref | `Fano inequality Assouad lemma Le Cam minimax lower bound hypothesis testing` | `query.bibliographic`; `rows=15` | 25,886 | 15 |
| PHASE2A1-SEARCH-0015 | OpenAlex | `sample complexity converse composite hypothesis testing packing lower bound` | `per-page=15`; default relevance | 525 | 15 |
| PHASE2A1-SEARCH-0016 | Crossref | `sample complexity converse composite hypothesis testing packing lower bound` | `query.bibliographic`; `rows=15` | 2,050,772 | 15 |

During primary-source verification for PHASE2A1-SEARCH-0013, an exact DOI
lookup recovered Guntuboyina (2011), DOI
`10.1109/TIT.2011.2110791`. The authoritative OpenAlex metadata snapshot and
the complete arXiv source (`1002.0042`) are preserved. This extra verification
record is explicitly labelled as such in the screening ledger and is not
presented as a hit in the original 15-result OpenAlex window.

## First citation-closure pass — Goldenshluger, Juditsky and Nemirovski

| ID | Source | Exact query or operation | Filters / ordering | Source total | Exported |
|---|---|---|---|---:|---:|
| PHASE2A1-SEARCH-0017 | OpenAlex | `"Hypothesis testing by convex optimization" Goldenshluger Juditsky Nemirovski` | `per-page=25`; default relevance | 11 | 11 |
| PHASE2A1-SEARCH-0018 | OpenAlex | works citing `W1742114735` | `filter=cites:W1742114735`; `sort=cited_by_count:desc`; `per-page=25` | 24 | 24 |
| PHASE2A1-SEARCH-0019 | OpenAlex | references in `W1742114735` | seed's 55 `referenced_works`; batch metadata | 55 references | 55 occurrences (52 metadata records; 3 retired IDs) |

The three retired OpenAlex IDs were individually checked once and returned
HTTP 404. They remain final `FULL_TEXT_UNAVAILABLE` occurrences with no inferred
bibliographic fields. This pass added the affine-detector and Euclidean-
separation constructive families but no method family outside the registered
A–C scope.

## Second citation-closure pass — Guntuboyina and Birgé

| ID | Source | Exact query or operation | Filters / ordering | Source total | Exported |
|---|---|---|---|---:|---:|
| PHASE2A1-SEARCH-0064 | OpenAlex | works citing `W2101210333` (Guntuboyina 2011) | `filter=cites:W2101210333`; `sort=cited_by_count:desc`; `per-page=25` | 96 | 25 |
| PHASE2A1-SEARCH-0065 | OpenAlex | references in `W2101210333` | seed's 28 `referenced_works`; batch metadata | 28 references | 28 occurrences (27 metadata records; 1 retired ID) |
| PHASE2A1-SEARCH-0066 | OpenAlex | `Tests robustes pour des variables independantes et des chaines de Markov Birge` | `per-page=10`; default relevance | 0 | 0 |
| PHASE2A1-SEARCH-0067 | Semantic Scholar | `Tests robustes pour des variables indépendantes et des chaînes de Markov` | `limit=10`; default relevance | 880 | 10 |
| PHASE2A1-SEARCH-0068 | Semantic Scholar | `"Robust Testing for Independent Non Identically Distributed Variables and Markov Chains"` | `limit=10`; default relevance | unavailable (HTTP 429) | 0 |
| PHASE2A1-SEARCH-0069 | Crossref | `Robust Testing for Independent Non Identically Distributed Variables and Markov Chains Lucien Birge` | `query.bibliographic`; `rows=20` | 66,447 | 20 |
| PHASE2A1-SEARCH-0070 | OpenAlex | exact DOI lookup `10.1007/978-1-4612-5503-1_9` | single-work endpoint | 1 | 1 |
| PHASE2A1-SEARCH-0071 | OpenAlex | works citing `W171842306` (Birgé 1983 English chapter) | `filter=cites:W171842306`; `sort=cited_by_count:desc`; `per-page=25` | 21 | 21 |
| PHASE2A1-SEARCH-0072 | OpenAlex | references in `W171842306` | seed's 18 `referenced_works`; batch metadata | 18 references | 18 |
| PHASE2A1-SEARCH-0073 | Numdam | official identifier `ASCFM_1982__71_20_70_0` | official metadata page and legal PDF | 1 | 1 |

PHASE2A1-SEARCH-0068 was not retried after the first rate-limit response. Its
structured failure snapshot is preserved. PHASE2A1-SEARCH-0067 was retained
because it is a real executed query, but its ten results were unrelated
false positives. Crossref and the exact DOI lookup established the indexed
English chapter; Numdam supplied the legally accessible French primary
article. The Guntuboyina and Birgé forward/backward passes returned familiar
Fano/Birgé/Le Cam, convex-testing, posterior-contraction and asymptotic
families but no additional load-bearing fixed-sample method family.

## Primary full-text retrievals

All retrievals were legal author manuscripts, arXiv source packages, official
publisher/repository files, or official metadata. Complete inspected sources
are preserved for:

- Comminges and Dalalyan (2013), arXiv `1208.1823`;
- Goldenshluger, Juditsky and Nemirovski (2015), arXiv `1311.6765`;
- Addario-Berry et al. (2010), arXiv `0908.3437`;
- Guntuboyina (2011), arXiv `1002.0042`;
- Juditsky and Nemirovski (2016), arXiv `1604.02576`;
- Guigues, Juditsky and Nemirovski (2020), arXiv `1705.07196`;
- Wei, Wainwright and Guntuboyina (2019), arXiv `1703.06810`;
- Venkataramanan and Johnson (2018), arXiv `1706.04410`;
- Birgé (1982), official Numdam PDF.

Official Project Euclid attempts for Huber and Strassen (1973) returned access
denial pages. The official Springer record for Birgé's 1983 English chapter is
subscription-only. Those versions were not repeatedly retried and do not carry
theorem-level coding.

## Disposition accounting

The separate AC ledger contains 444 prospective occurrences:

- `FULL_TEXT_INCLUDED`: 9;
- `FULL_TEXT_UNAVAILABLE`: 27;
- `DUPLICATE`: 66;
- `FALSE_POSITIVE`: 342.

There are 380 deduplicated bibliographic groups. Two first occurrences are
duplicates of existing corpus records (P0041 and P0043); 64 further
occurrences repeat an AC bibliographic group. All occurrences have a final
disposition. No title/abstract-included state remains in this workstream.

## Controlling interpretation correction

The earlier phrase “no additional load-bearing fixed-sample method family”
describes only the bounded, relevance-ranked result windows and citation
records actually inspected in this workstream. It is not evidence that no
additional family exists. The database result windows and citation passes
were truncated, `PHASE2A1-SEARCH-0068` was not retried after HTTP 429, and
some primary texts remained unavailable. The controlling family states are
therefore `ANCHOR_FAMILIES_VERIFIED` in
`audit/phase2_saturation_log.md`, not an exhaustive-coverage state.
