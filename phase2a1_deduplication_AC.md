# Phase 2A.1 deduplication log — workstream AC

Date: 2026-07-31 UTC

## Inputs

- 319 occurrences from PHASE2A1-SEARCH-0001 through -0019;
- 123 occurrences from the bounded citation/lookup closure series
  PHASE2A1-SEARCH-0064 through -0072;
- 2 explicitly labelled primary-source verification occurrences:
  Guntuboyina (2011), linked to PHASE2A1-SEARCH-0013, and Birgé (1982),
  PHASE2A1-SEARCH-0073.

The result windows and all citation occurrences are preserved separately in
`audit/phase2a1_screening_AC.csv`; deduplication never deletes provenance.

## Deterministic matching rules

1. Normalize DOI by lowercasing and removing a leading DOI resolver URL.
2. Match identical normalized DOIs.
3. Treat the arXiv and published records for *Hypothesis Testing via Euclidean
   Separation* as one documented version group because title, authors and
   manuscript are identical and the inspected arXiv source is the accepted
   work behind DOI `10.1214/19-AIHP1022`.
4. When no DOI exists, use an exact normalized title only; generic titled
   records carrying distinct identifiers are not merged.
5. Match corpus DOIs separately and retain the prospective occurrence as
   `DUPLICATE` with the existing stable paper ID.
6. Do not merge the inaccessible 1983 English chapter and the accessible 1982
   French article. They are linked primary versions with distinct publication
   records and evidence depths.
7. Retired OpenAlex reference IDs with no metadata remain separate unresolved
   bibliographic groups; no title, DOI or author is inferred.

## Outcome

- Prospective occurrences: **444**
- Deduplicated bibliographic groups: **380**
- Repeated AC occurrences: **64**
- Existing-corpus duplicate occurrences: **2**
  - `10.1093/jrsssb/qkae011` → P0043
  - `10.1109/TIT.2017.2693198` → P0041
- Total rows whose final disposition is `DUPLICATE`: **66**

Representative-group dispositions are:

- 9 `FULL_TEXT_INCLUDED`;
- 27 `FULL_TEXT_UNAVAILABLE`;
- 342 `FALSE_POSITIVE`;
- 2 existing-corpus duplicates.

No record was deduplicated on topical similarity, author alone, or an inferred
relationship. Every duplicate row names the first occurrence or stable corpus
record in `exclusion_reason`.

Eight occurrences inherited Unicode replacement characters from OpenAlex for
the names/titles Birgé, Österreicher, *métriques/théorie*, *décroissance/
associés* and *ungünstigsten/für*. The ledger spellings were corrected against
authoritative DOI/Numdam metadata; the raw API snapshots remain unchanged.

## Version and access decisions

- Huber and Strassen (1973), Birgé (1983 English chapter), Birgé (2005 lower
  bound) and other inaccessible historical sources retain
  `FULL_TEXT_UNAVAILABLE`; their guarantee fields are not inferred.
- Birgé's 1982 Numdam article is independently `FULL_TEXT_INCLUDED` because its
  exact pp. 70–77 primary text was inspected. It supplies equivalent evidence
  for the constructive non-IID/Markov family without pretending that the 1983
  English chapter was inspected.
- Guntuboyina (2011) is a primary-source verification occurrence, not a
  fabricated hit in the original top-15 OpenAlex result window.

The ledger has no interim `TITLE_ABSTRACT_INCLUDED`,
`DISCOVERED_NOT_SCREENED`, or `AWAITING_VERIFICATION` state.
