# Phase 2A Search Log Fragment — Workstream D

Searcher: Codex `/root`. Execution date: 2026-07-31 UTC.

| ID | Source | Exact query | Filters/export | Results | Directly retained |
|---|---|---|---|---:|---|
| PHASE2-SEARCH-0036 | PubMed E-utilities | `(isotope tracing[Title/Abstract] OR metabolic flux analysis[Title/Abstract]) AND (atom mapping error[Title/Abstract] OR omitted reaction[Title/Abstract] OR model misspecification[Title/Abstract])` | No date/language filter; `retmax=500`; JSON | Request failed with API rate-limit response; 0 records screened | 0 |
| PHASE2-SEARCH-0037 | PubMed E-utilities | `(13C metabolic flux analysis[Title/Abstract]) AND (measurement error model[Title/Abstract] OR incomplete network[Title/Abstract] OR model uncertainty[Title/Abstract])` | No date/language filter; `retmax=500`; JSON | 1 | P0033 (duplicate discovery) |
| PHASE2-SEARCH-0038 | OpenAlex | `search=metabolic flux analysis model misspecification omitted reactions atom mapping error` | `per-page=100`; JSON | 1 | P0035 |
| PHASE2-SEARCH-0039 | Supplementary web discovery | `"Model Misspecification" "metabolic flux analysis" omitted reactions` | Source exposed no native result export or total; retained complete primary XML `P0035-PMC5590471-fulltext.xml` | Count not exposed | P0035 |
| PHASE2-SEARCH-0040 | Supplementary web discovery | `"incorrect atom mapping" 13C metabolic flux analysis` | Source exposed no native result export or total; retained complete primary XML `P0034-PMC8878866-fulltext.xml` | Count not exposed | P0034 |
| PHASE2-SEARCH-0104 | Crossref REST API | `query.bibliographic=model misspecification metabolic flux analysis omitted reactions incomplete network robust model validation` | `rows=50`; selected fields `DOI,title,author,published,type,URL`; no date/language filter; exact request from the execution record, with the unmodified response preserved as JSON | 573,864 total; 50 exported and screened | P0045 (new full-text inclusion); P0015, P0033, P0034 and P0035-related versions were duplicates |
| PHASE2-SEARCH-0105 | OpenAlex bounded backward/forward citation pass from MetAMDB (P0034), DOI `10.3390/metabo12020122`, OpenAlex `W4210780466` | Anchor: `/works/https://doi.org/10.3390/metabo12020122`; backward metadata resolution: `/works?filter=ids.openalex:W1508604947\|W1964189732\|W1964572291\|W1999619962\|W2007750874\|W2034994407\|W2065163714\|W2078355959\|W2129727604\|W2134138595\|W2148497594\|W2319614057\|W2559588208\|W2626704831\|W2789128799\|W2796927648\|W2899903294\|W2929387033\|W2977870980\|W3096266289\|W3105895642\|W3172399532\|W3175749050\|W3183479527&per_page=100`; forward: `/works?filter=referenced_works:W4210780466&per_page=200` | No date/language filter; anchor, backward and forward responses preserved separately | 1 anchor + 24 resolved backward references + 9 forward citations = 34 screened occurrences | P0034 duplicate; no new full-text inclusion |
| PHASE2-SEARCH-0106 | OpenAlex bounded backward/forward citation pass from Gunawan et al. (P0035), DOI `10.3390/bioengineering4020048`, OpenAlex `W2601725879` | Anchor: `/works/https://doi.org/10.3390/bioengineering4020048`; backward metadata resolution: `/works?filter=ids.openalex:W1222146597\|W1583997234\|W1584375372\|W1989845358\|W2009378698\|W2027474258\|W2046154060\|W2056162424\|W2061226704\|W2065163714\|W2071646337\|W2075802407\|W2082382448\|W2100334725\|W2101981035\|W2128601422\|W2132177132\|W2133783666\|W2157264112\|W2163754616\|W2165674132\|W2429556350\|W2519327819\|W2543238710\|W3125511805\|W4253808107\|W4301515466\|W6604903323\|W953353200&per_page=100`; forward: `/works?filter=referenced_works:W2601725879&per_page=200` | No date/language filter; anchor, backward and forward responses preserved separately | 1 anchor + 29 backward identifiers (28 metadata-resolved, 1 unresolved) + 1 forward citation = 31 screened occurrences | P0045 duplicate discovery with its earlier PHASE2-SEARCH-0104 full-text inclusion; P0035 duplicate |

The failed PHASE2-SEARCH-0036 response is preserved and was not silently
retried. PHASE2-SEARCH-0037 and PHASE2-SEARCH-0038 constitute the two distinct
structured-source passes for this bounded family.

PHASE2-SEARCH-0104–0106 were a bounded closure, not a restart of the broad
workstream. The exact prospective dispositions are in
`audit/phase2_screening_D_closure.csv`. Twenty-seven title/metadata leads
remain discovery-only and support no substantive synthesis statement. The
OpenAlex identifier `W6604903323` was listed by the P0035 anchor but did not
resolve in the preserved batch response; it remains
`AWAITING_VERIFICATION`, without invented metadata.
