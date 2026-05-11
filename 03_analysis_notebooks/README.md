# Notebook Organization

This folder contains the readable economics analysis notebooks.

## Notebook order

1. `01_lucas_replication.ipynb`
   - Obj A motivation.
   - Lucas-style long-run replication and descriptive cross-country pattern.
2. `02_panel_fe_iv_baseline.ipynb`
   - Obj **B** YoY baseline: TWFE, diagnostics, Phillips block, sub-periods, COVID scatter, distributed lag, and core figures.
3. `03_short_run_lp_iv.ipynb`
   - Obj **B** appendix: LP-IV dynamics (fixed sample, Holm on inflation horizons, IT stratification). Directional only.
4. `04_did_it_event_study.ipynb`
   - Obj **C** exploratory: IT event-study and slope-shift probe (caveat-first).
5. `05_lucas_us_appendix.ipynb`
   - Obj **D** appendix: US FRED low-frequency Lucas-style check.

Old "Phase 0/1/2" labels in cells = `01` / `02` / `03`; `04` = Obj C.

## Outputs

- Current canonical outputs are collected in `04_current_results/` (preferred for claims).
- Notebook-local exports, if regenerated, land under `03_analysis_notebooks/exports/phase0|phase1|phase2/` (gitignored working copies).

## Reproducibility note

Run notebooks `01` through `05` top-to-bottom. Each notebook finds the project root from
`02_data/analysis_ready/macro_growth_merged.csv` and writes current figures/tables into
`04_current_results/`.
