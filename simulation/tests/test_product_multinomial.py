from __future__ import annotations

from dataclasses import replace
import itertools
import math

import numpy as np
import pytest
from scipy.special import gammaln

from fluxemu.composite_mid_minimax import MinimaxNumericalError, solve_finite_minimax
from fluxemu.product_multinomial import (
    AlternativeSupportUnionTest,
    DiscreteCommonProposalSupport,
    ProductMultinomialFamily,
    ProductMultinomialMIDLaw,
    alternative_support_union_probability,
    build_balanced_multinomial_proposal_support,
    build_product_multinomial_mixture_test,
    categorical_kl_divergence,
    categorical_renyi_divergence,
    last_coordinate_fsum_closure,
    multinomial_counts_from_mids,
    multinomial_importance_discretize,
    multinomial_mids_from_counts,
    product_multinomial_kl_divergence,
    product_multinomial_log_lr_moment,
    product_multinomial_renyi_divergence,
    support_event_probability,
    SIMPLEX_CLOSURE_POLICY,
    SIMPLEX_CLOSURE_TOLERANCE,
    validate_multinomial_counts,
)


BLOCK_NAMES = ("first", "second")
BLOCK_SIZES = (2, 3)
P = np.array([0.25, 0.75, 0.2, 0.3, 0.5])
Q = np.array([0.0, 1.0, 0.1, 0.0, 0.9])


def _law(probabilities: np.ndarray = P, depth: int = 2, name: str = "law"):
    return ProductMultinomialMIDLaw(
        member_id=name,
        block_names=BLOCK_NAMES,
        block_sizes=BLOCK_SIZES,
        probabilities=probabilities,
        n_count=depth,
    )


def _compositions(total: int, dimension: int):
    if dimension == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in _compositions(total - first, dimension - 1):
            yield (first,) + rest


def _alphabet(depth: int) -> np.ndarray:
    rows = [
        first + second
        for first, second in itertools.product(
            _compositions(depth, 2), _compositions(depth, 3)
        )
    ]
    return np.asarray(rows, dtype=np.int64)


def test_signed_zero_is_canonicalized_without_altering_positive_probabilities():
    values = np.array([-0.0, 1.0, 0.1, -0.0, 0.9])
    law = _law(values)
    assert not np.signbit(law.probabilities[0])
    assert not np.signbit(law.probabilities[3])
    np.testing.assert_array_equal(law.probabilities[[1, 2, 4]], values[[1, 2, 4]])
    with pytest.raises(ValueError, match="nonnegative"):
        _law(np.array([-1e-300, 1.0, 0.1, 0.0, 0.9]))


def test_authorized_last_coordinate_closure_changes_only_the_final_coordinate():
    raw = np.array([-0.0, 0.2, 0.3, 0.5000000000000002])
    closed = last_coordinate_fsum_closure(raw)
    assert SIMPLEX_CLOSURE_POLICY == "last_coordinate_fsum_closure_v1"
    assert SIMPLEX_CLOSURE_TOLERANCE == 64 * np.finfo(np.float64).eps
    assert not np.signbit(closed.raw[0])
    np.testing.assert_array_equal(closed.effective[:-1], closed.raw[:-1])
    assert closed.effective[-1] == 1.0 - math.fsum(closed.effective[:-1])
    assert closed.signed_delta == closed.effective[-1] - closed.raw[-1]
    assert closed.absolute_delta <= SIMPLEX_CLOSURE_TOLERANCE
    np.testing.assert_array_equal(closed.raw > 0.0, closed.effective > 0.0)
    assert not closed.support_changed


def test_closure_rejects_out_of_gate_inputs_and_does_not_smooth():
    with pytest.raises(ValueError, match="normalisation residual"):
        last_coordinate_fsum_closure([0.2, 0.3, 0.500000000001])
    with pytest.raises(ValueError, match="final simplex coordinate"):
        last_coordinate_fsum_closure([0.5, 0.5, 0.0])
    with pytest.raises(ValueError, match="nonnegative"):
        last_coordinate_fsum_closure([-1e-30, 0.5, 0.5])


