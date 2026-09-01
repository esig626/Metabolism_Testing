"""Focused controls for the abstract three-edge topology MID classes."""

from __future__ import annotations

from dataclasses import fields
import json

import numpy as np
import pytest

from fluxemu import topology_three_edge_motif as motif
from fluxemu.composite_mid_minimax import family_from_mid_class


def test_exact_topology_labels_order_edges_and_source_endpoints() -> None:
    assert motif.TOPOLOGY_LABELS == (
        "G_A",
        "G_B",
        "G_C",
        "G_AB",
        "G_AC",
        "G_BC",
    )
    assert tuple(motif.TOPOLOGY_EDGES) == motif.TOPOLOGY_LABELS
    assert motif.TOPOLOGY_EDGES == {
        "G_A": ("e_A",),
        "G_B": ("e_B",),
        "G_C": ("e_C",),
        "G_AB": ("e_A", "e_B"),
        "G_AC": ("e_A", "e_C"),
        "G_BC": ("e_B", "e_C"),
    }
    expected = {
        "A": (motif.A0, motif.A1),
        "B": (motif.B0, motif.B1),
        "C": (motif.C0, motif.C1),
    }
    for source_label, (endpoint0, endpoint1) in expected.items():
        observed = motif.source_mid("T1", source_label, np.asarray([0.0, 1.0]))
        assert np.array_equal(observed[0], np.asarray(endpoint0))
        assert np.array_equal(observed[1], np.asarray(endpoint1))
        assert np.all(observed > 0.0)
        assert np.allclose(np.sum(observed, axis=1), 1.0, rtol=0.0, atol=1.0e-15)


def test_t1_two_edge_formula_uses_one_shared_theta_and_bounded_weight() -> None:
    theta = np.asarray([0.0, 0.37, 1.0])
    weight = np.asarray([0.2, 0.61, 0.8])
    observed = motif.topology_mid("T1", "G_AB", theta, weight)
    expected = (
        weight[:, np.newaxis] * motif.source_mid("T1", "A", theta)
        + (1.0 - weight[:, np.newaxis]) * motif.source_mid("T1", "B", theta)
    )
    assert np.array_equal(observed, expected)
    assert np.all(observed > 0.0)
    assert np.allclose(np.sum(observed, axis=1), 1.0, rtol=0.0, atol=1.0e-15)

    with pytest.raises(ValueError, match="require a mixing weight"):
        motif.topology_mid("T1", "G_AB", 0.4)
    with pytest.raises(ValueError, match="do not have a mixing weight"):
        motif.topology_mid("T1", "G_A", 0.4, 0.5)
    with pytest.raises(ValueError, match=r"\[0.2, 0.8\]"):
        motif.topology_mid("T1", "G_AB", 0.4, 0.0)
    with pytest.raises(ValueError, match=r"\[0, 1\]"):
        motif.topology_mid("T1", "G_A", 1.01)


def test_observable_classes_exclude_nuisance_coordinates_and_keep_metadata_separate() -> None:
    observable, nuisance = motif.construct_topology_class_grid(
        "T1", "G_AC", theta_point_count=21, weight_point_count=21
    )
    assert {field.name for field in fields(motif.TopologyMIDClass)} == {
        "class_id",
        "member_ids",
        "blocks",
        "exact_mids",
    }
    assert observable.class_id == "G_AC"
    assert observable.blocks == (("X", 0, 4),)
    assert observable.exact_mids.shape == (21 * 21, 4)
    assert observable.member_ids == nuisance.member_ids
    assert nuisance.theta_values.shape == (21 * 21,)
    assert nuisance.mixing_weights is not None
    assert nuisance.mixing_weights.shape == (21 * 21,)
    assert not observable.exact_mids.flags.writeable
    assert not nuisance.theta_values.flags.writeable
    assert not nuisance.mixing_weights.flags.writeable
    assert np.array_equal(
        observable.exact_mids,
        motif.topology_mid(
            "T1", "G_AC", nuisance.theta_values, nuisance.mixing_weights
        ),
    )

    single, single_nuisance = motif.construct_topology_class_grid("T1", "G_A")
    assert single.exact_mids.shape == (21, 4)
    assert single_nuisance.mixing_weights is None


def test_t0_all_six_observable_law_sets_are_bit_identical() -> None:
    classes, nuisance_grids = motif.construct_all_topology_class_grids(
        "T0", theta_point_count=21, weight_point_count=21
    )
    assert tuple(item.class_id for item in classes) == motif.TOPOLOGY_LABELS
    single_reference = classes[0].exact_mids
    assert np.array_equal(classes[1].exact_mids, single_reference)
    assert np.array_equal(classes[2].exact_mids, single_reference)
    for pair_class, nuisance in zip(classes[3:], nuisance_grids[3:], strict=True):
        reshaped = pair_class.exact_mids.reshape(21, 21, 4)
        assert np.array_equal(reshaped[:, 0, :], single_reference)
        assert np.array_equal(
            reshaped, np.repeat(single_reference[:, np.newaxis, :], 21, axis=1)
        )
        assert nuisance.mixing_weights is not None
    assert all(
        motif.observable_law_sets_equal(classes[0], item, tolerance=0.0)
        for item in classes[1:]
    )

    diagnostics = motif.verify_t0_exact_aliases(tolerance=0.0)
    assert len(diagnostics) == 15
    assert all(item.passed for item in diagnostics)
    assert all(item.maximum_absolute_component_error == 0.0 for item in diagnostics)


