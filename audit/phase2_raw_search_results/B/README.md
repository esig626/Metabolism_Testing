# Workstream B raw-search material

All files in this directory were created prospectively on 2026-07-31 UTC.
They are separate from Phase 1 provenance.

- `PHASE2-SEARCH-0011`–`0014` are the initial PubMed/OpenAlex exports.
- PHASE2-SEARCH-0015 and 0016 were supplementary web-routing searches whose
  sources exposed neither a native result export nor a total count.
  `P0031-juser-record.html` preserves the official institutional record
  reached for 0015; `P0032-arxiv-metadata.xml` preserves the official arXiv
  metadata reached for 0016. These primary-routing pages verify the retained
  works but do not reconstruct the unexported search-result universes.
- `PHASE2-SEARCH-0100_crossref.json` is the first 50 records from the logged
  Crossref query; Crossref reported 529,007 total results. The unexported tail
  is not claimed as screened.
- `PHASE2-SEARCH-0101_*` and `0102_*` preserve the anchor, backward-reference
  and forward-citation OpenAlex responses for P0030 and P0031.
- `PHASE2-SEARCH-0110-0112_web_snapshot.json` and
  `PHASE2-SEARCH-0114_web_snapshot.json` are structured transcriptions of
  bibliographic records visible in supplementary web-search responses.
  Those sources exposed neither a total count nor a native export. The
  combined 0110–0112 file contains separately keyed entries for
  PHASE2-SEARCH-0110, 0111 and 0112; these snapshots are explicitly not
  represented as database-native raw exports.
- `PHASE2-SEARCH-0112_Liu-arxiv-fulltext.html` is the legal arXiv full text
  inspected for the Liu–Maini–Baker article, whose final DOI and publication
  status were separately verified against ScienceDirect and the Oxford
  University Research Archive.
- `PHASE2-SEARCH-0113_*` preserves exact PubMed metadata and complete PMC
  BioC text for Borah Slater et al. (PMCID PMC9996240).
- `PHASE2-SEARCH-0114_PMC3516143-fulltext.xml`,
  `PHASE2-SEARCH-0115_PMC3563641-fulltext.xml`, and
  `PHASE2-SEARCH-0116_PMC3946009-fulltext.xml` are complete PMC BioC primary
  texts for Flassig and Sundmacher, Stegmaier et al., and Vanlier et al.

Every bibliographic occurrence in the saved database exports and structured
web snapshots has a prospective disposition in
`audit/phase2_screening_B_audit.csv`. The same ledger contains one distinct
software record, ModelDiscriminationToolkitGUI, discovered in the inspected
PHASE2-SEARCH-0115 primary paper and verified at its official project route.
Index pages, author profiles and navigation-only pages are not bibliographic
records and are not counted.
