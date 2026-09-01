# Decision Log

Append consequential protocol, scope, interpretation, schema, and synthesis
decisions. Do not use this log to conceal or overwrite earlier decisions.

## Entry template

- **Decision ID:** DEC-####
- **Date (UTC):** YYYY-MM-DD
- **Decision maker:**
- **Decision:**
- **Rationale:**
- **Evidence:** Evidence record IDs, audit entries, or protocol sections
- **Alternatives considered:**
- **Consequences:** Files, records, candidate gaps, or searches affected
- **Uncertainty or dissent:**
- **Revisit trigger:**

## DEC-0001

- **Date (UTC):** 2026-07-30
- **Decision maker:** Codex `/root`
- **Decision:** Treat Phase 1 as a bounded protocol-stress test: retain 28
  primary papers and 8 software packages, while preserving abstract-only and
  metadata-only verification states.
- **Rationale:** The requested pilot size and category diversity were reached;
  pretending all records were fully verified would violate completion gates.
- **Evidence:** P0001-P0028; S0001-S0008; SEARCH-0001-SEARCH-0040.
- **Alternatives considered:** Expand into a full review; omit inaccessible
  anchors.
- **Consequences:** Inaccessible records remain retrieval priorities and do
  not solely support substantive synthesis.
- **Uncertainty or dissent:** Citation-network screening was bounded and
  Google Scholar was unavailable.
- **Revisit trigger:** Full-review search or access to additional primary
  texts.

## DEC-0002

- **Date (UTC):** 2026-07-30
- **Decision maker:** Codex `/root`
- **Decision:** Reject CLAIM-01, CLAIM-02, CLAIM-03, CLAIM-04 and CLAIM-06;
  weaken CLAIM-05 and GAP-02, GAP-03 and GAP-05.
- **Rationale:** Direct primary work establishes rational/EMU/robust/parallel
  tracer design and software, while adjacent and isotope literature narrow
  the remaining guarantee-level distinctions.
- **Evidence:** P0004-P0009, P0015, P0018-P0019, P0024-P0028; S0001-S0008.
- **Alternatives considered:** Leave all claims unassessed until the full
  review.
- **Consequences:** Candidate distinctions must be phrased at the level of
  decision objects and guarantees, not broad method absence.
- **Uncertainty or dissent:** These are pilot outcomes, not final novelty
  conclusions; several nearest papers are not fully verified.
- **Revisit trigger:** Full-text verification, expanded citation chaining, or
  discovery of a closer isotope-specific method.

## DEC-0003

- **Date (UTC):** 2026-07-30
- **Decision maker:** Codex `/root`
- **Decision:** Amend the evidence schema with separate criterion, guarantee,
  robustness, converse, stopping, structural-alternative, parameter-sharing,
  retrieval, access and screening fields.
- **Rationale:** The hostile review showed that the original fields permitted
  sampled robustness, asymptotic bounds, identifiability obstructions and
  access depth to be conflated.
- **Evidence:** Hostile-review comments; `audit/schema_issues.md`;
  P0018, P0024, P0026-P0028.
- **Alternatives considered:** Record distinctions only in notes.
- **Consequences:** Both corpus tables were migrated without changing stable
  IDs; reproducible migration/rebuild scripts are in `scripts/`.
- **Uncertainty or dissent:** Controlled vocabularies may need further
  amendment after the second go/no-go review.
- **Revisit trigger:** Schema review before any Phase 2 work.

## DEC-0004

- **Date (UTC):** 2026-07-30
- **Decision maker:** Codex `/root`
- **Decision:** Downgrade every consequential guarantee or software
  capability lacking inspected primary text and an exact location.
- **Rationale:** Abstracts, metadata and unversioned landing pages cannot
  establish theorem scope or implemented capability.
- **Evidence:** P0004, P0008, P0019, P0025; S0001-S0008.
- **Alternatives considered:** Preserve strong fields with an “unverified”
  note.
- **Consequences:** Synthesis and gap assessments were rewritten; no
  conclusion relies on the downgraded claims.
- **Uncertainty or dissent:** Some downgraded capabilities may be real but
  require versioned documentation or execution.
- **Revisit trigger:** Retrieval or direct execution.

## DEC-0005

- **Date (UTC):** 2026-07-30
- **Decision maker:** Codex `/root`
- **Decision:** Close automated retrieval for the nine named records and
  request manual retrieval only for P0008, P0015, P0016, P0021, and P0022.