def test_unclosed_raw_vector_is_rejected_by_every_statistical_path():
    raw = np.array([0.2, 0.3, 0.5000000000000002])
    closed = last_coordinate_fsum_closure(raw)
    with pytest.raises(ValueError, match="last-coordinate simplex closure"):
        ProductMultinomialMIDLaw("raw", ("only",), (3,), raw, 2)
    law = ProductMultinomialMIDLaw("effective", ("only",), (3,), closed.effective, 2)
    assert law.exact_mean[-1] == closed.effective[-1]
    globally_normalized = raw / np.sum(raw)
    assert not np.array_equal(globally_normalized[:-1], raw[:-1])
    global_law = ProductMultinomialMIDLaw(
        "globally-normalized", ("only",), (3,), globally_normalized, 2
    )
    assert global_law.fingerprint != law.fingerprint


def test_law_is_immutable_and_fingerprint_is_deterministic():
    source = P.copy()
    law = _law(source)
    source[0] = 0.5
    assert law.probabilities[0] == 0.25
    with pytest.raises(ValueError):
        law.probabilities[0] = 0.5
    assert law.fingerprint == _law(P.copy()).fingerprint
    assert law.fingerprint != _law(P.copy(), depth=3).fingerprint
    with pytest.raises(ValueError, match="positive integer"):
        _law(P.copy(), depth=True)
    with pytest.raises(ValueError, match="block sizes must be integers"):
        ProductMultinomialMIDLaw("bad", BLOCK_NAMES, (2.5, 3), P, 2)


def test_count_and_normalized_mid_roundtrip_and_invalid_panels():
    counts = np.array([[1, 1, 0, 1, 1], [0, 2, 2, 0, 0]])
    validated = validate_multinomial_counts(counts, BLOCK_SIZES, 2)
    mids = multinomial_mids_from_counts(validated, BLOCK_SIZES, 2)
    np.testing.assert_array_equal(
        multinomial_counts_from_mids(mids, BLOCK_SIZES, 2), counts
    )
    with pytest.raises(ValueError, match="total"):
        validate_multinomial_counts([[1, 0, 0, 1, 1]], BLOCK_SIZES, 2)
    with pytest.raises(ValueError, match="integers"):
        validate_multinomial_counts([[0.5, 1.5, 0, 1, 1]], BLOCK_SIZES, 2)
    with pytest.raises(ValueError, match="nonnegative"):
        validate_multinomial_counts([[-1, 3, 0, 1, 1]], BLOCK_SIZES, 2)
    with pytest.raises(ValueError, match="not an N_count"):
        multinomial_counts_from_mids([[0.2, 0.8, 0, 0.5, 0.5]], BLOCK_SIZES, 2)


def test_log_pmf_matches_hand_calculation_and_normalizes_by_enumeration():
    law = _law()
    alphabet = _alphabet(2)
    log_pmf = law.log_pmf(alphabet)
    assert np.sum(np.exp(log_pmf)) == pytest.approx(1.0, abs=2e-15)
    counts = np.array([[1, 1, 0, 1, 1]])
    expected = (
        gammaln(3) - gammaln(2) - gammaln(2)
        + math.log(0.25) + math.log(0.75)
        + gammaln(3) - gammaln(1) - gammaln(2) - gammaln(2)
        + math.log(0.3) + math.log(0.5)
    )
    assert law.log_pmf(counts)[0] == pytest.approx(expected, abs=1e-14)


def test_exact_zero_support_and_sampling_never_emit_forbidden_counts():
    law = _law(Q)
    draws = law.sample(20_000, np.random.default_rng(412))
    assert np.all(draws[:, 0] == 0)
    assert np.all(draws[:, 3] == 0)
    forbidden = np.array([[1, 1, 0, 1, 1]])
    assert law.log_pmf(forbidden)[0] == -math.inf
    assert not law.support_contains(forbidden)[0]
    assert np.all(law.support_contains(draws))


def test_sequential_sampler_matches_pmf_numpy_and_analytic_moments():
    depth = 2
    law = _law(P, depth=depth)
    draw_count = 120_000
    sequential = law.sample(draw_count, np.random.default_rng(9917))
    numpy_rng = np.random.default_rng(7199)
    numpy_draws = np.column_stack(
        tuple(
            numpy_rng.multinomial(depth, law.probabilities[block], size=draw_count)
            for block in law.block_slices
        )
    )
    expected_mean = law.exact_mean
    for draws in (sequential, numpy_draws):
        mids = draws / depth
        np.testing.assert_allclose(mids.mean(axis=0), expected_mean, atol=3.5e-3, rtol=0)
        for block, expected_covariance in zip(
            law.block_slices, law.covariance_blocks, strict=True
        ):
            empirical = np.cov(mids[:, block], rowvar=False, ddof=0)
            np.testing.assert_allclose(
                empirical, expected_covariance, atol=2.5e-3, rtol=0
            )
    np.testing.assert_allclose(
        sequential.mean(axis=0), numpy_draws.mean(axis=0), atol=8e-3, rtol=0
    )

    alphabet = _alphabet(depth)
    expected_pmf = np.exp(law.log_pmf(alphabet))
    observed = {
        tuple(row): count / draw_count
        for row, count in zip(
            *np.unique(sequential, axis=0, return_counts=True), strict=True
        )
    }
    empirical_pmf = np.asarray([observed.get(tuple(row), 0.0) for row in alphabet])
    np.testing.assert_allclose(empirical_pmf, expected_pmf, atol=3.5e-3, rtol=0)


