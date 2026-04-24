# Money Growth, Inflation, and GDP Growth

## Coffee Chat Version (60 seconds)

If we were chatting quickly:

- Inflation and money growth move together strongly in this panel.
- GDP growth links are weaker and not robust.
- Causal language is limited by first-stage strength, so interpretation stays careful.

## Contract First

Before reading anything else, use `RESEARCH_TARGET.md` as the source of truth.

- It defines the canonical run path.
- It defines the gate rules.
- It defines what we are and are not claiming.
- For full process memory (learning, assumptions, file map, and `.gitignore` policy), read `READING_GUIDE.md`.

## Reading Flow (Graph first, then table)

1. Context + assumptions: open `READING_GUIDE.md`.
2. Graphs: open `v2/outputs/portfolio_graphs/`.
3. Audit tables: open `v2/outputs/phase1_audit_v2/tables/`.
4. Short-run tables: open `v2/outputs/phase2_short_run_v2/tables/`.
5. Summary checkpoint: open `v2/outputs/V2_SUMMARY.md`.
6. Narrative draft in progress: open `deliverables/final_package/REPORT_DRAFT_IN_PROGRESS.md`.

## Fast Run Commands

```bash
python3 -m pip install -r requirements.txt

# Notebook-first canonical flow
# 1) notebooks/phase_0_objA_lucas_replication.ipynb (Run All)
# 2) notebooks/phase_1_objB_baseline.ipynb (Run All)
# 3) notebooks/phase_2_objB_short_run.ipynb (Run All)

# Optional script parity refresh
python3 v2/run_v2_rebuild.py
python3 v2/build_portfolio_graphs.py
```

## Legacy Note

- `outputs/phase1*` and `outputs/phase2_short_run*` are historical references.
- Current decision docs and claims should come from notebook exports plus `v2/outputs/` outputs under the contract.

## Visual Index

![Core coefficients](v2/outputs/portfolio_graphs/01_core_coefficients.png)
![First-stage strength](v2/outputs/portfolio_graphs/02_first_stage_strength.png)
![Gate drift](v2/outputs/portfolio_graphs/03_gate_drift.png)
![Stability checks](v2/outputs/portfolio_graphs/04_stability_coefficients.png)
![Placebo diagnostics](v2/outputs/portfolio_graphs/05_placebo_strength.png)
![Inflation LP paths](v2/outputs/portfolio_graphs/06_lp_inflation_paths.png)
![GDP h0 comparison](v2/outputs/portfolio_graphs/07_lp_gdp_h0_compare.png)
![LP first stage by horizon](v2/outputs/portfolio_graphs/08_lp_first_stage_horizon.png)
![Missingness](v2/outputs/portfolio_graphs/09_missingness.png)
![Scatter m2 vs inflation](v2/outputs/portfolio_graphs/10_scatter_m2_vs_inflation.png)
![Scatter m2 vs gdp](v2/outputs/portfolio_graphs/11_scatter_m2_vs_gdp_growth.png)
![Top inflation countries](v2/outputs/portfolio_graphs/12_top20_mean_inflation.png)
![Country means m2 vs inflation](v2/outputs/portfolio_graphs/13_country_means_m2_vs_inflation.png)
