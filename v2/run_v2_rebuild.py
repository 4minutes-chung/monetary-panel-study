from __future__ import annotations

from pathlib import Path
import warnings
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from linearmodels.panel import PanelOLS
from linearmodels.iv import IV2SLS

warnings.filterwarnings("ignore")
sns.set_theme(style="whitegrid")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BASE_PATH = PROJECT_ROOT / "macro_growth_merged.csv"
CTRL_PATH = PROJECT_ROOT / "data/phase1_controls.csv"
IV_PATH = PROJECT_ROOT / "data/phase1_instruments.csv"
REGION_MAP_PATH = PROJECT_ROOT / "v2/data/region_map_worldbank_2026-03-26.csv"
M2_RAW_PATH = PROJECT_ROOT / "m2_raw.csv"

OUT_ROOT = PROJECT_ROOT / "v2/outputs"
OUT_AUDIT = OUT_ROOT / "phase1_audit_v2"
OUT_AUDIT_T = OUT_AUDIT / "tables"
OUT_AUDIT_F = OUT_AUDIT / "figures"
OUT_LP = OUT_ROOT / "phase2_short_run_v2"
OUT_LP_T = OUT_LP / "tables"
OUT_LP_F = OUT_LP / "figures"

for p in [OUT_ROOT, OUT_AUDIT, OUT_AUDIT_T, OUT_AUDIT_F, OUT_LP, OUT_LP_T, OUT_LP_F]:
    p.mkdir(parents=True, exist_ok=True)

LOG_LINES: list[str] = []


def log(msg: str) -> None:
    print(msg)
    LOG_LINES.append(str(msg))


for req in [BASE_PATH, CTRL_PATH, IV_PATH, REGION_MAP_PATH, M2_RAW_PATH]:
    if not req.exists():
        raise FileNotFoundError(f"Missing required input: {req}")

base = pd.read_csv(BASE_PATH)
ctrl = pd.read_csv(CTRL_PATH)
iv = pd.read_csv(IV_PATH)

# Master merged panel used by both audit and LP stages.
df = base.merge(ctrl, on=["Country Name", "year"], how="left")
df = df.merge(iv, on=["Country Name", "year"], how="left")
df = df.sort_values(["Country Name", "year"]).copy()

restricted_controls = ["trade_open", "pop_growth", "investment_share"]

# -----------------------------
# Phase 1 Audit V2 (corrected)
# -----------------------------

audit_summary = pd.DataFrame(
    [
        {"check": "rows", "value": int(len(df))},
        {"check": "countries", "value": int(df["Country Name"].nunique())},
        {"check": "year_min", "value": int(df["year"].min())},
        {"check": "year_max", "value": int(df["year"].max())},
        {"check": "duplicate_country_year_rows", "value": int(df.duplicated(["Country Name", "year"]).sum())},
    ]
)
audit_summary.to_csv(OUT_AUDIT_T / "data_audit_summary_v2.csv", index=False)

