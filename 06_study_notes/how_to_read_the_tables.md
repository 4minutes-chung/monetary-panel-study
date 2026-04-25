# How To Read The Tables

## Start With These

1. `04_current_results/tables/phase1_audit/audit_scorecard.csv`
2. `04_current_results/tables/phase1_audit/core_model_results.csv`
3. `04_current_results/tables/phase1_audit/inference_sensitivity.csv`
4. `04_current_results/tables/phase1_audit/placebo_tests.csv`
5. `04_current_results/tables/short_run_lp/lp_iv_primary_results.csv`

## Table Guide

- `audit_scorecard.csv`: final gate pass/fail view. This is the most important table for claim discipline.
- `core_model_results.csv`: FE and IV headline coefficients for inflation and GDP growth.
- `inference_sensitivity.csv`: one-way vs two-way clustered first-stage diagnostics.
- `placebo_tests.csv`: checks whether the instrument behavior looks suspicious.
- `lp_iv_primary_results.csv`: short-run inflation and GDP response estimates.

## Reading Rule

Read coefficient tables together with the diagnostic tables. A large or significant IV coefficient does not automatically justify causal language if the first-stage and placebo gates are weak.
