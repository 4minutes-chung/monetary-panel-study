# V2 Plan (Based on Review Findings)

## Goal
Rebuild the core analysis with defensible panel-IV inference and close the project with a clear claim boundary.

## Why V2 exists
The review found three blocking issues:
1. Phase 2 used one-pass two-way demeaning in an unbalanced panel (not exact FE absorption).
2. First-stage strength in Phase 1.1/audit used non-clustered `t^2` proxies, overstating IV strength.
3. GDP models included `gdp_pc_growth` in some specs, creating mechanical overlap risk.

## V2 scope
- Re-estimate fixed model set only (no spec fishing):
  - FE baseline (inflation, GDP growth)
  - FE + restricted controls
  - IV TWFE with lag IV
  - IV TWFE with external IV
- Recompute first-stage diagnostics directly from linearmodels IV diagnostics with clustered covariance.
- Re-run stability checks (tail, period split, leave-one-region-out all regions).
- Re-run scorecard gate.
- Rebuild Phase 2 LP-IV using exact FE formula (`C(country)+C(year)`) with clustered SE.
- Keep GDP short-run equation static at horizon `h=0` (no dynamic GDP horizon path).

## Data policy in V2
- Required inputs:
  - `macro_growth_merged.csv`
  - `data/phase1_controls.csv`
  - `data/phase1_instruments.csv`
- Frozen region mapping for reproducibility:
  - `v2/data/region_map_worldbank_2026-03-26.csv`
- Controls used in audited core specs:
  - `trade_open`, `pop_growth`, `investment_share`
  - `gdp_pc_growth` excluded from GDP outcome equations.

## Deliverables
- Script:
  - `v2/run_v2_rebuild.py`
- Outputs:
  - `v2/outputs/phase1_audit_v2/tables/*.csv`
  - `v2/outputs/phase1_audit_v2/figures/*.png`
  - `v2/outputs/phase2_short_run_v2/tables/*.csv`
  - `v2/outputs/phase2_short_run_v2/figures/*.png`
  - `v2/outputs/V2_SUMMARY.md`

## Done criteria
- `python v2/run_v2_rebuild.py` runs end-to-end.
- All IV first-stage checks use clustered diagnostics from the estimation sample.
- No forbidden GDP control in audited GDP specs.
- Scorecard recommendation updates from corrected pipeline.
- Final summary states whether claim is causal or associational only.
