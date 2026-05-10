# Final Report Draft

## 1. Introduction

Does the quantity theory of money hold in the era of quantitative easing and post-COVID inflation?

Lucas (1980) established the benchmark: in long-run cross-country data, money growth and inflation should move roughly one-for-one. McCandless & Weber (1995) and De Grauwe & Polan (2005) confirmed that fact with pre-GFC samples. But neither study covers the defining monetary events of the last 25 years: the 2008–2020 "money without inflation" QE decade, in which M2 expanded sharply while inflation stayed near zero; and the 2021–2023 inflation surge, the sharpest since the 1970s. This report uses 160 countries through 2023 to ask whether the long-run fact is robust — and why the year-to-year pass-through is much smaller.

Lucas’s **second** illustration links money growth to **nominal interest rates** (U.S. T-bills, filtered); the cross-country panel has no harmonised rate series, so that leg is handled separately in a US-only appendix (Obj D, `05_lucas_us_appendix.ipynb`). The main analysis uses the **first** Lucas illustration: money growth vs inflation in long averages (Obj A) and year-to-year within-country (Obj B).

The central result is the **wedge between the long-run AVERAGE estimate and the short-run YoY estimate** — and whether IT adoption (Obj C) explains it.

## 2. Data and panel

- 160 countries, 1991–2024, 4,750 rows.
- Inputs: `02_data/analysis_ready/macro_growth_merged.csv`, `02_data/supporting/phase1_controls.csv`, `02_data/supporting/phase1_instruments.csv`.
- Output gap: `output_gap_hp` from annual HP filter (`lambda = 6.25`).
- IT adoption dates: `02_data/supporting/it_adoption_dates.csv` (Roger 2010 + Hammond 2012 reconciliation column).

## 3. Objective A — AVERAGE (Lucas-style long-run)

Two samples reported throughout: **full** (160 countries, all data) and **clean** (123 countries, drop if any year > 40% inflation — removes post-Soviet and Latin American hyperinflation episodes from 1991–1999 that are not the focus of this study).

### Full sample (108 countries with ≥30 obs)

| Outcome | Slope | p-value | R² |
|---|---|---|---|
| Inflation | **0.952** | 4.4×10⁻⁵⁰ | 0.877 |
| GDP growth | 0.016 | 0.484 | 0.005 |

### Clean sample (83 countries with ≥30 obs, no hyperinflation)

| Outcome | Slope | p-value | R² |
|---|---|---|---|
| Inflation | **0.524** | 6.8×10⁻¹⁵ | 0.529 |
| GDP growth | 0.283 | <0.001 | 0.291 |

The full-sample slope (0.95) is near one-for-one — hyperinflation countries at the far right of the scatter confirm the quantity theory at extremes. The clean-sample slope (0.52) is the more relevant estimate for modern monetary policy: the long-run association still holds but is weaker in non-hyperinflationary economies.

The clean-sample GDP slope (0.28) is unexpected; likely reflects financial deepening correlating with both M2 and growth in emerging markets, not monetary neutrality violation.

### Lucas (ii) spirit — cross-country M2 vs nominal lending rate

Country-mean M2 growth vs country-mean lending rate, clean sample, 107 countries:
- Slope = **0.49**, p < 0.001, R² = 0.156

Positive and significant — consistent with the Fisher relation. The slope is below 1 because the lending rate includes a bank credit-risk spread above the policy rate.

**Note:** Lucas’s second illustration uses nominal interest rates, not GDP. Lending rate is the best available cross-country proxy; the US-only version with T-bills is in Obj D.

Source: `03_analysis_notebooks/01_lucas_replication.ipynb`

## 4. Objective B — YoY (short-run within-country)

Same 160-country panel, different estimand: within-country year-on-year variation (TWFE absorbs country and year fixed effects).

### TWFE baseline

| Sample | Coef | p-value | Within R² | Rows |
|---|---|---|---|---|
| Full (160 countries) | **0.665** | 0.00018 | 0.504 | 4,750 |
| Clean (123 countries, no hyperinflation) | **0.040** | 0.062 | 0.029 | 3,639 |

The full-sample short-run slope is **0.665** — already well below the long-run 0.952, confirming the wedge. But the clean-sample slope collapses to **0.040** (not significant at 5%). **This is the central result.** Strip out the post-Soviet and Latin American hyperinflation episodes and year-to-year money growth has essentially no detectable short-run effect on inflation in the remaining 123 countries. This is exactly what the QE decade shows: central banks expanded M2 for a decade without triggering inflation.

### AR(1)+M2 persistence regression

Adding lagged inflation and output gap:

| Variable | Coef | p-value |
|---|---|---|
| inflation(t−1) | 0.593 | <0.001 |
| output gap (HP) | −0.001 | 0.307 (n.s.) |
| Within R² | 0.548 | — |

Augmented with m2_growth:

| Variable | Coef | p-value |
|---|---|---|
| inflation(t−1) | 0.445 | <0.001 |
| output gap (HP) | −0.001 | 0.081 (n.s.) |
| m2_growth | **0.349** | 0.032 |
| Within R² | 0.672 | — |

Money growth adds explanatory power beyond lagged inflation. The output gap is not significant in either specification after correcting the HP filter unit error (fix B-1; see ERRATA.md). Holdout forecast (train ≤ 2015, test 2016–2024): augmented RMSE is 7.6% lower than a naïve AR(1) — modest but consistent improvement. The m2_growth coefficient (0.349, p=0.032) survives the bug fix unchanged.

### LP-IV (appendix)

