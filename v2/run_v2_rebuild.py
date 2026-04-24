from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.formula.api as smf
from linearmodels.iv import IV2SLS
from linearmodels.panel import PanelOLS

sns.set_theme(style="whitegrid")
warnings.filterwarnings(
    "ignore",
    message="invalid value encountered in sqrt",
    category=RuntimeWarning,
    module=r"linearmodels\.iv\.results",
)

RESTRICTED_CONTROLS = ["trade_open", "pop_growth", "investment_share"]
PREFERRED_IV = "instrument_m2_external_level"
CHI2_1_95_CRITICAL = 3.841458820694124
STRONG_IV_STAT_THRESHOLD = 10.0
PLACEBO_PERMUTATIONS = 64


@dataclass(frozen=True)
class Paths:
    project_root: Path
    base_path: Path
    controls_path: Path
    iv_path: Path
    region_map_path: Path
    m2_raw_path: Path
    out_root: Path
    out_audit: Path
    out_audit_tables: Path
    out_audit_figures: Path
    out_lp: Path
    out_lp_tables: Path
    out_lp_figures: Path


def build_paths() -> Paths:
    root = Path(__file__).resolve().parents[1]
    out_root = root / "v2/outputs"
    out_audit = out_root / "phase1_audit_v2"
    out_lp = out_root / "phase2_short_run_v2"
    return Paths(
        project_root=root,
        base_path=root / "macro_growth_merged.csv",
        controls_path=root / "data/phase1_controls.csv",
        iv_path=root / "data/phase1_instruments.csv",
        region_map_path=root / "v2/data/region_map_worldbank_2026-03-26.csv",
        m2_raw_path=root / "m2_raw.csv",
        out_root=out_root,
        out_audit=out_audit,
        out_audit_tables=out_audit / "tables",
        out_audit_figures=out_audit / "figures",
        out_lp=out_lp,
        out_lp_tables=out_lp / "tables",
        out_lp_figures=out_lp / "figures",
    )


def ensure_inputs(paths: Paths) -> None:
    required = [
        paths.base_path,
        paths.controls_path,
        paths.iv_path,
        paths.region_map_path,
        paths.m2_raw_path,
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing required inputs: {', '.join(missing)}")


def ensure_output_dirs(paths: Paths) -> None:
    for out_dir in [
        paths.out_root,
        paths.out_audit,
        paths.out_audit_tables,
        paths.out_audit_figures,
        paths.out_lp,
        paths.out_lp_tables,
        paths.out_lp_figures,
    ]:
        out_dir.mkdir(parents=True, exist_ok=True)


def log(message: str, logs: list[str]) -> None:
    print(message)
    logs.append(message)


def read_panel(paths: Paths, logs: list[str]) -> pd.DataFrame:
    base = pd.read_csv(paths.base_path)
    controls = pd.read_csv(paths.controls_path)
    instruments = pd.read_csv(paths.iv_path)

    panel = base.merge(controls, on=["Country Name", "year"], how="left")
    panel = panel.merge(instruments, on=["Country Name", "year"], how="left")
    panel = panel.sort_values(["Country Name", "year"]).copy()

    log(
        "Loaded panel with "
        f"rows={len(panel)}, countries={panel['Country Name'].nunique()}, years={int(panel['year'].min())}-{int(panel['year'].max())}",
        logs,
    )
    return panel


def exact_horizon_series(
    source_df: pd.DataFrame,
    target_df: pd.DataFrame,
    value_col: str,
    horizon: int,
    *,
    entity_col: str = "Country Name",
    time_col: str = "year",
    out_col: str | None = None,
) -> pd.Series:
    """Return y_{t+h} aligned to row t using exact entity-year matching."""
    if horizon < 0:
        raise ValueError("horizon must be non-negative")

    out_col = out_col or f"{value_col}_h{horizon}"
    if horizon == 0:
        return target_df[value_col].copy()

    lookup = source_df[[entity_col, time_col, value_col]].dropna(subset=[value_col]).copy()
    lookup[time_col] = lookup[time_col] - horizon
    lookup = lookup.rename(columns={value_col: out_col}).drop_duplicates([entity_col, time_col], keep="last")

    aligned = target_df[[entity_col, time_col]].merge(lookup, on=[entity_col, time_col], how="left")
    return aligned[out_col]


def fit_fe(panel: pd.DataFrame, outcome: str, controls: list[str] | None = None):
    controls = controls or []
    cols = ["Country Name", "year", outcome, "m2_growth", *controls]
    fit_data = panel[cols].dropna().copy().set_index(["Country Name", "year"]).sort_index()

    rhs = "m2_growth"
    if controls:
        rhs = rhs + " + " + " + ".join(controls)

    formula = f"{outcome} ~ 1 + {rhs} + EntityEffects + TimeEffects"
    result = PanelOLS.from_formula(formula, data=fit_data).fit(cov_type="clustered", cluster_entity=True)
    return result


def fit_iv_twfe(panel: pd.DataFrame, outcome: str, instrument: str, controls: list[str]):
    cols = ["Country Name", "year", outcome, "m2_growth", instrument, *controls]
    fit_data = panel[cols].dropna().copy().rename(columns={"Country Name": "country"})

    formula = f"{outcome} ~ 1"
    if controls:
        formula = formula + " + " + " + ".join(controls)
    formula = formula + f" + C(country) + C(year) [m2_growth ~ {instrument}]"

    result = IV2SLS.from_formula(formula, data=fit_data).fit(cov_type="clustered", clusters=fit_data["country"])
    return result, fit_data


def extract_first_stage(result, instrument: str, outcome: str) -> dict:
    diagnostics = result.first_stage.diagnostics.loc["m2_growth"]
    return {
        "instrument": instrument,
        "outcome": outcome,
        "first_stage_stat": float(diagnostics["f.stat"]),
        "first_stage_p": float(diagnostics["f.pval"]),
        "partial_rsquared": float(diagnostics["partial.rsquared"]),
        "shea_rsquared": float(diagnostics["shea.rsquared"]),
        "dist": str(diagnostics["f.dist"]),
    }


def int_cluster_columns(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "country": pd.factorize(df["country"])[0],
            "year": pd.factorize(df["year"])[0],
        },
        index=df.index,
    )


