# Phase 2A Workstream A Handoff

Audit date: 2026-07-31 UTC. Scope: tracer, measurement, parallel-experiment,
robust and dynamic 13C-MFA experimental design only. No corpus or shared
synthesis file was modified in this audit.

## Prospective-search and screening audit

- Search IDs audited: **15** — PHASE2-SEARCH-0001 through 0010 and
  PHASE2-SEARCH-0056 through 0060.
- Raw JSON snapshots validated: **17** (the 15 discovery/citation snapshots
  plus two PubMed metadata companions).
- Result occurrences: **548**.
- Exact normalized DOI/identifier-or-title keys across both Workstream A
  ledgers: **375**. This is a within-workstream comparison, not a global
  unique-work count.
- Screening states across both ledgers:
  - `FULL_TEXT_INCLUDED`: **6** occurrences;
  - `FULL_TEXT_UNAVAILABLE`: **1**;
  - `TITLE_ABSTRACT_INCLUDED`: **64**;
  - `TITLE_ABSTRACT_EXCLUDED`: **337**;
  - `DUPLICATE`: **140**.
- The commissioned Crown–Antoniewicz EMU anchor was inspected directly and
  is not an additional result occurrence; including it, **7 unique primary
  full texts** support this workstream.
- Every occurrence has a permitted prospective screening state. Every
  exclusion has a non-empty reason. Search date and query ID are present for
  every row.
- All searches were executed prospectively on 2026-07-31. None is assigned
  Phase 1 provenance.

Identifier-keyed inclusion and duplicate aliases are encoded in the base
generator, while the closure generator applies its documented title rule and
ledger-local DOI/title deduplication. Regeneration is deterministic. The 140
`DUPLICATE` states are the sum of the two ledgers' local duplicate decisions;
the separate 375-key comparison identifies cross-ledger overlap without
rewriting those prospective states. Raw snapshots, query IDs and occurrences
were not removed or rewritten.

## Load-bearing evidence gate

| Primary paper | Ledger/corpus relationship | Exact inspected location | Claim permitted |
|---|---|---|---|
| Crown & Antoniewicz (2012), doi:10.1016/j.ymben.2011.12.005 | Commissioned anchor; existing P0005 | Sections “EMU coefficient sensitivities and tracer experiment design strategy” and “Comparison of tracers for mammalian network model”; §4 Conclusions | EMU rank/sensitivity and D-optimality guide tracer choice for flux observability/precision; no mechanism-error or finite-sample guarantee |
| Crown, Ahn & Antoniewicz (2012), doi:10.1186/1752-0509-6-43 | A0004; existing P0006 | “EMU coefficient sensitivities and tracer experiment design strategy”; “Comparison of tracers for mammalian network model”; Methods “Metabolic flux analysis”; Conclusions | Heuristic EMU sensitivity rules plus simulated profile-CI comparison for flux precision |
| Walther et al. (2012), doi:10.1016/j.ymben.2011.12.004 | A0011; existing P0007 | §2.1 equations (1)–(5); §3.1; reported selected-flux perturbation exercise | Genetic optimisation of tracer-mixture composition for nonlinear-CI precision; selected perturbations are not uniform robustness |
| Nöh et al. (2018), doi:10.1371/journal.pcbi.1006533 | A0002; existing P0036 | Methods “General framework,” equation (1); “Covariance-based information measures,” equations (7)–(14); Cost model; Figures 4–8 | Pareto coupling of tracer, platform, measurement group, technical repetition/error and cost using local A/D/E/Fisher criteria |
| Crown, Long & Antoniewicz (2016), doi:10.1016/j.ymben.2016.06.001 | A0148/A0172 occurrences; existing P0037 | §2.1 precision-score definition; §2.2 synergy-score definition; §4.1–4.3; Conclusions | Parallel-tracer ranking for joint flux precision; “synergy” is not mechanism power or sufficiency |
| Beyß et al. (2021), doi:10.3389/fbioe.2021.685323 | A0001; existing P0009 | §2.4 equations (3)–(8), Algorithm 1; §3.2.1 equations (9)–(11); §3.2.2 Algorithm 2; Figure 3; §4 | Median D-score and identifiability coverage over sampled flux maps; not uniform robustness over the polytope |
| Wahl, Nöh & Wiechert (2008), doi:10.1186/1471-2105-9-152 | AC closure inclusion; new-row proposal below | “Measurement model,” equations (4)–(5); “Statistical evaluation,” equation (10); “Sampling and quality”; Conclusion | Fixed 19-time-point dynamic simulation and linearised kinetic-parameter information comparison; not optimised sampling or sample-size design |