audit_missing = (
    df[
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
audit_missing["missing_share"] = audit_missing["missing_count"] / len(df)
audit_missing.reset_index().rename(columns={"index": "variable"}).to_csv(
    OUT_AUDIT_T / "data_audit_missingness_v2.csv", index=False
)

forbidden_for_gdp = {"gdp_pc_growth"}
proposed_controls = set(restricted_controls)
leakage_flags = pd.DataFrame(
    [
        {
            "rule": "forbidden_controls_in_gdp_models",
            "forbidden_set": ", ".join(sorted(forbidden_for_gdp)),
            "proposed_set": ", ".join(sorted(proposed_controls)),
            "violation": bool(len(forbidden_for_gdp.intersection(proposed_controls)) > 0),
            "action": "use_restricted_controls_excluding_gdp_pc_growth",
        }
    ]
)
leakage_flags.to_csv(OUT_AUDIT_T / "leakage_flags_v2.csv", index=False)


def fit_fe(df_in: pd.DataFrame, outcome: str, controls: list[str] | None = None):
    controls = controls or []
    cols = ["Country Name", "year", outcome, "m2_growth"] + controls
    d = df_in[cols].dropna().copy()
    d = d.set_index(["Country Name", "year"]).sort_index()
    rhs = "m2_growth"
    if controls:
        rhs += " + " + " + ".join(controls)
    formula = f"{outcome} ~ 1 + {rhs} + EntityEffects + TimeEffects"
    res = PanelOLS.from_formula(formula, data=d).fit(cov_type="clustered", cluster_entity=True)
    return res, d


def fit_iv_twfe(df_in: pd.DataFrame, outcome: str, instrument: str, controls: list[str]):
    cols = ["Country Name", "year", outcome, "m2_growth", instrument] + controls
    d = df_in[cols].dropna().copy().rename(columns={"Country Name": "country"})
    formula = f"{outcome} ~ 1"
    if controls:
        formula += " + " + " + ".join(controls)
    formula += f" + C(country) + C(year) [m2_growth ~ {instrument}]"
    res = IV2SLS.from_formula(formula, data=d).fit(cov_type="clustered", clusters=d["country"])
    return res, d


def first_stage_row(iv_res, instrument: str, outcome: str):
    diag = iv_res.first_stage.diagnostics.loc["m2_growth"]
    return {
        "instrument": instrument,
        "outcome": outcome,
        "first_stage_stat": float(diag["f.stat"]),
        "first_stage_p": float(diag["f.pval"]),
        "partial_rsquared": float(diag["partial.rsquared"]),
        "shea_rsquared": float(diag["shea.rsquared"]),
        "dist": str(diag["f.dist"]),
    }


core_rows: list[dict] = []
first_stage_rows: list[dict] = []

# FE baseline
for outcome in ["inflation", "gdp_growth"]:
    res, d_used = fit_fe(df, outcome, controls=[])
    core_rows.append(
        {
            "model": "fe_baseline_twfe",
            "outcome": outcome,
            "spec": "core",
            "coef_m2_growth": float(res.params["m2_growth"]),
            "std_error_m2_growth": float(res.std_errors["m2_growth"]),
            "p_value_m2_growth": float(res.pvalues["m2_growth"]),
            "nobs": int(res.nobs),
            "r2_within": float(res.rsquared_within),
        }
    )

# FE + restricted controls
for outcome in ["inflation", "gdp_growth"]:
    res, d_used = fit_fe(df, outcome, controls=restricted_controls)
    core_rows.append(
        {
            "model": "fe_controls_restricted_twfe",
            "outcome": outcome,
            "spec": "core",
            "coef_m2_growth": float(res.params["m2_growth"]),
            "std_error_m2_growth": float(res.std_errors["m2_growth"]),
            "p_value_m2_growth": float(res.pvalues["m2_growth"]),
            "nobs": int(res.nobs),
            "r2_within": float(res.rsquared_within),
        }
    )

# IV core models + first-stage diagnostics extracted from same fitted model
for instrument, model_name in [
    ("instrument_m2_l1", "iv_twfe_lag"),
    ("instrument_m2_external_level", "iv_twfe_external"),
]:
    for outcome in ["inflation", "gdp_growth"]:
        res, d_used = fit_iv_twfe(df, outcome, instrument=instrument, controls=restricted_controls)
        fs = first_stage_row(res, instrument=instrument, outcome=outcome)
        first_stage_rows.append({"model": model_name, **fs, "nobs": int(res.nobs)})
        core_rows.append(
            {
                "model": model_name,
                "outcome": outcome,
                "spec": "core",
                "coef_m2_growth": float(res.params["m2_growth"]),
                "std_error_m2_growth": float(res.std_errors["m2_growth"]),
                "p_value_m2_growth": float(res.pvalues["m2_growth"]),
                "nobs": int(res.nobs),
                "r2": float(res.rsquared),
                "first_stage_stat": float(fs["first_stage_stat"]),
                "first_stage_p": float(fs["first_stage_p"]),
                "partial_rsquared": float(fs["partial_rsquared"]),
            }
        )

core_tbl = pd.DataFrame(core_rows)
core_tbl.to_csv(OUT_AUDIT_T / "core_model_results_v2.csv", index=False)
first_stage_tbl = pd.DataFrame(first_stage_rows)
first_stage_tbl.to_csv(OUT_AUDIT_T / "first_stage_strength_v2.csv", index=False)

# Placebo tests with clustered SE
preferred_iv = "instrument_m2_external_level"
rng = np.random.default_rng(42)

lead_data = df[["Country Name", "year", "m2_growth", preferred_iv] + restricted_controls].dropna().copy()
lead_data = lead_data.sort_values(["Country Name", "year"]).rename(columns={"Country Name": "country"})
lead_data["instrument_lead"] = lead_data.groupby("country")[preferred_iv].shift(-1)
lead_data = lead_data.dropna(subset=["instrument_lead"])
lead_fit = smf.ols(
    "m2_growth ~ instrument_lead + " + " + ".join(restricted_controls) + " + C(country) + C(year)",
    data=lead_data,
).fit(cov_type="cluster", cov_kwds={"groups": lead_data["country"]})

perm_data = df[["Country Name", "year", "m2_growth", preferred_iv] + restricted_controls].dropna().copy()
perm_data = perm_data.rename(columns={"Country Name": "country"})
all_countries = np.array(sorted(perm_data["country"].unique()))
shuffled = all_countries.copy()
rng.shuffle(shuffled)
country_map = dict(zip(all_countries, shuffled))
perm_data["country_perm"] = perm_data["country"].map(country_map)
lookup = perm_data[["country", "year", preferred_iv]].rename(
    columns={"country": "country_perm", preferred_iv: "instrument_perm"}
)
perm_data = perm_data.merge(lookup, on=["country_perm", "year"], how="left").dropna(subset=["instrument_perm"])
perm_fit = smf.ols(
    "m2_growth ~ instrument_perm + " + " + ".join(restricted_controls) + " + C(country) + C(year)",
    data=perm_data,
).fit(cov_type="cluster", cov_kwds={"groups": perm_data["country"]})

placebo_tbl = pd.DataFrame(
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
            "coef": float(perm_fit.params["instrument_perm"]),
            "p_value": float(perm_fit.pvalues["instrument_perm"]),
            "stat_t_abs": float(abs(perm_fit.tvalues["instrument_perm"])),
            "stat_t2": float(perm_fit.tvalues["instrument_perm"] ** 2),
            "nobs": int(perm_fit.nobs),
        },
    ]
)
placebo_tbl.to_csv(OUT_AUDIT_T / "placebo_tests_v2.csv", index=False)

