"""Unit tests for observable-law Renyi and projected-test primitives."""

from __future__ import annotations

import ast
import inspect
import math

import numpy as np
import pytest
from scipy.integrate import quad
from scipy.special import betaln
from scipy.stats import beta as beta_distribution

from fluxemu import composite_mid_renyi as renyi


def test_dirichlet_formula_orientation_matches_independent_beta_quadrature() -> None:
    alpha_q = np.asarray([4.25, 7.5])
    alpha_p = np.asarray([2.75, 5.0])
    order = 0.37
    analytic = renyi.dirichlet_renyi_divergence(alpha_q, alpha_p, order)

    def integrand(value: float) -> float:
        q = beta_distribution.pdf(value, alpha_q[0], alpha_q[1])
        p = beta_distribution.pdf(value, alpha_p[0], alpha_p[1])
        return q**order * p ** (1.0 - order)

    affinity, error = quad(integrand, 0.0, 1.0, epsabs=1.0e-13, epsrel=1.0e-13)
    independent = math.log(affinity) / (order - 1.0)
    assert error < 1.0e-10
    assert analytic == pytest.approx(independent, rel=2.0e-11, abs=2.0e-12)

    reverse = renyi.dirichlet_renyi_divergence(alpha_p, alpha_q, order)
    assert abs(reverse - analytic) > 1.0e-3


def test_product_formula_is_additive_positive_and_exactly_zero_on_identity() -> None:
    q = np.asarray([4.0, 6.0, 3.0, 5.0, 7.0])
    p = np.asarray([5.0, 5.0, 2.0, 8.0, 6.0])
    order = 0.63
    total = renyi.product_dirichlet_renyi_divergence(q, p, (2, 3), order)
    separate = renyi.dirichlet_renyi_divergence(q[:2], p[:2], order) + renyi.dirichlet_renyi_divergence(
        q[2:], p[2:], order
    )
    assert total == pytest.approx(separate, abs=2.0e-13)
    assert total > 0.0
    assert renyi.product_dirichlet_renyi_divergence(q, q.copy(), (2, 3), order) == 0.0


def test_endpoint_stable_formula_has_correct_kl_limits() -> None:
    q = np.asarray([0.266, 25.0, 2781.98])
    p = np.asarray([17.0, 31.0, 1600.0])
    near_one = renyi.dirichlet_renyi_divergence(q, p, 1.0 - 1.0e-8)
    kl_qp = renyi.dirichlet_kl_divergence(q, p)
    assert near_one == pytest.approx(kl_qp, rel=2.0e-7, abs=2.0e-8)

    near_zero_order = 1.0e-8
    near_zero = renyi.dirichlet_renyi_divergence(q, p, near_zero_order)
    kl_pq = renyi.dirichlet_kl_divergence(p, q)
    assert near_zero / near_zero_order == pytest.approx(
        kl_pq, rel=2.0e-7, abs=2.0e-8
    )
    assert math.isfinite(near_zero) and near_zero > 0.0


def test_force_stable_quadrature_handles_outer_admissible_scale_contrast() -> None:
    q = np.asarray([0.2660465848826671, 2781.98, 5.0])
    p = np.asarray([30.373862433862424, 1200.0, 1600.0])
    values = [
        renyi.dirichlet_renyi_divergence(q, p, order, force_stable=True)
        for order in (1.0e-8, 1.0e-6, 1.0e-4, 1.0 - 1.0e-4, 1.0 - 1.0e-6, 1.0 - 1.0e-8)
    ]
    assert all(math.isfinite(value) and value > 0.0 for value in values)
    assert values == sorted(values)


def test_dense_pairwise_matrix_matches_scalar_orientation() -> None:
    q_rows = np.asarray([[4.0, 6.0], [7.0, 3.0], [8.0, 2.0]])
    p_rows = np.asarray([[3.0, 7.0], [6.0, 4.0]])
    matrix = renyi.pairwise_product_dirichlet_renyi(q_rows, p_rows, (2,), 0.41)
    assert matrix.shape == (3, 2)
    for q_index in range(3):
        for p_index in range(2):
            scalar = renyi.product_dirichlet_renyi_divergence(
                q_rows[q_index], p_rows[p_index], (2,), 0.41
            )
            assert matrix[q_index, p_index] == pytest.approx(scalar, abs=2.0e-13)


