# Final Report Draft

## 1. Introduction (Lucas)

This report studies how money growth relates to inflation and GDP growth across 163 countries from 1991 to 2020.

The starting reference is Lucas (1980): in long-run cross-country data, money growth and inflation are expected to move close to one-for-one; the paper’s **second** illustration links money growth to **nominal interest rates** (U.S. quarterly T-bills plus filtered series). This report’s panel has no comparable interest-rate field, so Obj A focuses on the money–inflation long average and adds a separate **descriptive** money–GDP country mean, not Lucas’s T-bill replication.

The contribution is the **wedge between the long-run AVERAGE estimate and the short-run YoY estimate** — and whether IT adoption explains that gap.

## 2. Data and panel

- 163 countries, 1991–2020, 4,292 rows.
- Inputs: `02_data/analysis_ready/macro_growth_merged.csv`, `02_data/supporting/phase1_controls.csv`, `02_data/supporting/phase1_instruments.csv`.
- Output gap: `output_gap_hp` from annual HP filter (`lambda = 6.25`).
- IT adoption dates: `02_data/supporting/it_adoption_dates.csv` (Roger 2010 + Hammond 2012 reconciliation column).

## 3. Objective A — AVERAGE (Lucas-style long-run)

Country-mean money growth regressed on country-mean inflation; same for GDP growth. This matches the **first** quantity-theoretic idea in Lucas (1980) (money and inflation in long averages). Lucas’s **second** illustration in that paper uses **nominal interest rates** (U.S. T-bills with filtered money and inflation), not GDP growth; **this panel has no harmonized interest-rate series**, so leg (ii) is not replicated here — the money–GDP figure is an extra descriptive slice for the real margin only.

Read this section for: the long-run cross-country slope and its implied super-neutrality on GDP.

Sources:

- `03_analysis_notebooks/01_lucas_replication.ipynb`
- `04_current_results/figures/13_country_means_m2_vs_inflation.png`

## 4. Objective B — YoY (short-run within-country)

Same panel, but the estimand changes: within-country year-on-year variation. Three estimators:

1. Two-way fixed-effects regression of inflation (and GDP growth) on money growth.
2. Phillips block: lagged inflation + output gap predicting current inflation.
3. LP-IV horizons under fixed-sample lock and Holm familywise correction across inflation horizons.

Read this section for: the short-run pass-through and how it differs from Section 3.

Sources:

- `03_analysis_notebooks/02_panel_fe_iv_baseline.ipynb`
- `03_analysis_notebooks/03_short_run_lp_iv.ipynb`
- `04_current_results/tables/phase1_audit/core_model_results.csv`
- `04_current_results/tables/short_run_lp/lp_iv_primary_results.csv`

## 5. Objective C — IT as a regime moderator (exploratory probe)

Caveats first:

1. IT adoption is endogenous to prior inflation history.
2. IT dates differ across Roger (2010) and Hammond (2012).
3. A level-shift estimand and a slope-shift estimand are not the same object.

Headline probe: slope-shift interaction `post_it × treated × m2_growth` on inflation. This asks whether the YoY money-inflation slope from Section 4 is moderated by the IT regime.

Companion (appendix-tier): TWFE event-study on inflation levels for the same adopter set.

The section is exploratory; no causal policy claim is made in this cycle.

Sources:

- `03_analysis_notebooks/04_did_it_event_study.ipynb`
- `04_current_results/tables/short_run_lp/lp_iv_it_stratified.csv`

## 6. Diagnostics and limits

- Conservative first-stage gate is authoritative (`min stat`, `max p` across clustering choices).
- IV and LP-IV are retained in the YoY section as directional, not causal, evidence.
- Placebo, drift, and weak-IV issues are transparency constraints on interpretation.

Sources:

- `04_current_results/tables/phase1_audit/audit_scorecard.csv`
- `04_current_results/tables/phase1_audit/spec_stability_table.csv`
- `04_current_results/tables/phase1_audit/placebo_tests.csv`
- `04_current_results/summary.md`

## 7. Conclusion

- The AVERAGE estimate is consistent with a strong cross-country money-inflation association.
- The YoY estimate is smaller and sensitivity-dependent — that gap is the report's main finding.
- IT regime probes are consistent with regime moderation but do not pass causal gates.
- A dedicated causal policy evaluation of inflation targeting is reserved for a future cycle.
