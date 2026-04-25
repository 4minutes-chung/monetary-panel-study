# Notebook Organization

This folder contains the readable economics analysis notebooks.

## Notebook order

1. `01_lucas_replication.ipynb`
   - Obj A motivation.
   - Lucas-style long-run replication and descriptive cross-country pattern.
2. `02_panel_fe_iv_baseline.ipynb`
   - Obj B baseline models.
   - FE + IV core estimates and first-stage read.
3. `03_short_run_lp_iv.ipynb`
   - Obj B short-run extension.
   - LP-IV dynamics (inflation horizons, GDP h=0).

## Outputs

- Current canonical outputs are collected in `04_current_results/`.
- Notebook-local exports, if regenerated, should be treated as working artifacts until checked against the current results.

## Reproducibility note

For parity checks and publication-style exports, run:

- `python3 90_reproduction_scripts/run_rebuild.py`
- `python3 90_reproduction_scripts/build_graphs.py`
