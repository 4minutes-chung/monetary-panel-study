# Report Draft (In Progress)

Status: patched review scaffold for final narrative write-up.

## 1. Core Question

Across countries, how strongly is money growth associated with inflation and GDP growth, and what can we responsibly claim?

## 2. Main Takeaways

- Inflation association is positive and robust in core panel specifications.
- GDP growth association is weaker and less stable.
- Identification diagnostics do not support strong causal language: the conservative relevance gate fails, the strong-IV threshold fails, drift exceeds the gate threshold, and one placebo check is significant.
- Current contract recommendation is `GO_PIVOT_SHORT_RUN`.

## 3. Table Backbone

1. `04_current_results/summary.md`
2. `04_current_results/tables/phase1_audit/audit_scorecard.csv`
3. `04_current_results/tables/phase1_audit/core_model_results.csv`
4. `04_current_results/tables/phase1_audit/inference_sensitivity.csv`
5. `04_current_results/tables/phase1_audit/placebo_tests.csv`
6. `04_current_results/tables/short_run_lp/lp_iv_primary_results.csv`

## 4. Graph Storyboard

1. `04_current_results/figures/01_core_coefficients.png`
2. `04_current_results/figures/02_first_stage_strength.png`
3. `04_current_results/figures/03_gate_drift.png`
4. `04_current_results/figures/05_placebo_strength.png`
5. `04_current_results/figures/06_lp_inflation_paths.png`
6. `04_current_results/figures/07_lp_gdp_h0_compare.png`

## 5. Claim Guardrails

- Use `01_research_question/research_target.md` as contract authority for gate definitions and claim boundary.
- Treat evidence as associational because the current conservative first-stage gate does not pass.
- Keep placebo and sensitivity checks visible in any final narrative.
- Do not cite notebook-local exports in the final package unless those exports are regenerated and checked; the tracked, canonical evidence currently lives under `04_current_results/`.

## 6. Fixes Applied In This Review

- Replaced stale pass-gate language in the final memo and appendix with the conservative failed-gate read.
- Redirected final-package source references from missing notebook exports to existing canonical `04_current_results/` tables.
- Reordered the report scaffold to put tables before graphs.

## 7. Open Writing TODO

- Convert draft bullets into full narrative sections.
- Add direct references to current `04_current_results/` exports for each headline claim.
- Align wording with executive memo and technical appendix language.
