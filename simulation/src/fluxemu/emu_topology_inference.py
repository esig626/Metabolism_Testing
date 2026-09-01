"""Small observable-law minimax proof for the explicit Phase 2A EMU motif."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence

import numpy as np

from .composite_mid_minimax import (
    ContinuousRepresentationUnavailable,
    ImportanceDiscretization,
    ProductDirichletFamily,
    family_from_mid_class,
)
from .composite_multihypothesis import (
    FiniteMultihypothesisSolution,
    MulticlassProposalSupport,
    build_balanced_proposal_support,
    build_continuous_multiclass_rule,
    discretize_families,
    solve_finite_minimax,
)
from .emu_topology_edge_reconstruction import (
    DEFAULT_WEIGHT_POINT_COUNT,
    MASTER_SEED,
    R_MEAS,
    SUPPORT_LABELS,
    ForwardAliasDiagnostic,
    ForwardGeneratedClasses,
    ObservableMIDClass,
    PairwiseObservableGeometry,
    SupportClassMetadata,
    generate_forward_classes,
    pairwise_observable_geometry,
    verify_declared_forward_aliases,
)
from .multiclass_rule_column_generation import (
    RuleColumnGenerationSolution,
    solve_rule_column_generation,
)


OBSERVATION_SUPPORT_SIZE = 3_000
RULE_COLUMN_TOLERANCE = 2.0e-7
RULE_COLUMN_MAXIMUM_ITERATIONS = 500
COMPATIBILITY_RMS_RADIUS = R_MEAS
EXACT_ALIAS_LOWER_BOUND = 2.0 / 3.0
GENERATING_CLASS_INDEX = 0
GENERATING_MEMBER_INDEX = 0


def build_observable_families(
    observable_classes: Sequence[ObservableMIDClass],
    *,
    rms_noise: float = R_MEAS,
) -> tuple[ProductDirichletFamily, ...]:
    """Cross only observed MID fields into the established measurement model."""

    items = tuple(observable_classes)
    if len(items) != len(SUPPORT_LABELS):
        raise ValueError("all six observable classes are required")
    return tuple(
        family_from_mid_class(item, rms_noise=float(rms_noise)) for item in items
    )


@dataclass(frozen=True)
class ObservableMinimaxSolution:
    """Numerical objects produced solely from observable Dirichlet families."""

    families: tuple[ProductDirichletFamily, ...]
    support: MulticlassProposalSupport
    discretizations: tuple[ImportanceDiscretization, ...]
    column_solution: RuleColumnGenerationSolution
    direct_solution: FiniteMultihypothesisSolution
    continuous_rule_available: bool
    continuous_rule_reason: str
    minimum_effective_sample_size: float
    maximum_absolute_raw_mass_error: float

    @property
    def finite_lower_bound(self) -> float:
        return max(
            EXACT_ALIAS_LOWER_BOUND,
            float(self.column_solution.dual_lower_bound),
        )

    @property
    def finite_upper_bound(self) -> float:
        return float(self.column_solution.primal_upper_bound)


def solve_observable_minimax(
    families: Sequence[ProductDirichletFamily],
    *,
    support_size: int = OBSERVATION_SUPPORT_SIZE,
    seed: int = MASTER_SEED,
) -> ObservableMinimaxSolution:
    """Solve the existing K-way memberwise minimax problem on one support."""

    family_items = tuple(families)
    if len(family_items) != len(SUPPORT_LABELS):
        raise ValueError("all six observable-law families are required")
    support = build_balanced_proposal_support(
        family_items,
        support_size=int(support_size),
        seed=int(seed),
        class_labels=SUPPORT_LABELS,
    )
    discretizations = discretize_families(family_items, support)
    probability_rows = tuple(item.weights for item in discretizations)
    column = solve_rule_column_generation(
        probability_rows,
        class_labels=SUPPORT_LABELS,
        convergence_tolerance=RULE_COLUMN_TOLERANCE,
        maximum_iterations=RULE_COLUMN_MAXIMUM_ITERATIONS,
    )
    direct = solve_finite_minimax(
        probability_rows,
        class_labels=SUPPORT_LABELS,
    )

    continuous_available = False
    continuous_reason = "not attempted"
    try:
        continuous = build_continuous_multiclass_rule(
            direct,
            family_items,
            discretizations,
            support,
            reproduction_tolerance=7.5e-4,
        )
    except ContinuousRepresentationUnavailable as error:
        continuous_reason = str(error)
    else:
        continuous_available = bool(continuous.stable_on_finite_support)
        continuous_reason = (
            "finite-support reproduction passed"
            if continuous_available
            else "finite-support reproduction failed"
        )

    minimum_ess = min(
        float(np.min(item.effective_sample_sizes)) for item in discretizations
    )
    maximum_mass_error = max(
        float(np.max(np.abs(item.raw_mass_estimates - 1.0)))
        for item in discretizations
    )
    return ObservableMinimaxSolution(
        families=family_items,
        support=support,
        discretizations=discretizations,
        column_solution=column,
        direct_solution=direct,
        continuous_rule_available=continuous_available,
        continuous_rule_reason=continuous_reason,
        minimum_effective_sample_size=minimum_ess,
        maximum_absolute_raw_mass_error=maximum_mass_error,
    )


@dataclass(frozen=True)
class EMUTopologyReconstruction:
    """Forward construction plus the separately solved observable-law problem."""

    generated_classes: ForwardGeneratedClasses
    aliases: tuple[ForwardAliasDiagnostic, ...]
    pairwise_geometry: tuple[PairwiseObservableGeometry, ...]
    minimax: ObservableMinimaxSolution


def run_emu_topology_reconstruction(
    *,
    weight_point_count: int = DEFAULT_WEIGHT_POINT_COUNT,
    support_size: int = OBSERVATION_SUPPORT_SIZE,
    seed: int = MASTER_SEED,
) -> EMUTopologyReconstruction:
    """Run the frozen small Phase 2A reconstruction without a noise sweep."""

    generated = generate_forward_classes(weight_point_count=weight_point_count)
    aliases = verify_declared_forward_aliases(generated)
    geometry = pairwise_observable_geometry(generated)
    # Only the deliberately narrow observable objects cross this boundary.
    families = build_observable_families(generated.observables, rms_noise=R_MEAS)
    minimax = solve_observable_minimax(
        families,
        support_size=support_size,
        seed=seed,
    )
    return EMUTopologyReconstruction(generated, aliases, geometry, minimax)


@dataclass(frozen=True)
class CompatibleObservableMember:
    """One opaque member retained by the observed-X-only screen."""

    class_index: int
    member_index: int
    member_id: str
    observed_rms_distance: float


@dataclass(frozen=True)
class ObservedCompatibilityScreen:
    """A deterministic centre-distance diagnostic, not a confidence set."""

    observed_mid: np.ndarray
    rms_radius: float
    compatible_members: tuple[CompatibleObservableMember, ...]


def screen_observed_compatibility(
    observed_mid: Sequence[float] | np.ndarray,
    observable_classes: Sequence[ObservableMIDClass],
    *,
    rms_radius: float = COMPATIBILITY_RMS_RADIUS,
) -> ObservedCompatibilityScreen:
    """Retain grid centres using only the selected observed MID block."""

    observed = np.asarray(observed_mid, dtype=float)
    radius = float(rms_radius)
    classes = tuple(observable_classes)
    if observed.shape != (3,) or not np.all(np.isfinite(observed)):
        raise ValueError("the compatibility observation must be one finite X MID")
    if np.any(observed <= 0.0) or not math.isclose(
        float(np.sum(observed)), 1.0, rel_tol=0.0, abs_tol=1.0e-12
    ):
        raise ValueError("the compatibility observation must be a positive X MID")
    if not math.isfinite(radius) or radius < 0.0:
        raise ValueError("the compatibility radius must be finite and nonnegative")
    if len(classes) != len(SUPPORT_LABELS):
        raise ValueError("all six observable classes are required")

    retained: list[CompatibleObservableMember] = []
    for class_index, observable in enumerate(classes):
        distances = np.sqrt(
            np.mean(np.square(observable.exact_mids - observed), axis=1)
        )
        for member_index in np.flatnonzero(distances <= radius + 1.0e-15):
            index = int(member_index)
            retained.append(
                CompatibleObservableMember(
                    class_index=class_index,
                    member_index=index,
                    member_id=observable.member_ids[index],
                    observed_rms_distance=float(distances[index]),
                )
            )
    return ObservedCompatibilityScreen(
        observed_mid=np.array(observed, copy=True),
        rms_radius=radius,
        compatible_members=tuple(retained),
    )


@dataclass(frozen=True)
class WithheldCloudMember:
    """A compatible member after hidden metadata is explicitly rejoined."""

    support_label: str
    member_id: str
    mixing_weight: float | None
    observed_rms_distance: float
    withheld_mid: np.ndarray


@dataclass(frozen=True)
class WithheldEnvelope:
    """Componentwise bounds for one surviving support's generated W MIDs."""

    support_label: str
    member_count: int
    minimum_mid: np.ndarray
    maximum_mid: np.ndarray


