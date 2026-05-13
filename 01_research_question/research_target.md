# Research Target Contract

This is the project contract. If another document conflicts with this file, this file wins.

## Research Question

Does broad money growth still predict inflation after QE and COVID once we separate:

1. long-run cross-country differences, and
2. short-run within-country annual timing?

The main frame is Lucas (1996) / McCandless-Weber (1995), not Lucas (1980). Lucas (1980) is kept only as a U.S. appendix.

## Main Claim

Long-run cross-country money-inflation evidence survives through 2024, but the clean short-run within-country association weakens sharply after 2008.

## Objectives

### Objective A - Long-Run Country Averages

Notebook: `03_analysis_notebooks/01_lucas96_mcweber_replication.ipynb`

Question: do countries with higher average broad money growth have higher average inflation?

Claim tier: descriptive.

### Objective B - Short-Run Within-Country TWFE

Notebook: `03_analysis_notebooks/02_money_inflation_twfe.ipynb`

Question: inside a country, do years with higher broad money growth have higher same-year inflation after country and year fixed effects?

Claim tier: associational, not causal.

Main outputs:

- full vs clean TWFE;
- pre/post-2008 TWFE split;
- compact robustness;
- between-vs-within figure.

### Objective B Appendix - Diagnostics And Lag Scaffold

Notebook: `03_analysis_notebooks/02b_money_inflation_exploratory.ipynb`

Role:

- Driscoll-Kraay sensitivity;
- cumulative distributed-lag association scaffold.

No Phillips/output-gap block. No active IV diagnostics.

### Objective C - Inflation Targeting

Notebook: `03_analysis_notebooks/04_did_it_event_study.ipynb`

Question: does the short-run money-inflation association differ around inflation-targeting adoption?

Claim tier: exploratory only. Adoption is endogenous.

### Objective D - U.S. Appendix

Notebook: `03_analysis_notebooks/05_lucas_us_appendix.ipynb`

Role: Lucas (1980)-inspired U.S. low-frequency appendix using FRED M2, CPI, and T-bill data.

Claim tier: descriptive.

## Claim Tier Discipline

Safe claims:

- broad money growth and inflation remain strongly associated across countries over long horizons;
- short-run within-country association is weak in the clean sample;
- the clean short-run association is visible before 2008 and near zero afterward;
- COVID is descriptive stress evidence only;
- IV and inflation targeting are exploratory appendices.

Forbidden claims:

- QE caused low inflation;
- COVID money growth alone caused 2021-2023 inflation;
- inflation targeting causally reduced pass-through;
- IV identifies causal monetary transmission.

## Canonical Execution Path

1. Read `README.md`.
2. Read `02_data/DATA_PROVENANCE.md`.
3. Run notebooks in order:
   - `01_lucas96_mcweber_replication.ipynb`
   - `02_money_inflation_twfe.ipynb`
   - `02b_money_inflation_exploratory.ipynb`
   - `03_short_run_lp_iv.ipynb`
   - `04_did_it_event_study.ipynb`
   - `05_lucas_us_appendix.ipynb`
4. Use `04_current_results/summary.md` only as a numeric snapshot.
5. Write final prose from the claim tiers above, not from exploratory notebook chronology.

## Definition Of Done

A cycle is done when:

1. current notebooks run without errors;
2. results in memo/report match notebook outputs;
3. every figure/table is labeled as main, appendix, or archive;
4. no causal claim is made without identification;
5. stale notebook names and stale figure references are removed.
