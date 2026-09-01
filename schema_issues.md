# Pilot Schema Issues

Assessment date: 2026-07-30. These are proposed changes for human review; the
protocol was not amended.

1. `estimated_or_decided_object` lacks `pool_size` and `stopping_time`.
   P0013-P0014 estimate pool sizes; P0025-P0028 optimise stopping implicitly.
2. `experimental_variables_optimised` conflates a biological condition with a
   generic design/control point. Add `input_labelling_pattern`, `control_action`
   and `stopping_rule`.
3. `statistical_criterion` needs `T_optimality`, `Chernoff_information`,
   `error_exponent` and a controlled value for rank/observability criteria.
   Using `other` hides distinctions central to P0005 and P0021-P0028.
4. `statistical_guarantee` mixes evidence type (`simulation_based`,
   `empirical_only`) with mathematical scope (`finite_sample`, `uniform`,
   `minimax`). Separate `result_basis` from `guarantee_scope`.
5. `finite_sample=yes` excludes exact finite-dimensional numerical confidence
   calculations unless accompanied by a theorem. Clarify whether calibrated
   bootstrap/profile procedures count and add `exact_model_based`.
6. `uniform_or_worst_case` is too coarse: P0009 aggregates sampled maps,
   whereas P0024 is explicitly minimax. Add the domain (`sampled_set`,
   `finite_scenario_set`, `continuous_parameter_set`, `distribution_class`).
7. `structural_alternatives` needs subtype and relation: reaction inclusion,
   topology, kinetic mechanism, nested/non-nested, simple/composite and
   overlapping.
8. `multiple_experiments` and `non_iid` need explicit shared-vs-condition-
   specific parameter mappings. P0008 and P0015 share fluxes across tracers;
   P0020 compares condition-specific fluxes.
9. `sample_size_design` should distinguish fixed-budget allocation, stopping
   time, power-based planning, and replicate count.
10. `model_misspecification` needs the misspecified component and whether the
    method detects, models or protects against it (P0016).
11. Software capability fields need evidence-location columns rather than
    putting all provenance into `notes`; licence and maintenance should record
    assessment date in dedicated fields.
12. Paper rows need `access_status`, `retrieval_priority`, `discovery_source`
    and `version_relation`. The current `verification_status` cannot alone
    distinguish paywall from incomplete pilot effort.

Recommended pre-full-review action: amend the schema only after human approval,
log the amendment, and migrate pilot rows with a deterministic script that
preserves the current files and IDs.

## Repair disposition — 2026-07-30

- **Resolved:** Screening now separates `SCREENED_DECISION_UNRECOVERABLE`
  from `EXCLUDED_WITH_RECORDED_REASON`.
- **Resolved:** Query provenance is a separate controlled field; exact query
  IDs are emitted only from preserved raw result membership.
- **Resolved:** Perl generators decode inputs and encode outputs as UTF-8;
  regression tests cover `Möllney`.
- **Resolved:** Corpus schema migration reads and preserves the current CSV,
  unknown columns and curated values; it backs up before replacement and
  refuses duplicate/lost/reordered stable IDs.
- **Resolved:** The migration report records a mechanically detected
  one-column alignment defect in seven new classification fields. The script
  realigned those controlled fields without embedding paper records; a
  post-migration validation reports no remaining vocabulary conflicts.
