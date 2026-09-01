"""Focused tests for the generic MID-only composite minimax solver."""

from __future__ import annotations

from dataclasses import dataclass
import inspect

import numpy as np
import pytest

import fluxemu.composite_mid_minimax as minimax_module
from fluxemu.composite_mid_minimax import (
    ContinuousMixtureTest,
    build_balanced_proposal_support,
    build_continuous_mixture_test,
    concatenate_families,
    dirichlet_rms_kappa,
    family_from_mid_class,
    importance_discretize,
    run_constraint_generation,
    solve_finite_disjoint_support_minimax_exact,
    solve_finite_minimax,
    solve_identical_class_minimax_exact,
)


@dataclass(frozen=True)
class _MIDOnlyClass:
    member_ids: tuple[str, ...]
    blocks: tuple[tuple[str, int, int], ...]
    exact_mids: np.ndarray


def _family(
    identifiers: tuple[str, ...], centres: list[tuple[float, float]], noise: float = 0.08
):
    return family_from_mid_class(
        _MIDOnlyClass(
            member_ids=identifiers,
            blocks=(("synthetic", 0, 2),),
            exact_mids=np.asarray(centres, dtype=float),
        ),
        rms_noise=noise,
    )


def test_dirichlet_measurement_law_uses_established_rms_convention() -> None:
    centre = np.asarray([0.2, 0.3, 0.5])
    target = 0.005
    concentration = dirichlet_rms_kappa(centre, target)
    reproduced = np.sqrt(
        (1.0 - np.sum(np.square(centre)))
        / (len(centre) * (concentration + 1.0))
    )
    assert reproduced == pytest.approx(target, abs=1.0e-15)


def test_common_proposal_is_shared_stable_and_rows_are_self_normalised() -> None:
    null = _family(("n0", "n1"), [(0.35, 0.65), (0.42, 0.58)])
    alternative = _family(("q0", "q1"), [(0.58, 0.42), (0.65, 0.35)])
    support = build_balanced_proposal_support(
        null, alternative, support_size=1200, seed=20260808
    )
    null_discretization = importance_discretize(null, support)
    alternative_discretization = importance_discretize(alternative, support)
    assert support.observations.shape == (1200, 2)
    assert np.allclose(
        np.sum(null_discretization.weights, axis=1), 1.0, atol=2.0e-12
    )
    assert np.allclose(
        np.sum(alternative_discretization.weights, axis=1), 1.0, atol=2.0e-12
    )
    assert np.all(null_discretization.raw_mass_estimates > 0.0)
    assert np.all(alternative_discretization.raw_mass_estimates > 0.0)
    assert null_discretization.minimum_effective_sample_size > 1.0
    assert alternative_discretization.minimum_effective_sample_size > 1.0


def test_proposal_deduplicates_laws_so_row_frequency_does_not_change_support() -> None:
    unique_null = _family(("n0", "n1"), [(0.35, 0.65), (0.42, 0.58)])
    duplicated_null = _family(
        ("n0", "n1", "n0-copy", "n1-copy"),
        [(0.35, 0.65), (0.42, 0.58), (0.35, 0.65), (0.42, 0.58)],
    )
    alternative = _family(("q0",), [(0.62, 0.38)])
    first = build_balanced_proposal_support(
        unique_null, alternative, support_size=500, seed=89
    )
    second = build_balanced_proposal_support(
        duplicated_null, alternative, support_size=500, seed=89
    )
    assert first.unique_null_component_count == 2
    assert second.unique_null_component_count == 2
    assert np.array_equal(first.observations, second.observations)
    assert np.array_equal(first.log_proposal_density, second.log_proposal_density)
    assert np.array_equal(
        first.sampled_component_indices, second.sampled_component_indices
    )
    assert np.array_equal(
        first.proposal_component_weights, second.proposal_component_weights
    )


