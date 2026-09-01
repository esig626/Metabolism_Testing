# Pilot Deduplication Log

## Reconstruction on 2026-07-30

- Inputs: the raw snapshots documented in
  `audit/raw_search_results/README.md`.
- PubMed query occurrences were grouped first by PMID and produced 206 unique
  PubMed records.
- OpenAlex records were normalised by canonical lowercase DOI and merged with
  PubMed records when the DOI matched.
- Retained records found only through the logged citation/supplementary routes
  were added by stable paper ID.
- DOI resolver prefixes were removed before matching. No fuzzy-title merge was
  performed.
- Reconstructed historical ledger: 226 discovered/deduplicated records, 28
  retained records and 198 records with unrecoverable historical decisions.
- Targeted repair addition: P0029 was discovered and screened prospectively,
  producing a current ledger of 227 records and 29 retained papers.
- No original record-level result export survives: exact preserved historical
  query provenance is 0 records and historical provenance is unrecoverable
  for 226 records.
- The 2026-07-30 reruns exactly matched 210 ledger records; 16 historical
  retained records were not found in those reruns. These repair matches use
  `REPAIR-SEARCH-####` identifiers and do not establish original discovery.

The original pilot did not retain record-level screening dispositions for
198 non-retained records. These cannot be reconstructed reliably. The
repaired searches and all subsequent review phases preserve complete
record-level screening decisions prospectively.

No record in the historical-unknown group is coded as a genuine exclusion.
The four count-only Crossref searches contributed no record identifiers and
therefore no rows. SEARCH-0010 could not be rerun because of HTTP 429.
Supplementary web result lists could not be reconstructed. Counts are exact
for the reconstructed ledger, not for every item displayed by all original
services.
