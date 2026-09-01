# Inclusion and Exclusion Protocol

No publication-year cutoff is imposed. Age alone is neither an inclusion nor
an exclusion criterion.

## Eligible publication types

Eligible records include peer-reviewed methodological articles, application
articles containing a substantive generalisable method, conference papers
with sufficient technical detail, books or chapters that are primary sources
for a method, theses, preprints, technical reports, standards, and official
software publications, repositories, manuals, or documentation.

Reviews, perspectives, tutorials, and benchmark papers are eligible as
secondary sources for terminology, context, and source discovery. They cannot
alone establish that a method, guarantee, or gap exists.

## Relevant disciplines

Relevant disciplines include stable-isotope tracing, metabolic flux analysis,
systems and computational biology, biostatistics, statistics, information
theory, optimal experimental design, control and estimation, active hypothesis
testing, controlled sensing, operations research, machine learning, scientific
computing, and software engineering for reproducible science.

## Inclusion criteria

Include a record when it supplies evidence material to at least one review
question and:

- defines or implements a computational, statistical, experimental-design, or
  decision method relevant to isotope tracing or a transferable adjacent
  problem;
- states enough about its objective, assumptions, criterion, computation, or
  guarantee to support evidence extraction;
- reports limitations or negative results relevant to a candidate gap;
- provides authoritative software capabilities or implementation details; or
- is a secondary source useful for discovering or contextualising primary
  work.

Adjacent work need not mention isotopes if its decision problem and
mathematical structure could materially test a proposed gap.

## Exclusion criteria

Exclude from the evidence corpus, while logging consequential exclusions, a
record that:

- is purely biological and uses isotope tracing without a relevant
  methodological, design, inferential, or software contribution;
- contains only an abstract, snippet, slide, advertisement, or unsupported
  claim with insufficient evidence for extraction;
- is a duplicate representation of the same version and adds no distinct
  information;
- concerns an unrelated method whose transfer to the review questions cannot
  be articulated;
- lacks adequate provenance or cannot be identified reliably; or
- is commentary that neither supplies primary evidence nor assists discovery
  or interpretation.

Keyword mismatch is never, by itself, an exclusion reason.

## Primary and secondary sources

A **primary methodological source** presents the original method, proof,
algorithm, experiment, benchmark, or software release being evaluated. A
**secondary source** synthesises, reviews, teaches, comments on, or cites that
work. An application paper is primary only for the methodological contribution
it actually introduces or directly evaluates.

When a secondary source identifies a relevant method, seek and cite the
primary source. If the primary source cannot be verified, retain the lead with
an explicit incomplete status rather than treating the secondary description
as proof.

## Preprints

Preprints are eligible and must be labelled `preprint`. Search for a
peer-reviewed or later version, link versions, and use the most authoritative
version for claims while preserving material differences. Do not call a
preprint peer reviewed or final. Record the version and access date where
relevant.

## Inaccessible papers

Do not infer full contributions or guarantees from metadata or abstracts.
Record an inaccessible but relevant paper with `verification_status =
metadata_only` or `abstract_only`, identify inaccessible fields as `NR` or
`unclear` as permitted, and place it in a retrieval queue. It cannot be sole
support for a substantive synthesis claim.

## Software documentation

Official repositories, release archives, manuals, API documentation, test
suites, and package registries may establish implemented capabilities,
licensing, maintenance, interfaces, and reproducibility features. They do not
alone establish methodological novelty or a statistical guarantee unless they
contain the relevant derivation and are the primary technical source. Record
the inspected version or commit and evidence location.

## Duplicate and superseded methods

Link conference, preprint, journal, correction, extension, and software
versions in notes. Prefer the latest authoritative version for citation, but
preserve earlier versions when priority, changed assumptions, retracted
claims, or distinct results matter. Do not double-count the same contribution.
Treat extensions as distinct only when the methodological difference is
explicitly recorded.

## Relevance classes

- **direct**: addresses stable-isotope tracing or 13C-MFA and materially
  answers a review question.
- **adjacent**: addresses a substantively transferable decision problem,
  guarantee, design framework, or software principle that can confirm or
  falsify a proposed isotope-method gap.
- **peripheral**: offers context, terminology, discovery leads, or a weakly
  transferable analogy but does not directly answer a review question.
- **exclude**: meets an exclusion criterion and is not entered as evidence,
  although a consequential decision may be logged.

Relevance is based on substance, not terminology or venue.
