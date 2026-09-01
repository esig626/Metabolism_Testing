"""Observable MID classes for the abstract three-edge topology motif.

This module defines the scientific objects in the T0, T1, and T2 topology
benchmarks.  It deliberately stops before hypothesis testing.  The public
:class:`TopologyMIDClass` contains only exact observable MIDs, their block
layout, and opaque member identifiers.  The nuisance coordinates used to
construct those MIDs are kept in a separate :class:`TopologyNuisanceGrid`
that must never be supplied to a decision rule.

The two-edge expression implemented here is the declared toy pool-mixing
model.  It is not presented as a generic EMU equation.  In every two-edge
class, both sources share the same ``theta`` and the mixing weight is confined
to ``[0.2, 0.8]`` so both declared edges contribute.

Deterministic parameter grids approximate continuous observable-law classes.
Their row frequency is not a prior over topologies or nuisance coordinates.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
import math
from types import MappingProxyType
from typing import Mapping, Sequence

import numpy as np
from scipy.spatial import cKDTree


TOPOLOGY_LABELS = ("G_A", "G_B", "G_C", "G_AB", "G_AC", "G_BC")
TOPOLOGY_EDGES: Mapping[str, tuple[str, ...]] = MappingProxyType(
    {
        "G_A": ("e_A",),
        "G_B": ("e_B",),
        "G_C": ("e_C",),
        "G_AB": ("e_A", "e_B"),
        "G_AC": ("e_A", "e_C"),
        "G_BC": ("e_B", "e_C"),
    }
)
TOPOLOGY_SOURCES: Mapping[str, tuple[str, ...]] = MappingProxyType(
    {
        "G_A": ("A",),
        "G_B": ("B",),
        "G_C": ("C",),
        "G_AB": ("A", "B"),
        "G_AC": ("A", "C"),
        "G_BC": ("B", "C"),
    }
)

SOURCE_LABELS = ("A", "B", "C")
BENCHMARK_LABELS = ("T0", "T1", "T2")
MID_COMPONENT_LABELS = ("M+0", "M+1", "M+2", "M+3")
MID_BLOCKS = (("X", 0, 4),)

THETA_LOWER = 0.0
THETA_UPPER = 1.0
WEIGHT_LOWER = 0.2
WEIGHT_UPPER = 0.8
INITIAL_THETA_POINT_COUNT = 21
INITIAL_WEIGHT_POINT_COUNT = 21
DENSE_THETA_POINT_COUNT = 161
DENSE_WEIGHT_POINT_COUNT = 161
MID_SUM_ABSOLUTE_TOLERANCE = 2.0e-12
EXACT_ALIAS_ABSOLUTE_TOLERANCE = 5.0e-15

A0 = (0.82, 0.13, 0.04, 0.01)
A1 = (0.76, 0.17, 0.05, 0.02)
B0 = (0.08, 0.72, 0.15, 0.05)
B1 = (0.10, 0.65, 0.18, 0.07)
C0 = (0.04, 0.10, 0.24, 0.62)
C1 = (0.05, 0.12, 0.28, 0.55)


class TopologyConstructionError(RuntimeError):
    """Raised when a required topology construction identity fails."""


def _readonly_float_array(values: Sequence[float] | np.ndarray) -> np.ndarray:
    result = np.array(values, dtype=float, copy=True)
    result.setflags(write=False)
    return result


def _validate_mid_rows(values: np.ndarray, *, context: str) -> None:
    rows = np.asarray(values, dtype=float)
    if rows.ndim < 1 or rows.shape[-1] != len(MID_COMPONENT_LABELS):
        raise ValueError(f"{context} must end in four MID components")
    if not np.all(np.isfinite(rows)) or np.any(rows <= 0.0):
        raise ValueError(f"{context} must be finite and strictly positive")
    sums = np.sum(rows, axis=-1)
    if float(np.max(np.abs(sums - 1.0))) > MID_SUM_ABSOLUTE_TOLERANCE:
        raise ValueError(f"{context} must sum to one")


@dataclass(frozen=True)
class SourceMIDFamily:
    """One affine source MID family on the shared coordinate ``theta``."""

    source_label: str
    endpoint0: np.ndarray
    endpoint1: np.ndarray

    def __post_init__(self) -> None:
        label = str(self.source_label)
        endpoint0 = _readonly_float_array(self.endpoint0)
        endpoint1 = _readonly_float_array(self.endpoint1)
        if label not in SOURCE_LABELS:
            raise ValueError(f"unknown source label {label!r}")
        if endpoint0.shape != (4,) or endpoint1.shape != (4,):
            raise ValueError("source-family endpoints must have four components")
        _validate_mid_rows(endpoint0, context=f"{label}0")
        _validate_mid_rows(endpoint1, context=f"{label}1")
        object.__setattr__(self, "source_label", label)
        object.__setattr__(self, "endpoint0", endpoint0)
        object.__setattr__(self, "endpoint1", endpoint1)

    def evaluate(self, theta: float | Sequence[float] | np.ndarray) -> np.ndarray:
        """Evaluate the affine family without renormalising its exact MID."""

        coordinate = np.asarray(theta, dtype=float)
        if not np.all(np.isfinite(coordinate)):
            raise ValueError("theta must be finite")
        if np.any(coordinate < THETA_LOWER) or np.any(coordinate > THETA_UPPER):
            raise ValueError("theta must lie in [0, 1]")
        result = self.endpoint0 + coordinate[..., np.newaxis] * (
            self.endpoint1 - self.endpoint0
        )
        _validate_mid_rows(result, context=f"p_{self.source_label}(theta)")
        return _readonly_float_array(result)


@dataclass(frozen=True)
class TopologyBenchmarkDefinition:
    """Immutable source-family definition for one declared benchmark."""

    benchmark_id: str
    description: str
    source_families: Mapping[str, SourceMIDFamily]

    def __post_init__(self) -> None:
        benchmark_id = str(self.benchmark_id)
        families = dict(self.source_families)
        if benchmark_id not in BENCHMARK_LABELS:
            raise ValueError(f"unknown topology benchmark {benchmark_id!r}")
        if tuple(families) != SOURCE_LABELS:
            raise ValueError("source families must be supplied in A, B, C order")
        for source_label, family in families.items():
            if family.source_label != source_label:
                raise ValueError("source-family mapping key and label differ")
        object.__setattr__(self, "benchmark_id", benchmark_id)
        object.__setattr__(self, "description", str(self.description))
        object.__setattr__(self, "source_families", MappingProxyType(families))


def _family(source_label: str, endpoint0: Sequence[float], endpoint1: Sequence[float]) -> SourceMIDFamily:
    return SourceMIDFamily(source_label, np.asarray(endpoint0), np.asarray(endpoint1))


_A_FAMILY = _family("A", A0, A1)
_B_FAMILY = _family("B", B0, B1)
_C_SEPARATED_FAMILY = _family("C", C0, C1)
_C_ALIAS_FAMILY = _family(
    "C",
    0.5 * (np.asarray(A0, dtype=float) + np.asarray(B0, dtype=float)),
    0.5 * (np.asarray(A1, dtype=float) + np.asarray(B1, dtype=float)),
)

BENCHMARK_DEFINITIONS: Mapping[str, TopologyBenchmarkDefinition] = MappingProxyType(
    {
        "T0": TopologyBenchmarkDefinition(
            "T0",
            "exact identical-observable-class impossibility control",
            {
                "A": _family("A", A0, A1),
                "B": _family("B", A0, A1),
                "C": _family("C", A0, A1),
            },
        ),
        "T1": TopologyBenchmarkDefinition(
            "T1",
            "separated six-topology positive control",
            {"A": _A_FAMILY, "B": _B_FAMILY, "C": _C_SEPARATED_FAMILY},
        ),
        "T2": TopologyBenchmarkDefinition(
            "T2",
            "exact topology-aliasing control",
            {"A": _A_FAMILY, "B": _B_FAMILY, "C": _C_ALIAS_FAMILY},
        ),
    }
)


def benchmark_definition(benchmark_id: str) -> TopologyBenchmarkDefinition:
    """Return a declared benchmark or reject an undeclared variant."""

    try:
        return BENCHMARK_DEFINITIONS[str(benchmark_id)]
    except KeyError as error:
        raise ValueError(f"unknown topology benchmark {benchmark_id!r}") from error


def topology_sources(topology_label: str) -> tuple[str, ...]:
    """Return the sources corresponding to one exact topology label."""

    try:
        return TOPOLOGY_SOURCES[str(topology_label)]
    except KeyError as error:
        raise ValueError(f"unknown topology label {topology_label!r}") from error


def source_mid(
    benchmark_id: str,
    source_label: str,
    theta: float | Sequence[float] | np.ndarray,
) -> np.ndarray:
    """Evaluate one source family for a declared topology benchmark."""

    definition = benchmark_definition(benchmark_id)
    try:
        family = definition.source_families[str(source_label)]
    except KeyError as error:
        raise ValueError(f"unknown source label {source_label!r}") from error
    return family.evaluate(theta)


def topology_mid(
    benchmark_id: str,
    topology_label: str,
    theta: float | Sequence[float] | np.ndarray,
    mixing_weight: float | Sequence[float] | np.ndarray | None = None,
) -> np.ndarray:
    """Evaluate the exact observable MID for one topology member.

    Array inputs are broadcast.  For a two-edge topology the result is
    ``w p_i(theta) + (1-w) p_j(theta)`` with one common ``theta``.  Supplying
    a weight for a single-edge class, or omitting it for a two-edge class, is
    an error rather than an implicit nuisance convention.
    """

    sources = topology_sources(topology_label)
    coordinate = np.asarray(theta, dtype=float)
    if len(sources) == 1:
        if mixing_weight is not None:
            raise ValueError("single-edge topology members do not have a mixing weight")
        return source_mid(benchmark_id, sources[0], coordinate)

    if mixing_weight is None:
        raise ValueError("two-edge topology members require a mixing weight")
    weight = np.asarray(mixing_weight, dtype=float)
    try:
        coordinate, weight = np.broadcast_arrays(coordinate, weight)
    except ValueError as error:
        raise ValueError("theta and mixing-weight arrays are not broadcast-compatible") from error
    if not np.all(np.isfinite(weight)):
        raise ValueError("mixing weights must be finite")
    if np.any(weight < WEIGHT_LOWER) or np.any(weight > WEIGHT_UPPER):
        raise ValueError("mixing weights must lie in [0.2, 0.8]")
    left = source_mid(benchmark_id, sources[0], coordinate)
    right = source_mid(benchmark_id, sources[1], coordinate)
    # In T0 the two source families are exactly identical.  Returning the
    # common row directly prevents arithmetic roundoff from obscuring that
    # mathematically exact observable-class identity.
    if np.array_equal(left, right):
        return _readonly_float_array(left)
    result = weight[..., np.newaxis] * left + (1.0 - weight[..., np.newaxis]) * right
    # ``C=(A+B)/2`` is a construction-level identity in T2.  Evaluate the
    # required G_C/G_AB anchor through the same source-family code path when
    # the declared weight is exactly 0.5.  This canonicalisation prevents a
    # harmless change in floating evaluation order from turning the exact
    # shared observable law into two merely adjacent Dirichlet parameter
    # vectors in the finite numerical control.
    if benchmark_id == "T2" and topology_label == "G_AB":
        anchor = weight == 0.5
        if np.any(anchor):
            result = np.where(
                anchor[..., np.newaxis],
                source_mid("T2", "C", coordinate),
                result,
            )
    _validate_mid_rows(result, context=f"{topology_label} exact MID")
    return _readonly_float_array(result)


@dataclass(frozen=True)
class TopologyMIDClass:
    """An immutable MID-only class safe to hand to a testing algorithm."""

    class_id: str
    member_ids: tuple[str, ...]
    blocks: tuple[tuple[str, int, int], ...]
    exact_mids: np.ndarray

    def __post_init__(self) -> None:
        class_id = str(self.class_id)
        member_ids = tuple(str(value) for value in self.member_ids)
        blocks = tuple(
            (str(name), int(start), int(stop)) for name, start, stop in self.blocks
        )
        mids = np.array(self.exact_mids, dtype=float, copy=True)
        if class_id not in TOPOLOGY_LABELS:
            raise ValueError(f"unknown topology label {class_id!r}")
        if blocks != MID_BLOCKS:
            raise ValueError("the three-edge motif observation must be the four-component X MID")
        if mids.ndim != 2 or mids.shape != (len(member_ids), 4) or len(mids) < 1:
            raise ValueError("MID rows and member identifiers do not align")
        if len(set(member_ids)) != len(member_ids):
            raise ValueError("topology member identifiers must be unique")
        _validate_mid_rows(mids, context=f"{class_id} MID class")
        mids.setflags(write=False)
        object.__setattr__(self, "class_id", class_id)
        object.__setattr__(self, "member_ids", member_ids)
        object.__setattr__(self, "blocks", blocks)
        object.__setattr__(self, "exact_mids", mids)

    @property
    def member_count(self) -> int:
        return len(self.member_ids)

    @property
    def observation_dimension(self) -> int:
        return self.exact_mids.shape[1]


@dataclass(frozen=True)
class TopologyNuisanceGrid:
    """Construction-only nuisance metadata that must not enter a decision rule."""

    benchmark_id: str
    class_id: str
    member_ids: tuple[str, ...]
    theta_values: np.ndarray
    mixing_weights: np.ndarray | None

    def __post_init__(self) -> None:
        benchmark_id = benchmark_definition(self.benchmark_id).benchmark_id
        sources = topology_sources(self.class_id)
        member_ids = tuple(str(value) for value in self.member_ids)
        theta_values = np.array(self.theta_values, dtype=float, copy=True)
        if theta_values.shape != (len(member_ids),) or len(theta_values) < 1:
            raise ValueError("theta values and member identifiers do not align")
        if not np.all(np.isfinite(theta_values)) or np.any(theta_values < 0.0) or np.any(theta_values > 1.0):
            raise ValueError("theta values must lie in [0, 1]")
        if len(sources) == 1:
            if self.mixing_weights is not None:
                raise ValueError("single-edge nuisance grids cannot contain weights")
            weights = None
        else:
            if self.mixing_weights is None:
                raise ValueError("two-edge nuisance grids require weights")
            weights = np.array(self.mixing_weights, dtype=float, copy=True)
            if weights.shape != theta_values.shape:
                raise ValueError("mixing weights and theta values do not align")
            if not np.all(np.isfinite(weights)) or np.any(weights < WEIGHT_LOWER) or np.any(weights > WEIGHT_UPPER):
                raise ValueError("mixing weights must lie in [0.2, 0.8]")
            weights.setflags(write=False)
        theta_values.setflags(write=False)
        object.__setattr__(self, "benchmark_id", benchmark_id)
        object.__setattr__(self, "class_id", str(self.class_id))
        object.__setattr__(self, "member_ids", member_ids)
        object.__setattr__(self, "theta_values", theta_values)
        object.__setattr__(self, "mixing_weights", weights)


def theta_grid(point_count: int = INITIAL_THETA_POINT_COUNT) -> np.ndarray:
    """Return an endpoint-inclusive deterministic grid on ``[0, 1]``."""

    count = int(point_count)
    if count < 2:
        raise ValueError("a theta grid needs at least two points")
    return _readonly_float_array(np.linspace(THETA_LOWER, THETA_UPPER, count))


def weight_grid(point_count: int = INITIAL_WEIGHT_POINT_COUNT) -> np.ndarray:
    """Return an endpoint-inclusive odd grid containing the T2 anchor.

    Requiring an odd count makes ``w=0.5`` an exact represented coordinate.
    An even grid would silently omit the required C/AB alias and is therefore
    rejected instead of being treated as an interchangeable refinement.
    """

    count = int(point_count)
    if count < 2:
        raise ValueError("a weight grid needs at least two points")
    if count % 2 == 0:
        raise ValueError("a topology weight grid needs an odd point count containing w=0.5")
    return _readonly_float_array(np.linspace(WEIGHT_LOWER, WEIGHT_UPPER, count))


def _point_arrays(
    topology_label: str,
    theta_values: Sequence[float] | np.ndarray,
    mixing_weights: Sequence[float] | np.ndarray | None,
) -> tuple[np.ndarray, np.ndarray | None]:
    sources = topology_sources(topology_label)
    theta_array = np.asarray(theta_values, dtype=float)
    if theta_array.ndim != 1 or len(theta_array) < 1:
        raise ValueError("topology members need a nonempty one-dimensional theta array")
    if len(sources) == 1:
        if mixing_weights is not None:
            raise ValueError("single-edge topology members cannot contain weights")
        return theta_array, None
    if mixing_weights is None:
        raise ValueError("two-edge topology members require weights")
    weight_array = np.asarray(mixing_weights, dtype=float)
    if weight_array.shape != theta_array.shape:
        raise ValueError("pointwise theta and weight arrays must have the same shape")
    return theta_array, weight_array


def construct_topology_class_from_points(
    benchmark_id: str,
    topology_label: str,
    theta_values: Sequence[float] | np.ndarray,
    mixing_weights: Sequence[float] | np.ndarray | None = None,
    *,
    member_id_prefix: str | None = None,
) -> tuple[TopologyMIDClass, TopologyNuisanceGrid]:
    """Construct observable members at paired nuisance coordinates.

    The returned objects intentionally separate the testing interface from
    construction metadata.  A solver should receive only the first object.
    """

    benchmark_id = benchmark_definition(benchmark_id).benchmark_id
    topology_label = str(topology_label)
    theta_array, weight_array = _point_arrays(
        topology_label, theta_values, mixing_weights
    )
    mids = topology_mid(benchmark_id, topology_label, theta_array, weight_array)
    prefix = (
        f"{benchmark_id}_{topology_label}_member"
        if member_id_prefix is None
        else str(member_id_prefix)
    )
    member_ids = tuple(f"{prefix}_{index:06d}" for index in range(len(theta_array)))
    observable = TopologyMIDClass(
        class_id=topology_label,
        member_ids=member_ids,
        blocks=MID_BLOCKS,
        exact_mids=mids,
    )
    nuisance = TopologyNuisanceGrid(
        benchmark_id=benchmark_id,
        class_id=topology_label,
        member_ids=member_ids,
        theta_values=theta_array,
        mixing_weights=weight_array,
    )
    return observable, nuisance


def construct_topology_class_grid(
    benchmark_id: str,
    topology_label: str,
    *,
    theta_point_count: int = INITIAL_THETA_POINT_COUNT,
    weight_point_count: int = INITIAL_WEIGHT_POINT_COUNT,
) -> tuple[TopologyMIDClass, TopologyNuisanceGrid]:
    """Construct one topology class on the declared Cartesian grid."""

    topology_label = str(topology_label)
    theta_values = theta_grid(theta_point_count)
    if len(topology_sources(topology_label)) == 1:
        return construct_topology_class_from_points(
            benchmark_id, topology_label, theta_values
        )
    weights = weight_grid(weight_point_count)
    theta_mesh, weight_mesh = np.meshgrid(theta_values, weights, indexing="ij")
    return construct_topology_class_from_points(
        benchmark_id,
        topology_label,
        theta_mesh.reshape(-1),
        weight_mesh.reshape(-1),
    )


def construct_all_topology_class_grids(
    benchmark_id: str,
    *,
    theta_point_count: int = INITIAL_THETA_POINT_COUNT,
    weight_point_count: int = INITIAL_WEIGHT_POINT_COUNT,
) -> tuple[tuple[TopologyMIDClass, ...], tuple[TopologyNuisanceGrid, ...]]:
    """Construct all six classes in their exact declared order."""

    observables: list[TopologyMIDClass] = []
    nuisance_grids: list[TopologyNuisanceGrid] = []
    for topology_label in TOPOLOGY_LABELS:
        observable, nuisance = construct_topology_class_grid(
            benchmark_id,
            topology_label,
            theta_point_count=theta_point_count,
            weight_point_count=weight_point_count,
        )
        observables.append(observable)
        nuisance_grids.append(nuisance)
    return tuple(observables), tuple(nuisance_grids)


@dataclass(frozen=True)
class PairwiseGridGeometry:
    """Deterministic geometry of two represented observable MID sets."""

    left_class_id: str
    right_class_id: str
    left_member_count: int
    right_member_count: int
    minimum_l2: float
    minimum_rms: float
    intersects_at_tolerance: bool
    intersection_tolerance: float
    closest_left_member_id: str
    closest_right_member_id: str
    left_to_right_hausdorff_l2: float
    right_to_left_hausdorff_l2: float


def pairwise_grid_geometry(
    left: TopologyMIDClass,
    right: TopologyMIDClass,
    *,
    intersection_tolerance: float = 1.0e-10,
) -> PairwiseGridGeometry:
    """Measure represented-set separation using a shared Euclidean metric."""

    tolerance = float(intersection_tolerance)
    if not math.isfinite(tolerance) or tolerance < 0.0:
        raise ValueError("intersection tolerance must be finite and nonnegative")
    left_tree = cKDTree(left.exact_mids)
    right_tree = cKDTree(right.exact_mids)
    left_distances, left_neighbours = right_tree.query(left.exact_mids, k=1)
    right_distances, _ = left_tree.query(right.exact_mids, k=1)
    left_index = int(np.argmin(left_distances))
    right_index = int(left_neighbours[left_index])
    minimum = float(left_distances[left_index])
    return PairwiseGridGeometry(
        left_class_id=left.class_id,
        right_class_id=right.class_id,
        left_member_count=left.member_count,
        right_member_count=right.member_count,
        minimum_l2=minimum,
        minimum_rms=minimum / math.sqrt(left.observation_dimension),
        intersects_at_tolerance=minimum <= tolerance,
        intersection_tolerance=tolerance,
        closest_left_member_id=left.member_ids[left_index],
        closest_right_member_id=right.member_ids[right_index],
        left_to_right_hausdorff_l2=float(np.max(left_distances)),
        right_to_left_hausdorff_l2=float(np.max(right_distances)),
    )


def all_pairwise_grid_geometry(
    classes: Sequence[TopologyMIDClass],
    *,
    intersection_tolerance: float = 1.0e-10,
) -> tuple[PairwiseGridGeometry, ...]:
    """Return all 15 unordered comparisons in declared topology order."""

    items = tuple(classes)
    if tuple(item.class_id for item in items) != TOPOLOGY_LABELS:
        raise ValueError("topology classes must be supplied in the declared order")
    return tuple(
        pairwise_grid_geometry(
            items[left_index],
            items[right_index],
            intersection_tolerance=intersection_tolerance,
        )
        for left_index, right_index in combinations(range(len(items)), 2)
    )


def observable_law_sets_equal(
    left: TopologyMIDClass,
    right: TopologyMIDClass,
    *,
    tolerance: float = 0.0,
) -> bool:
    """Test represented-law set equality without using row multiplicities."""

    geometry = pairwise_grid_geometry(
        left, right, intersection_tolerance=float(tolerance)
    )
    return bool(
        geometry.left_to_right_hausdorff_l2 <= float(tolerance)
        and geometry.right_to_left_hausdorff_l2 <= float(tolerance)
    )


@dataclass(frozen=True)
class NumericalContinuousGeometry:
    """A bounded numerical search result, not an exact continuum proof."""

    benchmark_id: str
    left_class_id: str
    right_class_id: str
    minimum_l2: float
    minimum_rms: float
    intersects_at_tolerance: bool
    intersection_tolerance: float
    left_theta: float
    left_weight: float | None
    right_theta: float
    right_weight: float | None
    optimizer_success: bool
    optimizer_message: str
    seed: int


def numerical_continuous_pair_geometry(
    benchmark_id: str,
    left_topology: str,
    right_topology: str,
    *,
    seed: int = 1729,
    intersection_tolerance: float = 1.0e-9,
    optimizer_tolerance: float = 1.0e-10,
    maximum_iterations: int = 600,
) -> NumericalContinuousGeometry:
    """Numerically minimize exact-MID distance over both nuisance domains.

    This deterministic-seed differential-evolution search is useful for
    auditing unexpected intersections that a Cartesian grid could miss.  A
    positive numerical minimum is evidence, not an exact separation proof.
    """

    from scipy.optimize import differential_evolution

    benchmark_id = benchmark_definition(benchmark_id).benchmark_id
    left_topology = str(left_topology)
    right_topology = str(right_topology)
    left_sources = topology_sources(left_topology)
    right_sources = topology_sources(right_topology)
    tolerance = float(intersection_tolerance)
    if not math.isfinite(tolerance) or tolerance < 0.0:
        raise ValueError("intersection tolerance must be finite and nonnegative")
    bounds: list[tuple[float, float]] = [(THETA_LOWER, THETA_UPPER)]
    if len(left_sources) == 2:
        bounds.append((WEIGHT_LOWER, WEIGHT_UPPER))
    right_offset = len(bounds)
    bounds.append((THETA_LOWER, THETA_UPPER))
    if len(right_sources) == 2:
        bounds.append((WEIGHT_LOWER, WEIGHT_UPPER))

    def objective(parameters: np.ndarray) -> float:
        left_weight = parameters[1] if len(left_sources) == 2 else None
        right_weight = (
            parameters[right_offset + 1] if len(right_sources) == 2 else None
        )
        left_mid = topology_mid(
            benchmark_id, left_topology, parameters[0], left_weight
        )
        right_mid = topology_mid(
            benchmark_id, right_topology, parameters[right_offset], right_weight
        )
        difference = left_mid - right_mid
        return float(np.dot(difference, difference))

    result = differential_evolution(
        objective,
        bounds,
        seed=int(seed),
        tol=float(optimizer_tolerance),
        atol=1.0e-15,
        maxiter=int(maximum_iterations),
        popsize=12,
        polish=True,
        updating="immediate",
        workers=1,
    )
    parameters = np.asarray(result.x, dtype=float)
    left_weight_value = float(parameters[1]) if len(left_sources) == 2 else None
    right_weight_value = (
        float(parameters[right_offset + 1]) if len(right_sources) == 2 else None
    )
    minimum = math.sqrt(max(0.0, float(result.fun)))
    return NumericalContinuousGeometry(
        benchmark_id=benchmark_id,
        left_class_id=left_topology,
        right_class_id=right_topology,
        minimum_l2=minimum,
        minimum_rms=minimum / math.sqrt(len(MID_COMPONENT_LABELS)),
        intersects_at_tolerance=minimum <= tolerance,
        intersection_tolerance=tolerance,
        left_theta=float(parameters[0]),
        left_weight=left_weight_value,
        right_theta=float(parameters[right_offset]),
        right_weight=right_weight_value,
        optimizer_success=bool(result.success),
        optimizer_message=str(result.message),
        seed=int(seed),
    )


@dataclass(frozen=True)
class ExactAliasDiagnostics:
    """Near-machine-precision verification of a construction-level identity."""

    benchmark_id: str
    left_class_id: str
    right_class_id: str
    relation: str
    evaluation_count: int
    maximum_absolute_component_error: float
    maximum_l2_error: float
    tolerance: float
    passed: bool


def _alias_diagnostics(
    benchmark_id: str,
    left_class_id: str,
    right_class_id: str,
    relation: str,
    left_mids: np.ndarray,
    right_mids: np.ndarray,
    *,
    tolerance: float,
) -> ExactAliasDiagnostics:
    left = np.asarray(left_mids, dtype=float)
    right = np.asarray(right_mids, dtype=float)
    if left.shape != right.shape or left.ndim != 2 or left.shape[1] != 4:
        raise ValueError("alias verification arrays must be aligned MID rows")
    errors = left - right
    maximum_absolute = float(np.max(np.abs(errors)))
    maximum_l2 = float(np.max(np.linalg.norm(errors, axis=1)))
    return ExactAliasDiagnostics(
        benchmark_id=benchmark_id,
        left_class_id=left_class_id,
        right_class_id=right_class_id,
        relation=relation,
        evaluation_count=len(left),
        maximum_absolute_component_error=maximum_absolute,
        maximum_l2_error=maximum_l2,
        tolerance=float(tolerance),
        passed=maximum_absolute <= float(tolerance),
    )


def verify_t0_exact_aliases(
    *,
    theta_values: Sequence[float] | np.ndarray | None = None,
    weight_values: Sequence[float] | np.ndarray | None = None,
    tolerance: float = EXACT_ALIAS_ABSOLUTE_TOLERANCE,
) -> tuple[ExactAliasDiagnostics, ...]:
    """Verify that all six T0 topologies induce the same observable laws."""

    thetas = theta_grid(17) if theta_values is None else np.asarray(theta_values, dtype=float)
    weights = weight_grid(7) if weight_values is None else np.asarray(weight_values, dtype=float)
    if thetas.ndim != 1 or weights.ndim != 1 or len(thetas) < 1 or len(weights) < 1:
        raise ValueError("T0 alias controls require nonempty one-dimensional grids")
    diagnostics: list[ExactAliasDiagnostics] = []
    for left_class_id, right_class_id in combinations(TOPOLOGY_LABELS, 2):
        left_weight_options: tuple[float | None, ...] = (
            (None,)
            if len(topology_sources(left_class_id)) == 1
            else tuple(float(value) for value in weights)
        )
        right_weight_options: tuple[float | None, ...] = (
            (None,)
            if len(topology_sources(right_class_id)) == 1
            else tuple(float(value) for value in weights)
        )
        left_rows: list[np.ndarray] = []
        right_rows: list[np.ndarray] = []
        for theta_value in thetas:
            for left_weight in left_weight_options:
                for right_weight in right_weight_options:
                    left_rows.append(
                        topology_mid("T0", left_class_id, float(theta_value), left_weight)
                    )
                    right_rows.append(
                        topology_mid("T0", right_class_id, float(theta_value), right_weight)
                    )
        diagnostics.append(
            _alias_diagnostics(
                "T0",
                left_class_id,
                right_class_id,
                "all sources equal p_A(theta); pair weights are observationally irrelevant",
                np.asarray(left_rows),
                np.asarray(right_rows),
                tolerance=tolerance,
            )
        )
    result = tuple(diagnostics)
    if not all(item.passed for item in result):
        worst = max(result, key=lambda item: item.maximum_absolute_component_error)
        raise TopologyConstructionError(
            "T0 observable-class identity failed for "
            f"{worst.left_class_id} versus {worst.right_class_id}: "
            f"{worst.maximum_absolute_component_error:.12g}"
        )
    return result


def verify_t2_exact_aliases(
    *,
    theta_values: Sequence[float] | np.ndarray | None = None,
    overlap_weight_values: Sequence[float] | np.ndarray | None = None,
    tolerance: float = EXACT_ALIAS_ABSOLUTE_TOLERANCE,
) -> tuple[ExactAliasDiagnostics, ...]:
    """Verify the required and additional exact T2 topology intersections.

    Besides the required ``G_C = G_AB(w=0.5)`` relation, the construction
    introduces two exact overlap families:

    * ``G_AB(w_AB) = G_AC(w_AC=2*w_AB-1)`` for ``w_AB in [0.6, 0.8]``;
    * ``G_AB(w_AB) = G_BC(w_BC=1-2*w_AB)`` for ``w_AB in [0.2, 0.4]``.

    Every relation uses the same theta on both sides.
    """

    thetas = theta_grid(161) if theta_values is None else np.asarray(theta_values, dtype=float)
    if thetas.ndim != 1 or len(thetas) < 1:
        raise ValueError("T2 alias controls require a nonempty theta grid")

    c_mid = topology_mid("T2", "G_C", thetas)
    c_as_ab_mid = topology_mid("T2", "G_AB", thetas, np.full(len(thetas), 0.5))
    required = _alias_diagnostics(
        "T2",
        "G_C",
        "G_AB",
        "theta shared; G_AB weight=0.5",
        c_mid,
        c_as_ab_mid,
        tolerance=tolerance,
    )

    base_weights = (
        np.linspace(0.0, 1.0, 17, dtype=float)
        if overlap_weight_values is None
        else np.asarray(overlap_weight_values, dtype=float)
    )
    if base_weights.ndim != 1 or len(base_weights) < 1 or np.any(base_weights < 0.0) or np.any(base_weights > 1.0):
        raise ValueError("overlap-weight coordinates must lie in [0, 1]")
    theta_mesh, base_mesh = np.meshgrid(thetas, base_weights, indexing="ij")
    flat_theta = theta_mesh.reshape(-1)
    flat_base = base_mesh.reshape(-1)

    # Generate the mapped topology weight first so the declared endpoints
    # remain inside [0.2, 0.8] under floating arithmetic.
    ac_weight = 0.2 + 0.4 * flat_base
    ab_ac_weight = 0.5 * (1.0 + ac_weight)
    ab_as_ac = _alias_diagnostics(
        "T2",
        "G_AB",
        "G_AC",
        "theta shared; w_AB in [0.6,0.8], w_AC=2*w_AB-1",
        topology_mid("T2", "G_AB", flat_theta, ab_ac_weight),
        topology_mid("T2", "G_AC", flat_theta, ac_weight),
        tolerance=tolerance,
    )

    bc_weight = 0.2 + 0.4 * flat_base
    ab_bc_weight = np.clip(
        0.5 * (1.0 - bc_weight), WEIGHT_LOWER, WEIGHT_UPPER
    )
    ab_as_bc = _alias_diagnostics(
        "T2",
        "G_AB",
        "G_BC",
        "theta shared; w_AB in [0.2,0.4], w_BC=1-2*w_AB",
        topology_mid("T2", "G_AB", flat_theta, ab_bc_weight),
        topology_mid("T2", "G_BC", flat_theta, bc_weight),
        tolerance=tolerance,
    )

    result = (required, ab_as_ac, ab_as_bc)
    if not all(item.passed for item in result):
        worst = max(result, key=lambda item: item.maximum_absolute_component_error)
        raise TopologyConstructionError(
            "T2 exact topology alias failed for "
            f"{worst.left_class_id} versus {worst.right_class_id}: "
            f"{worst.maximum_absolute_component_error:.12g}"
        )
    return result


def topology_definitions_payload() -> dict[str, object]:
    """Return a JSON-serialisable record of the frozen scientific definitions."""

    benchmarks: dict[str, object] = {}
    for benchmark_id in BENCHMARK_LABELS:
        definition = BENCHMARK_DEFINITIONS[benchmark_id]
        benchmarks[benchmark_id] = {
            "description": definition.description,
            "source_families": {
                source_label: {
                    "endpoint0": family.endpoint0.tolist(),
                    "endpoint1": family.endpoint1.tolist(),
                }
                for source_label, family in definition.source_families.items()
            },
        }
    return {
        "topology_order": list(TOPOLOGY_LABELS),
        "topologies": {
            topology_label: {"edges": list(TOPOLOGY_EDGES[topology_label])}
            for topology_label in TOPOLOGY_LABELS
        },
        "observation": {
            "pool": "X",
            "carbon_count": 3,
            "components": list(MID_COMPONENT_LABELS),
        },
        "nuisance_domains": {
            "theta": [THETA_LOWER, THETA_UPPER],
            "two_edge_weight": [WEIGHT_LOWER, WEIGHT_UPPER],
            "two_edge_theta_is_shared": True,
        },
        "benchmarks": benchmarks,
    }
