"""Focused tests for the observable-law-only K-way minimax engine."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pytest

import fluxemu.composite_multihypothesis as multi


@dataclass(frozen=True)
class _MIDClass:
    member_ids: tuple[str, ...]
    blocks: tuple[tuple[str, int, int], ...]
    exact_mids: np.ndarray


def _family(
    identifiers: tuple[str, ...],
    centres: list[tuple[float, float]],
    *,
    noise: float = 0.08,
) -> multi.ProductDirichletFamily:
    return multi.family_from_mid_class(
        _MIDClass(
            member_ids=identifiers,
            blocks=(("X", 0, 2),),
            exact_mids=np.asarray(centres, dtype=float),
        ),
        rms_noise=noise,
    )


def test_balanced_proposal_is_global_setwise_and_keeps_member_mapping() -> None:
    first = _family(("a0", "a1", "a0-copy"), [(0.2, 0.8), (0.3, 0.7), (0.2, 0.8)])
    second = _family(("b0", "shared"), [(0.7, 0.3), (0.3, 0.7)])
    third = _family(("c0",), [(0.8, 0.2)])
    support = multi.build_balanced_proposal_support(
        (first, second, third),
        support_size=600,
        seed=20260808,
        class_labels=("A", "B", "C"),
    )
    assert support.class_labels == ("A", "B", "C")
    assert support.unique_component_counts_by_class == (2, 2, 1)
    assert support.proposal_component_count == 4
    assert support.member_component_indices[0][0] == support.member_component_indices[0][2]
    assert support.member_component_indices[0][1] == support.member_component_indices[1][1]
    assert np.sum(support.component_class_masses, axis=1) == pytest.approx(
        np.full(3, 1.0 / 3.0), abs=2e-15
    )
    assert np.all(support.proposal_component_weights > 0.0)
    realized = np.bincount(
        support.sampled_component_indices,
        minlength=support.proposal_component_count,
    )
    assert np.max(
        np.abs(realized - support.support_size * support.proposal_component_weights)
    ) < 1.0


def test_randomized_systematic_components_balance_full_support_and_prefixes() -> None:
    weights = np.asarray([0.03, 0.17, 0.31, 0.49])
    support_size = 37
    prefix_size = 7
    prefix_counts = np.zeros(len(weights), dtype=float)
    for seed in range(2_000):
        sampled = multi._randomized_systematic_component_indices(
            weights, support_size, np.random.default_rng(seed)
        )
        counts = np.bincount(sampled, minlength=len(weights))
        assert np.max(np.abs(counts - support_size * weights)) < 1.0
        prefix_counts += np.bincount(
            sampled[:prefix_size], minlength=len(weights)
        )

    # The random permutation makes every prefix a random subset of the
    # systematically balanced multiset.  This deterministic many-seed check
    # guards that marginal without asserting independence between rows.
    observed_prefix_frequencies = prefix_counts / (2_000 * prefix_size)
    assert observed_prefix_frequencies == pytest.approx(weights, abs=4.0e-3)

    first = multi._randomized_systematic_component_indices(
        weights, support_size, np.random.default_rng(808)
    )
    repeated = multi._randomized_systematic_component_indices(
        weights, support_size, np.random.default_rng(808)
    )
    assert np.array_equal(first, repeated)


def test_proposal_and_lp_objective_ignore_duplicate_member_frequency() -> None:
    unique = _family(("a0", "a1"), [(0.2, 0.8), (0.3, 0.7)])
    duplicated = _family(
        ("a0", "a1", "a0-copy", "a0-copy-2"),
        [(0.2, 0.8), (0.3, 0.7), (0.2, 0.8), (0.2, 0.8)],
    )
    second = _family(("b0",), [(0.55, 0.45)])
    third = _family(("c0",), [(0.8, 0.2)])
    one = multi.build_balanced_proposal_support(
        (unique, second, third), support_size=800, seed=91
    )
    two = multi.build_balanced_proposal_support(
        (duplicated, second, third), support_size=800, seed=91
    )
    assert np.array_equal(one.observations, two.observations)
    assert np.array_equal(one.log_proposal_density, two.log_proposal_density)
    assert np.array_equal(one.proposal_component_weights, two.proposal_component_weights)

    rows = multi.discretize_families((unique, second, third), one)
    duplicate_rows = multi.discretize_families((duplicated, second, third), two)
    baseline = multi.solve_finite_minimax(tuple(item.weights for item in rows))
    attacked = multi.solve_finite_minimax(tuple(item.weights for item in duplicate_rows))
    assert attacked.primal_objective == pytest.approx(baseline.primal_objective, abs=2e-10)


def test_proposal_draw_is_invariant_to_member_reordering_and_duplication() -> None:
    ordered = _family(("a0", "a1"), [(0.2, 0.8), (0.3, 0.7)])
    reordered = _family(
        ("a1-copy", "a0", "a1"),
        [(0.3, 0.7), (0.2, 0.8), (0.3, 0.7)],
    )
    second = _family(("b0",), [(0.55, 0.45)])
    third = _family(("c0",), [(0.8, 0.2)])
    baseline = multi.build_balanced_proposal_support(
        (ordered, second, third), support_size=800, seed=177
    )
    attacked = multi.build_balanced_proposal_support(
        (reordered, second, third), support_size=800, seed=177
    )
    assert np.array_equal(baseline.proposal_component_weights, attacked.proposal_component_weights)
    assert np.array_equal(baseline.sampled_component_indices, attacked.sampled_component_indices)
    assert np.array_equal(baseline.observations, attacked.observations)
    assert np.array_equal(baseline.log_proposal_density, attacked.log_proposal_density)


def test_importance_rows_are_individually_normalized() -> None:
    families = (
        _family(("a0", "a1"), [(0.2, 0.8), (0.3, 0.7)]),
        _family(("b0",), [(0.6, 0.4)]),
        _family(("c0",), [(0.8, 0.2)]),
    )
    support = multi.build_balanced_proposal_support(families, support_size=900, seed=3)
    discretizations = multi.discretize_families(families, support)
    for discretization in discretizations:
        assert np.sum(discretization.weights, axis=1) == pytest.approx(
            np.ones(discretization.member_count), abs=2e-12
        )
        assert np.all(discretization.raw_mass_estimates > 0.0)
        assert np.all(discretization.effective_sample_sizes > 0.0)


def test_finite_k_way_lp_has_memberwise_constraints_and_correct_dual() -> None:
    classes = (
        np.asarray([[0.8, 0.2, 0.0], [0.3, 0.7, 0.0]]),
        np.asarray([[0.0, 0.7, 0.3], [0.1, 0.2, 0.7]]),
        np.asarray([[0.6, 0.0, 0.4], [0.2, 0.1, 0.7]]),
    )
    solution = multi.solve_finite_minimax(classes, class_labels=("A", "B", "C"))
    assert solution.decision_probabilities.shape == (3, 3)
    assert np.sum(solution.decision_probabilities, axis=0) == pytest.approx(np.ones(3), abs=2e-10)
    for class_index, rows in enumerate(classes):
        expected = rows @ (1.0 - solution.decision_probabilities[class_index])
        assert np.array_equal(solution.member_errors[class_index], expected)
        assert len(solution.member_errors[class_index]) == len(rows)
        assert np.max(expected) <= solution.primal_objective + 2e-9
    assert np.sum(solution.dual_class_weights) == pytest.approx(1.0, abs=2e-9)
    reconstructed = 1.0 - np.sum(np.max(solution.dual_scores, axis=0))
    assert solution.dual_objective == pytest.approx(reconstructed, abs=2e-12)
    assert solution.primal_objective == pytest.approx(solution.dual_objective, abs=2e-8)
    assert solution.absolute_duality_residual < 2e-8


def test_free_t_allows_zero_risk_disjoint_support_solution() -> None:
    classes = (
        np.asarray([[1.0, 0.0, 0.0]]),
        np.asarray([[0.0, 1.0, 0.0]]),
        np.asarray([[0.0, 0.0, 1.0]]),
    )
    solution = multi.solve_finite_minimax(classes)
    assert solution.primal_objective == pytest.approx(0.0, abs=2e-10)
    assert solution.global_worst_error == pytest.approx(0.0, abs=2e-10)
    assert solution.dual_objective == pytest.approx(0.0, abs=2e-10)
    assert np.sum(solution.dual_class_weights) == pytest.approx(1.0, abs=2e-9)


def test_nonzero_pruning_retains_a_separate_dense_certificate() -> None:
    epsilon = 1.0e-8
    classes = (
        np.asarray([[1.0 - epsilon, epsilon, 0.0]]),
        np.asarray([[0.0, 1.0 - epsilon, epsilon]]),
        np.asarray([[epsilon, 0.0, 1.0 - epsilon]]),
    )
    solution = multi.solve_finite_minimax(
        classes,
        probability_weight_pruning_cutoff=1.0e-7,
        maximum_pruned_row_mass=2.0e-8,
    )
    assert solution.primal_objective == pytest.approx(0.0, abs=2.0e-12)
    assert np.all(solution.maximum_pruned_row_masses > 0.0)
    assert solution.dense_primal_upper_bound == pytest.approx(epsilon, abs=2.0e-15)
    assert solution.raw_dense_dual_lower_bound == pytest.approx(epsilon, abs=2.0e-15)
    assert solution.dense_certificate_gap == pytest.approx(0.0, abs=2.0e-15)
    assert solution.dense_objective_recomputation_error == pytest.approx(
        epsilon, abs=2.0e-15
    )


def test_direct_lp_recovers_six_class_identical_law_t0() -> None:
    rng = np.random.default_rng(771)
    laws = rng.dirichlet(np.ones(80), size=5)
    solution = multi.solve_finite_minimax(
        (laws,) * 6,
        class_labels=("G_A", "G_B", "G_C", "G_AB", "G_AC", "G_BC"),
        identical_class_shortcut=False,
    )
    assert solution.primal_objective == pytest.approx(5.0 / 6.0, abs=2e-9)
    assert solution.global_worst_error == pytest.approx(5.0 / 6.0, abs=2e-9)
    assert solution.dual_objective == pytest.approx(5.0 / 6.0, abs=2e-9)
    assert solution.absolute_duality_residual < 2e-8


def test_generic_solver_automatically_certifies_duplicated_identical_classes() -> None:
    first = np.asarray([0.7, 0.2, 0.1])
    second = np.asarray([0.1, 0.3, 0.6])
    classes = (
        np.asarray([first, second, first]),
        np.asarray([second, first]),
        np.asarray([first, second, second, second]),
        np.asarray([second, first]),
        np.asarray([first, second]),
        np.asarray([second, first, first]),
    )
    solution = multi.solve_finite_minimax(classes)
    assert solution.primal_objective == 5.0 / 6.0
    assert solution.global_worst_error == pytest.approx(5.0 / 6.0, abs=2e-16)
    assert tuple(len(values) for values in solution.member_errors) == (
        3,
        2,
        4,
        2,
        2,
        3,
    )
    assert all(
        np.allclose(values, np.full(len(values), 5.0 / 6.0), rtol=0.0, atol=2e-16)
        for values in solution.member_errors
    )
    assert "exact identical-K" in solution.solver_message


def test_exact_identical_k_helper_is_setwise_and_uniform() -> None:
    first = np.asarray([0.7, 0.2, 0.1])
    second = np.asarray([0.1, 0.3, 0.6])
    classes = (
        np.asarray([first, second, first]),
        np.asarray([second, first]),
        np.asarray([first, second, second, second]),
        np.asarray([second, first]),
        np.asarray([first, second]),
        np.asarray([second, first, first]),
    )
    solution = multi.solve_identical_classes_exact(classes)
    assert solution.primal_objective == 5.0 / 6.0
    assert solution.dual_objective == pytest.approx(5.0 / 6.0, abs=2e-16)
    assert np.array_equal(solution.decision_probabilities, np.full((6, 3), 1.0 / 6.0))
    assert solution.dual_class_weights == pytest.approx(np.full(6, 1.0 / 6.0), abs=0.0)
    assert len(solution.randomized_support_indices) == 3
    assert "optimizer not invoked" in solution.solver_message

    average_only = list(classes)
    average_only[-1] = np.asarray([[0.4, 0.25, 0.35]])
    with pytest.raises(ValueError, match="not exactly identical"):
        multi.solve_identical_classes_exact(tuple(average_only))


def test_batched_risk_evaluation_matches_materialized_rows_and_selection() -> None:
    validation = _family(
        tuple(f"a{index}" for index in range(7)),
        [(0.20 + 0.025 * index, 0.80 - 0.025 * index) for index in range(7)],
    )
    other = _family(("b0", "b1"), [(0.6, 0.4), (0.7, 0.3)])
    third = _family(("c0",), [(0.82, 0.18)])
    support = multi.build_balanced_proposal_support(
        (validation, other, third), support_size=1100, seed=122
    )
    decision = np.linspace(0.0, 1.0, support.support_size)
    full = multi.importance_discretize(validation, support)
    selected = np.asarray([0, 2, 5, 6])
    batched = multi.evaluate_member_risks(
        validation,
        support,
        decision,
        member_indices=selected,
        batch_size=2,
    )
    assert np.array_equal(batched.member_indices, selected)
    assert batched.risks == pytest.approx(full.weights[selected] @ (1.0 - decision), abs=2e-14)
    assert batched.raw_mass_estimates == pytest.approx(full.raw_mass_estimates[selected], rel=2e-14)
    selected_rows = multi.discretize_selected_members(validation, support, selected)
    assert selected_rows.weights == pytest.approx(full.weights[selected], abs=2e-14)


def test_sparse_importance_discretization_matches_dense_rows_with_audited_pruning() -> None:
    families = (
        _family(("a0", "a1"), [(0.2, 0.8), (0.3, 0.7)]),
        _family(("b0",), [(0.6, 0.4)]),
        _family(("c0",), [(0.8, 0.2)]),
    )
    support = multi.build_balanced_proposal_support(
        families, support_size=900, seed=319
    )
    dense = multi.importance_discretize(families[0], support)
    sparse_rows = multi.importance_discretize_sparse(
        families[0],
        support,
        member_batch_size=1,
        probability_weight_pruning_cutoff=1.0e-15,
        maximum_pruned_row_mass=1.0e-10,
    )
    assert sparse_rows.weights.toarray() == pytest.approx(dense.weights, abs=1.0e-15)
    assert sparse_rows.raw_mass_estimates == pytest.approx(
        dense.raw_mass_estimates, rel=2.0e-14
    )
    assert sparse_rows.effective_sample_sizes == pytest.approx(
        dense.effective_sample_sizes, rel=2.0e-14
    )
    assert sparse_rows.maximum_pruned_row_mass <= 1.0e-10


def test_k_way_constraint_generation_adds_individual_cycle_constraints() -> None:
    initial = (
        np.asarray([[1.0, 0.0, 0.0]]),
        np.asarray([[0.0, 1.0, 0.0]]),
        np.asarray([[0.0, 0.0, 1.0]]),
    )
    validation = (
        np.asarray([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]),
        np.asarray([[0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]),
        np.asarray([[0.0, 0.0, 1.0], [1.0, 0.0, 0.0]]),
    )
    generated = multi.run_constraint_generation(
        initial,
        validation,
        class_labels=("A", "B", "C"),
        violation_tolerance=1.0e-9,
        near_worst_tolerance=0.0,
        maximum_additions_per_class=2,
        max_iterations=8,
        shared_alias_feasibility_slack=0.0,
    )
    assert generated.converged
    assert all(1 in values for values in generated.selected_validation_indices)
    assert max(np.max(values) for values in generated.validation_errors) <= (
        generated.solution.primal_objective + 1.0e-9
    )
    assert generated.solution.primal_objective == pytest.approx(0.5, abs=2.0e-9)


def test_continuous_k_way_rule_is_mid_only_and_uniform_on_identical_scores() -> None:
    family = _family(("m0",), [(0.35, 0.65)], noise=0.04)
    families = (family, family, family)
    support = multi.build_balanced_proposal_support(
        families, support_size=500, seed=717, class_labels=("A", "B", "C")
    )
    discretizations = multi.discretize_families(families, support)
    solution = multi.solve_identical_classes_exact(
        tuple(item.weights for item in discretizations),
        class_labels=("A", "B", "C"),
    )
    diagnostics = multi.build_continuous_multiclass_rule(
        solution, families, discretizations, support, reproduction_tolerance=1.0e-12
    )
    assert diagnostics.stable_on_finite_support
    observations = family.sample_member(0, 9, np.random.default_rng(817))
    assert diagnostics.rule.decision_probabilities(observations) == pytest.approx(
        np.full((9, 3), 1.0 / 3.0), abs=2.0e-15
    )
    assert tuple(
        __import__("inspect").signature(
            multi.ContinuousMulticlassDecisionRule.decision_probabilities
        ).parameters
    ) == ("self", "observations")
