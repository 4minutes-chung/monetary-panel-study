# Notebook Organization

This folder contains the readable economics analysis notebooks.

## Notebook order

1. `01_lucas_replication.ipynb`
   - Obj A motivation.
   - Lucas-style long-run replication and descriptive cross-country pattern.
2. `02_panel_fe_iv_baseline.ipynb`
   - Obj **B** YoY baseline: TWFE FE + IV plus Phillips (+ output gap + money), holdout inflation forecast notebook block; aligns with canonical `tables/phase1_audit/phillips_*.csv` after rebuild.
3. `03_short_run_lp_iv.ipynb`
   - Obj **B** continuation: LP-IV dynamics (fixed sample, Holm on inflation horizons, IT stratification).
4. `04_did_it_event_study.ipynb`
   - Obj **C** exploratory: IT event-study and slope-shift probe (caveat-first).

**Naming note:** Notebooks title cells may still say "Phase 0/1/2" for historical numbering. Map: Phase 0 = Obj A notebook `01`; Phase 1 = notebook `02` (YoY baseline inside Obj B); Phase 2 = notebook `03` (LP‑IV remains Obj B); notebook `04` = Obj C.

## Outputs

- Current canonical outputs are collected in `04_current_results/` (preferred for claims).
- Notebook-local exports, if regenerated, land under `03_analysis_notebooks/exports/phase0|phase1|phase2/` (gitignored working copies).

## Reproducibility note

For parity checks and publication-style exports, run:

- `python3 90_reproduction_scripts/run_rebuild.py`
- `python3 90_reproduction_scripts/build_graphs.py`
