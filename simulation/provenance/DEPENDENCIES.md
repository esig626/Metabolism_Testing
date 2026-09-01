# Dependency record

The canonical source baseline is fluxemu-prototype commit
711ead67cd739d0e13c16cde34d9d7113b83043d, dated
2026-08-12T09:32:16+09:00. The source environment recorded Python 3.11.2,
COBRApy 0.31.1, NumPy 2.4.6, pandas 2.3.3, SciPy 1.17.1, PyYAML 6.0.3,
optlang 1.9.1, swiglpk 5.0.13, joblib 1.5.3, pytest 9.1.1, and nlopt
2.11.0. These are observations about that environment, not a claim that every
combination is validated.

## mfapy

EMU numerical calculation is delegated to mfapy. The audited baseline is
https://github.com/fumiomatsuda/mfapy at commit
a10433af16682386548b360297e2476152d46ede (setup version 0.6.3). mfapy is not
vendored and its packaging does not provide a reliable registry dependency for
this export. Provide that checkout separately, either importably or through
FLUXEMU_MFAPY_SOURCE. The source's optional-nlopt patch is recorded, but not
applied, under provenance/patches/.

The required mfapy API surface is MetabolicModel construction from reaction,
reversible-reaction, metabolite, and target-fragment dictionaries; CarbonSource
construction and isotopomer setters; reconstruct; generated calmdv and
diffmdv functions; and isotope-correction helpers reached by those operations.
No mfapy text model is required at runtime. Fitting and confidence-interval
APIs are out of scope.

## COBRApy

COBRApy 0.31.1 is an ordinary external dependency. Used APIs include Model,
Reaction, and Metabolite; SBML read/write; FBA optimization; flux variability;
ACHR and single-process OptGP sampling; stoichiometric-matrix construction;
objective constraints; and solver status/constants. The development snapshot
formerly under vendor/cobrapy is neither copied nor required at runtime.

The selected SBML fixtures are simulation/examples/toy_model.xml and
simulation/examples/antoniewicz_tca/antoniewicz_tca.xml. The R1 fixture freezes
generated MIDs and metadata only; it does not include the larger originating
COBRA model or regenerate the R1 experiment.

## Installation limitation

pyproject.toml records registry-resolvable dependencies but intentionally does
not pretend that mfapy 0.6.3 is available as a normally pinned package. This
manual, commit-pinned source dependency is a remaining reproducibility
limitation.