- **Rationale:** Only those five materially block a candidate-gap or transfer
  assessment; equivalent inspected evidence makes the others supporting or
  nonessential.
- **Evidence:** `audit/human_access_requests.md`; P0005-P0007, P0014, P0018,
  P0024, P0026-P0028.
- **Alternatives considered:** Repeated automated retries; treating abstracts
  as complete methodological evidence.
- **Consequences:** All nine remain `full_text_inspected=no`; no guarantee
  field is promoted.
- **Uncertainty or dissent:** Manual copies could change narrower
  classifications, but cannot be anticipated from abstracts.
- **Revisit trigger:** A legally obtained complete primary text.

## DEC-0006

- **Date (UTC):** 2026-07-30
- **Decision maker:** Codex `/root`
- **Decision:** Replace hard-coded corpus rebuilding with a preservation-only
  migration that validates schema/order, writes a temporary file, creates a
  timestamped backup, reports conflicts/manual-review values, and refuses
  replacement on lost, duplicate, or reordered IDs.
- **Rationale:** Curated evidence must remain the source of truth; schema
  evolution cannot recreate it from script literals.
- **Evidence:** `scripts/rebuild_phase1_corpus.pl`,
  `tests/test_phase1_migration.pl`, `audit/migration_report.md`.
- **Consequences:** No paper records are embedded in the migration. Existing
  values and unknown columns survive unchanged; controlled-vocabulary
  anomalies are reported rather than silently repaired.
- **Revisit trigger:** Any future evidence-schema amendment.

## DEC-0007

- **Date (UTC):** 2026-07-30
- **Decision maker:** Codex `/root`
- **Decision:** Encode the 198 historical outcomes as
  `SCREENED_DECISION_UNRECOVERABLE`, with no exclusion reason, and encode
  retained records without demonstrated raw-query evidence as
  `PROVENANCE_UNRECOVERABLE`.
- **Rationale:** Non-retention is not evidence of an exclusion decision, and a
  plausible search route is not record-level provenance.
- **Evidence:** `audit/pilot_screening.csv`,
  `scripts/build_pilot_screening.pl`.
- **Consequences:** Original-pilot screening is not presented as a
  reproducible screening flow. Prospective decisions remain distinguishable.
- **Revisit trigger:** Recovery of an original raw export or decision ledger.

## DEC-0008

- **Date (UTC):** 2026-07-30
- **Decision maker:** Codex `/root`
- **Decision:** Classify GAP-06 and GAP-07 as WEAKENED after bounded hostile
  falsification.
- **Rationale:** P0029 establishes adjacent robust model-discrimination
  design under misspecification; official software evidence establishes many
  components of the alleged software absence. Remaining questions are
  narrower structural-error theory and integration/engineering.
- **Evidence:** P0029; S0001-S0008; SEARCH-0076-SEARCH-0077.
- **Consequences:** Neither gap is protected by absence language or described
  as novel.
- **Revisit trigger:** Full text for P0015-P0016 or execution-level software
  verification.

## DEC-0009

- **Date (UTC):** 2026-07-30
- **Decision maker:** Codex `/root`
- **Decision:** Eliminate semantic field-realignment heuristics from the
  corpus migration and separate original historical discovery provenance
  from exact 2026-07-30 repair-rerun matches.
- **Rationale:** Controlled-vocabulary membership cannot identify an intended
  column, and equivalent rerun query text cannot establish historical
  record-level provenance.
- **Evidence:** `scripts/rebuild_phase1_corpus.pl`,
  `scripts/build_pilot_screening.pl`, hostile-review finding 3.
- **Consequences:** Any invalid controlled value aborts before output or
  replacement. Rerun matches use `REPAIR-SEARCH-####`; historical IDs remain
  blank unless demonstrated by an original preserved export.
- **Revisit trigger:** Recovery of an original raw export or an intentional
  schema amendment.

## DEC-0010

- **Date (UTC):** 2026-07-31
- **Decision maker:** Codex `/root`, after independent workstreams A–E.
- **Decision:** Keep every Phase 2 search occurrence, query ID, raw result
  snapshot and screening disposition prospectively separate from the Phase 1
  historical ledger.
- **Rationale:** A prospective review can preserve record-level decisions
  without implying that query occurrences are globally unique papers or
  repairing historical provenance.
- **Evidence:** `audit/phase2_search_log.md`,
  `audit/phase2_screening.csv`, and the workstream-specific ledgers.
