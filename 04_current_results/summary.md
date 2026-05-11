# Current Results Summary

## Data

- 160 countries, 1991–2024, 4,750 rows
- `sample_main` = all 160 countries
- `sample_low_inflation` = 123 countries (drop if any year > 40% inflation)

## Obj A — Long-run country means (≥30 obs)

| Sample | n | M2→Inflation slope | p | R² |
|---|---|---|---|---|
| Full | 108 | 0.952 | 4.4e-50 | 0.877 |
| Clean | 83 | 0.524 | 6.8e-15 | 0.529 |

- Full-sample GDP slope: 0.016 (p=0.484, n.s.)
- Clean-sample GDP slope: 0.283 (p<0.001)
- Lucas ii cross-country (M2 mean vs lending rate, 107 clean countries): slope=0.49, R²=0.16

## Obj B — Short-run TWFE

| Sample | coef | p | Within R² | n |
|---|---|---|---|---|
| Full (160c) | 0.665 | 0.00018 | 0.504 | 4,750 |
| Clean (123c) | 0.040 | 0.062 | 0.029 | 3,639 |

**Headline:** Clean-sample slope collapses to 0.040 (n.s.). Short-run pass-through in the full sample lives in hyperinflation outliers.

## Obj B — AR(1)+M2 persistence regression (full sample)

| Variable | Baseline | p | Augmented | p |
|---|---|---|---|---|
| inflation_l1 | 0.593 | <0.001 | 0.445 | <0.001 |
| output_gap (HP) | -0.001 | 0.307 | -0.001 | 0.081 (n.s.) |
| m2_growth | — | — | 0.349 | 0.032 |
| Within R² | 0.548 | — | 0.672 | — |

- Holdout RMSE gain (augmented vs naive AR1): 7.4% (2016–2024)
- output_gap n.s. after HP filter unit fix (bug B-1)

## Obj B — IV identification

- Conservative first-stage F = 6.65 (instruments extended to 2024; passes ≥3.84; FAILS strong-IV ≥10)
- 1 placebo significant at p<0.05
- IV coefficient (1.468) diverges from TWFE — exclusion restriction not clean; directional only

## Obj B — Sub-period TWFE (clean sample)

| Era | coef | p | N obs | N countries |
|---|---|---|---|---|
| Pre-QE 1991–2007 | 0.113 | <0.001 | 1,764 | 119 |
| QE era 2008–2019 | 0.001 | 0.827 (n.s.) | 1,398 | 123 |
| COVID 2020–2024 | -0.014 | 0.655 (n.s.) | 477 | 107 |

**GFC was the breakpoint, not COVID.**

## Obj B — COVID cross-country scatter

| | Value |
|---|---|
| Countries | 102 |
| Slope (M2 2020–21 → Inflation 2021–23) | 0.494 |
| p-value | <0.0001 |
| R² | 0.255 |

## Obj B — Distributed lag (full sample)

| Horizon | coef | SE | p |
|---|---|---|---|
| h=0 | 0.338 | 0.118 | 0.004 |
| h=1 | 0.257 | 0.048 | <0.001 |
| h=2 | 0.132 | 0.036 | <0.001 |

Signal persists at least 2 years, decaying across horizons.

## Obj C — IT regime (exploratory)

| Term | coef | p |
|---|---|---|
| m2_growth (baseline) | 0.636 | 0.002 |
| it_m2 (pre-adoption offset) | 0.212 | 0.281 (n.s.) |
| post_treated_m2 (post-adoption shift) | -0.485 | <0.001 |

Endogenous adoption. No causal claim.

## Obj D — US appendix (FRED 1960–2024, 5-yr MA)

| Relationship | slope | R² | HAC p |
|---|---|---|---|
| M2 → Inflation | 0.474 | 0.196 | 0.060 (borderline) |
| M2 → T-bill | 0.421 | 0.092 | 0.155 (n.s.) |

## Diagnostics

| Test | Result |
|---|---|
| Pesaran CD | CD=158.4, p≈0 — strong CSD confirmed |
| IPS inflation | W=-34.4, p≈0 — stationary I(0) |
| IPS m2_growth | W=-36.3, p≈0 — stationary I(0) |
| DK full (HAC bw=4) | coef=0.665, t=2.945, p=0.003 |
| DK clean (HAC bw=4) | coef=0.040, t=1.456, p=0.145 |
| COVID robustness (excl 2020–21) | full=0.664, clean=0.040 — unchanged |
| TWFE on 108-country Obj A subset | coef=0.820, p<0.001 |

## Claim tiers

- Obj A, D: descriptive
- Obj B, C: exploratory / associational
- Forbidden: causal policy claims