def test_formula_agrees_with_independent_monte_carlo_affinity() -> None:
    q = np.asarray([5.0, 7.0, 4.0])
    p = np.asarray([4.0, 6.0, 6.0])
    order = 0.55
    score = renyi.projected_log_likelihood_score(p, q, (3,))
    rng = np.random.default_rng(8_081)
    observations = rng.dirichlet(p, size=300_000)
    weights = np.exp(order * score.evaluate(observations))
    estimated_affinity = float(np.mean(weights))
    standard_error = float(np.std(weights, ddof=1) / math.sqrt(len(weights)))
    estimated = math.log(estimated_affinity) / (order - 1.0)
    analytic = renyi.dirichlet_renyi_divergence(q, p, order)
    propagated_three_se = 3.0 * standard_error / (
        estimated_affinity * (1.0 - order)
    )
    assert abs(estimated - analytic) <= propagated_three_se


def test_projected_score_and_analytic_moments_have_mandatory_orientation() -> None:
    p = np.asarray([4.0, 6.0, 3.0, 7.0])
    q = np.asarray([6.0, 4.0, 5.0, 5.0])
    blocks = (2, 2)
    order = 0.38
    score = renyi.projected_log_likelihood_score(p, q, blocks)
    assert np.array_equal(score.coefficients, q - p)
    expected_constant = (
        betaln(p[0], p[1])
        + betaln(p[2], p[3])
        - betaln(q[0], q[1])
        - betaln(q[2], q[3])
    )
    assert score.log_constant == pytest.approx(expected_constant, abs=2.0e-13)
    divergence = renyi.product_dirichlet_renyi_divergence(q, p, blocks, order)
    log_affinity = (order - 1.0) * divergence
    assert score.log_moment(p, order) == pytest.approx(log_affinity, abs=2.0e-12)
    assert score.log_moment(q, order - 1.0) == pytest.approx(
        log_affinity, abs=2.0e-12
    )


def test_saddlepoint_cdf_is_smooth_and_agrees_with_independent_simulation() -> None:
    p = np.asarray([8.0, 12.0, 10.0])
    q = np.asarray([11.0, 9.0, 10.0])
    score = renyi.projected_log_likelihood_score(p, q, (3,))
    threshold = -0.15
    approximation = renyi.saddlepoint_score_cdf(score, p, threshold)
    rng = np.random.default_rng(81_001)
    observations = rng.dirichlet(p, size=400_000)
    estimate = float(np.mean(score.evaluate(observations) <= threshold))
    standard_error = math.sqrt(estimate * (1.0 - estimate) / len(observations))
    assert approximation.method in {"Lugannani-Rice", "mean Edgeworth limit"}
    assert approximation.log_probability == pytest.approx(
        math.log(approximation.probability), abs=2.0e-13
    )
    assert abs(approximation.probability - estimate) < max(6.0 * standard_error, 0.004)


def test_saddlepoint_log_cdf_retains_a_finite_underflow_tail() -> None:
    p = np.asarray([800.0, 1200.0, 1000.0])
    q = np.asarray([1100.0, 900.0, 1000.0])
    score = renyi.projected_log_likelihood_score(p, q, (3,))
    mean = score.cumulant_derivative(q, 0.0, 1)
    standard_deviation = math.sqrt(score.cumulant_derivative(q, 0.0, 2))
    tail = renyi.saddlepoint_score_cdf(
        score, q, mean - 50.0 * standard_deviation
    )
    assert tail.probability == 0.0
    assert math.isfinite(tail.log_probability)
    assert tail.log_probability < math.log(np.nextafter(0.0, 1.0))


def test_characteristic_inversion_agrees_with_simulation_and_reports_decay() -> None:
    p = np.asarray([8.0, 12.0, 10.0])
    q = np.asarray([11.0, 9.0, 10.0])
    score = renyi.projected_log_likelihood_score(p, q, (3,))
    threshold = -0.15
    inversion = renyi.characteristic_score_cdf(score, p, threshold)
    rng = np.random.default_rng(81_002)
    observations = rng.dirichlet(p, size=400_000)
    estimate = float(np.mean(score.evaluate(observations) <= threshold))
    standard_error = math.sqrt(estimate * (1.0 - estimate) / len(observations))
    assert abs(inversion.probability - estimate) < 5.0 * standard_error
    assert inversion.absolute_quadrature_error < 1.0e-8
    assert inversion.log_characteristic_magnitude_at_cutoff <= -80.0
    assert inversion.method.startswith("Gil-Pelaez")


