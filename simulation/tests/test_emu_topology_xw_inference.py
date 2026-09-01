from __future__ import annotations

from dataclasses import replace
import inspect
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

from fluxemu.emu_topology_edge_reconstruction import MASTER_SEED, SUPPORT_LABELS
from fluxemu.emu_topology_inference import OBSERVATION_SUPPORT_SIZE
from fluxemu.composite_mid_minimax import (
    ContinuousRepresentationUnavailable,
    family_from_mid_class,
)
from fluxemu import emu_topology_xw_inference as xw_inference
from fluxemu.emu_topology_xw_inference import (
    HELDOUT_DRAWS_PER_MEMBER,
    HELDOUT_PAIR_MEMBER_COUNT,
    HELDOUT_PAIR_WEIGHTS,
    MATHEMATICAL_NONNEGATIVITY_LOWER_BOUND,
    build_xw_observable_families,
    run_blind_xw_heldout_validation,
    run_xw_panel_confirmation,
    solve_xw_observable_minimax,
)


PHASE2A_RESULTS = (
    Path(__file__).resolve().parents[1]
    / "fixtures"
    / "topology_phase2a"
)


@pytest.fixture(scope="module")
def confirmation():
    return run_xw_panel_confirmation(PHASE2A_RESULTS)


@pytest.fixture(scope="module")
def heldout(confirmation):
    return run_blind_xw_heldout_validation(confirmation)


def test_minimax_boundary_accepts_only_mid_classes_then_law_families(
    confirmation,
) -> None:
    family_parameters = tuple(
        inspect.signature(build_xw_observable_families).parameters
    )
    solve_parameters = tuple(inspect.signature(solve_xw_observable_minimax).parameters)
    assert family_parameters == ("observable_classes", "rms_noise")
    assert solve_parameters == ("families", "support_size", "seed")
    for family in confirmation.minimax.families:
        assert family.block_names == ("X_full", "W_full")
        assert family.block_sizes == (3, 2)
        assert family.observation_dimension == 5
        assert np.sum(family.exact_mids[:, :3], axis=1) == pytest.approx(1.0)
        assert np.sum(family.exact_mids[:, 3:], axis=1) == pytest.approx(1.0)
        assert np.sum(family.exact_mids, axis=1) == pytest.approx(2.0)


def test_xw_finite_minimax_has_a_consistent_zero_risk_bracket(
    confirmation,
) -> None:
    minimax = confirmation.minimax
    column = minimax.column_solution
    direct = minimax.direct_solution
    assert MATHEMATICAL_NONNEGATIVITY_LOWER_BOUND == 0.0
    assert minimax.support.support_size == OBSERVATION_SUPPORT_SIZE
    assert column.class_labels == SUPPORT_LABELS
    assert column.converged
    assert minimax.finite_lower_bound == pytest.approx(0.0, abs=1.0e-15)
    assert minimax.finite_upper_bound >= minimax.finite_lower_bound
    assert minimax.certificate_gap < 2.0e-7
    assert minimax.finite_upper_bound < 1.0e-12
    assert column.maximum_simplex_violation < 1.0e-10
    assert column.maximum_primal_constraint_violation < 1.0e-10
    assert column.dual_weight_sum_error < 1.0e-10
    assert direct.absolute_duality_residual < 1.0e-10
    assert direct.dense_certificate_gap < 1.0e-10
    assert direct.dense_dual_lower_bound <= minimax.finite_upper_bound + 1.0e-10
    assert direct.dense_primal_upper_bound >= minimax.finite_lower_bound - 1.0e-10
    assert max(0.0, direct.dense_dual_lower_bound) == pytest.approx(
        minimax.finite_lower_bound, abs=1.0e-30
    )
    assert direct.dense_primal_upper_bound == pytest.approx(
        minimax.finite_upper_bound, abs=1.0e-30
    )
    for column_errors, direct_errors in zip(
        column.member_errors, direct.member_errors, strict=True
    ):
        assert direct_errors == pytest.approx(column_errors, abs=1.0e-30)
    assert minimax.minimum_effective_sample_size > 10.0
    assert minimax.maximum_absolute_raw_mass_error < 0.1


def test_all_six_classwise_worst_case_errors_are_retained(confirmation) -> None:
    solution = confirmation.minimax.column_solution
    assert solution.original_member_counts == (1, 1, 1, 11, 11, 11)
    assert solution.classwise_worst_errors.shape == (6,)
    assert np.all(np.isfinite(solution.classwise_worst_errors))
    assert np.all(solution.classwise_worst_errors >= 0.0)
    assert np.max(solution.classwise_worst_errors) == pytest.approx(
        confirmation.minimax.finite_upper_bound,
        abs=1.0e-30,
    )


def test_continuous_dual_density_rule_passes_existing_reproduction_gates(
    confirmation,
) -> None:
    minimax = confirmation.minimax
    assert minimax.continuous_rule_available
    assert minimax.continuous_rule_reason == (
        "finite-support reproduction gates passed"
    )
    diagnostics = minimax.continuous_diagnostics
    assert diagnostics is not None
    assert diagnostics.stable_on_finite_support
    assert diagnostics.maximum_member_error_difference_from_primal < (
        diagnostics.reproduction_tolerance
    )
    assert diagnostics.objective_difference < diagnostics.reproduction_tolerance
    assert diagnostics.rule.class_labels == SUPPORT_LABELS


