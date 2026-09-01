# Simulation snapshot

This directory is a scoped export of FluxEMU source and compact evidence used
to study hypothesis tests on observable isotope mass-distribution vectors
(MIDs). The canonical development history remains
[esig626/fluxemu-prototype](https://github.com/esig626/fluxemu-prototype).
Every imported file is tied to immutable source commit
711ead67cd739d0e13c16cde34d9d7113b83043d in
[provenance/SOURCE_MANIFEST.tsv](provenance/SOURCE_MANIFEST.tsv).

FluxEMU is not an independent EMU numerical solver. It constructs in-memory
mfapy model dictionaries and delegates EMU numerical calculation to mfapy.
COBRApy supplies SBML handling, constraint-based analysis, and complete
feasible flux sampling. The separately sourced dependencies and the historical
mfapy optional-nlopt patch are described in
[provenance/DEPENDENCIES.md](provenance/DEPENDENCIES.md) and
[docs/MFAPY_PATCH.md](docs/MFAPY_PATCH.md).

The snapshot separates reusable implementation (src/fluxemu/), compact models
and experiment configurations (examples/), deterministic fixtures (fixtures/),
and tests (tests/). In particular, the R1 fixture contains generated evidence
rather than raw biological observations.

## Scientific scope

The included code supports forward MID generation, product-multinomial
observation models, simple and composite testing, minimax and Renyi/KL
calculations, metabolic-class discrimination, and selected measurement-panel
and topology diagnostics. Its claims are deliberately limited:

- calculations over a finite grid do not establish a uniform theorem;
- coupled fragment observations from one culture are not independent
  biological replicates;
- flux non-identifiability and observable-distribution discrimination are
  different questions;
- the export does not claim novelty, complete reproducibility, or scientific
  validation.

See [docs/STATISTICAL_SCOPE.md](docs/STATISTICAL_SCOPE.md) and
[docs/KNOWN_LIMITATIONS.md](docs/KNOWN_LIMITATIONS.md) before interpreting the
examples or fixtures.

## Environment

Python 3.11 and COBRApy 0.31.1 were used in the recorded source environment.
mfapy is not vendored here. Supply the separately provenance-checked mfapy
source described in provenance/DEPENDENCIES.md, either as an importable package
or by setting FLUXEMU_MFAPY_SOURCE to its checkout root.

No bulk historical results, private/uploaded references, vendor snapshots, or
machine-local environments are included.
