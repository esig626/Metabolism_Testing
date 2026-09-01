# Phase 2A Workstream E — software and product landscape

## Scope and evidence rule

This prospective assessment used PHASE2-SEARCH-0041–0055,
PHASE2-SEARCH-0069–0074 and the named-lead closure
PHASE2-SEARCH-0090–0093, plus the adjacent model-discrimination software
paper retrieved under PHASE2-SEARCH-0115, together with the official
repositories, project documentation, and primary software papers they
identified. A capability is treated as verified only when a versioned
repository path or official methodological passage implements or documents
it. Repository activity is reported as observed on 2026-07-31 and is not a
quality judgment. No package was executed.

The strongest new evidence is 13CFLUX(v3) and OpenMebius2. The former is a
new open implementation family member rather than merely the restricted
13CFLUX2 distribution; the latter is a maintained, source-available GUI
successor to OpenMebius under a non-commercial licence. Together with the
other inspected platforms, they weaken a broad claim that modern and
reproducible 13C-MFA software is absent. Neither documents calibrated mechanism
discrimination, replicate/power design, finite-sample decision guarantees, or
impossibility reporting.

## Versioned platform evidence

| Platform | Version or inspected revision | Directly verified capability locations | Licence; maintenance evidence | Decision-oriented limits |
|---|---|---|---|---|
| 13CFLUX(v3) | commit `b89f343733aaf691170c801c4764b83e07dca680` (2026-07-29); Bioinformatics 2025, DOI `10.1093/bioinformatics/btaf630` | `README.md` lines 7–13: stationary/nonstationary simulation, fitting, frequentist/Bayesian statistics; `docs/source/index.rst` “Why 13CFLUX?” and “Key features”: EMU/cumomer simulation, experimental-design facade, multi-start fitting, UQ, pip/Docker; `docs/source/api/experimental_design.rst`: `TracerMixtureSpace`; `docs/source/api/simulator.rst`: stationary and nonstationary EMU systems | AGPL-3.0, `LICENSE` and docs “License & contributing”; official JuGit activity 2026-07-30 | Tracer-mixture search and UQ are implemented, but no inspected path documents structural model comparison, mechanism-error calibration, replicate/power optimisation, finite-sample certification, or impossibility reporting. Python API, not a documented standalone CLI or GUI. |
| 13CFLUX2 | official page and software paper, DOI `10.1093/bioinformatics/bts646`; existing S0001 evidence | Software paper abstract and official feature sheet: Cumomer/EMU workflows, design/evaluation, statistical analysis, GUI/CLI and FluxML workflows | academic non-commercial licence; official site current, but successor v3 exists | Restricted licence. “Experimental design” does not by itself establish mechanism discrimination or certification. |
| INCA | official MFA Suite page updated 2026-06-23; software paper DOI `10.1093/bioinformatics/btu015` | Official INCA page: stationary/transient EMU simulation, inverse flux/pool fitting, goodness-of-fit, parameter CIs, identifiability, computational search for isotope-experiment design | free academic/non-commercial licence; official suite update 2026-06-23 | Direct evidence supports flux inference/design, not model selection, power/replicate design, finite-sample decision guarantees, or impossibility. MATLAB application; GUI is advertised by platform context but not independently executed. |
| mfapy | commit `a10433af16682386548b360297e2476152d46ede` (2025-07-07) | `README.md` “mfapy supports”: EMU, INST-MFA, unlimited parallel labeling experiments, fitting, goodness-of-fit and automated model construction; examples and unit-test command; Phase 1 S0004 documentation locations verify CIs and simulation-assisted tracer comparison | MIT, `LICENSE`; repository update 2025-07-07 | Parallel fitting and goodness-of-fit are not calibrated structural discrimination. No verified replicate/power, finite-sample certification or impossibility reporting; no standalone CLI/GUI documented. |
| FreeFlux | commit `ec05c47bbc2e4ac58bb85d39408ff4ef4016a15c` (2026-05-08) | `README.rst` lines 5–11 and 63–98: stationary/transient flux estimation and labeling simulation; `docs/source/building_model.ipynb` EMU decomposition; tutorials for steady and INST simulation/estimation; `solve_with_confidence_intervals` documented in README | GPL-3.0, `LICENSE`; repository update 2026-05-08 | Strong open simulation/inference/UQ implementation. No verified tracer optimiser, structural comparison, replicate/power design, decision guarantee, or impossibility output. Scriptable Python API, no standalone CLI/GUI verified. |
| influx_s | commit `6ca6df5777ead8ccad2c8a1a087f7b1d78f59feb` (2026-03-04) | Official repository and manual files document flux/metabolite estimation from labelled data, simulation and command-line workflows; repository description and versioned examples | no machine-readable licence established in the GitHub API snapshot; active commit 2026-03-04 | Capability evidence supports estimation workflows, not decision-oriented structural discrimination or certification. Licence therefore remains unclear pending direct licence text verification. |
| Iso2Flux | commit `5c3f9a35e658b54d56eb00439de3036b5014d99b` (2020-03-29) | `README.md` sections “Label propagation rules” and “Experimental data file”: atom propagation, labelled-substrate mixtures, measured isotopologues and replicates; implementation integrates constraint-based models and isotope simulation/inference | GPL-3.0, `LICENSE`; no repository update after 2020 in inspected revision | Useful genome-scale integration, but no verified decision-oriented tracer optimiser, model comparison, sample-size design, guarantees or impossibility report. Maintenance is inactive/unclear rather than active. |
| BayFlux | commit `8d05f5c97e2c2cd1d5fa72eadbc66f13213d3eeb` (2025-06-26); DOI `10.1371/journal.pcbi.1011111` | `README.md` lines 5–16: Bayesian genome-scale 13C-MFA; lines 52–70: MCMC examples and EMU simulator; lines 86–106: MPI command-line mode; Docker, notebooks, tests and coverage instructions | custom LBNL/Basque licence in `license.txt`; repository updated 2025-06-26 | Verifies Bayesian flux inference/UQ, EMU forward simulation, CLI and reproducible Docker/notebook assets. Does not verify tracer/measurement design, structural comparison, replicate design, frequentist error certification or impossibility. |
| OpenMebius2 | release/tag `2.4.3`, commit `87ba35c9be4494482a2aa475c8687517ad667db9` (2026-07-10); bioRxiv DOI `10.64898/2026.03.20.698926` | `README.md` lines 15–25: GUI successor and INST-MFA; lines 53–76: reproducible tutorial and tracer suggestion; `docs/_docs/tutorials.md` heading “Evaluation of confidence intervals”; release installers for Windows/macOS/Linux | PolyForm Noncommercial 1.0.0 (`LICENSE.md`); active release 2.4.3 on 2026-07-10. Source-available, not an OSI open-source licence. | Tracer “suggestion” is flux-precision oriented and does not establish mechanism discrimination. No verified sample-size/power, finite-sample certification or impossibility. |
| OpenMebius | primary paper DOI `10.1155/2014/627014`; existing S0006 | Primary software paper and official successor history establish open INST-MFA command-line implementation | GPL-3.0 in Phase 1 record; superseded by OpenMebius2 | Superseded platform; no evidence for calibrated decision features. |
| OpenFLUX | primary software paper DOI `10.1186/1475-2859-8-25`; official SourceForge project; existing S0003 | Paper/repository establish steady-state 13C-MFA modelling | GPL-3.0-or-later in Phase 1 record; inactive | No direct evidence for the full decision stack; historical implementation rather than current integration target. |
| Metran | official Antoniewicz laboratory feature/download pages inspected 2026-07-31; version not stated | `metran.html`, “Metran Features”: MFA, EMU, GUI, goodness-of-fit, flux CIs, tracer simulation, optimal experimental design and flux observability | research/educational end-use licence obtained through MIT licensing; current binary/version and maintenance date not published | Directly verifies flux-oriented design and UQ, but not structural comparison, mechanism discrimination, replicate/power design, finite-sample certification or impossibility reporting. |
| sysmetab | Mottelet, Gaullier and Sadaka, DOI `10.1109/TCBB.2016.2544299`; PubMed PMID 28113867 | Primary abstract: stationary/nonstationary isotope-label balance equations, adjoint residual-gradient computation and flux-identification speedup; algorithms stated to be implemented in sysmetab | paper calls package open source, but the historical Scilab Forge URL was not retrievable; exact licence/version/maintenance remain unverified | Supporting evidence for computational acceleration only. No inspected implementation supports design, structural comparison or decision guarantees. |
| Isodyn | version 1.0, commit `c4f15c4ddce751d20c84b1916901c590594892e4` (2019-04-29); de Mas et al., BMC Systems Biology 2011, PMCID `PMC3292525` | Repository `README.md` “Description”, “Data Analysis” and usage options: dynamic isotopomer simulation, fitting, goodness-of-fit, flux CIs and shell interface; de Mas et al. Methods “χ² criterion for the acceptance or rejection of model”: comparison/rejection of kinetic network schemes | no licence file or statement found; repository metadata shows last push 2020-04-15, so maintenance is inactive/unclear | Direct counterevidence to an absolute claim that isotope software never compares structures. Its χ² rejection among supplied kinetic schemes is not calibrated composite mechanism-discrimination design, sample-size design, a finite-sample uniform guarantee, or an impossibility certificate. |
| FluxPyt | official SourceForge code commit `beb86d8811941aaaed0a05bcb3f6ebc6f49003ec` (2025-11-16); version conflicted (`setup.cfg` 0.1.7, `fluxpyt/__init__.py` 0.1.8); DOI `10.7717/peerj.4716` | `README.rst` scope/installation: stationary 13C-MFA; `fluxpyt/make_emu_networks.py` and `make_emu_model.py`: EMU construction; `fluxpyt/main.py`: inverse fitting plus Monte Carlo prompt; `fluxpyt/monte_carlo.py`, `bootstrap.py` and `net_flux_cal.py`: simulated flux uncertainty and CI output | New BSD / BSD-3-Clause text in `LICENSE.txt`; repository commit in 2025 indicates recent code activity, but the internal version conflict requires manual resolution before a corpus version is asserted | Verifies open steady-state EMU forward/inverse analysis and simulation-based UQ. No inspected tracer/measurement/replicate design, structural comparison, calibrated mechanism discrimination, finite-sample certification, impossibility reporting, GUI or standalone CLI. |
| FiatFlux | Zamboni, Fischer and Sauer 2005, DOI `10.1186/1471-2105-6-209`, PMCID `PMC1199586`; no current versioned code retrieved | Methods: RATIO performs local flux-ratio estimation with propagated covariance/SD; NETTO performs 13C-constrained net-flux balancing and Jacobian-based CIs; Methods and Figs. 2/5 document GUIs; Availability states MATLAB R14/Optimization Toolbox | source code available from authors for academic purposes; non-academic use requires a licence; current version and maintenance status unverified | Not an EMU simulator and not global isotopomer inverse MFA. It provides flux-ratio/net-flux estimation and UQ, not tracer design, multi-experiment inference, structural/model selection, decision-error certification or impossibility reporting. |
| WUFlux | He et al. 2016, DOI `10.1186/s12859-016-1314-0`, PMCID `PMC5096001`; paper-named project host inaccessible 2026-07-31 | Methods “WUFlux implementation”: GUI; Methods experimental-data paragraph: multiple tracer/isotopologue inputs; Methods flux-calculation paragraph: EMU forward model and weighted nonlinear inverse fitting; Methods CI paragraph: Monte Carlo/bootstrap CIs and χ² goodness-of-fit; Results workflow: estimation, CIs and visualization | paper states the software is freely available without non-academic restrictions, but supplies no standard licence identifier; current project URL did not resolve, so maintenance is inactive/unclear | Multi-tracer inputs are not multi-experiment joint inference or tracer optimisation. χ² goodness-of-fit is model-adequacy checking, not structural comparison. No replicate design, mechanism-error guarantee, certification or impossibility output. |
| ModelDiscriminationToolkitGUI | Stegmaier, Skanda and Lebiedz 2013, DOI `10.1371/journal.pone.0055723`, PMCID `PMC3563641`; S0017 | Abstract and Introduction identify the GPL SourceForge distribution; Methods “Model discrimination,” “Robust optimal designs,” “Numerical tools” and “The graphical user interface” document ODE simulation, parameter re-estimation, measurement-time/perturbation design and the interactive GUI | GPL, exact version unspecified; current maintenance not established | Directly verifies robust max-min model-discrimination and measurement-time design software in adjacent biochemical ODE systems. It has no EMU/isotope capability and no replicate/power design, finite-sample certification or impossibility report. |
| SteadyState-MFA / Nonstationary-MFA | GitHub discovery under `maranasgroup`; repositories returned by PHASE2-SEARCH-0055 | Official repository descriptions identify genome-scale steady-state and nonstationary 13C-MFA code | no licence shown in discovery export; last visible pushes 2021 and 2019 | Supporting leads only until versioned capability and licence paths are inspected; cannot support strong integration claims. |
| ScalaFlux, MIA, iMS2Flux | primary-paper leads from PHASE2-SEARCH-0043 and 0053–0054 | Their records establish separate subnetwork flux, isotopolome-analysis, or measurement-processing families at Level 2 only | version/licence/maintenance not uniformly verified in this bounded stream | They demonstrate ecosystem breadth but cannot support “yes” capability coding without repository/document inspection. Measurement-processing tools are not inverse 13C-MFA or decision-certification platforms merely because they process isotope data. |