def sample_derangement(values: np.ndarray, rng: np.random.Generator, max_attempts: int = 2000) -> np.ndarray:
    if len(values) < 2:
        raise ValueError("Need at least two values to build a derangement.")
    for _ in range(max_attempts):
        shuffled = values.copy()
        rng.shuffle(shuffled)
        if not np.any(shuffled == values):
            return shuffled
    raise RuntimeError("Failed to generate a derangement without fixed points.")


def empirical_two_sided_pvalue(observed: float, null_draws: list[float]) -> float:
    if not null_draws:
        return 1.0
    abs_observed = abs(float(observed))
    abs_null = np.abs(np.array(null_draws, dtype=float))
    # +1 correction keeps p-value valid in finite randomization samples.
    return float((1 + int(np.sum(abs_null >= abs_observed))) / (len(abs_null) + 1))


def run_placebo_tests(panel: pd.DataFrame) -> pd.DataFrame:
    lead_base = panel[["Country Name", "year", "m2_growth", *RESTRICTED_CONTROLS]].copy()
    lead_base["instrument_lead"] = exact_horizon_series(
        source_df=panel,
        target_df=lead_base,
        value_col=PREFERRED_IV,
        horizon=1,
        out_col="instrument_lead",
    )
    lead_data = lead_base.dropna(subset=["m2_growth", "instrument_lead", *RESTRICTED_CONTROLS]).copy()
    lead_data = lead_data.sort_values(["Country Name", "year"]).rename(columns={"Country Name": "country"})

    lead_fit = smf.ols(
        "m2_growth ~ instrument_lead + " + " + ".join(RESTRICTED_CONTROLS) + " + C(country) + C(year)",
        data=lead_data,
    ).fit(cov_type="cluster", cov_kwds={"groups": lead_data["country"]})

    perm_base = panel[["Country Name", "year", "m2_growth", PREFERRED_IV, *RESTRICTED_CONTROLS]].dropna().copy()
    perm_base = perm_base.rename(columns={"Country Name": "country"})

    rng = np.random.default_rng(42)
    countries = np.array(sorted(perm_base["country"].unique()))
    permutation_coefs: list[float] = []
    permutation_nobs: list[int] = []

    for _ in range(PLACEBO_PERMUTATIONS):
        shuffled = sample_derangement(countries, rng)
        perm_map = dict(zip(countries, shuffled))
        perm_data = perm_base.copy()
        perm_data["country_perm"] = perm_data["country"].map(perm_map)

        if bool((perm_data["country"] == perm_data["country_perm"]).any()):
            raise RuntimeError("Permutation placebo map contains fixed points; null contamination risk.")

        lookup = perm_data[["country", "year", PREFERRED_IV]].rename(
            columns={"country": "country_perm", PREFERRED_IV: "instrument_perm"}
        )
        perm_data = perm_data.merge(lookup, on=["country_perm", "year"], how="left").dropna(subset=["instrument_perm"])

        perm_fit = smf.ols(
            "m2_growth ~ instrument_perm + " + " + ".join(RESTRICTED_CONTROLS) + " + C(country) + C(year)",
            data=perm_data,
        ).fit(cov_type="cluster", cov_kwds={"groups": perm_data["country"]})
        permutation_coefs.append(float(perm_fit.params["instrument_perm"]))
        permutation_nobs.append(int(perm_fit.nobs))

    observed_fit = smf.ols(
        "m2_growth ~ " + PREFERRED_IV + " + " + " + ".join(RESTRICTED_CONTROLS) + " + C(country) + C(year)",
        data=perm_base,
    ).fit(cov_type="cluster", cov_kwds={"groups": perm_base["country"]})
    observed_coef = float(observed_fit.params[PREFERRED_IV])

    null_mean = float(np.mean(permutation_coefs))
    null_std = float(np.std(permutation_coefs, ddof=1)) if len(permutation_coefs) > 1 else 0.0
    if null_std <= 1e-12:
        stat = 0.0 if abs(observed_coef) <= 1e-12 else np.inf
    else:
        stat = observed_coef / null_std

    permutation_pvalue = empirical_two_sided_pvalue(observed_coef, permutation_coefs)

    return pd.DataFrame(
        [
            {
                "test": "lead_placebo",
                "coef": float(lead_fit.params["instrument_lead"]),
                "p_value": float(lead_fit.pvalues["instrument_lead"]),
                "stat_t_abs": float(abs(lead_fit.tvalues["instrument_lead"])),
                "stat_t2": float(lead_fit.tvalues["instrument_lead"] ** 2),
                "nobs": int(lead_fit.nobs),
            },
            {
                "test": "permutation_placebo",
                "coef": observed_coef,
                "p_value": permutation_pvalue,
                "stat_t_abs": float(abs(stat)),
                "stat_t2": float(stat**2),
                "nobs": int(round(float(np.mean(permutation_nobs)))),
                "num_permutations": PLACEBO_PERMUTATIONS,
                "null_coef_mean": null_mean,
                "null_coef_std": null_std,
            },
        ]
    )


