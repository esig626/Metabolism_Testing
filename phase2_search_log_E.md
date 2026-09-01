# Phase 2A prospective search log — Workstream E

All searches were executed on 2026-07-31 by Codex. Result counts below are
the records actually preserved in the structured snapshots, not database-wide
estimates. The snapshots are under `audit/phase2_raw_search_results/E/`.

| ID | Source | Exact query or request | Filters | Preserved results | Screening note |
|---|---|---|---|---:|---|
| PHASE2-SEARCH-0041 | JuGit API | `GET /api/v4/projects?search=13CFLUX&simple=true&per_page=100` | public projects; 100/page | 1 | 13CFLUX(v3) repository included and inspected. |
| PHASE2-SEARCH-0042 | PubMed E-utilities | `INCA[Title] AND computational platform[Title/Abstract]` | none; `retmax=100` | 1 | Software paper included; official MFA Suite documentation separately inspected. |
| PHASE2-SEARCH-0043 | PubMed E-utilities | `13CFLUX2[Title/Abstract]` | none; `retmax=100` | 6 | Software/tool records included when relevant; unrelated application records excluded with reasons. |
| PHASE2-SEARCH-0044 | GitHub API | `GET /repos/fumiomatsuda/mfapy` | exact repository | 1 | Included; repository commit recorded. |
| PHASE2-SEARCH-0045 | GitHub API | `GET /repos/Chaowu88/freeflux` | exact repository | 1 | Included; repository commit recorded. |
| PHASE2-SEARCH-0046 | Crossref API | `query.bibliographic="OpenFLUX" "efficient modelling software"` | `rows=10`; selected bibliographic fields | 10 | Name-matching software paper included; false matches excluded. |
| PHASE2-SEARCH-0047 | PubMed E-utilities | `OpenMebius[Title/Abstract]` | none; `retmax=100` | 1 | Included. |
| PHASE2-SEARCH-0048 | GitHub API | `GET /repos/sgsokol/influx` | exact repository | 1 | Included; repository commit recorded. |
| PHASE2-SEARCH-0049 | Crossref API | `query.bibliographic="Metran" "13C metabolic flux analysis"` | `rows=10`; selected bibliographic fields | 10 | No Metran-titled software record returned; all results excluded. Existing official lab-page evidence remains the only platform evidence in scope. |
| PHASE2-SEARCH-0050 | GitHub API | `GET /repos/cfoguet/iso2flux` | exact repository | 1 | Included; repository commit recorded. |
| PHASE2-SEARCH-0051 | Crossref API | `query.bibliographic="sysmetab" "isotope labeling"` | `rows=10`; selected bibliographic fields | 10 | No sysmetab-titled record returned; all results excluded. |
| PHASE2-SEARCH-0052 | Crossref API | `query.bibliographic="Isodyn" "metabolic flux"` | `rows=10`; selected bibliographic fields | 10 | No Isodyn-titled record returned; all results excluded. |
| PHASE2-SEARCH-0053 | Crossref API | `query.bibliographic="ScalaFlux" "metabolic flux"` | `rows=10`; selected bibliographic fields | 10 | Exact software lead included where returned; false matches excluded. |
| PHASE2-SEARCH-0054 | Crossref API | `query.bibliographic="Mass Isotopolome Analyzer"` | `rows=10`; selected bibliographic fields | 10 | MIA lead included where returned; false matches excluded. |
| PHASE2-SEARCH-0055 | GitHub API | repository search query `"13C" "metabolic flux analysis"` | `per_page=100`; public repositories | 13 | General platforms retained; application/thesis repositories excluded explicitly. |
| PHASE2-SEARCH-0069 | Antoniewicz laboratory | `GET https://cheresearch.engin.umich.edu/mranton/metran.html` | official platform page only | 1 | Metran included; directly verified GUI, EMU, simulation, flux design, GOF, CIs and observability; version/maintenance unspecified. |
| PHASE2-SEARCH-0070 | PubMed E-utilities | `10.1109/TCBB.2016.2544299[DOI]` | none; `retmax=20` | 1 | sysmetab paper included at Level 2; historical Scilab Forge implementation remained inaccessible. |
| PHASE2-SEARCH-0071 | GitHub repository API | `GET /repos/seliv55/isodyn` | exact official repository | 1 | Isodyn repository included and inspected at commit `c4f15c4ddce751d20c84b1916901c590594892e4`. |
| PHASE2-SEARCH-0072 | PMC BioC full text | `GET PMC12696647` followed by bounded software-reference inspection | 13CFLUX(v3) software paper only | 1 duplicate seed | Benchmarked FreeFlux, INCA and influx_si were already represented; no new decision-software family. |
| PHASE2-SEARCH-0073 | bioRxiv API | `GET /details/biorxiv/10.64898/2026.03.20.698926` | exact DOI | 1 | OpenMebius2 primary preprint included; flux-precision tracer suggestion and PolyForm Noncommercial licence confirmed. |
| PHASE2-SEARCH-0074 | PMC BioC full text | `GET PMC10664898` and `GET PMC10510750`; bounded software-reference inspection | BayFlux and FreeFlux primary papers only | 5 consequential records | BayFlux and FreeFlux full texts included; FluxPyt, FiatFlux and WUflux retained as Level 3 discovery leads. |
| PHASE2-SEARCH-0090 | SourceForge REST and official Git repository | `GET https://sourceforge.net/rest/p/fluxpyt`; inspect `https://git.code.sf.net/p/fluxpyt/code` | exact named project only; shallow inspection at HEAD | 1 | FluxPyt included; official code verified at commit `beb86d8811941aaaed0a05bcb3f6ebc6f49003ec`; version conflict recorded. |
| PHASE2-SEARCH-0091 | PubMed/PMC | `10.1186/1471-2105-6-209[DOI]`; retrieve PMC1199586 through PMC BioC | exact named software paper only | 1 | FiatFlux included from complete primary full text; current code distribution unavailable. |
| PHASE2-SEARCH-0092 | PMC BioC | `GET PMC5096001` | exact named WUFlux software paper only | 1 | WUFlux included; EMU, inverse fitting, GUI, UQ and multi-tracer-input claims checked at method passages. |
| PHASE2-SEARCH-0093 | Official project URL access check | `GET http://www.13cmfa.org/` | exact paper-named project homepage only | 0 | Host did not resolve; retained as `FULL_TEXT_UNAVAILABLE`, without negating primary-paper capability evidence. |

The PubMed `*_summary.json` files are metadata retrievals for identifiers
already returned by the corresponding search, not additional discovery
searches. Repository clones used for exact path inspection were shallow clones
of official repositories and do not add discovery records.

PHASE2-SEARCH-0069–0074 and PHASE2-SEARCH-0090–0093 were bounded
official/primary-source closures, not broad software searches. Citation
inspection stopped at named general-purpose 13C-MFA software families that
could affect the integration comparison.
