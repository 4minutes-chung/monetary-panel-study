# Report Draft (In Progress)

Status: working draft scaffold for final narrative write-up.

## 1. Core Question

Across countries, how strongly is money growth associated with inflation and GDP growth, and what can we responsibly claim?

## 2. Main Takeaways (Draft)

- Inflation association is positive and robust in core panel specifications.
- GDP growth association is weaker and less stable.
- Identification diagnostics improve confidence in direction but still support conservative language.

## 3. Figure-First Storyboard

1. `v2/outputs/portfolio_graphs/01_core_coefficients.png`
2. `v2/outputs/portfolio_graphs/02_first_stage_strength.png`
3. `v2/outputs/portfolio_graphs/03_gate_drift.png`
4. `v2/outputs/portfolio_graphs/06_lp_inflation_paths.png`
5. `v2/outputs/portfolio_graphs/07_lp_gdp_h0_compare.png`
6. `v2/outputs/portfolio_graphs/08_lp_first_stage_horizon.png`

## 4. Table Backbone

- `v2/outputs/phase1_audit_v2/tables/core_model_results_v2.csv`
- `v2/outputs/phase1_audit_v2/tables/first_stage_strength_v2.csv`
- `v2/outputs/phase1_audit_v2/tables/inference_sensitivity_v2.csv`
- `v2/outputs/phase1_audit_v2/tables/placebo_tests_v2.csv`
- `v2/outputs/phase1_audit_v2/tables/audit_scorecard_v2.csv`
- `v2/outputs/phase2_short_run_v2/tables/lp_iv_primary_results_v2.csv`

## 5. Claim Guardrails

- Use RESEARCH_TARGET.md as contract authority for gate definitions and claim boundary.
- Treat evidence as associational unless conservative first-stage gate conditions are clearly passed.
- Keep placebo and sensitivity checks visible in any final narrative.

## 6. Open Writing TODO

- Convert draft bullets into full narrative sections.
- Add direct references to notebook exports for each headline claim.
- Align wording with executive memo and technical appendix language.
