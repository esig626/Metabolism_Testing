# Statistical and experimental scope

The simulation component represents metabolic hypotheses as families of
probability distributions on observable MID count blocks. Flux states and
network parameters are latent generators of those distributions; the code
does not equate discriminating observable distributions with uniquely
estimating flux.

The product-multinomial model treats fragment-specific count totals explicitly.
Fragments observed from the same culture can form a coupled observation panel,
but they are not independent biological replicates. Biological variation over
latent states and technical/counting variation are separate layers and must
not be exchanged without a stated model.

The selected modules include simple and composite likelihood tests,
finite-support minimax rules, Renyi and KL calculations and bounds,
multihypothesis/metabolic-class rules, and selected tracer, panel, depth, and
sample-size diagnostics. Their guarantees retain the scope of their inputs:

- an exhaustive calculation on an explicitly finite class concerns that class;
- a finite grid is not a uniform theorem over an unsampled continuum;
- a ranking or separation diagnostic is not a confidence certificate;
- generated R1 MIDs are synthetic evidence, not raw biological observations;
- topology and R1 fixtures demonstrate software/data structures, not
  biological validation.

The component supports the review questions concerning observable MIDs versus
latent fluxes, non-identifiable flux with distinguishable observation laws,
network-coupled fragment panels, biological versus technical variability,
finite-sample testing, replication/sample size, measurement selection, and
robust/composite testing. It makes no novelty claim and does not establish
complete reproducibility.
