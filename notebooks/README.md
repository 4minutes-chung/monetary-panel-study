# Notebook Organization

This folder is the notebook-first research flow.

## Notebook order

1. `phase_0_objA_lucas_replication.ipynb`
   - Obj A motivation.
   - Lucas-style long-run replication and descriptive cross-country pattern.
2. `phase_1_objB_baseline.ipynb`
   - Obj B baseline models.
   - FE + IV core estimates and first-stage read.
3. `phase_2_objB_short_run.ipynb`
   - Obj B short-run extension.
   - LP-IV dynamics (inflation horizons, GDP h=0).

## Outputs

- Phase 0 writes to `outputs/notebook_phase0/`
- Phase 1 writes to `outputs/notebook_phase1/`
- Phase 2 writes to `outputs/notebook_phase2/`

## Reproducibility note

For parity checks and publication-style exports, run:

- `python3 v2/run_v2_rebuild.py`
- `python3 v2/build_portfolio_graphs.py`