# Stability checks
stab_rows: list[dict] = []
baseline_coef = float(
    core_tbl.loc[
        (core_tbl["model"] == "fe_baseline_twfe") & (core_tbl["outcome"] == "inflation"),
        "coef_m2_growth",
    ].iloc[0]
)

# Tail exclusion
tail_cut = df["inflation"].quantile(0.99)
r_tail, _ = fit_fe(df[df["inflation"] <= tail_cut].copy(), "inflation", controls=[])
stab_rows.append(
    {
        "spec": "tail_exclusion_99pct",
        "coef": float(r_tail.params["m2_growth"]),
        "p_value": float(r_tail.pvalues["m2_growth"]),
        "nobs": int(r_tail.nobs),
    }
)

# Period splits
for lo, hi, nm in [(1991, 2005, "period_1991_2005"), (2006, 2020, "period_2006_2020")]:
    d_split = df[(df["year"] >= lo) & (df["year"] <= hi)].copy()
    r, _ = fit_fe(d_split, "inflation", controls=[])
    stab_rows.append(
        {
            "spec": nm,
            "coef": float(r.params["m2_growth"]),
            "p_value": float(r.pvalues["m2_growth"]),
            "nobs": int(r.nobs),
        }
    )

# Leave-one-region-out (ALL regions, no cap)
region_map = pd.read_csv(REGION_MAP_PATH)
name_code = pd.read_csv(M2_RAW_PATH, skiprows=4)[["Country Name", "Country Code"]].drop_duplicates()
d_reg = (
    df.merge(name_code, on="Country Name", how="left")
    .merge(region_map[["Country Code", "region"]], on="Country Code", how="left")
)
regions = [
    x
    for x in sorted(d_reg["region"].dropna().unique().tolist())
    if x.strip().lower() != "aggregates"
]
for rg in regions:
    sub = d_reg[d_reg["region"] != rg].copy()
    try:
        r, _ = fit_fe(sub, "inflation", controls=[])
        stab_rows.append(
            {
                "spec": f"leave_out_region::{rg}",
                "coef": float(r.params["m2_growth"]),
                "p_value": float(r.pvalues["m2_growth"]),
                "nobs": int(r.nobs),
            }
        )
    except Exception as e:
        log(f"Region leave-out failed for {rg}: {e}")