def test_extended_likelihood_ratio_does_not_silently_define_zero_over_zero():
    numerator = _law(Q, name="q1")
    denominator = _law(Q, name="q2")
    forbidden = np.array([[1, 1, 0, 1, 1]])
    with pytest.raises(ValueError, match="both selected laws have zero PMF"):
        numerator.likelihood_ratio_score(denominator, forbidden)
    allowed = np.array([[0, 2, 0, 0, 2]])
    assert numerator.likelihood_ratio_score(denominator, allowed)[0] == 0.0


def test_exact_mean_and_covariance_match_enumeration():
    law = _law(depth=3)
    alphabet = _alphabet(3)
    pmf = np.exp(law.log_pmf(alphabet))
    mids = alphabet / 3.0
    mean = pmf @ mids
    np.testing.assert_allclose(mean, law.exact_mean, rtol=0.0, atol=2e-15)
    for block, expected in zip(law.block_slices, law.covariance_blocks, strict=True):
        centered = mids[:, block] - mean[block]
        enumerated = (centered * pmf[:, None]).T @ centered
        np.testing.assert_allclose(enumerated, expected, rtol=0.0, atol=3e-15)


def test_kl_orientations_and_product_tensorization():
    finite = categorical_kl_divergence([0.0, 1.0], [0.25, 0.75])
    assert finite == pytest.approx(math.log(4.0 / 3.0))
    assert categorical_kl_divergence([0.25, 0.75], [0.0, 1.0]) == math.inf
    one = product_multinomial_kl_divergence(Q, P, BLOCK_SIZES, 1)
    four = product_multinomial_kl_divergence(Q, P, BLOCK_SIZES, 4)
    assert four == pytest.approx(4.0 * one)
    assert product_multinomial_kl_divergence(P, Q, BLOCK_SIZES, 1) == math.inf
    q_law = _law(Q, depth=4, name="q")
    p_law = _law(P, depth=4, name="p")
    assert q_law.kl_divergence(p_law) == pytest.approx(four)
    assert p_law.kl_divergence(q_law) == math.inf
    assert q_law.renyi_divergence(p_law, 0.5) == pytest.approx(
        product_multinomial_renyi_divergence(Q, P, BLOCK_SIZES, 4, 0.5)
    )


@pytest.mark.parametrize("order", [0.1, 0.5, 0.9, 1.1, 2.0, 5.0])
def test_analytic_renyi_matches_enumeration_and_depth_tensorization(order):
    # P has full support, so D(Q||P) is finite above and below one.
    q_law = _law(Q, depth=2, name="q")
    p_law = _law(P, depth=2, name="p")
    alphabet = _alphabet(2)
    q_pmf = np.exp(q_law.log_pmf(alphabet))
    p_pmf = np.exp(p_law.log_pmf(alphabet))
    affinity = np.sum(
        np.power(q_pmf[q_pmf > 0], order)
        * np.power(p_pmf[q_pmf > 0], 1.0 - order)
    )
    enumerated = math.log(float(affinity)) / (order - 1.0)
    analytic = product_multinomial_renyi_divergence(
        Q, P, BLOCK_SIZES, 2, order
    )
    assert analytic == pytest.approx(enumerated, rel=2e-13, abs=2e-13)
    categorical_sum = sum(
        categorical_renyi_divergence(Q[block], P[block], order)
        for block in q_law.block_slices
    )
    assert analytic == pytest.approx(2.0 * categorical_sum, abs=2e-14)
    assert product_multinomial_renyi_divergence(
        Q, P, BLOCK_SIZES, 4, order
    ) == pytest.approx(2.0 * analytic, abs=2e-13)


