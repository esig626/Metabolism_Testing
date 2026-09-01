# Scripts

This directory contains the preserved Perl utilities used for corpus migration, search screening, deduplication, closure, validation, and audit checks.

The scripts were moved from the repository root without source edits. Their existing relative references to `audit/...`, `corpus/...`, and `scripts/...` were used to recover the intended repository layout.

They were not rerun during this structural cleanup. In particular, scripts that require `corpus/papers.csv` cannot currently complete because that canonical file is absent from the tracked tree. The missing corpus should be recovered and verified before those scripts are used.
