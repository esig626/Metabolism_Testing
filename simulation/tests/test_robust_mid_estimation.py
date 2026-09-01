from __future__ import annotations

import math

import numpy as np
import pytest

from fluxemu.robust_mid_estimation import (
    dimension_normalized_squared_mid_error,
    estimability_threshold_counts,
    finite_bayes_mid_risk,
    identical_observation_law_lower_bound,
    posterior_mean_mid_estimator,
    recompute_statewise_mid_risks,
    robust_rmse,
    solve_finite_minimax_mid_estimation,
)


def _pair_prior() -> np.ndarray:
    return np.asarray([0.5, 0.5], dtype=float)


def test_dimension_normalized_squared_mid_error_uses_target_dimension() -> None:
    target = np.asarray([0.25, 0.75])
    estimate = np.asarray([0.75, 0.25])
    assert dimension_normalized_squared_mid_error(target, estimate) == pytest.approx(
        0.25
    )
    rows = dimension_normalized_squared_mid_error(
        np.vstack((target, estimate)), estimate
    )
    assert rows == pytest.approx([0.25, 0.0])


def test_robust_rmse_is_root_of_worst_expected_squared_error() -> None:
    assert robust_rmse(0.0625) == pytest.approx(0.25)
    with pytest.raises(ValueError, match="nonnegative"):
        robust_rmse(-0.1)


def test_posterior_mean_formula_returns_valid_mid_simplex_points() -> None:
    probabilities = np.asarray([[0.8, 0.2], [0.2, 0.8]])
    targets = np.asarray([[1.0, 0.0], [0.0, 1.0]])
    posterior = posterior_mean_mid_estimator(
        _pair_prior(), probabilities, targets
    )
    assert np.allclose(
        posterior.estimates,
        np.asarray([[0.8, 0.2], [0.2, 0.8]]),
        rtol=0.0,
        atol=1.0e-15,
    )
    assert np.all(posterior.estimates >= 0.0)
    assert np.sum(posterior.estimates, axis=1) == pytest.approx(1.0)
    assert not np.any(posterior.zero_mixture_columns)


def test_posterior_scaling_preserves_midpoint_for_subnormal_identical_rows() -> None:
    subnormal = np.nextafter(0.0, 1.0)
    probabilities = np.asarray(
        [[subnormal, 0.5, 0.5], [subnormal, 0.5, 0.5]], dtype=float
    )
    targets = np.asarray([[0.25, 0.75], [0.75, 0.25]])
    posterior = posterior_mean_mid_estimator(
        _pair_prior(), probabilities, targets
    )
    assert posterior.estimates == pytest.approx(
        np.repeat([[0.5, 0.5]], 3, axis=0), abs=0.0
    )


def test_statewise_risk_recomputation_matches_an_independent_loop() -> None:
    probabilities = np.asarray([[0.8, 0.2], [0.2, 0.8]])
    targets = np.asarray([[1.0, 0.0], [0.0, 1.0]])
    actions = np.asarray([[0.8, 0.2], [0.2, 0.8]])
    observed = recompute_statewise_mid_risks(probabilities, targets, actions)
    expected = []
    for state_index in range(2):
        value = 0.0
        for support_index in range(2):
            value += probabilities[state_index, support_index] * float(
                np.mean(
                    np.square(targets[state_index] - actions[support_index])
                )
            )
        expected.append(value)
    assert observed == pytest.approx(expected)
    assert observed == pytest.approx([0.16, 0.16])


def test_control_e0_identical_law_recovers_exact_midpoint_minimax_value() -> None:
    probabilities = np.asarray([[0.25, 0.75], [0.25, 0.75]])
    targets = np.asarray([[0.25, 0.75], [0.75, 0.25]])
    bound = identical_observation_law_lower_bound(
        probabilities[0], probabilities[1], targets[0], targets[1]
    )
    assert bound.target_rms_separation == pytest.approx(0.5)
    assert bound.minimax_mse_lower_bound == pytest.approx(0.0625)
    assert bound.robust_rmse_lower_bound == pytest.approx(0.25)

    solution = solve_finite_minimax_mid_estimation(
        probabilities,
        targets,
        initial_priors=(_pair_prior(),),
        deterministic_start_count=5,
    )
    assert solution.optimisation_converged
    assert solution.least_favourable_prior == pytest.approx(_pair_prior())
    assert np.allclose(
        solution.estimator,
        np.asarray([[0.5, 0.5], [0.5, 0.5]]),
        rtol=0.0,
        atol=1.0e-15,
    )
    assert solution.bayes_risk_lower_bound == pytest.approx(0.0625)
    assert solution.maximum_risk_upper_bound == pytest.approx(0.0625)
    assert solution.finite_saddle_gap <= 1.0e-12
    assert solution.robust_rmse == pytest.approx(0.25)


