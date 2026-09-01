"""Two-block X+W observation panel for the frozen Phase 2A EMU motif.

Phase 2B changes only the measurement boundary.  The biological states and
their EMU-generated ``X_full`` and ``W_full`` MIDs come from the unchanged
Phase 2A generator in :mod:`fluxemu.emu_topology_edge_reconstruction`.
The object admitted to inference contains only opaque member identifiers,
the two-block layout, and the two generated MID blocks.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import json
import math
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

from .emu_topology_edge_reconstruction import (
    DEFAULT_WEIGHT_POINT_COUNT,
    OBSERVED_TARGET_ID,
    SUPPORT_LABELS,
    WITHHELD_TARGET_ID,
    ForwardGeneratedClasses,
    SupportClassMetadata,
    generate_forward_classes,
)


XW_BLOCKS = (
    (OBSERVED_TARGET_ID, 0, 3),
    (WITHHELD_TARGET_ID, 3, 5),
)
FORWARD_REGRESSION_TOLERANCE = 1.0e-15
EXACT_GEOMETRY_TOLERANCE = 1.0e-12
PHASE2A_EXACT_ALIAS_PAIRS = frozenset(
    {
        ("G_A", "G_C"),
        ("G_A", "G_AC"),
        ("G_C", "G_AC"),
        ("G_AB", "G_BC"),
    }
)

# Exact coordinates are (b, a), the e_B and e_A flux fractions.  In this
# motif the X block identifies b and the W block identifies a.  The remaining
# fraction is c=1-a-b.  Endpoints use exact rational values, so intersections
# below are algebraic segment calculations rather than floating-point tests.
_ExactPoint = tuple[Fraction, Fraction]
_ExactSegment = tuple[_ExactPoint, _ExactPoint]
_EXACT_SUPPORT_SEGMENTS: Mapping[str, _ExactSegment] = MappingProxyType(
    {
        "G_A": ((Fraction(0), Fraction(1)),) * 2,
        "G_B": ((Fraction(1), Fraction(0)),) * 2,
        "G_C": ((Fraction(0), Fraction(0)),) * 2,
        "G_AB": (
            (Fraction(4, 5), Fraction(1, 5)),
            (Fraction(1, 5), Fraction(4, 5)),
        ),
        "G_AC": (
            (Fraction(0), Fraction(1, 5)),
            (Fraction(0), Fraction(4, 5)),
        ),
        "G_BC": (
            (Fraction(1, 5), Fraction(0)),
            (Fraction(4, 5), Fraction(0)),
        ),
    }
)


def _readonly_float_array(values: Sequence[float] | np.ndarray) -> np.ndarray:
    result = np.array(values, dtype=float, copy=True)
    result.setflags(write=False)
    return result


@dataclass(frozen=True)
class XWObservableMIDClass:
    """The complete MID-only input admitted to Phase 2B inference."""

    member_ids: tuple[str, ...]
    blocks: tuple[tuple[str, int, int], ...]
    exact_mids: np.ndarray

    def __post_init__(self) -> None:
        member_ids = tuple(str(value) for value in self.member_ids)
        blocks = tuple(
            (str(name), int(start), int(stop)) for name, start, stop in self.blocks
        )
        mids = _readonly_float_array(self.exact_mids)
        if not member_ids or len(set(member_ids)) != len(member_ids):
            raise ValueError("observable member identifiers must be nonempty and unique")
        if blocks != XW_BLOCKS:
            raise ValueError("the Phase 2B observation must contain X_full and W_full")
        if mids.shape != (len(member_ids), 5):
            raise ValueError("X+W MID rows and member identifiers do not align")
        if not np.all(np.isfinite(mids)) or np.any(mids <= 0.0):
            raise ValueError("X+W MID components must be finite and positive")
        for name, start, stop in blocks:
            if not np.allclose(
                np.sum(mids[:, start:stop], axis=1),
                1.0,
                rtol=0.0,
                atol=1.0e-12,
            ):
                raise ValueError(f"{name} must remain a separately normalized MID")
        object.__setattr__(self, "member_ids", member_ids)
        object.__setattr__(self, "blocks", blocks)
        object.__setattr__(self, "exact_mids", mids)

    @property
    def member_count(self) -> int:
        return len(self.member_ids)


@dataclass(frozen=True)
class XWPanelConstruction:
    """MID-only classes plus separately quarantined construction metadata."""

    observables: tuple[XWObservableMIDClass, ...]
    audit_metadata: tuple[SupportClassMetadata, ...]
    forward_validation: Mapping[str, Any]
    weight_point_count: int

    def __post_init__(self) -> None:
        observables = tuple(self.observables)
        metadata = tuple(self.audit_metadata)
        if len(observables) != len(SUPPORT_LABELS) or len(metadata) != len(
            SUPPORT_LABELS
        ):
            raise ValueError("all six Phase 2B support classes are required")
        if tuple(item.support_label for item in metadata) != SUPPORT_LABELS:
            raise ValueError("construction metadata uses an unexpected support order")
        for observable, hidden in zip(observables, metadata, strict=True):
            if observable.member_ids != hidden.member_ids:
                raise ValueError("observable and construction member IDs do not align")
        if not bool(self.forward_validation.get("valid", False)):
            raise ValueError("the reused Phase 2A forward calculation is invalid")
        object.__setattr__(self, "observables", observables)
        object.__setattr__(self, "audit_metadata", metadata)
        object.__setattr__(
            self,
            "forward_validation",
            MappingProxyType(dict(self.forward_validation)),
        )
        object.__setattr__(self, "weight_point_count", int(self.weight_point_count))

    @property
    def support_labels(self) -> tuple[str, ...]:
        return tuple(item.support_label for item in self.audit_metadata)


def construct_xw_panel(
    *,
    weight_point_count: int = DEFAULT_WEIGHT_POINT_COUNT,
    phase2a_generated: ForwardGeneratedClasses | None = None,
) -> XWPanelConstruction:
    """Re-expose both generated blocks without changing any forward state."""

    generated = (
        generate_forward_classes(weight_point_count=int(weight_point_count))
        if phase2a_generated is None
        else phase2a_generated
    )
    if generated.weight_point_count != int(weight_point_count):
        raise ValueError("the supplied Phase 2A classes use a different weight grid")
    observables: list[XWObservableMIDClass] = []
    for observed_x, hidden in zip(
        generated.observables, generated.metadata, strict=True
    ):
        if observed_x.member_ids != hidden.member_ids:
            raise ValueError("Phase 2A X and W rows do not align")
        observables.append(
            XWObservableMIDClass(
                member_ids=observed_x.member_ids,
                blocks=XW_BLOCKS,
                exact_mids=np.hstack((observed_x.exact_mids, hidden.withheld_mids)),
            )
        )
    return XWPanelConstruction(
        observables=tuple(observables),
        audit_metadata=generated.metadata,
        forward_validation=generated.forward_validation,
        weight_point_count=generated.weight_point_count,
    )


@dataclass(frozen=True)
class Phase2AForwardRegression:
    """Comparison of a live Phase 2B construction with frozen Phase 2A rows."""

    passed: bool
    tolerance: float
    member_count: int
    same_member_ids: bool
    same_support_labels: bool
    same_active_edges: bool
    same_weight_grid: bool
    same_flux_vectors: bool
    same_x_mids: bool
    same_w_mids: bool
    same_forward_validation: bool
    maximum_absolute_weight_error: float
    maximum_absolute_flux_error: float
    maximum_absolute_x_mid_error: float
    maximum_absolute_w_mid_error: float


def _maximum_finite_absolute_error(left: np.ndarray, right: np.ndarray) -> float:
    first = np.asarray(left, dtype=float)
    second = np.asarray(right, dtype=float)
    if first.shape != second.shape:
        return math.inf
    first_nan = np.isnan(first)
    second_nan = np.isnan(second)
    if not np.array_equal(first_nan, second_nan):
        return math.inf
    if np.any(np.isinf(first)) or np.any(np.isinf(second)):
        return math.inf
    finite = ~first_nan
    if not np.any(finite):
        return 0.0
    return float(np.max(np.abs(first[finite] - second[finite])))


def regress_against_phase2a_artifacts(
    panel: XWPanelConstruction,
    phase2a_result_directory: str | Path,
    *,
    tolerance: float = FORWARD_REGRESSION_TOLERANCE,
) -> Phase2AForwardRegression:
    """Require live state identities and MIDs to match the frozen artifacts.

    CSV decimal serialization is not bit preserving, so numerical fields are
    compared at a tolerance far below any scientific or solver tolerance.  The
    maximum observed discrepancy is retained in the regression artifact.
    """

    threshold = float(tolerance)
    if not np.isfinite(threshold) or threshold < 0.0:
        raise ValueError("the forward-regression tolerance must be nonnegative")
    directory = Path(phase2a_result_directory)
    observed_csv = pd.read_csv(directory / "observable_classes.csv")
    construction_csv = pd.read_csv(directory / "construction_metadata.csv")
    with (directory / "forward_validation.json").open(encoding="utf-8") as handle:
        frozen_validation = json.load(handle)

    live_member_ids = tuple(
        member_id for item in panel.observables for member_id in item.member_ids
    )
    frozen_member_ids = tuple(str(value) for value in observed_csv["member_id"])
    metadata_member_ids = tuple(str(value) for value in construction_csv["member_id"])
    live_supports = tuple(
        hidden.support_label
        for hidden in panel.audit_metadata
        for _ in hidden.member_ids
    )
    live_active_edges = tuple(
        "+".join(hidden.active_edges)
        for hidden in panel.audit_metadata
        for _ in hidden.member_ids
    )
    live_weights = np.concatenate(
        [
            (
                np.full(len(hidden.member_ids), np.nan, dtype=float)
                if hidden.mixing_weights is None
                else np.asarray(hidden.mixing_weights, dtype=float)
            )
            for hidden in panel.audit_metadata
        ]
    )
    frozen_weights = construction_csv["mixing_weight"].to_numpy(dtype=float)
    live_fluxes = np.vstack(
        [hidden.complete_fluxes.to_numpy(dtype=float) for hidden in panel.audit_metadata]
    )
    flux_columns = tuple(panel.audit_metadata[0].complete_fluxes.columns)
    frozen_fluxes = construction_csv.loc[:, flux_columns].to_numpy(dtype=float)
    live_mids = np.vstack([item.exact_mids for item in panel.observables])
    frozen_x = observed_csv.loc[:, ("M+0", "M+1", "M+2")].to_numpy(dtype=float)
    frozen_w = construction_csv.loc[:, ("W_M+0", "W_M+1")].to_numpy(dtype=float)

    weight_error = _maximum_finite_absolute_error(live_weights, frozen_weights)
    flux_error = _maximum_finite_absolute_error(live_fluxes, frozen_fluxes)
    x_error = _maximum_finite_absolute_error(live_mids[:, :3], frozen_x)
    w_error = _maximum_finite_absolute_error(live_mids[:, 3:], frozen_w)
    same_weight_nan_pattern = np.array_equal(
        np.isnan(live_weights), np.isnan(frozen_weights)
    )
    finite_live_weights = np.all(np.isfinite(live_weights[~np.isnan(live_weights)]))
    finite_frozen_weights = np.all(
        np.isfinite(frozen_weights[~np.isnan(frozen_weights)])
    )
    checks = {
        "same_member_ids": (
            live_member_ids == frozen_member_ids == metadata_member_ids
        ),
        "same_support_labels": live_supports
        == tuple(str(value) for value in construction_csv["support_label"]),
        "same_active_edges": live_active_edges
        == tuple(str(value) for value in construction_csv["active_edges"]),
        "same_weight_grid": live_weights.shape == frozen_weights.shape
        and same_weight_nan_pattern
        and finite_live_weights
        and finite_frozen_weights
        and weight_error <= threshold,
        "same_flux_vectors": live_fluxes.shape == frozen_fluxes.shape
        and np.all(np.isfinite(live_fluxes))
        and np.all(np.isfinite(frozen_fluxes))
        and flux_error <= threshold,
        "same_x_mids": live_mids[:, :3].shape == frozen_x.shape
        and np.all(np.isfinite(live_mids[:, :3]))
        and np.all(np.isfinite(frozen_x))
        and x_error <= threshold,
        "same_w_mids": live_mids[:, 3:].shape == frozen_w.shape
        and np.all(np.isfinite(live_mids[:, 3:]))
        and np.all(np.isfinite(frozen_w))
        and w_error <= threshold,
        "same_forward_validation": dict(panel.forward_validation)
        == frozen_validation,
    }
    result = Phase2AForwardRegression(
        passed=all(checks.values()),
        tolerance=threshold,
        member_count=len(live_member_ids),
        **checks,
        maximum_absolute_weight_error=weight_error,
        maximum_absolute_flux_error=flux_error,
        maximum_absolute_x_mid_error=x_error,
        maximum_absolute_w_mid_error=w_error,
    )
    if not result.passed:
        failed = ", ".join(name for name, value in checks.items() if not value)
        raise ValueError(f"Phase 2A forward regression failed: {failed}")
    return result


@dataclass(frozen=True)
class XWAlgebraDiagnostic:
    """Numerical EMU-row check of the exact construction formulas."""

    passed: bool
    state_count: int
    tolerance: float
    maximum_absolute_component_error: float
    exact_coordinate_statement: str


def verify_xw_coordinate_algebra(
    panel: XWPanelConstruction,
    *,
    tolerance: float = EXACT_GEOMETRY_TOLERANCE,
) -> XWAlgebraDiagnostic:
    """Check EMU rows against the motif's exact candidate-flux coordinates.

    If ``a``, ``b``, and ``c`` are the candidate-edge fractions, the declared
    maps and tracer imply

    ``X0=3/16+3b/8, X1=5/8-b/4, X2=3/16-b/8`` and
    ``W0=3/4-a/2, W1=1/4+a/2``.

    These formulas make the joint observation injective in ``(a,b,c)``.
    This function only verifies that the numerical EMU output reproduces that
    exact construction; it is not the proof used by the intersection test.
    """

    threshold = float(tolerance)
    if not math.isfinite(threshold) or threshold < 0.0:
        raise ValueError("the algebra-regression tolerance must be nonnegative")
    maximum = 0.0
    state_count = 0
    for observable, hidden in zip(
        panel.observables, panel.audit_metadata, strict=True
    ):
        edge_a = hidden.complete_fluxes["e_A"].to_numpy(dtype=float)
        edge_b = hidden.complete_fluxes["e_B"].to_numpy(dtype=float)
        expected = np.column_stack(
            (
                3.0 / 16.0 + 3.0 * edge_b / 8.0,
                5.0 / 8.0 - edge_b / 4.0,
                3.0 / 16.0 - edge_b / 8.0,
                3.0 / 4.0 - edge_a / 2.0,
                1.0 / 4.0 + edge_a / 2.0,
            )
        )
        maximum = max(
            maximum,
            float(np.max(np.abs(observable.exact_mids - expected))),
        )
        state_count += observable.member_count
    passed = maximum <= threshold
    if not passed:
        raise ValueError(
            "EMU rows do not reproduce the exact X+W coordinate formulas: "
            f"{maximum:.12g}"
        )
    return XWAlgebraDiagnostic(
        passed=passed,
        state_count=state_count,
        tolerance=threshold,
        maximum_absolute_component_error=maximum,
        exact_coordinate_statement=(
            "X identifies b=e_B; W identifies a=e_A; c=1-a-b"
        ),
    )


def _point_subtract(left: _ExactPoint, right: _ExactPoint) -> _ExactPoint:
    return left[0] - right[0], left[1] - right[1]


def _point_add_scaled(
    point: _ExactPoint, direction: _ExactPoint, scale: Fraction
) -> _ExactPoint:
    return point[0] + scale * direction[0], point[1] + scale * direction[1]


def _cross(left: _ExactPoint, right: _ExactPoint) -> Fraction:
    return left[0] * right[1] - left[1] * right[0]


def _point_on_segment(point: _ExactPoint, segment: _ExactSegment) -> bool:
    start, stop = segment
    if _cross(_point_subtract(point, start), _point_subtract(stop, start)) != 0:
        return False
    return all(
        min(start[index], stop[index]) <= point[index]
        <= max(start[index], stop[index])
        for index in range(2)
    )


def _fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def _point_text(point: _ExactPoint) -> str:
    return f"b={_fraction_text(point[0])};a={_fraction_text(point[1])}"


def _exact_segment_intersection(
    left: _ExactSegment, right: _ExactSegment
) -> tuple[bool, str]:
    """Return exact rational-segment intersection status and a witness."""

    p, p_stop = left
    q, q_stop = right
    r = _point_subtract(p_stop, p)
    s = _point_subtract(q_stop, q)
    left_is_point = r == (0, 0)
    right_is_point = s == (0, 0)
    if left_is_point and right_is_point:
        return (True, _point_text(p)) if p == q else (False, "")
    if left_is_point:
        return (True, _point_text(p)) if _point_on_segment(p, right) else (False, "")
    if right_is_point:
        return (True, _point_text(q)) if _point_on_segment(q, left) else (False, "")

    offset = _point_subtract(q, p)
    denominator = _cross(r, s)
    if denominator != 0:
        left_parameter = _cross(offset, s) / denominator
        right_parameter = _cross(offset, r) / denominator
        if (
            Fraction(0) <= left_parameter <= Fraction(1)
            and Fraction(0) <= right_parameter <= Fraction(1)
        ):
            witness = _point_add_scaled(p, r, left_parameter)
            return True, _point_text(witness)
        return False, ""
    if _cross(offset, r) != 0:
        return False, ""

    shared_endpoints = sorted(
        {
            point
            for point in (p, p_stop, q, q_stop)
            if _point_on_segment(point, left) and _point_on_segment(point, right)
        }
    )
    if not shared_endpoints:
        return False, ""
    if len(shared_endpoints) == 1:
        return True, _point_text(shared_endpoints[0])
    return (
        True,
        f"{_point_text(shared_endpoints[0])} to {_point_text(shared_endpoints[-1])}",
    )


@dataclass(frozen=True)
class XWPairwiseGeometry:
    """Numerical represented-grid distance between two raw X+W panels."""

    left_support: str
    right_support: str
    minimum_xw_l2: float
    minimum_five_component_rms: float
    x_block_rms_at_minimum: float
    w_block_rms_at_minimum: float
    closest_left_member_id: str
    closest_right_member_id: str
    represented_grid_intersects_at_tolerance: bool
    represented_grid_set_equal_at_tolerance: bool
    tolerance: float


def pairwise_xw_geometry(
    panel: XWPanelConstruction,
    *,
    tolerance: float = EXACT_GEOMETRY_TOLERANCE,
) -> tuple[XWPairwiseGeometry, ...]:
    """Compare all 15 represented class pairs without changing block sums.

    The five-coordinate L2 and RMS values are only geometric summaries of the
    raw concatenated blocks.  They do not define a five-component simplex or
    replace the product-Dirichlet measurement model.
    """

    threshold = float(tolerance)
    if not math.isfinite(threshold) or threshold < 0.0:
        raise ValueError("the geometry tolerance must be nonnegative")
    result: list[XWPairwiseGeometry] = []
    for left_index in range(len(SUPPORT_LABELS)):
        for right_index in range(left_index + 1, len(SUPPORT_LABELS)):
            left = panel.observables[left_index]
            right = panel.observables[right_index]
            differences = (
                left.exact_mids[:, np.newaxis, :]
                - right.exact_mids[np.newaxis, :, :]
            )
            squared_l2 = np.sum(np.square(differences), axis=2)
            flat_index = int(np.argmin(squared_l2))
            nearest_left, nearest_right = np.unravel_index(
                flat_index, squared_l2.shape
            )
            difference = differences[nearest_left, nearest_right]
            minimum = math.sqrt(float(squared_l2[nearest_left, nearest_right]))
            result.append(
                XWPairwiseGeometry(
                    left_support=SUPPORT_LABELS[left_index],
                    right_support=SUPPORT_LABELS[right_index],
                    minimum_xw_l2=minimum,
                    minimum_five_component_rms=minimum / math.sqrt(5.0),
                    x_block_rms_at_minimum=float(
                        np.sqrt(np.mean(np.square(difference[:3])))
                    ),
                    w_block_rms_at_minimum=float(
                        np.sqrt(np.mean(np.square(difference[3:])))
                    ),
                    closest_left_member_id=left.member_ids[int(nearest_left)],
                    closest_right_member_id=right.member_ids[int(nearest_right)],
                    represented_grid_intersects_at_tolerance=minimum <= threshold,
                    represented_grid_set_equal_at_tolerance=bool(
                        np.all(np.sqrt(np.min(squared_l2, axis=1)) <= threshold)
                        and np.all(np.sqrt(np.min(squared_l2, axis=0)) <= threshold)
                    ),
                    tolerance=threshold,
                )
            )
    return tuple(result)


@dataclass(frozen=True)
class XWExactAlias:
    """Exact support-set result kept separate from numerical grid distance."""

    left_support: str
    right_support: str
    phase2a_exact_x_alias: bool
    exact_xw_alias: bool
    exact_xw_set_equal: bool
    exact_weight_domain: str
    exact_witness: str
    exact_method: str
    minimum_represented_xw_l2: float
    minimum_represented_five_component_rms: float
    interpretation: str


def _alias_interpretation(left: str, right: str, intersects: bool) -> str:
    if intersects:
        return "The exact bounded support segments share the stated X+W law."
    explanations = {
        ("G_A", "G_C"): "W differs exactly, so the Phase 2A A/C X alias is removed.",
        ("G_A", "G_AC"): (
            "Equality would require the excluded endpoint w=1; W removes the X alias."
        ),
        ("G_C", "G_AC"): (
            "Equality would require the excluded endpoint w=0; W removes the X alias."
        ),
        ("G_AB", "G_BC"): (
            "Mirrored X equality would also require AB e_A flux w=0; W removes the alias."
        ),
    }
    return explanations.get(
        (left, right),
        "The exact X+W support segments are disjoint; this pair was not a Phase 2A alias.",
    )


def exact_xw_aliases(
    panel: XWPanelConstruction,
    *,
    tolerance: float = EXACT_GEOMETRY_TOLERANCE,
) -> tuple[XWExactAlias, ...]:
    """Return algebraic intersections plus separately labelled grid distances."""

    geometry = {
        (item.left_support, item.right_support): item
        for item in pairwise_xw_geometry(panel, tolerance=tolerance)
    }
    result: list[XWExactAlias] = []
    for left_index in range(len(SUPPORT_LABELS)):
        for right_index in range(left_index + 1, len(SUPPORT_LABELS)):
            left = SUPPORT_LABELS[left_index]
            right = SUPPORT_LABELS[right_index]
            intersects, witness = _exact_segment_intersection(
                _EXACT_SUPPORT_SEGMENTS[left], _EXACT_SUPPORT_SEGMENTS[right]
            )
            set_equal = set(_EXACT_SUPPORT_SEGMENTS[left]) == set(
                _EXACT_SUPPORT_SEGMENTS[right]
            )
            numerical = geometry[(left, right)]
            result.append(
                XWExactAlias(
                    left_support=left,
                    right_support=right,
                    phase2a_exact_x_alias=(left, right)
                    in PHASE2A_EXACT_ALIAS_PAIRS,
                    exact_xw_alias=intersects,
                    exact_xw_set_equal=set_equal,
                    exact_weight_domain="w in [1/5,4/5] for two-edge supports",
                    exact_witness=witness,
                    exact_method=(
                        "exact rational segment intersection in (b=e_B,a=e_A); "
                        "X identifies b, W identifies a, c=1-a-b"
                    ),
                    minimum_represented_xw_l2=numerical.minimum_xw_l2,
                    minimum_represented_five_component_rms=(
                        numerical.minimum_five_component_rms
                    ),
                    interpretation=_alias_interpretation(left, right, intersects),
                )
            )
    return tuple(result)


__all__ = [
    "EXACT_GEOMETRY_TOLERANCE",
    "FORWARD_REGRESSION_TOLERANCE",
    "PHASE2A_EXACT_ALIAS_PAIRS",
    "Phase2AForwardRegression",
    "XW_BLOCKS",
    "XWAlgebraDiagnostic",
    "XWExactAlias",
    "XWObservableMIDClass",
    "XWPairwiseGeometry",
    "XWPanelConstruction",
    "construct_xw_panel",
    "exact_xw_aliases",
    "pairwise_xw_geometry",
    "regress_against_phase2a_artifacts",
    "verify_xw_coordinate_algebra",
]
