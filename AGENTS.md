# Binding Project Instructions

These instructions apply to every future Codex task in this repository. Inspect
this file and all relevant existing files before making changes.

## Scientific purpose

This repository supports a critical, reproducible review of computational and
statistical methods for designing and analysing stable-isotope
metabolic-tracing experiments, with primary emphasis on 13C metabolic flux
analysis (13C-MFA). The review must determine what is established, genuinely
new, or unresolved and identify a defensible methodological gap for a FY2027
JSPS Early-Career Scientists proposal.

The applicant's myeloma/stromal-cell, SLC25A10-deficient HEK293T, and
SDH-b-deficient chromaffin-cell datasets are possible future case studies.
They must not predetermine the review conclusion.

## Evidence and citation standards

- Treat every novelty claim and candidate gap as a hypothesis to falsify.
- Do not make or repeat an unsupported novelty, priority, absence, or
  "unexplored area" claim.
- Trace every substantive synthesis claim to one or more evidence rows and,
  through them, to an exact evidence location in a source.
- Prefer primary methodological papers. Secondary sources may orient the
  review and discover primary sources, but cannot be the sole evidence that a
  method or guarantee exists.
- Verify citation metadata, DOI, URL, publication status, and claimed
  contribution against the primary source or an authoritative bibliographic
  record. Do not infer verification from a search-result snippet.
- Distinguish terminology from substantive mathematical, statistical,
  computational, or decision-theoretic differences.
- Preserve contrary, negative, gap-destroying, null, and impossibility
  evidence with the same care as supporting evidence.
- Record inaccessible or incompletely verified sources as such; never fill
  evidence fields by guesswork.

## Uncertainty and guarantee rules

- State exactly what is uncertain: flux, kinetic or nuisance parameters,
  structure/mechanism, tracer purity, measurements, biological heterogeneity,
  experimental condition, forward-model misspecification, or another stated
  source.
- Record what guarantee is actually proved or computed. Distinguish local,
  asymptotic, Bayesian/posterior, simulation-based, finite-sample, uniform,
  worst-case, minimax, and converse/impossibility results.
- Do not translate empirical performance, experimental ranking, confidence
  intervals, or posterior summaries into stronger guarantees than the source
  supports.
- Distinguish flux estimation from structural or biological mechanism
  discrimination.
- Distinguish ranking candidate experiments from certifying sufficiency,
  required sample size, error control, or impossibility.
- Report uncertainty, conflicting interpretations, and unresolved ambiguities
  explicitly in evidence and synthesis files.

## Reproducibility

- Record every literature search in `audit/search_log.md`, including date,
  database, exact query, filters, result count, retained count, searcher, and
  notes.
- Record consequential protocol and interpretation decisions in
  `audit/decision_log.md`.
- Use stable record IDs and controlled vocabularies defined in
  `protocol/evidence_schema.md`.
- Keep raw source material separate from extracted evidence and synthesis.
- Scripts must be deterministic where practical, document inputs and outputs,
  avoid silently changing curated records, and preserve logs sufficient to
  reproduce transformations.
- Do not silently overwrite manually curated evidence. Before bulk or
  automated changes, inspect the target, preserve provenance, and either merge
  changes transparently or request human direction when conflicts cannot be
  resolved safely.

## File ownership and permitted modifications

- `protocol/`: review questions, eligibility rules, search strategy, and
  schemas. Change only when the protocol itself is intentionally amended, and
  log consequential amendments.
- `corpus/`: curated paper and software evidence tables. Add or edit rows only
  from verified evidence; preserve record IDs and existing manual judgments.
- `sources/pdfs/`: user-supplied or explicitly authorised source files. Do not
  download, replace, rename, or delete papers unless the user explicitly asks.
- `synthesis/`: taxonomy, candidate-gap assessment, and rejected claims.
  Synthesis must cite evidence record IDs and must retain evidence against a
  claim.
- `audit/`: append-oriented search, decision, and red-team records. Do not
  rewrite historical entries to conceal changes.
- `analyses/`: derived analyses whose inputs, methods, and outputs must be
  documented.
- `scripts/`: reproducible utilities only; do not place manually curated
  evidence here.

Do not modify files outside the scope of the current request. Preserve
unrelated user changes. Inspect existing content before editing, and report
which files changed, checks performed, remaining uncertainty, and unresolved
human decisions. Do not commit unless the user explicitly requests it.
