from __future__ import annotations

import math
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "90_reproduction_scripts/run_rebuild.py"
SPEC = importlib.util.spec_from_file_location("run_rebuild", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise ImportError(f"Could not load reproduction script: {SCRIPT_PATH}")

run_rebuild = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = run_rebuild
SPEC.loader.exec_module(run_rebuild)

empirical_two_sided_pvalue = run_rebuild.empirical_two_sided_pvalue
exact_horizon_series = run_rebuild.exact_horizon_series
sample_derangement = run_rebuild.sample_derangement


def test_empirical_two_sided_pvalue_uses_plus_one_correction() -> None:
    observed = 2.0
    null_draws = [-0.5, 1.0, 2.0, 3.0]

    p_value = empirical_two_sided_pvalue(observed, null_draws)

    # abs(null) >= abs(observed) occurs twice (2.0 and 3.0).
    assert math.isclose(p_value, 0.6)


def test_empirical_two_sided_pvalue_empty_null_is_one() -> None:
    assert empirical_two_sided_pvalue(1.0, []) == 1.0


def test_sample_derangement_reassigns_all_positions() -> None:
    values = np.array(["A", "B", "C", "D"])
    rng = np.random.default_rng(42)

    shuffled = sample_derangement(values, rng)

    assert set(shuffled.tolist()) == set(values.tolist())
    assert not np.any(shuffled == values)


def test_sample_derangement_requires_two_values() -> None:
    rng = np.random.default_rng(42)
    with pytest.raises(ValueError, match="at least two"):
        sample_derangement(np.array(["A"]), rng)


def test_exact_horizon_series_matches_by_entity_and_year() -> None:
    source = pd.DataFrame(
        {
            "Country Name": ["A", "A", "A", "B", "B", "B"],
            "year": [2000, 2001, 2002, 2000, 2001, 2002],
            "inflation": [10.0, 11.0, 12.0, 20.0, 21.0, 22.0],
        }
    )

    aligned = exact_horizon_series(
        source_df=source,
        target_df=source,
        value_col="inflation",
        horizon=1,
    )

    expected = pd.Series([11.0, 12.0, np.nan, 21.0, 22.0, np.nan], name="inflation_h1")
    pd.testing.assert_series_equal(aligned.reset_index(drop=True), expected, check_dtype=False)
