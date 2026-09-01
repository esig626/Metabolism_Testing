"""Focused directed Renyi diagnostics for the three-edge topology motif."""

from __future__ import annotations

import ast
import inspect

import numpy as np
import pytest

from fluxemu import composite_mid_renyi as analytic
from fluxemu import topology_pairwise_renyi as topology_renyi


def test_fixed_member_orientation_matches_analytic_product_dirichlet_formula() -> None:
    base_coordinates = (0.23,)
    directed_coordinates = (0.71, 0.37)
    alpha_p_i = topology_renyi.topology_dirichlet_alpha(
        "T1", "G_A", base_coordinates, rms_noise=0.005
    )
    alpha_q_j = topology_renyi.topology_dirichlet_alpha(
        "T1", "G_BC", directed_coordinates, rms_noise=0.005
    )

    for order in topology_renyi.REPRESENTATIVE_RENYI_ORDERS:
        observed = topology_renyi.directed_member_divergence(
            "T1",
            "G_A",
            base_coordinates,
            "G_BC",
            directed_coordinates,
            rms_noise=0.005,
            order=order,
        )
        expected = analytic.product_dirichlet_renyi_divergence(
            alpha_q_j, alpha_p_i, (4,), order
        )
        assert observed == pytest.approx(expected, rel=0.0, abs=1.0e-12)

    observed_kl = topology_renyi.directed_member_divergence(
        "T1",
        "G_A",
        base_coordinates,
        "G_BC",
        directed_coordinates,
        rms_noise=0.005,
        order=None,
    )
    expected_kl = analytic.product_dirichlet_kl_divergence(
        alpha_q_j, alpha_p_i, (4,)
    )
    reverse_kl = analytic.product_dirichlet_kl_divergence(
        alpha_p_i, alpha_q_j, (4,)
    )
    assert observed_kl == pytest.approx(expected_kl, rel=0.0, abs=1.0e-12)
    assert abs(observed_kl - reverse_kl) > 1.0


def test_t0_generic_k_matrix_preserves_caller_order_and_is_exactly_zero() -> None:
    labels = ("G_BC", "G_A", "G_C", "G_AB")
    matrices = topology_renyi.representative_directed_topology_matrices(
        "T0", class_labels=labels, rms_noise=0.005
    )
    assert tuple(item.order for item in matrices) == (0.1, 0.5, 0.9, None)
    for matrix in matrices:
        assert matrix.class_labels == labels
        assert matrix.values.shape == (len(labels), len(labels))
        assert np.array_equal(matrix.values, np.zeros((len(labels), len(labels))))
        assert not matrix.values.flags.writeable
        assert all(result.exact_zero_witness_used for result in matrix.pair_results)
        assert all(result.function_evaluations == 0 for result in matrix.pair_results)
        assert matrix.result("G_A", "G_BC").base_class_id == "G_A"
        assert matrix.result("G_A", "G_BC").directed_class_id == "G_BC"


@pytest.mark.parametrize(
    ("left_class_id", "right_class_id"),
    (
        ("G_C", "G_AB"),
        ("G_AB", "G_C"),
        ("G_AB", "G_AC"),
        ("G_AC", "G_AB"),
        ("G_AB", "G_BC"),
        ("G_BC", "G_AB"),
    ),
)
def test_t2_exact_alias_witnesses_are_oriented_verified_and_zero_both_ways(
    left_class_id: str, right_class_id: str
) -> None:
    witness = topology_renyi.exact_intersection_witness(
        "T2", left_class_id, right_class_id
    )
    assert witness is not None
    assert witness.verified
    assert witness.left_class_id == left_class_id
    assert witness.right_class_id == right_class_id
    assert witness.maximum_absolute_mid_error <= np.finfo(float).eps

    for order in (*topology_renyi.REPRESENTATIVE_RENYI_ORDERS, None):
        result = topology_renyi.minimise_directed_topology_separation(
            "T2",
            left_class_id,
            right_class_id,
            rms_noise=0.005,
            order=order,
        )
        assert result.divergence == 0.0
        assert result.exact_zero_witness_used
        assert result.optimizer_success
        assert result.function_evaluations == 0
        assert result.base_coordinates == witness.left_coordinates
        assert result.directed_coordinates == witness.right_coordinates
        assert result.witness_maximum_absolute_mid_error == (
            witness.maximum_absolute_mid_error
        )
        assert result.claim_type == "mathematically exact shared observable law"


