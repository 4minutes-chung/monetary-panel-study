# Current Results Summary

Working numeric snapshot. Narrative source of truth: `05_final_writing/report_draft.md`.

## Data

- 160 countries, 1991-2024, 4,750 country-years.
- Clean sample: 123 countries, dropping countries with any annual inflation above 40 percent.
- Main variables: `m2_growth`, `inflation`, `gdp_growth`.

## Long-Run Country Averages

Countries require at least 30 observations.

| Sample | Countries | Slope: M2 growth -> inflation | p-value | R2 |
|---|---:|---:|---:|---:|
| Full | 108 | 0.952 | 4.4e-50 | 0.877 |
| Clean | 83 | 0.524 | 6.8e-15 | 0.529 |

Read: long-run cross-country money-inflation evidence survives through 2024, but the slope is lower outside high-inflation episodes.

## Short-Run TWFE

Model:

```text
inflation_it = country FE + year FE + beta * m2_growth_it + error_it
```

| Sample | Coef | p-value | N |
|---|---:|---:|---:|
| Full | 0.665 | 0.0002 | 4,750 |
| Clean | 0.040 | 0.0621 | 3,639 |

Read: the annual within-country association is much weaker in the clean sample.

## Pre/Post-2008 TWFE

Clean sample only.

| Era | Coef | p-value | N obs | Countries |
|---|---:|---:|---:|---:|
| 1991-2007 | 0.1128 | <0.001 | 1,764 | 119 |
| 2008-2019 | 0.0005 | 0.8273 | 1,398 | 123 |
| 2020-2024 | -0.0139 | 0.6547 | 477 | 107 |

Read: the short-run clean-sample association is visible before 2008 and near zero afterward.

## Compact Robustness

| Check | Result |
|---|---|
| Exclude 2020-2021, full sample | coef about 0.664 |
| Exclude 2020-2021, clean sample | coef about 0.040 |
| Driscoll-Kraay full sample | coef 0.665, p about 0.003 |
| Driscoll-Kraay clean sample | coef 0.040, p about 0.145 |

Read: clean-sample weakness is not just a COVID-year artifact.

## Between-Vs-Within Figure

Figure: `04_current_results/figures/between_within_decomposition.png`

Purpose: show why long-run cross-country averages and annual within-country TWFE can produce different slopes.

## COVID Descriptive Scatter

| Statistic | Value |
|---|---:|
| Countries | 102 |
| Slope: M2 2020-2021 -> inflation 2021-2023 | 0.494 |
| p-value | <0.0001 |
| R2 | 0.255 |

Read: positive cross-country association in the COVID period, descriptive only.

## Distributed-Lag Appendix

Figure: `04_current_results/figures/distributed_lag_cumulative_association.png`

Current role: appendix/scaffold.

Interpretation: reduced-form cumulative distributed-lag association, not a causal impulse response.

## Exploratory Appendices

| Appendix | Result | Claim tier |
|---|---|---|
| LP-IV | weak/directional instruments | exploratory only |
| Inflation targeting | post-adoption slope shift about -0.485 | exploratory only; endogenous adoption |
| U.S. appendix | M2 -> inflation slope about 0.474 | descriptive only |

## Claim Discipline

Safe headline:

> Long-run cross-country money-inflation evidence remains strong through 2024, while the clean short-run within-country association weakens sharply after 2008.

Forbidden claims:

- QE caused low inflation.
- COVID money growth alone caused 2021-2023 inflation.
- Inflation targeting causally reduced pass-through.
- IV results identify causal monetary transmission.
