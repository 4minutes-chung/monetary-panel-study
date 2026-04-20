# Notebook vs V2 Parity Check (2026-04-19)

## Scope

Validated notebook-phase exports against canonical v2 outputs for headline coefficients and first-stage statistics.

Compared files:

- `outputs/notebook_phase1/phase1_fe_results.csv`
- `outputs/notebook_phase1/phase1_iv_results.csv`
- `outputs/notebook_phase2/phase2_lp_iv_primary_results.csv`
- `v2/outputs/phase1_audit_v2/tables/core_model_results_v2.csv`
- `v2/outputs/phase2_short_run_v2/tables/lp_iv_primary_results_v2.csv`

## Result

- Maximum absolute difference across all checked metrics: `0.0`
- Equality within tolerance `1e-9`: `True`

## Checked metrics

- FE baseline inflation coefficient
- FE baseline GDP growth coefficient
- IV external inflation coefficient
- IV external GDP growth coefficient
- LP primary inflation coefficient at horizons 0, 1, 2, 3
- LP primary inflation first-stage statistic at horizons 0, 1, 2, 3
- LP primary GDP growth coefficient at horizon 0
- LP primary GDP growth first-stage statistic at horizon 0

## Interpretation

Notebook-first workflow and v2 script parity path are numerically aligned on the current data and gate framework.
