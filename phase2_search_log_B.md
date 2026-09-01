# Phase 2A Search Log Fragment — Workstream B

Searcher: Codex `/root`. Execution date: 2026-07-31 UTC. No Phase 1 search
record was changed.

| ID | Source | Exact query | Filters/export | Results | Directly retained |
|---|---|---|---|---:|---|
| PHASE2-SEARCH-0011 | PubMed E-utilities | `(13C metabolic flux analysis[Title/Abstract]) AND (model selection[Title/Abstract] OR model validation[Title/Abstract] OR network validation[Title/Abstract])` | No date/language filter; `retmax=500`; JSON | 4 | P0030, P0033 |
| PHASE2-SEARCH-0012 | PubMed E-utilities | `(13C metabolic flux analysis[Title/Abstract]) AND (alternative reaction[Title/Abstract] OR pathway selection[Title/Abstract] OR structural model[Title/Abstract])` | No date/language filter; `retmax=500`; JSON | 0 | 0 |
| PHASE2-SEARCH-0013 | OpenAlex | `search=13C metabolic flux analysis model selection structural uncertainty` | `per-page=100`; JSON | 755 total; first 100 exported | P0030, P0031, P0033 |
| PHASE2-SEARCH-0014 | OpenAlex | `search=13C metabolic flux analysis Bayesian model averaging` | `per-page=100`; JSON | 706 total; first 100 exported | P0031, P0032 |
| PHASE2-SEARCH-0015 | Supplementary web discovery | `"Reversible jump MCMC" "metabolic flux analysis" Theorell Nöh 2020` | Source exposed no native result export or total; retained primary routing page `P0031-juser-record.html` | Count not exposed | P0031 |
| PHASE2-SEARCH-0016 | Supplementary web discovery | `"Bayesian model averaging" "13C" metabolic flux analysis structural` | Source exposed no native result export or total; retained official arXiv metadata `P0032-arxiv-metadata.xml` | Count not exposed | P0032 |

OpenAlex searches were deliberately broad discovery passes. Their first 100
results are preserved and prospectively dispositioned; the total-count tail
was not retrieved or claimed as screened.

## Targeted audit and citation-network closure

The searches below were run after the initial Workstream B extraction to
audit its two direct anchors and to test the nearest biochemical
model-discrimination transfer routes. Database-native exports are preserved
where available. Supplementary web searches did not expose total counts or a
native export; their visible bibliographic results were transcribed to a
structured snapshot and prospectively dispositioned without claiming a
complete result universe.

| ID | Source | Exact query or endpoint | Filters/export | Result occurrences preserved | New load-bearing records |
|---|---|---|---|---:|---:|
| PHASE2-SEARCH-0100 | Crossref REST API | `query.bibliographic=13C metabolic flux analysis model selection structural uncertainty mechanism discrimination` | `/works`; `rows=50`; `select=DOI,title,author,published,type,URL,container-title`; no date/language filter; JSON | 50 (529,007 total reported; first 50 only) | 0 |
| PHASE2-SEARCH-0101 | OpenAlex REST API | Anchor `https://doi.org/10.1371/journal.pcbi.1009999`; forward filter `cites:W4223583835`; backward filter is the pipe-joined `referenced_works` list from the anchor | No date/language filter; JSON | 1 anchor + 50 of 54 resolved backward references + 13 forward citations = 64 | 1: Borah Slater et al. 2023 |
| PHASE2-SEARCH-0102 | OpenAlex REST API | Anchor `https://doi.org/10.1093/bioinformatics/btz500`; forward filter `cites:W2958256899`; backward filter is the pipe-joined `referenced_works` list from the anchor | No date/language filter; JSON | 1 anchor + 38 of 39 resolved backward references + 20 forward citations = 59 | 0 additional; Borah Slater et al. duplicated 0101 |
| PHASE2-SEARCH-0110 | Supplementary web search | Batch: `"Liu Maini Baker 2026 model selection mechanism discrimination method"`; `"Liu Maini Baker 2026 experimental design model discrimination"`; `site:arxiv.org Liu Maini Baker 2026 hypothesis testing model`; `site:biorxiv.org Liu Maini Baker 2026 model selection` | First visible results; structured transcription; no exposed total | 10 scholarly records | 0 |
| PHASE2-SEARCH-0111 | Supplementary web search | Batch: `"Optimal experiment design for practical parameter identifiability and model discrimination"`; `"Yue Liu" "Philip K. Maini" "Ruth E. Baker" 2026`; `site:doi.org "Optimal experiment design for practical parameter identifiability"`; `site:academic.oup.com Yue Liu Maini Baker model discrimination` | First visible results; structured transcription in combined `PHASE2-SEARCH-0110-0112_web_snapshot.json`; no native export or exposed total | 9 scholarly records | 2: Liu et al. 2026; Flassig and Sundmacher 2012 |
| PHASE2-SEARCH-0112 | Supplementary web search | Batch: `"S0025556426001008" DOI`; `"Optimal experiment design for practical parameter identifiability and model discrimination" DOI Mathematical Biosciences`; `site:doi.org/10.1016 "Optimal experiment design for practical parameter identifiability"` | First visible results; structured transcription; no exposed total | 5 scholarly-record manifestations | 0 additional; final DOI and status verified |
| PHASE2-SEARCH-0113 | PubMed E-utilities and PMC BioC | `10.15252/msb.202211099[doi]`; exact PMID/PMCID retrieval | No date/language filter; JSON metadata and complete BioC XML | 1 | Borah Slater et al. full text verified |
| PHASE2-SEARCH-0114 | Supplementary web search | Batch: `10.1093/bioinformatics/bts585 PubMed PMC`; `"Optimal design of stimulus experiments for robust discrimination" PMC` | First visible results; structured transcription; no exposed total | 3 scholarly records | 2 additional: Stegmaier et al. 2013; Vanlier et al. 2014 |
| PHASE2-SEARCH-0115 | PMC BioC plus official software route | Exact `PMC3563641` full-text retrieval; inspect the paper-linked `ModelDiscriminationToolkitGUI` project | Complete BioC XML plus official project verification | 1 paper retrieval occurrence + 1 distinct software record | Stegmaier et al. full text and S0017 software verified |
| PHASE2-SEARCH-0116 | PMC BioC | Exact `PMC3946009` full-text retrieval | Complete BioC XML | 1 duplicate retrieval occurrence | Vanlier et al. full text verified |

The Crossref pass was too broad to support a saturation claim and was used
only as a prospectively screened audit sample. Searches 0101 and 0102 are
complete saved citation passes for the two principal direct anchors subject
to OpenAlex resolution (one unresolved P0031 reference and four unresolved
P0030 references are reported, not silently dropped). They added the
peer-reviewed biological application by Borah Slater et al. but no new
direct EMU-specific calibrated-testing method.

The adjacent transfer family is not treated as absent: searches 0111 and
0114 located fixed-parameter optimal-control separation, response-PDF
overlap design, Bayesian posterior-predictive design, and a max–min
parameter-robust biochemical design. These are load-bearing falsification
evidence. Workstream B is therefore closed only for the narrow question
“does structural/model-discrimination analysis already occur in isotope and
biochemical modeling?” The stronger finite-sample/composite-EMU question
remains cross-workstream and is not declared saturated here. P0033 also
remains full-text unavailable.
