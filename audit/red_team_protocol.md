# Independent Red-Team Protocol

## Purpose and independence

Before any candidate gap can be labelled `SURVIVES RED TEAM`, a later pass
must actively attempt to falsify it. The red-team pass should be conducted by
a person or agent that did not author the latest supporting synthesis where
practical. Identity, date, scope, and any independence limitation must be
logged.

Survival means only that the claim resisted the documented search and
comparison; it is not proof of novelty or absence of prior work.

## Preconditions

For each candidate:

1. state the narrow proposed gap and every material qualifier;
2. list supporting and contrary evidence record IDs;
3. identify the nearest known prior work;
4. separate substantive distinctions from terminology;
5. list unresolved metadata, access, or interpretation problems; and
6. ensure the relevant query families have reproducible search-log entries.

## Falsification procedure

### Broader terminology

Remove isotope-specific language in stages. Search synonyms for the decided
object, uncertainty, guarantee, design variable, and observation structure.
Search older terminology, author-supplied method names, spelling variants, and
descriptions that imply the method without using the candidate phrase.

### Neighbouring disciplines

Search statistics, biostatistics, information theory, optimal experimental
design, systems biology, control, active hypothesis testing, controlled
sensing, inverse problems, operations research, and reproducible scientific
software. Ask whether an adjacent method already solves the mathematical
problem and what adaptation, if any, remains isotope-specific.

### Backward citations

For every nearest prior work and supporting record, inspect references for
precursors, original proofs, earlier software, and contrary results. Log the
seed, scope, and records retained.

### Forward citations

Use one or more available citation indexes to inspect later extensions,
corrections, replications, comparisons, negative results, and implementations.
Search authors and method names separately when citation indexing is
incomplete.

### Software documentation

Inspect official repositories, manuals, release histories, issues, examples,
tests, and archived versions. Test whether the claimed missing capability
already exists under different terminology. Distinguish an implemented
feature from a proved guarantee and record the exact version and location.

### Strongest-counterexample test

Select the paper or software record most likely to destroy the gap. Compare it
field-by-field against the proposed distinction: decision object, structural
alternatives, uncertainty set, guarantee, design variables, multi-experiment
and non-IID handling, sample-size role, misspecification, and implementation.
Write the strongest fair case that the gap is already closed.

## Outcomes

- `REJECTED`: evidence establishes the proposed contribution or leaves no
  substantive distinction.
- `WEAKENED`: part of the claim is established; rewrite it narrowly and
  red-team the revision again.
- `SURVIVES RED TEAM`: no identified work closes the exact gap after the full
  procedure, with all uncertainty and closest counterevidence retained.
- `UNTESTED`: required searches, source access, or comparisons remain
  incomplete.

Record the outcome, rationale, supporting and contrary evidence, exact
search-log IDs, unresolved ambiguity, and date in both the candidate register
and decision log. Never infer survival from an exact-keyword search alone.
