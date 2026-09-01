# Phase 2A Progress Report

Date of controlling update: 2026-07-31 UTC

This update supersedes the earlier Phase 2A.1 accounting that classified 216
non-priority papers as false positives. It preserves the prospective Phase 2
occurrences and the original title/abstract relevance judgements. It does
not begin Phase 2B, establish novelty, or make a grant recommendation.

**Current state:** Phase 2A.1 is complete within
`protocol/phase2b_evidence_boundary.md`. The broader Phase 2 literature
remains incompletely assessed, and no saturation or exhaustive-coverage
claim follows from this handoff.

## Prospective Phase 2 evidence base

- Logged Phase 2 search identifiers: **91**.
- Consolidated Phase 2 occurrence rows: **1,937**.
- Workstream occurrences: **A 548; B 410; C 760; D 119; E 100**.
- Paper corpus: **74** ordered stable records, **57** with inspected primary
  full text.
- Software corpus: **17** verified platforms.
- Phase 2A.1 prospective operations: **73**.
- Separate Phase 2A.1 foundational occurrences: **959**, in **781**
  conservative bibliographic groups.

Occurrence, bibliographic-group and stable-corpus counts describe different
units and are not combined into a unique-paper total.

## Corrected unresolved-record triage

The original 264 `TITLE_ABSTRACT_INCLUDED` occurrences represent exactly
**241 unique papers** and **23 duplicate search occurrences**. Fourteen
unique papers were fully screened: 12 were included and two were excluded.
The corrected paper-level accounting is:

| Scoped disposition | Unique papers |
|---|---:|
| `FULL_TEXT_INCLUDED` | 12 |
| `FULL_TEXT_EXCLUDED` | 2 |
| `FULL_TEXT_UNAVAILABLE` | 11 |
| `FALSE_POSITIVE_CONFIRMED` | 2 |
| `DEFERRED_RELEVANT_SUPPORTING` | 60 |
| `DEFERRED_RELEVANT_ADJACENT` | 95 |
| `OUT_OF_SCOPE_FOR_PHASE2A1` | 59 |
| **Total** | **241** |

The 155 deferred relevant records and 59 records outside the narrow repair
retain their original relevance, method-family and candidate-gap metadata.
They are not excluded from the broader review and remain eligible for later
verification. Until verified, they cannot support a definitive method,
guarantee, converse, absence or novelty statement.

## Current Phase 2 occurrence states

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

Every confirmed false positive and every prospective exclusion has a
record-level reason. The single `AWAITING_VERIFICATION` occurrence is the
pre-existing OpenAlex reference `W6604903323` and supports no synthesis
claim.

## Phase 2A.1 foundational evidence

The separate Phase 2A.1 ledger contains 22 `FULL_TEXT_INCLUDED`, 30
`FULL_TEXT_UNAVAILABLE`, 727 individually screened `FALSE_POSITIVE`
representatives and 180 `DUPLICATE` occurrences. Across this ledger and the
priority closure, 25 distinct primary full texts were screened during
Phase 2A.1.

Verified anchors establish:

- constructive fixed-sample tests and uniform error bounds for stated
  convex, separated, robust-neighbourhood and heterogeneous-product classes;
  and
- exact-overlap, divergence, finite-packing, metric-entropy, Rényi and
  fixed-block converse techniques.

These positive results weaken broad missing-theory formulations of GAP-01
and GAP-03. They do not imply that all adjacent families were found.

## Candidate-gap status

| Gap | Current status | Evidence-bounded interpretation |
|---|---|---|
| GAP-01 finite-sample EMU mechanism discrimination | `WEAKENED` | General fixed-sample composite tests exist; residual certified nonlinear-EMU representation and design optimisation are computational |
| GAP-02 uniform flux/structural guarantees | `WEAKENED` | Generic guarantees and isotope estimation methods exist; the joint EMU decision formulation remains qualified |
| GAP-03 converse-guided isotope design | `WEAKENED` | Generic overlap, divergence, packing and fixed-block converse tools exist; EMU pair/packing/constants and outer-design computation remain |
| GAP-04 joint experimental design | `WEAKENED` | Existing design components weaken a missing-method claim; integration and computation remain |
| GAP-05 multi-condition non-IID discrimination | `WEAKENED` | Heterogeneous-product theory exists; shared-nuisance metabolic construction remains computational |
| GAP-06 forward-model misspecification | `WEAKENED` | General misspecification methods exist; an EMU discrepancy class and computation remain unresolved |
| GAP-07 decision-oriented open software | `WEAKENED` | Existing platforms supply many components; the residual is principally integration, usability and reproducibility |

No gap status is justified by literature exhaustion or by treating a
deferred record as negative evidence.

## Search-closure and access limits

The Phase 2A.1 queries were bounded and relevance-ranked. Most direct
database searches exported only the top 15 results from much larger result
sets. Citation passes were truncated, the Semantic Scholar Birgé query
`PHASE2A1-SEARCH-0068` returned HTTP 429 and was not retried, and several
potentially load-bearing texts remain unavailable. Query families D–F are
`INCOMPLETELY_SEARCHED`.

The bounded search verified the principal foundational method families
needed to reject broad claims that generic fixed-sample composite tests and
converse tools are absent. It did not establish exhaustive coverage or
literature saturation. Detailed controlled closure states are recorded in
`audit/phase2_saturation_log.md`.

## Transition boundary

Phase 2A.1 closes the narrow GAP-01/GAP-03 falsification question on
affirmative verified evidence. It does not close the entire Phase 2
literature. Phase 2B may use this evidence only within
`protocol/phase2b_evidence_boundary.md`; deferred records must be revisited
when they materially affect a proposed contribution.

This is an evidence-bounded handoff statement, not the start of Phase 2B.
