# Phase 2A Workstream E handoff

## Scope and disposition counts

This handoff covers only Workstream E. No `corpus/software.csv` row was
changed. The deterministic ledger contains 100 prospective occurrences:

- `FULL_TEXT_INCLUDED`: 13
- `TITLE_ABSTRACT_INCLUDED`: 19
- `TITLE_ABSTRACT_EXCLUDED`: 66
- `DUPLICATE`: 1
- `FULL_TEXT_UNAVAILABLE`: 1

All 66 exclusions have a nonblank reason. The unavailable occurrence is the
paper-named WUFlux homepage; the complete primary software paper remains
available and supports its capability extraction.
The ledger contains 93 local documentation/software-family groups. Grouping
is Workstream E-local and is not a bibliographic or global unique-work count.

## Proposed capability rows and updates

These are merge proposals, not curated corpus rows. `unclear` means the
inspected evidence did not directly verify the capability; it is not an
absence claim. IDs must be assigned by the parent merge after duplicate
checking.

| Package | Version / official evidence | Licence; maintenance | Proposed verified `yes` capabilities | Proposed `no` or `unclear` capabilities | Exact evidence locations |
|---|---|---|---|---|---|
| 13CFLUX(v3) | commit `b89f343733aaf691170c801c4764b83e07dca680`; DOI `10.1093/bioinformatics/btaf630` | AGPL-3.0; active 2026-07-31 | forward EMU simulation; inverse flux estimation; stationary; INST; tracer design; multi-experiment; UQ | measurement design, replicate allocation, model comparison, finite-sample certification, GUI, standalone CLI: `unclear` | repository `README.md` lines 7–13; `docs/source/index.rst` “Why 13CFLUX?”/“Key features”; `docs/source/api/experimental_design.rst`; `docs/source/api/simulator.rst`; primary paper Abstract, §§2.2–2.3 |
| BayFlux | commit `8d05f5c97e2c2cd1d5fa72eadbc66f13213d3eeb`; DOI `10.1371/journal.pcbi.1011111` | custom LBNL/Basque licence; active 2025-06-26 | forward EMU simulation; inverse flux estimation; steady-state support; Bayesian UQ; CLI | INST, tracer/measurement/replicate design, model comparison, finite-sample certification, GUI, multi-experiment: `unclear` | repository `README.md` lines 5–16, 52–70, 86–106; primary paper Data Availability and Methods |
| OpenMebius2 | tag 2.4.3, commit `87ba35c9be4494482a2aa475c8687517ad667db9`; preprint DOI `10.64898/2026.03.20.698926` | PolyForm Noncommercial 1.0.0; active 2026-07-31 | inverse flux estimation; steady-state; INST; tracer ranking/design; UQ; GUI | finite-sample certification: `unclear`; measurement/replicate design, model comparison, multi-experiment, forward EMU and CLI require cautious `partial`/`unclear` unless the parent checks deeper implementation paths | `README.md` lines 15–25 and 53–76; `docs/_docs/tutorials.md` “Evaluation of confidence intervals”; preprint Summary/Availability |
| Metran | official page; version unstated | research/educational end-use licence; maintenance `unclear` | forward EMU simulation; inverse flux estimation; steady-state; tracer design; UQ; GUI | INST, measurement/replicate design, multi-experiment, model comparison, finite-sample certification, CLI: `unclear` | official `metran.html`, “Metran Features”; official downloads page |
| Isodyn | v1.0, commit `c4f15c4ddce751d20c84b1916901c590594892e4`; PMCID `PMC3292525` | `none_stated`; inactive/unclear | inverse flux estimation; isotopically nonstationary kinetic-isotopomer simulation; model comparison; UQ; CLI | forward EMU: `no` (different kinetic-isotopomer representation); steady-state and design fields: `unclear`; finite-sample certification and GUI: `unclear` | repository `README.md` Description/Data Analysis/usage options; `con512tpl/stat.cpp`; de Mas et al. Methods “χ² criterion for the acceptance or rejection of model” |
| FluxPyt | official SourceForge commit `beb86d8811941aaaed0a05bcb3f6ebc6f49003ec`; DOI `10.7717/peerj.4716` | BSD-3-Clause text; active code commit 2025-11-16; version `conflicted` (`setup.cfg` 0.1.7 vs `__init__.py` 0.1.8) | forward EMU simulation; inverse flux estimation; steady-state; simulation-based UQ | INST: `no` (scope explicitly stationary); tracer/measurement/replicate design, multi-experiment, model comparison, finite-sample certification, GUI and standalone CLI: `unclear` | `README.rst`; `LICENSE.txt`; `fluxpyt/make_emu_networks.py`; `make_emu_model.py`; `main.py`; `monte_carlo.py`; `bootstrap.py`; `net_flux_cal.py` |
| FiatFlux | DOI `10.1186/1471-2105-6-209`, PMCID `PMC1199586`; current code/version not retrieved | academic source licence; non-academic licence required; maintenance `unclear` | inverse flux-ratio/net-flux estimation; steady-state; UQ; GUI | forward EMU and INST: `no` for the described implementation; tracer/measurement/replicate design, multi-experiment, model comparison, finite-sample certification and CLI: `unclear` | Methods RATIO paragraph; Methods NETTO paragraphs; Figs. 2 and 5; Availability and requirements |
| WUFlux | DOI `10.1186/s12859-016-1314-0`, PMCID `PMC5096001`; current project host inaccessible | exact statement “freely available; no non-academic restrictions,” no SPDX; maintenance inactive/unclear | forward EMU simulation; inverse flux estimation; steady-state; UQ; GUI | INST: `no` (paper scope explicitly steady-state); tracer/measurement/replicate design, multi-experiment, model comparison, finite-sample certification and CLI: `unclear` | Methods “WUFlux implementation”; experimental-data paragraph; flux-calculation paragraph; CI paragraph; Results workflow; Availability |
| sysmetab | DOI `10.1109/TCBB.2016.2544299`; repository inaccessible | paper says open source; exact licence/version/maintenance `unclear` | no `yes` proposed from repository evidence | stationary/INST simulation and inverse estimation may be `partial`; all other capabilities `unclear` | primary abstract only; retain at Level 2 until full implementation or full methods are inspected |

