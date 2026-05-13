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
| Full | 160 | 4,750 | all available country-years |
| Clean | 123 | 3,639 | drops countries with any annual inflation above 40 percent |

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
| Full | 0.665 | 0.0002 | 4,750 |
| Clean | 0.040 | 0.0621 | 3,639 |

Read:

The full sample has a positive short-run association. In the clean sample, the coefficient collapses to about 0.04 and is not robustly significant. This is the central contrast with the long-run country-average result.

## 5. Pre/Post-2008 Split

Same TWFE specification, clean sample only:

| Era | Coefficient | p-value | N obs | Countries |
|---|---:|---:|---:|---:|
| 1991-2007 | 0.1128 | <0.001 | 1,764 | 119 |
| 2008-2019 | 0.0005 | 0.8273 | 1,398 | 123 |
| 2020-2024 | -0.0139 | 0.6547 | 477 | 107 |

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
| Exclude 2020-2021, full sample | coefficient remains about 0.664 |
| Exclude 2020-2021, clean sample | coefficient remains about 0.040 |
| Driscoll-Kraay, full sample | coefficient 0.665, p about 0.003 |
| Driscoll-Kraay, clean sample | coefficient 0.040, p about 0.145 |

Read:

The clean-sample weakness is not just a COVID-year artifact. Wider Driscoll-Kraay inference also keeps the clean estimate non-robust.

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

| Horizon | Meaning |
|---|---|
| h=0 | same-year association |
| h=0+1 | same-year plus one lag |
| h=0+1+2 | same-year plus two lags |

Read:

The lag structure is interesting because annual money growth may not map into inflation only in the same calendar year. This belongs in the appendix unless developed into a cleaner extension.

## 10. Exploratory Appendices

### LP-IV

Notebook:

`03_analysis_notebooks/03_short_run_lp_iv.ipynb`

The IV results are directional only. Instruments fail the strong-IV threshold. Do not use these as causal evidence.

### Inflation Targeting

Notebook:

`03_analysis_notebooks/04_did_it_event_study.ipynb`

The post-adoption slope shift is about -0.485. This is exploratory because inflation-targeting adoption is endogenous.

### U.S. Appendix

Notebook:

`03_analysis_notebooks/05_lucas_us_appendix.ipynb`

This is Lucas (1980)-inspired descriptive evidence using U.S. FRED data and a 5-year moving average:

| Relationship | Slope | Read |
|---|---:|---|
| M2 growth -> inflation | 0.474 | borderline |
| M2 growth -> T-bill | 0.421 | directional only |

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
| `lucas_us_inflation.png` | U.S. M2 vs inflation, 5-year moving average |
| `lucas_us_tbill.png` | U.S. M2 vs T-bill, 5-year moving average |

## 13. Conclusion

The project's useful contribution is not a new causal macro design. It is a clean empirical contrast:

> Long-run cross-country money-inflation evidence remains strong through 2024, while the clean short-run within-country association weakens sharply after 2008.

That is enough for a portfolio project if the final presentation stays disciplined.