def test_adaptive_focus_retains_base_coverage_and_splits_focus_by_side() -> None:
    null = _family(("n0", "n1"), [(0.25, 0.75), (0.35, 0.65)])
    alternative = _family(("q0", "q1"), [(0.65, 0.35), (0.75, 0.25)])
    focused = build_balanced_proposal_support(
        null,
        alternative,
        support_size=600,
        seed=908,
        focus_mass=0.5,
        null_focus_indices=(1,),
        alternative_focus_indices=(0,),
    )
    # Half the proposal remains uniform base coverage and half is focused;
    # both allocations are independently split 50/50 between class sides.
    assert focused.proposal_component_weights == pytest.approx(
        [0.125, 0.375, 0.375, 0.125], abs=1.0e-15
    )
    assert np.sum(focused.proposal_component_weights[:2]) == pytest.approx(0.5)
    assert np.sum(focused.proposal_component_weights[2:]) == pytest.approx(0.5)
    assert np.all(focused.proposal_component_weights > 0.0)
    assert focused.focus_mass == 0.5
    assert focused.focused_null_component_count == 1
    assert focused.focused_alternative_component_count == 1


def test_adaptive_focus_is_invariant_to_duplicate_rows_and_focus_frequency() -> None:
    unique_null = _family(("n0", "n1"), [(0.25, 0.75), (0.35, 0.65)])
    duplicated_null = _family(
        ("n0", "n1", "n0-copy", "n1-copy"),
        [(0.25, 0.75), (0.35, 0.65), (0.25, 0.75), (0.35, 0.65)],
    )
    alternative = _family(("q0", "q1"), [(0.65, 0.35), (0.75, 0.25)])
    first = build_balanced_proposal_support(
        unique_null,
        alternative,
        support_size=700,
        seed=909,
        focus_mass=0.5,
        null_focus_indices=(1,),
        alternative_focus_indices=(0,),
    )
    second = build_balanced_proposal_support(
        duplicated_null,
        alternative,
        support_size=700,
        seed=909,
        focus_mass=0.5,
        null_focus_indices=(1, 3, 1, 3),
        alternative_focus_indices=(0, 0, 0),
    )
    assert second.focused_null_component_count == 1
    assert second.focused_alternative_component_count == 1
    assert np.array_equal(first.proposal_component_weights, second.proposal_component_weights)
    assert np.array_equal(first.sampled_component_indices, second.sampled_component_indices)
    assert np.array_equal(first.observations, second.observations)
    assert np.array_equal(first.log_proposal_density, second.log_proposal_density)


def test_zero_focus_keeps_default_proposal_bit_for_bit_and_positive_focus_needs_both_sides() -> None:
    null = _family(("n0",), [(0.35, 0.65)])
    alternative = _family(("q0",), [(0.65, 0.35)])
    default = build_balanced_proposal_support(
        null, alternative, support_size=300, seed=910
    )
    explicit_zero = build_balanced_proposal_support(
        null,
        alternative,
        support_size=300,
        seed=910,
        focus_mass=0.0,
        null_focus_indices=(0,),
        alternative_focus_indices=(0,),
    )
    assert np.array_equal(default.observations, explicit_zero.observations)
    assert np.array_equal(
        default.log_proposal_density, explicit_zero.log_proposal_density
    )
    assert np.array_equal(
        default.proposal_component_weights,
        explicit_zero.proposal_component_weights,
    )
    with pytest.raises(ValueError, match="focus laws on both sides"):
        build_balanced_proposal_support(
            null,
            alternative,
            support_size=30,
            seed=911,
            focus_mass=0.5,
            null_focus_indices=(0,),
        )


def test_identical_composite_classes_recover_exact_orientation_control() -> None:
    rng = np.random.default_rng(47)
    laws = rng.dirichlet(np.ones(75), size=9)
    solution = solve_finite_minimax(laws, laws, epsilon=0.05)
    assert solution.beta_objective == pytest.approx(0.95, abs=2.0e-9)
    assert solution.worst_case_type_i <= 0.05 + 2.0e-9
    assert solution.worst_case_type_ii == pytest.approx(0.95, abs=2.0e-9)
    assert solution.dual_objective == pytest.approx(0.95, abs=2.0e-9)
    assert solution.absolute_duality_gap < 2.0e-8
    assert np.sum(solution.alternative_dual_multipliers) == pytest.approx(
        1.0, abs=2.0e-8
    )


