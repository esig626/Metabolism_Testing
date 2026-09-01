# Phase 2A.1 unresolved-record triage handoff

Date: 2026-07-31 UTC  
Input: `audit/phase2_screening.csv`, limited to the 264 occurrences whose
prospective state was `TITLE_ABSTRACT_INCLUDED`  
Corpus link source: `corpus/papers.csv`  
Generator: `scripts/build_phase2_unresolved_triage.pl`

This normalization did not search for literature, alter the Phase 2
occurrence ledger, or make new full-text screening decisions. It treats the
source ledger as occurrence-level provenance and the generated triage table as
paper-level work allocation.

## Supersession note

This document records the **initial triage state before evidence closure**.
Its counts of unresolved records and the queue below are intentionally
preserved as work-allocation history. The final dispositions are in
`audit/phase2_unresolved_triage.csv`,
`audit/phase2a1_priority18_closure.csv`, and the Phase 2A.1 completion
report. No record in the current triage table remains `UNRESOLVED`.

## Normalization result

- Source occurrences: **264**
- Unique paper-level records: **241**
- Repeated search occurrences removed by normalization: **23**
- Unique records already represented in `corpus/papers.csv`: **15**
- Unique records without a stable paper ID: **226**
- Final dispositions carried from existing, inspected corpus evidence:
  **9 `FULL_TEXT_INCLUDED`**
- Records still requiring a final disposition: **232**

Canonical DOI or other identifiers were matched first. Normalized title was a
fallback only when author metadata overlapped, or when an occurrence lacked an
identifier and a sufficiently long exact title and compatible year supported
the match. Distinct identified works were not merged merely because they had a
generic shared title.

## Distribution

Workstream membership counts are A 57, B 25, C 117, D 27 and E 18. Three
records occur in both A and B, so membership counts sum to 244 rather than
241. Exclusive workstream combinations are A 54, A/B 3, B 22, C 117, D 27
and E 18.

Candidate-gap labels are:

- GAP-01 only: 57
- GAP-01 and GAP-03: 82
- Neither GAP-01 nor GAP-03: 102

Evidence depth is:

- `FULL_TEXT_INSPECTED`: 9
- `ABSTRACT_LEVEL`: 5
- `METADATA_OR_LEAD_ONLY`: 1
- `TITLE_ABSTRACT_LEVEL`: 60
- `DISCOVERY_ONLY`: 166

Triage priority is:

- `PRIORITY_1`: 10
- `PRIORITY_2`: 8
- `PRIORITY_3`: 155
- `PRIORITY_4`: 65
- `PRIORITY_5`: 3

Falsification classification is:

- `LOAD_BEARING`: 10
- `POTENTIALLY_LOAD_BEARING`: 8
- `SUPPORTING`: 155
- `PERIPHERAL`: 65
- `FALSE_POSITIVE`: 3

The classification deliberately does not elevate sequential/active tests,
best-arm papers, generic nuisance-parameter chapters, model-discrimination
design criteria, or domain applications to potentially load-bearing status
for the fixed-sample composite-testing question. Exact robust/composite,
fixed-block non-IID, and fixed-sample nuisance-testing leads receive the
highest priorities. This is a triage decision, not evidence that any claimed
result exists.

## Records requiring priority closure

Every row in `audit/phase2_unresolved_triage.csv` preserves its exact source
occurrence IDs and query IDs in `notes`. The complete load-bearing and
potentially load-bearing queue is:

| Unique ID | Source occurrence ID | Triage | Short title |
|---|---|---|---|
| P2UT-0018 | C0402 | LOAD_BEARING | Robust testing for independent non-identically distributed variables and Markov chains |
| P2UT-0026 | C0286 | LOAD_BEARING | Robust hypothesis testing with a single distance |
| P2UT-0027 | C0283 | LOAD_BEARING | Robust hypothesis testing with multiple distances |
| P2UT-0028 | C0285 | LOAD_BEARING | Robust hypothesis testing with repeated observations |
| P2UT-0031 | C0405 | LOAD_BEARING | Testing hypotheses on independent, not identically distributed models |
| P2UT-0123 | C0650 | LOAD_BEARING | Robust hypothesis testing for modeling errors |
| P2UT-0130 | C0653 | LOAD_BEARING | Robust hypothesis testing with composite distances |
| P2UT-0136 | C0656 | LOAD_BEARING | Robust hypothesis testing with alpha-divergence |
| P2UT-0143 | C0483 | LOAD_BEARING | Verifying composite hypotheses with nuisance parameters |
| P2UT-0221 | C0652 | LOAD_BEARING | Robust hypothesis testing with squared Hellinger distance |
| P2UT-0034 | C0235 | POTENTIALLY_LOAD_BEARING | Rank tests in a heteroscedastic linear model with nuisance parameters |
| P2UT-0070 | C0480 | POTENTIALLY_LOAD_BEARING | Sensitivity of score, Wald and likelihood-ratio tests to nuisance parameters |
| P2UT-0073 | C0242 | POTENTIALLY_LOAD_BEARING | Noncoherent detection and nuisance parameters, identified edition 1 |
| P2UT-0075 | C0241 | POTENTIALLY_LOAD_BEARING | Noncoherent detection and nuisance parameters, identified edition 2 |
| P2UT-0099 | C0231 | POTENTIALLY_LOAD_BEARING | Nuisance-parameter tests with invariant power functions |
| P2UT-0124 | C0136 | POTENTIALLY_LOAD_BEARING | Composite hypothesis testing for cooperative spectrum sensing |
| P2UT-0213 | C0664 | POTENTIALLY_LOAD_BEARING | P values and nuisance parameters |
| P2UT-0222 | C0492 | POTENTIALLY_LOAD_BEARING | One-sided likelihood-ratio test with nuisance parameters |

All 18 remain `UNRESOLVED`; none was promoted to a final inclusion from
title, abstract, or metadata alone.

## Reproduction and limitations

The original normalization was generated with:

```sh
perl scripts/build_phase2_unresolved_triage.pl
```

The script requires exactly 264 source occurrences in the included state,
reads both inputs as UTF-8, preserves source spellings, and writes the CSV
through a temporary file. Access is `NOT_ASSESSED` unless an exact existing
paper-corpus link supplies an access state. Authors, access routes and
evidence locations are never inferred.

After closure, the authoritative Phase 2 ledger contains no
`TITLE_ABSTRACT_INCLUDED` occurrences, so the script fails before writing
rather than regenerating or overwriting the curated final triage.

The triage table is not a substitute for the required final dispositions in
the main prospective screening ledger. In particular, the 18 priority
records require primary-source checking or a documented unavailable/excluded
outcome before either GAP-01 or GAP-03 can support a full-review status.
