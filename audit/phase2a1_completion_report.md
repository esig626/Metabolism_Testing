# Phase 2A.1 Completion Report

Date: 2026-07-31 UTC

Scope: prospective evidence closure and foundational fixed-sample
composite-testing repair. This report does not begin Phase 2B, establish
novelty, or recommend a grant direction.

**Review state: COMPLETE WITHIN THE DOCUMENTED EVIDENCE BOUNDARY.** This
means the narrow Phase 2A.1 falsification and audit tasks are closed on the
verified evidence below. It does not mean that the broader Phase 2 literature
is complete or exhaustively searched.

**Controlling correction:** the prior report incorrectly treated 216
non-priority records as false positives and overstated bounded search
closure. Those dispositions and statements are superseded below. The
original occurrence rows, title/abstract relevance judgements,
methodological-family labels and candidate-gap associations remain
preserved.

## 1. Starting set and bounded disposition

The 264 former `TITLE_ABSTRACT_INCLUDED` occurrences normalise to exactly
**241 unique paper records**; the remaining **23 occurrences** repeat one of
those papers. The source occurrences were not deleted.

Fourteen unique papers received full-text screening: 12 were included and
two were excluded with record-level reasons. The corrected, mutually
exclusive scoped dispositions for all 241 papers are:

| Phase 2A.1 paper-level disposition | Unique papers |
|---|---:|
| `FULL_TEXT_INCLUDED` | 12 |
| `FULL_TEXT_EXCLUDED` | 2 |
| `FULL_TEXT_UNAVAILABLE` | 11 |
| `FALSE_POSITIVE_CONFIRMED` | 2 |
| `DEFERRED_RELEVANT_SUPPORTING` | 60 |
| `DEFERRED_RELEVANT_ADJACENT` | 95 |
| `OUT_OF_SCOPE_FOR_PHASE2A1` | 59 |
| **Total** | **241** |

Thus the reportable full-text-screened count is **14**, including the two
full-text exclusions. The 155 deferred relevant papers remain eligible for
later synthesis after appropriate verification. The 59 records outside this
narrow repair retain their broader-review relevance metadata and are not
excluded from Phase 2. Only two records are confirmed false positives, and
each has a record-level reason showing that it addresses no review question.

`audit/phase2a1_deferred_records.csv` records the original Phase 2 state,
scoped Phase 2A.1 disposition, broader-review relevance, deferral reason,
later-synthesis eligibility and current evidence depth. Deferred records may
indicate a literature family but cannot support definitive synthesis until
their full text and claim location are verified.

## 2. Corrected Phase 2 occurrence ledger

The main ledger still contains 1,937 occurrences in its original order. Its
current state accounting is:

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

The single `AWAITING_VERIFICATION` record is the pre-existing OpenAlex
reference `W6604903323`; it supports no synthesis claim. The corrected
scoped dispositions do not convert a title/abstract relevance judgement
into a full-text exclusion.

## 3. Prospective foundational search and verified anchors

Seventy-three `PHASE2A1-SEARCH-####` operations covered testing between
sets, Le Cam/Birgé/Hellinger tests, Fano/Assouad/packing lower bounds,
nuisance parameters and fixed designs, nonparametric/high-dimensional
testing, and fixed-block information-theoretic converses. The separate
prospective ledger preserves 959 occurrences in 781 conservative
bibliographic groups: 22 `FULL_TEXT_INCLUDED`, 30
`FULL_TEXT_UNAVAILABLE`, 727 individually screened `FALSE_POSITIVE`
representatives, and 180 `DUPLICATE` occurrences. These counts are separate
from the 241-paper historical Phase 2 triage.

Twenty-five distinct primary full texts were screened during Phase 2A.1:
22 foundational inclusions, one additional non-overlapping priority
inclusion, and two priority full-text exclusions. Twenty-three verified
papers were integrated as P0052–P0074. The corpus contains 74 ordered stable
paper IDs, 57 with inspected primary full text.

The strongest affirmative anchors are:

- P0053 and P0060: constructive fixed-sample composite tests, including
  uniform error control for their stated convex, separated or heterogeneous
  product classes;
- P0065, P0071 and P0072: robust-neighbourhood or Hellinger-margin tests and
  their stated finite-sample bounds or overlap conditions; and
