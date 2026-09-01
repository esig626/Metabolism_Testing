from __future__ import annotations

import inspect

import numpy as np
import pytest

from fluxemu.emu_topology_edge_reconstruction import R_MEAS, SUPPORT_LABELS
from fluxemu.emu_topology_inference import (
    EXACT_ALIAS_LOWER_BOUND,
    OBSERVATION_SUPPORT_SIZE,
    build_observable_families,
    next_measurement_diagnostic,
    run_emu_topology_reconstruction,
    run_withheld_prediction,
    screen_observed_compatibility,
    solve_observable_minimax,
)


@pytest.fixture(scope="module")
def reconstruction():
    return run_emu_topology_reconstruction()


@pytest.fixture(scope="module")
def withheld_prediction(reconstruction):
    return run_withheld_prediction(reconstruction)


def test_observable_minimax_boundary_has_no_hidden_state_parameters(
    reconstruction,
) -> None:
    family_parameters = tuple(inspect.signature(build_observable_families).parameters)
    solve_parameters = tuple(inspect.signature(solve_observable_minimax).parameters)
    assert family_parameters == ("observable_classes", "rms_noise")
    assert solve_parameters == ("families", "support_size", "seed")
    assert all(family.observation_dimension == 3 for family in reconstruction.minimax.families)
    assert all(family.block_names == ("X_full",) for family in reconstruction.minimax.families)


def test_small_k_way_minimax_primal_dual_bracket_is_consistent(
    reconstruction,
) -> None:
    minimax = reconstruction.minimax
    column = minimax.column_solution
    direct = minimax.direct_solution
    assert minimax.support.support_size == OBSERVATION_SUPPORT_SIZE
    assert column.class_labels == SUPPORT_LABELS
    assert column.converged
    assert column.certificate_source == "exact_shared_law_3_class"
    assert minimax.finite_lower_bound == pytest.approx(EXACT_ALIAS_LOWER_BOUND)
    assert minimax.finite_upper_bound >= minimax.finite_lower_bound
    assert minimax.finite_upper_bound - minimax.finite_lower_bound < 2.0e-7
    assert column.maximum_simplex_violation < 1.0e-10
    assert column.maximum_primal_constraint_violation < 1.0e-10
    assert column.dual_weight_sum_error < 1.0e-10
    assert direct.absolute_duality_residual < 1.0e-10
    assert direct.dense_certificate_gap < 1.0e-10
    assert direct.dense_dual_lower_bound <= minimax.finite_upper_bound + 1.0e-10
    assert direct.dense_primal_upper_bound >= minimax.finite_lower_bound - 1.0e-10
    assert minimax.minimum_effective_sample_size > 10.0
    assert minimax.maximum_absolute_raw_mass_error < 0.1


def test_classwise_worst_cases_retain_all_six_memberwise_constraints(
    reconstruction,
) -> None:
    solution = reconstruction.minimax.column_solution
    assert solution.original_member_counts == (1, 1, 1, 11, 11, 11)
    assert solution.classwise_worst_errors.shape == (6,)
    assert np.all(np.isfinite(solution.classwise_worst_errors))
    assert np.max(solution.classwise_worst_errors) == pytest.approx(
        EXACT_ALIAS_LOWER_BOUND, abs=1.0e-12
    )
    assert solution.classwise_worst_errors[1] < EXACT_ALIAS_LOWER_BOUND


def test_fixed_seed_reproduces_support_and_minimax_solution(reconstruction) -> None:
    first = reconstruction.minimax
    repeated = solve_observable_minimax(
        first.families,
        support_size=OBSERVATION_SUPPORT_SIZE,
        seed=first.support.seed,
    )
    assert np.array_equal(first.support.observations, repeated.support.observations)
    assert np.array_equal(
        first.support.sampled_component_indices,
        repeated.support.sampled_component_indices,
    )
    assert repeated.column_solution.primal_upper_bound == pytest.approx(
        first.column_solution.primal_upper_bound, abs=1.0e-15
    )
    assert repeated.column_solution.dual_lower_bound == pytest.approx(
        first.column_solution.dual_lower_bound, abs=1.0e-15
    )


def test_withheld_mid_is_absent_from_the_compatibility_screen(
    withheld_prediction,
) -> None:
    parameters = tuple(inspect.signature(screen_observed_compatibility).parameters)
    assert parameters == ("observed_mid", "observable_classes", "rms_radius")
    assert "withheld" not in " ".join(parameters)
    screen = withheld_prediction.compatibility
    assert screen.rms_radius == R_MEAS
    assert len(screen.compatible_members) == 13
    assert all(item.observed_rms_distance <= R_MEAS for item in screen.compatible_members)


def test_withheld_prediction_retains_cloud_envelopes_and_true_mid(
    withheld_prediction,
) -> None:
    assert withheld_prediction.generating_support == "G_A"
    assert withheld_prediction.generating_mid_inside_cloud
    assert np.array_equal(
        withheld_prediction.generating_true_withheld_mid,
        np.asarray([0.25, 0.75]),
    )
    envelopes = {item.support_label: item for item in withheld_prediction.envelopes}
    assert tuple(envelopes) == ("G_A", "G_C", "G_AC")
    assert envelopes["G_A"].member_count == 1
    assert envelopes["G_C"].member_count == 1
    assert envelopes["G_AC"].member_count == 11
    assert np.array_equal(envelopes["G_A"].minimum_mid, [0.25, 0.75])
    assert np.array_equal(envelopes["G_C"].maximum_mid, [0.75, 0.25])
    assert np.allclose(envelopes["G_AC"].minimum_mid, [0.35, 0.35])
    assert np.allclose(envelopes["G_AC"].maximum_mid, [0.65, 0.65])


def test_withheld_mid_would_help_resolve_surviving_topologies(
    withheld_prediction,
) -> None:
    diagnostic = next_measurement_diagnostic(withheld_prediction)
    assert diagnostic.potentially_helpful
    assert diagnostic.maximum_cross_support_rms_difference == pytest.approx(0.5)
    assert diagnostic.comparison_threshold == R_MEAS
    assert set(diagnostic.support_pairs_with_different_predictions) == {
        ("G_A", "G_C"),
        ("G_A", "G_AC"),
        ("G_C", "G_AC"),
    }
