"""Integrity checks for the frozen generated R1 observable-MID fixture."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

import numpy as np
import pandas as pd


FIXTURE_DIR = (
    Path(__file__).resolve().parents[1] / "fixtures" / "r1_ecoli_u13c70"
)
STATE_MIDS = FIXTURE_DIR / "state_level_noise_free_mids.csv"


def test_r1_state_level_fixture_has_complete_normalized_mid_blocks() -> None:
    frame = pd.read_csv(STATE_MIDS)
    assert list(frame.columns) == [
        "condition",
        "state_id",
        "target_name",
        "internal_target_id",
        "direct_or_reporter",
        "carbon_count",
        "mass_index",
        "mass_isotopologue",
        "fraction",
    ]
    assert len(frame) == 11_600
    assert set(frame["condition"]) == {"condition0", "condition1"}
    assert frame.groupby("condition")["state_id"].nunique().to_dict() == {
        "condition0": 100,
        "condition1": 100,
    }
    assert frame["target_name"].nunique() == 12
    assert not frame.duplicated(
        ["condition", "state_id", "target_name", "mass_index"]
    ).any()
    assert np.isfinite(frame["fraction"]).all()
    assert frame["fraction"].between(0.0, 1.0).all()

    block_sums = frame.groupby(
        ["condition", "state_id", "target_name"], sort=False
    )["fraction"].sum()
    assert len(block_sums) == 2_400
    assert np.allclose(block_sums.to_numpy(), 1.0, rtol=0.0, atol=1.0e-12)

    expected_component_count = frame["carbon_count"] + 1
    assert (
        frame.groupby(["condition", "state_id", "target_name"], sort=False)
        .size()
        .to_numpy()
        == expected_component_count.groupby(
            [frame["condition"], frame["state_id"], frame["target_name"]],
            sort=False,
        )
        .first()
        .to_numpy()
    ).all()


def test_r1_fixture_bytes_match_the_originating_generation_manifest() -> None:
    manifest = json.loads(
        (FIXTURE_DIR / "source_experiment_manifest.json").read_text(
            encoding="utf-8"
        )
    )
    observed = sha256(STATE_MIDS.read_bytes()).hexdigest()
    assert observed == (
        "3982e129ee203b35f3e44b668fee98ab49a9b915d509cf6f0742b1a3e983b5da"
    )
    assert manifest["source_raw_mid_sha256"] == (
        "72bac2b3adeab74b715f819394c458123851a0e46039f037d2ae0328485b3ccf"
    )
    assert observed != manifest["source_raw_mid_sha256"]
    assert manifest["flux_states_regenerated"] is False
    assert manifest["cobra_model_constructed"] is False
    assert manifest["sampler_invoked"] is False

    difference = json.loads(
        (FIXTURE_DIR / "configuration_difference.json").read_text(
            encoding="utf-8"
        )
    )
    assert difference["only_expected_configuration_difference"] is True
    assert difference["revised_tracer_fractions"] == {
        "#000000": 0.3,
        "#111111": 0.7,
    }
