# Search Log

Append one entry per executed database query or bounded citation/software
search. Preserve exact syntax and do not rewrite old entries when a search is
updated.

## Entry template

- **Search ID:** SEARCH-####
- **Date (UTC):** YYYY-MM-DD
- **Database/service:**
- **Exact query:**

  ```text
  Paste the exact executed query or request parameters.
  ```

- **Filters:** None, or exact fields/date/language/type/sort/page filters
- **Result count:** Exact count, or `not exposed` with explanation
- **Records retained:** Count and record IDs, or `pending screening`
- **Searcher:** Person or agent identifier
- **Notes:** Query-family ID, syntax adaptation, pages screened, export path,
  access limits, deduplication, citation-search seed, or software version

## Pilot searches — 2026-07-30

All searches below were executed by agent `/root`. No date, language or
publication-type filters were applied unless stated. PubMed searches used the
E-utilities `esearch` endpoint with `retmax=0`; Crossref used `/works` with
`rows=0`; OpenAlex used `/works?search=...&per-page=1`. Retained counts are
deduplicated evidence records, not the number of useful hits visible in the
service.

| Search ID | Database/service | Exact query | Result count | Records retained | Notes |
|---|---|---|---:|---|---|
| SEARCH-0001 | PubMed E-utilities | `13C metabolic flux analysis AND tracer selection` | 19 | 6: P0004-P0009 | Tracer-selection family. |
| SEARCH-0002 | PubMed E-utilities | `13C metabolic flux analysis AND (confidence interval OR identifiability)` | 26 | 5: P0003, P0010, P0018, P0019, P0023 | UQ/identifiability family; P0023 found during adjacent expansion. |
| SEARCH-0003 | PubMed E-utilities | `13C metabolic flux analysis AND (model selection OR goodness of fit)` | 44 | 2: P0015-P0016 | Model-validation family; broad result set mostly applications/reviews. |
| SEARCH-0004 | PubMed E-utilities | `13C metabolic flux analysis AND (Bayesian OR robust)` | 55 | 4: P0009-P0011, P0016 | Robust/Bayesian family. |
| SEARCH-0005 | PubMed E-utilities | `13C metabolic flux analysis AND (sample size OR replicate)` | 14 | 0 | No retained primary paper made sample size or replicate count an output. Absence is not evidence of a gap. |
| SEARCH-0006 | PubMed E-utilities | `isotopically nonstationary metabolic flux analysis` | 83 | 5: P0012-P0014, P0016-P0017 | INST-MFA/time-course family. |
| SEARCH-0007 | Crossref API | `query.bibliographic=13C metabolic flux analysis tracer design&rows=0` | 9,267,105 | 0 | Crossref bibliographic matching was too broad; used only as a metadata check. |
| SEARCH-0008 | Crossref API | `query.bibliographic=13C metabolic flux analysis model selection&rows=0` | 10,177,796 | 0 | Overbroad count; no screening inference made. |
| SEARCH-0009 | Crossref API | `query.bibliographic=optimal experimental design model discrimination T-optimal KL-optimal&rows=0` | 7,701,485 | 0 | Overbroad count; DOI-by-title checks followed. |
| SEARCH-0010 | Crossref API | `query.bibliographic=active hypothesis testing controlled sensing composite&rows=0` | 3,044,793 | 0 | Overbroad count; no absence inference. |
| SEARCH-0011 | OpenAlex API | `search=13C metabolic flux analysis tracer design&per-page=1` | 3,253 | 2: P0001, P0005 | Discovery and metadata cross-check. |
| SEARCH-0012 | OpenAlex API | `search=13C metabolic flux analysis model selection&per-page=1` | 6,507 | 1: P0015 | Discovery only. |
| SEARCH-0013 | OpenAlex API | `search=optimal experimental design model discrimination&per-page=1` | 202,817 | 4: P0021-P0024 | Adjacent optimal-design expansion. |
| SEARCH-0014 | OpenAlex API | `search=active hypothesis testing controlled sensing composite&per-page=1` | 114,865 | 4: P0025-P0028 | Adjacent testing/controlled-sensing expansion. |
| SEARCH-0015 | OpenAlex citation graph | `works/https://doi.org/10.1016/j.ymben.2011.12.005` | 31 references; 77 citing works | 8: P0002-P0004, P0006-P0008, P0013, P0015 | Bounded backward/forward pass for P0005; titles/abstracts of the most relevant methodological links screened. |
| SEARCH-0016 | Official software sites and repositories | `13CFLUX2; INCA; OpenFLUX; mfapy; FreeFlux; OpenMebius; influx_s; Metran` | 8 named projects | 8: S0001-S0008 | Official repositories/docs searched separately; assessment date 2026-07-30. |

