"""MID-only numerical minimax tests for finite composite law classes.

This module deliberately starts *after* exact MID classes have been
constructed.  It has no model, flux, or inverse-MFA dependency.  One exact
MID row defines a product of independent Dirichlet laws, one per metabolite
block.  A common numerical proposal supplies a shared observation support;
importance weights turn every class member into a separate row-stochastic
law on that support.  The resulting finite minimax problem is solved as one
linear programme with every null and alternative constraint retained.

The balanced proposal is only an integration device.  In particular, its
weights are not probabilities assigned to feasible biological states.
Duplicate law centres are removed before the proposal is formed so that
duplicating rows without changing a represented class set cannot change the
proposal.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Protocol, Sequence, runtime_checkable

import numpy as np
from scipy import sparse
from scipy.optimize import linprog
from scipy.special import gammaln, logsumexp


DEFAULT_ROW_SUM_TOLERANCE = 2.0e-12
DEFAULT_LP_TOLERANCE = 1.0e-8
DEFAULT_LP_WEIGHT_PRUNING_CUTOFF = 1.0e-15
DEFAULT_MAXIMUM_PRUNED_ROW_MASS = 1.0e-11
HIGHS_SMALL_MATRIX_VALUE = 1.0e-9
# HiGHS ignores matrix entries no larger than 1e-9 in this runtime.  Since
# explicitly retained importance coefficients are strictly greater than the
# 1e-15 pruning cutoff, multiplying each complete inequality (including its
# RHS) by 1e6 lifts every retained coefficient above that internal threshold
# without changing the mathematical LP.
DEFAULT_LP_CONSTRAINT_SCALE = 1.0e6


class MinimaxNumericalError(RuntimeError):
    """Raised when a numerical minimax calculation is invalid or unstable."""


class ContinuousRepresentationUnavailable(MinimaxNumericalError):
    """Raised when the finite LP does not support a usable mixture test."""


@runtime_checkable
class MIDClassLike(Protocol):
    """Minimal, MID-only interface accepted at the testing boundary."""

    member_ids: tuple[str, ...]
    blocks: tuple[tuple[str, int, int], ...]
    exact_mids: np.ndarray


def _readonly_float_array(values: np.ndarray | Sequence[float]) -> np.ndarray:
    result = np.array(values, dtype=float, copy=True)
    result.setflags(write=False)
    return result


def _readonly_int_array(values: np.ndarray | Sequence[int]) -> np.ndarray:
    result = np.array(values, dtype=int, copy=True)
    result.setflags(write=False)
    return result


def dirichlet_rms_kappa(probabilities: Sequence[float], rms_noise: float) -> float:
    """Return the established concentration for per-component RMS ``r``.

    For a ``K``-component MID centre ``p`` and
    ``Y ~ Dirichlet(kappa * p)``, the convention is

    ``E[||Y-p||_2**2 / K] = r**2``.
    """

    centre = np.asarray(probabilities, dtype=float)
    noise = float(rms_noise)
    if centre.ndim != 1 or len(centre) < 2:
        raise ValueError("a Dirichlet MID block needs at least two components")
    if not math.isfinite(noise) or noise <= 0.0:
        raise ValueError("RMS measurement noise must be positive and finite")
    if not np.all(np.isfinite(centre)) or np.any(centre <= 0.0):
        raise ValueError("Dirichlet MID centres must be finite and positive")
    if not math.isclose(float(np.sum(centre)), 1.0, rel_tol=0.0, abs_tol=2.0e-12):
        raise ValueError("a Dirichlet MID centre must sum to one")
    concentration = (
        (1.0 - float(np.sum(np.square(centre))))
        / (len(centre) * noise * noise)
        - 1.0
    )
    if not math.isfinite(concentration) or concentration <= 0.0:
        raise ValueError(f"non-positive Dirichlet concentration {concentration}")
    reproduced = math.sqrt(
        (1.0 - float(np.sum(np.square(centre))))
        / (len(centre) * (concentration + 1.0))
    )
    if not math.isclose(reproduced, noise, rel_tol=2.0e-13, abs_tol=1.0e-15):
        raise MinimaxNumericalError("Dirichlet RMS identity did not reproduce r")
    return concentration


@dataclass(frozen=True)
class ProductDirichletFamily:
    """A finite family of observable laws described entirely by exact MIDs."""

    member_ids: tuple[str, ...]
    block_names: tuple[str, ...]
    block_sizes: tuple[int, ...]
    exact_mids: np.ndarray
    alpha_parameters: np.ndarray
    log_density_constants: np.ndarray
    rms_noise: float

    def __post_init__(self) -> None:
        identifiers = tuple(str(value) for value in self.member_ids)
        names = tuple(str(value) for value in self.block_names)
        sizes = tuple(int(value) for value in self.block_sizes)
        mids = np.array(self.exact_mids, dtype=float, copy=True)
        parameters = np.array(self.alpha_parameters, dtype=float, copy=True)
        constants = np.array(self.log_density_constants, dtype=float, copy=True)
        if not identifiers or len(set(identifiers)) != len(identifiers):
            raise ValueError("observable-law member identifiers must be nonempty and unique")
        if not names or len(names) != len(sizes) or any(value < 2 for value in sizes):
            raise ValueError("invalid product-Dirichlet block layout")
        expected_shape = (len(identifiers), sum(sizes))
        if mids.shape != expected_shape or parameters.shape != expected_shape:
            raise ValueError("MID centres or Dirichlet parameters have unexpected shape")
        if constants.shape != (len(identifiers),):
            raise ValueError("Dirichlet density constants have unexpected shape")
        if (
            not np.all(np.isfinite(mids))
            or not np.all(np.isfinite(parameters))
            or not np.all(np.isfinite(constants))
            or np.any(mids <= 0.0)
            or np.any(parameters <= 0.0)
        ):
            raise ValueError("observable-law arrays must be finite and positive")
        cursor = 0
        for size in sizes:
            stop = cursor + size
            if not np.allclose(
                np.sum(mids[:, cursor:stop], axis=1),
                1.0,
                rtol=0.0,
                atol=2.0e-12,
            ):
                raise ValueError("each exact MID block must sum to one")
            cursor = stop
        for array in (mids, parameters, constants):
            array.setflags(write=False)
        object.__setattr__(self, "member_ids", identifiers)
        object.__setattr__(self, "block_names", names)
        object.__setattr__(self, "block_sizes", sizes)
        object.__setattr__(self, "exact_mids", mids)
        object.__setattr__(self, "alpha_parameters", parameters)
        object.__setattr__(self, "log_density_constants", constants)
        object.__setattr__(self, "rms_noise", float(self.rms_noise))

    @property
    def member_count(self) -> int:
        return len(self.member_ids)

    @property
    def observation_dimension(self) -> int:
        return sum(self.block_sizes)

    @property
    def block_slices(self) -> tuple[slice, ...]:
        cursor = 0
        result: list[slice] = []
        for size in self.block_sizes:
            result.append(slice(cursor, cursor + size))
            cursor += size
        return tuple(result)

    def select(self, indices: Sequence[int]) -> "ProductDirichletFamily":
        selected = np.asarray(indices, dtype=int)
        if selected.ndim != 1 or len(selected) < 1:
            raise ValueError("at least one observable-law member must be selected")
        if np.any(selected < 0) or np.any(selected >= self.member_count):
            raise IndexError("observable-law member index is out of range")
        if len(set(int(value) for value in selected)) != len(selected):
            raise ValueError("observable-law selection indices must be unique")
        return ProductDirichletFamily(
            member_ids=tuple(self.member_ids[int(value)] for value in selected),
            block_names=self.block_names,
            block_sizes=self.block_sizes,
            exact_mids=self.exact_mids[selected],
            alpha_parameters=self.alpha_parameters[selected],
            log_density_constants=self.log_density_constants[selected],
            rms_noise=self.rms_noise,
        )

    def log_density(
        self, observations: np.ndarray, *, chunk_size: int = 2048
    ) -> np.ndarray:
        """Evaluate every member density on the same observations."""

        values = _validate_observations(
            observations, self.block_sizes, require_nonempty=True
        )
        if int(chunk_size) < 1:
            raise ValueError("log-density chunk size must be positive")
        result = np.empty((self.member_count, len(values)), dtype=float)
        exponents = self.alpha_parameters - 1.0
        for start in range(0, len(values), int(chunk_size)):
            stop = min(start + int(chunk_size), len(values))
            result[:, start:stop] = (
                self.log_density_constants[:, np.newaxis]
                + exponents @ np.log(values[start:stop]).T
            )
        if not np.all(np.isfinite(result)):
            raise MinimaxNumericalError("non-finite product-Dirichlet log density")
        return result

    def sample_member(
        self,
        member_index: int,
        count: int,
        rng: np.random.Generator,
    ) -> np.ndarray:
        """Draw MID observations from one observable class member."""

        index = int(member_index)
        sample_count = int(count)
        if index < 0 or index >= self.member_count:
            raise IndexError("observable-law member index is out of range")
        if sample_count < 1:
            raise ValueError("observation count must be positive")
        result = np.empty((sample_count, self.observation_dimension), dtype=float)
        for block in self.block_slices:
            result[:, block] = rng.dirichlet(
                self.alpha_parameters[index, block], size=sample_count
            )
        return _validate_observations(result, self.block_sizes, require_nonempty=True)


def concatenate_families(
    families: Sequence[ProductDirichletFamily],
    *,
    member_id_prefixes: Sequence[str] | None = None,
) -> ProductDirichletFamily:
    """Concatenate observable families without introducing class averaging.

    This helper is useful after constraint generation: concatenate the initial
    family and the selected dense-grid members in exactly the same order as
    their LP rows.  Prefixes make otherwise opaque identifiers unambiguous;
    they have no role in a decision statistic.
    """

    items = tuple(families)
    if not items:
        raise ValueError("at least one observable family is required")
    reference = items[0]
    for family in items[1:]:
        if (
            family.block_names != reference.block_names
            or family.block_sizes != reference.block_sizes
            or family.observation_dimension != reference.observation_dimension
            or not math.isclose(
                family.rms_noise,
                reference.rms_noise,
                rel_tol=0.0,
                abs_tol=1.0e-15,
            )
        ):
            raise ValueError("observable families use incompatible measurement laws")
    if member_id_prefixes is None:
        prefixes: tuple[str | None, ...] = (None,) * len(items)
    else:
        if len(member_id_prefixes) != len(items):
            raise ValueError("one member-identifier prefix is required per family")
        prefixes = tuple(str(value) for value in member_id_prefixes)
    identifiers = tuple(
        (
            identifier
            if prefix is None
            else f"{prefix}:{identifier}"
        )
        for family, prefix in zip(items, prefixes, strict=True)
        for identifier in family.member_ids
    )
    if len(set(identifiers)) != len(identifiers):
        raise ValueError(
            "concatenated member identifiers collide; supply member_id_prefixes"
        )
    return ProductDirichletFamily(
        member_ids=identifiers,
        block_names=reference.block_names,
        block_sizes=reference.block_sizes,
        exact_mids=np.vstack([family.exact_mids for family in items]),
        alpha_parameters=np.vstack(
            [family.alpha_parameters for family in items]
        ),
        log_density_constants=np.concatenate(
            [family.log_density_constants for family in items]
        ),
        rms_noise=reference.rms_noise,
    )


def family_from_mid_class(
    mid_class: MIDClassLike, *, rms_noise: float
) -> ProductDirichletFamily:
    """Create observable laws from the deliberately narrow ``MIDClass`` API."""

    # Access only the three fields in MIDClassLike.  Hidden construction
    # metadata is intentionally neither accepted nor inspected here.
    identifiers = tuple(str(value) for value in mid_class.member_ids)
    blocks = tuple(
        (str(name), int(start), int(stop)) for name, start, stop in mid_class.blocks
    )
    mids = np.asarray(mid_class.exact_mids, dtype=float)
    if mids.ndim != 2 or mids.shape[0] != len(identifiers):
        raise ValueError("MID-class rows and member identifiers do not align")
    cursor = 0
    block_names: list[str] = []
    block_sizes: list[int] = []
    for name, start, stop in blocks:
        if start != cursor or stop <= start or stop > mids.shape[1]:
            raise ValueError("MID blocks must be contiguous, nonempty, and ordered")
        block_names.append(name)
        block_sizes.append(stop - start)
        cursor = stop
    if cursor != mids.shape[1]:
        raise ValueError("MID blocks do not cover the observation")

    parameters = np.empty_like(mids)
    constants = np.zeros(len(mids), dtype=float)
    cursor = 0
    for size in block_sizes:
        stop = cursor + size
        for row_index, centre in enumerate(mids[:, cursor:stop]):
            concentration = dirichlet_rms_kappa(centre, rms_noise)
            block_parameters = concentration * centre
            parameters[row_index, cursor:stop] = block_parameters
            constants[row_index] += float(
                gammaln(np.sum(block_parameters))
                - np.sum(gammaln(block_parameters))
            )
        cursor = stop
    return ProductDirichletFamily(
        member_ids=identifiers,
        block_names=tuple(block_names),
        block_sizes=tuple(block_sizes),
        exact_mids=mids,
        alpha_parameters=parameters,
        log_density_constants=constants,
        rms_noise=float(rms_noise),
    )


def _validate_observations(
    observations: np.ndarray,
    block_sizes: Sequence[int],
    *,
    require_nonempty: bool,
) -> np.ndarray:
    values = np.asarray(observations, dtype=float)
    if values.ndim == 1:
        values = values[np.newaxis, :]
    expected_dimension = sum(int(value) for value in block_sizes)
    if values.ndim != 2 or values.shape[1] != expected_dimension:
        raise ValueError("MID observations have unexpected shape")
    if require_nonempty and len(values) < 1:
        raise ValueError("at least one MID observation is required")
    if not np.all(np.isfinite(values)) or np.any(values <= 0.0):
        raise ValueError("MID observations must be finite and strictly positive")
    cursor = 0
    for size in block_sizes:
        stop = cursor + int(size)
        if not np.allclose(
            np.sum(values[:, cursor:stop], axis=1),
            1.0,
            rtol=0.0,
            atol=2.0e-12,
        ):
            raise ValueError("each observed MID block must sum to one")
        cursor = stop
    return values


def _law_key(family: ProductDirichletFamily, index: int) -> tuple[object, ...]:
    """Exact observable-law identity used only to remove repeated rows."""

    row = np.ascontiguousarray(family.alpha_parameters[int(index)])
    return (family.block_names, family.block_sizes, row.dtype.str, row.tobytes())


@dataclass(frozen=True)
class CommonProposalSupport:
    """Shared observations drawn from a balanced numerical proposal."""

    observations: np.ndarray
    log_proposal_density: np.ndarray
    sampled_component_indices: np.ndarray
    proposal_component_weights: np.ndarray
    unique_null_component_count: int
    unique_alternative_component_count: int
    focused_null_component_count: int
    focused_alternative_component_count: int
    focus_mass: float
    proposal_component_count: int
    seed: int

    def __post_init__(self) -> None:
        observations = _readonly_float_array(self.observations)
        log_density = _readonly_float_array(self.log_proposal_density)
        component_indices = _readonly_int_array(self.sampled_component_indices)
        component_weights = _readonly_float_array(self.proposal_component_weights)
        count = len(observations)
        if observations.ndim != 2 or count < 1:
            raise ValueError("common proposal support must be a nonempty matrix")
        if log_density.shape != (count,) or component_indices.shape != (count,):
            raise ValueError("proposal support arrays do not align")
        if component_weights.shape != (int(self.proposal_component_count),):
            raise ValueError("proposal component weights have unexpected shape")
        if (
            not np.all(np.isfinite(log_density))
            or np.any(component_indices < 0)
            or np.any(component_indices >= int(self.proposal_component_count))
            or np.any(component_weights <= 0.0)
            or not math.isclose(
                float(np.sum(component_weights)), 1.0, rel_tol=0.0, abs_tol=2.0e-14
            )
        ):
            raise ValueError("invalid common-proposal support")
        object.__setattr__(self, "observations", observations)
        object.__setattr__(self, "log_proposal_density", log_density)
        object.__setattr__(self, "sampled_component_indices", component_indices)
        object.__setattr__(self, "proposal_component_weights", component_weights)
        focus_mass = float(self.focus_mass)
        if not 0.0 <= focus_mass < 1.0:
            raise ValueError("proposal focus mass must lie in [0,1)")
        if int(self.focused_null_component_count) < 0 or int(
            self.focused_alternative_component_count
        ) < 0:
            raise ValueError("focused proposal component counts cannot be negative")
        if (
            int(self.focused_null_component_count)
            > int(self.unique_null_component_count)
            or int(self.focused_alternative_component_count)
            > int(self.unique_alternative_component_count)
        ):
            raise ValueError("focused component count exceeds its distinct class size")
        object.__setattr__(self, "focus_mass", focus_mass)
        object.__setattr__(self, "seed", int(self.seed))

    @property
    def support_size(self) -> int:
        return len(self.observations)

    @property
    def observation_dimension(self) -> int:
        return self.observations.shape[1]

    def subset(self, support_size: int) -> "CommonProposalSupport":
        """Return a nested prefix while retaining the same proposal density."""

        size = int(support_size)
        if size < 1 or size > self.support_size:
            raise ValueError("proposal subset size is out of range")
        return CommonProposalSupport(
            observations=self.observations[:size],
            log_proposal_density=self.log_proposal_density[:size],
            sampled_component_indices=self.sampled_component_indices[:size],
            proposal_component_weights=self.proposal_component_weights,
            unique_null_component_count=self.unique_null_component_count,
            unique_alternative_component_count=self.unique_alternative_component_count,
            focused_null_component_count=self.focused_null_component_count,
            focused_alternative_component_count=(
                self.focused_alternative_component_count
            ),
            focus_mass=self.focus_mass,
            proposal_component_count=self.proposal_component_count,
            seed=self.seed,
        )


def build_balanced_proposal_support(
    null_family: ProductDirichletFamily,
    alternative_family: ProductDirichletFamily,
    *,
    support_size: int,
    seed: int,
    density_chunk_size: int = 1024,
    focus_mass: float = 0.0,
    null_focus_indices: Sequence[int] | None = None,
    alternative_focus_indices: Sequence[int] | None = None,
) -> CommonProposalSupport:
    """Draw common support from a class-balanced numerical mixture.

    By default, each *distinct* null law receives total proposal mass
    ``0.5/J`` and each distinct alternative law receives ``0.5/K``.  An
    optional pilot-discovered focus allocation retains class-balanced base
    mass over every distinct law, then splits ``focus_mass`` equally between
    explicitly selected null and alternative laws.  Focus lists are
    deduplicated by observable-law identity, so repeated rows or indices have
    no effect.  If an identical observable law occurs on both sides, its two
    numerical masses are combined.  This is a proposal for importance
    integration, not a prior over either class.
    """

    if (
        null_family.block_names != alternative_family.block_names
        or null_family.block_sizes != alternative_family.block_sizes
        or null_family.observation_dimension != alternative_family.observation_dimension
    ):
        raise ValueError("null and alternative observable laws use different MID layouts")
    size = int(support_size)
    if size < 1:
        raise ValueError("common proposal support size must be positive")
    focused_mass = float(focus_mass)
    if not math.isfinite(focused_mass) or not 0.0 <= focused_mass < 1.0:
        raise ValueError("proposal focus mass must lie in [0,1)")

    null_unique: list[int] = []
    null_seen: set[tuple[object, ...]] = set()
    for index in range(null_family.member_count):
        key = _law_key(null_family, index)
        if key not in null_seen:
            null_seen.add(key)
            null_unique.append(index)
    alternative_unique: list[int] = []
    alternative_seen: set[tuple[object, ...]] = set()
    for index in range(alternative_family.member_count):
        key = _law_key(alternative_family, index)
        if key not in alternative_seen:
            alternative_seen.add(key)
            alternative_unique.append(index)

    def unique_focus_indices(
        family: ProductDirichletFamily,
        requested: Sequence[int] | None,
        *,
        side: str,
    ) -> list[int]:
        source: Sequence[int] = () if requested is None else requested
        indices = tuple(int(value) for value in source)
        if any(value < 0 or value >= family.member_count for value in indices):
            raise IndexError(f"{side} proposal focus index is out of range")
        result: list[int] = []
        seen: set[tuple[object, ...]] = set()
        for index in indices:
            key = _law_key(family, index)
            if key not in seen:
                seen.add(key)
                result.append(index)
        return result

    focused_null = unique_focus_indices(
        null_family, null_focus_indices, side="null"
    )
    focused_alternative = unique_focus_indices(
        alternative_family, alternative_focus_indices, side="alternative"
    )
    if focused_mass > 0.0 and (not focused_null or not focused_alternative):
        raise ValueError(
            "positive proposal focus mass requires explicit focus laws on both sides"
        )

    component_keys: list[tuple[object, ...]] = []
    component_parameters: list[np.ndarray] = []
    component_constants: list[float] = []
    component_weights: list[float] = []
    key_to_component: dict[tuple[object, ...], int] = {}

    def add_side(
        family: ProductDirichletFamily, indices: Sequence[int], side_mass: float
    ) -> None:
        per_member = side_mass / len(indices)
        for member_index in indices:
            key = _law_key(family, member_index)
            component_index = key_to_component.get(key)
            if component_index is None:
                component_index = len(component_keys)
                key_to_component[key] = component_index
                component_keys.append(key)
                component_parameters.append(
                    np.array(family.alpha_parameters[member_index], copy=True)
                )
                component_constants.append(
                    float(family.log_density_constants[member_index])
                )
                component_weights.append(0.0)
            component_weights[component_index] += per_member

    base_side_mass = 0.5 * (1.0 - focused_mass)
    add_side(null_family, null_unique, base_side_mass)
    add_side(alternative_family, alternative_unique, base_side_mass)
    if focused_mass > 0.0:
        add_side(null_family, focused_null, 0.5 * focused_mass)
        add_side(
            alternative_family,
            focused_alternative,
            0.5 * focused_mass,
        )
    parameters = np.asarray(component_parameters, dtype=float)
    constants = np.asarray(component_constants, dtype=float)
    weights = np.asarray(component_weights, dtype=float)
    weights /= np.sum(weights)

    seed_sequence = np.random.SeedSequence(int(seed))
    component_seed, observation_seed = seed_sequence.spawn(2)
    component_rng = np.random.default_rng(component_seed)
    observation_rng = np.random.default_rng(observation_seed)
    sampled_components = component_rng.choice(
        len(weights), size=size, replace=True, p=weights
    )
    observations = np.empty((size, null_family.observation_dimension), dtype=float)
    cursor = 0
    block_slices: list[slice] = []
    for block_size in null_family.block_sizes:
        block_slices.append(slice(cursor, cursor + block_size))
        cursor += block_size
    for component_index in range(len(weights)):
        rows = np.flatnonzero(sampled_components == component_index)
        if len(rows) == 0:
            continue
        for block in block_slices:
            observations[rows, block] = observation_rng.dirichlet(
                parameters[component_index, block], size=len(rows)
            )
    _validate_observations(observations, null_family.block_sizes, require_nonempty=True)

    log_proposal = np.empty(size, dtype=float)
    log_weights = np.log(weights)
    exponents = parameters - 1.0
    for start in range(0, size, int(density_chunk_size)):
        stop = min(start + int(density_chunk_size), size)
        member_log_density = (
            constants[:, np.newaxis]
            + exponents @ np.log(observations[start:stop]).T
        )
        log_proposal[start:stop] = logsumexp(
            log_weights[:, np.newaxis] + member_log_density, axis=0
        )
    if not np.all(np.isfinite(log_proposal)):
        raise MinimaxNumericalError("common proposal has a non-finite log density")
    return CommonProposalSupport(
        observations=observations,
        log_proposal_density=log_proposal,
        sampled_component_indices=sampled_components,
        proposal_component_weights=weights,
        unique_null_component_count=len(null_unique),
        unique_alternative_component_count=len(alternative_unique),
        focused_null_component_count=len(focused_null),
        focused_alternative_component_count=len(focused_alternative),
        focus_mass=focused_mass,
        proposal_component_count=len(weights),
        seed=int(seed),
    )


@dataclass(frozen=True)
class ImportanceDiscretization:
    """Row-stochastic finite laws obtained from common-proposal quadrature."""

    member_ids: tuple[str, ...]
    weights: np.ndarray
    raw_mass_estimates: np.ndarray
    log_raw_mass_estimates: np.ndarray
    effective_sample_sizes: np.ndarray

    def __post_init__(self) -> None:
        identifiers = tuple(str(value) for value in self.member_ids)
        weights = _readonly_float_array(self.weights)
        masses = _readonly_float_array(self.raw_mass_estimates)
        log_masses = _readonly_float_array(self.log_raw_mass_estimates)
        effective_sizes = _readonly_float_array(self.effective_sample_sizes)
        if weights.ndim != 2 or weights.shape[0] != len(identifiers):
            raise ValueError("importance rows and member identifiers do not align")
        expected = (len(identifiers),)
        if masses.shape != expected or log_masses.shape != expected or effective_sizes.shape != expected:
            raise ValueError("importance diagnostics have unexpected shape")
        if (
            not np.all(np.isfinite(weights))
            or np.any(weights < 0.0)
            or not np.allclose(
                np.sum(weights, axis=1), 1.0, rtol=0.0, atol=DEFAULT_ROW_SUM_TOLERANCE
            )
            or not np.all(np.isfinite(masses))
            or np.any(masses <= 0.0)
            or not np.all(np.isfinite(log_masses))
            or not np.all(np.isfinite(effective_sizes))
            or np.any(effective_sizes <= 0.0)
        ):
            raise ValueError("invalid importance discretization")
        object.__setattr__(self, "member_ids", identifiers)
        object.__setattr__(self, "weights", weights)
        object.__setattr__(self, "raw_mass_estimates", masses)
        object.__setattr__(self, "log_raw_mass_estimates", log_masses)
        object.__setattr__(self, "effective_sample_sizes", effective_sizes)

    @property
    def member_count(self) -> int:
        return len(self.member_ids)

    @property
    def support_size(self) -> int:
        return self.weights.shape[1]

    @property
    def maximum_absolute_raw_mass_error(self) -> float:
        return float(np.max(np.abs(self.raw_mass_estimates - 1.0)))

    @property
    def zero_weight_counts(self) -> np.ndarray:
        """Numerical underflow count per law (the exact densities are positive)."""

        result = np.count_nonzero(self.weights == 0.0, axis=1)
        return _readonly_int_array(result)

    @property
    def maximum_zero_weight_fraction(self) -> float:
        return float(np.max(self.zero_weight_counts) / self.support_size)

    @property
    def minimum_effective_sample_size(self) -> float:
        return float(np.min(self.effective_sample_sizes))


def importance_discretize(
    family: ProductDirichletFamily,
    support: CommonProposalSupport,
    *,
    density_chunk_size: int = 2048,
) -> ImportanceDiscretization:
    """Evaluate and self-normalize all laws on one common support.

    Before self-normalization, the diagnostic mass for member ``j`` is

    ``Z_j = (1/S) sum_s p_j(y_s) / r(y_s)``.

    Self-normalization makes the finite support rows genuine probability laws.
    The estimated ``Z_j`` values are retained because a continuous mixture
    representation must absorb them into its dual coefficients.
    """

    if family.observation_dimension != support.observation_dimension:
        raise ValueError("observable laws and proposal support dimensions differ")
    log_density = family.log_density(
        support.observations, chunk_size=int(density_chunk_size)
    )
    log_ratio = log_density - support.log_proposal_density[np.newaxis, :]
    log_ratio_sums = logsumexp(log_ratio, axis=1)
    log_masses = log_ratio_sums - math.log(support.support_size)
    masses = np.exp(log_masses)
    weights = np.exp(log_ratio - log_ratio_sums[:, np.newaxis])
    effective_sizes = 1.0 / np.sum(np.square(weights), axis=1)
    return ImportanceDiscretization(
        member_ids=family.member_ids,
        weights=weights,
        raw_mass_estimates=masses,
        log_raw_mass_estimates=log_masses,
        effective_sample_sizes=effective_sizes,
    )


def _validate_probability_rows(values: np.ndarray, name: str) -> np.ndarray:
    rows = np.asarray(values, dtype=float)
    if rows.ndim != 2 or min(rows.shape) < 1:
        raise ValueError(f"{name} must be a nonempty two-dimensional matrix")
    if not np.all(np.isfinite(rows)) or np.any(rows < 0.0):
        raise ValueError(f"{name} contains invalid probability weights")
    row_sums = np.sum(rows, axis=1)
    if not np.allclose(
        row_sums, 1.0, rtol=0.0, atol=DEFAULT_ROW_SUM_TOLERANCE
    ):
        raise ValueError(f"{name} rows must each sum to one")
    return rows


def _pruned_probability_csr(
    rows: np.ndarray,
    *,
    cutoff: float,
    maximum_pruned_row_mass: float,
    name: str,
) -> tuple[sparse.csr_matrix, np.ndarray]:
    """Build a row-normalised CSR matrix without materialising a dense copy."""

    threshold = float(cutoff)
    mass_tolerance = float(maximum_pruned_row_mass)
    if threshold < 0.0 or not math.isfinite(threshold):
        raise ValueError("LP probability-weight pruning cutoff is invalid")
    if mass_tolerance < 0.0 or not math.isfinite(mass_tolerance):
        raise ValueError("maximum pruned row mass is invalid")
    data_parts: list[np.ndarray] = []
    index_parts: list[np.ndarray] = []
    indptr = np.zeros(rows.shape[0] + 1, dtype=np.int64)
    removed_masses = np.empty(rows.shape[0], dtype=float)
    for row_index, row in enumerate(rows):
        keep = row > threshold if threshold > 0.0 else row > 0.0
        indices = np.flatnonzero(keep).astype(np.int32, copy=False)
        data = np.asarray(row[indices], dtype=float)
        retained_mass = float(np.sum(data))
        # Count only coefficients actually discarded.  Row-sum roundoff is a
        # different quantity and must not be labelled pruning mass.
        removed_mass = float(np.sum(row[~keep]))
        removed_masses[row_index] = removed_mass
        if retained_mass <= 0.0:
            raise MinimaxNumericalError(f"pruning removed all mass from {name} row")
        if removed_mass > mass_tolerance:
            raise MinimaxNumericalError(
                f"{name} row {row_index} pruning removed mass "
                f"{removed_mass:.6g} > {mass_tolerance:.6g}"
            )
        data_parts.append(data / retained_mass)
        index_parts.append(indices)
        indptr[row_index + 1] = indptr[row_index] + len(indices)
    data_values = np.concatenate(data_parts)
    column_indices = np.concatenate(index_parts)
    matrix = sparse.csr_matrix(
        (data_values, column_indices, indptr), shape=rows.shape
    )
    if not np.allclose(
        np.asarray(matrix.sum(axis=1)).ravel(),
        1.0,
        rtol=0.0,
        atol=2.0e-14,
    ):
        raise MinimaxNumericalError(f"pruned {name} rows were not renormalized")
    return matrix, removed_masses


@dataclass(frozen=True)
class FiniteMinimaxSolution:
    """Primal/dual diagnostics plus an original-dense-law certificate.

    ``dual_objective`` and ``absolute_duality_gap`` refer to the audited
    pruned-and-renormalised sparse LP actually solved.  ``null_errors`` and
    ``alternative_errors`` use the original dense rows.  The latter problem
    is certified separately by ``dense_dual_lower_bound`` and
    ``dense_feasible_type_ii_upper_bound``.
    """

    epsilon: float
    beta_objective: float
    decision_probabilities: np.ndarray
    solver_null_errors: np.ndarray
    solver_alternative_errors: np.ndarray
    null_errors: np.ndarray
    alternative_errors: np.ndarray
    null_dual_multipliers: np.ndarray
    alternative_dual_multipliers: np.ndarray
    dual_objective: float
    signed_duality_gap: float
    absolute_duality_gap: float
    active_null_indices: np.ndarray
    active_alternative_indices: np.ndarray
    dense_worst_null_indices: np.ndarray
    dense_worst_alternative_indices: np.ndarray
    dual_supported_null_indices: np.ndarray
    dual_supported_alternative_indices: np.ndarray
    fractional_support_indices: np.ndarray
    dual_tie_support_indices: np.ndarray
    maximum_primal_constraint_violation: float
    alternative_dual_sum_error: float
    objective_recomputation_error: float
    dense_objective_recomputation_error: float
    raw_dense_dual_lower_bound: float
    dense_dual_lower_bound: float
    dense_feasible_type_ii_upper_bound: float
    dense_certificate_gap: float
    dense_feasibility_rescaling_factor: float
    maximum_dense_constraint_violation: float
    probability_weight_pruning_cutoff: float
    maximum_pruned_null_row_mass: float
    maximum_pruned_alternative_row_mass: float
    retained_lp_coefficient_fraction: float
    lp_constraint_scale: float
    minimum_scaled_retained_coefficient: float
    solver_status: int
    solver_message: str

    @property
    def worst_case_type_i(self) -> float:
        return float(np.max(self.null_errors))

    @property
    def worst_case_type_ii(self) -> float:
        return float(np.max(self.alternative_errors))

    @property
    def null_dual_total(self) -> float:
        return float(np.sum(self.null_dual_multipliers))

    @property
    def null_dual_mixture_weights(self) -> np.ndarray | None:
        total = self.null_dual_total
        if total <= 1.0e-12:
            return None
        result = np.array(self.null_dual_multipliers / total, copy=True)
        result.setflags(write=False)
        return result

    @property
    def alternative_dual_mixture_weights(self) -> np.ndarray:
        total = float(np.sum(self.alternative_dual_multipliers))
        if total <= 0.0:
            raise MinimaxNumericalError("alternative dual mixture has zero mass")
        result = np.array(self.alternative_dual_multipliers / total, copy=True)
        result.setflags(write=False)
        return result


def solve_finite_minimax(
    null_probability_rows: np.ndarray,
    alternative_probability_rows: np.ndarray,
    *,
    epsilon: float = 0.05,
    active_tolerance: float = DEFAULT_LP_TOLERANCE,
    dual_support_tolerance: float = 1.0e-9,
    tie_relative_tolerance: float = 2.0e-7,
    probability_weight_pruning_cutoff: float = DEFAULT_LP_WEIGHT_PRUNING_CUTOFF,
    maximum_pruned_row_mass: float = DEFAULT_MAXIMUM_PRUNED_ROW_MASS,
    lp_constraint_scale: float = DEFAULT_LP_CONSTRAINT_SCALE,
    lp_objective_scale: float = 1.0,
) -> FiniteMinimaxSolution:
    """Solve the genuine finite-class minimax LP on an audited sparse matrix.

    With ``phi_s`` the probability of deciding the alternative at support
    point ``s``, the programme is

    ``min t`` subject to ``P_j phi <= epsilon`` for every null member,
    ``1 - Q_k phi <= t`` for every alternative member, and
    ``0 <= phi_s <= 1``.  The scalar ``t`` is left free; its probability
    bounds are implied by the other constraints.  Coefficients no larger than
    the configured pruning cutoff are removed and each sparse law row is
    renormalised; the removed mass is bounded explicitly.  The returned exact
    solver gap is for those sparse rows, while a separate lower/upper bracket
    evaluates the unpruned dense rows.  Every complete inequality and its
    right-hand side are additionally multiplied by the same positive scale so
    HiGHS cannot silently discard retained small coefficients; this row
    scaling leaves the feasible set and objective unchanged, and returned
    inequality marginals are converted back to unscaled dual multipliers.
    """

    null_rows = _validate_probability_rows(null_probability_rows, "null laws")
    alternative_rows = _validate_probability_rows(
        alternative_probability_rows, "alternative laws"
    )
    if null_rows.shape[1] != alternative_rows.shape[1]:
        raise ValueError("null and alternative laws use different observation supports")
    level = float(epsilon)
    if not math.isfinite(level) or not 0.0 < level < 1.0:
        raise ValueError("Type-I level epsilon must lie strictly between zero and one")
    constraint_scale = float(lp_constraint_scale)
    if not math.isfinite(constraint_scale) or constraint_scale <= 0.0:
        raise ValueError("LP constraint scale must be positive and finite")
    objective_scale = float(lp_objective_scale)
    if not math.isfinite(objective_scale) or objective_scale <= 0.0:
        raise ValueError("LP objective scale must be positive and finite")
    support_size = null_rows.shape[1]
    null_count = null_rows.shape[0]
    alternative_count = alternative_rows.shape[0]

    objective = np.zeros(support_size + 1, dtype=float)
    # A positive objective scaling leaves the optimizer and beta variable
    # unchanged.  It is useful when a scientifically meaningful beta is far
    # below the solver's unscaled objective resolution.
    objective[-1] = objective_scale
    sparse_null, pruned_null_mass = _pruned_probability_csr(
        null_rows,
        cutoff=float(probability_weight_pruning_cutoff),
        maximum_pruned_row_mass=float(maximum_pruned_row_mass),
        name="null law",
    )
    sparse_alternative, pruned_alternative_mass = _pruned_probability_csr(
        alternative_rows,
        cutoff=float(probability_weight_pruning_cutoff),
        maximum_pruned_row_mass=float(maximum_pruned_row_mass),
        name="alternative law",
    )
    minimum_scaled_retained = constraint_scale * float(
        min(np.min(sparse_null.data), np.min(sparse_alternative.data))
    )
    if minimum_scaled_retained <= HIGHS_SMALL_MATRIX_VALUE:
        raise MinimaxNumericalError(
            "LP row scaling does not lift every retained probability "
            "coefficient above HiGHS' small-matrix threshold: "
            f"minimum_scaled={minimum_scaled_retained:.12g}, "
            f"threshold={HIGHS_SMALL_MATRIX_VALUE:.12g}"
        )
    null_scalar_column = sparse.csr_matrix((null_count, 1), dtype=float)
    alternative_scalar_column = sparse.csr_matrix(
        (
            -constraint_scale * np.ones(alternative_count, dtype=float),
            (np.arange(alternative_count, dtype=int), np.zeros(alternative_count, dtype=int)),
        ),
        shape=(alternative_count, 1),
    )
    constraint_matrix = sparse.vstack(
        (
            sparse.hstack(
                (constraint_scale * sparse_null, null_scalar_column), format="csr"
            ),
            sparse.hstack(
                (
                    -constraint_scale * sparse_alternative,
                    alternative_scalar_column,
                ),
                format="csr",
            ),
        ),
        format="csr",
    )
    possible_probability_coefficients = (
        null_count + alternative_count
    ) * support_size
    retained_fraction = float(
        (sparse_null.nnz + sparse_alternative.nnz)
        / possible_probability_coefficients
    )
    right_hand_side = np.concatenate(
        (
            np.full(null_count, level * constraint_scale, dtype=float),
            -constraint_scale * np.ones(alternative_count, dtype=float),
        )
    )
    bounds = [(0.0, 1.0)] * support_size + [(None, None)]
    result = linprog(
        objective,
        A_ub=constraint_matrix,
        b_ub=right_hand_side,
        bounds=bounds,
        method="highs",
        options={
            "primal_feasibility_tolerance": 1.0e-10,
            "dual_feasibility_tolerance": 1.0e-10,
        },
    )
    if not result.success or result.x is None:
        raise MinimaxNumericalError(
            f"finite minimax LP failed (status {result.status}): {result.message}"
        )
    decision = np.asarray(result.x[:support_size], dtype=float)
    if np.min(decision) < -1.0e-8 or np.max(decision) > 1.0 + 1.0e-8:
        raise MinimaxNumericalError("LP returned a test outside [0,1]")
    decision = np.clip(decision, 0.0, 1.0)
    beta = float(result.x[-1])
    # These are the exact rows passed to HiGHS after audited pruning and
    # renormalisation.
    solver_null_errors = np.asarray(sparse_null @ decision, dtype=float)
    solver_alternative_errors = np.asarray(
        sparse_alternative @ (1.0 - decision), dtype=float
    )
    # These retain the original, unpruned finite observation laws and are the
    # scientifically reported member errors.
    null_errors = null_rows @ decision
    # Compute misses directly.  ``1-Q@phi`` catastrophically cancels for the
    # easy, nearly perfectly separated benchmark.
    alternative_errors = alternative_rows @ (1.0 - decision)

    marginals = np.asarray(result.ineqlin.marginals, dtype=float)
    if marginals.shape != (null_count + alternative_count,):
        raise MinimaxNumericalError("LP solver did not return inequality duals")
    if float(np.max(marginals)) > 2.0e-8:
        raise MinimaxNumericalError("LP inequality dual orientation is inconsistent")
    # Each HiGHS constraint is ``constraint_scale`` times the mathematical
    # sparse constraint, so convert its marginal back to the unscaled
    # Lagrange multiplier before reconstructing the dual.
    multipliers = (
        constraint_scale
        * np.maximum(-marginals, 0.0)
        / objective_scale
    )
    null_dual = multipliers[:null_count]
    alternative_dual = multipliers[null_count:]
    alternative_sum_error = abs(float(np.sum(alternative_dual)) - 1.0)
    objective_recomputation_error = abs(
        beta - float(np.max(solver_alternative_errors))
    )
    dense_objective_recomputation_error = abs(
        beta - float(np.max(alternative_errors))
    )

    # Exact dual reconstruction for the one sparse LP solved by HiGHS.
    solver_alternative_mix = np.asarray(
        sparse_alternative.T @ alternative_dual, dtype=float
    ).ravel()
    solver_null_weighted = np.asarray(
        sparse_null.T @ null_dual, dtype=float
    ).ravel()
    dual_advantage = solver_alternative_mix - solver_null_weighted
    dual_objective = float(
        1.0
        - level * np.sum(null_dual)
        - np.sum(np.maximum(dual_advantage, 0.0))
    )
    signed_gap = beta - dual_objective
    absolute_gap = abs(signed_gap)
    null_slack = level - solver_null_errors
    alternative_slack = beta - solver_alternative_errors
    maximum_violation = max(
        0.0,
        float(np.max(-null_slack)),
        float(np.max(-alternative_slack)),
    )
    node_scale = np.maximum.reduce(
        (
            np.abs(solver_alternative_mix),
            np.abs(solver_null_weighted),
            np.full(support_size, 1.0 / support_size),
        )
    )
    tie_mask = np.abs(dual_advantage) <= float(tie_relative_tolerance) * node_scale
    fractional_mask = (decision > float(active_tolerance)) & (
        decision < 1.0 - float(active_tolerance)
    )

    # The sparse-LP multipliers remain dual-feasible for the original dense
    # finite LP.  Their dense objective is therefore a valid lower bound, not
    # the exact solver dual objective above.
    dense_alternative_mix = alternative_dual @ alternative_rows
    dense_null_weighted = null_dual @ null_rows
    raw_dense_dual_lower_bound = float(
        1.0
        - level * np.sum(null_dual)
        - np.sum(
            np.maximum(dense_alternative_mix - dense_null_weighted, 0.0)
        )
    )
    maximum_dense_violation = max(
        0.0,
        float(np.max(null_errors) - level),
        float(np.max(alternative_errors) - beta),
    )
    maximum_dense_null_error = float(np.max(null_errors))
    dense_rescaling = (
        1.0
        if maximum_dense_null_error <= level
        else level / maximum_dense_null_error
    )
    dense_feasible_decision = dense_rescaling * decision
    dense_feasible_null_error = float(
        np.max(null_rows @ dense_feasible_decision)
    )
    if dense_feasible_null_error > level:
        # Protect the last floating-point ulp: the upper-bound test reported
        # below must genuinely satisfy every original dense null row.
        dense_rescaling *= level / dense_feasible_null_error
        dense_feasible_decision = dense_rescaling * decision
    dense_upper_bound = float(
        np.max(alternative_rows @ (1.0 - dense_feasible_decision))
    )
    dense_bound_ordering_error = raw_dense_dual_lower_bound - dense_upper_bound
    if dense_bound_ordering_error > 2.0e-7:
        raise MinimaxNumericalError(
            "original dense lower bound exceeds its feasible upper bound: "
            f"lower={raw_dense_dual_lower_bound:.12g}, "
            f"upper={dense_upper_bound:.12g}"
        )
    # Roundoff can put a mathematically zero lower bound one ulp above a zero
    # feasible upper bound.  Preserve the raw calculation, but report an
    # ordered certificate bracket after an audited tolerance check.
    dense_dual_lower_bound = min(
        raw_dense_dual_lower_bound, dense_upper_bound
    )
    dense_certificate_gap = dense_upper_bound - dense_dual_lower_bound
    if (
        absolute_gap > 2.0e-7
        or maximum_violation > 2.0e-7
        or alternative_sum_error > 2.0e-7
    ):
        raise MinimaxNumericalError(
            "finite minimax LP failed primal/dual validation: "
            f"gap={signed_gap:.6g}, violation={maximum_violation:.6g}, "
            f"sum_alternative_dual_error={alternative_sum_error:.6g}"
        )
    return FiniteMinimaxSolution(
        epsilon=level,
        beta_objective=beta,
        decision_probabilities=_readonly_float_array(decision),
        solver_null_errors=_readonly_float_array(solver_null_errors),
        solver_alternative_errors=_readonly_float_array(
            solver_alternative_errors
        ),
        null_errors=_readonly_float_array(null_errors),
        alternative_errors=_readonly_float_array(alternative_errors),
        null_dual_multipliers=_readonly_float_array(null_dual),
        alternative_dual_multipliers=_readonly_float_array(alternative_dual),
        dual_objective=dual_objective,
        signed_duality_gap=signed_gap,
        absolute_duality_gap=absolute_gap,
        active_null_indices=_readonly_int_array(
            np.flatnonzero(null_slack <= float(active_tolerance))
        ),
        active_alternative_indices=_readonly_int_array(
            np.flatnonzero(alternative_slack <= float(active_tolerance))
        ),
        dense_worst_null_indices=_readonly_int_array(
            np.flatnonzero(
                np.max(null_errors) - null_errors <= float(active_tolerance)
            )
        ),
        dense_worst_alternative_indices=_readonly_int_array(
            np.flatnonzero(
                np.max(alternative_errors) - alternative_errors
                <= float(active_tolerance)
            )
        ),
        dual_supported_null_indices=_readonly_int_array(
            np.flatnonzero(null_dual > float(dual_support_tolerance))
        ),
        dual_supported_alternative_indices=_readonly_int_array(
            np.flatnonzero(alternative_dual > float(dual_support_tolerance))
        ),
        fractional_support_indices=_readonly_int_array(np.flatnonzero(fractional_mask)),
        dual_tie_support_indices=_readonly_int_array(np.flatnonzero(tie_mask)),
        maximum_primal_constraint_violation=maximum_violation,
        alternative_dual_sum_error=alternative_sum_error,
        objective_recomputation_error=objective_recomputation_error,
        dense_objective_recomputation_error=(
            dense_objective_recomputation_error
        ),
        raw_dense_dual_lower_bound=raw_dense_dual_lower_bound,
        dense_dual_lower_bound=dense_dual_lower_bound,
        dense_feasible_type_ii_upper_bound=dense_upper_bound,
        dense_certificate_gap=dense_certificate_gap,
        dense_feasibility_rescaling_factor=dense_rescaling,
        maximum_dense_constraint_violation=maximum_dense_violation,
        probability_weight_pruning_cutoff=float(probability_weight_pruning_cutoff),
        maximum_pruned_null_row_mass=float(np.max(pruned_null_mass)),
        maximum_pruned_alternative_row_mass=float(
            np.max(pruned_alternative_mass)
        ),
        retained_lp_coefficient_fraction=retained_fraction,
        lp_constraint_scale=constraint_scale,
        minimum_scaled_retained_coefficient=minimum_scaled_retained,
        solver_status=int(result.status),
        solver_message=str(result.message),
    )


def solve_identical_class_minimax_exact(
    null_probability_rows: np.ndarray,
    alternative_probability_rows: np.ndarray,
    *,
    epsilon: float = 0.05,
    active_tolerance: float = DEFAULT_LP_TOLERANCE,
) -> FiniteMinimaxSolution:
    """Return the theorem-backed finite solution for identical law classes.

    This helper first verifies equality of the *sets of individual probability
    rows*.  Row order and duplicate frequency are immaterial, but equality of
    class averages is insufficient.  It then uses the constant randomized
    test ``phi_s = epsilon``.  Every null constraint equals ``epsilon`` and
    every alternative miss equals ``1-epsilon``.  Giving dual mass one to any
    explicitly matched null/alternative row produces identical dual measures,
    zero node advantage, and dual objective ``1-epsilon``.  Thus the primal
    and dual certificates agree without invoking a numerical optimizer.
    """

    null_dense = _validate_probability_rows(
        null_probability_rows, "identical-class null laws"
    )
    alternative_dense = _validate_probability_rows(
        alternative_probability_rows, "identical-class alternative laws"
    )
    if null_dense.shape[1] != alternative_dense.shape[1]:
        raise ValueError("identical classes use different observation supports")
    level = float(epsilon)
    if not math.isfinite(level) or not 0.0 < level < 1.0:
        raise ValueError("Type-I level epsilon must lie strictly between zero and one")

    # Treat each already validated numerical probability row as a stochastic
    # law.  Renormalisation only removes row-sum roundoff and is applied
    # separately—not an average—member by member.
    null_rows = null_dense / np.sum(null_dense, axis=1, keepdims=True)
    alternative_rows = alternative_dense / np.sum(
        alternative_dense, axis=1, keepdims=True
    )

    def row_keys(rows: np.ndarray) -> tuple[tuple[bytes, ...], dict[bytes, int]]:
        keys = tuple(
            np.ascontiguousarray(row, dtype=float).tobytes() for row in rows
        )
        first_indices: dict[bytes, int] = {}
        for index, key in enumerate(keys):
            first_indices.setdefault(key, index)
        return keys, first_indices

    # Keep the key construction local and exact: C0's independently built
    # null and alternative rows are expected to be bit-identical.  Silently
    # accepting merely close classes would weaken the impossibility control.
    null_keys, null_first = row_keys(null_dense)
    alternative_keys, alternative_first = row_keys(alternative_dense)
    if set(null_keys) != set(alternative_keys):
        raise ValueError(
            "observable law row sets are not exactly identical; "
            "the identical-class theorem does not apply"
        )
    matched_key = null_keys[0]
    matched_null = null_first[matched_key]
    matched_alternative = alternative_first[matched_key]

    support_size = null_rows.shape[1]
    decision = np.full(support_size, level, dtype=float)
    beta = 1.0 - level
    solver_null_errors = null_rows @ decision
    solver_alternative_errors = alternative_rows @ (1.0 - decision)
    null_errors = null_dense @ decision
    alternative_errors = alternative_dense @ (1.0 - decision)
    null_dual = np.zeros(len(null_rows), dtype=float)
    alternative_dual = np.zeros(len(alternative_rows), dtype=float)
    null_dual[matched_null] = 1.0
    alternative_dual[matched_alternative] = 1.0
    solver_advantage = (
        alternative_dual @ alternative_rows - null_dual @ null_rows
    )
    dual_objective = float(
        1.0
        - level * np.sum(null_dual)
        - np.sum(np.maximum(solver_advantage, 0.0))
    )
    signed_gap = beta - dual_objective
    solver_null_slack = level - solver_null_errors
    solver_alternative_slack = beta - solver_alternative_errors
    maximum_solver_violation = max(
        0.0,
        float(np.max(-solver_null_slack)),
        float(np.max(-solver_alternative_slack)),
    )

    dense_advantage = (
        alternative_dual @ alternative_dense - null_dual @ null_dense
    )
    raw_dense_lower = float(
        1.0
        - level * np.sum(null_dual)
        - np.sum(np.maximum(dense_advantage, 0.0))
    )
    maximum_dense_null_error = float(np.max(null_errors))
    dense_rescaling = (
        1.0
        if maximum_dense_null_error <= level
        else level / maximum_dense_null_error
    )
    dense_feasible_decision = dense_rescaling * decision
    dense_feasible_null_error = float(
        np.max(null_dense @ dense_feasible_decision)
    )
    if dense_feasible_null_error > level:
        dense_rescaling *= level / dense_feasible_null_error
        dense_feasible_decision = dense_rescaling * decision
    dense_upper = float(
        np.max(alternative_dense @ (1.0 - dense_feasible_decision))
    )
    if raw_dense_lower - dense_upper > 2.0e-7:
        raise MinimaxNumericalError(
            "identical-class dense certificate ordering failed"
        )
    dense_lower = min(raw_dense_lower, dense_upper)
    maximum_dense_violation = max(
        0.0,
        float(np.max(null_errors) - level),
        float(np.max(alternative_errors) - beta),
    )
    positive_coefficients = np.concatenate(
        (null_rows[null_rows > 0.0], alternative_rows[alternative_rows > 0.0])
    )
    return FiniteMinimaxSolution(
        epsilon=level,
        beta_objective=beta,
        decision_probabilities=_readonly_float_array(decision),
        solver_null_errors=_readonly_float_array(solver_null_errors),
        solver_alternative_errors=_readonly_float_array(
            solver_alternative_errors
        ),
        null_errors=_readonly_float_array(null_errors),
        alternative_errors=_readonly_float_array(alternative_errors),
        null_dual_multipliers=_readonly_float_array(null_dual),
        alternative_dual_multipliers=_readonly_float_array(alternative_dual),
        dual_objective=dual_objective,
        signed_duality_gap=signed_gap,
        absolute_duality_gap=abs(signed_gap),
        active_null_indices=_readonly_int_array(
            np.flatnonzero(solver_null_slack <= float(active_tolerance))
        ),
        active_alternative_indices=_readonly_int_array(
            np.flatnonzero(
                solver_alternative_slack <= float(active_tolerance)
            )
        ),
        dense_worst_null_indices=_readonly_int_array(
            np.flatnonzero(
                np.max(null_errors) - null_errors <= float(active_tolerance)
            )
        ),
        dense_worst_alternative_indices=_readonly_int_array(
            np.flatnonzero(
                np.max(alternative_errors) - alternative_errors
                <= float(active_tolerance)
            )
        ),
        dual_supported_null_indices=_readonly_int_array([matched_null]),
        dual_supported_alternative_indices=_readonly_int_array(
            [matched_alternative]
        ),
        fractional_support_indices=_readonly_int_array(
            np.arange(support_size, dtype=int)
        ),
        dual_tie_support_indices=_readonly_int_array(
            np.arange(support_size, dtype=int)
        ),
        maximum_primal_constraint_violation=maximum_solver_violation,
        alternative_dual_sum_error=0.0,
        objective_recomputation_error=abs(
            beta - float(np.max(solver_alternative_errors))
        ),
        dense_objective_recomputation_error=abs(
            beta - float(np.max(alternative_errors))
        ),
        raw_dense_dual_lower_bound=raw_dense_lower,
        dense_dual_lower_bound=dense_lower,
        dense_feasible_type_ii_upper_bound=dense_upper,
        dense_certificate_gap=dense_upper - dense_lower,
        dense_feasibility_rescaling_factor=dense_rescaling,
        maximum_dense_constraint_violation=maximum_dense_violation,
        probability_weight_pruning_cutoff=0.0,
        maximum_pruned_null_row_mass=0.0,
        maximum_pruned_alternative_row_mass=0.0,
        retained_lp_coefficient_fraction=1.0,
        lp_constraint_scale=1.0,
        minimum_scaled_retained_coefficient=float(
            np.min(positive_coefficients)
        ),
        solver_status=0,
        solver_message=(
            "exact identical-class primal/dual theorem; numerical optimizer "
            "not invoked"
        ),
    )


def solve_finite_disjoint_support_minimax_exact(
    null_probability_rows: np.ndarray,
    alternative_probability_rows: np.ndarray,
    *,
    epsilon: float = 0.05,
    active_tolerance: float = DEFAULT_LP_TOLERANCE,
) -> FiniteMinimaxSolution:
    """Return an exact certificate for numerically disjoint finite supports.

    This theorem applies only to the supplied floating-point observation-space
    discretisation.  It does **not** assert disjoint support for the underlying
    continuous Dirichlet laws: cross-density importance weights may simply
    have underflowed to zero.  The helper therefore requires the unions of
    strictly positive null and alternative coefficients to be exactly
    disjoint and rejects even one positive overlapping node.

    On a validated disjoint support, choose ``phi=0`` on the null union and
    ``phi=1`` on the alternative union.  Then every finite null false-positive
    error and alternative miss is zero.  A unit alternative multiplier on any
    one alternative member, with all null multipliers zero, gives dual
    objective zero because that probability row has total mass one.
    """

    null_rows = _validate_probability_rows(
        null_probability_rows, "finite-disjoint null laws"
    )
    alternative_rows = _validate_probability_rows(
        alternative_probability_rows, "finite-disjoint alternative laws"
    )
    if null_rows.shape[1] != alternative_rows.shape[1]:
        raise ValueError("finite-disjoint classes use different observation supports")
    level = float(epsilon)
    if not math.isfinite(level) or not 0.0 < level < 1.0:
        raise ValueError("Type-I level epsilon must lie strictly between zero and one")
    null_union = np.any(null_rows > 0.0, axis=0)
    alternative_union = np.any(alternative_rows > 0.0, axis=0)
    overlap = np.flatnonzero(null_union & alternative_union)
    if len(overlap):
        raise ValueError(
            "finite null/alternative positive-support unions overlap; "
            "the disjoint-support theorem does not apply"
        )

    support_size = null_rows.shape[1]
    decision = np.zeros(support_size, dtype=float)
    decision[alternative_union] = 1.0
    null_errors = null_rows @ decision
    alternative_errors = alternative_rows @ (1.0 - decision)
    if np.any(null_errors != 0.0) or np.any(alternative_errors != 0.0):
        raise MinimaxNumericalError(
            "validated finite support did not produce zero class-member errors"
        )
    beta = 0.0
    null_dual = np.zeros(len(null_rows), dtype=float)
    alternative_dual = np.zeros(len(alternative_rows), dtype=float)
    alternative_dual[0] = 1.0
    dual_advantage = alternative_rows[0]
    # Mathematically this is exactly zero for a row-stochastic probability
    # law.  Preserve the raw floating-point evaluation separately below.
    dual_objective = 0.0
    raw_dense_lower = float(
        1.0 - np.sum(np.maximum(dual_advantage, 0.0))
    )
    dense_upper = 0.0
    if raw_dense_lower - dense_upper > 2.0e-7:
        raise MinimaxNumericalError(
            "finite-disjoint dense certificate ordering failed"
        )
    dense_lower = min(raw_dense_lower, dense_upper)
    positive_coefficients = np.concatenate(
        (
            null_rows[null_rows > 0.0],
            alternative_rows[alternative_rows > 0.0],
        )
    )
    all_null = np.arange(len(null_rows), dtype=int)
    all_alternative = np.arange(len(alternative_rows), dtype=int)
    return FiniteMinimaxSolution(
        epsilon=level,
        beta_objective=beta,
        decision_probabilities=_readonly_float_array(decision),
        solver_null_errors=_readonly_float_array(null_errors),
        solver_alternative_errors=_readonly_float_array(alternative_errors),
        null_errors=_readonly_float_array(null_errors),
        alternative_errors=_readonly_float_array(alternative_errors),
        null_dual_multipliers=_readonly_float_array(null_dual),
        alternative_dual_multipliers=_readonly_float_array(alternative_dual),
        dual_objective=dual_objective,
        signed_duality_gap=0.0,
        absolute_duality_gap=0.0,
        active_null_indices=_readonly_int_array([]),
        active_alternative_indices=_readonly_int_array(all_alternative),
        dense_worst_null_indices=_readonly_int_array(all_null),
        dense_worst_alternative_indices=_readonly_int_array(all_alternative),
        dual_supported_null_indices=_readonly_int_array([]),
        dual_supported_alternative_indices=_readonly_int_array([0]),
        fractional_support_indices=_readonly_int_array([]),
        dual_tie_support_indices=_readonly_int_array(
            np.flatnonzero(dual_advantage == 0.0)
        ),
        maximum_primal_constraint_violation=0.0,
        alternative_dual_sum_error=0.0,
        objective_recomputation_error=0.0,
        dense_objective_recomputation_error=0.0,
        raw_dense_dual_lower_bound=raw_dense_lower,
        dense_dual_lower_bound=dense_lower,
        dense_feasible_type_ii_upper_bound=dense_upper,
        dense_certificate_gap=dense_upper - dense_lower,
        dense_feasibility_rescaling_factor=1.0,
        maximum_dense_constraint_violation=0.0,
        probability_weight_pruning_cutoff=0.0,
        maximum_pruned_null_row_mass=0.0,
        maximum_pruned_alternative_row_mass=0.0,
        retained_lp_coefficient_fraction=1.0,
        lp_constraint_scale=1.0,
        minimum_scaled_retained_coefficient=float(
            np.min(positive_coefficients)
        ),
        solver_status=0,
        solver_message=(
            "exact finite disjoint-support primal/dual theorem; numerical "
            "optimizer not invoked; finite-support-only under floating-point "
            "observation discretisation"
        ),
    )


@dataclass(frozen=True)
class ConstraintGenerationIteration:
    iteration: int
    beta_objective: float
    active_null_count: int
    active_alternative_count: int
    validation_worst_type_i: float
    validation_worst_type_ii: float
    added_null_validation_index: int | None
    added_alternative_validation_index: int | None


@dataclass(frozen=True)
class ConstraintGenerationResult:
    solution: FiniteMinimaxSolution
    selected_null_validation_indices: np.ndarray
    selected_alternative_validation_indices: np.ndarray
    validation_null_errors: np.ndarray
    validation_alternative_errors: np.ndarray
    iterations: tuple[ConstraintGenerationIteration, ...]
    converged: bool
    violation_tolerance: float


def _row_already_present(row: np.ndarray, active_rows: np.ndarray) -> bool:
    return bool(
        np.any(np.max(np.abs(active_rows - row[np.newaxis, :]), axis=1) <= 2.0e-14)
    )


def run_constraint_generation(
    initial_null_rows: np.ndarray,
    initial_alternative_rows: np.ndarray,
    validation_null_rows: np.ndarray,
    validation_alternative_rows: np.ndarray,
    *,
    epsilon: float = 0.05,
    violation_tolerance: float = 2.0e-5,
    near_worst_tolerance: float = 5.0e-6,
    max_iterations: int = 30,
) -> ConstraintGenerationResult:
    """Add dense-grid constraints until validation worst cases stabilize."""

    initial_null = _validate_probability_rows(initial_null_rows, "initial null laws")
    initial_alternative = _validate_probability_rows(
        initial_alternative_rows, "initial alternative laws"
    )
    validation_null = _validate_probability_rows(
        validation_null_rows, "validation null laws"
    )
    validation_alternative = _validate_probability_rows(
        validation_alternative_rows, "validation alternative laws"
    )
    support_sizes = {
        initial_null.shape[1],
        initial_alternative.shape[1],
        validation_null.shape[1],
        validation_alternative.shape[1],
    }
    if len(support_sizes) != 1:
        raise ValueError("all generated constraints must use the same support")
    if int(max_iterations) < 1:
        raise ValueError("constraint generation needs at least one iteration")
    tolerance = float(violation_tolerance)
    near_tolerance = float(near_worst_tolerance)
    if tolerance <= 0.0 or near_tolerance < 0.0:
        raise ValueError("constraint-generation tolerances are invalid")

    active_null = np.array(initial_null, copy=True)
    active_alternative = np.array(initial_alternative, copy=True)
    selected_null: list[int] = []
    selected_alternative: list[int] = []
    records: list[ConstraintGenerationIteration] = []
    converged = False
    solution: FiniteMinimaxSolution | None = None
    validation_null_errors = np.empty(len(validation_null), dtype=float)
    validation_alternative_errors = np.empty(len(validation_alternative), dtype=float)

    for iteration in range(int(max_iterations)):
        solution = solve_finite_minimax(
            active_null, active_alternative, epsilon=float(epsilon)
        )
        decision = solution.decision_probabilities
        validation_null_errors = validation_null @ decision
        validation_alternative_errors = validation_alternative @ (1.0 - decision)
        worst_null_index = int(np.argmax(validation_null_errors))
        worst_alternative_index = int(np.argmax(validation_alternative_errors))
        worst_null = float(validation_null_errors[worst_null_index])
        worst_alternative = float(
            validation_alternative_errors[worst_alternative_index]
        )
        add_null: int | None = None
        add_alternative: int | None = None
        null_is_new = (
            worst_null_index not in selected_null
            and not _row_already_present(
                validation_null[worst_null_index], active_null
            )
        )
        alternative_is_new = (
            worst_alternative_index not in selected_alternative
            and not _row_already_present(
                validation_alternative[worst_alternative_index], active_alternative
            )
        )
        if null_is_new and (
            worst_null > float(epsilon) + tolerance
            or (
                near_tolerance > 0.0
                and abs(worst_null - float(epsilon)) <= near_tolerance
            )
        ):
            add_null = worst_null_index
        if alternative_is_new and (
            worst_alternative > solution.beta_objective + tolerance
            or (
                near_tolerance > 0.0
                and abs(worst_alternative - solution.beta_objective)
                <= near_tolerance
            )
        ):
            add_alternative = worst_alternative_index
        records.append(
            ConstraintGenerationIteration(
                iteration=iteration,
                beta_objective=solution.beta_objective,
                active_null_count=len(active_null),
                active_alternative_count=len(active_alternative),
                validation_worst_type_i=worst_null,
                validation_worst_type_ii=worst_alternative,
                added_null_validation_index=add_null,
                added_alternative_validation_index=add_alternative,
            )
        )
        if add_null is None and add_alternative is None:
            converged = bool(
                worst_null <= float(epsilon) + tolerance
                and worst_alternative <= solution.beta_objective + tolerance
            )
            break
        if add_null is not None:
            selected_null.append(add_null)
            active_null = np.vstack((active_null, validation_null[add_null]))
        if add_alternative is not None:
            selected_alternative.append(add_alternative)
            active_alternative = np.vstack(
                (active_alternative, validation_alternative[add_alternative])
            )

    if solution is None:  # pragma: no cover - guarded by max_iterations
        raise RuntimeError("constraint generation did not execute")
    if not converged:
        # Recompute against the final active set if the last iteration added a
        # constraint.  The explicit false result lets the caller enact a STOP
        # condition instead of silently treating an incomplete loop as stable.
        solution = solve_finite_minimax(
            active_null, active_alternative, epsilon=float(epsilon)
        )
        validation_null_errors = validation_null @ solution.decision_probabilities
        validation_alternative_errors = validation_alternative @ (
            1.0 - solution.decision_probabilities
        )
        converged = bool(
            float(np.max(validation_null_errors)) <= float(epsilon) + tolerance
            and float(np.max(validation_alternative_errors))
            <= solution.beta_objective + tolerance
        )
    return ConstraintGenerationResult(
        solution=solution,
        selected_null_validation_indices=_readonly_int_array(selected_null),
        selected_alternative_validation_indices=_readonly_int_array(
            selected_alternative
        ),
        validation_null_errors=_readonly_float_array(validation_null_errors),
        validation_alternative_errors=_readonly_float_array(
            validation_alternative_errors
        ),
        iterations=tuple(records),
        converged=converged,
        violation_tolerance=tolerance,
    )


@dataclass(frozen=True)
class ContinuousMixtureTest:
    """Deployable MID-only likelihood rule derived from finite-LP duals."""

    null_family: ProductDirichletFamily
    alternative_family: ProductDirichletFamily
    null_mixture_weights: np.ndarray
    alternative_mixture_weights: np.ndarray
    log_likelihood_threshold: float
    tie_probability: float
    tie_log_tolerance: float = 2.0e-10

    def __post_init__(self) -> None:
        null_weights = _readonly_float_array(self.null_mixture_weights)
        alternative_weights = _readonly_float_array(self.alternative_mixture_weights)
        if null_weights.shape != (self.null_family.member_count,):
            raise ValueError("null continuous-mixture weights have unexpected shape")
        if alternative_weights.shape != (self.alternative_family.member_count,):
            raise ValueError("alternative continuous-mixture weights have unexpected shape")
        for values, name in (
            (null_weights, "null"),
            (alternative_weights, "alternative"),
        ):
            if np.any(values < 0.0) or not math.isclose(
                float(np.sum(values)), 1.0, rel_tol=0.0, abs_tol=2.0e-10
            ):
                raise ValueError(f"{name} continuous-mixture weights are invalid")
        if not math.isfinite(float(self.log_likelihood_threshold)):
            raise ValueError("continuous likelihood threshold must be finite")
        if not 0.0 <= float(self.tie_probability) <= 1.0:
            raise ValueError("tie randomization probability must lie in [0,1]")
        object.__setattr__(self, "null_mixture_weights", null_weights)
        object.__setattr__(self, "alternative_mixture_weights", alternative_weights)

    @staticmethod
    def _mixture_log_density(
        family: ProductDirichletFamily,
        weights: np.ndarray,
        observations: np.ndarray,
    ) -> np.ndarray:
        positive = weights > 0.0
        positive_indices = np.flatnonzero(positive)
        # Dual mixtures are commonly supported on one or two class members.
        # Select first so held-out evaluation never materialises a dense
        # member-by-observation matrix for zero-weight laws.
        supported_family = family.select(positive_indices)
        member_log_density = supported_family.log_density(observations)
        return logsumexp(
            np.log(weights[positive])[:, np.newaxis] + member_log_density, axis=0
        )

    def log_score(self, observations: np.ndarray) -> np.ndarray:
        """Return alternative-minus-null mixture log density from MIDs only."""

        values = _validate_observations(
            observations, self.null_family.block_sizes, require_nonempty=True
        )
        return self._mixture_log_density(
            self.alternative_family,
            self.alternative_mixture_weights,
            values,
        ) - self._mixture_log_density(
            self.null_family,
            self.null_mixture_weights,
            values,
        )

    def decision_probability(self, observations: np.ndarray) -> np.ndarray:
        """Return ``phi(y)``, the probability of deciding the alternative."""

        centred_score = self.log_score(observations) - float(
            self.log_likelihood_threshold
        )
        probabilities = np.empty(len(centred_score), dtype=float)
        probabilities[centred_score > float(self.tie_log_tolerance)] = 1.0
        probabilities[centred_score < -float(self.tie_log_tolerance)] = 0.0
        tie = np.abs(centred_score) <= float(self.tie_log_tolerance)
        probabilities[tie] = float(self.tie_probability)
        return probabilities


@dataclass(frozen=True)
class ContinuousRepresentationDiagnostics:
    test: ContinuousMixtureTest
    finite_support_worst_type_i: float
    finite_support_worst_type_ii: float
    objective_difference: float
    maximum_member_error_difference_from_primal: float
    strict_support_count: int
    tie_support_count: int
    randomization_probability: float
    stable_on_finite_support: bool


def build_continuous_mixture_test(
    solution: FiniteMinimaxSolution,
    null_family: ProductDirichletFamily,
    alternative_family: ProductDirichletFamily,
    null_discretization: ImportanceDiscretization,
    alternative_discretization: ImportanceDiscretization,
    support: CommonProposalSupport,
    *,
    reproduction_tolerance: float = 2.0e-5,
    dual_coefficient_tolerance: float = 1.0e-12,
) -> ContinuousRepresentationDiagnostics:
    """Convert stable finite-LP duals into a continuous MID-space rule.

    Because the finite probability rows are self-normalized, the density
    coefficients are ``lambda_j/Z_j`` and ``gamma_k/Z_k`` where
    ``Z=(1/S) sum p/r``.  Treating the raw dual weights as density-mixture
    weights would generally fail to reproduce the solved finite LP.  When the
    LP used audited coefficient pruning, this continuous density rule has no
    exactly identical hard-pruned analogue; the returned independent
    finite-support reproduction diagnostic must therefore pass before use.
    """

    if (
        solution.null_dual_multipliers.shape != (null_family.member_count,)
        or solution.alternative_dual_multipliers.shape
        != (alternative_family.member_count,)
        or null_discretization.weights.shape
        != (null_family.member_count, support.support_size)
        or alternative_discretization.weights.shape
        != (alternative_family.member_count, support.support_size)
    ):
        raise ValueError("continuous-test inputs do not align with the finite LP")
    null_coefficients = (
        solution.null_dual_multipliers
        / null_discretization.raw_mass_estimates
    )
    alternative_coefficients = (
        solution.alternative_dual_multipliers
        / alternative_discretization.raw_mass_estimates
    )
    null_total = float(np.sum(null_coefficients))
    alternative_total = float(np.sum(alternative_coefficients))
    if (
        null_total <= float(dual_coefficient_tolerance)
        or alternative_total <= float(dual_coefficient_tolerance)
    ):
        raise ContinuousRepresentationUnavailable(
            "finite dual has no nonzero two-sided mixture representation"
        )
    null_weights = null_coefficients / null_total
    alternative_weights = alternative_coefficients / alternative_total
    log_threshold = math.log(null_total / alternative_total)

    discrete_alternative = (
        solution.alternative_dual_multipliers
        @ alternative_discretization.weights
    )
    discrete_null = (
        solution.null_dual_multipliers @ null_discretization.weights
    )
    advantage = discrete_alternative - discrete_null
    scale = np.maximum.reduce(
        (
            np.abs(discrete_alternative),
            np.abs(discrete_null),
            np.full(support.support_size, 1.0 / support.support_size),
        )
    )
    tie = np.abs(advantage) <= 2.0e-7 * scale
    strict = advantage > 2.0e-7 * scale
    null_dual_total = solution.null_dual_total
    if null_dual_total <= float(dual_coefficient_tolerance):
        raise ContinuousRepresentationUnavailable("null dual total is zero")
    least_favourable_null = (
        solution.null_dual_multipliers / null_dual_total
    ) @ null_discretization.weights
    target_probability = float(
        least_favourable_null @ solution.decision_probabilities
    )
    strict_probability = float(least_favourable_null @ strict.astype(float))
    tie_mass = float(least_favourable_null @ tie.astype(float))
    if tie_mass > 1.0e-14:
        randomization = (target_probability - strict_probability) / tie_mass
    else:
        randomization = 0.0
    if randomization < -2.0e-7 or randomization > 1.0 + 2.0e-7:
        raise ContinuousRepresentationUnavailable(
            "finite dual tie set cannot reproduce the primal randomization"
        )
    randomization = min(1.0, max(0.0, float(randomization)))
    continuous_test = ContinuousMixtureTest(
        null_family=null_family,
        alternative_family=alternative_family,
        null_mixture_weights=null_weights,
        alternative_mixture_weights=alternative_weights,
        log_likelihood_threshold=log_threshold,
        tie_probability=randomization,
    )
    probabilities = continuous_test.decision_probability(support.observations)
    null_errors = null_discretization.weights @ probabilities
    alternative_errors = alternative_discretization.weights @ (1.0 - probabilities)
    all_differences = np.concatenate(
        (
            np.abs(null_errors - solution.null_errors),
            np.abs(alternative_errors - solution.alternative_errors),
        )
    )
    maximum_difference = float(np.max(all_differences))
    worst_type_i = float(np.max(null_errors))
    worst_type_ii = float(np.max(alternative_errors))
    objective_difference = abs(worst_type_ii - solution.beta_objective)
    stable = bool(
        maximum_difference <= float(reproduction_tolerance)
        and worst_type_i <= solution.epsilon + float(reproduction_tolerance)
        and objective_difference <= float(reproduction_tolerance)
    )
    return ContinuousRepresentationDiagnostics(
        test=continuous_test,
        finite_support_worst_type_i=worst_type_i,
        finite_support_worst_type_ii=worst_type_ii,
        objective_difference=objective_difference,
        maximum_member_error_difference_from_primal=maximum_difference,
        strict_support_count=int(np.count_nonzero(strict)),
        tie_support_count=int(np.count_nonzero(tie)),
        randomization_probability=randomization,
        stable_on_finite_support=stable,
    )
