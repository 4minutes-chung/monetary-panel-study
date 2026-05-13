# Money Growth and Inflation After QE and COVID

### A 160-Country Empirical Audit, 1991-2024

This report is descriptive. It does not make causal policy claims.

## 1. Research Question

Lucas (1996), building on McCandless and Weber (1995), emphasizes a long-run cross-country fact: countries with faster average money growth tend to have faster average inflation.

This project updates that fact through 2024, then asks whether the same relationship appears in annual within-country variation after QE and COVID.

The organizing question is:

> Does broad money growth still predict inflation once we distinguish long-run cross-country differences from short-run within-country timing?

The answer is:

1. Long-run cross-country evidence remains strong.
2. Short-run within-country association is much weaker in clean low-inflation samples.
3. The short-run clean-sample association weakens sharply after 2008.
4. COVID is useful as descriptive stress evidence, not causal identification.

## 2. Data

Main panel:

- 160 countries.
- 1991-2024 annual data.
- 4,750 country-years.
- Source: World Bank WDI-derived macro panel.

Core variables:

| Variable | Meaning |
|---|---|
| `m2_growth` | World Bank broad money growth, decimal units |
| `inflation` | CPI inflation, decimal units |
| `gdp_growth` | real GDP growth, decimal units |
| `sample_main` | all usable country-years |
| `sample_low_inflation` | excludes countries with any inflation year above 40 percent |

World Bank broad money is M2-like for cross-country macro work, but it is not literally the U.S. FRED M2 series.

Two samples are used:

| Sample | Countries | Rows | Definition |
|---|---:|---:|---|
| Full | 160 | 4,749 | all available country-years |
| Clean | 123 | 3,638 | drops countries with any annual inflation above 40 percent |

Data note: Sierra Leone 2015 broad money growth is set to missing. The raw World Bank WDI source shows a unit break in that year (M2/GDP level series drops from ~13,000 to ~15, a redenomination/reporting artifact), producing a spurious -680% computed growth rate. The observation is excluded from all regressions via standard `dropna` handling.

## 3. Long-Run Country Averages

Notebook:

`03_analysis_notebooks/01_lucas96_mcweber_replication.ipynb`

Estimator:

```text
average_inflation_i = alpha + beta * average_m2_growth_i + error_i
```

Countries are included in the long-run regression if they have at least 30 observations.

| Sample | Countries | Slope | p-value | R2 |
|---|---:|---:|---:|---:|
| Full | 108 | 0.952 | 4.4e-50 | 0.877 |
| Clean | 83 | 0.524 | 6.8e-15 | 0.529 |

Read:

The classic long-run money-inflation relationship survives through 2024. The full-sample slope is near one-for-one. The clean-sample slope is smaller but still strongly positive.

This is the Lucas (1996) / McCandless-Weber side of the project.

## 4. Short-Run Within-Country TWFE

Notebook:

`03_analysis_notebooks/02_money_inflation_twfe.ipynb`

Estimator:

```text
inflation_it = country FE + year FE + beta * m2_growth_it + error_it
```

This is a descriptive within-country annual association. It is not a causal monetary policy multiplier.

| Sample | Coefficient | p-value | N |
|---|---:|---:|---:|
| Full | 0.855 | <0.001 | 4,749 |
| Clean | 0.096 | <0.001 | 3,638 |

Read:

The full sample has a strong positive short-run association. The clean-sample coefficient is much smaller than the full-sample one, confirming that high-inflation episodes drive much of the full-sample estimate. Even in the clean sample the association is statistically significant, but the magnitude is small relative to the long-run cross-country slope. This is the central contrast with the long-run country-average result.

## 5. Pre/Post-2008 Split

Same TWFE specification, clean sample only:

| Era | Coefficient | p-value | N obs | Countries |
|---|---:|---:|---:|---:|
| 1991-2007 | 0.1128 | <0.001 | 1,764 | 119 |
| 2008-2019 | -0.0063 | 0.711 | 1,397 | 123 |
| 2020-2024 | -0.0139 | 0.655 | 477 | 107 |

Read:

The short-run within-country association is visible before 2008 and near zero afterward. This supports the project subtitle: long-run evidence survives, but short-run pass-through weakens after 2008.

This does not prove that QE caused the weakening. It only documents the timing and association.