### Supplementary web-discovery queries

These searches used a general web index only for discovery and routing to
PubMed, PMC, DOI/publisher pages, arXiv author manuscripts, or official
software sites. Result counts were not exposed. The first results page was
screened; snippets were not used as evidence.

| Search ID | Exact query | Records retained |
|---|---|---|
| SEARCH-0017 | `site:pubmed.ncbi.nlm.nih.gov 13C metabolic flux analysis tracer selection experimental design Crown Antoniewicz` | P0005-P0008 |
| SEARCH-0018 | `site:pubmed.ncbi.nlm.nih.gov 13C metabolic flux analysis confidence intervals identifiability observability EMU` | P0003, P0018-P0019 |
| SEARCH-0019 | `site:pubmed.ncbi.nlm.nih.gov 13C metabolic flux analysis model validation network selection goodness of fit` | P0015 |
| SEARCH-0020 | `site:pubmed.ncbi.nlm.nih.gov Bayesian 13C metabolic flux analysis robust tracer design` | P0009-P0011 |
| SEARCH-0021 | `official 13CFLUX2 software repository documentation license` | S0001 |
| SEARCH-0022 | `official INCA 13C metabolic flux analysis software` | S0002, S0008 |
| SEARCH-0023 | `official OpenFLUX software 13C MFA repository` | S0003 |
| SEARCH-0024 | `official mfapy 13C metabolic flux analysis GitHub` | S0004 |
| SEARCH-0025 | `site:pubmed.ncbi.nlm.nih.gov elementary metabolite units framework metabolic network 2007 Antoniewicz Kelleher Stephanopoulos` | P0002 |
| SEARCH-0026 | `site:pubmed.ncbi.nlm.nih.gov determination confidence intervals metabolic fluxes stable isotope measurements Antoniewicz 2006` | P0003 |
| SEARCH-0027 | `site:pubmed.ncbi.nlm.nih.gov parallel labeling experiments 13C MFA COMPLETE-MFA Leighty Antoniewicz` | P0008 |
| SEARCH-0028 | `site:pubmed.ncbi.nlm.nih.gov isotopically nonstationary metabolic flux analysis Young 2008` | P0013-P0014 |
| SEARCH-0029 | `T-optimal experimental design model discrimination Atkinson Fedorov 1975 DOI` | P0021-P0022 |
| SEARCH-0030 | `KL-optimal discriminating designs Lopez-Fidalgo Tommasi Trandafir DOI` | P0023-P0024 |
| SEARCH-0031 | `Chernoff sequential design experiments 1959 DOI` | P0025 |
| SEARCH-0032 | `controlled sensing active hypothesis testing Nitinawarat Veeravalli DOI` | P0026-P0028 |
| SEARCH-0033 | `"optimal design of isotopomer labeling experiments" metabolic` | P0004 |
| SEARCH-0034 | `"experimental design" "13C metabolic flux analysis" Fisher information` | P0004, P0007 |
| SEARCH-0035 | `"measurement selection" 13C metabolic flux analysis` | P0004 |
| SEARCH-0036 | `"parallel labeling experiments" metabolic flux analysis Antoniewicz COMPLETE-MFA` | P0008, P0015 |
| SEARCH-0037 | `"COMPLETE-MFA" DOI 2013 49-55` | P0008 |
| SEARCH-0038 | `"To be certain about the uncertainty" DOI` | P0010 |
| SEARCH-0039 | `"Bayesian Metabolic Flux Analysis reveals intracellular flux couplings" DOI` | P0011 |
| SEARCH-0040 | `"Parallel labeling experiments validate Clostridium" DOI` | P0015 |