@dataclass(frozen=True)
class WithheldPrediction:
    """Observed-compatible W cloud, envelopes, and generating-state check."""

    generating_support: str
    generating_member_id: str
    generating_true_withheld_mid: np.ndarray
    compatibility: ObservedCompatibilityScreen
    cloud: tuple[WithheldCloudMember, ...]
    envelopes: tuple[WithheldEnvelope, ...]
    generating_mid_inside_cloud: bool


def rejoin_withheld_predictions(
    compatibility: ObservedCompatibilityScreen,
    construction_metadata: Sequence[SupportClassMetadata],
    *,
    generating_class_index: int,
    generating_member_index: int,
) -> WithheldPrediction:
    """Join W predictions only after the observed-only screen has finished."""

    metadata = tuple(construction_metadata)
    if len(metadata) != len(SUPPORT_LABELS):
        raise ValueError("all six construction metadata records are required")
    generating_hidden = metadata[int(generating_class_index)]
    generating_member_id = generating_hidden.member_ids[int(generating_member_index)]
    true_mid = np.asarray(
        generating_hidden.withheld_mids[int(generating_member_index)], dtype=float
    )

    cloud: list[WithheldCloudMember] = []
    for retained in compatibility.compatible_members:
        hidden = metadata[retained.class_index]
        if hidden.member_ids[retained.member_index] != retained.member_id:
            raise ValueError("observable and construction member IDs do not align")
        mixing_weight = (
            None
            if hidden.mixing_weights is None
            else float(hidden.mixing_weights[retained.member_index])
        )
        withheld = np.array(
            hidden.withheld_mids[retained.member_index], dtype=float, copy=True
        )
        withheld.setflags(write=False)
        cloud.append(
            WithheldCloudMember(
                support_label=hidden.support_label,
                member_id=retained.member_id,
                mixing_weight=mixing_weight,
                observed_rms_distance=retained.observed_rms_distance,
                withheld_mid=withheld,
            )
        )

    envelopes: list[WithheldEnvelope] = []
    for support_label in SUPPORT_LABELS:
        rows = [item.withheld_mid for item in cloud if item.support_label == support_label]
        if not rows:
            continue
        values = np.asarray(rows, dtype=float)
        minimum = np.min(values, axis=0)
        maximum = np.max(values, axis=0)
        minimum.setflags(write=False)
        maximum.setflags(write=False)
        envelopes.append(
            WithheldEnvelope(
                support_label=support_label,
                member_count=len(values),
                minimum_mid=minimum,
                maximum_mid=maximum,
            )
        )

    inside = any(
        np.allclose(item.withheld_mid, true_mid, rtol=0.0, atol=1.0e-12)
        for item in cloud
    )
    true_mid = np.array(true_mid, copy=True)
    true_mid.setflags(write=False)
    return WithheldPrediction(
        generating_support=generating_hidden.support_label,
        generating_member_id=generating_member_id,
        generating_true_withheld_mid=true_mid,
        compatibility=compatibility,
        cloud=tuple(cloud),
        envelopes=tuple(envelopes),
        generating_mid_inside_cloud=inside,
    )


