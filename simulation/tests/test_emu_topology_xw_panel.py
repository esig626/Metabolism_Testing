from __future__ import annotations

from dataclasses import fields, replace
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

from fluxemu import emu_topology_xw_panel as xw_module
from fluxemu.composite_mid_minimax import family_from_mid_class
from fluxemu.emu_topology_edge_reconstruction import (
    SUPPORT_LABELS,
    generate_forward_classes,
)
from fluxemu.emu_topology_xw_panel import (
    PHASE2A_EXACT_ALIAS_PAIRS,
    XW_BLOCKS,
    XWObservableMIDClass,
    construct_xw_panel,
    exact_xw_aliases,
    pairwise_xw_geometry,
    regress_against_phase2a_artifacts,
    verify_xw_coordinate_algebra,
)


PHASE2A_RESULTS = (
    Path(__file__).resolve().parents[1]
    / "fixtures"
    / "topology_phase2a"
)


@pytest.fixture(scope="module")
def phase2a_generated():
    return generate_forward_classes(weight_point_count=11)


@pytest.fixture(scope="module")
def xw_panel(phase2a_generated):
    return construct_xw_panel(
        weight_point_count=11,
        phase2a_generated=phase2a_generated,
    )


def test_phase2a_forward_states_regress_to_the_frozen_artifacts(xw_panel) -> None:
    regression = regress_against_phase2a_artifacts(xw_panel, PHASE2A_RESULTS)
    assert regression.passed
    assert regression.member_count == 36
    assert regression.same_member_ids
    assert regression.same_support_labels
    assert regression.same_active_edges
    assert regression.same_weight_grid
    assert regression.same_flux_vectors
    assert regression.same_x_mids
    assert regression.same_w_mids
    assert regression.same_forward_validation
    assert regression.maximum_absolute_x_mid_error <= regression.tolerance
    assert regression.maximum_absolute_w_mid_error <= regression.tolerance


def test_forward_regression_rejects_nonfinite_fluxes_and_weights(xw_panel) -> None:
    metadata = list(xw_panel.audit_metadata)
    corrupted_fluxes = metadata[0].complete_fluxes.copy()
    corrupted_fluxes.iloc[0, corrupted_fluxes.columns.get_loc("e_A")] = np.inf
    metadata[0] = replace(metadata[0], complete_fluxes=corrupted_fluxes)
    with pytest.raises(ValueError, match="same_flux_vectors"):
        regress_against_phase2a_artifacts(
            replace(xw_panel, audit_metadata=tuple(metadata)),
            PHASE2A_RESULTS,
        )

    metadata = list(xw_panel.audit_metadata)
    corrupted_weights = np.array(metadata[3].mixing_weights, copy=True)
    corrupted_weights[0] = np.inf
    metadata[3] = replace(metadata[3], mixing_weights=corrupted_weights)
    with pytest.raises(ValueError, match="same_weight_grid"):
        regress_against_phase2a_artifacts(
            replace(xw_panel, audit_metadata=tuple(metadata)),
            PHASE2A_RESULTS,
        )


def test_xw_panel_is_a_raw_two_block_observation_without_renormalisation(
    xw_panel,
    phase2a_generated,
) -> None:
    assert xw_panel.support_labels == SUPPORT_LABELS
    for xw, phase2a_x, hidden in zip(
        xw_panel.observables,
        phase2a_generated.observables,
        phase2a_generated.metadata,
        strict=True,
    ):
        assert xw.blocks == XW_BLOCKS
        assert np.array_equal(xw.exact_mids[:, :3], phase2a_x.exact_mids)
        assert np.array_equal(xw.exact_mids[:, 3:], hidden.withheld_mids)
        assert np.sum(xw.exact_mids[:, :3], axis=1) == pytest.approx(1.0)
        assert np.sum(xw.exact_mids[:, 3:], axis=1) == pytest.approx(1.0)
        assert np.sum(xw.exact_mids, axis=1) == pytest.approx(2.0)


def test_product_measurement_family_retains_independent_x_and_w_blocks(
    xw_panel,
) -> None:
    for observable in xw_panel.observables:
        family = family_from_mid_class(observable, rms_noise=0.005)
        assert family.block_names == ("X_full", "W_full")
        assert family.block_sizes == (3, 2)
        assert family.observation_dimension == 5
        draws = family.sample_member(0, 7, np.random.default_rng(20260809))
        assert np.sum(draws[:, :3], axis=1) == pytest.approx(1.0)
        assert np.sum(draws[:, 3:], axis=1) == pytest.approx(1.0)
        assert np.sum(draws, axis=1) == pytest.approx(2.0)


def test_five_component_global_renormalisation_is_rejected(xw_panel) -> None:
    observable = xw_panel.observables[0]
    with pytest.raises(ValueError, match="separately normalized MID"):
        XWObservableMIDClass(
            member_ids=observable.member_ids,
            blocks=XW_BLOCKS,
            exact_mids=observable.exact_mids / 2.0,
        )


