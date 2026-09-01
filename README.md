# Reconstructed Pilot Raw Search Results

These files preserve structured snapshots from repair reruns using query text
equivalent to the original SEARCH-0001 through SEARCH-0015. They are not
original historical exports. Reconstruction date: 2026-07-30 UTC.

- `SEARCH-0001`–`SEARCH-0006` filenames correspond to
  `REPAIR-SEARCH-0001`–`REPAIR-SEARCH-0006`: complete PubMed ESearch JSON with
  `retmax=10000`.
- `pubmed_unique_esummary.json`: metadata for the 206 unique PubMed IDs in
  those six searches.
- `SEARCH-0007`–`SEARCH-0009` filenames correspond to
  `REPAIR-SEARCH-0007`–`REPAIR-SEARCH-0009`: Crossref count-only responses.
- `SEARCH-0010` corresponds to `REPAIR-SEARCH-0010` and was unavailable because Crossref returned
  HTTP 429; the original count remains in `audit/search_log.md`.
- `SEARCH-0011`–`SEARCH-0014` filenames correspond to
  `REPAIR-SEARCH-0011`–`REPAIR-SEARCH-0014`: OpenAlex rerun JSON.
- `SEARCH-0015` corresponds to `REPAIR-SEARCH-0015`: OpenAlex work/citation snapshot for the Crown–Antoniewicz
  seed.

All rerun records retain `HISTORICAL_PROVENANCE_UNRECOVERABLE` and blank
historical query IDs because no original result export was preserved. Their
demonstrated matches and `REPAIR-SEARCH-####` IDs are recorded separately.
Retained historical records outside the rerun union are marked
`NOT_FOUND_IN_REPAIR_RERUN`. P0029 is a
prospective targeted-repair record and is marked
`MANUAL_CITATION_DISCOVERY`.

Generate the screening ledger with:

```text
perl scripts/build_pilot_screening.pl
```

The ledger is not a reproducible screening flow for the original pilot and is
not described as PRISMA-compliant.
