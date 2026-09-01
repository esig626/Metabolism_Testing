# Rejected Novelty Claims Register

## Phase 2A additions

- **Rejected broad claim:** 13C-MFA does not perform structural model
  selection or model averaging. P0030 selects reaction-network candidates
  using held-out tracer data; P0031–P0032 perform Bayesian structural
  inference and model averaging; P0047 applies Bayesian model averaging to
  biological isotope data.
- **Rejected broad claim:** heterogeneous experiment blocks inherently
  require new Type-I-error theory. P0043 gives exact anytime Type-I control
  across heterogeneous adaptive batches.
- **Rejected broad claim:** biochemical perturbation design for model
  discrimination is absent. P0039 and P0048–P0051 optimise inputs,
  interventions, measurements or conditions for rival nonlinear biochemical
  networks under deterministic, probabilistic, Bayesian or max-min
  criteria.
- **Rejected broad claim:** forward-model misspecification is untreated in
  metabolic flux analysis. P0030, P0034–P0035 and P0045 treat noise-scale
  error, atom-map error, omitted reactions and covariance-aware model-error
  diagnosis.
- **Rejected broad claim:** modern open EMU software with experimental-design
  support is absent. S0009 is an active AGPL-3.0 EMU/inference/UQ/design
  platform. S0017 separately implements open-GPL robust biochemical
  model-discrimination design, although it is not an isotope platform.

This register preserves attractive claims that evidence may show to be
established, trivial, terminological, or insufficiently distinct. It began
as a set of seeded falsification hypotheses and now records their assessed
dispositions. Each assessment cites evidence record IDs and records the exact
reason and date.

## CLAIM-01: Rational tracer selection is new

- **Status:** REJECTED (pilot, 2026-07-30)
- **Evidence establishing prior work:** P0005-P0007; P0004 is
  ABSTRACT-LEVEL ONLY.
- **Evidence preserving a narrower distinction:** Decision-oriented structural
  discrimination remains different from flux-precision tracer selection.
- **Disposition and rationale:** Full-text-checked EMU and mixture-search
  procedures already establish rational tracer selection (P0005-P0007).

## CLAIM-02: Robust tracer selection over uncertain flux maps is new

- **Status:** REJECTED (pilot, 2026-07-30)
- **Evidence establishing prior work:** P0007, P0009.
- **Evidence preserving a narrower distinction:** P0009 samples feasible flux
  maps; it does not prove a uniform guarantee over the continuous class.
- **Disposition and rationale:** Robustness to nominal-flux uncertainty is
  established as perturbation analysis and sampled-map robustification.

## CLAIM-03: Parallel tracer experiments are new

- **Status:** REJECTED (Phase 2A, 2026-07-31)
- **Evidence establishing prior work:** P0037 is full-text verified; P0008
  and P0015 remain ABSTRACT-LEVEL ONLY and P0020 remains metadata-level.
- **Evidence preserving a narrower distinction:** Explicit non-IID
  mechanism-testing guarantees remain distinct from joint flux fitting.
- **Disposition and rationale:** P0037 directly defines and evaluates
  precision and synergy scores for jointly fitted parallel tracer
  experiments.

## CLAIM-04: EMU-based experimental design is new

- **Status:** REJECTED (pilot, 2026-07-30)
- **Evidence establishing prior work:** P0005-P0006.
- **Evidence preserving a narrower distinction:** EMU-based
  mechanism-discrimination design is not established by those papers.
- **Disposition and rationale:** EMU basis-vector tracer design is explicit
  primary prior work.

## CLAIM-05: Model selection using isotope data is new

- **Status:** REJECTED (Phase 2A, 2026-07-31)
- **Evidence establishing prior work:** P0030 is full-text-verified
  held-out-tracer structural selection; P0031–P0032 are full-text-verified
  Bayesian structural inference/model averaging; P0047 applies the Bayesian
  multi-model method to biological co-labelling data. P0015 remains
  ABSTRACT-LEVEL ONLY.
- **Evidence preserving a narrower distinction:** None of P0030–P0032 gives
  a uniform fixed-block two-error guarantee or sample-complexity converse
  for continuous composite EMU classes.
- **Disposition and rationale:** Structural selection and model
  probabilities are established; the narrower guarantee question is
  assessed separately and is not rescued by calling model selection new.

## CLAIM-06: A graphical EMU simulator alone is methodologically novel

- **Status:** REJECTED (pilot, 2026-07-30)
- **Evidence establishing prior work:** P0002; S0002-S0006.
- **Evidence preserving a narrower distinction:** A GUI does not establish a
  statistical or decision-method contribution.
- **Disposition and rationale:** Multiple graphical or workflow-oriented EMU
  simulators already exist.
