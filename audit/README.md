# Audit trail

This directory preserves the review workflow at the paths recorded by the search logs and scripts. Existing audit files were moved here with their original Git blobs and were not rewritten during the structural cleanup.

## Review sequence

1. The pilot review is represented by `pilot_search_report.md`, `pilot_screening.csv`, `pilot_deduplication_log.md`, the cumulative `search_log.md`, and the preserved `raw_search_results/` captures.
2. Phase 2 is represented by the `phase2_search_log*`, `phase2_screening*`, workstream handoffs, deduplication, unresolved-triage, saturation, and progress records. Raw Workstream B captures restored from the tracked files are under `phase2_raw_search_results/B/`.
3. Phase 2A.1 is represented by the `phase2a1_*` screening, closure, deduplication, deferred-record, handoff, and completion files.
4. Phase 3B is represented by `phase3_search_log.md`, `phase3_screening.csv`, `phase3_progress_report.md`, and `phase3_raw_search_results/`. The raw Phase 3 directory follows the A–E families recorded in the search log, with separate `citation_checks/` and `verification/` directories.

Review-wide records include `decision_log.md`, `human_access_requests.md`, `schema_issues.md`, `red_team_protocol.md`, and `migration_report.md`.

`phase2_raw_search_results/phase2_raw_search_results.zip` is preserved exactly as uploaded. Its contents were not independently unpacked or reconciled during this structural pass. The visible Workstream B files are separately restored under the paths expected by the existing scripts.

The next inventory pass should compare the tracked raw-search directories with that archive and identify any missing Phase 2 workstream captures rather than inferring them from filenames.
