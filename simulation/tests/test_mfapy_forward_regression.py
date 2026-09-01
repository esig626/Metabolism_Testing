from __future__ import annotations

import copy
import json
from pathlib import Path

import numpy as np
import pytest

from fluxemu._mfapy import load_mfapy


FIXTURE_PATH = (
    Path(__file__).resolve().parents[1]
    / "fixtures"
    / "mfapy"
    / "example0_expected.json"
)
mfapy = load_mfapy()


@pytest.fixture
def official_example() -> dict:
    with FIXTURE_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def _fixture_constructor_args(example: dict) -> tuple[dict, dict, dict, dict]:
    dictionaries = example["constructor_dictionaries"]
    return (
        copy.deepcopy(dictionaries["reactions"]),
        copy.deepcopy(dictionaries["reversible_reactions"]),
        copy.deepcopy(dictionaries["metabolites"]),
        copy.deepcopy(dictionaries["target_fragments"]),
    )


def _set_official_tracers(model, example: dict):
    carbon_source = model.generate_carbon_source_template()
    for metabolite_id, tracer in example["tracers"].items():
        setter = getattr(carbon_source, tracer["setter"])
        assert setter(
            metabolite_id,
            copy.deepcopy(tracer["isotopomer_fractions"]),
            correction=tracer["correction"],
        )
    return carbon_source


def test_direct_dictionary_route_reproduces_official_example_without_text_parser(
    official_example: dict, monkeypatch: pytest.MonkeyPatch
) -> None:
    def forbidden_parser(*args, **kwargs):
        raise AssertionError("direct runtime route called load_metabolic_model")

    monkeypatch.setattr(mfapy.mfapyio, "load_metabolic_model", forbidden_parser)
    model = mfapy.metabolicmodel.MetabolicModel(
        *_fixture_constructor_args(official_example)
    )
    assert model.reaction_ids == official_example["reaction_order"]

    carbon_source = _set_official_tracers(model, official_example)
    mdv_vector, mdv_by_fragment = mfapy.optimize.calc_MDV_from_flux(
        official_example["complete_flux_vector"],
        official_example["requested_target_fragments"],
        carbon_source.generate_dict(),
        model.func,
    )

    expected = official_example["expected_mdvs"]["Glue"]
    tolerance = official_example["absolute_tolerance"]
    np.testing.assert_allclose(mdv_vector, expected, rtol=0.0, atol=tolerance)
    np.testing.assert_allclose(
        mdv_by_fragment["Glue"], expected, rtol=0.0, atol=tolerance
    )
    assert "X_list" in mdv_by_fragment
