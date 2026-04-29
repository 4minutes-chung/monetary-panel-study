from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid", context="talk")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = PROJECT_ROOT / "04_current_results/figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

TABLES_AUDIT = PROJECT_ROOT / "04_current_results/tables/phase1_audit"
TABLES_LP = PROJECT_ROOT / "04_current_results/tables/short_run_lp"
CHI2_1_95_CRITICAL = 3.841458820694124
NON_CAUSAL_MODE = False
CURRENT_CLAIM_TIER = "exploratory"
CURRENT_INTERPRETATION_READY = False


def save(fig: plt.Figure, name: str) -> None:
    if NON_CAUSAL_MODE:
        fig.text(
            0.5,
            0.01,
            "ASSOCIATIONAL EVIDENCE ONLY (IDENTIFICATION NOT PASSED)",
            ha="center",
            va="bottom",
            color="#e63946",
            fontsize=10,
            fontweight="bold",
        )
        fig.tight_layout(rect=(0, 0.05, 1, 1))
    else:
        fig.tight_layout()
    fig.savefig(OUT_DIR / name, dpi=180)
    plt.close(fig)


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    return pd.read_csv(path)


def _as_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    return str(value).strip().lower() in {"1", "true", "yes", "y", "t"}


def load_non_causal_mode() -> bool:
    status_path = TABLES_AUDIT / "interpretation_status.csv"
    if not status_path.exists():
        return False
    status = pd.read_csv(status_path)
    if status.empty or "interpretation_ready" not in status.columns:
        return False
    interpretation_ready = _as_bool(status.loc[0, "interpretation_ready"])
    return not interpretation_ready


def load_interpretation_status() -> tuple[bool, str]:
    status_path = TABLES_AUDIT / "interpretation_status.csv"
    if not status_path.exists():
        return False, "exploratory"
    status = pd.read_csv(status_path)
    if status.empty:
        return False, "exploratory"

    interpretation_ready = _as_bool(status.loc[0, "interpretation_ready"]) if "interpretation_ready" in status.columns else False
    claim_tier = str(status.loc[0, "claim_tier"]) if "claim_tier" in status.columns else "exploratory"
    if claim_tier not in {"exploratory", "associational", "causal"}:
        claim_tier = "exploratory"
    return interpretation_ready, claim_tier


def chart_core_coefficients(core: pd.DataFrame) -> None:
    d = core[core["model"].isin(["fe_baseline_twfe", "fe_controls_restricted_twfe", "iv_twfe_external", "iv_twfe_lag"])].copy()
    d["model"] = d["model"].str.replace("_", " ")

    fig, ax = plt.subplots(figsize=(11, 6))
    sns.barplot(data=d, x="model", y="coef_m2_growth", hue="outcome", ax=ax, palette=["#1f77b4", "#ff7f0e"])
    ax.axhline(0, color="black", linewidth=1)
    ax.set_title("Core Coefficients Across Specifications")
    ax.set_xlabel("")
    ax.set_ylabel("Coefficient on m2_growth")
    ax.tick_params(axis="x", rotation=25)
    save(fig, "01_core_coefficients.png")


def chart_first_stage(first_stage: pd.DataFrame) -> None:
    d = first_stage.copy()
    d["label"] = d["instrument"] + " | " + d["outcome"]

    fig, ax = plt.subplots(figsize=(11, 6))
    sns.barplot(data=d, x="label", y="first_stage_stat", ax=ax, color="#2a9d8f")
    ax.axhline(CHI2_1_95_CRITICAL, color="#e63946", linestyle="--", linewidth=2, label="chi2(1) 95% critical")
    ax.set_title("First-Stage Strength (Clustered Wald chi2)")
    ax.set_xlabel("")
    ax.set_ylabel("First-stage stat")
    ax.tick_params(axis="x", rotation=25)
    ax.legend()
    save(fig, "02_first_stage_strength.png")


def chart_gate_drift(gate: pd.DataFrame) -> None:
    d = gate.copy().sort_values("abs_drift_pct", ascending=False)

    fig, ax = plt.subplots(figsize=(11, 6))
    sns.barplot(data=d, x="spec", y="abs_drift_pct", ax=ax, color="#457b9d")
    ax.axhline(0.40, color="#e63946", linestyle="--", linewidth=2, label="40% drift threshold")
    ax.set_title("Inflation Coefficient Drift by Gate Spec")
    ax.set_xlabel("")
    ax.set_ylabel("Absolute drift vs baseline")
    ax.tick_params(axis="x", rotation=25)
    ax.legend()
    save(fig, "03_gate_drift.png")