def test_phase2b_solver_rejects_x_only_or_wrong_noise_families(confirmation) -> None:
    x_only = tuple(
        family_from_mid_class(
            SimpleNamespace(
                member_ids=family.member_ids,
                blocks=(("X_full", 0, 3),),
                exact_mids=family.exact_mids[:, :3],
            ),
            rms_noise=0.005,
        )
        for family in confirmation.minimax.families
    )
    with pytest.raises(ValueError, match="X_full/W_full"):
        solve_xw_observable_minimax(x_only)
    with pytest.raises(ValueError, match="r_meas=0.005"):
        build_xw_observable_families(
            confirmation.panel.observables,
            rms_noise=0.006,
        )


def test_continuous_rule_unavailable_and_failed_gates_preserve_finite_result(
    confirmation,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def unavailable(*args, **kwargs):
        raise ContinuousRepresentationUnavailable("deliberately unavailable")

    monkeypatch.setattr(
        xw_inference,
        "build_continuous_multiclass_rule",
        unavailable,
    )
    unavailable_result = solve_xw_observable_minimax(
        confirmation.minimax.families,
        support_size=300,
    )
    assert unavailable_result.continuous_diagnostics is None
    assert not unavailable_result.continuous_rule_available
    assert unavailable_result.continuous_rule_reason == "deliberately unavailable"
    assert np.isfinite(unavailable_result.finite_upper_bound)

    failed = replace(
        confirmation.minimax.continuous_diagnostics,
        stable_on_finite_support=False,
    )
    monkeypatch.setattr(
        xw_inference,
        "build_continuous_multiclass_rule",
        lambda *args, **kwargs: failed,
    )
    failed_result = solve_xw_observable_minimax(
        confirmation.minimax.families,
        support_size=300,
    )
    assert failed_result.continuous_diagnostics is failed
    assert not failed_result.continuous_rule_available
    assert failed_result.continuous_rule_reason == (
        "finite-support reproduction gates failed"
    )


def test_frozen_seed_reproduces_xw_support_and_minimax_solution(confirmation) -> None:
    first = confirmation.minimax
    repeated = solve_xw_observable_minimax(
        first.families,
        support_size=OBSERVATION_SUPPORT_SIZE,
        seed=MASTER_SEED,
    )
    assert np.array_equal(first.support.observations, repeated.support.observations)
    assert np.array_equal(
        first.support.sampled_component_indices,
        repeated.support.sampled_component_indices,
    )
    assert repeated.finite_upper_bound == pytest.approx(
        first.finite_upper_bound, abs=1.0e-30
    )
    assert repeated.finite_lower_bound == pytest.approx(
        first.finite_lower_bound, abs=1.0e-30
    )
    assert repeated.column_solution.classwise_worst_errors == pytest.approx(
        first.column_solution.classwise_worst_errors,
        abs=1.0e-30,
    )


def test_small_blind_heldout_runs_only_with_the_frozen_continuous_rule(
    confirmation,
    heldout,
) -> None:
    assert confirmation.minimax.continuous_rule_available
    assert heldout.status == "performed"
    assert heldout.rule_frozen_before_forward_generation
    assert heldout.rule_commitment_verified_after_decisions
    assert len(heldout.rule_commitment_sha256) == 64
    assert heldout.pair_member_count == HELDOUT_PAIR_MEMBER_COUNT == 4
    assert heldout.draws_per_member == HELDOUT_DRAWS_PER_MEMBER == 200
    assert heldout.total_members == 15
    assert heldout.total_trials == 3_000
    assert heldout.forward_validation["valid"] is True
    assert heldout.forward_validation["sample_count"] == 15
    assert heldout.forward_validation["target_ids"] == ["X_full", "W_full"]
    assert [item.member_count for item in heldout.class_results] == [1, 1, 1, 4, 4, 4]


def test_heldout_coordinates_are_predeclared_off_grid_emu_states(heldout) -> None:
    observed_pair_weights = tuple(
        item.mixing_weight
        for item in heldout.member_results
        if item.mixing_weight is not None
    )
    assert observed_pair_weights == pytest.approx(
        HELDOUT_PAIR_WEIGHTS * 3,
        abs=1.0e-15,
    )
    training_weights = np.linspace(0.2, 0.8, 11)
    assert not np.any(
        np.isclose(
            np.asarray(observed_pair_weights)[:, np.newaxis],
            training_weights,
            rtol=0.0,
            atol=1.0e-12,
        )
    )
    assert all("G_" not in item.member_id for item in heldout.member_results)
    assert all("e_" not in item.member_id for item in heldout.member_results)


def test_heldout_rule_classifies_the_frozen_small_draw_set(heldout) -> None:
    assert heldout.total_errors == 0
    assert heldout.overall_error_rate == 0.0
    assert np.array_equal(heldout.confusion, np.diag([200, 200, 200, 800, 800, 800]))
    assert all(item.errors == 0 for item in heldout.member_results)
    assert all(item.error_rate == 0.0 for item in heldout.class_results)
