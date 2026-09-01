# Review Questions

## Primary review question

What computational and statistical decision problems, methods, guarantees,
limitations, and reproducible software are established for designing and
analysing stable-isotope metabolic-tracing experiments—especially
EMU-based 13C-MFA—and, after active attempts to falsify proposed novelty,
which precise methodological questions remain unresolved enough to support a
defensible FY2027 JSPS Early-Career Scientists proposal?

## Secondary questions

### Decision problems

1. What object is estimated, selected, tested, discriminated, certified, or
   ruled out?
2. Which methods address flux estimation, parameter estimation, experiment
   ranking, identifiability, model validation, structural selection, mechanism
   discrimination, or impossibility?
3. What loss, utility, error event, or scientific decision connects the
   computation to an experimental objective?

### Uncertainty formulations

4. Which uncertainties are represented: flux, parameter, structural,
   measurement, biological heterogeneity, experimental condition,
   tracer/measurement implementation, or forward-model misspecification?
5. Are uncertainties probabilistic, set-valued, Bayesian, empirical,
   sensitivity-based, adversarial, or left implicit?
6. Are nuisance parameters and dependence between uncertainty sources handled?

### Statistical guarantees

7. Is the result local, asymptotic, Bayesian/posterior, simulation-based,
   finite-sample, uniform/worst-case, minimax, or a converse/impossibility
   result?
8. Which assumptions, error probabilities, parameter domains, and operating
   conditions delimit the guarantee?
9. Does a method merely rank designs, or certify sufficiency, sample size,
   controlled error, or impossibility?

### Design variables

10. Which variables are optimised jointly or separately: tracer identity,
    mixture/enrichment, measurement panel, time points, perturbations,
    conditions, experiment sequence, sample size, or replicate allocation?
11. Is design static, sequential/adaptive, robust, Bayesian, or
    decision-oriented?
12. What practical constraints and costs are represented?

### Model and mechanism discrimination

13. Are alternatives numerical flux states, parameter regions, network
    structures, pathway mechanisms, or biological hypotheses?
14. How are nested, non-nested, composite, or partially overlapping
    alternatives treated?
15. Does the method distinguish better fit from calibrated discrimination
    with controlled errors?

### Sample-size and replicate design

16. Are sample size and replicate allocation explicit design outputs?
17. Are power, type-I/type-II errors, precision, posterior risk, or other
    criteria used, and under what finite-sample or asymptotic assumptions?
18. Are biological and technical replicates distinguished?

### Non-IID and multi-experiment inference

19. Can methods combine multiple tracers, conditions, perturbations, time
    points, batches, or measurement platforms?
20. Are observations allowed to be independent but non-identically
    distributed, dependent, hierarchical, or heterogeneous?
21. How are information and error control combined across experiments?

### Model misspecification

22. Which departures from the assumed forward model are considered, including
    omitted reactions, incorrect atom maps, non-steady state, pool mixing,
    measurement bias, and distributional misspecification?
23. Are robustness claims sensitivity analyses, empirical stress tests,
    bounded guarantees, or formal minimax results?
24. Can design expose model inadequacy rather than merely optimise under the
    assumed model?

### Software capabilities

25. Which packages implement forward EMU simulation, inverse estimation,
    design, comparison, uncertainty quantification, or certification?
26. Are implementations open, licensed, maintained, scriptable, tested,
    documented, versioned, and capable of reproducing published examples?
27. Which methodological claims exist only in papers, and which software
    capabilities lack primary methodological support?

### Possible gaps

28. Which scientific or software gaps survive comparison with primary
    literature, adjacent disciplines, backward/forward citations, and
    software documentation?
29. Is each surviving gap substantive rather than terminological, and what is
    its nearest prior work and exact distinction?
30. Is the gap feasible and decision-relevant without being predetermined by
    the applicant's available datasets?