def chart_stability(stability: pd.DataFrame) -> None:
    d = stability.copy().sort_values("coef")

    fig, ax = plt.subplots(figsize=(11, 7))
    sns.barplot(data=d, y="spec", x="coef", ax=ax, color="#3a86ff")
    baseline = float(d["baseline_coef"].iloc[0])
    ax.axvline(baseline, color="#e63946", linestyle="--", linewidth=2, label="Baseline FE")
    ax.axvline(0, color="black", linewidth=1)
    ax.set_title("Stability Checks: Inflation Coefficient")
    ax.set_xlabel("Coefficient on m2_growth")
    ax.set_ylabel("")
    ax.legend()
    save(fig, "04_stability_coefficients.png")


def chart_placebo(placebo: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=placebo, x="test", y="stat_t2", ax=ax, color="#457b9d")
    ax.axhline(CHI2_1_95_CRITICAL, color="#e63946", linestyle="--", linewidth=2, label="chi2(1) 95% reference")
    ax.set_title("Placebo Diagnostics (lead t^2; permutation standardized score^2)")
    ax.set_xlabel("")
    ax.set_ylabel("Squared diagnostic statistic")
    ax.legend()
    save(fig, "05_placebo_strength.png")


def chart_lp_inflation(primary: pd.DataFrame, alt: pd.DataFrame) -> None:
    p = primary[primary["outcome"] == "inflation"].sort_values("horizon")
    a = alt[alt["outcome"] == "inflation"].sort_values("horizon")

    fig, ax = plt.subplots(figsize=(10, 6))
    if not p.empty:
        ax.plot(p["horizon"], p["coef_m2_growth"], marker="o", linewidth=2.5, label="Primary IV")
        ax.fill_between(p["horizon"], p["ci_low_95"], p["ci_high_95"], alpha=0.2)
    if not a.empty:
        ax.plot(a["horizon"], a["coef_m2_growth"], marker="s", linewidth=2.2, label="Lag IV (sensitivity)")
    ax.axhline(0, color="black", linewidth=1)
    ax.set_title("LP-IV Inflation Response by Horizon")
    ax.set_xlabel("Horizon (years)")
    ax.set_ylabel("Coefficient on m2_growth")
    ax.legend()
    save(fig, "06_lp_inflation_paths.png")


def chart_lp_gdp(primary: pd.DataFrame, alt: pd.DataFrame) -> None:
    p = primary[primary["outcome"] == "gdp_growth"].copy()
    a = alt[alt["outcome"] == "gdp_growth"].copy()
    d = pd.concat([p.assign(series="Primary IV"), a.assign(series="Lag IV")], ignore_index=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=d, x="series", y="coef_m2_growth", ax=ax, color="#1d3557")
    ax.axhline(0, color="black", linewidth=1)
    ax.set_title("GDP (h=0) LP-IV Coefficient Comparison")
    ax.set_xlabel("")
    ax.set_ylabel("Coefficient on m2_growth")
    save(fig, "07_lp_gdp_h0_compare.png")


def chart_lp_first_stage(all_lp: pd.DataFrame) -> None:
    d = all_lp.groupby(["instrument", "outcome", "horizon"], as_index=False)["first_stage_stat"].mean()
    d["series"] = d["instrument"] + " | " + d["outcome"]

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=d, x="horizon", y="first_stage_stat", hue="series", marker="o", linewidth=2.5, ax=ax)
    ax.axhline(CHI2_1_95_CRITICAL, color="#e63946", linestyle="--", linewidth=2, label="chi2(1) 95% critical")
    ax.set_title("First-Stage Strength by Horizon (Instrument x Outcome)")
    ax.set_xlabel("Horizon")
    ax.set_ylabel("First-stage stat")
    ax.legend()
    save(fig, "08_lp_first_stage_horizon.png")


def chart_missingness(missing: pd.DataFrame) -> None:
    d = missing.copy().sort_values("missing_share", ascending=False)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=d, y="variable", x="missing_share", ax=ax, color="#f4a261")
    ax.set_title("Data Missingness by Variable")
    ax.set_xlabel("Missing share")
    ax.set_ylabel("")
    save(fig, "09_missingness.png")


