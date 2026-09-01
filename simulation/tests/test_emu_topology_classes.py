from __future__ import annotations

from dataclasses import fields

import numpy as np
import pytest

from fluxemu.composite_mid_minimax import family_from_mid_class
from fluxemu.emu_topology_edge_reconstruction import (
    CANDIDATE_EDGES,
    OBSERVED_BLOCKS,
    SUPPORT_LABELS,
    ObservableMIDClass,
    generate_forward_classes,
    pairwise_observable_geometry,
    verify_declared_forward_aliases,
)


@pytest.fixture(scope="module")
def generated_classes():
    return generate_forward_classes(weight_point_count=11)


def test_six_forward_generated_support_classes_have_the_frozen_grid(
    generated_classes,
) -> None:
    assert generated_classes.support_labels == SUPPORT_LABELS
    assert [item.member_count for item in generated_classes.observables] == [
        1,
        1,
        1,
        11,
        11,
        11,
    ]
    for hidden in generated_classes.metadata:
        if len(hidden.active_edges) == 1:
            assert hidden.mixing_weights is None
        else:
            assert hidden.mixing_weights is not None
            assert hidden.mixing_weights[0] == pytest.approx(0.2)
            assert hidden.mixing_weights[-1] == pytest.approx(0.8)
            assert hidden.mixing_weights[5] == pytest.approx(0.5)


def test_observable_class_exposes_only_opaque_ids_blocks_and_observed_mids(
    generated_classes,
) -> None:
    assert tuple(field.name for field in fields(ObservableMIDClass)) == (
        "member_ids",
        "blocks",
        "exact_mids",
    )
    forbidden = {
        "support_label",
        "active_edges",
        "theta",
        "mixing_weights",
        "fluxes",
        "complete_fluxes",
        "withheld_mids",
    }
    for observable in generated_classes.observables:
        assert observable.blocks == OBSERVED_BLOCKS
        assert not forbidden.intersection(vars(observable))
        assert all("G_" not in member_id for member_id in observable.member_ids)
        assert all("e_" not in member_id for member_id in observable.member_ids)


def test_measurement_family_is_constructed_from_observed_x_only(
    generated_classes,
) -> None:
    families = tuple(
        family_from_mid_class(observable, rms_noise=0.005)
        for observable in generated_classes.observables
    )
    for observable, family, hidden in zip(
        generated_classes.observables,
        families,
        generated_classes.metadata,
        strict=True,
    ):
        assert family.block_names == ("X_full",)
        assert family.block_sizes == (3,)
        assert family.observation_dimension == 3
        assert np.array_equal(family.exact_mids, observable.exact_mids)
        assert hidden.withheld_mids.shape[1] == 2
        assert not hasattr(observable, "withheld_mids")


def test_all_grid_fluxes_keep_exactly_the_declared_edges_positive(
    generated_classes,
) -> None:
    for hidden in generated_classes.metadata:
        for _, row in hidden.complete_fluxes.iterrows():
            for edge in CANDIDATE_EDGES:
                if edge in hidden.active_edges:
                    assert row[edge] >= 0.2
                else:
                    assert row[edge] == 0.0
            assert sum(row[edge] for edge in CANDIDATE_EDGES) == pytest.approx(1.0)


def test_forward_generated_class_mids_are_positive_and_normalized(
    generated_classes,
) -> None:
    assert generated_classes.forward_validation["valid"] is True
    assert generated_classes.forward_validation["sample_count"] == 36
    for observable, hidden in zip(
        generated_classes.observables, generated_classes.metadata, strict=True
    ):
        assert np.isfinite(observable.exact_mids).all()
        assert np.all(observable.exact_mids > 0.0)
        assert np.allclose(
            observable.exact_mids.sum(axis=1), 1.0, rtol=0.0, atol=1.0e-12
        )
        assert np.isfinite(hidden.withheld_mids).all()
        assert np.all(hidden.withheld_mids > 0.0)
        assert np.allclose(
            hidden.withheld_mids.sum(axis=1), 1.0, rtol=0.0, atol=1.0e-12
        )


def test_only_the_declared_observable_class_sets_are_exact_aliases(
    generated_classes,
) -> None:
    diagnostics = verify_declared_forward_aliases(generated_classes)
    assert len(diagnostics) == 4
    assert all(item.passed for item in diagnostics)
    assert max(item.maximum_absolute_component_error for item in diagnostics) <= 1e-12

    equal_pairs = {
        (item.left_support, item.right_support)
        for item in pairwise_observable_geometry(generated_classes)
        if item.set_equal_at_tolerance
    }
    assert equal_pairs == {
        ("G_A", "G_C"),
        ("G_A", "G_AC"),
        ("G_C", "G_AC"),
        ("G_AB", "G_BC"),
    }


def test_forward_class_generation_is_reproducible(generated_classes) -> None:
    repeated = generate_forward_classes(weight_point_count=11)
    for first, second in zip(
        generated_classes.observables, repeated.observables, strict=True
    ):
        assert first.member_ids == second.member_ids
        assert np.array_equal(first.exact_mids, second.exact_mids)
    for first, second in zip(
        generated_classes.metadata, repeated.metadata, strict=True
    ):
        assert np.array_equal(first.withheld_mids, second.withheld_mids)
