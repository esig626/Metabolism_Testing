"""Directed pairwise Renyi diagnostics for the three-edge topology motif.

The primary topology benchmark is a K-way minimax classification problem.
The calculations here are deliberately narrower diagnostics: for an ordered
pair of observable-law classes ``(i, j)`` they numerically evaluate

``inf_{P_i in class i, P_j in class j} D_lambda(P_j || P_i)``.

The order is not cosmetic.  ``P_j`` is the first (``Q``) argument of the
analytic product-Dirichlet divergence and therefore receives weight
``lambda``.  The KL diagnostic has the same ``KL(P_j || P_i)`` orientation.
Pairwise divergences do not solve the K-way minimax decision problem and no
decision rule is constructed in this module.

Nuisance coordinates enter only the offline bounded separation search.  The
corresponding law at every point is obtained from the observable X MID using
the repository's controlled Dirichlet RMS convention.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
import math
from typing import Sequence

import numpy as np
from scipy.optimize import differential_evolution

from . import composite_mid_renyi as renyi
from .composite_mid_minimax import dirichlet_rms_kappa
from . import topology_three_edge_motif as motif


REPRESENTATIVE_RENYI_ORDERS = (0.1, 0.5, 0.9)
DEFAULT_R_MEAS = 0.005
DEFAULT_INTERSECTION_TOLERANCE = motif.EXACT_ALIAS_ABSOLUTE_TOLERANCE
DEFAULT_SEED = 49_003


class TopologyRenyiNumericalError(RuntimeError):
    """Raised when a directed topology separation search is invalid."""


def _validate_order(order: float | None) -> float | None:
    if order is None:
        return None
    value = float(order)
    if not math.isfinite(value) or not 0.0 < value < 1.0:
        raise ValueError("Renyi order must lie strictly inside (0, 1)")
    return value


def _coordinate_names(topology_label: str) -> tuple[str, ...]:
    return (
        ("theta",)
        if len(motif.topology_sources(topology_label)) == 1
        else ("theta", "w")
    )


def _coordinate_bounds(topology_label: str) -> tuple[tuple[float, float], ...]:
    result = [(motif.THETA_LOWER, motif.THETA_UPPER)]
    if len(motif.topology_sources(topology_label)) == 2:
        result.append((motif.WEIGHT_LOWER, motif.WEIGHT_UPPER))
    return tuple(result)


def _validated_coordinates(
    topology_label: str, coordinates: Sequence[float]
) -> tuple[float, ...]:
    values = tuple(float(value) for value in coordinates)
    bounds = _coordinate_bounds(topology_label)
    if len(values) != len(bounds) or any(not math.isfinite(value) for value in values):
        raise ValueError(
            f"{topology_label} coordinates must be finite and ordered as "
            f"{_coordinate_names(topology_label)}"
        )
    if any(
        value < lower or value > upper
        for value, (lower, upper) in zip(values, bounds, strict=True)
    ):
        raise ValueError(f"{topology_label} coordinates leave their bounded domain")
    return values


def topology_mid_at_coordinates(
    benchmark_id: str,
    topology_label: str,
    coordinates: Sequence[float],
) -> np.ndarray:
    """Evaluate one observable MID from a consistently ordered coordinate tuple."""

    values = _validated_coordinates(topology_label, coordinates)
    weight = values[1] if len(values) == 2 else None
    return motif.topology_mid(benchmark_id, topology_label, values[0], weight)


def topology_dirichlet_alpha(
    benchmark_id: str,
    topology_label: str,
    coordinates: Sequence[float],
    *,
    rms_noise: float = DEFAULT_R_MEAS,
) -> np.ndarray:
    """Map one exact observable MID to its controlled Dirichlet parameters."""

    centre = topology_mid_at_coordinates(
        benchmark_id, topology_label, coordinates
    )
    concentration = dirichlet_rms_kappa(centre, float(rms_noise))
    alpha = np.asarray(concentration * centre, dtype=float)
    if not np.all(np.isfinite(alpha)) or np.any(alpha <= 0.0):
        raise TopologyRenyiNumericalError("invalid topology Dirichlet parameters")
    alpha.setflags(write=False)
    return alpha


def directed_member_divergence(
    benchmark_id: str,
    base_class_id: str,
    base_coordinates: Sequence[float],
    directed_class_id: str,
    directed_coordinates: Sequence[float],
    *,
    rms_noise: float = DEFAULT_R_MEAS,
    order: float | None,
) -> float:
    """Evaluate ``D_lambda(P_j || P_i)`` or ``KL(P_j || P_i)``.

    ``base_class_id`` denotes class ``i`` and supplies the second analytic
    argument.  ``directed_class_id`` denotes class ``j`` and supplies the
    first analytic argument.
    """

    lam = _validate_order(order)
    alpha_p_i = topology_dirichlet_alpha(
        benchmark_id, base_class_id, base_coordinates, rms_noise=rms_noise
    )
    alpha_q_j = topology_dirichlet_alpha(
        benchmark_id,
        directed_class_id,
        directed_coordinates,
        rms_noise=rms_noise,
    )
    if lam is None:
        return renyi.product_dirichlet_kl_divergence(
            alpha_q_j, alpha_p_i, (len(alpha_p_i),)
        )
    return renyi.product_dirichlet_renyi_divergence(
        alpha_q_j, alpha_p_i, (len(alpha_p_i),), lam
    )


@dataclass(frozen=True)
class ExactIntersectionWitness:
    """A construction-level shared-law witness for two topology labels."""

    benchmark_id: str
    left_class_id: str
    right_class_id: str
    left_coordinate_names: tuple[str, ...]
    right_coordinate_names: tuple[str, ...]
    left_coordinates: tuple[float, ...]
    right_coordinates: tuple[float, ...]
    relation: str
    maximum_absolute_mid_error: float
    l2_mid_error: float
    verification_tolerance: float
    verified: bool


def exact_intersection_witness(
    benchmark_id: str,
    left_class_id: str,
    right_class_id: str,
    *,
    theta: float = 0.5,
    verification_tolerance: float = DEFAULT_INTERSECTION_TOLERANCE,
) -> ExactIntersectionWitness | None:
    """Return and verify a declared analytic intersection witness, if known.

    T0 supplies a witness for every ordered pair.  T2 supplies the required
    C/AB witness and the additional AB/AC and AB/BC overlap witnesses.  The
    returned orientation matches the requested labels; reversing a pair swaps
    its coordinates rather than relying on an implicit symmetry argument.
    """

    benchmark_id = motif.benchmark_definition(benchmark_id).benchmark_id
    left_class_id = str(left_class_id)
    right_class_id = str(right_class_id)
    motif.topology_sources(left_class_id)
    motif.topology_sources(right_class_id)
    theta_value = float(theta)
    if not math.isfinite(theta_value) or not 0.0 <= theta_value <= 1.0:
        raise ValueError("intersection-witness theta must lie in [0, 1]")
    tolerance = float(verification_tolerance)
    if not math.isfinite(tolerance) or tolerance < 0.0:
        raise ValueError("intersection-witness tolerance must be nonnegative")

    def common_coordinates(topology_label: str) -> tuple[float, ...]:
        return (
            (theta_value,)
            if len(motif.topology_sources(topology_label)) == 1
            else (theta_value, 0.5)
        )

    relation: str | None = None
    coordinates_by_class: dict[str, tuple[float, ...]] = {}
    if left_class_id == right_class_id:
        coordinates_by_class[left_class_id] = common_coordinates(left_class_id)
        relation = "identical topology member"
    elif benchmark_id == "T0":
        coordinates_by_class = {
            left_class_id: common_coordinates(left_class_id),
            right_class_id: common_coordinates(right_class_id),
        }
        relation = "T0 common source family at matched theta"
    elif benchmark_id == "T2":
        pair = frozenset((left_class_id, right_class_id))
        if pair == frozenset(("G_C", "G_AB")):
            coordinates_by_class = {
                "G_C": (theta_value,),
                "G_AB": (theta_value, 0.5),
            }
            relation = "G_C(theta) = G_AB(theta, w=0.5)"
        elif pair == frozenset(("G_AB", "G_AC")):
            coordinates_by_class = {
                "G_AB": (theta_value, 0.7),
                "G_AC": (theta_value, 0.4),
            }
            relation = "G_AB(theta, w=0.7) = G_AC(theta, w=0.4)"
        elif pair == frozenset(("G_AB", "G_BC")):
            coordinates_by_class = {
                "G_AB": (theta_value, 0.3),
                "G_BC": (theta_value, 0.4),
            }
            relation = "G_AB(theta, w=0.3) = G_BC(theta, w=0.4)"
    if relation is None:
        return None

    left_coordinates = coordinates_by_class[left_class_id]
    right_coordinates = coordinates_by_class[right_class_id]
    left_mid = topology_mid_at_coordinates(
        benchmark_id, left_class_id, left_coordinates
    )
    right_mid = topology_mid_at_coordinates(
        benchmark_id, right_class_id, right_coordinates
    )
    difference = np.asarray(left_mid - right_mid, dtype=float)
    maximum_absolute = float(np.max(np.abs(difference)))
    l2_error = float(np.linalg.norm(difference))
    verified = maximum_absolute <= tolerance
    if not verified:
        raise TopologyRenyiNumericalError(
            f"declared exact intersection {left_class_id}/{right_class_id} "
            f"failed at {maximum_absolute:.12g}"
        )
    return ExactIntersectionWitness(
        benchmark_id=benchmark_id,
        left_class_id=left_class_id,
        right_class_id=right_class_id,
        left_coordinate_names=_coordinate_names(left_class_id),
        right_coordinate_names=_coordinate_names(right_class_id),
        left_coordinates=left_coordinates,
        right_coordinates=right_coordinates,
        relation=relation,
        maximum_absolute_mid_error=maximum_absolute,
        l2_mid_error=l2_error,
        verification_tolerance=tolerance,
        verified=True,
    )


@dataclass(frozen=True)
class DirectedCompositeSeparation:
    """One bounded directed composite Renyi or KL minimisation result."""

    benchmark_id: str
    base_class_id: str
    directed_class_id: str
    orientation: str
    divergence_kind: str
    order: float | None
    divergence: float
    rms_noise: float
    base_coordinate_names: tuple[str, ...]
    directed_coordinate_names: tuple[str, ...]
    base_coordinates: tuple[float, ...]
    directed_coordinates: tuple[float, ...]
    optimizer_success: bool
    optimizer_message: str
    function_evaluations: int
    seed: int
    exact_zero_witness_used: bool
    witness_relation: str | None
    witness_maximum_absolute_mid_error: float | None
    claim_type: str

    def __post_init__(self) -> None:
        lam = _validate_order(self.order)
        kind = str(self.divergence_kind)
        if (lam is None and kind != "KL") or (lam is not None and kind != "Renyi"):
            raise ValueError("divergence kind and order are inconsistent")
        divergence = float(self.divergence)
        if not math.isfinite(divergence) or divergence < 0.0:
            raise ValueError("directed separation must be finite and nonnegative")
        expected_orientation = "KL(P_j || P_i)" if lam is None else "D(P_j || P_i)"
        if self.orientation != expected_orientation:
            raise ValueError("directed-separation orientation is inconsistent")
        _validated_coordinates(self.base_class_id, self.base_coordinates)
        _validated_coordinates(self.directed_class_id, self.directed_coordinates)
        if tuple(self.base_coordinate_names) != _coordinate_names(self.base_class_id):
            raise ValueError("base coordinate names are inconsistent")
        if tuple(self.directed_coordinate_names) != _coordinate_names(self.directed_class_id):
            raise ValueError("directed coordinate names are inconsistent")
        object.__setattr__(self, "order", lam)
        object.__setattr__(self, "divergence", divergence)


def minimise_directed_topology_separation(
    benchmark_id: str,
    base_class_id: str,
    directed_class_id: str,
    *,
    rms_noise: float = DEFAULT_R_MEAS,
    order: float | None,
    seed: int = DEFAULT_SEED,
    maximum_iterations: int = 400,
    population_size: int = 12,
    optimizer_tolerance: float = 1.0e-9,
    exact_witness_tolerance: float = DEFAULT_INTERSECTION_TOLERANCE,
) -> DirectedCompositeSeparation:
    """Minimise ``D(P_j || P_i)`` over both bounded topology classes.

    A verified analytic shared-law witness takes precedence over stochastic
    optimisation and returns the mathematically exact zero.  Every other pair
    uses bounded differential evolution plus explicit corners and the box
    midpoint.  Independent seeds should be used when reporting convergence.
    """

    benchmark_id = motif.benchmark_definition(benchmark_id).benchmark_id
    base_class_id = str(base_class_id)
    directed_class_id = str(directed_class_id)
    motif.topology_sources(base_class_id)
    motif.topology_sources(directed_class_id)
    lam = _validate_order(order)
    noise = float(rms_noise)
    # Validate the measurement convention even when an exact witness lets the
    # numerical optimiser be skipped.
    validation_coordinates = tuple(
        0.5 * (lower + upper) for lower, upper in _coordinate_bounds(base_class_id)
    )
    topology_dirichlet_alpha(
        benchmark_id,
        base_class_id,
        validation_coordinates,
        rms_noise=noise,
    )
    witness = exact_intersection_witness(
        benchmark_id,
        base_class_id,
        directed_class_id,
        verification_tolerance=exact_witness_tolerance,
    )
    divergence_kind = "KL" if lam is None else "Renyi"
    orientation = "KL(P_j || P_i)" if lam is None else "D(P_j || P_i)"
    if witness is not None:
        # Validate both induced alpha vectors.  Tiny floating discrepancies in
        # an analytically equal T2 construction are not fed to a subtractive
        # divergence formula; the verified construction identity is the exact
        # zero certificate.
        topology_dirichlet_alpha(
            benchmark_id,
            base_class_id,
            witness.left_coordinates,
            rms_noise=noise,
        )
        topology_dirichlet_alpha(
            benchmark_id,
            directed_class_id,
            witness.right_coordinates,
            rms_noise=noise,
        )
        return DirectedCompositeSeparation(
            benchmark_id=benchmark_id,
            base_class_id=base_class_id,
            directed_class_id=directed_class_id,
            orientation=orientation,
            divergence_kind=divergence_kind,
            order=lam,
            divergence=0.0,
            rms_noise=noise,
            base_coordinate_names=witness.left_coordinate_names,
            directed_coordinate_names=witness.right_coordinate_names,
            base_coordinates=witness.left_coordinates,
            directed_coordinates=witness.right_coordinates,
            optimizer_success=True,
            optimizer_message="verified exact construction witness",
            function_evaluations=0,
            seed=int(seed),
            exact_zero_witness_used=True,
            witness_relation=witness.relation,
            witness_maximum_absolute_mid_error=witness.maximum_absolute_mid_error,
            claim_type="mathematically exact shared observable law",
        )

    base_bounds = _coordinate_bounds(base_class_id)
    directed_bounds = _coordinate_bounds(directed_class_id)
    bounds = base_bounds + directed_bounds
    split = len(base_bounds)

    def objective(parameters: np.ndarray) -> float:
        return directed_member_divergence(
            benchmark_id,
            base_class_id,
            parameters[:split],
            directed_class_id,
            parameters[split:],
            rms_noise=noise,
            order=lam,
        )

    solution = differential_evolution(
        objective,
        bounds,
        seed=int(seed),
        maxiter=int(maximum_iterations),
        popsize=int(population_size),
        tol=float(optimizer_tolerance),
        atol=1.0e-12,
        polish=True,
        updating="immediate",
        workers=1,
    )
    candidates: list[tuple[float, np.ndarray, str]] = [
        (
            float(solution.fun),
            np.asarray(solution.x, dtype=float),
            "differential-evolution solution",
        )
    ]
    for corner in product(*[(lower, upper) for lower, upper in bounds]):
        point = np.asarray(corner, dtype=float)
        candidates.append((float(objective(point)), point, "explicit box corner"))
    midpoint = np.asarray(
        [0.5 * (lower + upper) for lower, upper in bounds], dtype=float
    )
    candidates.append((float(objective(midpoint)), midpoint, "explicit box midpoint"))
    best_value, best_point, selected_candidate = min(
        candidates, key=lambda item: (item[0], *item[1])
    )
    if best_value < -1.0e-10 or not math.isfinite(best_value):
        raise TopologyRenyiNumericalError("directed separation optimiser returned an invalid value")
    return DirectedCompositeSeparation(
        benchmark_id=benchmark_id,
        base_class_id=base_class_id,
        directed_class_id=directed_class_id,
        orientation=orientation,
        divergence_kind=divergence_kind,
        order=lam,
        divergence=max(0.0, float(best_value)),
        rms_noise=noise,
        base_coordinate_names=_coordinate_names(base_class_id),
        directed_coordinate_names=_coordinate_names(directed_class_id),
        base_coordinates=tuple(float(value) for value in best_point[:split]),
        directed_coordinates=tuple(float(value) for value in best_point[split:]),
        optimizer_success=bool(solution.success),
        optimizer_message=(
            f"{solution.message}; selected candidate: {selected_candidate}"
        ),
        function_evaluations=int(solution.nfev) + len(candidates) - 1,
        seed=int(seed),
        exact_zero_witness_used=False,
        witness_relation=None,
        witness_maximum_absolute_mid_error=None,
        claim_type=(
            "numerical candidate upper bound on the directed composite infimum; "
            "not a certified positive separation"
        ),
    )


@dataclass(frozen=True)
class DirectedSeparationMatrix:
    """A generic K-by-K matrix in caller-declared class order."""

    benchmark_id: str
    class_labels: tuple[str, ...]
    divergence_kind: str
    order: float | None
    orientation: str
    values: np.ndarray
    pair_results: tuple[DirectedCompositeSeparation, ...]

    def __post_init__(self) -> None:
        labels = tuple(str(value) for value in self.class_labels)
        lam = _validate_order(self.order)
        expected_kind = "KL" if lam is None else "Renyi"
        expected_orientation = "KL(P_j || P_i)" if lam is None else "D(P_j || P_i)"
        if self.divergence_kind != expected_kind or self.orientation != expected_orientation:
            raise ValueError("directed matrix metric metadata are inconsistent")
        if not labels or len(set(labels)) != len(labels):
            raise ValueError("directed matrix class labels must be nonempty and unique")
        values = np.array(self.values, dtype=float, copy=True)
        if values.shape != (len(labels), len(labels)):
            raise ValueError("directed separation matrix has the wrong shape")
        if not np.all(np.isfinite(values)) or np.any(values < 0.0):
            raise ValueError("directed separation matrix contains invalid values")
        if len(self.pair_results) != len(labels) ** 2:
            raise ValueError("directed separation pair results are incomplete")
        for base_index, base_class_id in enumerate(labels):
            for directed_index, directed_class_id in enumerate(labels):
                result = self.pair_results[
                    base_index * len(labels) + directed_index
                ]
                if (
                    result.base_class_id != base_class_id
                    or result.directed_class_id != directed_class_id
                    or result.order != lam
                ):
                    raise ValueError("directed separation pair ordering is inconsistent")
        if not np.array_equal(np.diag(values), np.zeros(len(labels))):
            raise ValueError("directed separation matrix diagonal must be exact zero")
        values.setflags(write=False)
        object.__setattr__(self, "class_labels", labels)
        object.__setattr__(self, "values", values)

    def result(self, base_class_id: str, directed_class_id: str) -> DirectedCompositeSeparation:
        """Return the row-major result for matrix entry ``(i, j)``."""

        base_index = self.class_labels.index(str(base_class_id))
        directed_index = self.class_labels.index(str(directed_class_id))
        return self.pair_results[base_index * len(self.class_labels) + directed_index]


def directed_topology_separation_matrix(
    benchmark_id: str,
    *,
    class_labels: Sequence[str] = motif.TOPOLOGY_LABELS,
    rms_noise: float = DEFAULT_R_MEAS,
    order: float | None,
    seed: int = DEFAULT_SEED,
    maximum_iterations: int = 400,
    population_size: int = 12,
    optimizer_tolerance: float = 1.0e-9,
) -> DirectedSeparationMatrix:
    """Compute a generic directed K-by-K composite separation matrix.

    Matrix row ``i`` and column ``j`` contain ``D(P_j || P_i)``.  The proposal
    or topology frequency has no role in this deterministic diagnostic.
    """

    labels = tuple(str(value) for value in class_labels)
    if not labels or len(set(labels)) != len(labels):
        raise ValueError("class labels must be nonempty and unique")
    for label in labels:
        motif.topology_sources(label)
    lam = _validate_order(order)
    results: list[DirectedCompositeSeparation] = []
    values = np.empty((len(labels), len(labels)), dtype=float)
    for base_index, base_class_id in enumerate(labels):
        for directed_index, directed_class_id in enumerate(labels):
            pair_seed = int(seed) + base_index * len(labels) + directed_index
            result = minimise_directed_topology_separation(
                benchmark_id,
                base_class_id,
                directed_class_id,
                rms_noise=rms_noise,
                order=lam,
                seed=pair_seed,
                maximum_iterations=maximum_iterations,
                population_size=population_size,
                optimizer_tolerance=optimizer_tolerance,
            )
            values[base_index, directed_index] = result.divergence
            results.append(result)
    return DirectedSeparationMatrix(
        benchmark_id=str(benchmark_id),
        class_labels=labels,
        divergence_kind="KL" if lam is None else "Renyi",
        order=lam,
        orientation="KL(P_j || P_i)" if lam is None else "D(P_j || P_i)",
        values=values,
        pair_results=tuple(results),
    )


def representative_directed_topology_matrices(
    benchmark_id: str,
    *,
    class_labels: Sequence[str] = motif.TOPOLOGY_LABELS,
    rms_noise: float = DEFAULT_R_MEAS,
    seed: int = DEFAULT_SEED,
    maximum_iterations: int = 400,
    population_size: int = 12,
) -> tuple[DirectedSeparationMatrix, ...]:
    """Return matrices for orders 0.1, 0.5, 0.9 and the directed KL limit."""

    metrics: tuple[float | None, ...] = (*REPRESENTATIVE_RENYI_ORDERS, None)
    return tuple(
        directed_topology_separation_matrix(
            benchmark_id,
            class_labels=class_labels,
            rms_noise=rms_noise,
            order=order,
            seed=int(seed) + metric_index * 10_000,
            maximum_iterations=maximum_iterations,
            population_size=population_size,
        )
        for metric_index, order in enumerate(metrics)
    )


def directed_topology_separation_curve(
    benchmark_id: str,
    base_class_id: str,
    directed_class_id: str,
    orders: Sequence[float],
    *,
    rms_noise: float = DEFAULT_R_MEAS,
    seed: int = DEFAULT_SEED,
    maximum_iterations: int = 400,
    population_size: int = 12,
) -> tuple[DirectedCompositeSeparation, ...]:
    """Retain a directed Renyi separation curve for one selected hard pair."""

    order_values = tuple(_validate_order(value) for value in orders)
    if not order_values:
        raise ValueError("a separation curve needs at least one order")
    return tuple(
        minimise_directed_topology_separation(
            benchmark_id,
            base_class_id,
            directed_class_id,
            rms_noise=rms_noise,
            order=order,
            seed=int(seed) + index,
            maximum_iterations=maximum_iterations,
            population_size=population_size,
        )
        for index, order in enumerate(order_values)
    )
