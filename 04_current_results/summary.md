# Current Results Summary

## Narrative (Lucas → AVERAGE → YoY → IT regime)
- Intro (Lucas): the long-run cross-country money-inflation slope is the benchmark object the report tests.
- Objective A (AVERAGE, descriptive): country-mean money growth is strongly associated with country-mean inflation; GDP links are weaker.
- Objective B (YoY, exploratory): within-country short-run dynamics are smaller and sensitivity-dependent — the AVG vs YoY wedge is the report's main finding.
- Objective C (IT regime, exploratory probe): inflation-targeting adoption is reported as a regime moderator on the YoY slope, caveat-first.

## Interpretation Status
- INTERPRETATION_READY: `False`
- Claim tier: `associational`
- Failed gates: `preferred_first_stage_stat_gt_chi2_95_conservative, preferred_first_stage_stat_ge_10_for_strong_iv_conservative, preferred_first_stage_p_lt_0p05_conservative, preferred_relevance_agrees_across_clustering, max_inflation_drift_lt_40pct, placebo_tests_not_significant`
- **Forbidden when tier != causal**: policy-effect and counterfactual causal-effect claims.

## Estimand & Assumptions
- Objective A (AVERAGE) estimand: Lucas-style long-run country-mean associations (between-country slope).
- Objective B (YoY) estimand: short-run within-country dynamic associations (Phillips + LP-IV), exploratory with fixed-sample lock and Holm correction.
- Objective C (IT regime) estimand: slope-shift moderator on the YoY money-inflation pass-through (`post_it × treated × m2_growth`); level event-study reported as appendix companion only.
- Decision rule: failed identification/stability/placebo gates keep claims non-causal.

## Conservative Diagnostics Snapshot
- Inference decision flag: `GO_PIVOT_SHORT_RUN`
- Identification diagnostic stat (country clustering): `4.2243`
- Identification diagnostic stat (country+year clustering): `3.8016`
- Conservative identification diagnostic stat: `3.8016`
- Conservative identification diagnostic p-value: `0.0512`
- Identification relevance agreement across clustering choices: `False`
- Strong-IV threshold status (>=10, conservative): `FAIL`
- Stability drift (max inflation drift across gate specs): `0.8750`
- Placebo tests significant at p<0.05: `1`

## Objective B (YoY — Phillips Curve + Inflation Forecast)
- In-sample TWFE Phillips (baseline): inflation_l1 coef=`0.5974` (p=`0.0000`), output_gap_hp coef=`-0.1043` (p=`0.3524`), within R²=`0.5481`, n=`4102`.
- In-sample TWFE Phillips (augmented +m2_growth): inflation_l1 coef=`0.4658` (p=`0.0000`), output_gap_hp coef=`-0.1530` (p=`0.1061`), m2_growth coef=`0.2925` (p=`0.0050`), within R²=`0.6594`.
- Holdout forecast (train ≤ 2015, test 2016–2020, country FE only):
  - `naive_ar1`: RMSE=`0.0758`, MAE=`0.0275`, bias=`+0.0056`, n=`721` rows / `151` countries.
  - `phillips`: RMSE=`0.0758`, MAE=`0.0275`, bias=`+0.0055`, n=`721` rows / `151` countries.
  - `phillips_augmented`: RMSE=`0.0635`, MAE=`0.0294`, bias=`-0.0035`, n=`721` rows / `151` countries.
- RMSE gain (augmented Phillips vs naive AR(1)): `16.2%`.

## Objective B (YoY — Short-Run LP-IV)
- Inference decision flag: `EVIDENCE_WEAK_REVISIT_IDENTIFICATION`
- LP horizon estimates use a fixed sample lock across horizons.
- LP horizon familywise control uses Holm correction for inflation horizons.
- Primary IV inflation significant horizons (5%, unadjusted): `4`
- Primary IV inflation significant horizons (5%, Holm): `4`
- Primary IV GDP significant horizons (5%): `0` (static h=0 only)

## Interpretation Scope
- Treat all estimates as descriptive association evidence only (non-causal).
- Forbidden claims: policy-effect statements and counterfactual causal-effect statements.