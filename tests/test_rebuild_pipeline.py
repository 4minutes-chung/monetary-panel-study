from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import pytest


def load_module(module_name: str, script_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load script: {script_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "90_reproduction_scripts"
run_rebuild = load_module("run_rebuild_pipeline", SCRIPT_DIR / "run_rebuild.py")
build_graphs = load_module("build_graphs_pipeline", SCRIPT_DIR / "build_graphs.py")


@pytest.fixture
def small_panel() -> pd.DataFrame:
    rows: list[dict] = []
    for country_idx, country in enumerate(["Aland", "Borland"], start=1):
        for year in range(2000, 2012):
            t = year - 1999
            rows.append(
                {
                    "Country Name": country,
                    "year": year,
                    "inflation": float(1.5 * t + country_idx),
                    "gdp_growth": float(2.0 + 0.05 * t + 0.1 * country_idx),
                    "m2_growth": float(4.0 + 0.3 * t + 0.2 * country_idx),
                    "instrument_m2_external_level": float(0.4 + 0.1 * t + 0.05 * country_idx),
                    "instrument_m2_l1": float(0.2 + 0.08 * t + 0.03 * country_idx),
                    "trade_open": float(40 + t + country_idx),
                    "pop_growth": float(1.0 + 0.01 * t),
                    "investment_share": float(20 + 0.2 * t),
                }
            )
    return pd.DataFrame(rows)


def make_temp_paths(tmp_path: Path):
    out_root = tmp_path / "04_current_results"
    paths = run_rebuild.Paths(
        project_root=tmp_path,
        base_path=tmp_path / "02_data/analysis_ready/macro_growth_merged.csv",
        controls_path=tmp_path / "02_data/supporting/phase1_controls.csv",
        iv_path=tmp_path / "02_data/supporting/phase1_instruments.csv",
        region_map_path=tmp_path / "02_data/supporting/region_map_worldbank_2026-03-26.csv",
        m2_raw_path=tmp_path / "02_data/raw/m2_raw.csv",
        out_root=out_root,
        out_audit=out_root,
        out_audit_tables=out_root / "tables/phase1_audit",
        out_audit_figures=out_root / "figures",
        out_lp=out_root,
        out_lp_tables=out_root / "tables/short_run_lp",
        out_lp_figures=out_root / "figures",
    )
    run_rebuild.ensure_output_dirs(paths)
    return paths


def write_panel_inputs(paths, panel: pd.DataFrame, *, duplicate_controls: bool = False) -> None:
    paths.base_path.parent.mkdir(parents=True, exist_ok=True)
    paths.controls_path.parent.mkdir(parents=True, exist_ok=True)
    paths.iv_path.parent.mkdir(parents=True, exist_ok=True)

    base = panel[["Country Name", "year", "inflation", "gdp_growth", "m2_growth"]].copy()
    controls = panel[["Country Name", "year", "trade_open", "pop_growth", "investment_share"]].copy()
    instruments = panel[["Country Name", "year", "instrument_m2_external_level", "instrument_m2_l1"]].copy()

    if duplicate_controls:
        controls = pd.concat([controls, controls.iloc[[0]]], ignore_index=True)

    base.to_csv(paths.base_path, index=False)
    controls.to_csv(paths.controls_path, index=False)
    instruments.to_csv(paths.iv_path, index=False)


def fake_lp_row(outcome: str, horizon: int, instrument: str) -> dict:
    base = 1.0 if outcome == "inflation" else 0.15
    instrument_shift = 0.2 if instrument == "instrument_m2_l1" else 0.0
    coef = base + instrument_shift - 0.1 * horizon
    return {
        "outcome": outcome,
        "horizon": horizon,
        "instrument": instrument,
        "coef_m2_growth": coef,
        "std_error": 0.05,
        "p_value": 0.04 if outcome == "inflation" else 0.2,
        "ci_low_95": coef - 0.1,
        "ci_high_95": coef + 0.1,
        "nobs": 200,
        "first_stage_stat": 5.0 + horizon,
        "first_stage_p": 0.03,
        "partial_rsquared": 0.02,
        "iv_r2": 0.1,
    }


def test_read_panel_rejects_duplicate_country_year_inputs(tmp_path: Path, small_panel: pd.DataFrame) -> None:
    paths = make_temp_paths(tmp_path)
    write_panel_inputs(paths, small_panel, duplicate_controls=True)

    with pytest.raises(ValueError, match="controls has duplicate Country Name-year rows"):
        run_rebuild.read_panel(paths, logs=[])


def test_build_phase2_lp_raises_when_any_spec_fails(
    tmp_path: Path, small_panel: pd.DataFrame, monkeypatch: pytest.MonkeyPatch
) -> None:
    paths = make_temp_paths(tmp_path)

    def fake_run_lp_iv(_panel: pd.DataFrame, outcome: str, horizon: int, instrument: str) -> dict:
        if outcome == "inflation" and horizon == 3 and instrument == "instrument_m2_l1":
            raise RuntimeError("synthetic estimation failure")
        return fake_lp_row(outcome=outcome, horizon=horizon, instrument=instrument)

    monkeypatch.setattr(run_rebuild, "run_lp_iv", fake_run_lp_iv)

    with pytest.raises(RuntimeError, match="LP-IV estimation failures detected"):
        run_rebuild.build_phase2_lp(small_panel, paths, logs=[])

    assert not (paths.out_lp_tables / "lp_iv_all_results.csv").exists()


def test_build_phase2_lp_writes_complete_exports(
    tmp_path: Path, small_panel: pd.DataFrame, monkeypatch: pytest.MonkeyPatch
) -> None:
    paths = make_temp_paths(tmp_path)

    def fake_run_lp_iv(_panel: pd.DataFrame, outcome: str, horizon: int, instrument: str) -> dict:
        return fake_lp_row(outcome=outcome, horizon=horizon, instrument=instrument)

    monkeypatch.setattr(run_rebuild, "run_lp_iv", fake_run_lp_iv)

    result = run_rebuild.build_phase2_lp(small_panel, paths, logs=[])

    assert len(result["lp_table"]) == 10
    assert len(result["primary"]) == 5
    assert len(result["alt"]) == 5

    all_results = pd.read_csv(paths.out_lp_tables / "lp_iv_all_results.csv")
    primary = pd.read_csv(paths.out_lp_tables / "lp_iv_primary_results.csv")
    alt = pd.read_csv(paths.out_lp_tables / "lp_iv_alt_results.csv")
    summary = pd.read_csv(paths.out_lp_tables / "powerbi_lp_iv_summary.csv")
    metrics = pd.read_csv(paths.out_lp_tables / "interpretation_metrics.csv")

    assert len(all_results) == 10
    assert len(primary) == 5
    assert len(alt) == 5
    assert len(summary) == 10
    assert len(metrics) == 6
    assert set(primary["instrument"]) == {"instrument_m2_external_level"}
    assert set(alt["instrument"]) == {"instrument_m2_l1"}

    assert (paths.out_lp_figures / "irf_primary_inflation.png").exists()
    assert (paths.out_lp_figures / "irf_primary_gdp_growth.png").exists()
    assert (paths.out_lp_figures / "first_stage_by_horizon.png").exists()


def test_build_phase2_lp_keeps_exploratory_status_when_familywise_check_fails(
    tmp_path: Path, small_panel: pd.DataFrame, monkeypatch: pytest.MonkeyPatch
) -> None:
    paths = make_temp_paths(tmp_path)

    def fake_run_lp_iv(_panel: pd.DataFrame, outcome: str, horizon: int, instrument: str) -> dict:
        row = fake_lp_row(outcome=outcome, horizon=horizon, instrument=instrument)
        row["first_stage_stat"] = 12.0
        row["first_stage_p"] = 0.004
        if outcome == "inflation":
            row["p_value"] = 0.04
        else:
            row["p_value"] = 0.2
        return row

    monkeypatch.setattr(run_rebuild, "run_lp_iv", fake_run_lp_iv)

    result = run_rebuild.build_phase2_lp(small_panel, paths, logs=[])

    assert result["inflation_sig"] == 4
    assert result["lp_inference_decision"] == "EVIDENCE_WEAK_REVISIT_IDENTIFICATION"


def test_build_graphs_main_creates_portfolio_outputs(
    tmp_path: Path, small_panel: pd.DataFrame, monkeypatch: pytest.MonkeyPatch
) -> None:
    out_root = tmp_path / "04_current_results"
    tables_audit = out_root / "tables/phase1_audit"
    tables_lp = out_root / "tables/short_run_lp"
    figures = out_root / "figures"
    data_dir = tmp_path / "02_data/analysis_ready"

    tables_audit.mkdir(parents=True, exist_ok=True)
    tables_lp.mkdir(parents=True, exist_ok=True)
    figures.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    core = pd.DataFrame(
        [
            {"model": "fe_baseline_twfe", "outcome": "inflation", "coef_m2_growth": 1.0},
            {"model": "fe_controls_restricted_twfe", "outcome": "inflation", "coef_m2_growth": 0.9},
            {"model": "iv_twfe_external", "outcome": "inflation", "coef_m2_growth": 1.1},
            {"model": "iv_twfe_lag", "outcome": "inflation", "coef_m2_growth": 1.2},
            {"model": "fe_baseline_twfe", "outcome": "gdp_growth", "coef_m2_growth": 0.1},
            {"model": "fe_controls_restricted_twfe", "outcome": "gdp_growth", "coef_m2_growth": 0.1},
            {"model": "iv_twfe_external", "outcome": "gdp_growth", "coef_m2_growth": -0.1},
            {"model": "iv_twfe_lag", "outcome": "gdp_growth", "coef_m2_growth": -0.1},
        ]
    )
    first_stage = pd.DataFrame(
        [
            {"instrument": "instrument_m2_external_level", "outcome": "inflation", "first_stage_stat": 4.2},
            {"instrument": "instrument_m2_external_level", "outcome": "gdp_growth", "first_stage_stat": 4.2},
            {"instrument": "instrument_m2_l1", "outcome": "inflation", "first_stage_stat": 6.3},
            {"instrument": "instrument_m2_l1", "outcome": "gdp_growth", "first_stage_stat": 6.3},
        ]
    )
    gate = pd.DataFrame(
        [
            {"spec": "fe_baseline_twfe", "abs_drift_pct": 0.0},
            {"spec": "fe_controls_restricted_twfe", "abs_drift_pct": 0.1},
            {"spec": "iv_twfe_external", "abs_drift_pct": 0.2},
            {"spec": "period_1991_2005", "abs_drift_pct": 0.3},
            {"spec": "period_2006_2020", "abs_drift_pct": 0.15},
        ]
    )
    stability = pd.DataFrame(
        [
            {"spec": "period_1991_2005", "coef": 0.8, "baseline_coef": 1.0},
            {"spec": "period_2006_2020", "coef": 1.1, "baseline_coef": 1.0},
            {"spec": "tail_exclusion_99pct", "coef": 1.0, "baseline_coef": 1.0},
        ]
    )
    placebo = pd.DataFrame(
        [
            {"test": "lead_placebo", "stat_t2": 2.0},
            {"test": "permutation_placebo", "stat_t2": 1.5},
        ]
    )
    missing = pd.DataFrame(
        [
            {"variable": "m2_growth", "missing_share": 0.0},
            {"variable": "inflation", "missing_share": 0.01},
            {"variable": "gdp_growth", "missing_share": 0.02},
        ]
    )
    lp_all = pd.DataFrame(
        [
            {"instrument": "instrument_m2_external_level", "outcome": "inflation", "horizon": 0, "first_stage_stat": 4.2},
            {"instrument": "instrument_m2_external_level", "outcome": "inflation", "horizon": 1, "first_stage_stat": 4.3},
            {"instrument": "instrument_m2_external_level", "outcome": "inflation", "horizon": 2, "first_stage_stat": 4.4},
            {"instrument": "instrument_m2_external_level", "outcome": "inflation", "horizon": 3, "first_stage_stat": 4.5},
            {"instrument": "instrument_m2_external_level", "outcome": "gdp_growth", "horizon": 0, "first_stage_stat": 4.2},
            {"instrument": "instrument_m2_l1", "outcome": "inflation", "horizon": 0, "first_stage_stat": 6.2},
            {"instrument": "instrument_m2_l1", "outcome": "inflation", "horizon": 1, "first_stage_stat": 6.1},
            {"instrument": "instrument_m2_l1", "outcome": "inflation", "horizon": 2, "first_stage_stat": 6.0},
            {"instrument": "instrument_m2_l1", "outcome": "inflation", "horizon": 3, "first_stage_stat": 5.9},
            {"instrument": "instrument_m2_l1", "outcome": "gdp_growth", "horizon": 0, "first_stage_stat": 6.2},
        ]
    )
    lp_primary = pd.DataFrame(
        [
            {"outcome": "inflation", "horizon": 0, "coef_m2_growth": 1.0, "ci_low_95": 0.8, "ci_high_95": 1.2},
            {"outcome": "inflation", "horizon": 1, "coef_m2_growth": 0.8, "ci_low_95": 0.6, "ci_high_95": 1.0},
            {"outcome": "inflation", "horizon": 2, "coef_m2_growth": 0.6, "ci_low_95": 0.4, "ci_high_95": 0.8},
            {"outcome": "inflation", "horizon": 3, "coef_m2_growth": 0.4, "ci_low_95": 0.2, "ci_high_95": 0.6},
            {"outcome": "gdp_growth", "horizon": 0, "coef_m2_growth": -0.1, "ci_low_95": -0.2, "ci_high_95": 0.0},
        ]
    )
    lp_alt = pd.DataFrame(
        [
            {"outcome": "inflation", "horizon": 0, "coef_m2_growth": 1.1},
            {"outcome": "inflation", "horizon": 1, "coef_m2_growth": 0.9},
            {"outcome": "inflation", "horizon": 2, "coef_m2_growth": 0.7},
            {"outcome": "inflation", "horizon": 3, "coef_m2_growth": 0.5},
            {"outcome": "gdp_growth", "horizon": 0, "coef_m2_growth": 0.0},
        ]
    )

    core.to_csv(tables_audit / "core_model_results.csv", index=False)
    first_stage.to_csv(tables_audit / "first_stage_strength.csv", index=False)
    gate.to_csv(tables_audit / "spec_gate_table.csv", index=False)
    stability.to_csv(tables_audit / "spec_stability_table.csv", index=False)
    placebo.to_csv(tables_audit / "placebo_tests.csv", index=False)
    missing.to_csv(tables_audit / "data_audit_missingness.csv", index=False)
    pd.DataFrame(
        [
            {
                "interpretation_ready": False,
                "claim_tier": "associational",
                "inference_decision": "GO_PIVOT_SHORT_RUN",
            }
        ]
    ).to_csv(tables_audit / "interpretation_status.csv", index=False)
    lp_all.to_csv(tables_lp / "lp_iv_all_results.csv", index=False)
    lp_primary.to_csv(tables_lp / "lp_iv_primary_results.csv", index=False)
    lp_alt.to_csv(tables_lp / "lp_iv_alt_results.csv", index=False)
    small_panel.to_csv(data_dir / "macro_growth_merged.csv", index=False)

    monkeypatch.setattr(build_graphs, "PROJECT_ROOT", tmp_path)
    monkeypatch.setattr(build_graphs, "OUT_DIR", figures)
    monkeypatch.setattr(build_graphs, "TABLES_AUDIT", tables_audit)
    monkeypatch.setattr(build_graphs, "TABLES_LP", tables_lp)

    assert build_graphs.load_non_causal_mode() is True
    build_graphs.main()

    expected_pngs = {
        "01_core_coefficients.png",
        "02_first_stage_strength.png",
        "03_gate_drift.png",
        "04_stability_coefficients.png",
        "05_placebo_strength.png",
        "06_lp_inflation_paths.png",
        "07_lp_gdp_h0_compare.png",
        "08_lp_first_stage_horizon.png",
        "09_missingness.png",
        "10_scatter_m2_vs_inflation.png",
        "11_scatter_m2_vs_gdp_growth.png",
        "12_top20_mean_inflation.png",
        "13_country_means_m2_vs_inflation.png",
    }
    produced = {path.name for path in figures.glob("*.png")}
    assert expected_pngs.issubset(produced)

    manifest = pd.read_csv(figures / "portfolio_graph_manifest.csv")
    assert expected_pngs.issubset(set(manifest["file"]))
    assert set(manifest["claim_tier"]) == {"associational"}
    assert set(manifest["interpretation_ready"]) == {False}
    assert str(manifest["status_header"].iloc[0]).startswith("claim_tier=associational")


def test_write_summary_includes_non_causal_guardrail(tmp_path: Path) -> None:
    paths = make_temp_paths(tmp_path)
    gate_table = pd.DataFrame([{"abs_drift_pct": 0.875}])
    placebo_table = pd.DataFrame([{"p_value": 0.04}, {"p_value": 0.13}])
    audit = {
        "gate_table": gate_table,
        "placebo_table": placebo_table,
        "preferred_first_stage_strong_pass": False,
        "inference_decision": "GO_PIVOT_SHORT_RUN",
        "preferred_first_stage_stat_country": 4.2243,
        "preferred_first_stage_stat_country_year": 3.8016,
        "preferred_first_stage_stat": 3.8016,
        "preferred_first_stage_p": 0.0512,
        "preferred_relevance_agrees_across_clustering": False,
        "interpretation_ready": False,
        "claim_tier": "associational",
        "failed_criteria": ["preferred_first_stage_stat_gt_chi2_95_conservative"],
    }
    lp = {
        "lp_inference_decision": "EVIDENCE_WEAK_REVISIT_IDENTIFICATION",
        "inflation_sig": 4,
        "gdp_sig": 0,
    }

    run_rebuild.write_summary(paths, audit=audit, lp=lp, logs=["ok"])
    summary = (paths.out_root / "summary.md").read_text()

    assert "## Empirical Design Updates" in summary
    assert "## Estimand & Assumptions" in summary
    assert "## Inference Decision" in summary
    assert "## Interpretation Scope" in summary
    assert "INTERPRETATION_READY: `False`" in summary
    assert "Claim tier: `associational`" in summary
    assert "Forbidden claims: policy-effect statements and counterfactual causal-effect statements." in summary
    assert "descriptive association evidence only (non-causal)" in summary
    for banned_phrase in ["causal effect of m2_growth", "identified causal effect", "production-ready"]:
        assert banned_phrase not in summary.lower()


def test_write_summary_includes_causal_scope_when_all_pass(tmp_path: Path) -> None:
    paths = make_temp_paths(tmp_path)
    gate_table = pd.DataFrame([{"abs_drift_pct": 0.12}])
    placebo_table = pd.DataFrame([{"p_value": 0.11}, {"p_value": 0.23}])
    audit = {
        "gate_table": gate_table,
        "placebo_table": placebo_table,
        "preferred_first_stage_strong_pass": True,
        "inference_decision": "GO_CONTINUE",
        "preferred_first_stage_stat_country": 12.2,
        "preferred_first_stage_stat_country_year": 11.1,
        "preferred_first_stage_stat": 11.1,
        "preferred_first_stage_p": 0.001,
        "preferred_relevance_agrees_across_clustering": True,
        "interpretation_ready": True,
        "claim_tier": "causal",
        "failed_criteria": [],
    }
    lp = {
        "lp_inference_decision": "EVIDENCE_SHORT_RUN_EFFECT_PRESENT",
        "inflation_sig": 4,
        "gdp_sig": 0,
    }

    run_rebuild.write_summary(paths, audit=audit, lp=lp, logs=["ok"])
    summary = (paths.out_root / "summary.md").read_text()

    assert "Claim tier: `causal`" in summary
    assert "Causal interpretation is allowed only under stated identification assumptions." in summary
    assert "Forbidden claims: policy-effect statements" not in summary


def test_write_summary_includes_exploratory_scope_when_diagnostics_not_ready(tmp_path: Path) -> None:
    paths = make_temp_paths(tmp_path)
    gate_table = pd.DataFrame([{"abs_drift_pct": 1.2}])
    placebo_table = pd.DataFrame([{"p_value": 0.01}])
    audit = {
        "gate_table": gate_table,
        "placebo_table": placebo_table,
        "preferred_first_stage_strong_pass": False,
        "inference_decision": "GO_PIVOT_SHORT_RUN",
        "preferred_first_stage_stat_country": 1.5,
        "preferred_first_stage_stat_country_year": 1.4,
        "preferred_first_stage_stat": 1.4,
        "preferred_first_stage_p": 0.2,
        "preferred_relevance_agrees_across_clustering": False,
        "interpretation_ready": False,
        "claim_tier": "exploratory",
        "failed_criteria": ["preferred_first_stage_stat_gt_chi2_95_conservative"],
    }
    lp = {
        "lp_inference_decision": "EVIDENCE_WEAK_REVISIT_IDENTIFICATION",
        "inflation_sig": 0,
        "gdp_sig": 0,
    }

    run_rebuild.write_summary(paths, audit=audit, lp=lp, logs=["ok"])
    summary = (paths.out_root / "summary.md").read_text()

    assert "Claim tier: `exploratory`" in summary
    assert "Forbidden claims: policy-effect statements and counterfactual causal-effect statements." in summary
    assert "causal effect of m2_growth" not in summary.lower()


def test_save_adds_non_causal_stamp_text(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(build_graphs, "OUT_DIR", tmp_path)
    monkeypatch.setattr(build_graphs, "NON_CAUSAL_MODE", True)
    monkeypatch.setattr(build_graphs, "CURRENT_CLAIM_TIER", "associational")
    monkeypatch.setattr(build_graphs, "CURRENT_INTERPRETATION_READY", False)

    fig, _ = plt.subplots()
    build_graphs.save(fig, "stamp_test.png")

    text_values = [text.get_text() for text in fig.texts]
    assert "ASSOCIATIONAL EVIDENCE ONLY (IDENTIFICATION NOT PASSED)" in text_values
    assert (tmp_path / "stamp_test.png").exists()
