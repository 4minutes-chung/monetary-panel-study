# Technical Appendix (Simple, Traceable Version, 2026-04-19)

**Narrative authority:** Prefer `01_research_question/research_target.md` for objective labels (Lucas → AVERAGE → YoY → IT regime). Older labels **Phase 1 / Phase 2** appear in scripts as pipeline stage names (“Phase 1 audit”, “Phase 2 LP‑IV”), not objective letters.

## What this file is for

This is the "show me exactly where the number came from" file.
Every active claim below maps to tracked canonical `04_current_results/` files.

## Repro path used

1. Run `python3 90_reproduction_scripts/run_rebuild.py`.
2. Run `python3 90_reproduction_scripts/build_graphs.py`.
3. Use `01_research_question/research_target.md` as the authority for gate definitions.

Units:

- Growth and inflation are decimal rates (`0.01 = 1` percentage point).

## How we interpret identification

Canonical gate rules:

- Conservative first-stage stat = minimum of the country-clustered and country+year-clustered first-stage stats.
- Conservative first-stage p-value = maximum of the country-clustered and country+year-clustered first-stage p-values.
- Relevance passes only if conservative stat `> 3.8415` and conservative p-value `< 0.05`.
- Strong-IV label requires conservative first-stage stat `>= 10.0`.

Current gate read:

- Country-clustered first-stage: stat `4.2243`, p-value `0.0398`.
- Country+year-clustered first-stage: stat `3.8016`, p-value `0.0512`.
- Conservative relevance gate: fail.
- Strong-IV gate: fail.
- Current recommendation: `GO_PIVOT_SHORT_RUN`.

## Claim-to-table map

