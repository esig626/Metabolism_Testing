# Reproducible Search Strategy

## Scope and sequencing

Searches begin only when Phase 0 is approved. Use query families rather than a
single giant Boolean query so that terminology, disciplinary indexing, and
negative findings remain visible. Pilot each family, record the exact executed
syntax, and adapt syntax to each database without changing the underlying
concepts silently.

Every executed search must be appended to `audit/search_log.md` with UTC date,
database, exact query, filters, result count, retained count, searcher, and
notes. Export or otherwise preserve stable identifiers when permitted.
Deduplicate by DOI and other identifiers, then by verified citation; preserve
version relationships rather than discarding them invisibly.

## Databases and discovery routes

- **PubMed:** biomedical and metabolic-method coverage. Record field tags,
  filters, sort, and result count.
- **Crossref:** DOI and publication-metadata discovery and verification.
  Record query parameters and API/UI route.
- **OpenAlex:** cross-disciplinary discovery, concepts, citation links, and
  metadata. Record filters and work identifiers.
- **Google Scholar:** supplementary discovery only, especially for obscure
  phrasing and citation chaining. Record the exact query, date, accessible
  result count or the limits of count visibility, and pages screened. Do not
  use ranking or snippets as evidence.
- **Backward citation searching:** inspect references of included primary
  papers and relevant reviews; log the seed record and scope.
- **Forward citation searching:** use at least one citation index where
  available; log the seed record, service, date, and count.
- **Software:** search official repositories, package registries, project
  sites, archived releases, manuals, and documentation. Verify identity,
  version/commit, licence, maintenance evidence, and capability locations.

Metadata and contribution claims must ultimately be checked against primary
sources or authoritative records.

## Query construction

Within each family, combine selected terms from:

1. a domain block, such as `"13C metabolic flux analysis"`, `13C-MFA`,
   `"stable isotope tracing"`, `isotopomer`, `isotopologue`, `EMU`, or
   `"elementary metabolite unit"`;
2. a problem block listed below; and
3. optional guarantee, uncertainty, or implementation terms.

Run narrower and broader variants. Search spelling, hyphenation, acronym, and
conceptual synonyms. For adjacent disciplines, omit the isotope domain block
and add structural terms such as composite hypotheses, controlled sensing,
non-IID observations, experimental design, or model discrimination. Never
interpret absence of an exact phrase as absence of the method.

## Query families

### Tracer selection and optimal experimental design

Problem terms: `tracer selection`, `isotope tracer design`, `optimal tracer`,
`labeling mixture`, `labelling mixture`, `optimal experimental design`,
`Fisher information`, `D-optimal`, `A-optimal`, `E-optimal`, `expected
information gain`, `sensitivity`, `precision`, and `robust design`.

Run isotope-specific variants and broader optimal-design variants that include
nonlinear inverse problems or biochemical networks.

### EMU observability and identifiability

Problem terms: `EMU`, `elementary metabolite unit`, `observability`,
`identifiability`, `structural identifiability`, `practical identifiability`,
`flux determinability`, `estimability`, `rank deficiency`, `null space`,
`sensitivity matrix`, and `information matrix`.

Separate forward-simulation efficiency from claims about which fluxes or
structures observations can identify.

### Robust and Bayesian 13C-MFA

Problem terms: `robust`, `worst case`, `distributionally robust`, `minimax`,
`uncertain flux`, `uncertain parameters`, `Bayesian`, `posterior`,
`hierarchical`, `prior`, `credible interval`, `ensemble`, and `model
averaging`.

Search robust tracer/design work separately from robust estimation, and record
whether robustness is formal, Bayesian, sensitivity-based, or empirical.

### Model validation and structural model selection

Problem terms: `model validation`, `goodness of fit`, `lack of fit`,
`chi-square`, `likelihood ratio`, `model selection`, `network selection`,
`structural model`, `alternative pathways`, `nested models`, `non-nested
models`, `information criterion`, and `cross-validation`.

Distinguish residual checking and fit comparison from calibrated structural
decisions.

### Mechanism discrimination

Problem terms: `mechanism discrimination`, `hypothesis discrimination`,
`pathway discrimination`, `network discrimination`, `model discrimination`,
`alternative mechanisms`, `composite hypothesis`, `error probability`,
`power`, and `decision rule`.

Include biochemical-systems and kinetic-model discrimination without isotope
terms to discover transferable methods.

### Sample-size and replicate design

Problem terms: `sample size`, `power analysis`, `replicate allocation`,
`biological replicate`, `technical replicate`, `budget allocation`, `optimal
allocation`, `precision target`, and `experimental replication`.

Search isotope-tracing, metabolomics, nonlinear-model, and multi-condition
variants.

### Finite-sample and minimax testing

Problem terms: `finite sample`, `nonasymptotic`, `exact test`, `uniform test`,
`worst-case error`, `minimax testing`, `composite hypothesis testing`,
`generalized likelihood ratio`, `converse`, `lower bound`, `impossibility`,
`sample complexity`, `type I error`, and `type II error`.

Search both isotope-domain combinations and adjacent statistical literature
for nonlinear, hierarchical, and inverse models.

### Active hypothesis testing and controlled sensing

Problem terms: `active hypothesis testing`, `controlled sensing`, `sequential
design`, `adaptive experiment`, `experiment selection`, `Chernoff test`,
`multi-hypothesis`, `composite hypothesis`, `information acquisition`,
`sensor selection`, and `experiment allocation`.

Search static and adaptive settings, fixed-budget and fixed-confidence
formulations, and IID versus non-IID observations.

### Metabolic tracing software

Problem terms: `software`, `package`, `toolbox`, `framework`, `pipeline`,
`simulator`, `EMU simulator`, `flux estimation`, `isotopically nonstationary`,
`tracer design`, `graphical interface`, `command line`, `API`,
`reproducibility`, and `open source`.

Search bibliographic databases for software papers and official repositories
and documentation for implemented functionality. A GUI or implementation
feature is not itself evidence of methodological novelty.

## Screening and citation expansion

Screen titles/abstracts broadly enough to retain adjacent terminology. For
each provisionally included primary paper:

1. inspect backward references for precursors and competing approaches;
2. inspect forward citations for extensions, corrections, comparisons, and
   gap-destroying work;
3. search the method name, authors, DOI, and software name;
4. verify whether a preprint, final article, correction, or superseding method
   exists; and
5. log each reproducible search or bounded citation pass.

Stopping decisions must be documented by query family and cannot rest solely
on lack of new exact-keyword results. Surviving candidate gaps require the
independent red-team procedure in `audit/red_team_protocol.md`.
