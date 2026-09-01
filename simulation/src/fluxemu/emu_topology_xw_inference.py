"""Frozen-scale K-way minimax confirmation for the Phase 2B X+W panel."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping, Sequence

import numpy as np

from .composite_mid_minimax import (
    ContinuousRepresentationUnavailable,
    ImportanceDiscretization,
    ProductDirichletFamily,
    family_from_mid_class,
)
from .composite_multihypothesis import (
    ContinuousMulticlassDecisionRule,
    ContinuousMulticlassDiagnostics,
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
    OBSERVED_TARGET_ID,
    R_MEAS,
    SUPPORT_LABELS,
    WEIGHT_LOWER,
    WEIGHT_UPPER,
    WITHHELD_TARGET_ID,
    SupportFluxStates,
    build_forward_system,
    construct_support_flux_states,
    mixing_weight_grid,
    run_forward_states,
    support_edges,
)
from .emu_topology_inference import (
    OBSERVATION_SUPPORT_SIZE,
    RULE_COLUMN_MAXIMUM_ITERATIONS,
    RULE_COLUMN_TOLERANCE,
)
from .emu_topology_xw_panel import (
    Phase2AForwardRegression,
    XWAlgebraDiagnostic,
    XW_BLOCKS,
    XWExactAlias,
    XWObservableMIDClass,
    XWPairwiseGeometry,
    XWPanelConstruction,
    construct_xw_panel,
    exact_xw_aliases,
    pairwise_xw_geometry,
    regress_against_phase2a_artifacts,
    verify_xw_coordinate_algebra,
)
from .multiclass_rule_column_generation import (
    RuleColumnGenerationSolution,
    solve_rule_column_generation,
)


CONTINUOUS_REPRODUCTION_TOLERANCE = 7.5e-4
MATHEMATICAL_NONNEGATIVITY_LOWER_BOUND = 0.0
HELDOUT_PAIR_MEMBER_COUNT = 4
HELDOUT_DRAWS_PER_MEMBER = 200
HELDOUT_SEED = MASTER_SEED + 1
HELDOUT_PAIR_WEIGHTS = (0.275, 0.425, 0.575, 0.725)


def build_xw_observable_families(
    observable_classes: Sequence[XWObservableMIDClass],
    *,
    rms_noise: float = R_MEAS,
) -> tuple[ProductDirichletFamily, ...]:
    """Cross only opaque X+W MID objects into the established noise model."""

    items = tuple(observable_classes)
    if len(items) != len(SUPPORT_LABELS):
        raise ValueError("all six X+W observable classes are required")
    families = tuple(
        family_from_mid_class(item, rms_noise=float(rms_noise)) for item in items
    )
    _validate_frozen_xw_families(families)
    return families


def _validate_frozen_xw_families(
    families: Sequence[ProductDirichletFamily],
) -> tuple[ProductDirichletFamily, ...]:
    items = tuple(families)
    if len(items) != len(SUPPORT_LABELS):
        raise ValueError("all six X+W observable-law families are required")
    for family in items:
        if (
            family.block_names != ("X_full", "W_full")
            or family.block_sizes != (3, 2)
            or family.observation_dimension != 5
            or not np.isclose(family.rms_noise, R_MEAS, rtol=0.0, atol=1.0e-15)
        ):
            raise ValueError(
                "Phase 2B requires frozen X_full/W_full product laws at r_meas=0.005"
            )
    return items


@dataclass(frozen=True)
class XWMinimaxSolution:
    """Finite common-support solution and optional dual-density rule."""

    families: tuple[ProductDirichletFamily, ...]
    support: MulticlassProposalSupport
    discretizations: tuple[ImportanceDiscretization, ...]
    column_solution: RuleColumnGenerationSolution
    direct_solution: FiniteMultihypothesisSolution
    continuous_diagnostics: ContinuousMulticlassDiagnostics | None
    continuous_rule_reason: str
    minimum_effective_sample_size: float
    maximum_absolute_raw_mass_error: float

    @property
    def finite_lower_bound(self) -> float:
        return max(
            MATHEMATICAL_NONNEGATIVITY_LOWER_BOUND,
            float(self.column_solution.dual_lower_bound),
        )

    @property
    def finite_upper_bound(self) -> float:
        return float(self.column_solution.primal_upper_bound)

    @property
    def certificate_gap(self) -> float:
        return self.finite_upper_bound - self.finite_lower_bound

    @property
    def continuous_rule_available(self) -> bool:
        return bool(
            self.continuous_diagnostics is not None
            and self.continuous_diagnostics.stable_on_finite_support
        )


def solve_xw_observable_minimax(
    families: Sequence[ProductDirichletFamily],
    *,
    support_size: int = OBSERVATION_SUPPORT_SIZE,
    seed: int = MASTER_SEED,
) -> XWMinimaxSolution:
    """Reuse the Phase 2A-scale K-way common-support minimax calculation."""

    family_items = _validate_frozen_xw_families(families)
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

    continuous: ContinuousMulticlassDiagnostics | None = None
    continuous_reason = "not attempted"
    try:
        candidate = build_continuous_multiclass_rule(
            direct,
            family_items,
            discretizations,
            support,
            reproduction_tolerance=CONTINUOUS_REPRODUCTION_TOLERANCE,
        )
    except ContinuousRepresentationUnavailable as error:
        continuous_reason = str(error)
    else:
        continuous = candidate
        if candidate.stable_on_finite_support:
            continuous_reason = "finite-support reproduction gates passed"
        else:
            continuous_reason = "finite-support reproduction gates failed"

    minimum_ess = min(
        float(np.min(item.effective_sample_sizes)) for item in discretizations
    )
    maximum_mass_error = max(
        float(np.max(np.abs(item.raw_mass_estimates - 1.0)))
        for item in discretizations
    )
    return XWMinimaxSolution(
        families=family_items,
        support=support,
        discretizations=discretizations,
        column_solution=column,
        direct_solution=direct,
        continuous_diagnostics=continuous,
        continuous_rule_reason=continuous_reason,
        minimum_effective_sample_size=minimum_ess,
        maximum_absolute_raw_mass_error=maximum_mass_error,
    )


@dataclass(frozen=True)
class XWPanelConfirmation:
    """Complete Phase 2B forward, geometry, and minimax confirmation."""

    panel: XWPanelConstruction
    forward_regression: Phase2AForwardRegression
    algebra: XWAlgebraDiagnostic
    aliases: tuple[XWExactAlias, ...]
    pairwise_geometry: tuple[XWPairwiseGeometry, ...]
    minimax: XWMinimaxSolution


def run_xw_panel_confirmation(
    phase2a_result_directory: str | Path,
    *,
    weight_point_count: int = DEFAULT_WEIGHT_POINT_COUNT,
    support_size: int = OBSERVATION_SUPPORT_SIZE,
    seed: int = MASTER_SEED,
) -> XWPanelConfirmation:
    """Run the frozen Phase 2B confirmation without changing the experiment."""

    panel = construct_xw_panel(weight_point_count=weight_point_count)
    regression = regress_against_phase2a_artifacts(
        panel, phase2a_result_directory
    )
    algebra = verify_xw_coordinate_algebra(panel)
    aliases = exact_xw_aliases(panel)
    geometry = pairwise_xw_geometry(panel)
    # Only the narrow observable objects cross the inference boundary.
    families = build_xw_observable_families(panel.observables, rms_noise=R_MEAS)
    minimax = solve_xw_observable_minimax(
        families,
        support_size=support_size,
        seed=seed,
    )
    return XWPanelConfirmation(
        panel=panel,
        forward_regression=regression,
        algebra=algebra,
        aliases=aliases,
        pairwise_geometry=geometry,
        minimax=minimax,
    )


def continuous_rule_commitment(
    rule: ContinuousMulticlassDecisionRule,
) -> str:
    """Hash every array and setting that determines continuous decisions."""

    metadata = {
        "version": "fluxemu.phase2b_xw_continuous_rule.v1",
        "class_labels": list(rule.class_labels),
        "tie_log_tolerance": rule.tie_log_tolerance,
        "family_layout": [
            {
                "block_names": list(family.block_names),
                "block_sizes": list(family.block_sizes),
                "member_count": family.member_count,
            }
            for family in rule.class_families
        ],
    }
    digest = hashlib.sha256(
        json.dumps(
            metadata,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    )

    def update_array(label: str, values: np.ndarray) -> None:
        array = np.ascontiguousarray(values)
        framing = json.dumps(
            {"label": label, "dtype": array.dtype.str, "shape": list(array.shape)},
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
        digest.update(framing)
        digest.update(array.tobytes())

    for family, coefficients in zip(
        rule.class_families, rule.density_coefficients, strict=True
    ):
        update_array("alpha_parameters", family.alpha_parameters)
        update_array("log_density_constants", family.log_density_constants)
        update_array("density_coefficients", coefficients)
    return digest.hexdigest()


@dataclass(frozen=True)
class _HeldoutConstruction:
    families: tuple[ProductDirichletFamily, ...]
    states: tuple[SupportFluxStates, ...]
    forward_validation: Mapping[str, Any]


def _off_grid_pair_weights() -> tuple[np.ndarray, ...]:
    """Return symmetric equal-cell midpoints, frozen before any result."""

    frozen = mixing_weight_grid(DEFAULT_WEIGHT_POINT_COUNT)
    values = np.asarray(HELDOUT_PAIR_WEIGHTS, dtype=float)
    if (
        len(values) != HELDOUT_PAIR_MEMBER_COUNT
        or np.any(values <= WEIGHT_LOWER)
        or np.any(values >= WEIGHT_UPPER)
        or np.any(np.isclose(values[:, np.newaxis], frozen, rtol=0.0, atol=1.0e-12))
    ):
        raise RuntimeError("the frozen held-out weights are not strictly off-grid")
    return tuple(np.array(values, copy=True) for _ in range(3))


def _construct_heldout_families(
    *,
    rms_noise: float,
) -> _HeldoutConstruction:
    """Generate off-grid biological centres through the unchanged EMU path."""

    pair_weights = iter(_off_grid_pair_weights())
    system = build_forward_system()
    states: list[SupportFluxStates] = []
    member_offset = 100_000
    for support_label in SUPPORT_LABELS:
        weights = None if len(support_edges(support_label)) == 1 else next(pair_weights)
        state = construct_support_flux_states(
            system.cobra_model,
            support_label,
            weights,
            member_id_offset=member_offset,
            tolerances=system.experiment.tolerances,
        )
        states.append(state)
        member_offset += len(state.member_ids)
    forward = run_forward_states(system, states)
    observable_classes: list[XWObservableMIDClass] = []
    for state in states:
        rows = np.asarray(
            [
                np.concatenate(
                    (
                        forward.predictions[member_id][OBSERVED_TARGET_ID],
                        forward.predictions[member_id][WITHHELD_TARGET_ID],
                    )
                )
                for member_id in state.member_ids
            ],
            dtype=float,
        )
        observable_classes.append(
            XWObservableMIDClass(
                member_ids=state.member_ids,
                blocks=XW_BLOCKS,
                exact_mids=rows,
            )
        )
    families = build_xw_observable_families(
        observable_classes,
        rms_noise=rms_noise,
    )
    return _HeldoutConstruction(
        families=families,
        states=tuple(states),
        forward_validation=MappingProxyType(dict(forward.validation)),
    )


@dataclass(frozen=True)
class HeldoutMemberResult:
    support_label: str
    member_id: str
    mixing_weight: float | None
    trials: int
    errors: int
    error_rate: float


@dataclass(frozen=True)
class HeldoutClassResult:
    support_label: str
    member_count: int
    trials: int
    errors: int
    error_rate: float
    worst_member_error_rate: float


@dataclass(frozen=True)
class XWHeldoutValidation:
    """Small blind Monte Carlo check run only after a rule is committed."""

    status: str
    rule_commitment_sha256: str
    rule_frozen_before_forward_generation: bool
    rule_commitment_verified_after_decisions: bool
    seed: int
    pair_member_count: int
    draws_per_member: int
    total_members: int
    total_trials: int
    total_errors: int
    overall_error_rate: float
    member_results: tuple[HeldoutMemberResult, ...]
    class_results: tuple[HeldoutClassResult, ...]
    confusion: np.ndarray
    forward_validation: Mapping[str, Any]

    def __post_init__(self) -> None:
        confusion = np.array(self.confusion, dtype=int, copy=True)
        if confusion.shape != (len(SUPPORT_LABELS), len(SUPPORT_LABELS)):
            raise ValueError("held-out confusion matrix has an invalid shape")
        if np.any(confusion < 0) or int(np.sum(confusion)) != int(self.total_trials):
            raise ValueError("held-out confusion counts are invalid")
        confusion.setflags(write=False)
        object.__setattr__(self, "confusion", confusion)
        object.__setattr__(
            self,
            "forward_validation",
            MappingProxyType(dict(self.forward_validation)),
        )


def run_blind_xw_heldout_validation(
    confirmation: XWPanelConfirmation,
    *,
    pair_member_count: int = HELDOUT_PAIR_MEMBER_COUNT,
    draws_per_member: int = HELDOUT_DRAWS_PER_MEMBER,
    seed: int = HELDOUT_SEED,
) -> XWHeldoutValidation:
    """Freeze the legitimate MID-only rule, then generate and decide blindly."""

    if int(pair_member_count) != HELDOUT_PAIR_MEMBER_COUNT:
        raise ValueError("the Phase 2B held-out pair-member count is frozen")
    if int(draws_per_member) != HELDOUT_DRAWS_PER_MEMBER:
        raise ValueError("the Phase 2B held-out draw count is frozen")
    minimax = confirmation.minimax
    if (
        any(item.exact_xw_alias for item in confirmation.aliases)
        or any(
            item.represented_grid_intersects_at_tolerance
            for item in confirmation.pairwise_geometry
        )
        or minimax.finite_upper_bound > RULE_COLUMN_TOLERANCE
    ):
        raise ValueError(
            "held-out validation requires numerically separated X+W classes"
        )
    diagnostics = minimax.continuous_diagnostics
    if diagnostics is None or not diagnostics.stable_on_finite_support:
        raise ContinuousRepresentationUnavailable(
            "no continuous rule passed the finite-support reproduction gates"
        )
    rule = diagnostics.rule
    # The immutable decision rule and its commitment are fixed before any
    # held-out biological coordinate, forward MID, noisy draw, or label exists.
    commitment = continuous_rule_commitment(rule)
    root_seed = np.random.SeedSequence(int(seed))
    measurement_seed, shuffle_seed, decision_seed = root_seed.spawn(3)
    heldout = _construct_heldout_families(
        rms_noise=R_MEAS,
    )

    observation_parts: list[np.ndarray] = []
    truth_parts: list[np.ndarray] = []
    member_parts: list[np.ndarray] = []
    for class_index, (family, class_seed) in enumerate(
        zip(heldout.families, measurement_seed.spawn(len(SUPPORT_LABELS)), strict=True)
    ):
        rng = np.random.default_rng(class_seed)
        for member_index in range(family.member_count):
            observation_parts.append(
                family.sample_member(member_index, int(draws_per_member), rng)
            )
            truth_parts.append(
                np.full(int(draws_per_member), class_index, dtype=np.int16)
            )
            member_parts.append(
                np.full(int(draws_per_member), member_index, dtype=np.int16)
            )
    observations = np.vstack(observation_parts)
    truths = np.concatenate(truth_parts)
    members = np.concatenate(member_parts)
    permutation = np.random.default_rng(shuffle_seed).permutation(len(observations))
    blind_observations = observations[permutation]
    sealed_labels = (truths[permutation], members[permutation])

    probabilities = rule.decision_probabilities(blind_observations)
    if (
        probabilities.shape != (len(blind_observations), len(SUPPORT_LABELS))
        or not np.all(np.isfinite(probabilities))
        or np.any(probabilities < 0.0)
        or not np.allclose(
            np.sum(probabilities, axis=1), 1.0, rtol=0.0, atol=2.0e-12
        )
    ):
        raise ValueError("the continuous rule returned invalid held-out decisions")
    uniforms = np.random.default_rng(decision_seed).random(len(probabilities))
    predictions = np.sum(
        uniforms[:, np.newaxis] > np.cumsum(probabilities, axis=1), axis=1
    )
    predictions = np.minimum(predictions, len(SUPPORT_LABELS) - 1)
    if continuous_rule_commitment(rule) != commitment:
        raise RuntimeError("the continuous rule changed during held-out decisions")

    # Labels are revealed only after every observation-only decision is fixed.
    revealed_truths, revealed_members = sealed_labels
    confusion = np.zeros((len(SUPPORT_LABELS), len(SUPPORT_LABELS)), dtype=int)
    np.add.at(confusion, (revealed_truths, predictions), 1)
    member_results: list[HeldoutMemberResult] = []
    class_results: list[HeldoutClassResult] = []
    for class_index, (family, state) in enumerate(
        zip(heldout.families, heldout.states, strict=True)
    ):
        class_errors = 0
        member_error_rates: list[float] = []
        for member_index, member_id in enumerate(family.member_ids):
            selected = (revealed_truths == class_index) & (
                revealed_members == member_index
            )
            trials = int(np.count_nonzero(selected))
            errors = int(np.count_nonzero(predictions[selected] != class_index))
            error_rate = errors / trials
            class_errors += errors
            member_error_rates.append(error_rate)
            member_results.append(
                HeldoutMemberResult(
                    support_label=SUPPORT_LABELS[class_index],
                    member_id=member_id,
                    mixing_weight=(
                        None
                        if state.mixing_weights is None
                        else float(state.mixing_weights[member_index])
                    ),
                    trials=trials,
                    errors=errors,
                    error_rate=error_rate,
                )
            )
        class_trials = family.member_count * int(draws_per_member)
        class_results.append(
            HeldoutClassResult(
                support_label=SUPPORT_LABELS[class_index],
                member_count=family.member_count,
                trials=class_trials,
                errors=class_errors,
                error_rate=class_errors / class_trials,
                worst_member_error_rate=max(member_error_rates),
            )
        )
    total_errors = int(np.count_nonzero(predictions != revealed_truths))
    return XWHeldoutValidation(
        status="performed",
        rule_commitment_sha256=commitment,
        rule_frozen_before_forward_generation=True,
        rule_commitment_verified_after_decisions=True,
        seed=int(seed),
        pair_member_count=int(pair_member_count),
        draws_per_member=int(draws_per_member),
        total_members=sum(item.member_count for item in heldout.families),
        total_trials=len(predictions),
        total_errors=total_errors,
        overall_error_rate=total_errors / len(predictions),
        member_results=tuple(member_results),
        class_results=tuple(class_results),
        confusion=confusion,
        forward_validation=heldout.forward_validation,
    )


__all__ = [
    "CONTINUOUS_REPRODUCTION_TOLERANCE",
    "HELDOUT_DRAWS_PER_MEMBER",
    "HELDOUT_PAIR_MEMBER_COUNT",
    "HELDOUT_PAIR_WEIGHTS",
    "HELDOUT_SEED",
    "HeldoutClassResult",
    "HeldoutMemberResult",
    "MATHEMATICAL_NONNEGATIVITY_LOWER_BOUND",
    "XWHeldoutValidation",
    "XWMinimaxSolution",
    "XWPanelConfirmation",
    "build_xw_observable_families",
    "continuous_rule_commitment",
    "run_blind_xw_heldout_validation",
    "run_xw_panel_confirmation",
    "solve_xw_observable_minimax",
]
