# Phase 2A.1 deduplication log — consolidated

Date: 2026-07-31 UTC

## Inputs and preservation

- `audit/phase2a1_screening_AC.csv`: 444 occurrences in 380 source groups;
- `audit/phase2a1_screening_DEF.csv`: 515 occurrences in 455 source groups;
- total: 959 occurrences in 835 independently assigned source groups.

The consolidation retains every occurrence. It does not edit either source
ledger, discard an evidence location, or substitute a consolidated
disposition for the source disposition. The output records both
`source_screening_state` and `screening_state`, and retains the source
duplicate group and source exclusion reason.

## Deterministic rules

1. Preserve each source ledger's documented duplicate groups.
2. Across AC and DEF only, merge an identical normalized DOI after lowercasing
   and removing a DOI-resolver prefix.
3. If both records lack a DOI, permit exact Unicode-NFKC/case-normalized title
   matching only when the title has at least four words and 30 characters,
   and nonblank authors and four-digit year also match exactly.
4. Never merge DOI-bearing versions by title, conflicting DOIs, generic
   titles, author similarity, citation context or fuzzy matching.
5. Choose the representative deterministically by strongest final evidence
   state (`FULL_TEXT_INCLUDED`, `FULL_TEXT_EXCLUDED`,
   `FULL_TEXT_UNAVAILABLE`, `FALSE_POSITIVE`, then `DUPLICATE`), followed by
   source occurrence order.
6. Re-label only a nonrepresentative cross-ledger occurrence. Preserve its
   original state, reason and exact evidence location in the `source_*`
   fields.

## Outcome

- 54 source-group joins were supported by normalized DOI;
- zero cross-stream joins used the exact-title fallback;
- 835 source groups became 781 consolidated bibliographic groups;
- 54 previously nonduplicate source occurrences became cross-workstream
  `DUPLICATE` occurrences;
- 126 occurrences were already duplicates in their source ledgers;
- total consolidated `DUPLICATE` occurrences: 180.

Existing-corpus duplicate representatives outrank a discovery-only
false-positive occurrence in the same cross-stream group. This keeps the
verified corpus links to P0041 and P0043 canonical without elevating either
prospective occurrence to a new inclusion.

## Cross-stream full-text traceability

Two independently inspected full-text occurrences were cross-stream
duplicates:

- A1DEF-0107 (Comminges and Dalalyan, DOI
  `10.1214/13-ejs766`) is linked to representative A1AC-0001; and
- A1DEF-0128 (Venkataramanan and Johnson, DOI
  `10.1214/18-ejs1419`) is linked to representative A1AC-0147.

Both consolidated duplicate rows retain `source_screening_state =
FULL_TEXT_INCLUDED`, their independent exact evidence locations, raw
snapshots and notes. Thus deduplication prevents double counting without
erasing independent verification.

## Version boundary

Version relationships that lack an identical DOI are not silently merged.
In particular, the inaccessible 1983 English Birgé chapter and accessible
1982 French Numdam article remain distinct records, as documented in the AC
source log.