## 6. Between-Vs-Within Wedge

Figure:

`04_current_results/figures/between_within_decomposition.png`

This figure compares two questions using the same clean country panel:

1. Between countries: do countries with higher average M2 growth have higher average inflation?
2. Within countries: do annual deviations in M2 growth line up with annual deviations in inflation?

The answer differs because the estimands differ. The long-run cross-country relationship can be strong while the annual within-country relationship is weak.

## 7. Robustness Layer

Notebook 02 keeps the robustness layer compact:

| Check | Result |
|---|---|
| Exclude 2020-2021, full sample | coefficient remains about 0.858 |
| Exclude 2020-2021, clean sample | coefficient remains about 0.099 |
| Driscoll-Kraay, full sample | coefficient 0.855, p < 0.001 |
| Driscoll-Kraay, clean sample | coefficient 0.096, p about 0.023 |

Read:

The clean-sample result is not a COVID-year artifact — excluding 2020-2021 leaves it essentially unchanged. Under Driscoll-Kraay inference the clean estimate remains significant (p=0.023), though with wider standard errors than clustered.

## 8. COVID Descriptive Evidence

COVID is not a causal design in this project.

The descriptive cross-country scatter asks whether countries with larger cumulative broad money growth in 2020-2021 had larger cumulative inflation in 2021-2023.

| Statistic | Value |
|---|---:|
| Slope | 0.494 |
| p-value | <0.0001 |
| R2 | 0.255 |
| Countries | 102 |

Read:

The COVID period shows a positive cross-country money-inflation association. This is consistent with a monetary interpretation, but it cannot separate broad money from fiscal transfers, supply shocks, exchange rates, or expectations.

## 9. Distributed-Lag Appendix

Notebook:

`03_analysis_notebooks/02b_money_inflation_exploratory.ipynb`

Figure:

`04_current_results/figures/distributed_lag_cumulative_association.png`

This part is worth keeping, but only with careful wording.

The old "IRF/shock response" language is too strong. The current version treats the estimates as reduced-form cumulative distributed-lag associations:

| Horizon | Cumulative estimate | 95% CI |
|---|---:|---|
| h=0 | 0.481 | [0.314, 0.649] |
| h=0+1 | 0.777 | [0.622, 0.931] |
| h=0+1+2 | 0.881 | [0.694, 1.068] |

Read:

The same-year association (0.48) is smaller than the 3-year cumulative (0.88), which is close to the long-run between-country slope. This suggests money growth affects inflation over multiple years, not just within the same calendar year. Treat as appendix descriptive evidence only.

## 10. Exploratory Appendices

### LP-IV

Notebook:

`03_analysis_notebooks/03_short_run_lp_iv.ipynb`

Fixed sample: 3,390 rows. Two instruments tested.

| Instrument | First-stage F | Verdict |
|---|---:|---|
| instrument_m2_external_level | 6.60 | above relevance gate (3.84), below strong-IV (10) |
| instrument_m2_l1 | 2.99 | below relevance gate — discard |

Under the primary instrument, inflation LP-IV coefficients across horizons:

| Horizon | Coefficient | p-value | Holm p-value |
|---|---:|---:|---:|
| h=0 | 1.224 | 0.00017 | 0.00068 |
| h=1 | 0.954 | 0.00099 | 0.00297 |
| h=2 | 0.879 | 0.00441 | 0.00882 |
| h=3 | 0.696 | 0.01153 | 0.01153 |

GDP h=0: coefficient -0.172, p=0.190 — not significant.

What this supports: in this panel, higher money growth is followed by higher inflation over the next 0–3 years. GDP short-run effect is not statistically clear. Evidence is directional and suggestive, not strong causal proof, because first-stage strength is moderate (F=6.60).

IT stratification (adopters vs never-adopters) was attempted but both subgroups fail the relevance gate (adopters F=1.43, never-adopters F=3.21). Those results are archived and should not be interpreted.

Do not use any of these as causal evidence.

### Inflation Targeting

Notebook:

`03_analysis_notebooks/04_did_it_event_study.ipynb`

The full-sample post-adoption slope shift is -0.512 (p<0.001); clean-sample -0.266 (p<0.001). This is exploratory because inflation-targeting adoption is endogenous.

