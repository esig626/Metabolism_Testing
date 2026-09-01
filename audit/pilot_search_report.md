# Phase 1 Controlled Pilot Search Report — Repaired

Date: 2026-07-30. No Phase 2 search was conducted.

## Reconstructed discovery ledger

- Historical records reconstructed: **226**.
- Prospectively discovered and screened during this repair: **1** (P0029).
- Current discovery ledger: **227**.
- Retained primary papers: **29**.
- Genuine recorded exclusions: **0**.
- Historical screening decisions unrecoverable: **198**.
- Software packages retained and separately audited: **8**.
- Exact preserved historical query provenance: **0**.
- Historical provenance unrecoverable: **226**.
- Exact matches in the 2026-07-30 repair reruns: **210**.
- Not found in the repair reruns: **16**.
- Manual discovery: **1** (P0029; prospective repair).

The original pilot is not represented as a reproducible screening flow and
these are not PRISMA counts. The governing historical limitation is recorded
once in `audit/pilot_deduplication_log.md`.

## Evidence depth

- Primary full text inspected: **13** — P0002, P0005-P0007, P0009, P0011,
  P0014, P0018, P0024, P0026-P0029.
- Abstract-only: **12** — P0001, P0003-P0004, P0008, P0010, P0013,
  P0015-P0016, P0019, P0021-P0023.
- Metadata-only: **4** — P0012, P0017, P0020, P0025.

New full-text verification in this repair: P0018, P0026, P0027 and P0028.
P0024 was rechecked and its citation corrected.

## Category coverage

| Category | Retained count |
|---|---:|
| Classical MFA/EMU/identifiability | 7 |
| Tracer and measurement design | 6 |
| Robust/Bayesian uncertainty | 6 |
| Validation/structural selection | 4 |
| Time-course/multi-experiment/scale | 8 |
| Adjacent design/testing/controlled sensing | 9 |

Records can occur in more than one category.

## Corrections from hostile review

- P0018 DOI corrected and its identifiability obstruction tied to Theorem 4.
- P0024 year/pages/DOI corrected from the author manuscript’s journal record.
- P0028 venue and DOI corrected to *Sequential Analysis*,
  `10.1080/07474946.2021.1912525`.
- P0008 DOI corrected from an unrelated article to
  `10.1016/j.ymben.2013.08.006`.
- P0025’s converse, non-IID and sample-size claims were removed as unverified.
- Strong fields in abstract/metadata-only rows were downgraded to `unclear`
  or `no`.
- P0026-P0028 retain guarantee fields only with exact section,
  proposition/theorem locations.
- Metran and other software capabilities without location-specific direct
  evidence were downgraded.
- Historical non-retained records are now
  `SCREENED_DECISION_UNRECOVERABLE`, never exclusions.
- Synthetic query ranges were removed. Exact repair-rerun matches use
  `REPAIR-SEARCH` identifiers and remain distinct from unrecoverable original
  historical provenance.
- UTF-8 decoding and encoding are regression-tested with `Möllney`.

## Candidate gaps and transfer

- GAP-01: SURVIVES PILOT ONLY.
- GAP-02: WEAKENED.
- GAP-03: WEAKENED.
- GAP-04: SURVIVES PILOT ONLY.
- GAP-05: WEAKENED.
- GAP-06: WEAKENED.
- GAP-07: WEAKENED.

P0029 verifies robust T-optimal discrimination under parameter
misspecification, leaving only structural EMU forward-error classes
unresolved. GAP-07 remains **WEAKENED** because audited platforms already
provide much of the component stack; the missing integration is mainly
engineering unless it implements a separately unresolved guarantee.

T-optimal and classical sequential transfer remain unresolved from current
evidence. KL design is applicable with computational adaptation. Robust
maximin, Bayesian discrimination, active testing, controlled sensing and
composite testing require nontrivial theoretical extensions in the stated
EMU formulation. Details and precise obstructions are in
`analyses/adjacent_method_transfer.md`.

## Bounded access outcome

Manual retrieval is requested only for P0008, P0015, P0016, P0021 and P0022.
P0004, P0019 and P0023 are supporting, and P0025 is nonessential; their
unsupported fields remain downgraded and automated retrieval is closed.
Exact blocked claims are registered in `audit/human_access_requests.md`.

## Scaling statement

The repaired pilot can proceed to a second hostile go/no-go review. It **does
not authorize or begin Phase 2**. This is a process assessment, not a novelty
conclusion and not a grant recommendation.