- **Consequences:** Phase 2 counts distinguish occurrences, within-workstream
  deduplication groups, retained corpus rows and evidence depth. Phase 1
  screening files remain unchanged.
- **Revisit trigger:** A later phase may add new prospective searches under
  new identifiers, but must not reuse Phase 2A occurrence IDs.

## DEC-0011

- **Date (UTC):** 2026-07-31
- **Decision maker:** Codex `/root`, after independent evidence audit.
- **Decision:** Treat T/KL/Fisher/posterior and max-min criterion optimality
  separately from calibrated statistical decision guarantees.
- **Rationale:** Exact characterisation or numerical optimisation of a design
  criterion does not establish finite-sample Type-I/Type-II control,
  sufficiency, sample complexity or impossibility.
- **Evidence:** P0038–P0044 and P0048–P0051 at their recorded theorem,
  equation and method locations.
- **Consequences:** Transfer of several design families is classified as
  computational adaptation, while only the narrower fixed-block,
  continuous-composite guarantee questions remain possible theoretical
  extensions.
- **Revisit trigger:** Primary evidence for an EMU-specific calibrated test,
  certified maximin solver, or matching converse.

## DEC-0012

- **Date (UTC):** 2026-07-31
- **Decision maker:** Codex `/root`.
- **Decision:** Retain `SURVIVES FULL REVIEW` only for the narrowed GAP-01
  fixed-block two-error problem and GAP-03 fixed-block converse problem;
  classify GAP-02 and GAP-04–GAP-07 as `WEAKENED`.
- **Rationale:** Direct isotope structural inference and substantial
  biochemical/decision-theory/software prior work falsify all broader
  formulations. The surviving formulations identify continuous composite
  overlap, shared nuisance, fixed/batched design and converse requirements
  explicitly.
- **Evidence:** `synthesis/candidate_gaps.md`; P0030–P0051; S0001–S0017.
- **Consequences:** These are non-novel evidence statuses, not a grant
  recommendation.
- **Revisit trigger:** Additional load-bearing primary work or a formal
  assumption check that directly covers either residual formulation.

## DEC-0013

- **Date (UTC):** 2026-07-31
- **Decision maker:** Codex `/root`, responding to the hostile Phase 2A
  methodological review.
- **Decision:** Withdraw the `SURVIVES FULL REVIEW` dispositions for GAP-01
  and GAP-03, restore both to `UNRESOLVED`, and suspend affected saturation
  claims before beginning Phase 2A.1 analysis.
- **Rationale:** The Phase 2 ledger contains unresolved
  title/abstract-included records, including foundational fixed-sample
  composite-testing and converse candidates. Those records and the
  Le Cam/Birgé/Fano/Assouad, metric-entropy, nuisance-parameter and
  fixed-design theory families must be resolved before an absence,
  extension, or saturation conclusion is supportable.
- **Evidence:** Hostile Phase 2A review; `audit/phase2_screening.csv`;
  `audit/phase2_progress_report.md`; `audit/phase2_saturation_log.md`.
- **Consequences:** Phase 2B is blocked. Phase 2A.1 prospectively records
  evidence closure and foundational-theory searches under distinct
  identifiers.
- **Revisit trigger:** Completion of the Phase 2A.1 registered stopping
  rules and primary-source verification.

## DEC-0014

- **Current status:** **SUPERSEDED IN PART BY DEC-0015.** The positive
  verified-theory findings remain; the automatic false-positive accounting,
  family-exhaustion wording and unconditional Phase 2B-readiness conclusion
  do not.
- **Date (UTC):** 2026-07-31
- **Decision maker:** Codex `/root`, after independent Phase 2A.1
  fixed-sample-theory and record-closure workstreams.
- **Decision:** Close the 241-record unresolved triage, classify GAP-01 and
  GAP-03 as `WEAKENED`, and treat the broad fixed-sample composite-test and
  converse families as boundedly saturated for those two registered
  falsification hypotheses. Do not claim global Phase 2 saturation.
- **Rationale:** The 264 included occurrences were normalised to 241 unique
  records and all received final dispositions. Independent-source searches
  and bounded citation passes verified constructive uniform composite tests,
  independent heterogeneous-product tests, exact robust-neighbourhood tests,
  and finite-sample two-point, packing, entropy, sample-complexity, and
  fixed-block converses. These results falsify the proposed absence of
  generic fixed-sample theory. The remaining EMU distinction is certified
  representation and nested global computation over nonlinear law images,
  shared nuisance constraints, and mixed experimental designs.
