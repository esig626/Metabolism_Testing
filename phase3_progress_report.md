# Phase 3B progress report

Date: 2026-08-01 UTC

Scope: bounded exact-formulation prior-art review of the direct-MID decision
problem.

Decision boundary: no literature-saturation, novelty or grant recommendation
is made.

## Completion status

All five planned search families were run in at least two sources:

| Family | Sources searched | Principal primary full texts checked |
|---|---|---|
| A. Direct MID-level inference | PubMed, OpenAlex, supplementary browser discovery | Zamboni 2004; X13CMS 2014; Weindl 2016; Frahm 2020; MIAMI 2020; DIMet 2024; IMPACT 2025; Bleuler 2007 |
| B. Testing without parameter identification | PubMed, Europe PMC, OpenAlex, supplementary browser discovery | Isermann 2003; Cedersund 2012; Todem et al. 2010; Andrews & Mikusheva 2016; Sundqvist 2022 |
| C. Network-coupled parallel observations | PubMed, OpenAlex, Crossref, supplementary browser discovery | Crown et al. 2015; Schellenberger 2012; Sundqvist 2022; Antoniewicz et al. 2007; MIAMI 2020; IMPACT 2025 |
| D. Hierarchical experimental pipeline | PubMed, OpenAlex, supplementary browser discovery | Mairinger et al. 2018; Zhang et al. 2023; DIMet 2024; qSIP 2020; IMPACT 2025 |
| E. Geometry of induced families | PubMed, OpenAlex, supplementary browser discovery | Wiechert & Wurzel 2001; Isermann 2003; Rantanen 2006; Antoniewicz et al. 2007; Schellenberger 2012 |

The exact queries, counts, filters and retained counts are in
`audit/phase3_search_log.md`; retained-paper dispositions are in
`audit/phase3_screening.csv`; machine-readable captures are under
`audit/phase3_raw_search_results/`.

The `P3-####` values are stable retained-evidence identifiers within this
Phase 3B workstream, not canonical `corpus/papers.csv` record IDs. Existing
canonical mappings are recorded where available. Assigning new `P####` IDs
and completing every full corpus-schema field is deferred to a separately
scoped corpus-integration pass; the Phase 3 IDs must not be silently
renumbered or represented as canonical corpus records in the meantime. The
current register contains only retained primary papers. Key potentially
category-changing citation neighbours have paper-level dispositions in the
search-log appendix; all other query-result and citation-neighbour exclusions
remain search-occurrence provenance rather than canonical corpus exclusions.

## Stopping-rule audit

1. **Two sources per family:** satisfied, as shown above.
2. **Principal exact and partial matches checked in primary full text:**
   satisfied for the principal matches. No exact match was found. Abstract-
   only or inaccessible papers were not used to establish substantive claims.
3. **Backward and forward checks from the closest matches:** satisfied as a
   bounded category-stability check. Reference lists and OpenAlex forward
   records were screened from Zamboni, Schellenberger, Cedersund, Isermann,
   Sundqvist, Crown, Mairinger, Zhang, DIMet, Weindl, MIAMI and IMPACT. They
   added direct applications and estimation/design variants but no new
   structural formulation category or joined coverage cell. The operational
   categories, counts and indexing discrepancies are recorded in the search
   log.
4. **GAP-08 classification not based on one keyword query:** satisfied. The
   classification triangulates direct analysis, isotope identifiability,
   mechanistic non-identification, generic tests, parallel-MFA coupling,
   analytical uncertainty and induced-map geometry.

This stopping decision says that the executed search was sufficient for the
bounded classification below. It does not say the literature is saturated.

## Classification totals

| Required category | Verified retained primary papers | Interpretation |
|---|---:|---|
| EXACT FORMULATION | 0 | no checked paper contains the essentially complete conjunction |
| PARTIAL FORMULATION | 11 | substantive forward-map, non-ID, parallel-fit, uncertainty or target-set components |
| GENERIC THEORY ONLY | 3 | testing results for already specified probability/moment families |
| APPLICATION WITHOUT THEORY | 8 | direct isotope-profile processing/comparison/classification without the relevant law or guarantee |
| ADJACENT BUT NONTRANSFERABLE | 1 | qSIP power/error work with a different primary measurement process |

The zero exact count is bounded to the retained set and citation neighborhoods;
it is not a universal absence or novelty claim.

## Closest prior formulations

No retained paper dominates every defining axis.

- **Closest direct empirical precedent:** Zamboni & Sauer (2004), P3-0009,
  because corrected multi-fragment mass-isotope profiles directly discriminate
  mutants/conditions without a flux/network fit. It has no calibrated class
  test or network-coupled probability law.
- **Closest explicit mode-of-action application:** MIAMI (2020), P3-0022,
  because it detects thresholded MID changes, creates similarity/reference
  networks and proposes metabolic targets. Its user-defined threshold is not
  a calibrated class test and the displayed network is not a shared-latent
  law.