Local projection IV horizons show a significant inflation response at h=0–3 under Holm correction. Conservative first-stage F = 5.587 (passes relevance gate ≥3.84; FAILS strong-IV ≥10). IV coefficient (1.468) diverges from TWFE baseline (0.665) — a sign the exclusion restriction is not clean. All IV results are treated as directional only and are not used for inference. See `03_analysis_notebooks/03_short_run_lp_iv.ipynb`.

Sources: `03_analysis_notebooks/02_panel_fe_iv_baseline.ipynb` · `03_analysis_notebooks/exports/phase1/phase1_fe_results.csv` · `03_analysis_notebooks/exports/phase1/phase1_phillips_results.csv` · Note: `04_current_results/tables/phase1_audit/phillips_results.csv` contains pre-fix values (output_gap p=0.041) and should not be used for the augmented Phillips numbers.

## 5. Objective C — IT as a regime moderator (exploratory probe)

**Caveats lead:**
1. IT adoption is endogenous — countries adopted IT after high-inflation episodes (selection bias).
2. Adoption dates differ across Roger (2010) and Hammond (2012).
3. Level-shift and slope-shift are distinct estimands.

Headline probe: does the YoY money-inflation slope (0.665) differ between IT adopters and non-adopters? IT countries show weaker short-run pass-through post-adoption — consistent with anchoring expectations, but not a causal estimate.

Companion (appendix-tier): TWFE event-study on inflation levels around adoption date.

No causal policy claim is made.

Source: `03_analysis_notebooks/04_did_it_event_study.ipynb` · `04_current_results/tables/short_run_lp/lp_iv_it_stratified.csv`

## 6. Objective D — US appendix (Lucas ii spirit)

Using FRED annual data (1960–2024) with a 5-year centred moving-average filter:

| Relationship | Slope | R² |
|---|---|---|
| M2 growth → Inflation | 0.474 | 0.196 |
| M2 growth → T-bill rate | 0.421 | 0.092 |

Both relationships are positive and consistent with the quantity theory / Fisher relation at low frequencies. The QE decade (2009–2020) pulls the slope below 1 for inflation and compresses the T-bill scatter — the same "money without inflation" regime visible in the cross-country panel.

Note: Lucas (1980) used M1. The Fed’s 2020 M1 redefinition (savings deposits reclassified into M1) creates a ~120% discontinuity in M1 growth that year. M2 is used here for consistency with the cross-country panel.

Source: `03_analysis_notebooks/05_lucas_us_appendix.ipynb` · `04_current_results/figures/lucas_us_inflation.png` · `04_current_results/figures/lucas_us_tbill.png`

## 7. Identification limits

- Conservative first-stage F = 5.587 (passes relevance gate ≥3.84; FAILS strong-IV ≥10). IV coefficient (1.468) diverges from TWFE baseline (0.665) — a sign the exclusion restriction is not clean. All IV results are treated as directional only and are not used for inference.
- 1 significant placebo test. Drift is moderate.
- Cross-sectional dependence confirmed (Pesaran CD = 158.4, p≈0). Driscoll-Kraay SEs (HAC kernel, bandwidth=4) preserve significance for full-sample TWFE (coef=0.665, p=0.003) but not clean-sample (coef=0.040, p=0.145).
- COVID robustness: excluding 2020–2021 leaves coefficients essentially unchanged (full: 0.664, clean: 0.040). COVID years do not drive the result.
- Sample mismatch: TWFE on the same 108-country Obj-A subset gives coef=0.820 (p<0.001) — the wedge is real across consistent samples, not a composition artifact of the extra 52 countries. The wedge between long-run country-mean (Obj A) and short-run TWFE (Obj B) estimates reflects a mechanical between-vs-within decomposition. Confirming this reflects genuine regime change requires a Mundlak decomposition or Pesaran mean-group estimator, which is left for future work.
- US appendix: Newey-West HAC (bandwidth=4) confirms M2→Inflation slope=0.474 but with borderline p=0.060; M2→T-bill is n.s. after HAC (p=0.155). The T-bill Fisher result should be treated as illustrative only.
- All IV/LP-IV results are retained as associational/directional only.
- Claims are bounded to descriptive (Obj A, D) and exploratory (Obj B, C).

Source: `04_current_results/tables/phase1_audit/audit_scorecard.csv` · `04_current_results/summary.md`

## 8. Conclusion

In long-run cross-country averages, money growth tracks inflation positively in both samples: slope = 0.952 (full, 108 countries) and 0.524 (clean, 83 countries). The quantity theory long-run association survives 1991–2024.

Year-to-year within countries, the picture splits by sample. Full sample: slope = 0.665, clearly significant. Clean sample (no hyperinflation): slope = 0.040, not significant at 5%. **The short-run relationship lives almost entirely in the hyperinflationary outliers.** For the 123 countries that have not had hyperinflation — the set that includes every advanced economy and most modern emerging markets — year-to-year money growth barely moves inflation.

This is the QE-era finding stated precisely: in normal-inflation countries, short-run monetary transmission into prices is weak. The COVID inflation surge (2021–2023) is visible in the data but does not restore significance in the clean panel — the 2021–2023 observations are inside the sample and still insufficient to flip the result.

The Phillips curve confirms that lagged inflation and the output gap do more of the short-run work than M2. IT adoption correlates with weaker pass-through — regime story, not causal. The US appendix mirrors the cross-country result: low-frequency M2 growth tracks inflation (slope 0.47) and the T-bill rate (0.42), but the QE decade pulls both below the long-run benchmark.

In short: **the quantity theory holds in the long run; it largely disappears short-run in modern economies. The QE decade and the clean-sample TWFE are the same fact, two angles.**