Targeted Crossref searches did not rediscover sysmetab or Isodyn by name.
The official closure did recover sysmetab by DOI and Isodyn by its exact
repository; the earlier name-query failure is retained as a search limitation,
not treated as absence.

The subsequent named-lead closure directly verified FluxPyt, FiatFlux and
WUFlux. Their existence further weakens software-absence claims but does not
add the missing decision-certification stack.

## Capability comparison of selected load-bearing implementations

Values are `YES`, `PARTIAL`, `NO EVIDENCE` (not a claim of nonexistence), or
`NA`. “YES” points to the versioned locations above.

Isodyn (S0013) adds a verified historical structural-comparison component:
it fits alternative kinetic schemes and applies a chi-square goodness-of-fit
acceptance/rejection rule. It is omitted from the selected open-platform
comparison below because no software licence is stated and maintenance is
inactive/unclear, not because it was excluded from the corpus.

| Capability | 13CFLUX(v3) | mfapy | FreeFlux | BayFlux | OpenMebius2 |
|---|---|---|---|---|---|
| Forward EMU simulation | YES | YES | YES | YES | PARTIAL (forward implementation documented, representation not reverified here) |
| Stationary inverse flux estimation | YES | YES | YES | YES | YES |
| INST-MFA | YES | PARTIAL | YES | NO EVIDENCE | YES |
| Bayesian inference | YES | PARTIAL (example implementation) | NO EVIDENCE | YES | NO EVIDENCE |
| Frequentist confidence/UQ | YES | YES | YES | NA | YES |
| Tracer design/ranking | YES (mixture space/API) | PARTIAL (simulation-assisted) | NO EVIDENCE | NO EVIDENCE | YES (suggestion/ranking) |
| Measurement design | NO EVIDENCE | NO EVIDENCE | NO EVIDENCE | NO EVIDENCE | NO EVIDENCE |
| Parallel/multi-experiment inference | paper/docs claim; exact API path not fully verified | YES | NO EVIDENCE | NO EVIDENCE | NO EVIDENCE |
| Structural model comparison | NO EVIDENCE | PARTIAL (goodness-of-fit only) | NO EVIDENCE | NO EVIDENCE | NO EVIDENCE |
| Mechanism discrimination | NO EVIDENCE | NO EVIDENCE | NO EVIDENCE | NO EVIDENCE | NO EVIDENCE |
| Replicate/sample-size or power design | NO EVIDENCE | NO EVIDENCE | NO EVIDENCE | NO EVIDENCE | NO EVIDENCE |
| Finite-sample decision guarantee | NO EVIDENCE | NO EVIDENCE | NO EVIDENCE | NO EVIDENCE | NO EVIDENCE |
| Impossibility/insufficiency reporting | NO EVIDENCE | NO EVIDENCE | NO EVIDENCE | NO EVIDENCE | NO EVIDENCE |
| GUI | NO EVIDENCE | NO EVIDENCE | NO EVIDENCE | NO EVIDENCE | YES |
| CLI | NO EVIDENCE (Python API) | NO EVIDENCE | NO EVIDENCE | YES | PARTIAL (legacy CLI; current GUI) |
| Reproducibility assets | pip, Docker, CI, docs | tests, examples | pip, docs, tutorials | Docker, notebooks, tests | tagged installers, tutorials |