Google Scholar was not used: its result counts and reproducible access were
not available in this environment. This is a missing supplementary route, not
an exclusion criterion or evidence of absence.

## Targeted hostile-review repair — 2026-07-30

- **Search IDs:** SEARCH-0041–SEARCH-0048
- **Database/service:** General web index routed to primary publisher,
  Project Euclid, arXiv and author-repository sources.
- **Exact queries:** `"Bidirectional reaction steps in metabolic networks:
  IV" PDF`; `"COMPLETE-MFA" "49-55" PDF`; `"Metabolic isotopomer labeling
  systems. Part II" PDF`; `"Sequential controlled sensing for composite
  multihypothesis testing" PDF`; `site:projecteuclid.org "Sequential Design
  of Experiments" Chernoff 1959 pdf`; `site:projecteuclid.org "Active
  sequential hypothesis testing" Naghshvar Javidi`; `"Controlled Sensing for
  Multihypothesis Testing" arxiv theorem lower bound`; `"Sequential controlled
  sensing for composite multihypothesis testing" theorem lower bound arxiv`.
- **Filters:** Targeted named-paper verification only.
- **Result count:** Not exposed.
- **Records retained:** Existing P0018, P0026-P0028 verified; no new paper ID.
- **Searcher:** Codex `/root`.
- **Notes:** Full author manuscripts downloaded for P0026-P0028; P0018
  publisher full-text HTML inspected. P0004/P0008/P0025 remained inaccessible.

- **Search IDs:** SEARCH-0049–SEARCH-0063
- **Database/service:** PubMed, Crossref and OpenAlex APIs.
- **Exact query:** Exact reruns of SEARCH-0001–SEARCH-0015, unchanged.
- **Filters:** Original API parameters; PubMed `retmax` increased to 10000
  solely to export all identifiers.
- **Result count:** 206 unique PubMed IDs; four one-record OpenAlex responses;
  Crossref count-only responses; SEARCH-0010 rerun failed HTTP 429.
- **Records retained:** Existing P0001-P0028 as mapped in
  `audit/pilot_screening.csv`.
- **Searcher:** Codex `/root`.
- **Notes:** Raw snapshots preserved under `audit/raw_search_results/`.

## Bounded access triage — 2026-07-30

- **Search IDs:** SEARCH-0064–SEARCH-0075
- **Database/service:** General web index routed only to DOI/publisher,
  recognised repository, and official author sources.
- **Exact queries:** `"Parallel labeling experiments and metabolic flux
  analysis" Antoniewicz full text`; `"13C metabolic flux analysis as an
  inverse problem" model validation Antoniewicz full text`; `"Optimal tracer
  selection for in vivo 13C metabolic flux analysis" full text`; `"T-optimum
  designs for discrimination between two polynomial models" full text`;
  `"10.1016/j.ymben.2013.07.006" PDF`; `"10.1016/j.ymben.2014.08.002" PDF`;
  `"10.1002/biot.202000427" PDF`; `site:academic.oup.com/biomet
  "10.1093/biomet/62.2.289"`; `"COMPLETE-MFA" "complementary parallel
  labeling" DOI`; `"The design of experiments for discriminating between two
  rival models" PDF Atkinson Fedorov`; `"Optimal design experiments for
  discriminating between several models" PDF Atkinson Fedorov`; `"Pool size
  measurements" Zheng Young author manuscript`.
- **Filters:** Named-paper access triage only; no broad discovery; at most two
  additional targeted routes for each load-bearing record.
- **Result count:** Not exposed.
- **Records retained:** No new records. P0008 DOI corrected to
  `10.1016/j.ymben.2013.08.006`.
- **Searcher:** Codex `/root`.
- **Notes:** Complete primary text was not obtained for P0008, P0015, P0016,
  P0021, or P0022. Automated retrieval is now closed for all nine records.

## Targeted GAP-06/GAP-07 falsification — 2026-07-30

- **Search ID:** SEARCH-0076
- **Database/service:** General web index routed to primary publisher and
  arXiv full text.
