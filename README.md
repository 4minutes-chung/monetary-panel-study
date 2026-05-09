# Does the Quantity Theory Hold in the QE-to-COVID Era?

Cross-country macro panel, 160 countries, 1991–2024. The canonical money-inflation papers (McCandless & Weber 1995; De Grauwe & Polan 2005) predate QE and COVID. This project updates them.

## Headline finding

| Estimator | Full sample (160c) | Clean sample (123c, no hyperinflation) |
|---|---|---|
| Long-run country means (Obj A) | 0.952 | 0.524 |
| Short-run TWFE year-on-year (Obj B) | 0.665 | **0.040** (n.s.) |

In modern non-hyperinflationary economies, year-to-year money growth barely moves inflation. The QE decade in one number.

## Notebooks (run in order)

| Notebook | What |
|---|---|
| `01_lucas_replication` | Obj A — Lucas-style long-run country-mean scatter, full + clean samples, cross-country lending rate |
| `02_panel_fe_iv_baseline` | Obj B — TWFE baseline + Phillips curve, clean-sample robustness |
| `03_short_run_lp_iv` | Obj B — LP-IV horizons (appendix, weak instrument) |
| `04_did_it_event_study` | Obj C — IT adoption event study + slope-shift probe |
| `05_lucas_us_appendix` | Obj D — US M2 vs inflation and T-bill, 1960–2024, 5-yr MA |

## Data

- `02_data/analysis_ready/macro_growth_merged.csv` — main panel (columns: `Country Name, year, m2_growth, inflation, gdp_growth, sample_main, sample_low_inflation`)
- `02_data/raw/fred_*.csv` — US FRED series (M2, CPI, T-bill, M1)
- `02_data/supporting/intl_lending_rates.csv` — World Bank lending rates, 147 countries 1991–2024
- `02_data/supporting/it_adoption_dates.csv` — IT adoption dates (Roger 2010 + Hammond 2012)

## Sample flags

- `sample_main = 1` — all 160 countries
- `sample_low_inflation = 1` — 123 countries, drop if any year > 40% inflation (removes post-Soviet and Latin American hyperinflation episodes from the 1990s)

## Read first

1. `01_research_question/research_target.md` — research contract
2. `04_current_results/summary.md` — all key numbers
3. `05_final_writing/report_draft.md` — full report
4. `05_final_writing/executive_memo.md` — one-page summary

## Rebuild

```bash
# Data (if refreshing from World Bank / FRED)
python3 02_data/supporting/fetch_intl_rates.py

# Notebooks
jupyter nbconvert --to notebook --execute --inplace 03_analysis_notebooks/01_lucas_replication.ipynb
# ... repeat for 02–05
```

Claims stay non-causal while identification gates in `summary.md` fail.
