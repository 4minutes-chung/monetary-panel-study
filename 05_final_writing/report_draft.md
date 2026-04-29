# Final Report (Concise)

## 1. Research question
Across countries, how strongly is money growth associated with inflation and GDP growth, and what can be responsibly claimed under conservative identification checks?

Contract authority for claim boundary and identification gates:
- `01_research_question/research_target.md`
- `01_research_question/claim_boundary.md`

## 2. Executive summary (what you can say)
- **Inflation**: money growth is **positively and robustly associated** with inflation in the core panel specifications.
- **GDP growth**: the relationship is **weak and not robust** in the same core specifications.
- **Causality boundary**: the conservative identification gate fails and multiple diagnostics fail, so interpretation is **associational**, with IV/LP-IV treated as **directionally informative but weak-identification-sensitive**.

Canonical “current results” entrypoint: `04_current_results/summary.md`.

## 3. Data (panel window and units)
Panel window and sample integrity checks are recorded in:
- `04_current_results/tables/phase1_audit/data_audit_summary.csv`
- `04_current_results/tables/phase1_audit/data_audit_missingness.csv`
- `04_current_results/tables/phase1_audit/leakage_flags.csv`

Key facts (units are decimal rates, `0.01 = 1` percentage point):
- Rows: **4,292**
- Countries: **163**
- Years: **1991–2020**

Source of record: `05_final_writing/technical_appendix.md` (Claim-to-table map).

## 4. Methods (what was estimated)
This project is organized into two evidence layers:

### Phase 1: Panel FE and IV baselines
Core estimates are stored in:
- `04_current_results/tables/phase1_audit/core_model_results.csv`

Identification diagnostics and gates are stored in:
- `04_current_results/tables/phase1_audit/inference_sensitivity.csv`
- `04_current_results/tables/phase1_audit/audit_scorecard.csv`
- `04_current_results/tables/phase1_audit/spec_gate_table.csv`
- `04_current_results/tables/phase1_audit/placebo_tests.csv`
- `04_current_results/tables/phase1_audit/spec_stability_table.csv`

### Phase 2: Short-run LP-IV (horizons)
LP-IV outputs are stored in:
- `04_current_results/tables/short_run_lp/lp_iv_primary_results.csv`
- `04_current_results/tables/short_run_lp/interpretation_metrics.csv`

## 5. Results (tables first)

### 5.1 Phase 1: FE baselines (associational backbone)
From `04_current_results/tables/phase1_audit/core_model_results.csv`:
- FE baseline inflation coefficient on money growth: **0.5706** (p = **2.83e-06**)
- FE baseline GDP growth coefficient on money growth: **-0.0080** (p = **0.3951**)

Interpretation: the inflation relationship is statistically clear; GDP growth is not.

### 5.2 Phase 1: IV (external instrument) — informative but not gate-passing
From `04_current_results/tables/phase1_audit/core_model_results.csv`:
- IV external inflation coefficient: **1.0327** (p = **1.04e-04**)
- IV external GDP growth coefficient: **-0.1196** (p = **0.1570**)

First-stage diagnostics (preferred spec) are recorded in:
- `04_current_results/tables/phase1_audit/inference_sensitivity.csv`

Conservative gate logic (min stat / max p across clustering choices) is the authority standard.
Current conservative read:
- Country-clustered stat: **4.2243** (p = **0.0398**)
- Country+year clustered stat: **3.8016** (p = **0.0512**)
- **Conservative relevance gate: FAIL**
- **Strong-IV threshold (>=10): FAIL**

Implication: IV magnitudes are directionally consistent with the inflation association, but inference is weak-identification-sensitive and should not be used for strong causal policy elasticities.

### 5.3 Phase 2: LP-IV short-run inflation dynamics (h = 0..3)
From `04_current_results/tables/short_run_lp/lp_iv_primary_results.csv`:
- Inflation: h0 **1.0327**, h1 **0.6572**, h2 **0.5697**, h3 **0.5451**
- GDP growth (static h0): **-0.1196**

Interpretation metric summary is recorded in:
- `04_current_results/tables/short_run_lp/interpretation_metrics.csv`

Key caution: horizon-by-horizon p-values are unadjusted for multiple testing; later horizons (h2–h3) should be treated as suggestive.

## 6. Identification and diagnostics (what limits claims)
The project’s conservative “do not overclaim” boundary is not optional; it follows from the scorecard recorded in:
- `04_current_results/tables/phase1_audit/audit_scorecard.csv`
- `04_current_results/tables/phase1_audit/placebo_tests.csv`

Current diagnostic issues to keep visible in any presentation:
- Conservative relevance gate fails.
- Strong-IV label fails.
- Stability drift exceeds the contract threshold.
- One placebo test is significant.

Contract recommendation: `GO_PIVOT_SHORT_RUN` (see `04_current_results/summary.md`).

## 7. Figures (graph support, not primary evidence)
All figures are rebuildable and stored in `04_current_results/figures/`:
- `01_core_coefficients.png`
- `02_first_stage_strength.png`
- `03_gate_drift.png`
- `05_placebo_strength.png`
- `06_lp_inflation_paths.png`
- `07_lp_gdp_h0_compare.png`

Figure inventory: `04_current_results/figures/graph_inventory.md`.

## 8. Reproducibility (how to regenerate outputs)
Canonical rebuild path:
- `python3 90_reproduction_scripts/run_rebuild.py`
- `python3 90_reproduction_scripts/build_graphs.py`

Run status snapshot is recorded in:
- `04_current_results/run_log.md`

## 9. What is “done”
This package is done when:
- All headline numbers in `05_final_writing/` map to existing `04_current_results/` files (see `05_final_writing/technical_appendix.md`).
- Wording follows `01_research_question/claim_boundary.md` (association-first; no strong causal language).
- The rebuild scripts reproduce the same outputs without manual intervention.