def run_stability_checks(panel: pd.DataFrame, baseline_coef: float, paths: Paths, logs: list[str]) -> pd.DataFrame:
    rows: list[dict] = []

    tail_cutoff = panel["inflation"].quantile(0.99)
    tail_result = fit_fe(panel[panel["inflation"] <= tail_cutoff].copy(), "inflation", controls=[])
    rows.append(
        {
            "spec": "tail_exclusion_99pct",
            "coef": float(tail_result.params["m2_growth"]),
            "p_value": float(tail_result.pvalues["m2_growth"]),
            "nobs": int(tail_result.nobs),
        }
    )

    for lower, upper, name in [(1991, 2005, "period_1991_2005"), (2006, 2020, "period_2006_2020")]:
        split = panel[(panel["year"] >= lower) & (panel["year"] <= upper)].copy()
        split_result = fit_fe(split, "inflation", controls=[])
        rows.append(
            {
                "spec": name,
                "coef": float(split_result.params["m2_growth"]),
                "p_value": float(split_result.pvalues["m2_growth"]),
                "nobs": int(split_result.nobs),
            }
        )

    region_map = pd.read_csv(paths.region_map_path)
    name_code = pd.read_csv(paths.m2_raw_path, skiprows=4)[["Country Name", "Country Code"]].drop_duplicates()
    with_regions = panel.merge(name_code, on="Country Name", how="left")
    with_regions = with_regions.merge(region_map[["Country Code", "region"]], on="Country Code", how="left")

    regions = [
        region
        for region in sorted(with_regions["region"].dropna().unique().tolist())
        if region.strip().lower() != "aggregates"
    ]

    for region in regions:
        subset = with_regions[with_regions["region"] != region].copy()
        try:
            result = fit_fe(subset, "inflation", controls=[])
            rows.append(
                {
                    "spec": f"leave_out_region::{region}",
                    "coef": float(result.params["m2_growth"]),
                    "p_value": float(result.pvalues["m2_growth"]),
                    "nobs": int(result.nobs),
                }
            )
        except Exception as exc:  # pragma: no cover - defensive
            log(f"Region leave-out failed for {region}: {exc}", logs)

    stability = pd.DataFrame(rows)
    stability["baseline_coef"] = baseline_coef
    stability["abs_drift_pct"] = (stability["coef"] - baseline_coef).abs() / (
        abs(baseline_coef) if abs(baseline_coef) > 1e-8 else np.nan
    )
    return stability


