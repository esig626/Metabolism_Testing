# Phase 2A.1 prospective search log — consolidated index

Execution date: 2026-07-31 UTC

This index consolidates the independently executed Phase 2A.1 searches without
rewriting either workstream log. Exact query text, API parameters,
database-reported totals, exported-window counts, citation-pass scope and raw
filenames are preserved in:

- `audit/phase2a1_search_log_AC.md` for query families A–C and the bounded
  Guntuboyina/Birgé citation passes;
- `audit/phase2a1_search_log_DEF.md` for query families D–F and their bounded
  anchor/citation passes; and
- `audit/phase2a1_raw_search_results/root/supplementary_web_search_snapshots.csv`
  for the root reviewer's supplementary primary-location checks.

Those three records are the authoritative exact operation-level logs. This
file is a deterministic cross-workstream index, not a replacement for them.

## Query-ID registry

| Owner | Query identifiers | Number of operations | Screened occurrences |
|---|---|---:|---:|
| AC: families A–C | `PHASE2A1-SEARCH-0001`–`0019`; `0064`–`0073` | 29 | 444 |
| DEF: families D–F | `PHASE2A1-SEARCH-0021`–`0039` | 19 | 515 |
| Root supplementary location checks | `PHASE2A1-SEARCH-0041`–`0063`; `0074`–`0075` | 25 | 0 independent screening occurrences |
| **Total** | 73 distinct prospective operation IDs | **73** | **959** |

`PHASE2A1-SEARCH-0020` and `PHASE2A1-SEARCH-0040` were never assigned. The
gap is intentional; identifiers were not backfilled.

The 25 root checks did not expose stable per-query totals. Their structured
snapshot records `NOT_EXPOSED_BY_INTERFACE` rather than an invented count.
They locate legal primary copies or official metadata for records already
represented by the formal AC/DEF searches, and therefore do not create
additional screening occurrences.

## Consolidated screening result

`scripts/build_phase2a1_screening.pl` merged the two source ledgers while
retaining all 959 prospective occurrences and every query ID, native ID, raw
snapshot, source disposition and evidence location. Conservative cross-stream
deduplication produced 781 bibliographic groups:

- 22 `FULL_TEXT_INCLUDED` representatives;
- 30 `FULL_TEXT_UNAVAILABLE` representatives;
- 727 `FALSE_POSITIVE` representatives; and
- two `DUPLICATE` representatives already linked to the existing corpus.

The output also contains 178 nonrepresentative `DUPLICATE` occurrences; the
state counts over all occurrences are therefore 22, 30, 727 and 180,
respectively. No interim title/abstract-included state remains.

## Raw material and access boundary

Structured database exports and inspected legal primary copies are inventoried
in `audit/phase2a1_raw_search_results/README.md`. Search results were bounded
as documented in the source logs; large database-reported universes were not
represented as screened. Inaccessible sources remain
`FULL_TEXT_UNAVAILABLE`, and metadata/location checks do not support
theorem-level claims.

## Saturation boundary

This consolidation makes no new saturation claim. The D–F evidence set still
has four load-bearing primary texts unavailable: the 1983 English Birgé
chapter, Wefelmeyer (1987), Bernshtein (1981), and the 2024 POMDP paper. The
AC citation passes found no additional load-bearing method
family within their bounded scope, but that result is not promoted here into
saturation of Phase 2 or of any other workstream.