- **Closest mathematical class/geometry precedent:** Schellenberger et al.
  (2012), P3-0001, because high/low feasible-flux classes are mapped into
  multiple fragment-MDV clouds even when full flux recovery is limited. Its
  sampled `Z` score is not a finite-sample composite test.
- **Closest probabilistic network model:** Zhang et al. (2023), P3-0002,
  because repeated isotopomer vectors have an explicit nonlinear-network
  likelihood. Flux/kinetic parameters are targets and only one residual level
  is modeled.
- **Closest parallel shared-state workflow:** Crown et al. (2015), P3-0004,
  and Sundqvist et al. (2022), P3-0003/P0030. They jointly fit MIDs through
  shared fluxes for estimation or model validation.
- **Closest analytical-pipeline uncertainty model:** Mairinger et al. (2018),
  P3-0005, which propagates raw ion/integration/correction errors but does not
  separate the complete experimental hierarchy.

## GAP-08 assessment

**GAP-08 — Construction, geometry and operational testing of experimentally
induced network-coupled MID families**

**Status: PARTIALLY ADDRESSED.**

| Subquestion | Evidence-bounded answer | Principal evidence |
|---|---|---|
| A. Complete culture-to-MID pipeline formalised probabilistically? | No complete model verified. Analytical propagation and one-level isotope likelihoods cover parts of it. | P3-0005, P3-0002 |
| B. Metabolic-class testing separated from flux estimation? | Direct flux-free discrimination/comparison exists; formal network-induced metabolic-class testing was not verified. | P3-0009–P3-0014, P3-0022–P3-0023; P3-0001 partial analogue |
| C. Testing under flux non-identifiability studied? | Structural flux non-ID, target/core-prediction identification and generic non-ID tests exist separately; their isotope-class conjunction was not verified. | P3-0006, P3-0015–P3-0018 |
| D. Several fragment MIDs as parallel composite evidence coupled by one latent state? | Shared-state multi-MID simulation/fitting exists for design and estimation; a direct parallel composite class test was not verified. | P3-0001, P3-0003–P3-0004, P3-0008 |
| E. Biological and technical levels distinguished in finite-sample guarantees? | No retained isotope paper verified the full hierarchy with such a guarantee. | P3-0002, P3-0005; negative boundary from inspected full texts |
| F. Geometry, ordering, support and least-favourable structure characterised? | Forward maps, stability, identifiability, fragment equivalence and sampled images are partial prior art; full law-image geometry and least-favourable structure remain unresolved. | P3-0001, P3-0006–P3-0008, P3-0020 |

The allowed status `GENERIC THEORY ONLY` is too weak for GAP-08 overall because
substantive isotope-specific partial formulations exist. `EXACT PRIOR ART
FOUND` is not supported because the required conjunction is absent from every
checked record.

## Structural components still unaddressed in combination

- a declared primary sampling unit and its independent-replication semantics;
- one probability model spanning batch, culture, sibling fraction,
  preparation, injection, fragment/MID and ion levels;
- raw-ion/correction/missingness support tied to fragment atom maps;
- metabolic classes defined as sets of observation laws rather than fitted
  flux point estimates;
- a shared flux/nuisance constraint across every measured fragment and
  fraction without treating coordinates as biological replicates;
- an overlap/separation or partial-identification analysis for those induced
  law families;
- least-favourable states/distributions or a certified alternative;
- finite-sample class error, prospective biological sample requirement, and
  an insufficiency conclusion when the classes overlap; and
- validation against replicate-level rather than summary MIDs.

The two source manuscripts do not report enough lineage and variance metadata
to instantiate these items empirically. Their unresolved fields remain listed
in `problem/source_information_gaps.md` and were not replaced by assumptions.

## Does an actual theoretical programme remain?

**Yes, as an unresolved programme under the current evidence—not as a verified
novelty claim.** A defensible programme would:

1. declare the primary sampling unit and construct the experiment-specific
   joint law from culture lineage through raw ions/correction to sibling MIDs;
2. define metabolic classes as constrained sets of those laws while retaining
   nonidentifiable flux and technical nuisance;
3. characterize or certify class overlap, separation, support and shared-
   state dependence;
4. prove that an existing generic detector theorem applies, or state the
   narrower additional result needed when its assumptions fail; and
5. derive finite-sample error/sample requirements under a declared hierarchy,
   with synthetic proof of concept until replicate-level metadata are
   available.

It is premature to call this merely a computational gap. Applicability of an
existing theorem to the actual pipeline-induced family has not been proved.
Once a representation and applicability result exist, particular detector or
global-optimisation steps may turn out to be computational.

## Quality-control state

- Generic theory is classified separately from isotope-specific prior art.
- MFA estimation is not classified as direct metabolic-class testing.
- Ordinary multiple testing is separated from shared-state parallel composite
  testing.
- Sampling units and independence are not inferred from “replicated” or
  “repeated.”
- Fragments, isotopologues and ions are not counted as biological replicates.
- Fitted fluxes remain downstream estimators/derived quantities, not primary
  observations.
- `git diff --check` is required at final handoff and its result will be added
  to the final response rather than retroactively altering this audit entry.
