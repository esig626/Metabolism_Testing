"""Pure construction tests for the exported Control 0 MID-class module."""

from __future__ import annotations

from dataclasses import fields
import inspect

import numpy as np
import pytest

from fluxemu import control0_composite_mid_classes as classes


def _target_indices() -> dict[str, tuple[int, ...]]:
    result: dict[str, tuple[int, ...]] = {}
    offset = 0
    for target in classes.FULL_TARGET_ORDER:
        count = classes.TARGET_COMPONENT_COUNTS[target]
        result[target] = tuple(range(offset, offset + count))
        offset += count
    return result


TARGET_INDICES = _target_indices()


def _deterministic_normalized_predictor(a_value: float, b_value: float) -> np.ndarray:
    """Return normalized blocks that vary with a and deliberately ignore b."""

    del b_value
    labelled = 0.1 + float(a_value) / 250.0
    blocks = []
    for target in classes.FULL_TARGET_ORDER:
        count = classes.TARGET_COMPONENT_COUNTS[target]
        block = np.full(count, 1.0e-6, dtype=float)
        remaining_mass = 1.0 - float(count - 2) * 1.0e-6
        block[:2] = (
            remaining_mass * (1.0 - labelled),
            remaining_mass * labelled,
        )
        blocks.append(block)
    return np.concatenate(blocks)


def test_prescribed_hidden_conditions_and_exact_affine_projections() -> None:
    intervals = {
        benchmark_id: (
            (definition.h0.a_interval.lower, definition.h0.a_interval.upper),
            (definition.h1.a_interval.lower, definition.h1.a_interval.upper),
        )
        for benchmark_id, definition in classes.BENCHMARK_DEFINITIONS.items()
    }
    assert intervals == {
        "C0": ((40.0, 60.0), (40.0, 60.0)),
        "C1": ((20.0, 35.0), (65.0, 80.0)),
        "C2": ((40.0, 49.0), (51.0, 60.0)),
    }
    assert classes.exact_flux_vector(50.0, 75.0) == (
        100.0,
        100.0,
        50.0,
        50.0,
        50.0,
        125.0,
        75.0,
        50.0,
    )
    for definition in classes.BENCHMARK_DEFINITIONS.values():
        for condition in (definition.h0, definition.h1):
            diagnostics = classes.feasible_set_diagnostics(condition)
            assert diagnostics.feasible_dimension == 2
            assert diagnostics.state_cardinality == "uncountably infinite"
            assert diagnostics.b_global_lower == 0.0
            assert diagnostics.b_global_upper == 999_900.0 + condition.a_interval.upper
            ranges = {
                item.reaction_id: (item.lower, item.upper)
                for item in diagnostics.fva_equivalent_ranges
            }
            assert ranges["v3"] == (
                condition.a_interval.lower,
                condition.a_interval.upper,
            )
            assert ranges["v7"] == (
                0.0,
                999_900.0 + condition.a_interval.upper,
            )


def test_mid_only_interface_keeps_hidden_flux_metadata_separate() -> None:
    definition = classes.BENCHMARK_DEFINITIONS["C1"]
    law_class, hidden = classes.construct_mid_class(
        definition.h0,
        5,
        full_mid_predictor=_deterministic_normalized_predictor,
        target_indices=TARGET_INDICES,
    )
    field_names = {field.name for field in fields(classes.MIDClass)}
    assert field_names == {
        "class_id",
        "panel_id",
        "member_ids",
        "blocks",
        "exact_mids",
    }
    assert field_names.isdisjoint({"a", "b", "a_values", "b_values", "flux_vectors"})
    assert law_class.exact_mids.shape == (5, 29)
    assert law_class.blocks == (
        ("OAC", 0, 5),
        ("citrate", 5, 12),
        ("AKG", 12, 18),
        ("succinate", 18, 23),
        ("glutamate", 23, 29),
    )
    assert law_class.member_ids == hidden.member_ids
    assert hidden.flux_vectors.shape == (5, 8)
    assert not law_class.exact_mids.flags.writeable
    assert not hidden.flux_vectors.flags.writeable


def test_synthetic_callback_audits_b_invariance_without_biology_runner() -> None:
    diagnostics = classes.verify_b_invariance(
        full_mid_predictor=_deterministic_normalized_predictor,
        target_indices=TARGET_INDICES,
        a_values=(20.0, 50.0, 80.0),
    )
    assert diagnostics.passed
    assert diagnostics.maximum_absolute_mid_change == 0.0
    assert diagnostics.maximum_l2_mid_change == 0.0


def test_finite_grid_geometry_retains_identical_easy_and_hard_controls() -> None:
    geometry = {}
    for benchmark_id, definition in classes.BENCHMARK_DEFINITIONS.items():
        h0, _ = classes.construct_mid_class(
            definition.h0,
            41,
            full_mid_predictor=_deterministic_normalized_predictor,
            target_indices=TARGET_INDICES,
        )
        h1, _ = classes.construct_mid_class(
            definition.h1,
            41,
            full_mid_predictor=_deterministic_normalized_predictor,
            target_indices=TARGET_INDICES,
        )
        geometry[benchmark_id] = classes.mid_class_geometry(benchmark_id, h0, h1)
    ratio = classes.verify_prescribed_geometry(
        geometry["C0"], geometry["C1"], geometry["C2"]
    )
    assert geometry["C0"].identical_grids
    assert geometry["C1"].minimum_cross_l2 > geometry["C2"].minimum_cross_l2
    assert ratio == pytest.approx(15.0)


def test_construction_module_has_no_inverse_fit_or_classifier() -> None:
    source = inspect.getsource(classes)
    assert "fitting_flux" not in source
    assert "GLR" not in source
    assert "logistic" not in source
    assert "classifier" not in source.lower()