def run_withheld_prediction(
    reconstruction: EMUTopologyReconstruction,
    *,
    generating_class_index: int = GENERATING_CLASS_INDEX,
    generating_member_index: int = GENERATING_MEMBER_INDEX,
    rms_radius: float = COMPATIBILITY_RMS_RADIUS,
) -> WithheldPrediction:
    """Run one synthetic validation with W absent from the compatibility step."""

    generated = reconstruction.generated_classes
    observed = generated.observables[int(generating_class_index)].exact_mids[
        int(generating_member_index)
    ]
    compatibility = screen_observed_compatibility(
        observed,
        generated.observables,
        rms_radius=rms_radius,
    )
    return rejoin_withheld_predictions(
        compatibility,
        generated.metadata,
        generating_class_index=generating_class_index,
        generating_member_index=generating_member_index,
    )


@dataclass(frozen=True)
class NextMeasurementDiagnostic:
    """Whether surviving supports make materially different withheld predictions."""

    potentially_helpful: bool
    support_pairs_with_different_predictions: tuple[tuple[str, str], ...]
    maximum_cross_support_rms_difference: float
    comparison_threshold: float


def next_measurement_diagnostic(
    prediction: WithheldPrediction,
    *,
    rms_difference_threshold: float = R_MEAS,
) -> NextMeasurementDiagnostic:
    """Compare surviving W clouds; this is not a panel optimizer."""

    threshold = float(rms_difference_threshold)
    if not math.isfinite(threshold) or threshold < 0.0:
        raise ValueError("the withheld comparison threshold must be nonnegative")
    by_support = {
        support_label: np.asarray(
            [
                item.withheld_mid
                for item in prediction.cloud
                if item.support_label == support_label
            ],
            dtype=float,
        )
        for support_label in SUPPORT_LABELS
        if any(item.support_label == support_label for item in prediction.cloud)
    }
    labels = tuple(by_support)
    differing: list[tuple[str, str]] = []
    maximum = 0.0
    for left_index in range(len(labels)):
        for right_index in range(left_index + 1, len(labels)):
            left_label = labels[left_index]
            right_label = labels[right_index]
            differences = (
                by_support[left_label][:, np.newaxis, :]
                - by_support[right_label][np.newaxis, :, :]
            )
            pair_maximum = float(
                np.max(np.sqrt(np.mean(np.square(differences), axis=2)))
            )
            maximum = max(maximum, pair_maximum)
            if pair_maximum > threshold:
                differing.append((left_label, right_label))
    return NextMeasurementDiagnostic(
        potentially_helpful=bool(differing),
        support_pairs_with_different_predictions=tuple(differing),
        maximum_cross_support_rms_difference=maximum,
        comparison_threshold=threshold,
    )


__all__ = [
    "COMPATIBILITY_RMS_RADIUS",
    "CompatibleObservableMember",
    "EMUTopologyReconstruction",
    "EXACT_ALIAS_LOWER_BOUND",
    "GENERATING_CLASS_INDEX",
    "GENERATING_MEMBER_INDEX",
    "NextMeasurementDiagnostic",
    "OBSERVATION_SUPPORT_SIZE",
    "ObservableMinimaxSolution",
    "ObservedCompatibilityScreen",
    "RULE_COLUMN_MAXIMUM_ITERATIONS",
    "RULE_COLUMN_TOLERANCE",
    "WithheldCloudMember",
    "WithheldEnvelope",
    "WithheldPrediction",
    "build_observable_families",
    "next_measurement_diagnostic",
    "rejoin_withheld_predictions",
    "run_emu_topology_reconstruction",
    "run_withheld_prediction",
    "screen_observed_compatibility",
    "solve_observable_minimax",
]