def test_exact_identical_class_helper_returns_constant_primal_and_matched_dual() -> None:
    rng = np.random.default_rng(470)
    null_laws = rng.dirichlet(np.ones(40), size=5)
    permutation = np.asarray([3, 0, 4, 1, 2])
    alternative_laws = null_laws[permutation]
    solution = solve_identical_class_minimax_exact(
        null_laws, alternative_laws, epsilon=0.05
    )
    assert np.array_equal(
        solution.decision_probabilities,
        np.full(null_laws.shape[1], 0.05),
    )
    assert solution.beta_objective == 0.95
    assert solution.dual_objective == 0.95
    assert solution.absolute_duality_gap == 0.0
    assert solution.worst_case_type_i == pytest.approx(0.05, abs=2.0e-16)
    assert solution.worst_case_type_ii == pytest.approx(0.95, abs=1.0e-14)
    assert len(solution.active_null_indices) == len(null_laws)
    assert len(solution.active_alternative_indices) == len(alternative_laws)
    assert len(solution.fractional_support_indices) == null_laws.shape[1]
    assert len(solution.dual_tie_support_indices) == null_laws.shape[1]
    assert len(solution.dual_supported_null_indices) == 1
    assert len(solution.dual_supported_alternative_indices) == 1
    null_index = int(solution.dual_supported_null_indices[0])
    alternative_index = int(solution.dual_supported_alternative_indices[0])
    assert np.array_equal(null_laws[null_index], alternative_laws[alternative_index])
    assert "optimizer not invoked" in solution.solver_message


def test_exact_identical_class_helper_ignores_duplicate_frequency_but_not_class_members() -> None:
    first = np.asarray([0.7, 0.2, 0.1])
    second = np.asarray([0.1, 0.3, 0.6])
    null_laws = np.asarray([first, second, first, first])
    same_set_different_frequency = np.asarray([second, second, first])
    solution = solve_identical_class_minimax_exact(
        null_laws, same_set_different_frequency, epsilon=0.05
    )
    assert solution.beta_objective == 0.95
    # These two classes have the same average but not the same member set.
    average_only_null = np.asarray([[0.8, 0.2], [0.2, 0.8]])
    average_only_alternative = np.asarray([[0.5, 0.5]])
    assert np.array_equal(
        np.mean(average_only_null, axis=0), average_only_alternative[0]
    )
    with pytest.raises(ValueError, match="row sets are not exactly identical"):
        solve_identical_class_minimax_exact(
            average_only_null, average_only_alternative, epsilon=0.05
        )


