# Phase 2A Workstream A Search Log

Searcher: Codex Workstream A. Execution date: 2026-07-31 UTC. These are
prospective Phase 2 searches and are not merged with Phase 1 provenance.
API snapshots preserve the returned result sets in
`audit/phase2_raw_search_results/A/`. OpenAlex and Crossref counts are total
API matches; screening was limited to the explicitly returned page. No date
or language filter was applied.

| ID | Source | Exact query / route | Returned / total | Included after occurrence-level screening | Raw snapshot |
|---|---|---|---:|---:|---|
| PHASE2-SEARCH-0001 | PubMed ESearch | `(13C metabolic flux analysis[Title/Abstract] OR 13C-MFA[Title/Abstract]) AND (tracer selection[Title/Abstract] OR optimal tracer[Title/Abstract] OR experimental design[Title/Abstract])` | 9 / 9 | 6 | `PHASE2-SEARCH-0001_pubmed_esearch.json`; metadata in `pubmed_esummary_union.json` |
| PHASE2-SEARCH-0002 | OpenAlex works search | `13C metabolic flux analysis tracer selection optimal experimental design`; `per-page=25` | 25 / 635 | 5 | `PHASE2-SEARCH-0002_openalex.json` |
| PHASE2-SEARCH-0003 | PubMed ESearch | `(13C metabolic flux analysis[Title/Abstract] OR isotope tracing[Title/Abstract]) AND (measurement selection[Title/Abstract] OR fragment selection[Title/Abstract] OR metabolite selection[Title/Abstract])` | 1 / 1 | 0 (duplicate) | `PHASE2-SEARCH-0003_pubmed_esearch.json`; metadata in `pubmed_esummary_union.json` |
| PHASE2-SEARCH-0004 | OpenAlex works search | `parallel tracer experiments multi experiment 13C metabolic flux analysis`; `per-page=25` | 25 / 820 | 2 | `PHASE2-SEARCH-0004_openalex.json` |
| PHASE2-SEARCH-0005 | PubMed ESearch | `(13C-MFA[Title/Abstract] OR 13C metabolic flux analysis[Title/Abstract]) AND (robust tracer[Title/Abstract] OR robust experimental design[Title/Abstract] OR uncertain flux[Title/Abstract])` | 6 / 6 | 1 | `PHASE2-SEARCH-0005_pubmed_esearch.json`; metadata in `pubmed_esummary_union.json` |
| PHASE2-SEARCH-0006 | Crossref works | `query.bibliographic=13C metabolic flux analysis sample size replicate allocation power design`; `rows=25` | 25 / 521766 | 4 | `PHASE2-SEARCH-0006_crossref.json` |
| PHASE2-SEARCH-0007 | PubMed ESearch | `(isotopically nonstationary metabolic flux analysis[Title/Abstract] OR INST-MFA[Title/Abstract]) AND (experimental design[Title/Abstract] OR time point[Title/Abstract] OR sampling[Title/Abstract] OR identifiability[Title/Abstract])` | 3 / 3 | 0 | `PHASE2-SEARCH-0007_pubmed_esearch.json`; metadata in `pubmed_esummary_union.json` |
| PHASE2-SEARCH-0008 | OpenAlex works search | `metabolic flux analysis perturbation selection identifiability isotope`; `per-page=25` | 25 / 314 | 0 | `PHASE2-SEARCH-0008_openalex.json` |
| PHASE2-SEARCH-0009 | OpenAlex forward-citation search | `filter=cites:W2076863223`, where `W2076863223` is the OpenAlex work for the EMU-basis anchor DOI `10.1016/j.ymben.2011.12.005`; `per-page=50` | 50 / 77 | 11 | `PHASE2-SEARCH-0009_openalex_forward_citations.json` |
| PHASE2-SEARCH-0010 | Crossref works | `query.bibliographic=13C metabolic flux analysis D-optimal A-optimal E-optimal tracer design`; `rows=25` | 25 / 9637398 | 1 | `PHASE2-SEARCH-0010_crossref.json` |

## Deduplication and disposition

The ten snapshots contain 194 result occurrences representing 160 deduplicated
record groups. Thirty-four later/supplemental occurrences are marked
`DUPLICATE`. Five occurrences were full-text included, 25 were
title/abstract included as supporting or discovery leads, and 130 were
prospectively excluded with an explicit reason.
The apparent extreme total counts in the Crossref searches reflect permissive
bibliographic ranking; only the preserved first 25 results were discovered
and screened here.

