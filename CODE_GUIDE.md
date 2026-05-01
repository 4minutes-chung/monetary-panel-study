# CODE GUIDE

This is the technical runbook for working in this repo.

## 1) Source of truth

- Research contract: `01_research_question/research_target.md`
- Claim language guardrail: `01_research_question/claim_boundary.md`
- Current output narrative: `04_current_results/summary.md`

If docs conflict, `research_target.md` wins.

## 2) Core workflow

From repo root:

```bash
python3 -m pip install -r 90_reproduction_scripts/requirements.txt
python3 90_reproduction_scripts/run_rebuild.py
python3 90_reproduction_scripts/build_graphs.py
python3 -m pytest tests -q
```

## 3) Notebook responsibilities

- `03_analysis_notebooks/01_lucas_replication.ipynb`
  - Objective A long-run cross-country descriptive facts.
- `03_analysis_notebooks/02_panel_fe_iv_baseline.ipynb`
  - FE baseline, IV TWFE core, Phillips block (`inflation_l1`, `output_gap_hp`, `m2_growth`), and optional holdout inflation forecast outputs next to canonical `phillips_*.csv` in `tables/phase1_audit/` after rebuild.
- `03_analysis_notebooks/03_short_run_lp_iv.ipynb`
  - LP-IV dynamics with fixed-sample lock and Holm correction.
  - IT stratified comparison is exploratory.
- `03_analysis_notebooks/04_did_it_event_study.ipynb`
  - Objective C exploratory IT event-study and slope probe.

## 4) Output contract

Canonical generated outputs live in:

- `04_current_results/summary.md`
- `04_current_results/tables/phase1_audit/`
- `04_current_results/tables/short_run_lp/`
- `04_current_results/figures/`

Do not hand-edit generated CSVs unless explicitly required; regenerate via scripts.

**Notebook outputs**: Code cells save working exports under `03_analysis_notebooks/exports/phase0|phase1|phase2/` (ignored by Git). Previously saved cell stdout in some notebooks referenced legacy `outputs/notebook_*` paths; those were cleared — **re-run notebooks** locally if you need inline output again.

## 5) Folder hygiene rules

- Keep runnable code in notebooks/scripts, not in study-note markdown.
- Keep one report narrative in `05_final_writing/report_draft.md`.
- Avoid duplicate start docs and stale entrypoints.
- If a top-level doc is removed, remove all references in `README.md` and guide docs.

## 6) Git ignore policy

`.gitignore` is set to exclude:

- Python cache, notebook checkpoints, local envs.
- Notebook export folders (`03_analysis_notebooks/exports/`).
- Local OS/node noise and LaTeX build artifacts.

If new generated folders are introduced, add them to `.gitignore` only if they are non-canonical artifacts.

## 7) Claim discipline in code and writing

- Objective A language: descriptive.
- Objective B language: exploratory.
- Objective C language: exploratory probe, not causal.
- Never upgrade interpretation beyond current diagnostic gates.