## Gap-type separation

- **Scientific-method gap:** software inspection cannot establish one.
  Packages implement flux estimation, UQ, goodness-of-fit and experiment
  ranking; their lack of documented calibrated mechanism decisions simply
  inherits the separate statistical-method question.
- **Computational/integration gap:** a common open workflow combining
  simulation, inference, tracer design and provenance is increasingly
  weakened by 13CFLUX(v3). Adding a model-comparison objective to an existing
  API could be a nontrivial computational adaptation, but the software
  evidence alone does not show that new mathematics is necessary.
- **Software-engineering gap:** no inspected platform integrates verified
  structural alternatives with tracer optimisation, sample-size/power design, finite-sample
  certification and insufficiency reporting. This is an integration statement
  over the inspected set, not a novelty claim and not automatically a
  scientific contribution.
- **Usability gap:** OpenMebius2 supplies a maintained source-available GUI and tracer
  suggestions; 13CFLUX(v3), FreeFlux, mfapy and BayFlux provide scriptable
  workflows. A claim that both GUI and reproducible scripting are absent is
  false.
- **Reproducibility gap:** containers, package managers, tests, notebooks,
  tagged releases and machine-readable models already exist, although not
  uniformly.
- **Product opportunity:** restricted licences for 13CFLUX2/INCA and uneven
  documentation may motivate support or distribution, but do not establish a
  scientific or methodological gap.

