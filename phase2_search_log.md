# Phase 2A Prospective Search Log

Execution date: 2026-07-31 UTC. Phase 1 search history and screening records
were not modified.

The exact prospective queries, filters, result counts and raw paths are
recorded in these authoritative workstream logs:

- `audit/phase2_search_log_A.md`: PHASE2-SEARCH-0001–0010 and closure
  PHASE2-SEARCH-0056–0060.
- `audit/phase2_search_log_B.md`: PHASE2-SEARCH-0011–0016, citation/audit
  closure PHASE2-SEARCH-0100–0102, and targeted primary-source closure
  PHASE2-SEARCH-0110–0116.
- `audit/phase2_search_log_C.md`: PHASE2-SEARCH-0021–0035 and closure
  PHASE2-SEARCH-0061–0068 and PHASE2-SEARCH-0080–0083.
- `audit/phase2_search_log_D.md`: PHASE2-SEARCH-0036–0040 and bounded
  citation/audit closure PHASE2-SEARCH-0104–0106.
- `audit/phase2_search_log_E.md`: PHASE2-SEARCH-0041–0055 and closure
  PHASE2-SEARCH-0069–0074 and PHASE2-SEARCH-0090–0093.

Ninety-one distinct search identifiers were executed and logged. Identifiers
0017–0020, 0075–0079, 0084–0089, 0094–0099, 0103 and 0107–0109 were
intentionally left unassigned rather than reused. Every record occurrence
physically preserved by a successful search or verification route has a
prospective disposition in `audit/phase2_screening.csv`.
PHASE2-SEARCH-0012 returned zero records. Failed PHASE2-SEARCH-0036 is logged
and preserved but contributes no screening row.

The consolidated ledger is a deterministic concatenation of the separately
generated A–E ledgers. Its 1,937 rows are occurrence-level records, not a
claim of 1,937 globally unique works. Counts and deduplication scope are
documented in `audit/phase2_deduplication_log.md`.

## Phase 2A.1 prospective repair series — appended 2026-07-31 UTC

The fixed-sample composite-testing repair used a separate identifier
namespace and did not alter or reuse any `PHASE2-SEARCH-####` record:

- `PHASE2A1-SEARCH-0001`–`0019` and `0064`–`0073`: query families A–C
  and bounded Goldenshluger–Juditsky–Nemirovski, Guntuboyina, and Birgé
  citation passes;
- `PHASE2A1-SEARCH-0021`–`0039`: query families D–F and their bounded
  anchor/citation passes; and
- `PHASE2A1-SEARCH-0041`–`0063` and `0074`–`0075`: supplementary
  legal-primary-location and official-metadata checks.

Identifiers `0020` and `0040` were intentionally never assigned. There are
**73** distinct Phase 2A.1 operations. Exact query text, source parameters,
reported and exported counts, raw filenames, and access outcomes remain in
`audit/phase2a1_search_log.md` and its AC/DEF source logs. The 25
supplementary checks add no independent screening occurrences because they
only verify locations for records already discovered by the formal searches.

The AC/DEF ledgers preserve **959** prospective occurrences and all have final
screening dispositions. These Phase 2A.1 records are not merged into the
1,937-row Phase 2 occurrence ledger; only final paper-level decisions from
the separate 241-record unresolved triage are propagated to close the 264
formerly included Phase 2 occurrences. Phase 1 provenance remains untouched.
