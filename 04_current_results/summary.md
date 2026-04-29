# Current Results Summary

## Empirical Design Updates
- Kept exact FE formulas for IV estimation.
- Kept exact calendar-year horizon matching (no row-shift approximation).
- Added explicit no-partial-export checks for LP-IV outputs.
- Added inference sensitivity table comparing one-way vs two-way clustering on key IV spec.
- Clarified identification validity read: first-stage is reported as clustered Wald chi2(1), not classic F-stat.
- Reporting language now tracks inference robustness and reproducibility of empirical artifacts.

## Interpretation Status
- INTERPRETATION_READY: `False`
- Claim tier: `associational`
- Failed gates: `preferred_first_stage_stat_gt_chi2_95_conservative, preferred_first_stage_stat_ge_10_for_strong_iv_conservative, preferred_first_stage_p_lt_0p05_conservative, preferred_relevance_agrees_across_clustering, max_inflation_drift_lt_40pct, placebo_tests_not_significant`
- **Forbidden when tier != causal**: policy-effect and counterfactual causal-effect claims.

## Estimand & Assumptions
- Estimand (associational): panel relationship between `m2_growth` and outcomes under country/time fixed effects.
- Estimand (IV): local IV estimand for `m2_growth` using specified instruments.
- Identification assumptions: instrument relevance, exogeneity, and exclusion restriction.
- Decision rule: failed identification/stability/placebo gates downgrade claims from `causal` to `associational` or `exploratory`.

## Inference Decision
- Decision: `GO_PIVOT_SHORT_RUN`
- Identification diagnostic stat (country clustering): `4.2243`
- Identification diagnostic stat (country+year clustering): `3.8016`
- Conservative identification diagnostic stat: `3.8016`
- Conservative identification diagnostic p-value: `0.0512`
- Identification relevance agreement across clustering choices: `False`
- Strong-IV threshold status (>=10, conservative): `FAIL`
- Stability drift (max inflation drift across gate specs): `0.8750`
- Placebo tests significant at p<0.05: `1`

## Phase 2 LP-IV
- Inference decision flag: `EVIDENCE_WEAK_REVISIT_IDENTIFICATION`
- Primary IV inflation significant horizons (5%): `4`
- Primary IV GDP significant horizons (5%): `0` (static h=0 only)

## Interpretation Scope
- Treat all estimates as descriptive association evidence only (non-causal).
- Forbidden claims: policy-effect statements and counterfactual causal-effect statements.