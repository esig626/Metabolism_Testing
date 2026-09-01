# Phase 2A.1 corpus-row proposal handoff

Date: 2026-07-31

## Scope and preservation

This handoff proposes corpus rows for every unique `FULL_TEXT_INCLUDED`
record in:

- `audit/phase2a1_screening_AC.csv`;
- `audit/phase2a1_screening_DEF.csv`; and
- `audit/phase2a1_priority18_closure.csv`.

It does not modify `corpus/papers.csv`. The proposed rows are in
`audit/phase2a1_corpus_row_proposals.csv` and use the current
`corpus/papers.csv` header and controlled vocabularies without a schema
change.

The three inputs contain 27 included occurrences representing 23 unique
papers. Four included occurrences repeat papers already included through a
different ledger. None of the 23 unique DOI/title identifiers duplicated the
51-record pre-merge corpus baseline inspected when this proposal was
prepared. A separate preservation-aware merge may subsequently make these
rows appear in the working `corpus/papers.csv`; that is expected and is not a
second set of records.

| Input | Included occurrences | New unique papers | Proposed IDs |
|---|---:|---:|---|
| A–C ledger | 9 | 9 | P0052–P0060 |
| D–F ledger | 15 | 13 | P0061–P0073 |
| Priority-18 closure | 3 | 1 | P0074 |
| Total | 27 | 23 | P0052–P0074 |

## Deterministic ID assignment

IDs follow first occurrence order: A–C ledger order, then previously unseen
D–F records in D–F ledger order, then previously unseen priority-18 records.
Cross-ledger repeats resolve to the ID assigned at first occurrence.

| Proposed ID | Included source record(s) | DOI or authoritative identifier |
|---|---|---|
| P0052 | A1AC-0001; A1DEF-0107 | 10.1214/13-ejs766 |
| P0053 | A1AC-0037 | 10.1214/15-ejs1054 |
| P0054 | A1AC-0039 | 10.1214/10-aos817 |
| P0055 | A1AC-0043 | 10.1214/18-aos1701 |
| P0056 | A1AC-0147; A1DEF-0128 | 10.1214/18-ejs1419 |
| P0057 | A1AC-0232 | 10.1214/19-aihp1022 |
| P0058 | A1AC-0252 | 10.1214/16-ejs1170 |
| P0059 | A1AC-0443 | 10.1109/tit.2011.2110791 |
| P0060 | A1AC-0444 | Numdam ASCFM_1982__71_20_70_0 |
| P0061 | A1DEF-0004 | 10.1080/10618600.2021.2020128 |
| P0062 | A1DEF-0061 | 10.1080/01621459.1994.10476836 |
| P0063 | A1DEF-0122 | 10.1214/18-aos1729 |
| P0064 | A1DEF-0286 | 10.1016/j.jeconom.2005.06.007 |
| P0065 | A1DEF-0337; C0656 / P2UT-0136 | 10.1109/tsp.2016.2569405 |
| P0066 | A1DEF-0339 | ORBilu 10993/40202 |
| P0067 | A1DEF-0342 | 10.1214/aos/1046294463 |
| P0068 | A1DEF-0383 | 10.1214/12-ejs667 |
| P0069 | A1DEF-0427 | 10.1109/tit.2010.2043769 |
| P0070 | A1DEF-0509 | 10.1073/pnas.1922664117 |
| P0071 | A1DEF-0510; C0652 / P2UT-0221 | 10.5281/zenodo.54502 |
| P0072 | A1DEF-0511 | PMLR v130:theertha-suresh21a |
| P0073 | A1DEF-0512 | 10.48550/arXiv.2602.19803 |
| P0074 | C0650 / P2UT-0123 | 10.1109/icassp.2013.6638718 |

The four repeated included occurrences are therefore A1DEF-0107,
A1DEF-0128, C0656 / P2UT-0136, and C0652 / P2UT-0221. They must point to
P0052, P0056, P0065, and P0071 respectively rather than create additional
paper rows.

## Evidence and coding decisions

- All 23 rows record a primary full-text location. Guarantee coding follows
  the inspected result rather than wording in the title or abstract.
- P0052 is coded `global_asymptotic`, not finite-sample, because its matching
  separation-rate statements retain asymptotic terms.
- P0061 is coded `simulation_based`, not finite-sample, because the
  simulation-trained procedure does not prove uniform finite-sample error
  control.
- Average-error finite-hypothesis converses (notably P0054 and P0056) are not
  promoted to uniform composite Type-I/Type-II guarantees.
- Minimax coding is `partial` where the inspected result is a
  theorem-specific comparison or an average-risk reduction rather than a
  general minimax identity.
- Positive non-IID coding is limited to papers with inspected heterogeneous
  product/block results: P0053, P0057, P0058, P0060, and P0068.
- Robust-neighbourhood results are coded for their stated dominated
  divergence or Hellinger classes, not as results over exact nonlinear
  EMU-induced law families.
- P0057 uses the peer-reviewed 2020 citation and DOI while identifying the
  inspected author-manuscript source in `evidence_location` and `notes`.
- P0073 is explicitly a 2026 preprint. It must not be represented as
  peer-reviewed evidence.
- No row is coded as directly testing metabolic structural alternatives.

Three rows use `doi=NR` because the inspected authoritative record did not
report a DOI: P0060 (Numdam), P0066 (ORBilu), and P0072 (PMLR). Their
authoritative identifiers and URLs are retained. The remaining 20 DOI values
are unique within the proposal and do not collide with the existing corpus.

## Validation performed

- Parsed 23 data rows against the exact 49-column corpus header.
- Confirmed the stable proposed-ID sequence P0052–P0074 with no gaps,
  duplicates, or reordering.
- Validated controlled vocabularies and boolean/status fields against
  `protocol/evidence_schema.md`.
- Confirmed all row keys are known corpus fields and no current corpus column
  is missing.
- Checked normalized DOI values against the 51-record pre-merge
  `corpus/papers.csv`; no collisions were found.
- Checked UTF-8 sentinels including `Gül`, `Birgé`, `Loubès`, and `Verdú`.
- Scanned for common mojibake patterns; none were found.

The proposal is ready for a preservation-aware merge. Before merging, the
consolidated screening ledger should map all repeated occurrences above to
their single proposed stable ID.