stab_tbl = pd.DataFrame(stab_rows)
stab_tbl["baseline_coef"] = baseline_coef
stab_tbl["abs_drift_pct"] = (stab_tbl["coef"] - baseline_coef).abs() / (
    abs(baseline_coef) if abs(baseline_coef) > 1e-8 else np.nan
)
stab_tbl.to_csv(OUT_AUDIT_T / "spec_stability_table_v2.csv", index=False)

# Gate table (same 5 specs)
get_core = lambda m: float(
    core_tbl.loc[
        (core_tbl["model"] == m) & (core_tbl["outcome"] == "inflation"),
        "coef_m2_growth",
    ].iloc[0]
)
get_core_p = lambda m: float(
    core_tbl.loc[
        (core_tbl["model"] == m) & (core_tbl["outcome"] == "inflation"),
        "p_value_m2_growth",
    ].iloc[0]
)

get_stab = lambda s: float(stab_tbl.loc[stab_tbl["spec"] == s, "coef"].iloc[0])
get_stab_p = lambda s: float(stab_tbl.loc[stab_tbl["spec"] == s, "p_value"].iloc[0])

gate_tbl = pd.DataFrame(
    [
        {"spec": "fe_baseline_twfe", "coef": get_core("fe_baseline_twfe"), "p_value": get_core_p("fe_baseline_twfe")},
        {
            "spec": "fe_controls_restricted_twfe",
            "coef": get_core("fe_controls_restricted_twfe"),
            "p_value": get_core_p("fe_controls_restricted_twfe"),
        },
        {"spec": "iv_twfe_external", "coef": get_core("iv_twfe_external"), "p_value": get_core_p("iv_twfe_external")},
        {"spec": "period_1991_2005", "coef": get_stab("period_1991_2005"), "p_value": get_stab_p("period_1991_2005")},
        {"spec": "period_2006_2020", "coef": get_stab("period_2006_2020"), "p_value": get_stab_p("period_2006_2020")},
    ]
)
gate_tbl["abs_drift_pct"] = (gate_tbl["coef"] - baseline_coef).abs() / (
    abs(baseline_coef) if abs(baseline_coef) > 1e-8 else np.nan
)
gate_tbl.to_csv(OUT_AUDIT_T / "spec_gate_table_v2.csv", index=False)

# Corrected scorecard
preferred_fs_val = float(
    first_stage_tbl.loc[
        (first_stage_tbl["instrument"] == preferred_iv) & (first_stage_tbl["outcome"] == "inflation"),
        "first_stage_stat",
    ].iloc[0]
)

score_rows = []
score_rows.append(
    {
        "criterion": "preferred_first_stage_stat_ge_10",
        "value": preferred_fs_val,
        "threshold": ">=10",
        "pass": bool(preferred_fs_val >= 10),
    }
)

