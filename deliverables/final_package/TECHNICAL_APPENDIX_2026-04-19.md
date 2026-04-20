# Technical Appendix and Traceability (2026-04-19)

## 1) Scope and Objective

This appendix documents the exact source tables and row filters used to construct all headline statements in the executive memo.

Canonical workflow used for this package:

1. Run `notebooks/phase_0_objA_lucas_replication.ipynb`
2. Run `notebooks/phase_1_objB_baseline.ipynb`
3. Run `notebooks/phase_2_objB_short_run.ipynb`
4. Cross-check against `v2/` parity report

## 2) Identification Framework

Two-tier first-stage interpretation:

- Relevance gate: first-stage Wald `chi2(1) > 3.8415` and `p < 0.05`
- Strong-IV label: first-stage statistic `>= 10.0`

Interpretation rule used in memo:

- If relevance passes but strong-IV fails, treat effects as associational evidence with caution on causal strength.

## 3) Traceability Matrix

| Memo claim ID | Statement (short form) | Value | Source file | Row filter / extraction rule |
| --- | --- | ---: | --- | --- |
| C1 | Sample rows | 4292 | outputs/notebook_phase0/phase0_sample_summary.csv | `metric == rows` -> `value` |
| C2 | Countries | 163 | outputs/notebook_phase0/phase0_sample_summary.csv | `metric == countries` -> `value` |
| C3 | Year min | 1991 | outputs/notebook_phase0/phase0_sample_summary.csv | `metric == year_min` -> `value` |
| C4 | Year max | 2020 | outputs/notebook_phase0/phase0_sample_summary.csv | `metric == year_max` -> `value` |
| C5 | Pooled inflation coef | 0.6451 | outputs/notebook_phase0/phase0_pooled_results.csv | `model == pooled_inflation` -> `coef_m2_growth` |
| C6 | Pooled inflation p-value | 5.11e-07 | outputs/notebook_phase0/phase0_pooled_results.csv | `model == pooled_inflation` -> `p_value` |
| C7 | Pooled GDP coef | -0.0010 | outputs/notebook_phase0/phase0_pooled_results.csv | `model == pooled_gdp_growth` -> `coef_m2_growth` |
| C8 | Pooled GDP p-value | 0.8687 | outputs/notebook_phase0/phase0_pooled_results.csv | `model == pooled_gdp_growth` -> `p_value` |
| C9 | Long-run inflation coef | 0.8909 | outputs/notebook_phase0/phase0_longrun_results.csv | `model == longrun_inflation_country_avg` -> `coef_m2_growth` |
| C10 | Long-run inflation p-value | 2.84e-38 | outputs/notebook_phase0/phase0_longrun_results.csv | `model == longrun_inflation_country_avg` -> `p_value` |
| C11 | Long-run inflation nobs | 86 | outputs/notebook_phase0/phase0_longrun_results.csv | `model == longrun_inflation_country_avg` -> `nobs` |
| C12 | Long-run GDP coef | 0.0616 | outputs/notebook_phase0/phase0_longrun_results.csv | `model == longrun_gdp_country_avg` -> `coef_m2_growth` |
| C13 | Long-run GDP p-value | 0.0320 | outputs/notebook_phase0/phase0_longrun_results.csv | `model == longrun_gdp_country_avg` -> `p_value` |
| C14 | FE baseline inflation coef | 0.5706 | outputs/notebook_phase1/phase1_fe_results.csv | `model == fe_baseline and outcome == inflation` -> `coef` |
| C15 | FE baseline inflation p-value | 2.83e-06 | outputs/notebook_phase1/phase1_fe_results.csv | `model == fe_baseline and outcome == inflation` -> `p_value` |
| C16 | FE baseline GDP coef | -0.0080 | outputs/notebook_phase1/phase1_fe_results.csv | `model == fe_baseline and outcome == gdp_growth` -> `coef` |
| C17 | FE baseline GDP p-value | 0.3951 | outputs/notebook_phase1/phase1_fe_results.csv | `model == fe_baseline and outcome == gdp_growth` -> `p_value` |
| C18 | IV external inflation coef | 1.0327 | outputs/notebook_phase1/phase1_iv_results.csv | `outcome == inflation and instrument == instrument_m2_external_level` -> `coef` |
| C19 | IV external inflation p-value | 1.04e-04 | outputs/notebook_phase1/phase1_iv_results.csv | `outcome == inflation and instrument == instrument_m2_external_level` -> `p_value` |
| C20 | IV external GDP coef | -0.1196 | outputs/notebook_phase1/phase1_iv_results.csv | `outcome == gdp_growth and instrument == instrument_m2_external_level` -> `coef` |
| C21 | IV external GDP p-value | 0.1570 | outputs/notebook_phase1/phase1_iv_results.csv | `outcome == gdp_growth and instrument == instrument_m2_external_level` -> `p_value` |
| C22 | IV first-stage stat (external) | 4.2243 | outputs/notebook_phase1/phase1_iv_results.csv | `outcome == inflation and instrument == instrument_m2_external_level` -> `first_stage_stat` |
| C23 | IV first-stage p-value (external) | 0.0398 | outputs/notebook_phase1/phase1_iv_results.csv | `outcome == inflation and instrument == instrument_m2_external_level` -> `first_stage_p` |
| C24 | Gate relevance pass | True | outputs/notebook_phase1/phase1_gate_read.csv | `criterion == first_stage_relevance_chi2_95` -> `pass` |
| C25 | Gate p<0.05 pass | True | outputs/notebook_phase1/phase1_gate_read.csv | `criterion == first_stage_p_lt_0p05` -> `pass` |
| C26 | Gate strong-IV pass | False | outputs/notebook_phase1/phase1_gate_read.csv | `criterion == first_stage_strong_iv_ge_10` -> `pass` |
| C27 | LP inflation h0 coef | 1.0327 | outputs/notebook_phase2/phase2_lp_iv_primary_results.csv | `outcome == inflation and horizon == 0` -> `coef_m2_growth` |
| C28 | LP inflation h0 p-value | 1.04e-04 | outputs/notebook_phase2/phase2_lp_iv_primary_results.csv | `outcome == inflation and horizon == 0` -> `p_value` |
| C29 | LP inflation h1 coef | 0.6572 | outputs/notebook_phase2/phase2_lp_iv_primary_results.csv | `outcome == inflation and horizon == 1` -> `coef_m2_growth` |
| C30 | LP inflation h1 p-value | 0.0033 | outputs/notebook_phase2/phase2_lp_iv_primary_results.csv | `outcome == inflation and horizon == 1` -> `p_value` |
| C31 | LP inflation h2 coef | 0.5697 | outputs/notebook_phase2/phase2_lp_iv_primary_results.csv | `outcome == inflation and horizon == 2` -> `coef_m2_growth` |
| C32 | LP inflation h2 p-value | 0.0238 | outputs/notebook_phase2/phase2_lp_iv_primary_results.csv | `outcome == inflation and horizon == 2` -> `p_value` |
| C33 | LP inflation h3 coef | 0.5451 | outputs/notebook_phase2/phase2_lp_iv_primary_results.csv | `outcome == inflation and horizon == 3` -> `coef_m2_growth` |
| C34 | LP inflation h3 p-value | 0.0333 | outputs/notebook_phase2/phase2_lp_iv_primary_results.csv | `outcome == inflation and horizon == 3` -> `p_value` |
| C35 | LP GDP h0 coef | -0.1196 | outputs/notebook_phase2/phase2_lp_iv_primary_results.csv | `outcome == gdp_growth and horizon == 0` -> `coef_m2_growth` |
| C36 | LP GDP h0 p-value | 0.1570 | outputs/notebook_phase2/phase2_lp_iv_primary_results.csv | `outcome == gdp_growth and horizon == 0` -> `p_value` |
| C37 | Inflation significant horizons count | 4 | outputs/notebook_phase2/phase2_interpretation_metrics.csv | `metric == inflation_sig_horizons_5pct` -> `value` |
| C38 | GDP significant horizons count | 0 | outputs/notebook_phase2/phase2_interpretation_metrics.csv | `metric == gdp_sig_horizons_5pct` -> `value` |
| C39 | Min inflation first-stage stat | 4.2243 | outputs/notebook_phase2/phase2_interpretation_metrics.csv | `metric == inflation_min_first_stage_stat_primary` -> `value` |
| C40 | Inflation relevance gate all horizons | True | outputs/notebook_phase2/phase2_interpretation_metrics.csv | `metric == inflation_relevance_gate_all_horizons` -> `value` |
| C41 | Inflation strong-IV all horizons | False | outputs/notebook_phase2/phase2_interpretation_metrics.csv | `metric == inflation_strong_iv_all_horizons` -> `value` |

## 4) Cross-Pipeline Consistency

Notebook outputs were compared against canonical v2 outputs for FE/IV/LP-primary headline metrics.

- Maximum absolute difference: `0.0`
- Tolerance check (`<= 1e-9`): pass
- Reference: `docs/NOTEBOOK_V2_PARITY_2026-04-19.md`

## 5) Caveats for Interpretation

1. The relevance gate is satisfied for primary external-instrument specifications.
2. Strong-IV threshold is not satisfied in key primary rows.
3. Accordingly, policy language should avoid definitive causal claims and keep emphasis on robust association patterns.