- **Evidence:** P0053, P0056, P0059–P0060, P0065, P0069, P0071–P0072;
  `audit/phase2_unresolved_triage.csv`;
  `audit/phase2a1_screening.csv`;
  `analyses/fixed_sample_composite_testing_foundations.md`;
  `analyses/gap01_component_assessment.md`;
  `analyses/gap03_converse_assessment.md`.
- **Alternatives considered:** Restore a full-review survival status because
  no EMU-labelled theorem was found; keep both gaps unresolved until every
  inaccessible historical theorem is manually retrieved.
- **Consequences:** Neither GAP-01 nor GAP-03 is a surviving theoretical-gap
  claim. All seven gap hypotheses are `WEAKENED`; Phase 2A evidence can
  proceed to Phase 2B synthesis, but this decision neither starts Phase 2B
  nor recommends a grant direction. The Phase 2 ledger now requires an
  explicit reason for every final non-inclusion; the E-D0100 WUFlux
  `FULL_TEXT_UNAVAILABLE` reason is preserved in its generator and output.
- **Uncertainty or dissent:** Eleven priority triage records and 30
  representatives in the separate foundational ledger are full-text
  unavailable. The exact 1983 English Birgé chapter, Bernshtein (1981), and
  2024 fixed-budget POMDP theorem remain unverified. Wefelmeyer (1987) is
  excluded from this repair as asymptotic from the official abstract. No
  substantive conclusion relies on these inaccessible sources. The fixed-
  budget POMDP subfamily and unrelated Phase 2 workstream access limits are
  not declared saturated.
- **Interpretation correction:** Convexification is decision-theoretically
  exact for worst-case test risk because each error is linear in the law;
  taking each family's convex hull does not change any test's supremum risk
  or the minimax value. A convex-hull intersection can nevertheless be
  witnessed by mixtures rather than one physical metabolic parameterisation.
  This replaces the earlier AC handoff wording that suggested
  convexification necessarily weakens the testing problem.
- **Revisit trigger:** Primary text showing a materially different
  fixed-sample theorem, or an executed EMU formulation demonstrating that
  the residual cannot be handled by established tests and converses plus
  computational adaptation.

## DEC-0015

- **Date (UTC):** 2026-07-31
- **Decision maker:** Codex `/root`, responding to the hostile Phase 2A.1
  methodological review.
- **Decision:** Supersede the automatic-false-positive, search-saturation and
  unconditional Phase 2B-readiness portions of DEC-0014. Preserve
  non-priority records according to explicit scoped dispositions; retain the
  affirmative conclusion that verified general fixed-sample tests and
  converse tools weaken GAP-01 and GAP-03; and require any later Phase 2B
  synthesis to follow `protocol/phase2b_evidence_boundary.md`.
- **Rationale:** Non-priority for the narrow GAP-01/GAP-03 repair is not
  evidence that a record is irrelevant to the broader review. In addition,
  top-ranked result windows, truncated citation passes, an unretried HTTP 429
  and unavailable texts cannot establish exhaustive coverage. The verified
  anchors support positive existence claims without a literature-absence
  premise.
- **Evidence:** Hostile Phase 2A.1 review;
  `audit/phase2_unresolved_triage.csv`;
  `audit/phase2a1_deferred_records.csv`;
  `audit/phase2_saturation_log.md`; P0053, P0056, P0059–P0060, P0065,
  P0069, P0071–P0072.
- **Consequences:** Of the 241-paper triage, 12 records are full-text
  included, two full-text excluded, 11 unavailable, two confirmed false
  positives, 60 deferred relevant supporting, 95 deferred relevant
  adjacent, and 59 outside the narrow Phase 2A.1 repair. Deferred records
  remain in the broader evidence base and cannot carry definitive claims
  until verified. The bounded operations are documented as such; query
  families D–F are `INCOMPLETELY_SEARCHED`. Phase 2A.1 closes only the
  narrow broad-theory falsification question and does not begin Phase 2B.
- **History:** DEC-0014 remains visible as the decision that generated the
  superseded accounting. Its positive verified-theory findings remain in
  force; its 216-record false-positive closure, family-exhaustion wording and
  unconditional readiness conclusion do not.
- **Revisit trigger:** A deferred paper materially affects a proposed
  contribution, a missing primary text becomes legally available, or a later
  search is prospectively authorised under a new protocol phase.

## DEC-0016

- **Date (UTC):** 2026-07-31
- **Decision maker:** Codex `/root`, after independent accounting,
  synthesis-boundary and technical audits.