positive_count = int((gate_tbl["coef"] > 0).sum())
score_rows.append(
    {
        "criterion": "inflation_positive_sign_at_least_4_of_5",
        "value": positive_count,
        "threshold": ">=4",
        "pass": bool(positive_count >= 4),
    }
)

max_drift = float(gate_tbl["abs_drift_pct"].max())
score_rows.append(
    {
        "criterion": "max_inflation_drift_lt_40pct",
        "value": max_drift,
        "threshold": "<0.40",
        "pass": bool(max_drift < 0.40),
    }
)

core_gdp = core_tbl[core_tbl["outcome"] == "gdp_growth"].copy()
weak_count = int((core_gdp["p_value_m2_growth"] >= 0.05).sum())
all_gdp_specs = int(len(core_gdp))
score_rows.append(
    {
        "criterion": "gdp_effect_weak_all_core_specs",
        "value": f"{weak_count}/{all_gdp_specs}",
        "threshold": "all p>=0.05",
        "pass": bool(weak_count == all_gdp_specs),
    }
)

placebo_sig_count = int((placebo_tbl["p_value"] < 0.05).sum())
score_rows.append(
    {
        "criterion": "placebo_tests_not_significant",
        "value": placebo_sig_count,
        "threshold": "0 significant",
        "pass": bool(placebo_sig_count == 0),
    }
)

scorecard = pd.DataFrame(score_rows)
all_pass = bool(scorecard["pass"].all())
recommendation = "GO_CONTINUE" if all_pass else "GO_PIVOT_SHORT_RUN"
scorecard["recommendation_if_fail"] = np.where(scorecard["pass"], "", "GO_PIVOT_SHORT_RUN")
scorecard.to_csv(OUT_AUDIT_T / "audit_scorecard_v2.csv", index=False)

powerbi_core = core_tbl.copy()
powerbi_core["abs_coef"] = powerbi_core["coef_m2_growth"].abs()
powerbi_core["is_significant_5pct"] = powerbi_core["p_value_m2_growth"] < 0.05
powerbi_core["recommendation"] = recommendation
powerbi_core.to_csv(OUT_AUDIT_T / "powerbi_model_summary_v2.csv", index=False)

# Audit figures
fig, ax = plt.subplots(figsize=(9, 4))
sns.barplot(data=gate_tbl, x="spec", y="coef", ax=ax)
ax.axhline(0, color="black", linewidth=1)
ax.axhline(baseline_coef, color="red", linestyle="--", label="Baseline FE coef")
ax.set_title("V2 Inflation Coefficient Across Gate Specs")
ax.set_ylabel("Coefficient on m2_growth")
ax.tick_params(axis="x", rotation=25)
ax.legend()
fig.tight_layout()
fig.savefig(OUT_AUDIT_F / "stability_coefficients_gate_v2.png", dpi=170)
plt.close(fig)

fig2, ax2 = plt.subplots(figsize=(9, 4))
fs_plot = (
    first_stage_tbl[["instrument", "first_stage_stat"]]
    .drop_duplicates()
    .rename(columns={"first_stage_stat": "value"})
)
fs_plot["metric"] = "first_stage_stat"
pl_plot = placebo_tbl[["test", "stat_t2"]].rename(columns={"test": "instrument", "stat_t2": "value"})
pl_plot["metric"] = "placebo_t2"
combo = pd.concat([fs_plot[["instrument", "value", "metric"]], pl_plot[["instrument", "value", "metric"]]], ignore_index=True)
sns.barplot(data=combo, x="instrument", y="value", hue="metric", ax=ax2)
ax2.axhline(10, color="red", linestyle="--", label="10 threshold")
ax2.set_title("V2 First-Stage and Placebo Diagnostics")
ax2.tick_params(axis="x", rotation=20)
ax2.legend()
fig2.tight_layout()
fig2.savefig(OUT_AUDIT_F / "first_stage_and_placebo_strength_v2.png", dpi=170)
plt.close(fig2)

