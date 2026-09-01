"""Observable-law-only numerical minimax classification for ``K`` classes.

The module starts after observable MID law classes have been constructed.  It
does not accept a topology, flux, nuisance coordinate, or hidden class label
at decision time.  A shared proposal is used only for numerical integration;
every represented member remains a separate worst-case constraint in the
finite linear programme.

For finite class-member laws ``P[k][j, s]`` on a common support, the primal is

``minimise t``

subject to ``sum_s P[k][j,s] * (1 - phi[k,s]) <= t`` for every ``k,j``,
``sum_k phi[k,s] = 1`` for every ``s``, and ``phi[k,s] >= 0``.  The scalar
``t`` is deliberately free.  Its dual has nonnegative member weights
``lambda[k,j]`` with one *global* normalization ``sum_kj lambda[k,j] = 1``:

``maximise 1 - sum_s max_k sum_j lambda[k,j] P[k][j,s]``.

Thus the dual weights are numerical least-favourable minimax objects.  They
are not priors over biological topologies.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence

import numpy as np
from scipy import sparse
from scipy.optimize import linprog
from scipy.special import logsumexp

from .composite_mid_minimax import (
    DEFAULT_LP_CONSTRAINT_SCALE,
    DEFAULT_LP_TOLERANCE,
    DEFAULT_LP_WEIGHT_PRUNING_CUTOFF,
    DEFAULT_MAXIMUM_PRUNED_ROW_MASS,
    DEFAULT_ROW_SUM_TOLERANCE,
    HIGHS_SMALL_MATRIX_VALUE,
    ImportanceDiscretization,
    ContinuousRepresentationUnavailable,
    MinimaxNumericalError,
    ProductDirichletFamily,
    concatenate_families,
    dirichlet_rms_kappa,
    family_from_mid_class,
)
from .multiclass_rule_column_generation import (
    RuleColumnGenerationSolution,
    solve_rule_column_generation,
)


def _readonly_float(values: np.ndarray | Sequence[float]) -> np.ndarray:
    result = np.array(values, dtype=float, copy=True)
    result.setflags(write=False)
    return result


def _readonly_int(values: np.ndarray | Sequence[int]) -> np.ndarray:
    result = np.array(values, dtype=int, copy=True)
    result.setflags(write=False)
    return result


def _labels(count: int, labels: Sequence[str] | None) -> tuple[str, ...]:
    if labels is None:
        result = tuple(f"class_{index}" for index in range(count))
    else:
        result = tuple(str(value) for value in labels)
    if len(result) != count or len(set(result)) != count or any(not x for x in result):
        raise ValueError("class labels must be nonempty, unique, and align with classes")
    return result


def _law_key(family: ProductDirichletFamily, index: int) -> tuple[object, ...]:
    row = np.ascontiguousarray(family.alpha_parameters[int(index)])
    return (family.block_names, family.block_sizes, row.dtype.str, row.tobytes())


def _randomized_systematic_component_indices(
    weights: np.ndarray,
    support_size: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """Allocate a categorical mixture with stratified full-support counts.

    A uniformly shifted systematic lattice gives every component its correct
    expected count and keeps its realized full-support count within one of
    that expectation.  Randomly permuting the resulting multiset is essential:
    conditional on the full counts, every prefix is a simple random subset,
    hence its marginal component law remains the declared categorical mixture.
    """

    probabilities = np.asarray(weights, dtype=float)
    size = int(support_size)
    if (
        probabilities.ndim != 1
        or len(probabilities) < 1
        or not np.all(np.isfinite(probabilities))
        or np.any(probabilities <= 0.0)
        or not math.isclose(
            float(np.sum(probabilities)), 1.0, rel_tol=0.0, abs_tol=2.0e-14
        )
        or size < 1
    ):
        raise ValueError("systematic categorical inputs are invalid")
    cumulative = np.cumsum(probabilities)
    cumulative[-1] = 1.0
    offset = float(rng.random())
    positions = (np.arange(size, dtype=float) + offset) / size
    systematic = np.searchsorted(cumulative, positions, side="right")
    return np.asarray(systematic[rng.permutation(size)], dtype=int)


@dataclass(frozen=True)
class MulticlassProposalSupport:
    """Shared observations from a set-invariant, class-balanced proposal.

    ``member_component_indices`` maps every original member, including exact
    duplicates, to its globally deduplicated proposal component.  Proposal
    construction is setwise, while this mapping preserves auditability.
    ``component_class_masses[k,c]`` records the mass contributed by class
    ``k`` to global component ``c``; each row sums to ``1 / K``.
    """

    class_labels: tuple[str, ...]
    observations: np.ndarray
    log_proposal_density: np.ndarray
    sampled_component_indices: np.ndarray
    proposal_component_weights: np.ndarray
    component_class_masses: np.ndarray
    member_component_indices: tuple[np.ndarray, ...]
    unique_component_counts_by_class: tuple[int, ...]
    seed: int

    def __post_init__(self) -> None:
        labels = tuple(str(value) for value in self.class_labels)
        observations = _readonly_float(self.observations)
        log_density = _readonly_float(self.log_proposal_density)
        sampled = _readonly_int(self.sampled_component_indices)
        weights = _readonly_float(self.proposal_component_weights)
        masses = _readonly_float(self.component_class_masses)
        mappings = tuple(_readonly_int(values) for values in self.member_component_indices)
        class_count = len(labels)
        component_count = len(weights)
        support_size = len(observations)
        if class_count < 2 or len(set(labels)) != class_count:
            raise ValueError("a multiclass proposal needs at least two unique labels")
        if observations.ndim != 2 or support_size < 1:
            raise ValueError("proposal observations must be a nonempty matrix")
        if log_density.shape != (support_size,) or sampled.shape != (support_size,):
            raise ValueError("proposal support arrays do not align")
        if component_count < 1 or masses.shape != (class_count, component_count):
            raise ValueError("proposal component arrays do not align")
        if len(mappings) != class_count or len(self.unique_component_counts_by_class) != class_count:
            raise ValueError("proposal class metadata do not align")
        if (
            not np.all(np.isfinite(observations))
            or np.any(observations <= 0.0)
            or not np.all(np.isfinite(log_density))
            or not np.all(np.isfinite(weights))
            or np.any(weights <= 0.0)
            or np.any(sampled < 0)
            or np.any(sampled >= component_count)
            or not np.all(np.isfinite(masses))
            or np.any(masses < 0.0)
        ):
            raise ValueError("invalid multiclass proposal support")
        if not math.isclose(float(np.sum(weights)), 1.0, rel_tol=0.0, abs_tol=2e-14):
            raise ValueError("proposal component weights must sum to one")
        expected_class_mass = 1.0 / class_count
        if not np.allclose(
            np.sum(masses, axis=1), expected_class_mass, rtol=0.0, atol=2e-14
        ):
            raise ValueError("each class must retain equal positive proposal mass")
        if not np.allclose(np.sum(masses, axis=0), weights, rtol=0.0, atol=2e-14):
            raise ValueError("class contributions do not reproduce proposal weights")
        for mapping in mappings:
            if mapping.ndim != 1 or len(mapping) < 1 or np.any(mapping < 0) or np.any(mapping >= component_count):
                raise ValueError("invalid original-member proposal mapping")
        object.__setattr__(self, "class_labels", labels)
        object.__setattr__(self, "observations", observations)
        object.__setattr__(self, "log_proposal_density", log_density)
        object.__setattr__(self, "sampled_component_indices", sampled)
        object.__setattr__(self, "proposal_component_weights", weights)
        object.__setattr__(self, "component_class_masses", masses)
        object.__setattr__(self, "member_component_indices", mappings)
        object.__setattr__(self, "unique_component_counts_by_class", tuple(int(x) for x in self.unique_component_counts_by_class))
        object.__setattr__(self, "seed", int(self.seed))

    @property
    def support_size(self) -> int:
        return len(self.observations)

    @property
    def observation_dimension(self) -> int:
        return self.observations.shape[1]

    @property
    def proposal_component_count(self) -> int:
        return len(self.proposal_component_weights)

    def subset(self, support_size: int) -> "MulticlassProposalSupport":
        size = int(support_size)
        if size < 1 or size > self.support_size:
            raise ValueError("proposal subset size is out of range")
        return MulticlassProposalSupport(
            class_labels=self.class_labels,
            observations=self.observations[:size],
            log_proposal_density=self.log_proposal_density[:size],
            sampled_component_indices=self.sampled_component_indices[:size],
            proposal_component_weights=self.proposal_component_weights,
            component_class_masses=self.component_class_masses,
            member_component_indices=self.member_component_indices,
            unique_component_counts_by_class=self.unique_component_counts_by_class,
            seed=self.seed,
        )


def build_balanced_proposal_support(
    families: Sequence[ProductDirichletFamily],
    *,
    support_size: int,
    seed: int,
    class_labels: Sequence[str] | None = None,
    density_chunk_size: int = 1024,
) -> MulticlassProposalSupport:
    """Draw shared support from equal class masses and distinct member laws.

    Within each class, its ``1/K`` numerical mass is uniform over the set of
    distinct observable laws.  Equal laws are then merged globally.  Exact
    member duplication therefore changes neither proposal weights nor a draw
    made with the same seed, while every class retains positive base mass.

    Component indices use a uniformly shifted systematic allocation followed
    by an independent random permutation.  Full-support component counts are
    within one of their expectations, and every nested prefix has the declared
    categorical proposal as its marginal law.  Rows are therefore exchangeable
    rather than independent; importance weights continue to use the unchanged
    exact mixture density.
    """

    items = tuple(families)
    if len(items) < 2:
        raise ValueError("at least two observable-law classes are required")
    labels = _labels(len(items), class_labels)
    size = int(support_size)
    chunk = int(density_chunk_size)
    if size < 1 or chunk < 1:
        raise ValueError("support size and density chunk size must be positive")
    reference = items[0]
    for family in items[1:]:
        if (
            family.block_names != reference.block_names
            or family.block_sizes != reference.block_sizes
            or family.observation_dimension != reference.observation_dimension
            or not math.isclose(family.rms_noise, reference.rms_noise, rel_tol=0.0, abs_tol=1e-15)
        ):
            raise ValueError("observable classes use incompatible measurement laws")

    # Canonicalize components by their exact observable-law key rather than
    # by first encounter.  Otherwise merely permuting a class's member rows
    # changes which law a fixed RNG component index denotes, even though the
    # proposal measure is mathematically unchanged.  The representative used
    # to evaluate a key is immaterial because equal keys have bit-identical
    # Dirichlet parameters.
    key_to_representative: dict[
        tuple[object, ...], tuple[ProductDirichletFamily, int]
    ] = {}
    class_member_keys: list[tuple[tuple[object, ...], ...]] = []
    for family in items:
        keys = tuple(_law_key(family, index) for index in range(family.member_count))
        class_member_keys.append(keys)
        for member_index, key in enumerate(keys):
            key_to_representative.setdefault(key, (family, member_index))

    ordered_keys = tuple(sorted(key_to_representative))
    key_to_component = {key: index for index, key in enumerate(ordered_keys)}
    representatives = [key_to_representative[key] for key in ordered_keys]
    mappings: list[np.ndarray] = []
    unique_by_class: list[tuple[int, ...]] = []
    for keys in class_member_keys:
        mapping = np.asarray([key_to_component[key] for key in keys], dtype=int)
        mappings.append(mapping)
        unique_by_class.append(tuple(sorted(set(int(value) for value in mapping))))

    component_count = len(representatives)
    class_masses = np.zeros((len(items), component_count), dtype=float)
    for class_index, components in enumerate(unique_by_class):
        mass = 1.0 / (len(items) * len(components))
        class_masses[class_index, np.asarray(components, dtype=int)] = mass
    weights = np.sum(class_masses, axis=0)
    parameters = np.vstack(
        [family.alpha_parameters[index] for family, index in representatives]
    )
    constants = np.asarray(
        [family.log_density_constants[index] for family, index in representatives],
        dtype=float,
    )

    seed_sequence = np.random.SeedSequence(int(seed))
    component_seed, observation_seed = seed_sequence.spawn(2)
    component_rng = np.random.default_rng(component_seed)
    observation_rng = np.random.default_rng(observation_seed)
    sampled = _randomized_systematic_component_indices(
        weights, size, component_rng
    )
    observations = np.empty((size, reference.observation_dimension), dtype=float)
    cursor = 0
    blocks: list[slice] = []
    for block_size in reference.block_sizes:
        blocks.append(slice(cursor, cursor + block_size))
        cursor += block_size
    for component in range(component_count):
        rows = np.flatnonzero(sampled == component)
        if len(rows) == 0:
            continue
        for block in blocks:
            observations[rows, block] = observation_rng.dirichlet(
                parameters[component, block], size=len(rows)
            )

    log_proposal = np.empty(size, dtype=float)
    log_component_weights = np.log(weights)
    exponents = parameters - 1.0
    for start in range(0, size, chunk):
        stop = min(start + chunk, size)
        member_log_density = (
            constants[:, np.newaxis]
            + exponents @ np.log(observations[start:stop]).T
        )
        log_proposal[start:stop] = logsumexp(
            log_component_weights[:, np.newaxis] + member_log_density, axis=0
        )
    if not np.all(np.isfinite(log_proposal)):
        raise MinimaxNumericalError("common proposal has non-finite log density")
    return MulticlassProposalSupport(
        class_labels=labels,
        observations=observations,
        log_proposal_density=log_proposal,
        sampled_component_indices=sampled,
        proposal_component_weights=weights,
        component_class_masses=class_masses,
        member_component_indices=tuple(mappings),
        unique_component_counts_by_class=tuple(len(values) for values in unique_by_class),
        seed=int(seed),
    )


def importance_discretize(
    family: ProductDirichletFamily,
    support: MulticlassProposalSupport,
    *,
    density_chunk_size: int = 2048,
) -> ImportanceDiscretization:
    """Self-normalize each observable law separately on the shared support."""

    if family.observation_dimension != support.observation_dimension:
        raise ValueError("observable laws and proposal support dimensions differ")
    log_density = family.log_density(support.observations, chunk_size=density_chunk_size)
    log_ratio = log_density - support.log_proposal_density[np.newaxis, :]
    log_sums = logsumexp(log_ratio, axis=1)
    log_masses = log_sums - math.log(support.support_size)
    weights = np.exp(log_ratio - log_sums[:, np.newaxis])
    return ImportanceDiscretization(
        member_ids=family.member_ids,
        weights=weights,
        raw_mass_estimates=np.exp(log_masses),
        log_raw_mass_estimates=log_masses,
        effective_sample_sizes=1.0 / np.sum(np.square(weights), axis=1),
    )


def discretize_families(
    families: Sequence[ProductDirichletFamily],
    support: MulticlassProposalSupport,
    *,
    density_chunk_size: int = 2048,
) -> tuple[ImportanceDiscretization, ...]:
    return tuple(
        importance_discretize(family, support, density_chunk_size=density_chunk_size)
        for family in families
    )


@dataclass(frozen=True)
class SparseImportanceDiscretization:
    """Memory-bounded row-stochastic laws on a common proposal support.

    Rows are self-normalized before coefficients at or below ``pruning_cutoff``
    are removed and the retained mass is renormalized.  The removed mass for
    every original row is retained explicitly, so the sparse approximation is
    auditable rather than an implicit underflow shortcut.
    """

    member_ids: tuple[str, ...]
    weights: sparse.csr_matrix
    raw_mass_estimates: np.ndarray
    log_raw_mass_estimates: np.ndarray
    effective_sample_sizes: np.ndarray
    pruned_row_masses: np.ndarray
    pruning_cutoff: float

    def __post_init__(self) -> None:
        identifiers = tuple(str(value) for value in self.member_ids)
        matrix = sparse.csr_matrix(self.weights, dtype=float, copy=True)
        matrix.sort_indices()
        masses = _readonly_float(self.raw_mass_estimates)
        log_masses = _readonly_float(self.log_raw_mass_estimates)
        effective = _readonly_float(self.effective_sample_sizes)
        removed = _readonly_float(self.pruned_row_masses)
        expected = (len(identifiers),)
        if not identifiers or len(set(identifiers)) != len(identifiers):
            raise ValueError("sparse importance member identifiers must be unique")
        if matrix.shape[0] != len(identifiers) or matrix.shape[1] < 1:
            raise ValueError("sparse importance rows and identifiers do not align")
        if (
            masses.shape != expected
            or log_masses.shape != expected
            or effective.shape != expected
            or removed.shape != expected
        ):
            raise ValueError("sparse importance diagnostics do not align")
        if (
            not np.all(np.isfinite(matrix.data))
            or np.any(matrix.data <= 0.0)
            or not np.allclose(
                np.asarray(matrix.sum(axis=1)).ravel(),
                np.ones(len(identifiers)),
                rtol=0.0,
                atol=DEFAULT_ROW_SUM_TOLERANCE,
            )
            or not np.all(np.isfinite(masses))
            or np.any(masses <= 0.0)
            or not np.all(np.isfinite(log_masses))
            or not np.all(np.isfinite(effective))
            or np.any(effective <= 0.0)
            or not np.all(np.isfinite(removed))
            or np.any(removed < 0.0)
        ):
            raise ValueError("invalid sparse importance discretization")
        cutoff = float(self.pruning_cutoff)
        if not math.isfinite(cutoff) or cutoff < 0.0:
            raise ValueError("sparse importance pruning cutoff is invalid")
        object.__setattr__(self, "member_ids", identifiers)
        object.__setattr__(self, "weights", matrix)
        object.__setattr__(self, "raw_mass_estimates", masses)
        object.__setattr__(self, "log_raw_mass_estimates", log_masses)
        object.__setattr__(self, "effective_sample_sizes", effective)
        object.__setattr__(self, "pruned_row_masses", removed)
        object.__setattr__(self, "pruning_cutoff", cutoff)

    @property
    def member_count(self) -> int:
        return len(self.member_ids)

    @property
    def support_size(self) -> int:
        return self.weights.shape[1]

    @property
    def minimum_effective_sample_size(self) -> float:
        return float(np.min(self.effective_sample_sizes))

    @property
    def maximum_absolute_raw_mass_error(self) -> float:
        return float(np.max(np.abs(self.raw_mass_estimates - 1.0)))

    @property
    def maximum_pruned_row_mass(self) -> float:
        return float(np.max(self.pruned_row_masses))

    @property
    def maximum_zero_weight_fraction(self) -> float:
        return float(1.0 - np.min(self.weights.getnnz(axis=1)) / self.support_size)

    def select(self, indices: Sequence[int]) -> "SparseImportanceDiscretization":
        selected = np.asarray(indices, dtype=int)
        if (
            selected.ndim != 1
            or len(selected) < 1
            or np.any(selected < 0)
            or np.any(selected >= self.member_count)
            or len(set(int(value) for value in selected)) != len(selected)
        ):
            raise ValueError("sparse importance selection must be unique and in range")
        return SparseImportanceDiscretization(
            member_ids=tuple(self.member_ids[int(index)] for index in selected),
            weights=self.weights[selected],
            raw_mass_estimates=self.raw_mass_estimates[selected],
            log_raw_mass_estimates=self.log_raw_mass_estimates[selected],
            effective_sample_sizes=self.effective_sample_sizes[selected],
            pruned_row_masses=self.pruned_row_masses[selected],
            pruning_cutoff=self.pruning_cutoff,
        )


def importance_discretize_sparse(
    family: ProductDirichletFamily,
    support: MulticlassProposalSupport,
    *,
    member_batch_size: int = 32,
    density_chunk_size: int = 2048,
    probability_weight_pruning_cutoff: float = DEFAULT_LP_WEIGHT_PRUNING_CUTOFF,
    maximum_pruned_row_mass: float = DEFAULT_MAXIMUM_PRUNED_ROW_MASS,
) -> SparseImportanceDiscretization:
    """Discretize a family in member batches without a dense J-by-S result."""

    if family.observation_dimension != support.observation_dimension:
        raise ValueError("observable laws and proposal support dimensions differ")
    batch_size = int(member_batch_size)
    cutoff = float(probability_weight_pruning_cutoff)
    maximum_removed = float(maximum_pruned_row_mass)
    if batch_size < 1:
        raise ValueError("sparse importance member batch size must be positive")
    if int(density_chunk_size) < 1:
        raise ValueError("sparse importance density chunk size must be positive")
    if not math.isfinite(cutoff) or cutoff < 0.0:
        raise ValueError("sparse importance pruning cutoff is invalid")
    if not math.isfinite(maximum_removed) or maximum_removed < 0.0:
        raise ValueError("maximum sparse importance pruned mass is invalid")

    member_count = family.member_count
    data_parts: list[np.ndarray] = []
    index_parts: list[np.ndarray] = []
    indptr = np.zeros(member_count + 1, dtype=np.int64)
    masses = np.empty(member_count, dtype=float)
    log_masses = np.empty(member_count, dtype=float)
    effective = np.empty(member_count, dtype=float)
    removed = np.empty(member_count, dtype=float)
    log_observation_transpose = np.log(support.observations).T
    for start in range(0, member_count, batch_size):
        stop = min(start + batch_size, member_count)
        selected = family.select(np.arange(start, stop, dtype=int))
        # The observation log is common to every member batch.  Reusing it is
        # essential when screening a 161x161 nuisance grid and is algebraically
        # identical to ProductDirichletFamily.log_density for its precomputed
        # block constants.
        log_ratio = (
            selected.log_density_constants[:, np.newaxis]
            + (selected.alpha_parameters - 1.0) @ log_observation_transpose
        )
        log_ratio -= support.log_proposal_density[np.newaxis, :]
        log_sums = logsumexp(log_ratio, axis=1)
        normalized = np.exp(log_ratio - log_sums[:, np.newaxis])
        batch_log_masses = log_sums - math.log(support.support_size)
        log_masses[start:stop] = batch_log_masses
        masses[start:stop] = np.exp(batch_log_masses)
        effective[start:stop] = 1.0 / np.sum(np.square(normalized), axis=1)
        for local_index, row in enumerate(normalized):
            member_index = start + local_index
            keep = row > cutoff if cutoff > 0.0 else row > 0.0
            indices = np.flatnonzero(keep).astype(np.int32, copy=False)
            retained = float(np.sum(row[indices]))
            removed_mass = float(np.sum(row[~keep]))
            if retained <= 0.0:
                raise MinimaxNumericalError(
                    f"sparse importance pruning removed member {member_index}"
                )
            if removed_mass > maximum_removed:
                raise MinimaxNumericalError(
                    f"sparse importance member {member_index} removed mass "
                    f"{removed_mass:.6g} > {maximum_removed:.6g}"
                )
            data_parts.append(np.asarray(row[indices] / retained, dtype=float))
            index_parts.append(indices)
            removed[member_index] = removed_mass
            indptr[member_index + 1] = indptr[member_index] + len(indices)
    matrix = sparse.csr_matrix(
        (
            np.concatenate(data_parts),
            np.concatenate(index_parts),
            indptr,
        ),
        shape=(member_count, support.support_size),
    )
    return SparseImportanceDiscretization(
        member_ids=family.member_ids,
        weights=matrix,
        raw_mass_estimates=masses,
        log_raw_mass_estimates=log_masses,
        effective_sample_sizes=effective,
        pruned_row_masses=removed,
        pruning_cutoff=cutoff,
    )


def discretize_families_sparse(
    families: Sequence[ProductDirichletFamily],
    support: MulticlassProposalSupport,
    **kwargs: object,
) -> tuple[SparseImportanceDiscretization, ...]:
    """Memory-bounded sparse discretization of every declared class."""

    return tuple(
        importance_discretize_sparse(family, support, **kwargs)
        for family in families
    )


def discretize_selected_members(
    family: ProductDirichletFamily,
    support: MulticlassProposalSupport,
    member_indices: Sequence[int],
    *,
    density_chunk_size: int = 2048,
) -> ImportanceDiscretization:
    """Materialize common-support rows only for explicitly selected members."""

    return importance_discretize(
        family.select(member_indices), support, density_chunk_size=density_chunk_size
    )


@dataclass(frozen=True)
class BatchedRiskEvaluation:
    member_indices: np.ndarray
    member_ids: tuple[str, ...]
    risks: np.ndarray
    raw_mass_estimates: np.ndarray
    log_raw_mass_estimates: np.ndarray
    effective_sample_sizes: np.ndarray

    @property
    def worst_index(self) -> int:
        return int(self.member_indices[int(np.argmax(self.risks))])

    @property
    def worst_risk(self) -> float:
        return float(np.max(self.risks))


def evaluate_member_risks(
    family: ProductDirichletFamily,
    support: MulticlassProposalSupport,
    class_decision_probabilities: np.ndarray,
    *,
    member_indices: Sequence[int] | None = None,
    batch_size: int = 64,
    density_chunk_size: int = 2048,
) -> BatchedRiskEvaluation:
    """Evaluate memberwise errors without materializing a dense class grid.

    Each batch is independently self-normalized against the same proposal.
    The decision input is one class's ``phi_k(y_s)`` vector; nuisance values
    and truth labels are neither accepted nor inspected.
    """

    decision = np.asarray(class_decision_probabilities, dtype=float)
    if decision.shape != (support.support_size,) or not np.all(np.isfinite(decision)):
        raise ValueError("class decision probabilities do not match the support")
    if np.any(decision < 0.0) or np.any(decision > 1.0):
        raise ValueError("class decision probabilities must lie in [0,1]")
    if family.observation_dimension != support.observation_dimension:
        raise ValueError("observable laws and proposal support dimensions differ")
    if member_indices is None:
        indices = np.arange(family.member_count, dtype=int)
    else:
        indices = np.asarray(member_indices, dtype=int)
    if indices.ndim != 1 or len(indices) < 1 or np.any(indices < 0) or np.any(indices >= family.member_count):
        raise ValueError("member indices must be a nonempty in-range vector")
    if int(batch_size) < 1:
        raise ValueError("risk-evaluation batch size must be positive")
    if int(density_chunk_size) < 1:
        raise ValueError("density chunk size must be positive")

    risks = np.empty(len(indices), dtype=float)
    masses = np.empty(len(indices), dtype=float)
    log_masses = np.empty(len(indices), dtype=float)
    effective = np.empty(len(indices), dtype=float)
    miss = 1.0 - decision
    # The observation support is fixed across every screened member.  Compute
    # its logarithm once rather than once per member batch; this is the same
    # product-Dirichlet algebra as ProductDirichletFamily.log_density and is
    # decisive for the full 161x161 topology screens.
    log_observation_transpose = np.log(support.observations).T
    for start in range(0, len(indices), int(batch_size)):
        stop = min(start + int(batch_size), len(indices))
        selected_indices = indices[start:stop]
        log_ratio = (
            family.log_density_constants[selected_indices, np.newaxis]
            + (family.alpha_parameters[selected_indices] - 1.0)
            @ log_observation_transpose
        )
        log_ratio -= support.log_proposal_density[np.newaxis, :]
        log_sums = logsumexp(log_ratio, axis=1)
        log_ratio -= log_sums[:, np.newaxis]
        np.exp(log_ratio, out=log_ratio)
        batch_log_masses = log_sums - math.log(support.support_size)
        risks[start:stop] = log_ratio @ miss
        log_masses[start:stop] = batch_log_masses
        masses[start:stop] = np.exp(batch_log_masses)
        effective[start:stop] = 1.0 / np.sum(np.square(log_ratio), axis=1)
    return BatchedRiskEvaluation(
        member_indices=_readonly_int(indices),
        member_ids=tuple(family.member_ids[int(index)] for index in indices),
        risks=_readonly_float(risks),
        raw_mass_estimates=_readonly_float(masses),
        log_raw_mass_estimates=_readonly_float(log_masses),
        effective_sample_sizes=_readonly_float(effective),
    )


def _validate_probability_classes(
    class_probability_rows: Sequence[np.ndarray],
) -> tuple[np.ndarray, ...]:
    classes = tuple(np.asarray(rows, dtype=float) for rows in class_probability_rows)
    if len(classes) < 2:
        raise ValueError("at least two finite observable-law classes are required")
    support_sizes: set[int] = set()
    for class_index, rows in enumerate(classes):
        if rows.ndim != 2 or min(rows.shape) < 1:
            raise ValueError(f"class {class_index} laws must be a nonempty matrix")
        if not np.all(np.isfinite(rows)) or np.any(rows < 0.0):
            raise ValueError(f"class {class_index} contains invalid probability weights")
        if not np.allclose(
            np.sum(rows, axis=1), 1.0, rtol=0.0, atol=DEFAULT_ROW_SUM_TOLERANCE
        ):
            raise ValueError(f"class {class_index} law rows must each sum to one")
        support_sizes.add(rows.shape[1])
    if len(support_sizes) != 1:
        raise ValueError("all classes must use the same observation support")
    return classes


def _pruned_csr(
    rows: np.ndarray,
    *,
    cutoff: float,
    maximum_pruned_row_mass: float,
    class_label: str,
) -> tuple[sparse.csr_matrix, np.ndarray]:
    if not math.isfinite(cutoff) or cutoff < 0.0:
        raise ValueError("probability pruning cutoff is invalid")
    if not math.isfinite(maximum_pruned_row_mass) or maximum_pruned_row_mass < 0.0:
        raise ValueError("maximum pruned row mass is invalid")
    data_parts: list[np.ndarray] = []
    index_parts: list[np.ndarray] = []
    indptr = np.zeros(len(rows) + 1, dtype=np.int64)
    removed = np.empty(len(rows), dtype=float)
    for row_index, row in enumerate(rows):
        keep = row > cutoff if cutoff > 0.0 else row > 0.0
        indices = np.flatnonzero(keep).astype(np.int32, copy=False)
        data = np.asarray(row[indices], dtype=float)
        retained_mass = float(np.sum(data))
        removed[row_index] = float(np.sum(row[~keep]))
        if retained_mass <= 0.0:
            raise MinimaxNumericalError(f"pruning removed all mass from {class_label} member {row_index}")
        if removed[row_index] > maximum_pruned_row_mass:
            raise MinimaxNumericalError(
                f"{class_label} member {row_index} pruning removed mass "
                f"{removed[row_index]:.6g} > {maximum_pruned_row_mass:.6g}"
            )
        data_parts.append(data / retained_mass)
        index_parts.append(indices)
        indptr[row_index + 1] = indptr[row_index] + len(indices)
    matrix = sparse.csr_matrix(
        (np.concatenate(data_parts), np.concatenate(index_parts), indptr),
        shape=rows.shape,
    )
    return matrix, removed


@dataclass(frozen=True)
class FiniteMultihypothesisSolution:
    """Finite common-support primal, dual, and dense-row certificate."""

    class_labels: tuple[str, ...]
    primal_objective: float
    decision_probabilities: np.ndarray
    solver_member_errors: tuple[np.ndarray, ...]
    member_errors: tuple[np.ndarray, ...]
    dual_member_weights: tuple[np.ndarray, ...]
    dual_class_weights: np.ndarray
    dual_scores: np.ndarray
    dual_objective: float
    signed_duality_residual: float
    absolute_duality_residual: float
    active_member_indices: tuple[np.ndarray, ...]
    dual_supported_member_indices: tuple[np.ndarray, ...]
    randomized_support_indices: np.ndarray
    dual_tie_support_indices: np.ndarray
    maximum_primal_constraint_violation: float
    maximum_simplex_violation: float
    dual_weight_sum_error: float
    maximum_argmax_complementarity_violation: float
    maximum_member_complementarity_violation: float
    objective_recomputation_error: float
    dense_objective_recomputation_error: float
    raw_dense_dual_lower_bound: float
    dense_dual_lower_bound: float
    dense_primal_upper_bound: float
    dense_certificate_gap: float
    maximum_pruned_row_masses: np.ndarray
    retained_lp_coefficient_fraction: float
    lp_constraint_scale: float
    minimum_scaled_retained_coefficient: float
    solver_status: int
    solver_message: str

    @property
    def class_count(self) -> int:
        return len(self.class_labels)

    @property
    def support_size(self) -> int:
        return self.decision_probabilities.shape[1]

    @property
    def classwise_worst_errors(self) -> np.ndarray:
        return _readonly_float([np.max(values) for values in self.member_errors])

    @property
    def global_worst_error(self) -> float:
        return float(np.max(self.classwise_worst_errors))

    @property
    def objective(self) -> float:
        return self.primal_objective


def solve_finite_minimax(
    class_probability_rows: Sequence[np.ndarray],
    *,
    class_labels: Sequence[str] | None = None,
    identical_class_shortcut: bool = True,
    solver_method: str = "highs",
    active_tolerance: float = DEFAULT_LP_TOLERANCE,
    dual_support_tolerance: float = 1.0e-9,
    tie_relative_tolerance: float = 2.0e-7,
    probability_weight_pruning_cutoff: float = DEFAULT_LP_WEIGHT_PRUNING_CUTOFF,
    maximum_pruned_row_mass: float = DEFAULT_MAXIMUM_PRUNED_ROW_MASS,
    lp_constraint_scale: float = DEFAULT_LP_CONSTRAINT_SCALE,
    shared_alias_feasibility_slack: float = 0.0,
) -> FiniteMultihypothesisSolution:
    """Solve the generic memberwise ``K``-class minimax LP.

    Member rows are never averaged or deduplicated.  Sparse coefficient
    pruning is audited per original row and each pruned row is renormalized.
    The returned exact primal/dual residual refers to that sparse LP; the
    unpruned input rows receive a separately labelled lower/upper certificate.
    """

    dense_classes = _validate_probability_classes(class_probability_rows)
    labels = _labels(len(dense_classes), class_labels)
    if bool(identical_class_shortcut):
        row_sets = tuple(
            {
                np.ascontiguousarray(row, dtype=float).tobytes()
                for row in rows
            }
            for rows in dense_classes
        )
        if all(values == row_sets[0] for values in row_sets[1:]):
            return solve_identical_classes_exact(
                dense_classes,
                class_labels=labels,
                active_tolerance=active_tolerance,
            )
    scale = float(lp_constraint_scale)
    if not math.isfinite(scale) or scale <= 0.0:
        raise ValueError("LP constraint scale must be positive and finite")
    alias_slack = float(shared_alias_feasibility_slack)
    if not math.isfinite(alias_slack) or alias_slack < 0.0:
        raise ValueError("shared-law feasibility slack must be finite and nonnegative")
    support_size = dense_classes[0].shape[1]
    class_count = len(dense_classes)
    sparse_classes: list[sparse.csr_matrix] = []
    removed_masses: list[np.ndarray] = []
    for label, rows in zip(labels, dense_classes, strict=True):
        matrix, removed = _pruned_csr(
            rows,
            cutoff=float(probability_weight_pruning_cutoff),
            maximum_pruned_row_mass=float(maximum_pruned_row_mass),
            class_label=label,
        )
        sparse_classes.append(matrix)
        removed_masses.append(removed)
    minimum_scaled = scale * min(float(np.min(matrix.data)) for matrix in sparse_classes)
    if minimum_scaled <= HIGHS_SMALL_MATRIX_VALUE:
        raise MinimaxNumericalError(
            "LP row scaling does not lift every retained coefficient above "
            f"HiGHS' threshold: {minimum_scaled:.12g}"
        )

    # Any law shared by two labels gives the exact finite lower bound 1/2.
    # Retain one explicit sparse-row witness so we can first ask whether that
    # bound is feasible.  If it is, optimization is unnecessary and the two
    # half-weighted member constraints provide the matching dual certificate.
    shared_alias: tuple[int, int, int, int] | None = None

    def sparse_row_key(matrix: sparse.csr_matrix, row_index: int) -> tuple[bytes, bytes]:
        start = int(matrix.indptr[row_index])
        stop = int(matrix.indptr[row_index + 1])
        return (
            np.ascontiguousarray(matrix.indices[start:stop]).tobytes(),
            np.ascontiguousarray(matrix.data[start:stop]).tobytes(),
        )

    for left_index in range(len(sparse_classes)):
        left_keys = {
            sparse_row_key(sparse_classes[left_index], member_index): member_index
            for member_index in range(sparse_classes[left_index].shape[0])
        }
        for right_index in range(left_index + 1, len(sparse_classes)):
            for right_member in range(sparse_classes[right_index].shape[0]):
                key = sparse_row_key(sparse_classes[right_index], right_member)
                if key in left_keys:
                    shared_alias = (
                        left_index,
                        int(left_keys[key]),
                        right_index,
                        right_member,
                    )
                    break
            if shared_alias is not None:
                break
        if shared_alias is not None:
            break

    member_count = sum(matrix.shape[0] for matrix in sparse_classes)

    # A class decision at a support point where every retained member of that
    # class has zero mass cannot improve any constraint for that class.  It
    # can always be reassigned to a class with positive mass at the same node,
    # weakly decreasing risk.  Remove those provably useless variables.  At a
    # node represented by exactly one class, its decision is forced to one and
    # can be eliminated as well.  This reduction is exact for the audited
    # sparse LP and is decisive for low-noise topology problems, where most
    # common-support nodes belong to only one or two numerical class supports.
    represented = np.vstack(
        [np.asarray(matrix.getnnz(axis=0) > 0).ravel() for matrix in sparse_classes]
    )
    represented_count = np.count_nonzero(represented, axis=0)
    uncovered_support = np.flatnonzero(represented_count == 0)
    ambiguous_support = np.flatnonzero(represented_count > 1)
    forced_support = np.flatnonzero(represented_count == 1)
    baseline_class = np.full(support_size, -1, dtype=int)
    if len(ambiguous_support):
        baseline_class[ambiguous_support] = np.argmax(
            represented[:, ambiguous_support], axis=0
        )
    variable_support_by_class = tuple(
        np.flatnonzero(
            represented[class_index]
            & (represented_count > 1)
            & (baseline_class != class_index)
        )
        for class_index in range(class_count)
    )
    variable_offsets = np.cumsum(
        [0] + [len(values) for values in variable_support_by_class]
    )
    variable_count = int(variable_offsets[-1])

    fixed_decision = np.zeros((class_count, support_size), dtype=float)
    if len(uncovered_support):
        # A node carrying zero retained mass for every active constraint is
        # constraint-neutral.  Uniform allocation is setwise and supplies a
        # deterministic starting convention for constraint generation; once
        # a violating member is added, its positive nodes cease to be neutral.
        fixed_decision[:, uncovered_support] = 1.0 / class_count
    if len(forced_support):
        forced_classes = np.argmax(represented[:, forced_support], axis=0)
        fixed_decision[forced_classes, forced_support] = 1.0
    variable_support = np.concatenate(variable_support_by_class)
    fixed_correct_masses: list[np.ndarray] = []
    coefficient_data: list[np.ndarray] = []
    coefficient_rows: list[np.ndarray] = []
    coefficient_columns: list[np.ndarray] = []
    member_offsets = np.cumsum([0] + [matrix.shape[0] for matrix in sparse_classes])
    for class_index, matrix in enumerate(sparse_classes):
        class_fixed = np.concatenate(
            (
                forced_support[represented[class_index, forced_support]],
                ambiguous_support[
                    baseline_class[ambiguous_support] == class_index
                ],
            )
        )
        if len(class_fixed):
            fixed_mass = np.asarray(
                matrix[:, class_fixed].sum(axis=1), dtype=float
            ).ravel()
        else:
            fixed_mass = np.zeros(matrix.shape[0], dtype=float)
        fixed_correct_masses.append(fixed_mass)

        # A nonbaseline variable is that class's direct decision probability,
        # hence enters its own correct-probability term with coefficient -W.
        own = matrix[:, variable_support_by_class[class_index]].tocoo()
        if own.nnz:
            coefficient_rows.append(int(member_offsets[class_index]) + own.row)
            coefficient_columns.append(
                int(variable_offsets[class_index]) + own.col
            )
            coefficient_data.append(-scale * own.data)

        # At nodes where this class is the baseline, phi_baseline is
        # 1-sum(x_nonbaseline).  Every nonbaseline variable there therefore
        # enters -correct_probability with coefficient +W.
        baseline_variable_columns = np.flatnonzero(
            baseline_class[variable_support] == class_index
        )
        if len(baseline_variable_columns):
            baseline_part = matrix[
                :, variable_support[baseline_variable_columns]
            ].tocoo()
            if baseline_part.nnz:
                coefficient_rows.append(
                    int(member_offsets[class_index]) + baseline_part.row
                )
                coefficient_columns.append(
                    baseline_variable_columns[baseline_part.col]
                )
                coefficient_data.append(scale * baseline_part.data)
    if coefficient_data:
        phi_block = sparse.csr_matrix(
            (
                np.concatenate(coefficient_data),
                (
                    np.concatenate(coefficient_rows),
                    np.concatenate(coefficient_columns),
                ),
            ),
            shape=(member_count, variable_count),
        )
    else:
        phi_block = sparse.csr_matrix((member_count, variable_count), dtype=float)
    t_column = sparse.csr_matrix(
        (
            -scale * np.ones(member_count, dtype=float),
            (np.arange(member_count, dtype=int), np.zeros(member_count, dtype=int)),
        ),
        shape=(member_count, 1),
    )
    inequalities = sparse.hstack((phi_block, t_column), format="csr")
    rhs = scale * (
        np.concatenate(fixed_correct_masses) - np.ones(member_count, dtype=float)
    )

    # One nonbaseline variable (a degree-two node) only needs its [0,1]
    # bound.  Higher-degree nodes additionally require sum(x)<=1 so the
    # reconstructed baseline probability stays nonnegative.
    higher_degree_support = np.flatnonzero(represented_count > 2)
    if len(higher_degree_support):
        higher_positions = np.full(support_size, -1, dtype=int)
        higher_positions[higher_degree_support] = np.arange(
            len(higher_degree_support), dtype=int
        )
        higher_columns = np.flatnonzero(
            higher_positions[variable_support] >= 0
        )
        higher_rows = higher_positions[variable_support[higher_columns]]
        higher_block = sparse.csr_matrix(
            (
                np.ones(len(higher_columns), dtype=float),
                (higher_rows, higher_columns),
            ),
            shape=(len(higher_degree_support), variable_count),
        )
        inequalities = sparse.vstack(
            (
                inequalities,
                sparse.hstack(
                    (
                        higher_block,
                        sparse.csr_matrix(
                            (len(higher_degree_support), 1), dtype=float
                        ),
                    ),
                    format="csr",
                ),
            ),
            format="csr",
        )
        rhs = np.concatenate((rhs, np.ones(len(higher_degree_support), dtype=float)))
    method = str(solver_method)
    if method not in {"highs", "highs-ds", "highs-ipm"}:
        raise ValueError("unsupported scipy linprog method")
    solver_options = {
        "primal_feasibility_tolerance": 1.0e-10,
        "dual_feasibility_tolerance": 1.0e-10,
    }
    alias_certificate_used = False
    result = None
    if shared_alias is not None and variable_count > 0:
        certified_lower_bound = 0.5
        certified_upper_bound = certified_lower_bound + alias_slack
        t_coefficients = np.asarray(
            inequalities[:, -1].toarray(), dtype=float
        ).ravel()
        result = linprog(
            np.zeros(variable_count, dtype=float),
            A_ub=inequalities[:, :-1],
            b_ub=rhs - certified_upper_bound * t_coefficients,
            bounds=[(0.0, 1.0)] * variable_count,
            method=method,
            options=solver_options,
        )
        alias_certificate_used = bool(result.success and result.x is not None)
    if not alias_certificate_used:
        objective = np.zeros(variable_count + 1, dtype=float)
        objective[-1] = 1.0
        result = linprog(
            objective,
            A_ub=inequalities,
            b_ub=rhs,
            bounds=[(0.0, 1.0)] * variable_count + [(None, None)],
            method=method,
            options=solver_options,
        )
    assert result is not None
    if not result.success or result.x is None:
        raise MinimaxNumericalError(
            f"finite multiclass minimax LP failed (status {result.status}): {result.message}"
        )

    raw_variables = np.asarray(
        result.x if alias_certificate_used else result.x[:-1], dtype=float
    )
    if len(raw_variables) and np.min(raw_variables) < -2e-8:
        raise MinimaxNumericalError("LP returned negative decision probabilities")
    decision = fixed_decision
    if len(ambiguous_support):
        decision[
            baseline_class[ambiguous_support], ambiguous_support
        ] = 1.0
    for class_index, support_indices in enumerate(variable_support_by_class):
        start = int(variable_offsets[class_index])
        stop = int(variable_offsets[class_index + 1])
        values = np.maximum(raw_variables[start:stop], 0.0)
        decision[class_index, support_indices] = values
        decision[baseline_class[support_indices], support_indices] -= values
    if np.min(decision) < -2e-8:
        raise MinimaxNumericalError("reduced LP reconstructed a negative baseline probability")
    decision = np.maximum(decision, 0.0)
    column_sums = np.sum(decision, axis=0)
    if np.max(np.abs(column_sums - 1.0)) > 2e-7 or np.any(column_sums <= 0.0):
        raise MinimaxNumericalError("LP returned a decision outside the simplex")
    decision /= column_sums[np.newaxis, :]
    primal = (
        0.5 + alias_slack
        if alias_certificate_used
        else float(result.x[-1])
    )
    solver_errors = tuple(
        np.asarray(matrix @ (1.0 - decision[index]), dtype=float)
        for index, matrix in enumerate(sparse_classes)
    )
    dense_errors = tuple(
        rows @ (1.0 - decision[index])
        for index, rows in enumerate(dense_classes)
    )
    if alias_certificate_used:
        # Report the achieved feasible upper bound, not the looser target that
        # made the highly degenerate feasibility problem numerically tractable.
        primal = max(float(np.max(values)) for values in solver_errors)

    all_marginals = np.asarray(result.ineqlin.marginals, dtype=float)
    if len(all_marginals) != len(rhs) or np.max(all_marginals) > 2e-8:
        raise MinimaxNumericalError("LP inequality dual orientation is inconsistent")
    marginals = all_marginals[:member_count]
    flat_dual = scale * np.maximum(-marginals, 0.0)
    if alias_certificate_used:
        assert shared_alias is not None
        flat_dual = np.zeros(member_count, dtype=float)
        left_class, left_member, right_class, right_member = shared_alias
        flat_dual[int(member_offsets[left_class]) + left_member] = 0.5
        flat_dual[int(member_offsets[right_class]) + right_member] = 0.5
    elif variable_count == 0:
        # The sparse finite classes are support-disjoint, so every globally
        # normalized nonnegative member mixture is dual-optimal at value zero.
        # HiGHS is free to return a degenerate mixture concentrated on one
        # class.  Select instead a setwise, class-balanced optimum so duplicate
        # row frequency cannot determine a later continuous-score attempt.
        flat_dual = np.zeros(member_count, dtype=float)
        cursor = 0
        for rows in dense_classes:
            first_by_law: dict[bytes, int] = {}
            for member_index, row in enumerate(rows):
                first_by_law.setdefault(
                    np.ascontiguousarray(row, dtype=float).tobytes(), member_index
                )
            mass = 1.0 / (class_count * len(first_by_law))
            for member_index in first_by_law.values():
                flat_dual[cursor + member_index] = mass
            cursor += len(rows)
    offsets = member_offsets
    dual_weights = tuple(
        flat_dual[offsets[index] : offsets[index + 1]]
        for index in range(class_count)
    )
    dual_class_weights = np.asarray([np.sum(values) for values in dual_weights])
    dual_weight_sum_error = abs(float(np.sum(dual_class_weights)) - 1.0)
    solver_scores = np.vstack(
        [
            np.asarray(matrix.T @ weights, dtype=float).ravel()
            for matrix, weights in zip(sparse_classes, dual_weights, strict=True)
        ]
    )
    maximum_scores = np.max(solver_scores, axis=0)
    dual_objective = float(1.0 - np.sum(maximum_scores))
    signed_residual = primal - dual_objective
    absolute_residual = abs(signed_residual)
    objective_error = abs(primal - max(float(np.max(values)) for values in solver_errors))
    dense_objective_error = abs(primal - max(float(np.max(values)) for values in dense_errors))
    maximum_constraint_violation = max(
        0.0, max(float(np.max(values)) - primal for values in solver_errors)
    )
    simplex_violation = float(np.max(np.abs(np.sum(decision, axis=0) - 1.0)))
    node_scale = np.maximum(np.abs(maximum_scores), 1.0 / support_size)
    tie_mask = np.abs(solver_scores - maximum_scores[np.newaxis, :]) <= (
        float(tie_relative_tolerance) * node_scale[np.newaxis, :]
    )
    positive_decision = decision > float(active_tolerance)
    complementarity_violation = float(
        np.max(
            np.where(
                positive_decision,
                maximum_scores[np.newaxis, :] - solver_scores,
                0.0,
            )
        )
    )
    member_complementarity_violation = max(
        float(np.max(np.abs(weights * (primal - errors))))
        for weights, errors in zip(dual_weights, solver_errors, strict=True)
    )

    certificate_total = float(np.sum(dual_class_weights))
    if certificate_total <= 0.0:
        raise MinimaxNumericalError("finite LP returned an empty dual certificate")
    certificate_weights = tuple(values / certificate_total for values in dual_weights)
    dense_scores = np.vstack(
        [
            weights @ rows
            for weights, rows in zip(
                certificate_weights, dense_classes, strict=True
            )
        ]
    )
    raw_dense_lower = float(1.0 - np.sum(np.max(dense_scores, axis=0)))
    dense_upper = max(float(np.max(values)) for values in dense_errors)
    if raw_dense_lower - dense_upper > 2e-7:
        raise MinimaxNumericalError("dense dual lower bound exceeds dense primal upper bound")
    dense_lower = min(raw_dense_lower, dense_upper)
    dense_gap = dense_upper - dense_lower
    if (
        (
            absolute_residual > 2e-7
            and not (
                alias_certificate_used
                and signed_residual >= -2e-7
                and signed_residual <= alias_slack + 2e-7
            )
        )
        or maximum_constraint_violation > 2e-7
        or simplex_violation > 2e-7
        or dual_weight_sum_error > 2e-7
        or complementarity_violation > 2e-7
        or member_complementarity_violation > 2e-7
        or objective_error > 2e-7
        or dense_objective_error > 2e-7
    ):
        raise MinimaxNumericalError(
            "finite multiclass LP failed primal/dual validation: "
            f"gap={signed_residual:.6g}, constraint={maximum_constraint_violation:.6g}, "
            f"simplex={simplex_violation:.6g}, dual_sum={dual_weight_sum_error:.6g}, "
            f"argmax={complementarity_violation:.6g}, "
            f"member_complementarity={member_complementarity_violation:.6g}, "
            f"objective={objective_error:.6g}, dense_objective={dense_objective_error:.6g}"
        )

    possible_coefficients = member_count * support_size
    retained_fraction = sum(matrix.nnz for matrix in sparse_classes) / possible_coefficients
    return FiniteMultihypothesisSolution(
        class_labels=labels,
        primal_objective=primal,
        decision_probabilities=_readonly_float(decision),
        solver_member_errors=tuple(_readonly_float(values) for values in solver_errors),
        member_errors=tuple(_readonly_float(values) for values in dense_errors),
        dual_member_weights=tuple(_readonly_float(values) for values in dual_weights),
        dual_class_weights=_readonly_float(dual_class_weights),
        dual_scores=_readonly_float(solver_scores),
        dual_objective=dual_objective,
        signed_duality_residual=signed_residual,
        absolute_duality_residual=absolute_residual,
        active_member_indices=tuple(
            _readonly_int(np.flatnonzero(primal - values <= float(active_tolerance)))
            for values in solver_errors
        ),
        dual_supported_member_indices=tuple(
            _readonly_int(np.flatnonzero(values > float(dual_support_tolerance)))
            for values in dual_weights
        ),
        randomized_support_indices=_readonly_int(
            np.flatnonzero(np.count_nonzero(decision > float(active_tolerance), axis=0) > 1)
        ),
        dual_tie_support_indices=_readonly_int(
            np.flatnonzero(np.count_nonzero(tie_mask, axis=0) > 1)
        ),
        maximum_primal_constraint_violation=maximum_constraint_violation,
        maximum_simplex_violation=simplex_violation,
        dual_weight_sum_error=dual_weight_sum_error,
        maximum_argmax_complementarity_violation=complementarity_violation,
        maximum_member_complementarity_violation=member_complementarity_violation,
        objective_recomputation_error=objective_error,
        dense_objective_recomputation_error=dense_objective_error,
        raw_dense_dual_lower_bound=raw_dense_lower,
        dense_dual_lower_bound=dense_lower,
        dense_primal_upper_bound=dense_upper,
        dense_certificate_gap=dense_gap,
        maximum_pruned_row_masses=_readonly_float([np.max(values) for values in removed_masses]),
        retained_lp_coefficient_fraction=float(retained_fraction),
        lp_constraint_scale=scale,
        minimum_scaled_retained_coefficient=minimum_scaled,
        solver_status=int(result.status),
        solver_message=(
            f"{result.message}; "
            + (
                f"verified shared-law bracket [0.5, {0.5 + alias_slack:.12g}] "
                "was primal-feasible; "
                if alias_certificate_used
                else ""
            )
            + "exact sparse support-node reduction retained "
            f"{variable_count} ambiguous class-node variables across "
            f"{len(ambiguous_support)} of {support_size} support nodes"
        ),
    )


def solve_identical_classes_exact(
    class_probability_rows: Sequence[np.ndarray],
    *,
    class_labels: Sequence[str] | None = None,
    active_tolerance: float = DEFAULT_LP_TOLERANCE,
) -> FiniteMultihypothesisSolution:
    """Return the exact ``1 - 1/K`` solution after exact set verification.

    Class row order and duplicate frequency are immaterial.  Equality of
    class averages is insufficient: the set of individual finite laws must
    be bit-identical in every class.
    """

    raw_classes = _validate_probability_classes(class_probability_rows)
    labels = _labels(len(raw_classes), class_labels)

    def keys(rows: np.ndarray) -> tuple[tuple[bytes, ...], dict[bytes, int]]:
        sequence = tuple(np.ascontiguousarray(row, dtype=float).tobytes() for row in rows)
        first: dict[bytes, int] = {}
        for index, key in enumerate(sequence):
            first.setdefault(key, index)
        return sequence, first

    all_keys: list[tuple[bytes, ...]] = []
    first_indices: list[dict[bytes, int]] = []
    for rows in raw_classes:
        sequence, first = keys(rows)
        all_keys.append(sequence)
        first_indices.append(first)
    reference_set = set(all_keys[0])
    if any(set(sequence) != reference_set for sequence in all_keys[1:]):
        raise ValueError("observable law row sets are not exactly identical")

    classes = tuple(rows / np.sum(rows, axis=1, keepdims=True) for rows in raw_classes)
    class_count = len(classes)
    support_size = classes[0].shape[1]
    risk = 1.0 - 1.0 / class_count
    decision = np.full((class_count, support_size), 1.0 / class_count, dtype=float)
    member_errors = tuple(rows @ (1.0 - decision[index]) for index, rows in enumerate(classes))
    matched_key = all_keys[0][0]
    dual_weights: list[np.ndarray] = []
    for rows, first in zip(classes, first_indices, strict=True):
        weights = np.zeros(len(rows), dtype=float)
        weights[first[matched_key]] = 1.0 / class_count
        dual_weights.append(weights)
    scores = np.vstack(
        [weights @ rows for weights, rows in zip(dual_weights, classes, strict=True)]
    )
    dual_objective = float(1.0 - np.sum(np.max(scores, axis=0)))
    positive_coefficients = np.concatenate([rows[rows > 0.0] for rows in classes])
    all_support = np.arange(support_size, dtype=int)
    all_members = tuple(np.arange(len(rows), dtype=int) for rows in classes)
    return FiniteMultihypothesisSolution(
        class_labels=labels,
        primal_objective=risk,
        decision_probabilities=_readonly_float(decision),
        solver_member_errors=tuple(_readonly_float(values) for values in member_errors),
        member_errors=tuple(_readonly_float(values) for values in member_errors),
        dual_member_weights=tuple(_readonly_float(values) for values in dual_weights),
        dual_class_weights=_readonly_float(np.full(class_count, 1.0 / class_count)),
        dual_scores=_readonly_float(scores),
        dual_objective=dual_objective,
        signed_duality_residual=risk - dual_objective,
        absolute_duality_residual=abs(risk - dual_objective),
        active_member_indices=tuple(_readonly_int(values) for values in all_members),
        dual_supported_member_indices=tuple(
            _readonly_int(np.flatnonzero(values > 0.0)) for values in dual_weights
        ),
        randomized_support_indices=_readonly_int(all_support),
        dual_tie_support_indices=_readonly_int(all_support),
        maximum_primal_constraint_violation=0.0,
        maximum_simplex_violation=0.0,
        dual_weight_sum_error=0.0,
        maximum_argmax_complementarity_violation=0.0,
        maximum_member_complementarity_violation=0.0,
        objective_recomputation_error=max(abs(float(np.max(values)) - risk) for values in member_errors),
        dense_objective_recomputation_error=max(abs(float(np.max(values)) - risk) for values in member_errors),
        raw_dense_dual_lower_bound=dual_objective,
        dense_dual_lower_bound=min(dual_objective, risk),
        dense_primal_upper_bound=risk,
        dense_certificate_gap=risk - min(dual_objective, risk),
        maximum_pruned_row_masses=_readonly_float(np.zeros(class_count)),
        retained_lp_coefficient_fraction=1.0,
        lp_constraint_scale=1.0,
        minimum_scaled_retained_coefficient=float(np.min(positive_coefficients)),
        solver_status=0,
        solver_message=(
            "exact identical-K finite-law theorem; numerical optimizer not invoked; "
            "uniform randomized decision"
        ),
    )


# Explicit long-form aliases make call sites self-documenting while retaining
# the concise names used by the earlier binary module.
solve_finite_multihypothesis_minimax = solve_finite_minimax
solve_identical_k_classes_exact = solve_identical_classes_exact


@dataclass(frozen=True)
class MulticlassConstraintGenerationIteration:
    """One solve-and-screen record for K-way constraint generation."""

    iteration: int
    primal_upper_bound: float
    dual_lower_bound: float
    active_member_counts: tuple[int, ...]
    validation_worst_errors: np.ndarray
    validation_worst_member_indices: np.ndarray
    added_validation_indices: tuple[np.ndarray, ...]


@dataclass(frozen=True)
class MulticlassConstraintGenerationResult:
    """A finite master LP certified against every supplied screening row."""

    solution: FiniteMultihypothesisSolution | RuleColumnGenerationSolution
    active_probability_rows: tuple[np.ndarray, ...]
    selected_validation_indices: tuple[np.ndarray, ...]
    validation_errors: tuple[np.ndarray, ...]
    iterations: tuple[MulticlassConstraintGenerationIteration, ...]
    converged: bool
    violation_tolerance: float
    near_worst_tolerance: float


def _screening_matrix(values: np.ndarray | sparse.spmatrix, name: str) -> sparse.csr_matrix:
    matrix = sparse.csr_matrix(values, dtype=float, copy=True)
    if min(matrix.shape) < 1:
        raise ValueError(f"{name} must be a nonempty probability matrix")
    if not np.all(np.isfinite(matrix.data)) or np.any(matrix.data < 0.0):
        raise ValueError(f"{name} contains invalid probability coefficients")
    if not np.allclose(
        np.asarray(matrix.sum(axis=1)).ravel(),
        np.ones(matrix.shape[0]),
        rtol=0.0,
        atol=DEFAULT_ROW_SUM_TOLERANCE,
    ):
        raise ValueError(f"{name} rows must each sum to one")
    matrix.sort_indices()
    return matrix


def _row_bytes(row: np.ndarray) -> bytes:
    return np.ascontiguousarray(row, dtype=float).tobytes()


def run_constraint_generation(
    initial_class_rows: Sequence[np.ndarray | sparse.spmatrix],
    validation_class_rows: Sequence[np.ndarray | sparse.spmatrix],
    *,
    class_labels: Sequence[str] | None = None,
    violation_tolerance: float = 5.0e-4,
    near_worst_tolerance: float = 1.0e-4,
    maximum_additions_per_class: int = 12,
    max_iterations: int = 30,
    shared_alias_feasibility_slack: float = 0.0,
    solver_backend: str = "rule_column_generation",
    solver_convergence_tolerance: float = 2.0e-7,
    solver_maximum_iterations: int = 500,
) -> MulticlassConstraintGenerationResult:
    """Solve a K-way master LP while screening every supplied member row.

    Screening matrices may be sparse, but every selected member is inserted
    into the master as its own row.  No class average is formed.  The common
    support is fixed for the entire call, and each re-solve is followed by a
    complete memberwise risk screen.  Up to a declared number of the worst
    violating rows per class are added together to avoid arbitrary uncovered
    support decisions causing one-at-a-time tail chasing.
    """

    initial = tuple(
        _screening_matrix(values, f"initial class {index}")
        for index, values in enumerate(initial_class_rows)
    )
    validation = tuple(
        _screening_matrix(values, f"validation class {index}")
        for index, values in enumerate(validation_class_rows)
    )
    if len(initial) < 2 or len(validation) != len(initial):
        raise ValueError("constraint generation needs aligned K-way classes")
    labels = _labels(len(initial), class_labels)
    support_sizes = {
        matrix.shape[1] for matrix in (*initial, *validation)
    }
    if len(support_sizes) != 1:
        raise ValueError("constraint-generation rows must share one support")
    tolerance = float(violation_tolerance)
    near_tolerance = float(near_worst_tolerance)
    additions_per_class = int(maximum_additions_per_class)
    iteration_limit = int(max_iterations)
    backend = str(solver_backend)
    if (
        not math.isfinite(tolerance)
        or tolerance <= 0.0
        or not math.isfinite(near_tolerance)
        or near_tolerance < 0.0
        or additions_per_class < 1
        or iteration_limit < 1
    ):
        raise ValueError("constraint-generation controls are invalid")
    if backend not in {"rule_column_generation", "direct_primal"}:
        raise ValueError("unsupported constraint-generation solver backend")

    active = [matrix.toarray() for matrix in initial]
    active_keys = [
        {_row_bytes(row) for row in rows}
        for rows in active
    ]
    selected: list[list[int]] = [[] for _ in initial]
    records: list[MulticlassConstraintGenerationIteration] = []
    validation_errors: tuple[np.ndarray, ...] = tuple()
    solution: FiniteMultihypothesisSolution | RuleColumnGenerationSolution | None = None
    converged = False
    warm_rule_labels: np.ndarray | None = None

    for iteration in range(iteration_limit + 1):
        solved_active_counts = tuple(len(rows) for rows in active)
        if backend == "rule_column_generation":
            solution = solve_rule_column_generation(
                tuple(active),
                class_labels=labels,
                convergence_tolerance=float(solver_convergence_tolerance),
                maximum_iterations=int(solver_maximum_iterations),
                initial_rule_labels=warm_rule_labels,
            )
            if not solution.converged:
                raise MinimaxNumericalError(
                    "constraint-generation master rule columns did not converge"
                )
            warm_rule_labels = solution.generated_rule_labels
            dual_lower_bound = solution.dual_lower_bound
        else:
            solution = solve_finite_minimax(
                tuple(active),
                class_labels=labels,
                shared_alias_feasibility_slack=shared_alias_feasibility_slack,
            )
            dual_lower_bound = solution.dual_objective
        validation_errors = tuple(
            np.asarray(
                matrix @ (1.0 - solution.decision_probabilities[class_index]),
                dtype=float,
            ).ravel()
            for class_index, matrix in enumerate(validation)
        )
        worst_indices = np.asarray(
            [int(np.argmax(values)) for values in validation_errors], dtype=int
        )
        worst_errors = np.asarray(
            [values[index] for values, index in zip(validation_errors, worst_indices, strict=True)],
            dtype=float,
        )
        added_this_iteration: list[np.ndarray] = []
        if iteration == iteration_limit:
            added_this_iteration = [np.asarray([], dtype=int) for _ in initial]
        else:
            for class_index, (matrix, errors) in enumerate(
                zip(validation, validation_errors, strict=True)
            ):
                ordered = np.argsort(-errors, kind="stable")
                additions: list[int] = []
                worst = float(errors[int(ordered[0])])
                for candidate in ordered:
                    candidate_index = int(candidate)
                    risk = float(errors[candidate_index])
                    qualifies = bool(
                        risk > solution.primal_objective + tolerance
                        or (
                            near_tolerance > 0.0
                            and worst - risk <= near_tolerance
                            and risk >= solution.primal_objective - near_tolerance
                        )
                    )
                    if not qualifies:
                        if risk < solution.primal_objective - near_tolerance:
                            break
                        continue
                    row = matrix.getrow(candidate_index).toarray().ravel()
                    key = _row_bytes(row)
                    if key in active_keys[class_index]:
                        continue
                    additions.append(candidate_index)
                    active_keys[class_index].add(key)
                    active[class_index] = np.vstack((active[class_index], row))
                    selected[class_index].append(candidate_index)
                    if len(additions) >= additions_per_class:
                        break
                added_this_iteration.append(np.asarray(additions, dtype=int))
        records.append(
            MulticlassConstraintGenerationIteration(
                iteration=iteration,
                primal_upper_bound=solution.primal_objective,
                dual_lower_bound=dual_lower_bound,
                active_member_counts=solved_active_counts,
                validation_worst_errors=_readonly_float(worst_errors),
                validation_worst_member_indices=_readonly_int(worst_indices),
                added_validation_indices=tuple(
                    _readonly_int(values) for values in added_this_iteration
                ),
            )
        )
        no_additions = all(len(values) == 0 for values in added_this_iteration)
        all_within = bool(
            np.all(worst_errors <= solution.primal_objective + tolerance)
        )
        if no_additions:
            converged = all_within
            break

    if solution is None:  # pragma: no cover - guarded above
        raise RuntimeError("constraint generation did not execute")
    return MulticlassConstraintGenerationResult(
        solution=solution,
        active_probability_rows=tuple(_readonly_float(rows) for rows in active),
        selected_validation_indices=tuple(
            _readonly_int(values) for values in selected
        ),
        validation_errors=tuple(_readonly_float(values) for values in validation_errors),
        iterations=tuple(records),
        converged=converged,
        violation_tolerance=tolerance,
        near_worst_tolerance=near_tolerance,
    )


@dataclass(frozen=True)
class ContinuousMulticlassDecisionRule:
    """Deployable K-way density-score rule whose only input is observed MIDs."""

    class_labels: tuple[str, ...]
    class_families: tuple[ProductDirichletFamily, ...]
    density_coefficients: tuple[np.ndarray, ...]
    tie_log_tolerance: float = 2.0e-10

    def __post_init__(self) -> None:
        labels = _labels(len(self.class_families), self.class_labels)
        families = tuple(self.class_families)
        coefficients = tuple(
            _readonly_float(values) for values in self.density_coefficients
        )
        if len(families) < 2 or len(coefficients) != len(families):
            raise ValueError("continuous multiclass rule inputs do not align")
        reference = families[0]
        for family, values in zip(families, coefficients, strict=True):
            if (
                family.block_names != reference.block_names
                or family.block_sizes != reference.block_sizes
                or family.observation_dimension != reference.observation_dimension
                or values.shape != (family.member_count,)
                or not np.all(np.isfinite(values))
                or np.any(values < 0.0)
                or float(np.sum(values)) <= 0.0
            ):
                raise ValueError("continuous multiclass density scores are invalid")
        tolerance = float(self.tie_log_tolerance)
        if not math.isfinite(tolerance) or tolerance < 0.0:
            raise ValueError("continuous multiclass tie tolerance is invalid")
        object.__setattr__(self, "class_labels", labels)
        object.__setattr__(self, "class_families", families)
        object.__setattr__(self, "density_coefficients", coefficients)
        object.__setattr__(self, "tie_log_tolerance", tolerance)

    def log_scores(self, observations: np.ndarray) -> np.ndarray:
        """Return one Z-corrected dual log score per observation and class."""

        columns: list[np.ndarray] = []
        for family, coefficients in zip(
            self.class_families, self.density_coefficients, strict=True
        ):
            positive = np.flatnonzero(coefficients > 0.0)
            selected = family.select(positive)
            member_log_density = selected.log_density(observations)
            columns.append(
                logsumexp(
                    np.log(coefficients[positive])[:, np.newaxis]
                    + member_log_density,
                    axis=0,
                )
            )
        return _readonly_float(np.column_stack(columns))

    def decision_probabilities(self, observations: np.ndarray) -> np.ndarray:
        """Return K-way probabilities from argmax scores and uniform score ties."""

        scores = self.log_scores(observations)
        maximum = np.max(scores, axis=1)
        ties = maximum[:, np.newaxis] - scores <= self.tie_log_tolerance
        probabilities = ties / np.count_nonzero(ties, axis=1)[:, np.newaxis]
        return _readonly_float(probabilities)


@dataclass(frozen=True)
class ContinuousMulticlassDiagnostics:
    rule: ContinuousMulticlassDecisionRule
    finite_support_member_errors: tuple[np.ndarray, ...]
    finite_support_worst_error: float
    objective_difference: float
    maximum_member_error_difference_from_primal: float
    randomized_support_count: int
    stable_on_finite_support: bool
    reproduction_tolerance: float


def build_continuous_multiclass_rule(
    solution: FiniteMultihypothesisSolution,
    class_families: Sequence[ProductDirichletFamily],
    class_discretizations: Sequence[
        ImportanceDiscretization | SparseImportanceDiscretization
    ],
    support: MulticlassProposalSupport,
    *,
    reproduction_tolerance: float = 7.5e-4,
    dual_coefficient_tolerance: float = 1.0e-12,
) -> ContinuousMulticlassDiagnostics:
    """Attempt the Z-corrected K-way dual-density representation.

    Relative coefficient totals across classes are deliberately preserved.
    Uniform randomization is used only for observable score ties.  If any
    class has no positive dual score, or if this fixed rule does not reproduce
    all finite-support member errors within tolerance, callers must report the
    representation as unavailable rather than substitute another classifier.
    """

    families = tuple(class_families)
    discretizations = tuple(class_discretizations)
    if (
        len(families) != solution.class_count
        or len(discretizations) != solution.class_count
    ):
        raise ValueError("continuous multiclass inputs do not align with the LP")
    tolerance = float(reproduction_tolerance)
    if not math.isfinite(tolerance) or tolerance <= 0.0:
        raise ValueError("continuous reproduction tolerance must be positive")
    coefficients: list[np.ndarray] = []
    for class_index, (family, discretization) in enumerate(
        zip(families, discretizations, strict=True)
    ):
        dual = solution.dual_member_weights[class_index]
        masses = np.asarray(discretization.raw_mass_estimates, dtype=float)
        if (
            dual.shape != (family.member_count,)
            or masses.shape != (family.member_count,)
            or discretization.weights.shape
            != (family.member_count, support.support_size)
        ):
            raise ValueError("continuous multiclass family rows do not align")
        values = dual / masses
        if float(np.sum(values)) <= float(dual_coefficient_tolerance):
            raise ContinuousRepresentationUnavailable(
                f"finite dual has no positive score for {solution.class_labels[class_index]}"
            )
        coefficients.append(values)
    rule = ContinuousMulticlassDecisionRule(
        class_labels=solution.class_labels,
        class_families=families,
        density_coefficients=tuple(coefficients),
    )
    probabilities = rule.decision_probabilities(support.observations)
    errors = tuple(
        np.asarray(
            discretization.weights @ (1.0 - probabilities[:, class_index]),
            dtype=float,
        ).ravel()
        for class_index, discretization in enumerate(discretizations)
    )
    maximum_difference = max(
        float(np.max(np.abs(observed - expected)))
        for observed, expected in zip(errors, solution.member_errors, strict=True)
    )
    worst = max(float(np.max(values)) for values in errors)
    objective_difference = abs(worst - solution.primal_objective)
    stable = bool(
        maximum_difference <= tolerance
        and objective_difference <= tolerance
        and worst <= solution.primal_objective + tolerance
        and np.max(np.abs(np.sum(probabilities, axis=1) - 1.0)) <= 2.0e-12
    )
    return ContinuousMulticlassDiagnostics(
        rule=rule,
        finite_support_member_errors=tuple(_readonly_float(values) for values in errors),
        finite_support_worst_error=worst,
        objective_difference=objective_difference,
        maximum_member_error_difference_from_primal=maximum_difference,
        randomized_support_count=int(
            np.count_nonzero(np.count_nonzero(probabilities > 0.0, axis=1) > 1)
        ),
        stable_on_finite_support=stable,
        reproduction_tolerance=tolerance,
    )