def test_renyi_above_one_obeys_absolute_continuity_domain():
    assert product_multinomial_renyi_divergence(
        P, Q, BLOCK_SIZES, 2, 1.1
    ) == math.inf
    assert math.isfinite(
        product_multinomial_renyi_divergence(Q, P, BLOCK_SIZES, 2, 1.1)
    )


@pytest.mark.parametrize("order", [0.25, 0.5, 0.75])
def test_log_likelihood_ratio_moments_match_enumeration(order):
    depth = 2
    p_law = _law(P, depth=depth, name="p")
    q_law = _law(Q, depth=depth, name="q")
    alphabet = _alphabet(depth)
    p_log = p_law.log_pmf(alphabet)
    q_log = q_law.log_pmf(alphabet)
    finite_q = np.isfinite(q_log)
    null_enumerated = np.sum(
        np.exp(p_log[finite_q] + order * (q_log[finite_q] - p_log[finite_q]))
    )
    null_analytic = math.exp(
        product_multinomial_log_lr_moment(
            P, Q, P, BLOCK_SIZES, depth, order
        )
    )
    assert null_analytic == pytest.approx(null_enumerated, rel=2e-13)
    alternative_enumerated = np.sum(
        np.exp(q_log[finite_q] + (order - 1.0) * (q_log[finite_q] - p_log[finite_q]))
    )
    alternative_analytic = math.exp(
        product_multinomial_log_lr_moment(
            Q, Q, P, BLOCK_SIZES, depth, order - 1.0
        )
    )
    assert alternative_analytic == pytest.approx(alternative_enumerated, rel=2e-13)


def test_exact_support_probability_union_and_zero_beta_rule():
    null = _law(P, depth=2, name="p")
    q1 = _law(Q, depth=2, name="q1")
    q2 = _law(np.array([0.0, 1.0, 0.0, 0.4, 0.6]), depth=2, name="q2")
    masks = tuple(q1.probabilities[block] > 0 for block in q1.block_slices)
    expected_one = (0.75**2) * (0.7**2)
    assert support_event_probability(null, masks) == pytest.approx(expected_one)
    alphabet = _alphabet(2)
    exact_union = np.sum(
        np.exp(null.log_pmf(alphabet))
        * np.logical_or(q1.support_contains(alphabet), q2.support_contains(alphabet))
    )
    assert alternative_support_union_probability(null, (q1, q2)) == pytest.approx(
        exact_union, abs=2e-15
    )
    rule = AlternativeSupportUnionTest((q1, q2))
    assert np.array_equal(
        rule.decision_probability(alphabet),
        np.logical_or(q1.support_contains(alphabet), q2.support_contains(alphabet)),
    )
    assert np.sum(np.exp(q1.log_pmf(alphabet)) * (1 - rule.decision_probability(alphabet))) == 0


def test_family_proposal_importance_rows_are_memberwise_and_deterministic():
    null = ProductMultinomialFamily(
        ("p0", "p1"), BLOCK_NAMES, BLOCK_SIZES, np.vstack((P, P)), 2
    )
    alternatives = ProductMultinomialFamily(
        ("q0", "q1"),
        BLOCK_NAMES,
        BLOCK_SIZES,
        np.vstack((Q, np.array([0.1, 0.9, 0.0, 0.4, 0.6]))),
        2,
    )
    one = build_balanced_multinomial_proposal_support(
        null, alternatives, support_size=2_000, seed=711
    )
    two = build_balanced_multinomial_proposal_support(
        null, alternatives, support_size=2_000, seed=711
    )
    np.testing.assert_array_equal(one.observations, two.observations)
    # Duplicate p0/p1 is removed; class mass remains exactly balanced.
    assert one.component_class_labels.count("null") == 1
    assert np.sum(one.component_weights[np.array(one.component_class_labels) == "null"]) == pytest.approx(0.5)
    null_rows = multinomial_importance_discretize(null, one)
    alternative_rows = multinomial_importance_discretize(alternatives, one)
    assert null_rows.weights.shape == (2, 2_000)
    assert alternative_rows.weights.shape == (2, 2_000)
    np.testing.assert_allclose(np.sum(null_rows.weights, axis=1), 1.0, atol=2e-15)
    assert np.min(null_rows.effective_sample_sizes) > 0