## Workstream conclusion

The broad “decision-oriented open software is absent” hypothesis is further
weakened. Seventeen platforms are retained in the software corpus.
ModelDiscriminationToolkitGUI establishes that open robust biochemical
model-discrimination design software exists, although outside isotope MFA.
13CFLUX(v3)
is open, active, containerised, EMU-capable, supports
stationary/nonstationary workflows, fitting, UQ and an experimental-design
API. OpenMebius2 supplies an active source-available GUI with tracer suggestion and
confidence-interval workflows. The remaining missing integration is narrower:
no inspected platform documents calibrated structural/mechanism
discrimination together with replicate/power design, finite-sample
certification, and impossibility reporting. OpenMebius2 does not satisfy an
open-licence requirement because its PolyForm licence restricts use to
non-commercial purposes. Whether the missing decision components require
new science depends entirely on the separate theory workstreams; packaging
established criteria is engineering.

## Search-closure assessment

Workstream E is `ANCHOR_FAMILIES_VERIFIED` for the bounded
decision-oriented software comparison. The official closure resolved
Metran, sysmetab and Isodyn; the subsequent named-lead closure verified
FluxPyt, FiatFlux and WUFlux from an official repository or complete primary
software paper. Within the inspected S0001–S0017 evidence, those additions
did not document calibrated mechanism discrimination, replicate or power
design, finite-sample decision certification, or impossibility reporting.
The 13CFLUX(v3), BayFlux and FreeFlux citation passes likewise supplied
verified component evidence.

This bounded verification does not establish exhaustive enumeration of
historical or current isotope software, and a deferred platform may change
the integration comparison after verification.
Maintenance remains unresolved for WUFlux and FiatFlux because their current
code distributions were unavailable, ModelDiscriminationToolkitGUI's current
version and maintenance are unresolved, and FluxPyt has conflicting internal
version metadata. Those access/version issues affect product comparison, but
not the bounded conclusion about the missing decision stack.