def chart_scatter(panel: pd.DataFrame, x: str, y: str, title: str, out_name: str) -> None:
    d = panel[[x, y]].dropna().copy()
    if len(d) > 5000:
        d = d.sample(5000, random_state=42)

    fig, ax = plt.subplots(figsize=(9, 6))
    sns.regplot(data=d, x=x, y=y, scatter_kws={"alpha": 0.2, "s": 20}, line_kws={"color": "#e63946", "linewidth": 2}, ax=ax)
    ax.set_title(title)
    save(fig, out_name)


def chart_country_rankings(panel: pd.DataFrame) -> None:
    country = (
        panel.groupby("Country Name", as_index=False)
        .agg(mean_inflation=("inflation", "mean"), mean_m2=("m2_growth", "mean"), n=("year", "count"))
        .query("n >= 10")
    )

    top = country.nlargest(20, "mean_inflation").sort_values("mean_inflation")
    fig1, ax1 = plt.subplots(figsize=(10, 8))
    sns.barplot(data=top, y="Country Name", x="mean_inflation", ax=ax1, color="#f4a261")
    ax1.set_title("Top 20 Countries by Mean Inflation (Panel Window)")
    ax1.set_xlabel("Mean inflation")
    ax1.set_ylabel("")
    save(fig1, "12_top20_mean_inflation.png")

    fig2, ax2 = plt.subplots(figsize=(9, 6))
    sns.regplot(
        data=country,
        x="mean_m2",
        y="mean_inflation",
        scatter_kws={"alpha": 0.6, "s": 35},
        line_kws={"color": "#e63946", "linewidth": 2},
        ax=ax2,
    )
    ax2.set_title("Country Means: Money Growth vs Inflation")
    ax2.set_xlabel("Mean m2_growth")
    ax2.set_ylabel("Mean inflation")
    save(fig2, "13_country_means_m2_vs_inflation.png")


def write_manifest() -> None:
    status_header = f"claim_tier={CURRENT_CLAIM_TIER}; interpretation_ready={CURRENT_INTERPRETATION_READY}"
    rows = [
        {
            "file": p.name,
            "claim_tier": CURRENT_CLAIM_TIER,
            "interpretation_ready": CURRENT_INTERPRETATION_READY,
            "status_header": status_header,
        }
        for p in sorted(OUT_DIR.glob("*.png"))
    ]
    pd.DataFrame(rows).to_csv(OUT_DIR / "portfolio_graph_manifest.csv", index=False)


def main() -> None:
    global NON_CAUSAL_MODE, CURRENT_CLAIM_TIER, CURRENT_INTERPRETATION_READY
    CURRENT_INTERPRETATION_READY, CURRENT_CLAIM_TIER = load_interpretation_status()
    NON_CAUSAL_MODE = not CURRENT_INTERPRETATION_READY

    core = read_csv(TABLES_AUDIT / "core_model_results.csv")
    first_stage = read_csv(TABLES_AUDIT / "first_stage_strength.csv")
    gate = read_csv(TABLES_AUDIT / "spec_gate_table.csv")
    stability = read_csv(TABLES_AUDIT / "spec_stability_table.csv")
    placebo = read_csv(TABLES_AUDIT / "placebo_tests.csv")
    missing = read_csv(TABLES_AUDIT / "data_audit_missingness.csv")

    all_lp = read_csv(TABLES_LP / "lp_iv_all_results.csv")
    primary_lp = read_csv(TABLES_LP / "lp_iv_primary_results.csv")
    alt_lp = read_csv(TABLES_LP / "lp_iv_alt_results.csv")

    panel = read_csv(PROJECT_ROOT / "02_data/analysis_ready/macro_growth_merged.csv")

    chart_core_coefficients(core)
    chart_first_stage(first_stage)
    chart_gate_drift(gate)
    chart_stability(stability)
    chart_placebo(placebo)
    chart_lp_inflation(primary_lp, alt_lp)
    chart_lp_gdp(primary_lp, alt_lp)
    chart_lp_first_stage(all_lp)
    chart_missingness(missing)
    chart_scatter(panel, "m2_growth", "inflation", "Scatter: Money Growth vs Inflation", "10_scatter_m2_vs_inflation.png")
    chart_scatter(panel, "m2_growth", "gdp_growth", "Scatter: Money Growth vs GDP Growth", "11_scatter_m2_vs_gdp_growth.png")
    chart_country_rankings(panel)

    write_manifest()
    print(f"Portfolio graphs written to: {OUT_DIR}")


if __name__ == "__main__":
    main()