- **Exact queries:** `primary paper robust optimal experimental design model
  misspecification model discrimination pdf`; `Bayesian calibration computer
  models model discrepancy Kennedy O'Hagan primary paper pdf`;
  `distributionally robust optimal experimental design primary paper model
  uncertainty`; `robust hypothesis testing model uncertainty contamination
  neighborhoods primary paper pdf`; `10.1214/13-AOS1117 citation pages`.
- **Filters:** Primary adjacent methods directly testing GAP-06 only; first
  result page; no broader citation expansion.
- **Result count:** Not exposed.
- **Records retained:** 1 (P0029).
- **Searcher:** Codex `/root`.
- **Notes:** Complete arXiv primary text for P0029 inspected; equations (3)-(6),
  Theorem 4.1, Sections 5.3-5.4 and Figure 3 checked. Other results were used
  only for routing/context and were not encoded as evidence.

- **Search ID:** SEARCH-0077
- **Database/service:** Official project pages, official documentation, and
  official repositories for the existing software corpus.
- **Exact queries:** `site:github.com/Chaowu88/freeflux README uncertainty
  tracer design model comparison`; `site:github.com/fumiomatsuda/mfapy README
  confidence interval model comparison`; `site:13cflux.net/13cflux2 tracer
  design documentation`; `site:github.com/sgsokol/influx README confidence
  intervals model comparison`; `official FreeFlux documentation GitHub
  Chaowu88 freeflux README`; `official mfapy GitHub documentation metabolic
  flux confidence interval`; `official INCA metabolic flux analysis
  documentation model comparison tracer design`.
- **Filters:** The eight already-retained packages only; official sources;
  no discovery of additional packages.
- **Result count:** Not applicable.
- **Records retained:** Existing S0001-S0008; no new software record.
- **Searcher:** Codex `/root`.
- **Notes:** S0001 and S0004 capability evidence was strengthened only where
  an exact official page, fact-sheet section, paper section, or API method was
  inspectable.

## Provenance correction for 2026-07-30 API reruns

- **Repair query IDs:** REPAIR-SEARCH-0001–REPAIR-SEARCH-0015.
- **Database/service and query text:** Same services, query text, and filters
  documented for the corresponding original SEARCH-0001–SEARCH-0015 entries;
  PubMed used `retmax=10000` to export identifiers.
- **Date:** 2026-07-30.
- **Searcher:** Codex `/root`.
- **Notes:** These identifiers describe only the repair reruns stored in
  `audit/raw_search_results/`. A match under a REPAIR-SEARCH identifier does
  not demonstrate which original pilot query discovered the record. No
  original record-level exports survive, so original historical query IDs are
  blank in the screening ledger.

## Phase 3B bounded direct-MID exact-formulation search — 2026-08-01

- **Search IDs:** the non-contiguous `P3-SEARCH-*` series through
  `P3-SEARCH-0021`, supplementary
  `P3-A-*`, `P3-B-*`, `P3-E-*`, `P3-WEB-01`–`P3-WEB-52`, and
  `P3-CITE-01`–`P3-CITE-15`.
- **Database/service:** PubMed, Europe PMC, OpenAlex, Crossref, primary
  publisher/repository pages, and backward/forward citation searches from the
  closest direct-MID, induced-family, non-identification, shared-state, and
  measurement-error papers.
- **Exact queries, filters and result counts:** Recorded row by row in
  `audit/phase3_search_log.md`; API result captures are in
  `audit/phase3_raw_search_results/`. Searches had no date, language or
  publication-type restriction unless the detailed row states otherwise.
- **Records retained:** 23 unique primary papers: 0 `EXACT FORMULATION`, 11
  `PARTIAL FORMULATION`, 3 `GENERIC THEORY ONLY`, 8 `APPLICATION WITHOUT
  THEORY`, and 1 `ADJACENT BUT NONTRANSFERABLE`. The record-level disposition
  and exact evidence locations are in `audit/phase3_screening.csv`.
- **Searcher:** Codex `/root` with delegated read-only extraction and hostile
  QC.
- **Notes:** This was a bounded exact-formulation search across families A–E,
  not a literature-saturation search. Citation chaining added no new
  structural formulation category or new combination of defining coverage
  cells; the operational definition and anchor-specific outcomes are in the
  detailed Phase 3B log. Search absence was not used as a novelty claim.