# -----------------------------
# Phase 2 LP-IV V2 (exact FE)
# -----------------------------

lp_df = df.copy()
for y in ["inflation", "gdp_growth"]:
    for h in [0, 1, 2, 3]:
        lp_df[f"{y}_h{h}"] = lp_df.groupby("Country Name")[y].shift(-h)


def run_lp_iv_exact(df_in: pd.DataFrame, outcome: str, horizon: int, instrument: str, controls: list[str]):
    ycol = f"{outcome}_h{horizon}"
    cols = ["Country Name", "year", ycol, "m2_growth", instrument] + controls
    d = df_in[cols].dropna().copy().rename(columns={"Country Name": "country"})
    formula = f"{ycol} ~ 1"
    if controls:
        formula += " + " + " + ".join(controls)
    formula += f" + C(country) + C(year) [m2_growth ~ {instrument}]"
    res = IV2SLS.from_formula(formula, data=d).fit(cov_type="clustered", clusters=d["country"])
    fs = res.first_stage.diagnostics.loc["m2_growth"]
    coef = float(res.params["m2_growth"])
    se = float(res.std_errors["m2_growth"])
    return {
        "outcome": outcome,
        "horizon": horizon,
        "instrument": instrument,
        "coef_m2_growth": coef,
        "std_error": se,
        "p_value": float(res.pvalues["m2_growth"]),
        "ci_low_95": coef - 1.96 * se,
        "ci_high_95": coef + 1.96 * se,
        "nobs": int(res.nobs),
        "first_stage_stat": float(fs["f.stat"]),
        "first_stage_p": float(fs["f.pval"]),
        "partial_rsquared": float(fs["partial.rsquared"]),
        "iv_r2": float(res.rsquared),
    }


lp_rows: list[dict] = []
for inst in ["instrument_m2_external_level", "instrument_m2_l1"]:
    for outcome in ["inflation", "gdp_growth"]:
        for h in [0, 1, 2, 3]:
            try:
                lp_rows.append(run_lp_iv_exact(lp_df, outcome=outcome, horizon=h, instrument=inst, controls=restricted_controls))
            except Exception as e:
                log(f"LP-IV exact failed: outcome={outcome}, h={h}, inst={inst}, err={e}")

lp_tbl = pd.DataFrame(lp_rows).sort_values(["instrument", "outcome", "horizon"])
lp_tbl.to_csv(OUT_LP_T / "lp_iv_all_results_v2.csv", index=False)

primary = lp_tbl[lp_tbl["instrument"] == "instrument_m2_external_level"].copy()
alt = lp_tbl[lp_tbl["instrument"] == "instrument_m2_l1"].copy()
primary.to_csv(OUT_LP_T / "lp_iv_primary_results_v2.csv", index=False)
alt.to_csv(OUT_LP_T / "lp_iv_alt_results_v2.csv", index=False)

powerbi_lp = lp_tbl.copy()
powerbi_lp["is_sig_5pct"] = powerbi_lp["p_value"] < 0.05
powerbi_lp["abs_coef"] = powerbi_lp["coef_m2_growth"].abs()
powerbi_lp.to_csv(OUT_LP_T / "powerbi_lp_iv_summary_v2.csv", index=False)

# LP plots
for outcome in ["inflation", "gdp_growth"]:
    d_out = primary[primary["outcome"] == outcome].sort_values("horizon")
    fig3, ax3 = plt.subplots(figsize=(7, 4))
    ax3.plot(d_out["horizon"], d_out["coef_m2_growth"], marker="o", label="LP-IV coefficient")
    ax3.fill_between(d_out["horizon"], d_out["ci_low_95"], d_out["ci_high_95"], alpha=0.25, label="95% CI")
    ax3.axhline(0, color="black", linewidth=1)
    ax3.set_title(f"V2 LP-IV Path: {outcome} (primary IV)")
    ax3.set_xlabel("Horizon (years)")
    ax3.set_ylabel("Effect of m2_growth shock")
    ax3.legend()
    fig3.tight_layout()
    fig3.savefig(OUT_LP_F / f"irf_primary_{outcome}_v2.png", dpi=170)
    plt.close(fig3)

