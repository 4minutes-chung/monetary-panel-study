# Executive Memo

**Question:** Does the quantity theory of money hold in the post-QE, post-COVID era?

The canonical papers (McCandless & Weber 1995; De Grauwe & Polan 2005) end before 2008.
This panel covers 1991–2024, including the QE decade (M2 up, inflation flat) and COVID surge (2021–2023).

Two samples throughout: **full** (160 countries) and **clean** (123 countries — drop if any year > 40% inflation, removing post-Soviet and Latin American hyperinflation episodes from the 1990s).

---

## Data

- 160 countries, 1991–2024, 4,750 rows
- M2 growth, CPI inflation, GDP growth (World Bank WDI)
- Lending rate (World Bank FR.INR.LEND), 147 countries
- US appendix: FRED M2, CPI, 3-month T-bill, 1960–2024

---

## Obj A — Long-run (country means, ≥30 obs)

| Sample | n countries | M2→Inflation slope | R² | M2→GDP slope |
|---|---|---|---|---|
| Full | 108 | **0.952** (p=4.4e-50) | 0.877 | 0.016 (n.s.) |
| Clean | 83 | **0.524** (p=6.8e-15) | 0.529 | 0.283 (p<0.001) |

Long-run association holds in both samples. Full-sample slope near one-for-one — driven partly by hyperinflation outliers confirming QTM at extremes. Clean-sample slope (0.52) is the modern-economy estimate.

**Lucas ii cross-country:** M2 mean vs lending rate mean, 107 clean countries — slope = 0.49, R² = 0.16. Fisher relation holds in direction.

---

## Obj B — Short-run TWFE (year-on-year, within country)

| Sample | coef | p-value | Within R² | Rows |
|---|---|---|---|---|
| Full (160c) | **0.665** | 0.00018 | 0.504 | 4,750 |
| Clean (123c) | **0.040** | 0.062 | 0.029 | 3,639 |

**The clean-sample TWFE is the headline result.** Without hyperinflation countries, year-to-year money growth has no significant short-run effect on inflation. The full-sample slope (0.665) lives in the 1990s transition economies.

### Phillips curve (full sample)

- Baseline: inflation(t−1) coef = 0.593, within R² = 0.548
- Augmented (+m2): m2_growth coef = 0.349 (p=0.032), within R² = 0.672
- Holdout RMSE gain vs naïve AR(1): 8.1%

Lagged inflation and output gap do most short-run work. M2 adds something in the full sample but not significantly in the clean sample.

---

## The wedge — what the project actually shows

| Estimator | Full sample | Clean sample |
|---|---|---|
| Long-run Obj A | 0.952 | 0.524 |
| Short-run TWFE Obj B | 0.665 | **0.040** |

In modern non-hyperinflationary economies: long-run ~0.5, short-run ~0. That is the QE decade in one number.

---

## Obj C — IT regime (exploratory)

IT adopters show weaker short-run pass-through. Consistent with expectations anchoring. Endogenous adoption — not a causal claim.

---

## Obj D — US appendix (1960–2024)

| | Slope | R² |
|---|---|---|
| M2 → Inflation (5yr MA) | 0.474 | 0.196 |
| M2 → T-bill (5yr MA) | 0.421 | 0.092 |

Same story as cross-country: low-frequency relationship holds but QE decade pulls slope below the long-run benchmark.

---

## Identification limits

- Conservative first-stage F = 4.4 (passes relevance gate; fails strong-IV ≥10)
- 1 significant placebo test
- All IV results associational only
- Claim tier: descriptive (Obj A, D), exploratory (Obj B, C)

---

## One paragraph

In long-run country averages, money growth and inflation are positively associated (slope 0.52–0.95 depending on sample). Year-to-year within countries, the pass-through collapses: 0.665 in the full panel, 0.040 in the 123 non-hyperinflationary countries. That near-zero short-run slope in the clean sample is the QE decade's empirical signature — central banks expanded M2 for a decade without inflation, and this panel quantifies exactly how weak the short-run transmission was. The COVID surge appears in the data but is not enough to flip the result. Long run: quantity theory holds. Short run in modern economies: it largely disappears.