def test_phase2b_decision_input_has_no_support_or_flux_metadata(xw_panel) -> None:
    assert tuple(field.name for field in fields(XWObservableMIDClass)) == (
        "member_ids",
        "blocks",
        "exact_mids",
    )
    forbidden = {
        "support_label",
        "active_edges",
        "mixing_weights",
        "weight",
        "fluxes",
        "complete_fluxes",
        "generating_state",
    }
    for observable in xw_panel.observables:
        assert not forbidden.intersection(vars(observable))
        assert all("G_" not in member_id for member_id in observable.member_ids)
        assert all("e_" not in member_id for member_id in observable.member_ids)


def test_emu_rows_reproduce_the_exact_joint_coordinate_formulas(xw_panel) -> None:
    diagnostic = verify_xw_coordinate_algebra(xw_panel)
    assert diagnostic.passed
    assert diagnostic.state_count == 36
    assert diagnostic.maximum_absolute_component_error <= diagnostic.tolerance
    assert diagnostic.exact_coordinate_statement == (
        "X identifies b=e_B; W identifies a=e_A; c=1-a-b"
    )


def test_xw_support_sets_have_no_exact_algebraic_intersections(xw_panel) -> None:
    aliases = exact_xw_aliases(xw_panel)
    assert len(aliases) == 15
    assert all(not item.exact_xw_alias for item in aliases)
    assert all(not item.exact_xw_set_equal for item in aliases)
    assert all(item.exact_witness == "" for item in aliases)
    assert all(item.exact_method.startswith("exact rational") for item in aliases)
    assert {
        (item.left_support, item.right_support)
        for item in aliases
        if item.phase2a_exact_x_alias
    } == PHASE2A_EXACT_ALIAS_PAIRS


def test_w_removes_every_phase2a_alias_without_creating_a_new_one(xw_panel) -> None:
    by_pair = {
        (item.left_support, item.right_support): item
        for item in exact_xw_aliases(xw_panel)
    }
    for pair in PHASE2A_EXACT_ALIAS_PAIRS:
        item = by_pair[pair]
        assert item.phase2a_exact_x_alias
        assert not item.exact_xw_alias
        assert "remov" in item.interpretation.lower()
        assert item.minimum_represented_xw_l2 > 0.0
    assert not any(
        item.exact_xw_alias and not item.phase2a_exact_x_alias
        for item in by_pair.values()
    )


def test_numerical_grid_geometry_is_reported_separately_from_exact_status(
    xw_panel,
) -> None:
    geometry = pairwise_xw_geometry(xw_panel)
    assert len(geometry) == 15
    assert all(not item.represented_grid_intersects_at_tolerance for item in geometry)
    assert all(not item.represented_grid_set_equal_at_tolerance for item in geometry)
    minimum = min(item.minimum_xw_l2 for item in geometry)
    assert minimum == pytest.approx(np.sqrt(7.0 / 800.0), abs=1.0e-15)
    assert min(item.minimum_five_component_rms for item in geometry) == pytest.approx(
        np.sqrt(7.0 / 800.0) / np.sqrt(5.0),
        abs=1.0e-15,
    )
    by_pair = {
        (item.left_support, item.right_support): item for item in geometry
    }
    assert by_pair[("G_A", "G_C")].minimum_xw_l2 == pytest.approx(
        np.sqrt(0.5), abs=1.0e-15
    )
    assert by_pair[("G_AB", "G_BC")].minimum_xw_l2 == pytest.approx(
        np.sqrt(1.0 / 50.0), abs=1.0e-15
    )


@pytest.mark.parametrize(
    ("left", "right", "expected", "witness"),
    (
        (((0, 0), (0, 0)), ((0, 0), (0, 0)), True, "b=0;a=0"),
        (((0, 0), (0, 0)), ((1, 0), (1, 0)), False, ""),
        (((0, 0), (1, 1)), ((0, 1), (1, 0)), True, "b=1/2;a=1/2"),
        (((1, 1), (0, 0)), ((1, 0), (2, 0)), False, ""),
        (((0, 0), (2, 0)), ((1, 0), (3, 0)), True, "b=1;a=0 to b=2;a=0"),
        (((0, 0), (1, 0)), ((2, 0), (3, 0)), False, ""),
    ),
)
def test_exact_segment_primitive_uses_rational_arithmetic(
    left,
    right,
    expected: bool,
    witness: str,
) -> None:
    as_segment = lambda item: tuple(
        tuple(Fraction(value) for value in point) for point in item
    )
    observed, observed_witness = xw_module._exact_segment_intersection(
        as_segment(left), as_segment(right)
    )
    assert observed is expected
    assert observed_witness == witness
