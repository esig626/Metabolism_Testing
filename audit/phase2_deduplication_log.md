# Phase 2A Deduplication Log

All counts below are prospective Phase 2 occurrence counts. They are not
counts of globally unique papers, software packages, or database records.
Phase 1 screening provenance was not used or altered.

## Deterministic source-ledger accounting

| Source ledger | Workstream routing | Occurrences | Ledger-local groups | `DUPLICATE` states |
|---|---|---:|---:|---:|
| `phase2_screening_A.csv` | A | 194 | 160 | 34 |
| `phase2_screening_A_closure.csv` | A | 354 | 248 | 106 |
| `phase2_screening_root.csv` | B and D | 210 | 187 | 23 |
| `phase2_screening_B_audit.csv` | B | 204 | 184 | 31 |
| `phase2_screening_C.csv` | C | 760 | 633 | 127 |
| `phase2_screening_D_closure.csv` | D | 115 | 106 | 15 |
| `phase2_screening_E.csv` | E | 100 | 93 | 1 |
| **Consolidated occurrence total** | **A–E** | **1,937** | **1,611 source-ledger group labels** | **337** |

The 1,611 group labels are local to their originating ledgers and are
preserved in the consolidated `duplicate_group` column. They must not be
treated as a global deduplicated record count. In particular:

- later full-text or official-documentation verification can share a group
  with an earlier discovery occurrence without being coded `DUPLICATE`;
- a record already represented in the curated corpus can be coded
  `DUPLICATE` even when it is the first occurrence of its local group; and
- Workstream E groups documentation manifestations or named software
  families, whereas paper workstreams primarily group bibliographic records.

The 337 `DUPLICATE` states and 1,600 other screening states are occurrence
dispositions, not unique-record totals.

## Matching rules

- A: canonical DOI, otherwise normalized title, with explicitly enumerated
  supplemental/version aliases in the generator. The base and closure
  ledgers retain separate group namespaces. An additional exact normalized
  identifier/title comparison finds 375 keys across both A ledgers; that is a
  Workstream A-only diagnostic.
- Root B/D: canonical DOI, otherwise native identifier.
- B audit: canonical DOI or normalized title, plus explicit version groups
  for the Liu–Maini–Baker and one-shot 13C15N records. Matches to curated
  corpus IDs are recorded as such.
- C: canonical DOI, otherwise normalized title, across all C query and
  citation snapshots.
- D closure: exact DOI and documented final/preprint relationships; an
  unresolved OpenAlex identifier remains `AWAITING_VERIFICATION`.
- E: explicit documentation/software-family groups; otherwise deterministic
  singleton groups. No blank group is emitted.

No title similarity, author similarity, or inferred topic equivalence is
used to manufacture cross-workstream matches.

## Rebuild

The component builders regenerate their ledgers from the preserved raw
snapshots. `scripts/build_phase2_screening.pl` then validates query IDs,
screening states, evidence levels, duplicate groups, exclusion reasons and
occurrence-ID uniqueness before atomically replacing
`audit/phase2_screening.csv`.

The consolidated state totals are:

| Screening state | Occurrences |
|---|---:|
| `FULL_TEXT_INCLUDED` | 39 |
| `TITLE_ABSTRACT_INCLUDED` | 264 |
| `TITLE_ABSTRACT_EXCLUDED` | 1,294 |
| `DUPLICATE` | 337 |
| `FULL_TEXT_UNAVAILABLE` | 2 |
| `AWAITING_VERIFICATION` | 1 |
| **Total** | **1,937** |

All 1,294 prospective exclusions and all 337 duplicate occurrences have an
explicit reason.

## Phase 2A.1 included-record normalisation — appended 2026-07-31 UTC

The preceding table is the retained pre-closure Phase 2A snapshot. During
Phase 2A.1, the 264 former `TITLE_ABSTRACT_INCLUDED` occurrences were
normalised by canonical DOI, otherwise a conservative exact bibliographic
key, into **241 unique paper records**. No fuzzy topical or
author-similarity merge was used. The difference is **23 repeated
occurrences**. The paper-level triage preserves every source occurrence count
and ends with:

| Final paper-level disposition | Unique records |
|---|---:|
| `FULL_TEXT_INCLUDED` | 12 |
| `FULL_TEXT_EXCLUDED` | 2 |
| `FULL_TEXT_UNAVAILABLE` | 11 |
| `FALSE_POSITIVE` | 216 |
| **Total** | **241** |

When those final paper-level decisions were propagated back to the
occurrence ledger, the 23 noncanonical repeated occurrences became
`DUPLICATE`. The original 1,937 occurrence rows, their order, query IDs, raw
paths, and source-ledger groups were preserved. This accounts for the change
from 337 to **360** occurrence-level duplicates; it does not assert a global
deduplication of the remaining Phase 2 ledger.

The current consolidated state totals are:

| Screening state | Occurrences |
|---|---:|
| `FULL_TEXT_INCLUDED` | 51 |
| `FULL_TEXT_EXCLUDED` | 2 |
| `FULL_TEXT_UNAVAILABLE` | 13 |
| `FALSE_POSITIVE` | 216 |
| `TITLE_ABSTRACT_EXCLUDED` | 1,294 |
| `DUPLICATE` | 360 |
| `AWAITING_VERIFICATION` | 1 |
| `TITLE_ABSTRACT_INCLUDED` | 0 |
| **Total** | **1,937** |

Every final non-inclusion has an explicit reason. In particular, the
generator and consolidated output now preserve the reason for E-D0100
(WUFlux) as `FULL_TEXT_UNAVAILABLE`; it is not left blank or inferred during
validation.

## Phase 2A.1 foundational-search deduplication

The separate foundational series contains **959 occurrences**. Its two
source ledgers supplied 835 source-local groups; 54 normalized-DOI
cross-stream joins yielded **781 consolidated bibliographic groups**. No
cross-stream merge used fuzzy matching. All 126 source-ledger duplicates and
54 additional cross-stream duplicate occurrences remain represented, for
**180 `DUPLICATE` occurrences** in the consolidated Phase 2A.1 ledger.

Detailed rules, the two independently inspected cross-stream duplicates, and
the decision not to merge unverified publication versions are preserved in
`audit/phase2a1_deduplication_log.md`.

## Scoped-disposition correction — appended 2026-07-31 UTC

The preceding Phase 2A.1 included-record tables are historical records of the
automatic closure that was subsequently rejected. They remain visible to
preserve the audit trail, but their `FALSE_POSITIVE = 216` interpretation is
not the current screening semantics.

The deduplication result itself is unchanged: 264 source occurrences
represent **241 unique papers**, with **23 repeated occurrences** retained as
`DUPLICATE`. Explicit scoped mapping, not priority level, now assigns the 241
paper-level records as follows:

| Current paper-level scoped disposition | Unique papers |
|---|---:|
| `FULL_TEXT_INCLUDED` | 12 |
| `FULL_TEXT_EXCLUDED` | 2 |
| `FULL_TEXT_UNAVAILABLE` | 11 |
| `FALSE_POSITIVE_CONFIRMED` | 2 |
| `DEFERRED_RELEVANT_SUPPORTING` | 60 |
| `DEFERRED_RELEVANT_ADJACENT` | 95 |
| `OUT_OF_SCOPE_FOR_PHASE2A1` | 59 |
| **Total** | **241** |

The current consolidated occurrence accounting is:

| Screening state | Occurrences |
|---|---:|
| `FULL_TEXT_INCLUDED` | 51 |
| `FULL_TEXT_EXCLUDED` | 2 |
| `FULL_TEXT_UNAVAILABLE` | 13 |
| `FALSE_POSITIVE_CONFIRMED` | 2 |
| `DEFERRED_RELEVANT_SUPPORTING` | 60 |
| `DEFERRED_RELEVANT_ADJACENT` | 95 |
| `OUT_OF_SCOPE_FOR_PHASE2A1` | 59 |
| `TITLE_ABSTRACT_EXCLUDED` | 1,294 |
| `DUPLICATE` | 360 |
| `AWAITING_VERIFICATION` | 1 |
| **Total** | **1,937** |

The corrected mapping changes no occurrence identifier, source query,
source-ledger group, row order or duplicate link. Deferred and scoped-out
states preserve the original title/abstract relevance metadata and are not
full-text exclusions from the broader Phase 2 evidence base.