Existing mfapy, FreeFlux, influx_s and Iso2Flux capability evidence is
summarized in `analyses/phase2_software_landscape.md`. Their proposed
yes-level values should be copied only with the commit/path citations already
recorded there.

## Capability audit conclusions

- A GUI, goodness-of-fit test, confidence interval, or tracer ranking is not
  coded as calibrated mechanism discrimination.
- Isodyn is the only inspected platform with direct structural/model
  comparison evidence: chi-square acceptance/rejection among supplied kinetic
  schemes. This is not a composite decision-error guarantee.
- WUFlux accepts multiple tracers/isotopologues in one labeling input. This is
  not evidence of joint heterogeneous multi-experiment inference.
- FluxPyt and WUFlux implement simulation-based UQ. Neither supplies an exact
  finite-sample decision certification.
- FiatFlux is a local flux-ratio and 13C-constrained net-flux workflow, not an
  EMU/global-isotopomer solver.

## Access and metadata issues

- WUFlux: `www.13cmfa.org` did not resolve on 2026-07-31.
- FiatFlux: source is offered by the authors for academic use, but no current
  public versioned repository was verified.
- sysmetab: historical Scilab Forge repository was inaccessible.
- FluxPyt: official code is accessible, but internal version metadata
  conflicts (0.1.7 versus 0.1.8).
- Metran: official features are accessible; binary version and maintenance
  date are unstated and distribution requires licensing contact.
- Isodyn: official code is accessible, but no licence statement was found.

## Corrected search-closure assessment

**`ANCHOR_FAMILIES_VERIFIED` FOR THE BOUNDED DECISION-ORIENTED SOFTWARE
COMPARISON.**

FluxPyt, FiatFlux and WUFlux were the only outstanding named leads from the
principal software-paper pass. Each now has official-repository or complete
primary-paper verification. They add established forward/inverse MFA, GUI and
UQ capabilities, but no calibrated mechanism-discrimination design,
replicate/power optimisation, finite-sample certification or impossibility
reporting. The earlier 13CFLUX(v3), BayFlux and FreeFlux citation passes also
added no new decision-certification family.

This assessment does not establish exhaustive enumeration of historical or
current isotope utilities. Remaining access/version issues affect product and
maintenance comparison, and deferred software evidence may alter the bounded
integration comparison after verification.