def test_control_e1_different_laws_matches_direct_action_grid() -> None:
    probabilities = np.asarray([[0.8, 0.2], [0.2, 0.8]])
    targets = np.asarray([[1.0, 0.0], [0.0, 1.0]])
    solution = solve_finite_minimax_mid_estimation(
        probabilities,
        targets,
        initial_priors=(_pair_prior(),),
        deterministic_start_count=5,
    )

    grid = np.linspace(0.0, 1.0, 401)
    first, second = np.meshgrid(grid, grid, indexing="ij")
    risk_zero = 0.8 * np.square(1.0 - first) + 0.2 * np.square(1.0 - second)
    risk_one = 0.2 * np.square(first) + 0.8 * np.square(second)
    direct = float(np.min(np.maximum(risk_zero, risk_one)))
    assert direct == pytest.approx(0.16, abs=1.0e-12)
    assert solution.bayes_risk_lower_bound == pytest.approx(direct, abs=1.0e-11)
    assert solution.maximum_risk_upper_bound == pytest.approx(direct, abs=1.0e-11)
    assert np.allclose(
        solution.estimator,
        np.asarray([[0.8, 0.2], [0.2, 0.8]]),
        rtol=0.0,
        atol=1.0e-11,
    )


def test_least_favourable_solution_audits_simplex_risks_and_kkt() -> None:
    probabilities = np.asarray(
        [[0.8, 0.2], [0.2, 0.8], [0.5, 0.5]], dtype=float
    )
    targets = np.asarray([[1.0, 0.0], [0.0, 1.0], [0.5, 0.5]])
    pair = np.asarray([0.5, 0.5, 0.0])
    solution = solve_finite_minimax_mid_estimation(
        probabilities,
        targets,
        initial_priors=(pair,),
        deterministic_start_count=6,
    )
    assert np.all(solution.least_favourable_prior >= 0.0)
    assert np.sum(solution.least_favourable_prior) == pytest.approx(1.0)
    assert solution.simplex_residual <= 1.0e-12
    assert np.all(
        solution.statewise_risks
        <= solution.maximum_risk_upper_bound + 1.0e-14
    )
    assert solution.active_risk_equalization_residual <= 1.0e-8
    assert solution.inactive_risk_violation <= 1.0e-8
    assert solution.maximum_complementarity_residual <= 1.0e-8
    assert solution.optimizer_runs
    assert any(item.success for item in solution.optimizer_runs)


def test_bayes_risk_equals_prior_weighted_recomputed_risk() -> None:
    probabilities = np.asarray([[0.7, 0.3], [0.1, 0.9]])
    targets = np.asarray([[0.8, 0.2], [0.2, 0.8]])
    prior = np.asarray([0.4, 0.6])
    posterior = posterior_mean_mid_estimator(prior, probabilities, targets)
    risks = recompute_statewise_mid_risks(
        probabilities, targets, posterior.estimates
    )
    assert finite_bayes_mid_risk(prior, probabilities, targets) == pytest.approx(
        float(prior @ risks), abs=1.0e-15
    )


def test_solver_is_deterministic_for_fixed_starts_and_seed() -> None:
    probabilities = np.asarray([[0.8, 0.2], [0.2, 0.8]])
    targets = np.asarray([[1.0, 0.0], [0.0, 1.0]])
    first = solve_finite_minimax_mid_estimation(
        probabilities, targets, deterministic_start_count=5, start_seed=91
    )
    second = solve_finite_minimax_mid_estimation(
        probabilities, targets, deterministic_start_count=5, start_seed=91
    )
    assert np.array_equal(
        first.least_favourable_prior, second.least_favourable_prior
    )
    assert np.array_equal(first.estimator, second.estimator)
    assert first.maximum_risk_upper_bound == second.maximum_risk_upper_bound


def test_estimability_threshold_counting_is_inclusive_at_frozen_levels() -> None:
    observed = estimability_threshold_counts(
        [0.25, math.sqrt(7.0 / 384.0)],
        [0.10, 0.15, 0.25],
    )
    assert [item.estimable_count for item in observed] == [0, 1, 2]
    assert all(item.target_count == 2 for item in observed)
