# Phase 2A.1 deduplication log — workstreams D–F

Date: 2026-07-31 UTC

## Deterministic rule

Each raw API result and each explicitly recorded access-pass record is retained
as a prospective occurrence. Occurrences are grouped first by normalized DOI
(lowercase, DOI URL prefix removed), otherwise by an explicit stable
repository identifier, otherwise by a Unicode-aware normalized title. The
first occurrence carries the paper-level disposition; later occurrences in
the same group are `DUPLICATE`. Existing `corpus/papers.csv` DOI matches are
also `DUPLICATE` and name the stable corpus ID.

No fuzzy title matching, citation-count heuristic, or inferred DOI was used.
The DOI-less Baraud (2002) anchor is grouped by its normalized exact title.

## Counts

- Prospective source occurrences: **515**
- Unique duplicate groups: **455**
- Duplicate search occurrences: **60**
- `FULL_TEXT_INCLUDED`: **15**
- `FULL_TEXT_UNAVAILABLE`: **4**
- `FALSE_POSITIVE`: **436**
- `DUPLICATE`: **60**
- Records left in an interim screening state: **0**

The high false-positive count reflects deliberately broad citation passes and
top-15 API searches. These records were resolved at title/abstract/citation
context only and are discovery-only; they are not used to support a
substantive claim or an absence conclusion.

## Known corpus duplicate

Gül and Zoubir (2017), DOI `10.1109/TIT.2017.2693198`, is already represented
as `P0041`; its prospective occurrence is therefore `DUPLICATE`. The handoff
flags a possible nuance for the curator: the paper proves a single-observation
saddle result, while Section IV states that minimax robustness of the product
test is not generally guaranteed for `n > 1`.

## Access-limited groups

- Birgé (1983), DOI `10.1007/978-1-4612-5503-1_9`
- Wefelmeyer (1987), DOI `10.1007/978-94-009-3963-9_20`
- Bernshtein (1981), DOI `10.1137/1125037`
- Active hypothesis testing under a POMDP (2024), DOI
  `10.23919/ACC60939.2024.10644574`

All remain `FULL_TEXT_UNAVAILABLE`; no guarantee field should be inferred from
their titles or abstracts.