Every definitive Workstream A claim is bounded by one of these inspected
locations. Abstract-only records are retained only as supporting leads.

## Retained-row proposals

These are proposals for the corpus curator, not edits made by Workstream A.

1. **Update evidence detail without changing stable IDs** for P0005, P0006,
   P0007 and P0009 using the exact locations and guarantee boundaries above.
   Their existing high-level classifications are consistent with the audit.
2. **P0036 metadata correction required:** DOI verification identifies the
   open full text as PMCID `PMC6209137`; the current corpus URL points to
   `PMC6226191`. Preserve P0036 and correct only the URL after curator review.
3. **P0037 metadata correction required:** DOI verification identifies the
   open full text as PMCID `PMC5891732`; the current corpus URL points to
   `PMC5131839`. Preserve P0037 and correct only the URL after curator review.
4. **Propose one new supporting primary row** for Wahl SA, Nöh K, Wiechert W.
   “13C labeling experiments at metabolic nonstationary conditions: An
   exploratory study.” *BMC Bioinformatics*. 2008;9:152.
   doi:10.1186/1471-2105-9-152. Code the decided object as kinetic parameters,
   the design variables as `none` (sampling times are fixed, not optimised),
   the criterion as local Fisher/covariance information, guarantee regime as
   `simulation_based;local_asymptotic`, sample-size design as `no`, and use
   the exact locations in the table above.
5. **Retain as awaiting verification, not as a strong evidence row:** Nöh K,
   Wiechert W. “Experimental design principles for isotopically instationary
   13C labeling experiments.” *Biotechnology and Bioengineering*.
   2006;94(2):234–251. doi:10.1002/bit.20803. The complete primary text was
   not legally retrieved; no exact algorithm, design-variable or guarantee
   coding should be inferred from its abstract.

Supporting candidates such as IsoDesign, COMPLETE-MFA, optimal measurement
sets, Designer Labels and multi-flux-map tracer evaluation remain
title/abstract leads. They should not be promoted to load-bearing corpus rows
without full-text extraction.

## Corrected search-closure assessment

The correct-anchor forward pass, six-anchor backward pass, bounded OpenAlex
and Crossref dynamic-design searches, and Nöh forward-citation pass recovered
local FIM/covariance design, EMU rank/sensitivity, mixture optimisation,
multi-objective cost/information, parallel precision scoring, sampled-flux
robustification and dynamic information design. These searches are
`BOUNDED_SEARCH_COMPLETE`, not exhaustive.

The dynamic-design family remains `INCOMPLETELY_SEARCHED`. The load-bearing
2006 Nöh–Wiechert full text remains unavailable after the previously
documented legal access attempts, and result/citation windows were bounded.
The exact “almost optimal” time-design formulation cannot presently support
definitive synthesis. No further automated retry was made because the source
is already an explicit manual access request and repeated inaccessible-source
retries are not evidence.

This access block limits only claims about the exact historical dynamic
time-point design method. It does not weaken the verified conclusion that
the inspected tracer-design literature optimises flux/parameter information
and precision rather than calibrated mechanism-discrimination error,
biological replicate power or impossibility.