| Claim ID | Statement (short form) | Value | Source file | Row filter / extraction rule |
| --- | --- | ---: | --- | --- |
| C1 | Sample rows | 4292 | 04_current_results/tables/phase1_audit/data_audit_summary.csv | `check == rows` -> `value` |
| C2 | Countries | 163 | 04_current_results/tables/phase1_audit/data_audit_summary.csv | `check == countries` -> `value` |
| C3 | Year min | 1991 | 04_current_results/tables/phase1_audit/data_audit_summary.csv | `check == year_min` -> `value` |
| C4 | Year max | 2020 | 04_current_results/tables/phase1_audit/data_audit_summary.csv | `check == year_max` -> `value` |
| C5 | Duplicate country-year rows | 0 | 04_current_results/tables/phase1_audit/data_audit_summary.csv | `check == duplicate_country_year_rows` -> `value` |
| C6 | FE baseline inflation coef | 0.5706 | 04_current_results/tables/phase1_audit/core_model_results.csv | `model == fe_baseline_twfe and outcome == inflation` -> `coef_m2_growth` |
| C7 | FE baseline inflation p-value | 2.83e-06 | 04_current_results/tables/phase1_audit/core_model_results.csv | `model == fe_baseline_twfe and outcome == inflation` -> `p_value_m2_growth` |
| C8 | FE baseline GDP coef | -0.0080 | 04_current_results/tables/phase1_audit/core_model_results.csv | `model == fe_baseline_twfe and outcome == gdp_growth` -> `coef_m2_growth` |
| C9 | FE baseline GDP p-value | 0.3951 | 04_current_results/tables/phase1_audit/core_model_results.csv | `model == fe_baseline_twfe and outcome == gdp_growth` -> `p_value_m2_growth` |
| C10 | IV external inflation coef | 1.0327 | 04_current_results/tables/phase1_audit/core_model_results.csv | `model == iv_twfe_external and outcome == inflation` -> `coef_m2_growth` |
| C11 | IV external inflation p-value | 1.04e-04 | 04_current_results/tables/phase1_audit/core_model_results.csv | `model == iv_twfe_external and outcome == inflation` -> `p_value_m2_growth` |
| C12 | IV external GDP coef | -0.1196 | 04_current_results/tables/phase1_audit/core_model_results.csv | `model == iv_twfe_external and outcome == gdp_growth` -> `coef_m2_growth` |
| C13 | IV external GDP p-value | 0.1570 | 04_current_results/tables/phase1_audit/core_model_results.csv | `model == iv_twfe_external and outcome == gdp_growth` -> `p_value_m2_growth` |
| C14 | Country-clustered first-stage stat | 4.2243 | 04_current_results/tables/phase1_audit/inference_sensitivity.csv | `clustering == country` -> `first_stage_stat` |
| C15 | Country+year first-stage stat | 3.8016 | 04_current_results/tables/phase1_audit/inference_sensitivity.csv | `clustering == country_year` -> `first_stage_stat` |
| C16 | Conservative first-stage stat gate | fail | 04_current_results/tables/phase1_audit/audit_scorecard.csv | `criterion == preferred_first_stage_stat_gt_chi2_95_conservative` -> `pass` |
| C17 | Conservative p-value gate | fail | 04_current_results/tables/phase1_audit/audit_scorecard.csv | `criterion == preferred_first_stage_p_lt_0p05_conservative` -> `pass` |
| C18 | Strong-IV gate | fail | 04_current_results/tables/phase1_audit/audit_scorecard.csv | `criterion == preferred_first_stage_stat_ge_10_for_strong_iv_conservative` -> `pass` |
| C19 | Stability drift gate | fail | 04_current_results/tables/phase1_audit/audit_scorecard.csv | `criterion == max_inflation_drift_lt_40pct` -> `pass` |
| C20 | Placebo gate | fail | 04_current_results/tables/phase1_audit/audit_scorecard.csv | `criterion == placebo_tests_not_significant` -> `pass` |
| C21 | Lead placebo p-value | 0.0394 | 04_current_results/tables/phase1_audit/placebo_tests.csv | `test == lead_placebo` -> `p_value` |
| C22 | Permutation placebo p-value | 0.1385 | 04_current_results/tables/phase1_audit/placebo_tests.csv | `test == permutation_placebo` -> `p_value` |
| C23 | LP inflation h0 coef | 1.0327 | 04_current_results/tables/short_run_lp/lp_iv_primary_results.csv | `outcome == inflation and horizon == 0` -> `coef_m2_growth` |
| C24 | LP inflation h1 coef | 0.6572 | 04_current_results/tables/short_run_lp/lp_iv_primary_results.csv | `outcome == inflation and horizon == 1` -> `coef_m2_growth` |
| C25 | LP inflation h2 coef | 0.5697 | 04_current_results/tables/short_run_lp/lp_iv_primary_results.csv | `outcome == inflation and horizon == 2` -> `coef_m2_growth` |
| C26 | LP inflation h3 coef | 0.5451 | 04_current_results/tables/short_run_lp/lp_iv_primary_results.csv | `outcome == inflation and horizon == 3` -> `coef_m2_growth` |
| C27 | LP GDP h0 coef | -0.1196 | 04_current_results/tables/short_run_lp/lp_iv_primary_results.csv | `outcome == gdp_growth and horizon == 0` -> `coef_m2_growth` |
| C28 | Primary inflation significant horizons | 4 | 04_current_results/tables/short_run_lp/interpretation_metrics.csv | `metric == inflation_sig_horizons_primary` -> `value` |
| C29 | Primary GDP significant horizons | 0 | 04_current_results/tables/short_run_lp/interpretation_metrics.csv | `metric == gdp_sig_horizons_primary` -> `value` |
| C30 | Minimum primary first-stage stat | 4.2243 | 04_current_results/tables/short_run_lp/interpretation_metrics.csv | `metric == min_first_stage_stat_primary` -> `value` |

## Cross-pipeline consistency

Notebook outputs were previously compared against the current script outputs for FE/IV/LP-primary headline metrics.

- Maximum absolute difference: `0.0`
- Tolerance check (`<= 1e-9`): pass
- Current final-package citations should use tracked `04_current_results/` files unless notebook exports are regenerated.

## Caveats you should keep in mind

1. The canonical conservative relevance gate does not pass.
2. The strong-IV threshold is not satisfied.
3. Stability drift exceeds the contract threshold and one placebo check is significant.
4. Policy language should avoid definitive causal claims and emphasize robust association patterns.
5. Horizon-by-horizon LP-IV p-values are unadjusted for multiple testing, so later-horizon significance should be interpreted cautiously.