def test_duplicate_observable_panels_are_consolidated_before_the_lp():
    family = ProductMultinomialFamily(
        ("p",), BLOCK_NAMES, BLOCK_SIZES, P[np.newaxis, :], 2
    )
    first = np.array([1, 1, 0, 1, 1])
    second = np.array([0, 2, 2, 0, 0])
    observations = np.vstack((first, first, second))
    law = family.law(0)
    support = DiscreteCommonProposalSupport(
        observations=observations,
        proposal_log_pmf=law.log_pmf(observations),
        component_member_ids=("p",),
        component_class_labels=("null",),
        component_weights=np.array([1.0]),
        component_laws=(law,),
        sampled_component_indices=np.array([0, 0, 0]),
        seed=99,
    )
    discretization = multinomial_importance_discretize(family, support)
    np.testing.assert_allclose(
        discretization.weights[0], np.array([2.0 / 3.0, 0.0, 1.0 / 3.0])
    )
    assert discretization.raw_sample_count == 3
    assert discretization.unique_observation_count == 2
    assert discretization.duplicate_observation_count == 1
    assert discretization.effective_sample_sizes[0] == pytest.approx(3.0)
    assert discretization.consolidated_effective_sample_sizes[0] == pytest.approx(1.8)


def test_corrupted_proposal_density_fails_component_mixture_recomputation():
    null = ProductMultinomialFamily(
        ("p",), BLOCK_NAMES, BLOCK_SIZES, P[np.newaxis, :], 2
    )
    alternative = ProductMultinomialFamily(
        ("q",), BLOCK_NAMES, BLOCK_SIZES, Q[np.newaxis, :], 2
    )
    support = build_balanced_multinomial_proposal_support(
        null, alternative, support_size=500, seed=1771
    )
    corrupted = np.array(support.proposal_log_pmf, copy=True)
    corrupted[0] += 5.0
    with pytest.raises(MinimaxNumericalError, match="component-mixture"):
        replace(support, proposal_log_pmf=corrupted)


def test_compensated_importance_weight_corruption_fails_integrity_hash():
    null = ProductMultinomialFamily(
        ("p",), BLOCK_NAMES, BLOCK_SIZES, P[np.newaxis, :], 2
    )
    alternative = ProductMultinomialFamily(
        ("q",), BLOCK_NAMES, BLOCK_SIZES, Q[np.newaxis, :], 2
    )
    support = build_balanced_multinomial_proposal_support(
        null, alternative, support_size=500, seed=1772
    )
    discretization = multinomial_importance_discretize(null, support)
    corrupted = np.array(discretization.weights, copy=True)
    positive = np.flatnonzero(corrupted[0] > 0.0)
    assert len(positive) >= 2
    source, destination = int(positive[0]), int(positive[1])
    shift = min(1.0e-5, 0.25 * corrupted[0, source])
    corrupted[0, source] -= shift
    corrupted[0, destination] += shift
    assert np.sum(corrupted[0]) == pytest.approx(1.0)
    with pytest.raises(MinimaxNumericalError, match="integrity hash"):
        replace(discretization, weights=corrupted)


def test_deployable_dual_rule_accepts_an_unseen_count_panel():
    null = ProductMultinomialFamily(("p",), BLOCK_NAMES, BLOCK_SIZES, P[None, :], 2)
    alternative = ProductMultinomialFamily(("q",), BLOCK_NAMES, BLOCK_SIZES, Q[None, :], 2)
    support = build_balanced_multinomial_proposal_support(
        null, alternative, support_size=5_000, seed=815
    )
    p_rows = multinomial_importance_discretize(null, support)
    q_rows = multinomial_importance_discretize(alternative, support)
    solution = solve_finite_minimax(p_rows.weights, q_rows.weights, epsilon=0.05)
    representation = build_product_multinomial_mixture_test(
        solution, null, alternative, p_rows, q_rows, support,
        reproduction_tolerance=5e-3,
    )
    unseen = np.array([[2, 0, 2, 0, 0]])
    probability = representation.test.decision_probability(unseen)
    assert probability.shape == (1,)
    assert 0.0 <= probability[0] <= 1.0
    assert not hasattr(representation.test, "state_id")


def test_identical_laws_have_unavoidable_pointwise_minimax_floor():
    law = _law(depth=1)
    alphabet = _alphabet(1)
    row = np.exp(law.log_pmf(alphabet))[None, :]
    solution = solve_finite_minimax(row, row, epsilon=0.05)
    assert solution.worst_case_type_i == pytest.approx(0.05, abs=2e-9)
    assert solution.worst_case_type_ii == pytest.approx(0.95, abs=2e-9)
