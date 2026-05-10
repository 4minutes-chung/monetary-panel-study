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

## Obj B — AR(1)+M2 persistence regression (full sample)

- Baseline: inflation_l1=0.593 (p<0.001), output_gap=-0.001 (p=0.307, n.s.), within R²=0.548, n=4,590
- Augmented +m2: inflation_l1=0.445, output_gap=-0.001 (p=0.081, n.s. — HP filter corrected), m2_growth=0.349 (p=0.032), within R²=0.672
- Holdout RMSE gain (augmented vs naive AR1): 7.4% (2016–2024)
- Note: output_gap was previously over-stated (p=0.041) due to HP filter unit error (B-1). After fix, output_gap is n.s.

## Obj B — IV identification

- Conservative first-stage F = 5.587 (passes ≥3.84; FAILS strong-IV ≥10)
- Conservative p = 0.018
- 1 placebo significant at p<0.05
- All IV results associational only
- IV coefficient (1.468) diverges from TWFE (0.665) — exclusion restriction not clean; directional only

## Obj C — IT regime (exploratory)

IT adopters show weaker short-run pass-through. Endogenous adoption. No causal claim.

## Obj D — US appendix (FRED 1960–2024, 5-yr MA)

- M2 → Inflation: slope=0.474, R²=0.196
- M2 → T-bill: slope=0.421, R²=0.092

## Diagnostic results (post-council audit)

### Pesaran CD test (cross-sectional dependence)

- CD = 158.435, p = 0.000 → REJECT H0: strong cross-sectional dependence confirmed
- Expected given common global shocks (GFC, COVID)

### Panel unit root (IPS test)

- Inflation: W = -34.4, p ≈ 0.000 → REJECT H0 (unit root) — inflation is stationary I(0)
- M2 growth: W = -36.3, p ≈ 0.000 → REJECT H0 — m2_growth is stationary I(0)
- TWFE is valid; no spurious regression concern

### Driscoll-Kraay standard errors (robust to CSD + serial correlation)

- Full sample: coef=0.6649, t=2.945, p=0.003 → survives DK correction
- Clean sample: coef=0.0403, t=1.456, p=0.145 → remains n.s.

### COVID robustness (exclude 2020–2021)

- Full sample: coef=0.6641, p=0.0002 — virtually unchanged from 0.6649 with COVID
- Clean sample: coef=0.0405, p=0.067 — unchanged; COVID years do not drive result

### Sample mismatch test

- ≥30 obs countries (Obj A set): n=108 (confirmed)
- TWFE on 108-country subset: coef=0.820, p=0.000 (higher than 160-country 0.665 — extra 52 countries pull within-slope down)
- Obj A between-estimator on all 160c: slope=0.879, R²=0.851
- Same-sample wedge: 0.952 (Obj A) − 0.820 (TWFE on 108c) = 0.132; less than half the headline wedge of 0.287 (0.952 − 0.665). Wedge survives but is smaller under matched samples.

### US appendix Newey-West HAC (nb05)

- M2→Inflation NW: slope=0.474, t=1.884, p=0.060 (borderline; OLS p was lower)
- M2→T-bill NW: slope=0.421, t=1.423, p=0.155 (n.s. after HAC)
- T-bill Fisher result is fragile to HAC correction; note in appendix

### Mundlak / Pesaran mean-group

- The wedge between long-run Obj A (0.952) and short-run TWFE (0.665) reflects a mechanical between-vs-within decomposition
- Confirming genuine regime change requires Mundlak decomposition or mean-group estimator — left for future work

## Claim tiers

- Obj A, D: descriptive
- Obj B, C: exploratory / associational
- Forbidden: policy-effect and counterfactual causal claims
