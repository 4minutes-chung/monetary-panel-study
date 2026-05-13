# Money Growth and Inflation After QE and COVID

160-country annual macro panel, 1991-2024.

Subtitle: long-run quantity-theory evidence survives; short-run within-country pass-through weakens after 2008.

This is a descriptive empirical audit, not a causal policy paper.

## Main Finding

| Question | Estimate | Read |
|---|---:|---|
| Long-run country averages, full sample | 0.952 | near one-for-one |
| Long-run country averages, clean sample | 0.524 | positive, smaller outside high-inflation episodes |
| Short-run TWFE, full sample | 0.855 | driven partly by high-inflation episodes |
| Short-run TWFE, clean sample | 0.096 | smaller but statistically significant |
| Regime split — low prior inflation (≤5%) | 0.053 | near zero in modern low-inflation environments |
| Regime split — extreme prior inflation (>40%) | 0.893 | near one-for-one in high-inflation regimes |

The useful tension is simple: countries with persistently higher broad money growth have higher long-run inflation, but year-to-year broad money growth does not map cleanly into year-to-year inflation in modern low-inflation regimes, especially after 2008. The short-run pass-through is state-dependent: it is near zero when prior-year inflation is low and near one-for-one when it is high.

## Notebooks

Run in order:

| Notebook | Role |
|---|---|
| `03_analysis_notebooks/01_lucas96_mcweber_replication.ipynb` | Lucas (1996) / McCandless-Weber long-run country-average update |
| `03_analysis_notebooks/02_money_inflation_twfe.ipynb` | Main short-run TWFE notebook: full/clean sample, pre/post-2008, compact robustness, outlier robustness, inflation-regime split, between-vs-within |
| `03_analysis_notebooks/02b_money_inflation_exploratory.ipynb` | Appendix diagnostics and cumulative distributed-lag scaffold |
| `03_analysis_notebooks/03_short_run_lp_iv.ipynb` | LP-IV appendix, directional only |
| `03_analysis_notebooks/04_did_it_event_study.ipynb` | Inflation-targeting appendix, exploratory only |
| `03_analysis_notebooks/05_lucas_us_appendix.ipynb` | Lucas (1980)-inspired U.S. appendix |

## Data

- `02_data/analysis_ready/macro_growth_merged.csv` - main cleaned panel.
- `02_data/DATA_PROVENANCE.md` - source map for checked-in data snapshots.
- `02_data/raw/worldbank_wdi_core_1991_2024.csv` - World Bank WDI source snapshot.
- `02_data/raw/fred_*.csv` - U.S. FRED source snapshots.
- `02_data/supporting/wb_controls_1991_2024.csv` - World Bank control variables.
- `02_data/supporting/bartik_instruments_1991_2024.csv` - appendix IV support file.
- `02_data/supporting/intl_lending_rates.csv` - World Bank lending-rate snapshot.
- `02_data/supporting/it_adoption_dates.csv` - inflation-targeting adoption dates.

Data files are checked-in CSV snapshots. This repo intentionally contains no standalone Python scripts.

## Rebuild

```bash
jupyter nbconvert --to notebook --execute --inplace 03_analysis_notebooks/01_lucas96_mcweber_replication.ipynb
jupyter nbconvert --to notebook --execute --inplace 03_analysis_notebooks/02_money_inflation_twfe.ipynb
jupyter nbconvert --to notebook --execute --inplace 03_analysis_notebooks/02b_money_inflation_exploratory.ipynb
jupyter nbconvert --to notebook --execute --inplace 03_analysis_notebooks/03_short_run_lp_iv.ipynb
jupyter nbconvert --to notebook --execute --inplace 03_analysis_notebooks/04_did_it_event_study.ipynb
jupyter nbconvert --to notebook --execute --inplace 03_analysis_notebooks/05_lucas_us_appendix.ipynb
```

## Claim Discipline

Safe claims:

- Broad money growth and inflation remain strongly associated across countries over long horizons.
- The annual within-country association is much weaker in the clean sample.
- The clean-sample short-run association is visible before 2008 and near zero afterward.
- Short-run pass-through is state-dependent: near zero when prior-year inflation is low, near one-for-one when it is high.
- COVID is a descriptive stress episode, not a causal design.
- IV and inflation-targeting results are exploratory appendices.

Do not claim that QE caused low inflation, COVID money growth alone caused 2021-2023 inflation, or inflation targeting causally reduced pass-through.