- P0056, P0059 and P0069: two-point, packing/entropy, Rényi and fixed-block
  converse machinery.

These verified results reject broad claims that generic fixed-sample
composite tests or generic converse tools are missing. This conclusion is
based on existing positive results, not on an unreturned search result.

## 4. GAP-01 and GAP-03

### GAP-01 — `WEAKENED`

- Existence of fixed-sample tests for composite mechanism classes:
  `ESTABLISHED` for the verified represented classes.
- Uniform finite-sample guarantees: `ESTABLISHED` under the source
  assumptions.
- Nonlinear EMU-induced family construction and certified testing:
  `COMPUTATIONAL GAP`.
- Tracer/intervention/replicate optimisation: `COMPUTATIONAL GAP`.
- Independent heterogeneous blocks: established at the probability-theory
  level; exact shared-nuisance EMU representation remains computational.

The residual is affirmative and limited: certified representation of
nonlinear EMU law images, computation of least-favourable pairs, and nested
experimental-design optimisation.

### GAP-03 — `WEAKENED`

Generic exact-overlap, divergence, minimax packing and design-specific
converse templates are established by verified primary results. The
residual concerns computing valid opposing pairs, packings, constants and
global outer-design optima for EMU-induced families. It is not justified as
missing general converse theory.

All seven registered gaps remain `WEAKENED`; their evidence-type boundaries
are recorded in `synthesis/candidate_gaps.md`.

## 5. Search-closure and access boundary

The searches were bounded and relevance-ranked. Direct database operations
usually exported only the top 15 results from much larger reported sets;
citation passes were truncated; `PHASE2A1-SEARCH-0068` received Semantic
Scholar HTTP 429 and was not retried. The 1983 English Birgé chapter,
Bernshtein (1981), the 2024 fixed-budget POMDP paper, and other listed
load-bearing texts remain unavailable.

Query families D–F are `INCOMPLETELY_SEARCHED`. For the other foundational
families, verified anchors establish positive existence results, but no
claim is made that an additional load-bearing family does not exist.
Controlled states and family-specific limits are in
`audit/phase2_saturation_log.md`.

The bounded search verified the principal foundational method families
needed to reject broad claims that generic fixed-sample composite tests and
converse tools are absent. It did not establish exhaustive coverage or
literature saturation.

## 6. Completion boundary

Phase 2A.1 closes the narrow falsification question: verified general theory
substantially weakens GAP-01 and GAP-03. It does not close the entire Phase 2
literature. Any later Phase 2B synthesis must remain within
`protocol/phase2b_evidence_boundary.md`; deferred records may be revisited
whenever they could materially affect a proposed contribution.

This report establishes an evidence-bounded handoff, not an exhaustive
review, and does not itself begin Phase 2B.

## 7. Final completion validation

The final completion gate checked the authoritative ledgers, curated corpus,
controlled gap statuses and evidence boundary together:

- all five relevant regression suites passed, including **17,560 assertions**
  after the final UTF-8 regression was added;
- the Phase 2 audit validator passed for all 1,937 authoritative
  occurrences;
- 25 CSV files containing 6,957 data rows parsed as strict UTF-8;
- P0001–P0074 and S0001–S0017 remain stable and ordered, and nonblank paper
  DOIs remain unique;
- the 241-paper triage, 229-row scoped ledger and 216 explicit correction
  transitions reconcile exactly;
- all seven candidate gaps remain `WEAKENED`;
- family-level transfer classifications that cannot be decided from the
  bounded evidence are `UNRESOLVED FROM CURRENT EVIDENCE`, not inferred
  theoretical-necessity claims;
- the known OpenAlex mojibake for `Begüm D. Topçuoğlu` is normalised in the
  derived source and authoritative ledgers, with a regression check;
- Phase 1 audit files and the raw Phase 2 source snapshots were not rewritten;
  and
- `git diff --check` passed.

Eleven papers have the scoped disposition `FULL_TEXT_UNAVAILABLE`; this is a
disposition count, not a claim that only eleven records have any access
limitation. Deferred evidence remains qualified under
`protocol/phase2b_evidence_boundary.md`.

No commit is made by this completion report.