def test_t1_exact_mid_geometry_has_no_numerical_grid_intersections() -> None:
    classes, _ = motif.construct_all_topology_class_grids(
        "T1", theta_point_count=41, weight_point_count=41
    )
    geometry = motif.all_pairwise_grid_geometry(
        classes, intersection_tolerance=1.0e-10
    )
    assert len(geometry) == 15
    assert not any(item.intersects_at_tolerance for item in geometry)
    assert min(item.minimum_l2 for item in geometry) > 0.1

    # Audit one of the closest represented pairs over the continuous nuisance
    # boxes.  This remains a numerical search rather than an exact proof.
    continuous = motif.numerical_continuous_pair_geometry(
        "T1", "G_B", "G_BC", seed=20260808, maximum_iterations=300
    )
    assert not continuous.intersects_at_tolerance
    assert continuous.minimum_l2 == pytest.approx(0.1126055061, abs=5.0e-7)


def test_t2_required_alias_and_additional_exact_intersection_families() -> None:
    theta = np.linspace(0.0, 1.0, 37)
    assert np.max(
        np.abs(
            motif.source_mid("T2", "C", theta)
            - 0.5
            * (
                motif.source_mid("T2", "A", theta)
                + motif.source_mid("T2", "B", theta)
            )
        )
    ) <= np.finfo(float).eps
    assert np.array_equal(
        motif.topology_mid("T2", "G_C", theta),
        motif.topology_mid("T2", "G_AB", theta, np.full(len(theta), 0.5)),
    )

    diagnostics = motif.verify_t2_exact_aliases(theta_values=theta)
    assert tuple(
        (item.left_class_id, item.right_class_id) for item in diagnostics
    ) == (
        ("G_C", "G_AB"),
        ("G_AB", "G_AC"),
        ("G_AB", "G_BC"),
    )
    assert all(item.passed for item in diagnostics)
    assert max(item.maximum_absolute_component_error for item in diagnostics) <= np.finfo(float).eps

    # The required C/AB witness is present on every odd endpoint-inclusive
    # weight grid because w=0.5 is explicitly represented.
    classes, _ = motif.construct_all_topology_class_grids(
        "T2", theta_point_count=21, weight_point_count=21
    )
    geometry = {
        (item.left_class_id, item.right_class_id): item
        for item in motif.all_pairwise_grid_geometry(classes)
    }
    assert geometry[("G_C", "G_AB")].minimum_l2 == 0.0
    assert geometry[("G_C", "G_AB")].intersects_at_tolerance


def test_weight_grids_cannot_silently_omit_the_required_t2_anchor() -> None:
    assert 0.5 in motif.weight_grid(21)
    with pytest.raises(ValueError, match="odd point count"):
        motif.weight_grid(20)


def test_t2_required_alias_is_bit_exact_after_dirichlet_construction() -> None:
    c_class, _ = motif.construct_topology_class_grid(
        "T2", "G_C", theta_point_count=21, weight_point_count=21
    )
    ab_class, ab_nuisance = motif.construct_topology_class_grid(
        "T2", "G_AB", theta_point_count=21, weight_point_count=21
    )
    c_family = family_from_mid_class(c_class, rms_noise=0.005)
    ab_family = family_from_mid_class(ab_class, rms_noise=0.005)
    assert ab_nuisance.mixing_weights is not None
    anchor = np.flatnonzero(ab_nuisance.mixing_weights == 0.5)
    assert len(anchor) == 21
    assert np.array_equal(c_family.exact_mids, ab_family.exact_mids[anchor])
    assert np.array_equal(c_family.alpha_parameters, ab_family.alpha_parameters[anchor])


def test_definition_payload_is_complete_json_and_does_not_change_science() -> None:
    payload = motif.topology_definitions_payload()
    encoded = json.dumps(payload, sort_keys=True)
    assert encoded
    assert payload["topology_order"] == list(motif.TOPOLOGY_LABELS)
    assert payload["nuisance_domains"] == {
        "theta": [0.0, 1.0],
        "two_edge_weight": [0.2, 0.8],
        "two_edge_theta_is_shared": True,
    }
    assert tuple(payload["benchmarks"]) == motif.BENCHMARK_LABELS


@pytest.mark.parametrize(
    ("benchmark_id", "topology_label"),
    (("T3", "G_A"), ("T1", "G_D")),
)
def test_undeclared_benchmark_or_topology_is_rejected(
    benchmark_id: str, topology_label: str
) -> None:
    with pytest.raises(ValueError):
        motif.topology_mid(benchmark_id, topology_label, 0.5)
