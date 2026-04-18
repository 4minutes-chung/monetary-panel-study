# Start Here (Notebook-First Workflow)

## 1. Canonical Path

This repository is currently notebook-first for research storytelling, with script parity checks.

Run from project root:

1. `python3 -m pip install -r requirements.txt`
2. Run `notebooks/phase_0_objA_lucas_replication.ipynb` (Run All)
3. Run `notebooks/phase_1_objB_baseline.ipynb` (Run All)
4. Run `notebooks/phase_2_objB_short_run.ipynb` (Run All)
5. Optional parity check:
   - `python3 v2/run_v2_rebuild.py`
   - `python3 v2/build_portfolio_graphs.py`

## 2. Research Question

Across countries, how strongly is money growth associated with inflation and GDP growth, and what can be claimed under credible identification checks?

## 3. Identification Gate Framework (V2)

Use a two-tier first-stage interpretation:

- Relevance gate: clustered first-stage Wald chi2(1) > 3.8415 and p < 0.05.
- Strong-IV label: first-stage statistic >= 10.0.

This keeps relevance and strength distinct and avoids over-claiming when instruments are only marginally strong.

## 4. Claim Boundary

Inflation association is robust across specifications, but causal interpretation remains limited while first-stage strength is weak-to-moderate.

## 5. Primary Outputs To Inspect

- `outputs/notebook_phase0/`
- `outputs/notebook_phase1/`
- `outputs/notebook_phase2/`
- `v2/outputs/V2_SUMMARY.md`
- `v2/outputs/phase1_audit_v2/tables/audit_scorecard_v2.csv`
- `v2/outputs/phase2_short_run_v2/tables/lp_iv_primary_results_v2.csv`
- `v2/outputs/portfolio_graphs/`

## 6. Notebook Map

- Notebook 1 (Obj A motivation): `notebooks/phase_0_objA_lucas_replication.ipynb`
- Notebook 2 (Obj B baseline): `notebooks/phase_1_objB_baseline.ipynb`
- Notebook 3 (Obj B short-run): `notebooks/phase_2_objB_short_run.ipynb`

## 7. Legacy And Recovery Status

- `outputs/phase1*` and `outputs/phase2_short_run*` are historical references, not canonical claim sources.
- Legacy tracked notebooks have been archived under `archive/notebooks_legacy/` (history preserved).
- Step 0 triage decision is recorded in `RECOVERY_STEP0_GIT_TRIAGE.md`.