def test_nonalias_composite_search_is_bounded_positive_and_oriented() -> None:
    forward = topology_renyi.minimise_directed_topology_separation(
        "T1",
        "G_A",
        "G_B",
        rms_noise=0.005,
        order=None,
        seed=81_001,
        maximum_iterations=100,
        population_size=8,
    )
    reverse = topology_renyi.minimise_directed_topology_separation(
        "T1",
        "G_B",
        "G_A",
        rms_noise=0.005,
        order=None,
        seed=81_002,
        maximum_iterations=100,
        population_size=8,
    )
    assert forward.orientation == reverse.orientation == "KL(P_j || P_i)"
    assert forward.divergence > 0.0
    assert reverse.divergence > 0.0
    assert forward.divergence != pytest.approx(reverse.divergence, rel=1.0e-3)
    assert 0.0 <= forward.base_coordinates[0] <= 1.0
    assert 0.0 <= forward.directed_coordinates[0] <= 1.0
    assert not forward.exact_zero_witness_used
    assert forward.function_evaluations > 0
    assert "candidate upper bound" in forward.claim_type
    assert "not a certified positive separation" in forward.claim_type
    reproduced = topology_renyi.directed_member_divergence(
        "T1",
        "G_A",
        forward.base_coordinates,
        "G_B",
        forward.directed_coordinates,
        rms_noise=0.005,
        order=None,
    )
    assert forward.divergence == pytest.approx(reproduced, rel=0.0, abs=1.0e-10)


def test_directed_curve_retains_declared_orders_and_diagnostic_scope() -> None:
    orders = (0.1, 0.3, 0.5, 0.9)
    curve = topology_renyi.directed_topology_separation_curve(
        "T2", "G_C", "G_AB", orders, rms_noise=0.02
    )
    assert tuple(item.order for item in curve) == orders
    assert all(item.divergence == 0.0 for item in curve)
    assert all(item.orientation == "D(P_j || P_i)" for item in curve)

    tree = ast.parse(inspect.getsource(topology_renyi))
    declared_classes = {
        node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)
    }
    assert not any("Decision" in name or "Classifier" in name for name in declared_classes)


@pytest.mark.parametrize("order", (0.0, 1.0, -0.1, 1.1))
def test_invalid_renyi_orders_are_rejected_before_exact_alias_shortcut(
    order: float,
) -> None:
    with pytest.raises(ValueError, match="strictly inside"):
        topology_renyi.minimise_directed_topology_separation(
            "T2", "G_C", "G_AB", order=order
        )


def test_invalid_noise_and_coordinate_layout_are_rejected() -> None:
    with pytest.raises(ValueError, match="RMS measurement noise"):
        topology_renyi.minimise_directed_topology_separation(
            "T0", "G_A", "G_B", rms_noise=0.0, order=0.5
        )
    with pytest.raises(ValueError, match="ordered as"):
        topology_renyi.topology_mid_at_coordinates("T1", "G_AB", (0.5,))
    with pytest.raises(ValueError, match="bounded domain"):
        topology_renyi.topology_mid_at_coordinates("T1", "G_AB", (0.5, 1.0))
    with pytest.raises(ValueError, match="unique"):
        topology_renyi.directed_topology_separation_matrix(
            "T1", class_labels=("G_A", "G_A"), order=0.5
        )