The forward-citation seed in PHASE2-SEARCH-0009 is Crown and Antoniewicz's
EMU-basis tracer-selection paper, DOI `10.1016/j.ymben.2011.12.005`.

## Search-family stopping assessment

This workstream is **not independently declared saturated**. The bounded
queries and correct-anchor forward pass recovered all pilot
experimental-design families and added no
direct 13C-MFA method that optimises calibrated mechanism-discrimination
error, prospective power, or biological replicate allocation. However,
Crossref ranking was noisy, the dynamic-design search retrieved only
secondary/protocol material, and a documented backward-reference pass remains
appropriate in the integrated Phase 2 saturation audit. No absence inference
is made from these negative searches.

## Bounded closure pass

Executed prospectively on 2026-07-31 UTC after the initial workstream.

| ID | Source | Exact query / route | Returned / total | Outcome | Raw snapshot |
|---|---|---|---:|---|---|
| PHASE2-SEARCH-0056 | Primary full-text reference lists | Bounded backward-reference extraction from doi:10.1016/j.ymben.2011.12.005, doi:10.1186/1752-0509-6-43, doi:10.1016/j.ymben.2011.12.004, doi:10.1371/journal.pcbi.1006533, doi:10.1016/j.ymben.2016.06.001 and doi:10.3389/fbioe.2021.685323 | 251 reference occurrences | No new experimental-design method family; known isotopomer/FIM, dynamic design, EMU, parallel and robust design precursors recovered | `PHASE2-SEARCH-0056_backward_references.json` |
| PHASE2-SEARCH-0057 | PubMed ESearch | `(13C[Title/Abstract] OR isotope[Title/Abstract]) AND (metabolic flux analysis[Title/Abstract]) AND (dynamic experimental design[Title/Abstract] OR optimal sampling[Title/Abstract] OR sampling time[Title/Abstract] OR time point selection[Title/Abstract] OR instationary experimental design[Title/Abstract])` | 3 / 3 | The 2006 Nöh–Wiechert design paper remains full-text unavailable; two closely related methods recovered | `PHASE2-SEARCH-0057_pubmed_dynamic_design.json`; metadata in `PHASE2-SEARCH-0057_pubmed_esummary.json` |
| PHASE2-SEARCH-0058 | OpenAlex works search | `isotopically nonstationary metabolic flux analysis experimental design sampling times`; `per-page=25` | 25 / 235 | No new directly relevant design family | `PHASE2-SEARCH-0058_openalex_dynamic_design.json` |
| PHASE2-SEARCH-0059 | Crossref works | `query.bibliographic=isotopically nonstationary metabolic flux analysis optimal experimental design sampling times`; `rows=25` | 25 returned / 459,397 API total | No new directly relevant design family; recovered the known Nöh dynamic-design lineage and a 2008 exploratory kinetic-identification paper | `PHASE2-SEARCH-0059_crossref_dynamic_design.json` |
| PHASE2-SEARCH-0060 | OpenAlex forward citations | `filter=cites:W2039977436`, where the seed is doi:10.1002/bit.20803; `per-page=50` | 50 / 90 | No new load-bearing dynamic experimental-design method | `PHASE2-SEARCH-0060_openalex_noh_forward.json` |

The closure ledger contains 354 occurrences and 248 ledger-local
deduplication groups: 106 duplicate occurrences, one full-text supporting
inclusion, one full text unavailable, 39 title/abstract supporting or
discovery leads, and 207 explicit exclusions. Across the base and closure
ledgers, exact normalized DOI/identifier-or-title comparison gives 375
Workstream A keys. That within-workstream key count is not a global
cross-workstream unique-work count. No raw result or provenance was changed.

**Corrected closure determination:** the bounded OpenAlex, Crossref and Nöh
forward-citation passes recovered the known dynamic/INST experimental-design
lineage but do not establish exhaustive coverage. The result and citation
windows were truncated, and the load-bearing 2006 Nöh–Wiechert primary full
text remains unavailable. This family is therefore
`INCOMPLETELY_SEARCHED`, and the workstream supports no definitive statement
about that paper's exact time-point optimisation algorithm or guarantee.
