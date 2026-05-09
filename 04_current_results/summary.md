# Current Results Summary

## Data

- 160 countries, 1991–2024, 4,750 rows
- `sample_main` = all 160 countries
- `sample_low_inflation` = 123 countries (drop if any year > 40% inflation — removes post-Soviet / Latin American hyperinflation)

## Obj A — Long-run country means (≥30 obs)

| Sample | n | M2→Inflation | p | R² |
|---|---|---|---|---|
| Full | 108 | 0.952 | 4.4e-50 | 0.877 |
| Clean | 83 | 0.524 | 6.8e-15 | 0.529 |

- Full-sample GDP slope: 0.016 (p=0.484, n.s.)
- Clean-sample GDP slope: 0.283 (p<0.001) — financial deepening effect, not QTM
- Lucas ii cross-country (M2 mean vs lending rate, 107 clean countries): slope=0.49, R²=0.16

## Obj B — Short-run TWFE

| Sample | coef | p | Within R² | n |
|---|---|---|---|---|
| Full (160c) | 0.665 | 0.00018 | 0.504 | 4,750 |
| Clean (123c) | 0.040 | 0.062 | 0.029 | 3,639 |

**Headline:** Clean-sample slope collapses to 0.040 (n.s.). Short-run pass-through in the full sample lives in hyperinflation outliers.

## Obj B — Phillips curve (full sample)

- Baseline: inflation_l1=0.593 (p<0.001), output_gap=-0.115 (p=0.214), within R²=0.548, n=4,483
- Augmented +m2: inflation_l1=0.445, output_gap=-0.174 (p=0.041), m2_growth=0.349 (p=0.032), within R²=0.672
- Holdout RMSE gain (augmented vs naive AR1): 8.1%

## Obj B — IV identification

- Conservative first-stage F = 4.363 (passes ≥3.84; FAILS strong-IV ≥10)
- Conservative p = 0.037
- 1 placebo significant at p<0.05
- All IV results associational only

## Obj C — IT regime (exploratory)

IT adopters show weaker short-run pass-through. Endogenous adoption. No causal claim.

## Obj D — US appendix (FRED 1960–2024, 5-yr MA)

- M2 → Inflation: slope=0.474, R²=0.196
- M2 → T-bill: slope=0.421, R²=0.092

## Claim tiers

- Obj A, D: descriptive
- Obj B, C: exploratory / associational
- Forbidden: policy-effect and counterfactual causal claims