Cross-notebook read: Notebook 02 shows the aggregate short-run pass-through near zero post-2008. Notebook 02b shows the association accumulates over multiple years. Notebook 03 shows directional money→inflation prediction over h=0–3. Notebook 04 adds a structural feature: IT-adopting countries show much lower short-run M2→inflation slopes post-adoption. Together these notebooks point the same direction — pass-through exists, is slow, and is weaker in countries with IT frameworks. This is a consistent associational pattern across designs, not a causal chain.

### U.S. Appendix

Notebook:

`03_analysis_notebooks/05_lucas_us_appendix.ipynb`

This is Lucas (1980)-inspired descriptive evidence using U.S. FRED data. The filter matches Lucas (1980) eq. (1) exactly: two-sided exponential MA with β=0.9, boundary-normalised. Two estimations are run:

**M1 (1960–2019, pre-2020 definitional break):**

| Relationship | Slope | R² | Read |
|---|---:|---:|---|
| M1 growth → inflation | 0.079 | 0.003 | breaks down |
| M1 growth → T-bill | -0.272 | 0.015 | breaks down |

M1 fails because sweep-account distortions (1990s–2000s) and QE-era M1 surge (2009–2019) pull M1 growth away from inflation over the full sample.

**M2 (1960–2024):**

| Relationship | Slope | R² | Read |
|---|---:|---:|---|
| M2 growth → inflation | 1.041 | 0.623 | close to Lucas's theoretical 1.0 |
| M2 growth → T-bill | 1.357 | 0.377 | directional |

With the correct Lucas filter, M2 produces a slope near 1.0 — the key Lucas (1980) prediction. Pre-2008 slope ≈ 0.87; post-2008 slope ≈ 0.39 (QE era weakening, consistent with Notebook 02).

The main project frame is still Lucas (1996) / McCandless-Weber, not Lucas (1980).

## 11. Claim Tiers

| Component | Claim tier | Limitation |
|---|---|---|
| Long-run country averages | descriptive | no causal design |
| TWFE short-run association | associational | no causal identification |
| Pre/post-2008 split | descriptive timing | does not identify QE effect |
| COVID scatter | descriptive stress evidence | fiscal/supply/expectations confounds |
| Distributed lag | appendix scaffold | reduced-form association only |
| LP-IV | exploratory | weak instruments |
| Inflation targeting | exploratory | endogenous adoption |
| U.S. appendix | descriptive | one-country time series |

Forbidden claims:

- "QE caused low inflation."
- "COVID money growth alone caused 2021-2023 inflation."
- "Inflation targeting causally reduced pass-through."
- "The IV results identify causal monetary transmission."

## 12. Data And Code Provenance

| Notebook | Content |
|---|---|
| `01_lucas96_mcweber_replication.ipynb` | long-run country-average benchmark |
| `02_money_inflation_twfe.ipynb` | main short-run TWFE spine |
| `02b_money_inflation_exploratory.ipynb` | appendix diagnostics and cumulative lag scaffold |
| `03_short_run_lp_iv.ipynb` | LP-IV appendix |
| `04_did_it_event_study.ipynb` | inflation-targeting appendix |
| `05_lucas_us_appendix.ipynb` | U.S. Lucas (1980)-inspired appendix |

| Figure | Description |
|---|---|
| `between_within_decomposition.png` | country-average vs within-country annual association |
| `distributed_lag_cumulative_association.png` | cumulative distributed-lag association |
| `covid_money_inflation_scatter.png` | descriptive COVID cross-country scatter |
| `it_event_time_inflation.png` | inflation-targeting event-time chart |
| `it_slope_probe_coefficients.png` | inflation-targeting slope probe |
| `us_m2_inflation_two_eras.png` | U.S. pre/post-2008 scatter |
| `lucas_m1_scatter.png` | U.S. M1 vs inflation, Lucas filter β=0.9 |
| `lucas_m2_scatter.png` | U.S. M2 vs inflation and T-bill, Lucas filter β=0.9 |

## 13. Conclusion

The project's useful contribution is not a new causal macro design. It is a clean empirical contrast:

> Long-run cross-country money-inflation evidence remains strong through 2024, while the clean short-run within-country association weakens sharply after 2008.

That is enough for a portfolio project if the final presentation stays disciplined.
