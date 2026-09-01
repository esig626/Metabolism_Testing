# Curated corpus

This directory is reserved for the canonical curated paper and software evidence tables defined by the review protocol.

A current `corpus/papers.csv` is not present in the tracked tree. This is a substantive inventory gap, not something filled during reorganisation. The existing `audit/migration_report.md` records that a 29-row `corpus/papers.csv` existed during the Phase 1 migration on 2026-07-30, and the scripts still treat that path as canonical.

Historical `papers` snapshots are preserved under `archive/migrations/data/backups/`. Phase 2A.1 corpus-row proposals and their handoff are preserved in `audit/phase2a1_corpus_row_proposals.csv` and `audit/phase2a1_corpus_row_handoff.md`. Neither source is silently promoted here to the canonical current corpus.

The next inventory pass should determine whether the missing current corpus can be recovered exactly from tracked history or an archive before any corpus-dependent script is run.