fs_plot = lp_tbl.groupby(["instrument", "horizon"], as_index=False)["first_stage_stat"].mean()
fig4, ax4 = plt.subplots(figsize=(8, 4))
sns.lineplot(data=fs_plot, x="horizon", y="first_stage_stat", hue="instrument", marker="o", ax=ax4)
ax4.axhline(10, color="red", linestyle="--", label="10 threshold")
ax4.set_title("V2 First-Stage Strength by Horizon")
ax4.set_ylabel("First-stage stat")
ax4.legend()
fig4.tight_layout()
fig4.savefig(OUT_LP_F / "first_stage_by_horizon_v2.png", dpi=170)
plt.close(fig4)

# LP interpretation metrics
sig_count = lambda d: int((d["p_value"] < 0.05).sum())
primary_inf = primary[primary["outcome"] == "inflation"].sort_values("horizon")
primary_gdp = primary[primary["outcome"] == "gdp_growth"].sort_values("horizon")

interp = pd.DataFrame(
    [
        {"metric": "inflation_sig_horizons_primary", "value": sig_count(primary_inf)},
        {"metric": "gdp_sig_horizons_primary", "value": sig_count(primary_gdp)},
        {"metric": "mean_first_stage_stat_primary", "value": float(primary["first_stage_stat"].mean())},
        {"metric": "mean_first_stage_stat_alt_lag", "value": float(alt["first_stage_stat"].mean()) if len(alt) else np.nan},
    ]
)
interp.to_csv(OUT_LP_T / "phase2_interpretation_metrics_v2.csv", index=False)

primary_min_fs = float(primary["first_stage_stat"].min()) if len(primary) else np.nan
if sig_count(primary_inf) >= 1 and primary_min_fs >= 10:
    lp_rec = "EVIDENCE_SHORT_RUN_EFFECT_PRESENT"
else:
    lp_rec = "EVIDENCE_WEAK_REVISIT_IDENTIFICATION"

# Summary write-up
summary_lines = [
    "# V2 Rebuild Summary",
    "",
    "## What changed",
    "- Replaced approximate FE handling with exact FE formulas in IV estimation.",
    "- Replaced plain first-stage t^2 proxies with clustered first-stage diagnostics from linearmodels.",
    "- Enforced restricted controls in audited GDP specs (no gdp_pc_growth leakage).",
    "- Expanded stability audit to leave-one-region-out across all available regions.",
    "",
    "## Phase 1 Audit V2",
    f"- Recommendation: `{recommendation}`",
    f"- Preferred first-stage stat (external IV, inflation spec): `{preferred_fs_val:.4f}`",
    f"- Max inflation drift across gate specs: `{max_drift:.4f}`",
    f"- Placebo significant tests (p<0.05): `{placebo_sig_count}`",
    "",
    "## Phase 2 LP-IV V2",
    f"- Recommendation flag: `{lp_rec}`",
    f"- Primary IV mean first-stage stat: `{float(primary['first_stage_stat'].mean()):.4f}`",
    f"- Primary IV inflation significant horizons (5%): `{sig_count(primary_inf)}`",
    f"- Primary IV GDP significant horizons (5%): `{sig_count(primary_gdp)}`",
    "",
    "## Claim boundary",
    "- If first-stage remains below strong threshold, treat this as robust association evidence, not defended causal effect.",
]

summary_path = OUT_ROOT / "V2_SUMMARY.md"
summary_path.write_text("\n".join(summary_lines))

# logs
(OUT_ROOT / "v2_run_log.md").write_text("\n".join(["# V2 Run Log", ""] + [f"- {x}" for x in LOG_LINES]))

print("V2 rebuild completed.")
print("Audit outputs:", OUT_AUDIT)
print("LP outputs:", OUT_LP)
print("Summary:", summary_path)