def test_exact_identical_class_helper_does_not_invoke_numerical_optimizer(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    laws = np.asarray([[0.7, 0.2, 0.1], [0.1, 0.3, 0.6]])

    def fail_if_called(*args, **kwargs):  # noqa: ANN002, ANN003
        raise AssertionError("identical-class theorem called linprog")

    monkeypatch.setattr(minimax_module, "linprog", fail_if_called)
    solution = solve_identical_class_minimax_exact(laws, laws, epsilon=0.05)
    assert solution.beta_objective == 0.95


def test_exact_finite_disjoint_support_helper_has_zero_error_certificate() -> None:
    null_laws = np.asarray(
        [
            [0.7, 0.3, 0.0, 0.0, 0.0],
            [0.2, 0.8, 0.0, 0.0, 0.0],
        ]
    )
    alternative_laws = np.asarray(
        [
            [0.0, 0.0, 0.6, 0.4, 0.0],
            [0.0, 0.0, 0.1, 0.2, 0.7],
        ]
    )
    solution = solve_finite_disjoint_support_minimax_exact(
        null_laws, alternative_laws, epsilon=0.05
    )
    assert np.array_equal(
        solution.decision_probabilities,
        np.asarray([0.0, 0.0, 1.0, 1.0, 1.0]),
    )
    assert solution.beta_objective == 0.0
    assert solution.worst_case_type_i == 0.0
    assert solution.worst_case_type_ii == 0.0
    assert solution.dual_objective == 0.0
    assert solution.absolute_duality_gap == 0.0
    assert len(solution.active_null_indices) == 0
    assert np.array_equal(solution.active_alternative_indices, [0, 1])
    assert len(solution.dual_supported_null_indices) == 0
    assert np.array_equal(solution.dual_supported_alternative_indices, [0])
    assert np.sum(solution.alternative_dual_multipliers) == 1.0
    assert "finite-support-only" in solution.solver_message
    assert "optimizer not invoked" in solution.solver_message


def test_exact_finite_disjoint_support_helper_rejects_any_positive_overlap() -> None:
    null_laws = np.asarray([[0.7, 0.3, 0.0, 0.0]])
    alternative_laws = np.asarray([[0.0, 1.0e-300, 0.4, 0.6 - 1.0e-300]])
    with pytest.raises(ValueError, match="positive-support unions overlap"):
        solve_finite_disjoint_support_minimax_exact(
            null_laws, alternative_laws, epsilon=0.05
        )


def test_exact_finite_disjoint_support_helper_does_not_invoke_optimizer(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    null_laws = np.asarray([[1.0, 0.0]])
    alternative_laws = np.asarray([[0.0, 1.0]])

    def fail_if_called(*args, **kwargs):  # noqa: ANN002, ANN003
        raise AssertionError("finite disjoint-support theorem called linprog")

    monkeypatch.setattr(minimax_module, "linprog", fail_if_called)
    solution = solve_finite_disjoint_support_minimax_exact(
        null_laws, alternative_laws, epsilon=0.05
    )
    assert solution.beta_objective == 0.0


def test_lp_retains_every_null_and_alternative_constraint_and_error_orientation() -> None:
    null_laws = np.asarray(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
        ]
    )
    alternative_laws = np.asarray(
        [
            [0.0, 0.0, 1.0],
            [0.5, 0.0, 0.5],
        ]
    )
    solution = solve_finite_minimax(null_laws, alternative_laws, epsilon=0.05)
    expected_type_i = null_laws @ solution.decision_probabilities
    expected_type_ii = alternative_laws @ (
        1.0 - solution.decision_probabilities
    )
    assert np.array_equal(solution.null_errors, expected_type_i)
    assert np.array_equal(solution.alternative_errors, expected_type_ii)
    assert len(solution.null_errors) == len(null_laws)
    assert len(solution.alternative_errors) == len(alternative_laws)
    assert np.max(solution.null_errors) <= 0.05 + 2.0e-9
    assert np.max(solution.alternative_errors) <= solution.beta_objective + 2.0e-9
    assert solution.objective_recomputation_error < 2.0e-9


def test_sparse_pruning_matches_unpruned_lp_and_reports_removed_mass() -> None:
    tiny = 2.0e-16
    null_laws = np.asarray(
        [
            [0.70 - tiny, 0.20, 0.10, tiny],
            [tiny, 0.65 - tiny, 0.20, 0.15],
        ]
    )
    alternative_laws = np.asarray(
        [
            [0.10, tiny, 0.25, 0.65 - tiny],
            [tiny, 0.15, 0.20, 0.65 - tiny],
        ]
    )
    unpruned = solve_finite_minimax(
        null_laws,
        alternative_laws,
        epsilon=0.05,
        probability_weight_pruning_cutoff=0.0,
        lp_constraint_scale=1.0e8,
    )
    pruned = solve_finite_minimax(
        null_laws,
        alternative_laws,
        epsilon=0.05,
        probability_weight_pruning_cutoff=1.0e-15,
    )
    assert pruned.beta_objective == pytest.approx(
        unpruned.beta_objective, abs=2.0e-12
    )
    assert pruned.worst_case_type_i == pytest.approx(
        unpruned.worst_case_type_i, abs=2.0e-12
    )
    assert pruned.worst_case_type_ii == pytest.approx(
        unpruned.worst_case_type_ii, abs=2.0e-12
    )
    assert pruned.maximum_pruned_null_row_mass <= 1.0e-15
    assert pruned.maximum_pruned_alternative_row_mass <= 1.0e-15
    assert pruned.retained_lp_coefficient_fraction < 1.0
    assert unpruned.retained_lp_coefficient_fraction == pytest.approx(1.0)
    assert pruned.lp_constraint_scale == pytest.approx(1.0e6)
    assert (
        pruned.minimum_scaled_retained_coefficient > 1.0e-9
    )
    assert pruned.absolute_duality_gap < 2.0e-8
    assert pruned.dense_dual_lower_bound <= (
        pruned.dense_feasible_type_ii_upper_bound + 2.0e-12
    )
    assert pruned.dense_certificate_gap >= 0.0
    assert pruned.raw_dense_dual_lower_bound - pruned.dense_dual_lower_bound <= 2.0e-7
    assert pruned.dense_feasibility_rescaling_factor <= 1.0


def test_pruned_solver_gap_and_original_dense_certificate_are_separate() -> None:
    small = 1.0e-5
    null_laws = np.asarray(
        [
            [0.70 - small, 0.20, 0.10, small],
            [small, 0.65 - small, 0.20, 0.15],
        ]
    )
    alternative_laws = np.asarray(
        [
            [0.10, small, 0.25, 0.65 - small],
            [small, 0.15, 0.20, 0.65 - small],
        ]
    )
    solution = solve_finite_minimax(
        null_laws,
        alternative_laws,
        epsilon=0.05,
        probability_weight_pruning_cutoff=2.0e-5,
        maximum_pruned_row_mass=2.0e-5,
    )
    assert solution.maximum_pruned_null_row_mass == pytest.approx(small)
    assert solution.maximum_pruned_alternative_row_mass == pytest.approx(small)
    # This is the exact primal/dual gap for pruned and renormalised P', Q'.
    assert solution.absolute_duality_gap < 2.0e-8
    assert np.max(solution.solver_null_errors) <= 0.05 + 2.0e-8
    # These are a separately labelled lower/upper certificate for original P,Q.
    assert solution.dense_dual_lower_bound <= (
        solution.dense_feasible_type_ii_upper_bound
    )
    assert solution.dense_certificate_gap >= 0.0
    assert solution.raw_dense_dual_lower_bound - solution.dense_dual_lower_bound <= 2.0e-7
    feasible_decision = (
        solution.dense_feasibility_rescaling_factor
        * solution.decision_probabilities
    )
    assert np.max(null_laws @ feasible_decision) <= 0.05 + 1.0e-15
    assert np.max(alternative_laws @ (1.0 - feasible_decision)) == pytest.approx(
        solution.dense_feasible_type_ii_upper_bound, abs=2.0e-12
    )


def test_positive_row_scaling_preserves_the_lp_and_rescales_duals() -> None:
    null_laws = np.asarray(
        [[0.7, 0.2, 0.1], [0.2, 0.6, 0.2]], dtype=float
    )
    alternative_laws = np.asarray(
        [[0.1, 0.2, 0.7], [0.15, 0.25, 0.6]], dtype=float
    )
    unit_scale = solve_finite_minimax(
        null_laws,
        alternative_laws,
        epsilon=0.05,
        lp_constraint_scale=1.0,
    )
    protected_scale = solve_finite_minimax(
        null_laws,
        alternative_laws,
        epsilon=0.05,
        lp_constraint_scale=1.0e6,
    )
    assert protected_scale.beta_objective == pytest.approx(
        unit_scale.beta_objective, abs=2.0e-10
    )
    assert protected_scale.dual_objective == pytest.approx(
        unit_scale.dual_objective, abs=2.0e-10
    )
    assert protected_scale.worst_case_type_i == pytest.approx(
        unit_scale.worst_case_type_i, abs=2.0e-10
    )
    assert protected_scale.worst_case_type_ii == pytest.approx(
        unit_scale.worst_case_type_ii, abs=2.0e-10
    )
    assert np.sum(protected_scale.alternative_dual_multipliers) == pytest.approx(
        1.0, abs=2.0e-9
    )


def test_constraint_generation_adds_off_grid_worst_cases() -> None:
    initial_null = np.asarray([[1.0, 0.0, 0.0]])
    initial_alternative = np.asarray([[0.0, 1.0, 0.0]])
    validation_null = np.asarray([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
    validation_alternative = np.asarray(
        [[0.0, 1.0, 0.0], [1.0, 0.0, 0.0]]
    )
    generated = run_constraint_generation(
        initial_null,
        initial_alternative,
        validation_null,
        validation_alternative,
        epsilon=0.05,
        violation_tolerance=1.0e-9,
        near_worst_tolerance=0.0,
        max_iterations=8,
    )
    assert generated.converged is True
    assert 1 in generated.selected_null_validation_indices
    assert 1 in generated.selected_alternative_validation_indices
    assert np.max(generated.validation_null_errors) <= 0.05 + 1.0e-9
    assert np.max(generated.validation_alternative_errors) <= (
        generated.solution.beta_objective + 1.0e-9
    )


def test_dual_continuous_rule_absorbs_importance_mass_and_reproduces_lp() -> None:
    null = _family(("n0", "n1"), [(0.35, 0.65), (0.40, 0.60)])
    alternative = _family(("q0", "q1"), [(0.60, 0.40), (0.65, 0.35)])
    support = build_balanced_proposal_support(
        null, alternative, support_size=1600, seed=1234
    )
    null_discretization = importance_discretize(null, support)
    alternative_discretization = importance_discretize(alternative, support)
    solution = solve_finite_minimax(
        null_discretization.weights,
        alternative_discretization.weights,
        epsilon=0.05,
    )
    representation = build_continuous_mixture_test(
        solution,
        null,
        alternative,
        null_discretization,
        alternative_discretization,
        support,
        reproduction_tolerance=2.0e-8,
    )
    assert representation.stable_on_finite_support is True
    assert representation.maximum_member_error_difference_from_primal < 2.0e-8
    assert representation.finite_support_worst_type_i <= 0.05 + 2.0e-8
    assert representation.objective_difference < 2.0e-8


def test_identical_law_continuous_rule_uses_randomisation_on_full_tie_set() -> None:
    family = _family(("m0", "m1"), [(0.35, 0.65), (0.45, 0.55)])
    support = build_balanced_proposal_support(
        family, family, support_size=700, seed=567
    )
    discretization = importance_discretize(family, support)
    solution = solve_finite_minimax(
        discretization.weights, discretization.weights, epsilon=0.05
    )
    representation = build_continuous_mixture_test(
        solution,
        family,
        family,
        discretization,
        discretization,
        support,
    )
    probabilities = representation.test.decision_probability(support.observations)
    assert representation.stable_on_finite_support is True
    assert representation.randomization_probability == pytest.approx(0.05, abs=2.0e-10)
    assert np.allclose(probabilities, 0.05, atol=2.0e-10)


def test_decision_api_accepts_mid_observations_only_and_module_has_no_inverse_path() -> None:
    signature = inspect.signature(ContinuousMixtureTest.decision_probability)
    assert tuple(signature.parameters) == ("self", "observations")
    source = inspect.getsource(ContinuousMixtureTest.decision_probability)
    assert "observations" in source
    assert "fit(" not in source
    assert "inverse" not in source.lower()


def test_family_concatenation_preserves_selected_constraint_order() -> None:
    initial = _family(("member-0",), [(0.4, 0.6)])
    dense = _family(("member-0", "member-1"), [(0.42, 0.58), (0.44, 0.56)])
    combined = concatenate_families(
        (initial, dense.select([1])), member_id_prefixes=("initial", "dense")
    )
    assert combined.member_ids == ("initial:member-0", "dense:member-1")
    assert np.array_equal(combined.exact_mids[0], initial.exact_mids[0])
    assert np.array_equal(combined.exact_mids[1], dense.exact_mids[1])
