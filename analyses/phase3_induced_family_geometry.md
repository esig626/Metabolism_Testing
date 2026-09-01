# Phase 3B: geometry of experimentally induced MID families

## Object whose geometry is at issue

For metabolic class `c`, a Phase 3 family would have to be constructed as

`P_c(d) = { Law_d(Y, Q, L | v, eta) : v in V_c, eta in E_c }`,

where `d` fixes the tracer/condition/panel, `v` is a flux or metabolic state,
`eta` includes biological and technical nuisance, `Y` is the replicate-level
joint MID object, and `Q,L` preserve QC and lineage. Geometry can refer to at
least four different objects and they must not be conflated:

1. the feasible flux set `V_c`;
2. its deterministic image under an EMU/isotopomer map;
3. the image after isotope correction, normalisation and missingness; or
4. the set of full probability laws after biological and measurement noise.

A convex flux polytope does not imply a convex nonlinear MID image. A
nonconvex optimisation objective does not prove that the law family is
nonconvex. Convexification of a law family introduces mixtures of states and
need not correspond to one physical culture.

## Positive prior art

### P3-0020 — Wiechert & Wurzel (2001)

**Classification: PARTIAL FORMULATION.** The isotopomer/cumomer dynamics,
state constraints and global stability under stated no-trap conditions
provide prerequisites for a well-defined steady-state forward map. Flux is a
fixed system input; there is no statistical image or class test. Exact
locations: §5, Equation 12 and the cascade construction; §7, cumomer
transformation and feasibility/stability results. DOI
`10.1016/S0025-5564(00)00059-6`.

### P3-0008 — Antoniewicz et al. (2007), EMU

**Classification: PARTIAL FORMULATION.** EMU decomposition constructs the
network-to-measured-fragment map efficiently and establishes exact
computational equivalence for the stated decomposition. Multiple measured
MIDs share fluxes and atom maps. The paper does not characterize the global
image as a probability-family set. Exact locations: Methods §§2.1–2.6 and the
decomposition algorithms; calculation/equivalence comparisons. DOI
`10.1016/j.ymben.2006.09.001`; PMCID `PMC1994654`.

### P3-0006 / P0018 — Isermann & Wiechert (2003)

**Classification: PARTIAL FORMULATION.** Full- and partial-information rank
analyses characterize local/global structural flux identifiability and give
explicit non-identifiable mappings. These results address injectivity or rank
of a deterministic isotope forward system, not separation of two noisy
metabolic-class law images. Exact locations: “Measurement models for CLEs”;
the non-identifiable example; Theorem 4; “Partial information analysis”; and
Conclusions. DOI `10.1016/S0025-5564(02)00222-5`.

### P3-0007 — Rantanen et al. (2006)

**Classification: PARTIAL FORMULATION.** The paper defines a network and
carbon maps, isotopomer distributions and measurement-induced linear
constraints. Lemmas 1–2 identify fragment equivalence—identical isotopomer
distributions in every isotopomeric steady state, including equal composite
atom maps along branched paths—and the measurement-selection problem orders
sets by retained information. This is exact structure in the deterministic
image, not a stochastic family geometry.

Exact locations: §2, equations (1)–(4); §3, Lemmas 1–2 and Figures 1–3;
§4.1, Problem 1 and Theorem 1; §4.4, full-isotopomer extension; §6. The §6
suggestion to design measurements that falsify a network is future work, not
an implemented statistical test. DOI `10.1093/bioinformatics/btl069`.

### P3-0001 — Schellenberger et al. (2012)

**Classification: PARTIAL FORMULATION.** This paper samples a constrained
flux space, maps points into several fragment-MDV coordinates and compares
high/low target classes. It therefore displays finite empirical images of
network-induced classes and uses an SVD-based approximation to dimension.
Uniform sampling and a marginal `Z` score do not establish the image's exact
support, convexity, boundaries, order or least-favourable distributions.

Exact locations: Results “Monte Carlo Sampling Approach,” Figure 2;
“Generating and Evaluating 13C Experimental Hypotheses,” `Z_i`/`Z` equations;
“Dimensionality of Isotopomer Data,” Figure 6; Methods “Monte Carlo
Sampling” and isotopomer calculation. DOI `10.1186/1752-0509-6-9`; PMCID
`PMC3323462`.

### P3-0015 — Cedersund (2012)

**Classification: PARTIAL FORMULATION.** The acceptable parameter set and its
image under a prediction functional are searched directionally, showing how a
target image can be narrow while parameter values remain broad. It is a
generic ODE/set-valued analogue, not an isotope-law construction. Exact
locations: Definitions 1–8, Lemmas 1–2, and “Modified optimization,” Steps
1–3. DOI `10.1111/j.1742-4658.2012.08725.x`.

## What the checked papers establish—and what they do not

| Geometric property | Positive evidence | Remaining boundary |
|---|---|---|
| existence/stability of an isotope state | P3-0020 under stated network conditions | does not include culture or measurement randomness |
| efficient deterministic forward map | P3-0008 | no full probability-law image |
| structural injectivity/rank failures | P3-0006 | no class-level overlap or finite-sample separation |
| exact fragment equivalence/redundancy | P3-0007 | no covariance, support or stochastic ordering |
| sampled class clouds and approximate dimension | P3-0001 | a flux grid is not a certified cover or boundary proof |
| target image despite broad parameter set | P3-0015 in a generic ODE setting | isotope sampling family and class error absent |
| least-favourable pair for represented convex law sets | P3-0018/P0053, already reviewed in Phase 2A.1 | assumptions and computation are not proved for the actual pipeline-induced families |

No retained primary source in this bounded set characterizes all of the
following for the actual direct-MID family: support after correction and
closure, global convexity/nonconvexity, inclusion or monotone ordering,
distance between metabolic classes, boundary singularities created by zero
isotopologues/missingness, or a least-favourable state/distribution.
This is an unresolved-evidence statement, not a universal absence claim.

## Why manuscript metadata matter to geometry

The still-unreported items in `problem/source_information_gaps.md` change the
family itself:

- the exact natural-abundance correction and fragment atom maps determine the
  deterministic coordinate map;
- ion-count availability and censoring rules determine support and boundary
  masses;
- the primary sampling unit and nested variance levels determine the product
  or mixture structure;
- repeated injections can create conditionally dependent technical
  observations rather than new cultures;
- steady-state verification determines whether a steady EMU image is the
  correct state space; and
- replicate-level rather than summary MIDs are needed to identify empirical
  covariance and assess a proposed noise law.

Synthetic work can proceed only by declaring these as assumptions and
varying them in sensitivity analyses. It cannot report a sample size for the
source studies without the missing lineage and variance information.

## Family-E conclusion

GAP-08F is **PARTIALLY ADDRESSED**. Forward construction, stability,
structural identifiability, fragment equivalence and sampled images are
established components. The geometry and least-favourable structure of the
full experimentally induced joint-law families are unresolved from the
current evidence.

Accordingly, the residual must not be labelled a “computational gap.” First
one must define the actual family and prove whether an existing represented-
family theorem applies. Only after that proof would detector evaluation or
global optimisation be correctly classified as purely computational.
