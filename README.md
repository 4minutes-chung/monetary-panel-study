# Money Growth and Inflation After QE and COVID

160-country annual macro panel, 1991-2024.

This is a descriptive empirical audit, not a causal policy paper. The project separates two objects that are often blurred together: long-run cross-country money-inflation differences and short-run annual within-country pass-through.

## Main Result

Long-run quantity-theory evidence remains strong across countries. In contrast, the clean annual within-country association is small and becomes near zero after 2008.

<img src="04_current_results/figures/between_within_decomposition.png" width="800">

| Question | Coefficient | Interpretation |
|---|---:|---|
| Long-run cross-country, full sample | 0.952 | Near one-for-one over 30 years |
| Long-run cross-country, clean sample | 0.524 | Positive outside high-inflation episodes |
| Short-run within-country, full sample | 0.855 | Driven heavily by extreme-inflation years |
| Short-run within-country, clean sample | 0.096 | Weak annual pass-through |

## Additional Figures

- Pre/post-2008 clean-sample TWFE: `04_current_results/figures/pre_post_2008_coef_plot.png`
- Prior-inflation regime split: `04_current_results/figures/regime_split_coef_plot.png`
- COVID cross-country stress episode: `04_current_results/figures/covid_money_inflation_scatter.png`
- Distributed-lag appendix: `04_current_results/figures/distributed_lag_cumulative_association.png`
- Inflation-targeting appendix: `04_current_results/figures/it_slope_probe_coefficients.png`
- U.S. Lucas-style appendix: `04_current_results/figures/us_m2_inflation_two_eras.png`

## Files

- Final memo: [`money_inflation_audit_report.pdf`](money_inflation_audit_report.pdf)
- Memo source: [`money_inflation_audit_report.tex`](money_inflation_audit_report.tex)
- Main panel: `02_data/analysis_ready/macro_growth_merged.csv`
- Data notes: `02_data/DATA_PROVENANCE.md`, `02_data/UNITS_REGISTER.md`
- Notebooks: `03_analysis_notebooks/`
- Figures and tables: `04_current_results/`

## Reproduce

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run notebooks in order:

```bash
jupyter nbconvert --to notebook --execute --inplace 03_analysis_notebooks/01_lucas96_mcweber_replication.ipynb
jupyter nbconvert --to notebook --execute --inplace 03_analysis_notebooks/02_money_inflation_twfe.ipynb
jupyter nbconvert --to notebook --execute --inplace 03_analysis_notebooks/02b_money_inflation_exploratory.ipynb
jupyter nbconvert --to notebook --execute --inplace 03_analysis_notebooks/03_short_run_lp_iv.ipynb
jupyter nbconvert --to notebook --execute --inplace 03_analysis_notebooks/04_did_it_event_study.ipynb
jupyter nbconvert --to notebook --execute --inplace 03_analysis_notebooks/05_lucas_us_appendix.ipynb
```

Data snapshots are checked into `02_data/`; regenerated outputs write to `04_current_results/`.
