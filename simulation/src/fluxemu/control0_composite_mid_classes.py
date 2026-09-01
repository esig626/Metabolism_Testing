"""Scientific construction for the Control 0 composite MID-law benchmarks.

This module stops at the boundary between synthetic hidden-state generation and
hypothesis testing.  Flux coordinates are used only to evaluate the frozen
forward EMU model.  The public :class:`MIDClass` handed to a testing algorithm
contains exact MIDs, their block layout, and opaque member identifiers; hidden
coordinates and complete flux vectors are returned in a separate object.

The deterministic grids approximate continuous classes.  They do not define a
distribution over feasible states and their row frequency has no biological
meaning.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from types import MappingProxyType
from typing import Callable, Mapping, Sequence

import numpy as np


EXPECTED_CONTROL0_FINGERPRINT = (
    "abe6a2f0832b8d2833297d065b21cce0be74622d03cfdaad2b0523f997969c70"
)
REACTION_ORDER = tuple(f"v{index}" for index in range(1, 9))
FULL_TARGET_ORDER = (
    "OAC",
    "citrate",
    "AKG",
    "succinate",
    "fumarate",
    "glutamate",
)
PANEL_ID = "panel_047"
PANEL_TARGETS = ("OAC", "citrate", "AKG", "succinate", "glutamate")
TARGET_COMPONENT_COUNTS = MappingProxyType(
    {
        "OAC": 5,
        "citrate": 7,
        "AKG": 6,
        "succinate": 5,
        "fumarate": 5,
        "glutamate": 6,
    }
)
PANEL_COMPONENT_COUNT = sum(TARGET_COMPONENT_COUNTS[target] for target in PANEL_TARGETS)

CANONICAL_A_LOWER = 0.0
CANONICAL_A_UPPER = 100.0
CANONICAL_FLUX_LOWER = 0.0
CANONICAL_FLUX_UPPER = 1_000_000.0
REPRESENTATIVE_B = 75.0
PRIMARY_R_MEAS = 0.005
CLASS_GRID_SIZES = (41, 81, 161)
VALIDATION_GRID_CELLS = 640
B_INVARIANCE_ABSOLUTE_TOLERANCE = 1.0e-9
MID_SUM_ABSOLUTE_TOLERANCE = 2.0e-12
MID_DISTINCT_TOLERANCE = 1.0e-8
CLEAR_SEPARATION_FACTOR = 5.0


class ScientificConstructionError(RuntimeError):
    """A required Control 0 construction or geometry check failed."""


@dataclass(frozen=True)
class AInterval:
    """Closed interval for the hidden synthetic coordinate ``a``."""

    lower: float
    upper: float

    def __post_init__(self) -> None:
        lower = float(self.lower)
        upper = float(self.upper)
        if not (math.isfinite(lower) and math.isfinite(upper)):
            raise ValueError("a-interval endpoints must be finite")
        if not CANONICAL_A_LOWER <= lower < upper <= CANONICAL_A_UPPER:
            raise ValueError(f"invalid Control 0 a interval {(lower, upper)}")
        object.__setattr__(self, "lower", lower)
        object.__setattr__(self, "upper", upper)

    @property
    def width(self) -> float:
        return self.upper - self.lower

    def contains(self, a: float, *, tolerance: float = 1.0e-12) -> bool:
        value = float(a)
        return self.lower - tolerance <= value <= self.upper + tolerance


@dataclass(frozen=True)
class HiddenCondition:
    """One infinite hidden feasible condition set before forward evaluation."""

    condition_id: str
    a_interval: AInterval

    def b_bounds(self, a: float) -> tuple[float, float]:
        value = float(a)
        if not self.a_interval.contains(value):
            raise ValueError(f"a={value} is outside {self.condition_id}")
        return 0.0, 999_900.0 + value


@dataclass(frozen=True)
class BenchmarkDefinition:
    benchmark_id: str
    description: str
    h0: HiddenCondition
    h1: HiddenCondition


def _condition(benchmark_id: str, hypothesis: str, lower: float, upper: float) -> HiddenCondition:
    return HiddenCondition(f"{benchmark_id}_{hypothesis}", AInterval(lower, upper))


BENCHMARK_DEFINITIONS: Mapping[str, BenchmarkDefinition] = MappingProxyType(
    {
        "C0": BenchmarkDefinition(
            "C0",
            "identical-class impossibility control",
            _condition("C0", "H0", 40.0, 60.0),
            _condition("C0", "H1", 40.0, 60.0),
        ),
        "C1": BenchmarkDefinition(
            "C1",
            "easy composite positive control",
            _condition("C1", "H0", 20.0, 35.0),
            _condition("C1", "H1", 65.0, 80.0),
        ),
        "C2": BenchmarkDefinition(
            "C2",
            "nontrivial composite benchmark",
            _condition("C2", "H0", 40.0, 49.0),
            _condition("C2", "H1", 51.0, 60.0),
        ),
    }
)


@dataclass(frozen=True)
class ReactionRange:
    reaction_id: str
    lower: float
    upper: float


@dataclass(frozen=True)
class FeasibleSetDiagnostics:
    """Exact condition-specific projections implied by the affine geometry."""

    condition_id: str
    a_lower: float
    a_upper: float
    b_global_lower: float
    b_global_upper: float
    b_upper_formula: str
    feasible_dimension: int
    state_cardinality: str
    fva_equivalent_ranges: tuple[ReactionRange, ...]


def exact_coordinate_feasible(a: float, b: float) -> bool:
    """Return whether ``(a,b)`` is in the unchanged exact feasible domain."""

    a_value = float(a)
    b_value = float(b)
    return bool(
        math.isfinite(a_value)
        and math.isfinite(b_value)
        and CANONICAL_A_LOWER <= a_value <= CANONICAL_A_UPPER
        and 0.0 <= b_value <= 999_900.0 + a_value
    )


def exact_flux_vector(a: float, b: float) -> tuple[float, ...]:
    """Evaluate the established affine Control 0 flux parameterisation."""

    a_value = float(a)
    b_value = float(b)
    if not exact_coordinate_feasible(a_value, b_value):
        raise ValueError(f"infeasible Control 0 coordinates {(a_value, b_value)}")
    return (
        100.0,
        100.0,
        a_value,
        100.0 - a_value,
        100.0 - a_value,
        100.0 - a_value + b_value,
        b_value,
        a_value,
    )


def feasible_set_diagnostics(condition: HiddenCondition) -> FeasibleSetDiagnostics:
    """Compute exact FVA-equivalent ranges without independently sampling them.

    These are analytic projections of the already validated affine feasible
    set.  They are not raw COBRApy FVA results: the canonical boundary-source
    metabolites retain different balance semantics in the unconfigured COBRA
    object, and changing those semantics is outside this benchmark.
    """

    lower = condition.a_interval.lower
    upper = condition.a_interval.upper
    ranges = (
        ReactionRange("v1", 100.0, 100.0),
        ReactionRange("v2", 100.0, 100.0),
        ReactionRange("v3", lower, upper),
        ReactionRange("v4", 100.0 - upper, 100.0 - lower),
        ReactionRange("v5", 100.0 - upper, 100.0 - lower),
        ReactionRange("v6", 100.0 - upper, 1_000_000.0),
        ReactionRange("v7", 0.0, 999_900.0 + upper),
        ReactionRange("v8", lower, upper),
    )
    for item in ranges:
        if not (
            CANONICAL_FLUX_LOWER <= item.lower <= item.upper <= CANONICAL_FLUX_UPPER
        ):
            raise ScientificConstructionError(
                f"condition {condition.condition_id} has an infeasible range for {item.reaction_id}"
            )
    # Joint corner checks guard the affine construction; the ranges above are
    # diagnostics and are never sampled reaction by reaction.
    for a_value in (lower, upper):
        for b_value in (0.0, 999_900.0 + a_value):
            flux = exact_flux_vector(a_value, b_value)
            if not all(
                CANONICAL_FLUX_LOWER <= value <= CANONICAL_FLUX_UPPER
                for value in flux
            ):
                raise ScientificConstructionError(
                    f"condition {condition.condition_id} has an infeasible joint corner"
                )
    return FeasibleSetDiagnostics(
        condition_id=condition.condition_id,
        a_lower=lower,
        a_upper=upper,
        b_global_lower=0.0,
        b_global_upper=999_900.0 + upper,
        b_upper_formula="999900 + a",
        feasible_dimension=2,
        state_cardinality="uncountably infinite",
        fva_equivalent_ranges=ranges,
    )


def validate_scientific_identity(
    *,
    forward_fingerprint: str,
    inverse_fingerprint: str,
    reaction_order: Sequence[str],
    panel_id: str,
    panel_targets: Sequence[str],
    a_bounds: Sequence[float],
    b_bounds_at_a0: Sequence[float],
    b_bounds_at_a100: Sequence[float],
) -> None:
    """Stop if the live canonical identity, panel, or domain has changed."""

    if forward_fingerprint != EXPECTED_CONTROL0_FINGERPRINT:
        raise ScientificConstructionError("canonical Control 0 fingerprint changed")
    if inverse_fingerprint != forward_fingerprint:
        raise ScientificConstructionError("forward/inverse ordered identity failed")
    if tuple(reaction_order) != REACTION_ORDER:
        raise ScientificConstructionError("canonical reaction order changed")
    if panel_id != PANEL_ID or tuple(panel_targets) != PANEL_TARGETS:
        raise ScientificConstructionError("panel_047 is not the full panel minus fumarate")
    if tuple(float(value) for value in a_bounds) != (0.0, 100.0):
        raise ScientificConstructionError("canonical a-domain changed")
    if tuple(float(value) for value in b_bounds_at_a0) != (0.0, 999_900.0):
        raise ScientificConstructionError("canonical b-domain changed at a=0")
    if tuple(float(value) for value in b_bounds_at_a100) != (0.0, 1_000_000.0):
        raise ScientificConstructionError("canonical b-domain changed at a=100")


# Each triple is (metabolite target, inclusive start, exclusive stop).
MIDBlock = tuple[str, int, int]


@dataclass(frozen=True)
class MIDClass:
    """MID-only class representation safe to hand to a testing algorithm."""

    class_id: str
    panel_id: str
    member_ids: tuple[str, ...]
    blocks: tuple[MIDBlock, ...]
    exact_mids: np.ndarray

    def __post_init__(self) -> None:
        member_ids = tuple(str(value) for value in self.member_ids)
        blocks = tuple(
            (str(name), int(start), int(stop)) for name, start, stop in self.blocks
        )
        mids = np.array(self.exact_mids, dtype=float, copy=True)
        if self.panel_id != PANEL_ID:
            raise ValueError(f"unsupported MID panel {self.panel_id!r}")
        if mids.ndim != 2 or mids.shape[0] != len(member_ids) or mids.shape[0] < 1:
            raise ValueError("MID class rows and member identifiers do not align")
        if len(set(member_ids)) != len(member_ids):
            raise ValueError("MID class member identifiers must be unique")
        if not np.all(np.isfinite(mids)) or np.any(mids <= 0.0):
            raise ValueError("Dirichlet MID centres must be finite and strictly positive")
        cursor = 0
        names: list[str] = []
        for name, start, stop in blocks:
            if start != cursor or stop <= start or stop > mids.shape[1]:
                raise ValueError("MID blocks must be nonempty, contiguous, and ordered")
            sums = np.sum(mids[:, start:stop], axis=1)
            if float(np.max(np.abs(sums - 1.0))) > MID_SUM_ABSOLUTE_TOLERANCE:
                raise ValueError(f"{name} MID block does not sum to one")
            cursor = stop
            names.append(name)
        if cursor != mids.shape[1] or tuple(names) != PANEL_TARGETS:
            raise ValueError("MID blocks do not define canonical panel_047")
        if mids.shape[1] != PANEL_COMPONENT_COUNT:
            raise ValueError("panel_047 component count changed")
        mids.setflags(write=False)
        object.__setattr__(self, "member_ids", member_ids)
        object.__setattr__(self, "blocks", blocks)
        object.__setattr__(self, "exact_mids", mids)

    @property
    def member_count(self) -> int:
        return self.exact_mids.shape[0]

    @property
    def observation_dimension(self) -> int:
        return self.exact_mids.shape[1]


@dataclass(frozen=True)
class HiddenStateGrid:
    """Synthetic construction metadata that must not be passed to a test."""

    condition_id: str
    member_ids: tuple[str, ...]
    a_values: np.ndarray
    b_values: np.ndarray
    flux_vectors: np.ndarray

    def __post_init__(self) -> None:
        member_ids = tuple(str(value) for value in self.member_ids)
        a_values = np.array(self.a_values, dtype=float, copy=True)
        b_values = np.array(self.b_values, dtype=float, copy=True)
        flux_vectors = np.array(self.flux_vectors, dtype=float, copy=True)
        count = len(member_ids)
        if a_values.shape != (count,) or b_values.shape != (count,):
            raise ValueError("hidden coordinate arrays do not align with member identifiers")
        if flux_vectors.shape != (count, len(REACTION_ORDER)):
            raise ValueError("hidden complete-flux matrix has unexpected shape")
        for index in range(count):
            expected = exact_flux_vector(a_values[index], b_values[index])
            if not np.array_equal(flux_vectors[index], np.asarray(expected, dtype=float)):
                raise ValueError("hidden flux row does not match the exact affine geometry")
        for array in (a_values, b_values, flux_vectors):
            array.setflags(write=False)
        object.__setattr__(self, "member_ids", member_ids)
        object.__setattr__(self, "a_values", a_values)
        object.__setattr__(self, "b_values", b_values)
        object.__setattr__(self, "flux_vectors", flux_vectors)


def deterministic_a_grid(interval: AInterval, point_count: int) -> np.ndarray:
    """Return an endpoint-inclusive deterministic class grid."""

    count = int(point_count)
    if count < 2:
        raise ValueError("a class grid requires at least two points")
    values = np.linspace(interval.lower, interval.upper, count, dtype=float)
    values.setflags(write=False)
    return values


def staggered_validation_a_grid(
    interval: AInterval, *, cell_count: int = VALIDATION_GRID_CELLS
) -> np.ndarray:
    """Return endpoints plus a dense midpoint-staggered validation grid."""

    count = int(cell_count)
    if count < 2:
        raise ValueError("validation grid requires at least two cells")
    fractions = (np.arange(count, dtype=float) + 0.5) / count
    interior = interval.lower + interval.width * fractions
    values = np.concatenate(([interval.lower], interior, [interval.upper]))
    values.setflags(write=False)
    return values


def panel_blocks() -> tuple[MIDBlock, ...]:
    offset = 0
    result: list[MIDBlock] = []
    for target in PANEL_TARGETS:
        stop = offset + TARGET_COMPONENT_COUNTS[target]
        result.append((target, offset, stop))
        offset = stop
    if offset != PANEL_COMPONENT_COUNT:  # pragma: no cover - constant consistency guard
        raise RuntimeError("panel component layout is inconsistent")
    return tuple(result)


FullMIDPredictor = Callable[[float, float], Sequence[float]]


def _panel_indices(target_indices: Mapping[str, Sequence[int]]) -> np.ndarray:
    arrays: list[np.ndarray] = []
    used: set[int] = set()
    for target in PANEL_TARGETS:
        if target not in target_indices:
            raise ScientificConstructionError(f"forward output lacks target {target}")
        indices = np.asarray(target_indices[target], dtype=int)
        expected_count = TARGET_COMPONENT_COUNTS[target]
        if indices.ndim != 1 or len(indices) != expected_count:
            raise ScientificConstructionError(
                f"forward component count changed for {target}"
            )
        if np.any(indices < 0) or np.any(np.diff(indices) <= 0):
            raise ScientificConstructionError(f"forward component order changed for {target}")
        if any(int(index) in used for index in indices):
            raise ScientificConstructionError("forward target component indices overlap")
        used.update(int(index) for index in indices)
        arrays.append(indices)
    return np.concatenate(arrays)


def construct_mid_class_at_a_values(
    condition: HiddenCondition,
    a_values: Sequence[float],
    *,
    full_mid_predictor: FullMIDPredictor,
    target_indices: Mapping[str, Sequence[int]],
    representative_b: float = REPRESENTATIVE_B,
) -> tuple[MIDClass, HiddenStateGrid]:
    """Push joint feasible hidden states through the fixed forward EMU model."""

    values = np.asarray(a_values, dtype=float)
    if values.ndim != 1 or len(values) < 1 or not np.all(np.isfinite(values)):
        raise ValueError("a values must be a nonempty finite one-dimensional array")
    if np.any(np.diff(values) <= 0.0):
        raise ValueError("a values must be strictly increasing")
    if not all(condition.a_interval.contains(value) for value in values):
        raise ValueError(f"a grid leaves hidden condition {condition.condition_id}")
    b_value = float(representative_b)
    if not all(exact_coordinate_feasible(value, b_value) for value in values):
        raise ValueError("representative b is infeasible for the requested a grid")

    indices = _panel_indices(target_indices)
    member_ids = tuple(
        f"{condition.condition_id}_member_{index:04d}"
        for index in range(len(values))
    )
    rows: list[np.ndarray] = []
    for a_value in values:
        full_mid = np.asarray(full_mid_predictor(float(a_value), b_value), dtype=float)
        if full_mid.ndim != 1 or len(full_mid) <= int(np.max(indices)):
            raise ScientificConstructionError("forward MID output has unexpected shape")
        rows.append(np.asarray(full_mid[indices], dtype=float))
    mids = np.asarray(rows, dtype=float)
    b_values = np.full(len(values), b_value, dtype=float)
    flux_vectors = np.asarray(
        [exact_flux_vector(a_value, b_value) for a_value in values], dtype=float
    )
    law_class = MIDClass(
        class_id=condition.condition_id,
        panel_id=PANEL_ID,
        member_ids=member_ids,
        blocks=panel_blocks(),
        exact_mids=mids,
    )
    hidden = HiddenStateGrid(
        condition_id=condition.condition_id,
        member_ids=member_ids,
        a_values=values,
        b_values=b_values,
        flux_vectors=flux_vectors,
    )
    return law_class, hidden


def construct_mid_class(
    condition: HiddenCondition,
    point_count: int,
    *,
    full_mid_predictor: FullMIDPredictor,
    target_indices: Mapping[str, Sequence[int]],
    representative_b: float = REPRESENTATIVE_B,
) -> tuple[MIDClass, HiddenStateGrid]:
    return construct_mid_class_at_a_values(
        condition,
        deterministic_a_grid(condition.a_interval, point_count),
        full_mid_predictor=full_mid_predictor,
        target_indices=target_indices,
        representative_b=representative_b,
    )


@dataclass(frozen=True)
class BInvarianceDiagnostics:
    panel_id: str
    tested_a_count: int
    evaluations: int
    maximum_absolute_mid_change: float
    maximum_l2_mid_change: float
    tolerance: float
    passed: bool
    worst_a: float
    worst_b: float
    reference_b: float


def verify_b_invariance(
    *,
    full_mid_predictor: FullMIDPredictor,
    target_indices: Mapping[str, Sequence[int]],
    a_values: Sequence[float],
    tolerance: float = B_INVARIANCE_ABSOLUTE_TOLERANCE,
) -> BInvarianceDiagnostics:
    """Numerically audit fixed-``a`` panel_047 invariance across feasible ``b``."""

    indices = _panel_indices(target_indices)
    values = tuple(float(value) for value in a_values)
    if not values or any(
        not CANONICAL_A_LOWER <= value <= CANONICAL_A_UPPER for value in values
    ):
        raise ValueError("b-invariance audit has invalid a values")
    maximum_absolute = -math.inf
    maximum_l2 = -math.inf
    worst_a = math.nan
    worst_b = math.nan
    worst_reference_b = math.nan
    evaluations = 0
    for a_value in values:
        b_upper = 999_900.0 + a_value
        reference_b = min(REPRESENTATIVE_B, b_upper)
        reference = np.asarray(
            full_mid_predictor(a_value, reference_b), dtype=float
        )[indices]
        b_values = tuple(dict.fromkeys((0.0, reference_b, 0.5 * b_upper, b_upper)))
        for b_value in b_values:
            candidate = np.asarray(
                full_mid_predictor(a_value, b_value), dtype=float
            )[indices]
            difference = candidate - reference
            absolute = float(np.max(np.abs(difference)))
            l2 = float(np.linalg.norm(difference))
            evaluations += 1
            if absolute > maximum_absolute:
                maximum_absolute = absolute
                worst_a = a_value
                worst_b = b_value
                worst_reference_b = reference_b
            maximum_l2 = max(maximum_l2, l2)
    diagnostics = BInvarianceDiagnostics(
        panel_id=PANEL_ID,
        tested_a_count=len(values),
        evaluations=evaluations,
        maximum_absolute_mid_change=maximum_absolute,
        maximum_l2_mid_change=maximum_l2,
        tolerance=float(tolerance),
        passed=maximum_absolute <= float(tolerance),
        worst_a=worst_a,
        worst_b=worst_b,
        reference_b=worst_reference_b,
    )
    if not diagnostics.passed:
        raise ScientificConstructionError(
            "panel_047 changed materially along the hidden b direction: "
            f"max_abs={maximum_absolute:.12g}, tolerance={float(tolerance):.12g}"
        )
    return diagnostics


@dataclass(frozen=True)
class MIDGeometryDiagnostics:
    benchmark_id: str
    h0_member_count: int
    h1_member_count: int
    observation_dimension: int
    identical_grids: bool
    minimum_cross_l2: float
    minimum_cross_rms: float
    h0_to_h1_directed_hausdorff_l2: float
    h1_to_h0_directed_hausdorff_l2: float
    hausdorff_l2: float
    h0_diameter_l2: float
    h1_diameter_l2: float
    closest_h0_member_id: str
    closest_h1_member_id: str


def _pairwise_geometry(
    left: np.ndarray, right: np.ndarray, *, chunk_size: int = 128
) -> tuple[float, int, int, float, float]:
    best = math.inf
    best_left = -1
    best_right = -1
    left_nearest = np.full(len(left), math.inf, dtype=float)
    right_nearest = np.full(len(right), math.inf, dtype=float)
    for start in range(0, len(left), int(chunk_size)):
        stop = min(start + int(chunk_size), len(left))
        distances = np.linalg.norm(
            left[start:stop, np.newaxis, :] - right[np.newaxis, :, :], axis=2
        )
        flat_index = int(np.argmin(distances))
        local_left, local_right = np.unravel_index(flat_index, distances.shape)
        candidate = float(distances[local_left, local_right])
        if candidate < best:
            best = candidate
            best_left = start + int(local_left)
            best_right = int(local_right)
        left_nearest[start:stop] = np.min(distances, axis=1)
        right_nearest = np.minimum(right_nearest, np.min(distances, axis=0))
    return (
        best,
        best_left,
        best_right,
        float(np.max(left_nearest)),
        float(np.max(right_nearest)),
    )


def _diameter(values: np.ndarray, *, chunk_size: int = 128) -> float:
    result = 0.0
    for start in range(0, len(values), int(chunk_size)):
        stop = min(start + int(chunk_size), len(values))
        distances = np.linalg.norm(
            values[start:stop, np.newaxis, :] - values[np.newaxis, :, :], axis=2
        )
        result = max(result, float(np.max(distances)))
    return result


def mid_class_geometry(
    benchmark_id: str, h0: MIDClass, h1: MIDClass
) -> MIDGeometryDiagnostics:
    """Measure deterministic grid geometry without assuming endpoint reduction."""

    if h0.panel_id != PANEL_ID or h1.panel_id != PANEL_ID or h0.blocks != h1.blocks:
        raise ValueError("MID classes do not share canonical panel_047")
    if h0.observation_dimension != h1.observation_dimension:
        raise ValueError("MID class dimensions differ")
    minimum, i0, i1, directed0, directed1 = _pairwise_geometry(
        h0.exact_mids, h1.exact_mids
    )
    dimension = h0.observation_dimension
    return MIDGeometryDiagnostics(
        benchmark_id=str(benchmark_id),
        h0_member_count=h0.member_count,
        h1_member_count=h1.member_count,
        observation_dimension=dimension,
        identical_grids=(
            h0.member_count == h1.member_count
            and np.array_equal(h0.exact_mids, h1.exact_mids)
        ),
        minimum_cross_l2=minimum,
        minimum_cross_rms=minimum / math.sqrt(dimension),
        h0_to_h1_directed_hausdorff_l2=directed0,
        h1_to_h0_directed_hausdorff_l2=directed1,
        hausdorff_l2=max(directed0, directed1),
        h0_diameter_l2=_diameter(h0.exact_mids),
        h1_diameter_l2=_diameter(h1.exact_mids),
        closest_h0_member_id=h0.member_ids[i0],
        closest_h1_member_id=h1.member_ids[i1],
    )


def verify_prescribed_geometry(
    c0: MIDGeometryDiagnostics,
    c1: MIDGeometryDiagnostics,
    c2: MIDGeometryDiagnostics,
    *,
    distinct_tolerance: float = MID_DISTINCT_TOLERANCE,
    clear_separation_factor: float = CLEAR_SEPARATION_FACTOR,
) -> float:
    """Enforce the C0 identity and predeclared easy-versus-hard geometry checks."""

    if not c0.identical_grids or c0.minimum_cross_l2 != 0.0 or c0.hausdorff_l2 != 0.0:
        raise ScientificConstructionError("C0 induced MID grids are not identical")
    if c1.minimum_cross_l2 <= float(distinct_tolerance):
        raise ScientificConstructionError("C1 MID classes are not numerically distinct")
    if c2.minimum_cross_l2 <= float(distinct_tolerance):
        raise ScientificConstructionError("C2 MID classes are not numerically distinct")
    ratio = c1.minimum_cross_l2 / c2.minimum_cross_l2
    if ratio < float(clear_separation_factor):
        raise ScientificConstructionError(
            "C1 is not clearly more separated than C2 on the independent MID grid: "
            f"ratio={ratio:.12g}, required={float(clear_separation_factor):.12g}"
        )
    return ratio