def test_closed_form_minimum_threshold_uses_epsilon_translation() -> None:
    order = 0.6
    separation = 4.25
    epsilon = 0.05
    threshold = renyi.closed_form_minimum_threshold(
        order, separation, epsilon=epsilon, sample_size=1
    )
    expected = (-math.log(epsilon) - (1.0 - order) * separation) / order
    assert threshold == pytest.approx(expected, abs=1.0e-15)
    bound = renyi.complete_moment_exponential_bound(order, separation, threshold)
    assert bound == pytest.approx(
        math.exp((1.0 - order) / order * (-math.log(epsilon) - separation)),
        rel=2.0e-15,
    )


def test_empirical_calibration_keeps_randomisation_interface() -> None:
    null_rows = [np.asarray([0.0] * 95 + [1.0] * 5)]
    alternative_rows = [np.asarray([0.0] * 20 + [1.0] * 80)]
    calibrated = renyi.calibrate_empirical_threshold(
        null_rows, alternative_rows, epsilon=0.025
    )
    assert calibrated.threshold == 1.0
    assert calibrated.tie_probability == pytest.approx(0.5)
    assert calibrated.worst_type_i == pytest.approx(0.025)
    assert calibrated.worst_type_ii == pytest.approx(0.6)


def test_corrected_bound_couples_slack_and_rejection_under_same_q() -> None:
    rows = [
        np.asarray([-1.0, 0.0, 1.0, 2.0]),
        np.asarray([-2.0, -0.5, 0.5, 3.0]),
    ]
    result = renyi.evaluate_empirical_corrected_bound(
        rows, 0.65, 0.4, 0.25, tie_probability=0.0
    )
    c = math.exp((0.65 - 1.0) * 0.4)
    same_q_terms = []
    accepted = []
    for row in rows:
        weights = np.exp((0.65 - 1.0) * row)
        rejected = float(np.mean(weights * (row > 0.25)))
        full = float(np.mean(weights))
        same_q_terms.append(c - full + rejected)
        accepted.append(float(np.mean(weights * (row <= 0.25))))
    assert result.tilde_gamma == pytest.approx(min(same_q_terms), abs=2.0e-15)
    assert result.corrected_bound == pytest.approx(
        math.exp(0.35 * 0.25) * max(accepted), abs=2.0e-15
    )
    assert result.same_q_identity_residual < 1.0e-14


def test_global_order_optimiser_checks_multiple_basins_and_flat_sets() -> None:
    def multimodal(order: float) -> float:
        return min((order - 0.22) ** 2 + 0.03, (order - 0.78) ** 2 + 0.01)

    result = renyi.optimise_order_globally(
        multimodal,
        objective_name="synthetic_multibasin",
        exploratory_grid_size=101,
        validation_grid_size=301,
    )
    assert result.order == pytest.approx(0.78, abs=2.0e-7)
    assert result.objective == pytest.approx(0.01, abs=1.0e-12)
    assert result.candidate_basin_count >= 2

    flat = renyi.optimise_order_globally(
        lambda order: 0.25,
        objective_name="flat",
        exploratory_grid_size=51,
        validation_grid_size=101,
    )
    assert flat.order is None
    assert flat.optimiser_kind == "set-valued flat objective"
    assert flat.equivalent_order_lower == 0.0
    assert flat.equivalent_order_upper == 1.0


def test_parameterised_pair_search_refines_all_boundaries_and_dense_grid() -> None:
    # Both families move in the same one-parameter beta family.  The separated
    # intervals make their adjacent endpoints the unique closest pair.
    null_alpha = lambda coordinate: np.asarray([20.0 + coordinate, 30.0 - coordinate])
    alternative_alpha = lambda coordinate: np.asarray(
        [20.0 + coordinate, 30.0 - coordinate]
    )
    result = renyi.minimise_parameterised_pair(
        0.47,
        null_alpha,
        alternative_alpha,
        (0.0, 2.0),
        (4.0, 6.0),
        (2,),
        exploratory_grid_size=9,
        validation_grid_size=21,
        candidate_start_count=4,
    )
    assert result.null_coordinate == pytest.approx(2.0, abs=2.0e-7)
    assert result.alternative_coordinate == pytest.approx(4.0, abs=2.0e-7)
    assert result.dense_grid_discrepancy < 1.0e-9
    assert result.success


def test_module_has_no_model_flux_or_inverse_mfa_import_path() -> None:
    tree = ast.parse(inspect.getsource(renyi))
    imported = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }
    assert not any("cobra" in name for name in imported)
    assert not any("mfapy" in name for name in imported)
    assert not any("forward" in name for name in imported)
    public_parameters = inspect.signature(
        renyi.product_dirichlet_renyi_divergence
    ).parameters
    assert set(public_parameters) >= {"alpha_q", "alpha_p", "block_sizes", "order"}
    assert not any("flux" in name for name in public_parameters)