- **Decision:** Mark Phase 2A.1 complete only within
  `protocol/phase2b_evidence_boundary.md`. Retain all seven candidate gaps as
  `WEAKENED`; treat the verified fixed-sample and converse results as
  affirmative gap-destroying evidence; and use `UNRESOLVED FROM CURRENT
  EVIDENCE` wherever the bounded sources do not determine whether an
  EMU-specific transfer is direct, computational or theoretical.
- **Rationale:** The scoped screening repair now reconciles all 241 unique
  papers without excluding deferred relevant evidence, and verified primary
  anchors refute broad missing-theory premises. However, truncated searches,
  inaccessible texts and deferred records cannot support an absence claim or
  a general claim that new theory is required.
- **Evidence:** `audit/phase2a1_completion_report.md`;
  `audit/phase2_saturation_log.md`;
  `audit/phase2a1_deferred_records.csv`;
  `protocol/phase2b_evidence_boundary.md`; P0053, P0056, P0059–P0060,
  P0065, P0069 and P0071–P0072.
- **Consequences:** Phase 2A.1 supplies an auditable, bounded evidence base
  for a later synthesis, but this decision does not begin Phase 2B, claim
  saturation or novelty, recommend a grant direction, or make deferred
  papers irrelevant.
- **Quality-control correction:** The derived ROOT-D0177 author metadata is
  normalised from mojibake to `Begüm D. Topçuoğlu`; the raw OpenAlex snapshot
  remains unchanged and the exact-record transformation is encoded in the
  deterministic source-ledger builder.
- **Revisit trigger:** A later proposed contribution depends materially on a
  deferred record, a presently inaccessible load-bearing source becomes
  available, or a prospectively authorised search changes the nearest-prior
  comparison.

## DEC-0017

- **Date (UTC):** 2026-08-01
- **Decision maker:** Codex `/root`, during the bounded Phase 3B
  exact-formulation search.
- **Decision:** Register GAP-08 and classify it `PARTIALLY ADDRESSED`. Record
  zero `EXACT FORMULATION` papers in the bounded retained set; keep direct
  PCA/ICA, ordinary differential-analysis and machine-learning papers as
  `APPLICATION WITHOUT THEORY`; keep specified-family non-identification and
  composite tests as `GENERIC THEORY ONLY`; and require an experiment-induced
  family construction/applicability proof before calling the residual purely
  computational.
- **Rationale:** Primary full texts establish direct flux-free isotope-profile
  discrimination, shared-flux multi-MID fitting, analytical uncertainty
  propagation, isotope structural non-identifiability, target prediction
  despite parameter non-identifiability, generic non-identification-robust
  tests, EMU forward maps and exact fragment equivalences. These components
  occur in separate formulations. The checked sources do not combine them
  with the complete biological/technical hierarchy and finite-sample
  metabolic-class risk.
- **Evidence:** Phase 3 rows P3-0001–P3-0023 in
  `audit/phase3_screening.csv`; exact source locations in
  `analyses/phase3_exact_match_matrix.md`; query and citation-neighborhood
  audit in `audit/phase3_search_log.md`.
- **Consequences:** GAP-08 is neither closed by the existence of a generic
  theorem nor asserted novel from a zero exact-match count. A synthetic proof
  of concept may declare missing hierarchy/noise/correction assumptions, but
  it cannot report an empirical sample size for the two source studies. The
  Phase 2 positive-theory evidence remains intact; only its direct-MID
  transfer interpretation is narrowed.
- **Record-identity boundary:** `P3-####` identifiers are stable within the
  Phase 3B retained-evidence register but are not canonical `P####` corpus
  assignments. Existing crosswalks are preserved; new canonical assignments
  and full-schema corpus integration are deferred to a separately scoped
  pass rather than guessed or silently renumbered here.
- **Uncertainty or dissent:** Search windows and citation passes were bounded;
  several publisher records/supplements were inaccessible; and terminology is
  heterogeneous. No result count or inaccessible source is used as absence
  evidence. Classifying Zamboni, DIMet, X13CMS, Weindl, Frahm, Bleuler,
  MIAMI and IMPACT as applications reflects the rule that they do not
  construct the relevant probability family or guarantee, despite being
  substantive empirical or workflow precedents.
- **Revisit trigger:** Primary full text provides an essentially complete
  direct-MID hierarchical class-test formulation; replicate-level lineage and
  MID data become available; or a proof establishes that a verified generic
  theorem applies to the declared pipeline-induced families.