def build_phase1_audit(panel: pd.DataFrame, paths: Paths, logs: list[str]) -> dict:
    audit_summary = pd.DataFrame(
        [
            {"check": "rows", "value": int(len(panel))},
            {"check": "countries", "value": int(panel["Country Name"].nunique())},
            {"check": "year_min", "value": int(panel["year"].min())},
            {"check": "year_max", "value": int(panel["year"].max())},
            {"check": "duplicate_country_year_rows", "value": int(panel.duplicated(["Country Name", "year"]).sum())},
        ]
    )
    audit_summary.to_csv(paths.out_audit_tables / "data_audit_summary_v2.csv", index=False)

    missing_table = (
        panel[
            [
                "m2_growth",
                "inflation",
                "gdp_growth",
                "trade_open",
                "gdp_pc_growth",
                "pop_growth",
                "investment_share",
                "instrument_m2_l1",
                "instrument_m2_external_level",
            ]
        ]
        .isna()
        .sum()
        .to_frame("missing_count")
    )
    missing_table["missing_share"] = missing_table["missing_count"] / len(panel)
    missing_table.reset_index().rename(columns={"index": "variable"}).to_csv(
        paths.out_audit_tables / "data_audit_missingness_v2.csv", index=False
    )

    forbidden = {"gdp_pc_growth"}
    proposed = set(RESTRICTED_CONTROLS)
    leakage_flags = pd.DataFrame(
        [
            {
                "rule": "forbidden_controls_in_gdp_models",
                "forbidden_set": ", ".join(sorted(forbidden)),
                "proposed_set": ", ".join(sorted(proposed)),
                "violation": bool(forbidden.intersection(proposed)),
                "action": "use_restricted_controls_excluding_gdp_pc_growth",
            }
        ]
    )
    leakage_flags.to_csv(paths.out_audit_tables / "leakage_flags_v2.csv", index=False)

    core_rows: list[dict] = []
    first_stage_rows: list[dict] = []

    for outcome in ["inflation", "gdp_growth"]:
        baseline = fit_fe(panel, outcome, controls=[])
        core_rows.append(
            {
                "model": "fe_baseline_twfe",
                "outcome": outcome,
                "spec": "core",
                "coef_m2_growth": float(baseline.params["m2_growth"]),
                "std_error_m2_growth": float(baseline.std_errors["m2_growth"]),
                "p_value_m2_growth": float(baseline.pvalues["m2_growth"]),
                "nobs": int(baseline.nobs),
                "r2_within": float(baseline.rsquared_within),
            }
        )

        controlled = fit_fe(panel, outcome, controls=RESTRICTED_CONTROLS)
        core_rows.append(
            {
                "model": "fe_controls_restricted_twfe",
                "outcome": outcome,
                "spec": "core",
                "coef_m2_growth": float(controlled.params["m2_growth"]),
                "std_error_m2_growth": float(controlled.std_errors["m2_growth"]),
                "p_value_m2_growth": float(controlled.pvalues["m2_growth"]),
                "nobs": int(controlled.nobs),
                "r2_within": float(controlled.rsquared_within),
            }
        )

    for instrument, model_name in [
        ("instrument_m2_l1", "iv_twfe_lag"),
        ("instrument_m2_external_level", "iv_twfe_external"),
    ]:
        for outcome in ["inflation", "gdp_growth"]:
            iv_result, iv_data = fit_iv_twfe(panel, outcome=outcome, instrument=instrument, controls=RESTRICTED_CONTROLS)
            first_stage = extract_first_stage(iv_result, instrument=instrument, outcome=outcome)
            first_stage_rows.append({"model": model_name, **first_stage, "nobs": int(iv_result.nobs)})
            core_rows.append(
                {
                    "model": model_name,
                    "outcome": outcome,
                    "spec": "core",
                    "coef_m2_growth": float(iv_result.params["m2_growth"]),
                    "std_error_m2_growth": float(iv_result.std_errors["m2_growth"]),
                    "p_value_m2_growth": float(iv_result.pvalues["m2_growth"]),
                    "nobs": int(iv_result.nobs),
                    "r2": float(iv_result.rsquared),
                    "first_stage_stat": float(first_stage["first_stage_stat"]),
                    "first_stage_p": float(first_stage["first_stage_p"]),
                    "partial_rsquared": float(first_stage["partial_rsquared"]),
                }
            )

    core_table = pd.DataFrame(core_rows)
    first_stage_table = pd.DataFrame(first_stage_rows)
    core_table.to_csv(paths.out_audit_tables / "core_model_results_v2.csv", index=False)
    first_stage_table.to_csv(paths.out_audit_tables / "first_stage_strength_v2.csv", index=False)

    placebo_table = run_placebo_tests(panel)
    placebo_table.to_csv(paths.out_audit_tables / "placebo_tests_v2.csv", index=False)

    baseline_inflation = float(
        core_table.loc[
            (core_table["model"] == "fe_baseline_twfe") & (core_table["outcome"] == "inflation"),
            "coef_m2_growth",
        ].iloc[0]
    )
    stability_table = run_stability_checks(panel, baseline_coef=baseline_inflation, paths=paths, logs=logs)
    stability_table.to_csv(paths.out_audit_tables / "spec_stability_table_v2.csv", index=False)

    def get_core(model: str, metric: str) -> float:
        return float(
            core_table.loc[
                (core_table["model"] == model) & (core_table["outcome"] == "inflation"),
                metric,
            ].iloc[0]
        )

    def get_stability(spec: str, metric: str) -> float:
        return float(stability_table.loc[stability_table["spec"] == spec, metric].iloc[0])

    gate_table = pd.DataFrame(
        [
            {"spec": "fe_baseline_twfe", "coef": get_core("fe_baseline_twfe", "coef_m2_growth"), "p_value": get_core("fe_baseline_twfe", "p_value_m2_growth")},
            {
                "spec": "fe_controls_restricted_twfe",
                "coef": get_core("fe_controls_restricted_twfe", "coef_m2_growth"),
                "p_value": get_core("fe_controls_restricted_twfe", "p_value_m2_growth"),
            },
            {"spec": "iv_twfe_external", "coef": get_core("iv_twfe_external", "coef_m2_growth"), "p_value": get_core("iv_twfe_external", "p_value_m2_growth")},
            {"spec": "period_1991_2005", "coef": get_stability("period_1991_2005", "coef"), "p_value": get_stability("period_1991_2005", "p_value")},
            {"spec": "period_2006_2020", "coef": get_stability("period_2006_2020", "coef"), "p_value": get_stability("period_2006_2020", "p_value")},
        ]
    )
    gate_table["abs_drift_pct"] = (gate_table["coef"] - baseline_inflation).abs() / (
        abs(baseline_inflation) if abs(baseline_inflation) > 1e-8 else np.nan
    )
    gate_table.to_csv(paths.out_audit_tables / "spec_gate_table_v2.csv", index=False)

    # Inference sensitivity snapshot (one-way vs two-way cluster on key specs)
    iv_core_data = panel[["Country Name", "year", "inflation", "m2_growth", PREFERRED_IV, *RESTRICTED_CONTROLS]].dropna().copy()
    iv_core_data = iv_core_data.rename(columns={"Country Name": "country"})
    core_formula = (
        "inflation ~ 1 + "
        + " + ".join(RESTRICTED_CONTROLS)
        + f" + C(country) + C(year) [m2_growth ~ {PREFERRED_IV}]"
    )
    one_way = IV2SLS.from_formula(core_formula, data=iv_core_data).fit(cov_type="clustered", clusters=iv_core_data["country"])
    two_way = IV2SLS.from_formula(core_formula, data=iv_core_data).fit(
        cov_type="clustered", clusters=int_cluster_columns(iv_core_data)
    )

    sensitivity = pd.DataFrame(
        [
            {
                "check": "core_iv_inflation_first_stage",
                "clustering": "country",
                "first_stage_stat": float(one_way.first_stage.diagnostics.loc["m2_growth", "f.stat"]),
                "first_stage_p": float(one_way.first_stage.diagnostics.loc["m2_growth", "f.pval"]),
                "coef": float(one_way.params["m2_growth"]),
                "p_value": float(one_way.pvalues["m2_growth"]),
            },
            {
                "check": "core_iv_inflation_first_stage",
                "clustering": "country_year",
                "first_stage_stat": float(two_way.first_stage.diagnostics.loc["m2_growth", "f.stat"]),
                "first_stage_p": float(two_way.first_stage.diagnostics.loc["m2_growth", "f.pval"]),
                "coef": float(two_way.params["m2_growth"]),
                "p_value": float(two_way.pvalues["m2_growth"]),
            },
        ]
    )
    sensitivity.to_csv(paths.out_audit_tables / "inference_sensitivity_v2.csv", index=False)

    preferred_country = sensitivity.loc[sensitivity["clustering"] == "country"].iloc[0]
    preferred_country_year = sensitivity.loc[sensitivity["clustering"] == "country_year"].iloc[0]

    preferred_stat_country = float(preferred_country["first_stage_stat"])
    preferred_p_country = float(preferred_country["first_stage_p"])
    preferred_stat_country_year = float(preferred_country_year["first_stage_stat"])
    preferred_p_country_year = float(preferred_country_year["first_stage_p"])

    # Canonical gate is conservative: use weakest stat / largest p across supported clustering choices.
    preferred_stat_conservative = min(preferred_stat_country, preferred_stat_country_year)
    preferred_p_conservative = max(preferred_p_country, preferred_p_country_year)

    relevance_country = bool(preferred_stat_country > CHI2_1_95_CRITICAL and preferred_p_country < 0.05)
    relevance_country_year = bool(preferred_stat_country_year > CHI2_1_95_CRITICAL and preferred_p_country_year < 0.05)
    clustering_agrees_on_relevance = bool(relevance_country == relevance_country_year)

    gdp_core = core_table[core_table["outcome"] == "gdp_growth"].copy()
    placebo_significant = int((placebo_table["p_value"] < 0.05).sum())

    scorecard = pd.DataFrame(
        [
            {
                "criterion": "preferred_first_stage_stat_gt_chi2_95_conservative",
                "value": preferred_stat_conservative,
                "threshold": f">{CHI2_1_95_CRITICAL:.4f}",
                "pass": bool(preferred_stat_conservative > CHI2_1_95_CRITICAL),
            },
            {
                "criterion": "preferred_first_stage_stat_ge_10_for_strong_iv_conservative",
                "value": preferred_stat_conservative,
                "threshold": f">={STRONG_IV_STAT_THRESHOLD:.1f}",
                "pass": bool(preferred_stat_conservative >= STRONG_IV_STAT_THRESHOLD),
            },
            {
                "criterion": "preferred_first_stage_p_lt_0p05_conservative",
                "value": preferred_p_conservative,
                "threshold": "<0.05",
                "pass": bool(preferred_p_conservative < 0.05),
            },
            {
                "criterion": "preferred_relevance_agrees_across_clustering",
                "value": int(clustering_agrees_on_relevance),
                "threshold": "1",
                "pass": bool(clustering_agrees_on_relevance),
            },
            {
                "criterion": "inflation_positive_sign_at_least_4_of_5",
                "value": int((gate_table["coef"] > 0).sum()),
                "threshold": ">=4",
                "pass": bool((gate_table["coef"] > 0).sum() >= 4),
            },
            {
                "criterion": "max_inflation_drift_lt_40pct",
                "value": float(gate_table["abs_drift_pct"].max()),
                "threshold": "<0.40",
                "pass": bool(gate_table["abs_drift_pct"].max() < 0.40),
            },
            {
                "criterion": "gdp_effect_weak_all_core_specs",
                "value": f"{int((gdp_core['p_value_m2_growth'] >= 0.05).sum())}/{int(len(gdp_core))}",
                "threshold": "all p>=0.05",
                "pass": bool((gdp_core["p_value_m2_growth"] >= 0.05).all()),
            },
            {
                "criterion": "placebo_tests_not_significant",
                "value": placebo_significant,
                "threshold": "0 significant",
                "pass": bool(placebo_significant == 0),
            },
        ]
    )

    recommendation = "GO_CONTINUE" if bool(scorecard["pass"].all()) else "GO_PIVOT_SHORT_RUN"
    scorecard["recommendation_if_fail"] = np.where(scorecard["pass"], "", "GO_PIVOT_SHORT_RUN")
    scorecard.to_csv(paths.out_audit_tables / "audit_scorecard_v2.csv", index=False)

    powerbi_core = core_table.copy()
    powerbi_core["abs_coef"] = powerbi_core["coef_m2_growth"].abs()
    powerbi_core["is_significant_5pct"] = powerbi_core["p_value_m2_growth"] < 0.05
    powerbi_core["recommendation"] = recommendation
    powerbi_core["preferred_first_stage_stat_conservative"] = preferred_stat_conservative
    powerbi_core["preferred_first_stage_p_conservative"] = preferred_p_conservative
    powerbi_core.to_csv(paths.out_audit_tables / "powerbi_model_summary_v2.csv", index=False)

    # Audit figures
    fig, ax = plt.subplots(figsize=(9, 4))
    sns.barplot(data=gate_table, x="spec", y="coef", ax=ax)
    ax.axhline(0, color="black", linewidth=1)
    ax.axhline(baseline_inflation, color="red", linestyle="--", label="Baseline FE coef")
    ax.set_title("V2 Inflation Coefficient Across Gate Specs")
    ax.set_ylabel("Coefficient on m2_growth")
    ax.tick_params(axis="x", rotation=25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(paths.out_audit_figures / "stability_coefficients_gate_v2.png", dpi=170)
    plt.close(fig)

    fig2, ax2 = plt.subplots(figsize=(9, 4))
    fs_plot = first_stage_table[["instrument", "first_stage_stat"]].drop_duplicates().rename(
        columns={"first_stage_stat": "value"}
    )
    fs_plot["metric"] = "first_stage_stat"
    placebo_plot = placebo_table[["test", "stat_t2"]].rename(columns={"test": "instrument", "stat_t2": "value"})
    placebo_plot["metric"] = "placebo_t2"
    combo = pd.concat(
        [fs_plot[["instrument", "value", "metric"]], placebo_plot[["instrument", "value", "metric"]]],
        ignore_index=True,
    )
    sns.barplot(data=combo, x="instrument", y="value", hue="metric", ax=ax2)
    ax2.axhline(CHI2_1_95_CRITICAL, color="red", linestyle="--", label="chi2(1) 95% critical")
    ax2.set_title("V2 First-Stage and Placebo Diagnostics")
    ax2.tick_params(axis="x", rotation=20)
    ax2.legend()
    fig2.tight_layout()
    fig2.savefig(paths.out_audit_figures / "first_stage_and_placebo_strength_v2.png", dpi=170)
    plt.close(fig2)

    log(f"Phase 1 audit completed. Recommendation={recommendation}", logs)

    return {
        "core_table": core_table,
        "first_stage_table": first_stage_table,
        "placebo_table": placebo_table,
        "gate_table": gate_table,
        "scorecard": scorecard,
        "recommendation": recommendation,
        "preferred_first_stage_stat": preferred_stat_conservative,
        "preferred_first_stage_p": preferred_p_conservative,
        "preferred_first_stage_stat_country": preferred_stat_country,
        "preferred_first_stage_p_country": preferred_p_country,
        "preferred_first_stage_stat_country_year": preferred_stat_country_year,
        "preferred_first_stage_p_country_year": preferred_p_country_year,
        "preferred_first_stage_relevance_pass": bool(preferred_stat_conservative > CHI2_1_95_CRITICAL and preferred_p_conservative < 0.05),
        "preferred_first_stage_strong_pass": bool(preferred_stat_conservative >= STRONG_IV_STAT_THRESHOLD),
        "preferred_relevance_agrees_across_clustering": clustering_agrees_on_relevance,
    }


def run_lp_iv(panel: pd.DataFrame, outcome: str, horizon: int, instrument: str) -> dict:
    y_col = f"{outcome}_h{horizon}"
    cols = ["Country Name", "year", y_col, "m2_growth", instrument, *RESTRICTED_CONTROLS]
    fit_data = panel[cols].dropna().copy().rename(columns={"Country Name": "country"})

    formula = f"{y_col} ~ 1 + " + " + ".join(RESTRICTED_CONTROLS) + f" + C(country) + C(year) [m2_growth ~ {instrument}]"
    result = IV2SLS.from_formula(formula, data=fit_data).fit(cov_type="clustered", clusters=fit_data["country"])

    diagnostics = result.first_stage.diagnostics.loc["m2_growth"]
    coef = float(result.params["m2_growth"])
    std_error = float(result.std_errors["m2_growth"])

    return {
        "outcome": outcome,
        "horizon": horizon,
        "instrument": instrument,
        "coef_m2_growth": coef,
        "std_error": std_error,
        "p_value": float(result.pvalues["m2_growth"]),
        "ci_low_95": coef - 1.96 * std_error,
        "ci_high_95": coef + 1.96 * std_error,
        "nobs": int(result.nobs),
        "first_stage_stat": float(diagnostics["f.stat"]),
        "first_stage_p": float(diagnostics["f.pval"]),
        "partial_rsquared": float(diagnostics["partial.rsquared"]),
        "iv_r2": float(result.rsquared),
    }


def build_phase2_lp(panel: pd.DataFrame, paths: Paths, logs: list[str]) -> dict:
    lp_panel = panel.copy()
    horizons = {
        "inflation": [0, 1, 2, 3],
        "gdp_growth": [0],
    }

    for outcome, horizon_list in horizons.items():
        for horizon in horizon_list:
            out_col = f"{outcome}_h{horizon}"
            lp_panel[out_col] = exact_horizon_series(
                source_df=panel,
                target_df=lp_panel,
                value_col=outcome,
                horizon=horizon,
                out_col=out_col,
            )

    rows: list[dict] = []
    failures: list[str] = []
    for instrument in ["instrument_m2_external_level", "instrument_m2_l1"]:
        for outcome, horizon_list in horizons.items():
            for horizon in horizon_list:
                try:
                    rows.append(run_lp_iv(lp_panel, outcome=outcome, horizon=horizon, instrument=instrument))
                except Exception as exc:  # pragma: no cover - defensive
                    failures.append(f"outcome={outcome},h={horizon},instrument={instrument},err={exc}")

    expected_rows = sum(len(h) for h in horizons.values()) * 2
    if failures:
        raise RuntimeError("LP-IV estimation failures detected:\n" + "\n".join(failures))
    if len(rows) != expected_rows:
        raise RuntimeError(f"LP-IV row mismatch: expected {expected_rows}, got {len(rows)}")

    lp_table = pd.DataFrame(rows).sort_values(["instrument", "outcome", "horizon"])
    lp_table.to_csv(paths.out_lp_tables / "lp_iv_all_results_v2.csv", index=False)

    primary = lp_table[lp_table["instrument"] == "instrument_m2_external_level"].copy()
    alt = lp_table[lp_table["instrument"] == "instrument_m2_l1"].copy()
    primary.to_csv(paths.out_lp_tables / "lp_iv_primary_results_v2.csv", index=False)
    alt.to_csv(paths.out_lp_tables / "lp_iv_alt_results_v2.csv", index=False)

    powerbi = lp_table.copy()
    powerbi["is_sig_5pct"] = powerbi["p_value"] < 0.05
    powerbi["abs_coef"] = powerbi["coef_m2_growth"].abs()
    powerbi.to_csv(paths.out_lp_tables / "powerbi_lp_iv_summary_v2.csv", index=False)

    for outcome, horizon_list in horizons.items():
        plot_data = primary[primary["outcome"] == outcome].sort_values("horizon")
        if plot_data.empty:
            continue

        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(plot_data["horizon"], plot_data["coef_m2_growth"], marker="o", label="LP-IV coefficient")
        ax.fill_between(plot_data["horizon"], plot_data["ci_low_95"], plot_data["ci_high_95"], alpha=0.25, label="95% CI")
        ax.axhline(0, color="black", linewidth=1)
        if len(horizon_list) == 1:
            ax.set_title(f"V2 IV Estimate: {outcome} at h=0 (static, primary IV)")
        else:
            ax.set_title(f"V2 LP-IV Path: {outcome} (primary IV)")
        ax.set_xlabel("Horizon (years)")
        ax.set_ylabel("Effect of m2_growth shock")
        ax.legend()
        fig.tight_layout()
        fig.savefig(paths.out_lp_figures / f"irf_primary_{outcome}_v2.png", dpi=170)
        plt.close(fig)

    fs_plot = lp_table.groupby(["instrument", "horizon"], as_index=False)["first_stage_stat"].mean()
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    sns.lineplot(data=fs_plot, x="horizon", y="first_stage_stat", hue="instrument", marker="o", ax=ax2)
    ax2.axhline(CHI2_1_95_CRITICAL, color="red", linestyle="--", label="chi2(1) 95% critical")
    ax2.set_title("V2 First-Stage Strength by Horizon")
    ax2.set_ylabel("First-stage stat")
    ax2.legend()
    fig2.tight_layout()
    fig2.savefig(paths.out_lp_figures / "first_stage_by_horizon_v2.png", dpi=170)
    plt.close(fig2)

    primary_inflation = primary[primary["outcome"] == "inflation"].sort_values("horizon")
    primary_gdp = primary[primary["outcome"] == "gdp_growth"].sort_values("horizon")

    inflation_sig = int((primary_inflation["p_value"] < 0.05).sum())
    gdp_sig = int((primary_gdp["p_value"] < 0.05).sum())

    metrics = pd.DataFrame(
        [
            {"metric": "inflation_sig_horizons_primary", "value": inflation_sig},
            {"metric": "gdp_sig_horizons_primary", "value": gdp_sig},
            {"metric": "gdp_horizon_mode_primary", "value": "static_h0_only"},
            {"metric": "mean_first_stage_stat_primary", "value": float(primary["first_stage_stat"].mean())},
            {"metric": "mean_first_stage_stat_alt_lag", "value": float(alt["first_stage_stat"].mean()) if len(alt) else np.nan},
            {"metric": "min_first_stage_stat_primary", "value": float(primary["first_stage_stat"].min()) if len(primary) else np.nan},
        ]
    )
    metrics.to_csv(paths.out_lp_tables / "phase2_interpretation_metrics_v2.csv", index=False)

    # Keep the recommendation conservative for portfolio communication.
    # Even with chi2 significance, we only mark "effect present" when first-stage stats are comfortably strong.
    lp_recommendation = (
        "EVIDENCE_SHORT_RUN_EFFECT_PRESENT"
        if inflation_sig >= 1 and float(primary["first_stage_stat"].min()) >= 10.0
        else "EVIDENCE_WEAK_REVISIT_IDENTIFICATION"
    )

    log(f"Phase 2 LP-IV completed. Recommendation={lp_recommendation}", logs)

    return {
        "lp_table": lp_table,
        "primary": primary,
        "alt": alt,
        "inflation_sig": inflation_sig,
        "gdp_sig": gdp_sig,
        "lp_recommendation": lp_recommendation,
    }


def write_summary(paths: Paths, audit: dict, lp: dict, logs: list[str]) -> None:
    max_drift = float(audit["gate_table"]["abs_drift_pct"].max())
    strong_iv_status = "PASS" if audit["preferred_first_stage_strong_pass"] else "FAIL"

    summary_lines = [
        "# V2 Rebuild Summary",
        "",
        "## What changed",
        "- Kept exact FE formulas for IV estimation.",
        "- Kept exact calendar-year horizon matching (no row-shift approximation).",
        "- Added explicit no-partial-export checks for LP-IV outputs.",
        "- Added inference sensitivity table comparing one-way vs two-way clustering on key IV spec.",
        "- Clarified weak-IV read: first-stage is reported as clustered Wald chi2(1), not classic F-stat.",
        "",
        "## Phase 1 Audit V2",
        f"- Recommendation: `{audit['recommendation']}`",
        f"- Preferred first-stage stat (country clustering): `{audit['preferred_first_stage_stat_country']:.4f}`",
        f"- Preferred first-stage stat (country+year clustering): `{audit['preferred_first_stage_stat_country_year']:.4f}`",
        f"- Canonical conservative first-stage stat: `{audit['preferred_first_stage_stat']:.4f}`",
        f"- Canonical conservative first-stage p-value: `{audit['preferred_first_stage_p']:.4f}`",
        f"- Relevance agreement across clustering choices: `{audit['preferred_relevance_agrees_across_clustering']}`",
        f"- Preferred first-stage strong-IV threshold (>=10, conservative): `{strong_iv_status}`",
        f"- Max inflation drift across gate specs: `{max_drift:.4f}`",
        f"- Placebo significant tests (p<0.05): `{int((audit['placebo_table']['p_value'] < 0.05).sum())}`",
        "",
        "## Phase 2 LP-IV V2",
        f"- Recommendation flag: `{lp['lp_recommendation']}`",
        f"- Primary IV inflation significant horizons (5%): `{lp['inflation_sig']}`",
        f"- Primary IV GDP significant horizons (5%): `{lp['gdp_sig']}` (static h=0 only)",
        "",
        "## Claim boundary",
        "- Treat this as strong cross-country association evidence.",
        "- Causal interpretation remains limited while first-stage strength is weak/moderate.",
    ]

    (paths.out_root / "V2_SUMMARY.md").write_text("\n".join(summary_lines))
    (paths.out_root / "v2_run_log.md").write_text("\n".join(["# V2 Run Log", "", *[f"- {msg}" for msg in logs]]))


def main() -> None:
    paths = build_paths()
    logs: list[str] = []

    ensure_output_dirs(paths)
    ensure_inputs(paths)

    panel = read_panel(paths, logs)
    audit = build_phase1_audit(panel, paths, logs)
    lp = build_phase2_lp(panel, paths, logs)
    write_summary(paths, audit, lp, logs)

    print("V2 rebuild completed.")
    print("Audit outputs:", paths.out_audit)
    print("LP outputs:", paths.out_lp)
    print("Summary:", paths.out_root / "V2_SUMMARY.md")


if __name__ == "__main__":
    main()
