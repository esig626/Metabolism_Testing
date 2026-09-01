# Phase 2A Search-Closure Log

Date of controlling correction: 2026-07-31 UTC

This file retains the required path from the Phase 2 protocol, but it no
longer treats a bounded search as evidence that a literature family has been
exhausted. The earlier Phase 2A.1 family-exhaustion wording is withdrawn
because it overstated a relevance-ranked, truncated search. It is superseded
by the controlled search-closure states below.

## Controlled search-closure states

- `ANCHOR_FAMILIES_VERIFIED`: primary full text verifies the principal
  method families needed for the stated positive conclusion.
- `BOUNDED_SEARCH_COMPLETE`: the predeclared bounded operations were
  executed and recorded; this is not an exhaustiveness claim.
- `YIELD_DECLINING_NOT_SATURATED`: the bounded searches produced fewer new
  relevant families late in the sequence, but the protocol stopping rules
  were not met.
- `INCOMPLETELY_SEARCHED`: material search, citation, screening, or access
  work remains.
- `NOT_ASSESSED`: no defensible family-level closure assessment has been
  made.

## Phase 2A.1 operation boundary

The Phase 2A.1 search series executed 73 recorded operations. Direct query
families generally exported only the relevance-ranked top 15 OpenAlex or
Crossref records even when the database reported hundreds, thousands, or
millions of matches. These exported windows are screened occurrences, not
the searched universe. Citation passes were also bounded: examples include
25 of 96 Guntuboyina citations, 25 of 318 Berger–Boos citations, 25 of 264
Dufour citations, 25 of 152 Baraud citations, and 25 of 3,885 Polyanskiy,
Poor and Verdú citations. The second Semantic Scholar Birgé query
(`PHASE2A1-SEARCH-0068`) returned HTTP 429 and was not retried.

The bounded operations found and verified primary anchors for constructive
fixed-sample composite tests, heterogeneous-product tests, robust
neighbourhood tests, and several finite-sample converse techniques. This
affirmative evidence is enough to reject broad claims that generic
fixed-sample composite-testing or converse machinery is absent. It does not
establish that no additional method family exists.

## Current family assessments

| Family or closure gate | Controlled state | Positive evidence established | Boundary preventing a stronger state |
|---|---|---|---|
| Execution of the registered Phase 2A.1 bounded operations | `BOUNDED_SEARCH_COMPLETE` | Exact queries, exported windows, raw files and prospective screening decisions are preserved | Completion of the bounded plan is not exhaustive coverage |
| Testing between sets and convex composite hypotheses | `ANCHOR_FAMILIES_VERIFIED` | P0053/P0057/P0058 verify constructive uniform fixed-sample methods under their stated represented classes | Direct searches exported top-15 windows from much larger result sets; citation passes were bounded |
| Le Cam/Birgé/Hellinger and metric-separated tests | `ANCHOR_FAMILIES_VERIFIED` | P0060 and P0071–P0072 verify robust or separated-class constructions at their recorded strength | The 1983 English Birgé chapter is unavailable; citation retrieval was truncated; the Semantic Scholar retry failed with HTTP 429 |
| Fano, Assouad, finite-packing and metric-entropy converses | `ANCHOR_FAMILIES_VERIFIED` | P0056/P0059/P0069 verify two-point, multiple-point, packing, entropy and fixed-block converse forms | Direct result windows and Guntuboyina citation passes were truncated |
| Nuisance parameters and fixed heterogeneous designs | `INCOMPLETELY_SEARCHED` | P0053/P0060/P0062/P0064/P0068/P0070 verify selected heterogeneous-product and nuisance-handling results | Bernshtein (1981) remains unavailable; generic Type-I results do not by themselves give uniform two-error control; top-15 and citation windows were bounded |
| Nonparametric and high-dimensional minimax testing | `INCOMPLETELY_SEARCHED` | P0063/P0066–P0068 verify selected class-specific upper and lower bounds | Only bounded result and citation windows were screened; class-specific assumptions limit transfer |
| Fixed-block information-theoretic converses | `INCOMPLETELY_SEARCHED` | P0056/P0059/P0069 verify selected nonasymptotic fixed-block converse tools | Large direct result sets and citation networks were truncated; no exhaustive method-family assessment was made |
| Fixed-budget active-design/POMDP subfamily | `INCOMPLETELY_SEARCHED` | Official metadata and repository routes identify the subfamily | The 2024 primary conference text remains unavailable |
| Broader Phase 2 literature | `NOT_ASSESSED` | Phase 2A and Phase 2A.1 provide verified anchors in several workstreams | Deferred relevant records, workstream-specific access limits and incomplete search families preclude an exhaustiveness claim |

The exact 1983 English Birgé chapter, Bernshtein (1981), and the 2024
fixed-budget POMDP paper remain unavailable and cannot support theorem-level
claims. Other access limits are retained in the completion report. Query
families D–F are `INCOMPLETELY_SEARCHED`; the absence of an additional
method family has not been established for them or for the review as a
whole.

## Narrow Phase 2A.1 conclusion

The bounded search verified the principal foundational method families
needed to reject broad claims that generic fixed-sample composite tests and
converse tools are absent. It did not establish exhaustive coverage or
literature saturation. The narrow falsification question can therefore be
closed affirmatively—existing general theory weakens GAP-01 and GAP-03—
without an absence claim.

Any Phase 2B synthesis must apply
`protocol/phase2b_evidence_boundary.md`. Deferred or inaccessible records
remain capable of changing a proposed residual contribution and cannot be
used to support definitive claims until verified.
