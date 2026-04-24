# Reading Guide: Learning, Process, Assumptions, Files, and Git Hygiene

## 1. Why this guide exists

This is the single detailed onboarding and maintenance guide.

Use this file to understand:

- what we learned,
- how the repo workflow runs,
- what assumptions limit interpretation,
- what each major file/folder is for,
- what is tracked vs ignored in `.gitignore`.

## 2. Fast reading order (10-minute version)

1. `RESEARCH_TARGET.md` (contract, gate logic, claim boundary)
2. `README.md` (coffee-chat narrative and graph-first flow)
3. `v2/outputs/V2_SUMMARY.md` (latest numeric checkpoint)
4. `v2/outputs/phase1_audit_v2/tables/audit_scorecard_v2.csv`
5. `v2/outputs/phase2_short_run_v2/tables/lp_iv_primary_results_v2.csv`
6. `deliverables/final_package/REPORT_DRAFT_IN_PROGRESS.md`

## 3. What we learned (current state)

- Inflation and money growth show a strong positive association in core specs.
- GDP growth effects are weaker and less robust.
- Identification remains sensitive around first-stage thresholds.
- Conservative clustering-aware gates currently point to cautious interpretation.

Current conservative diagnostic snapshot (see `v2/outputs/V2_SUMMARY.md`):

- Recommendation: `GO_PIVOT_SHORT_RUN`
- Conservative first-stage stat: `3.8016`
- Conservative first-stage p-value: `0.0512`
- Clustering relevance agreement: `False`

## 4. Process map (how the analysis is produced)

### 4.1 Canonical run path

From project root:

1. `python3 -m pip install -r requirements.txt`
2. Run notebook chain:
   - `notebooks/phase_0_objA_lucas_replication.ipynb`
   - `notebooks/phase_1_objB_baseline.ipynb`
   - `notebooks/phase_2_objB_short_run.ipynb`
3. Optional parity refresh:
   - `python3 v2/run_v2_rebuild.py`
   - `python3 v2/build_portfolio_graphs.py`

### 4.2 Why notebook-first + script parity

- Notebooks are the readable research story.
- `v2/` scripts are reproducibility backstop and consistency checks.

## 5. Assumptions and boundaries

- Baseline interpretation is associational.
- Causal language is limited unless conservative relevance gate is passed.
- Preferred first-stage gate uses conservative clustering rule:
  - stat = `min(country, country_year)`
  - p = `max(country, country_year)`
- Strong-IV label requires first-stage stat `>= 10.0`.
- Permutation placebo uses empirical two-sided randomization p-value.

## 6. File map (what each major area is for)

## 6.1 Root files

- `RESEARCH_TARGET.md`: master contract.
- `README.md`: quick reading flow.
- `READING_GUIDE.md`: this deep guide.
- `RECOVERY_STEP0_GIT_TRIAGE.md`: historical recovery record.
- `requirements.txt`: pinned Python dependencies.
- `macro_growth_merged.csv`, `m2_raw.csv`, `cpi_raw.csv`, `gdp_raw.csv`: active run inputs.

## 6.2 Core directories

- `notebooks/`: three-phase research storyline.
- `v2/`: script parity pipeline and graph builder.
- `v2/outputs/`: canonical script outputs (summary, tables, figures).
- `deliverables/final_package/`: memo, appendix, and report draft.
- `docs/`: active technical notes used by current workflow.
- `outputs/phase*`: historical references (non-canonical for current claims).

Lean-mode note:

- Historical notebooks/reports/references are not kept in the working tree anymore.
- If needed, recover them from git history rather than maintaining archive copies in the active repo.

## 6.3 High-priority outputs to cite

- `v2/outputs/V2_SUMMARY.md`
- `v2/outputs/phase1_audit_v2/tables/core_model_results_v2.csv`
- `v2/outputs/phase1_audit_v2/tables/first_stage_strength_v2.csv`
- `v2/outputs/phase1_audit_v2/tables/inference_sensitivity_v2.csv`
- `v2/outputs/phase1_audit_v2/tables/placebo_tests_v2.csv`
- `v2/outputs/phase1_audit_v2/tables/audit_scorecard_v2.csv`
- `v2/outputs/phase2_short_run_v2/tables/lp_iv_primary_results_v2.csv`
- `v2/outputs/portfolio_graphs/`

## 7. Git and .gitignore policy

Current `.gitignore` intent:

- Ignore local environment/cache noise:
  - `.venv/`, `__pycache__/`, `*.pyc`, `.pytest_cache/`, `.ruff_cache/`
- Ignore notebook checkpoint noise:
  - `.ipynb_checkpoints/`
- Ignore OS noise:
  - `.DS_Store`
- Ignore local Node installs:
  - `node_modules/`
- Ignore LaTeX build artifacts:
  - `*.aux`, `*.log`, `*.out`
- Ignore notebook-export output folders used as local rerun artifacts:
  - `outputs/notebook_phase0/`, `outputs/notebook_phase1/`, `outputs/notebook_phase2/`

Important tracking convention:

- `v2/outputs/` is intentionally tracked as canonical reproducibility evidence.
- Legacy `outputs/phase*` can exist for historical comparison, but should not drive current claim text.

## 8. Cleanup actions completed in this simplification wave

- Removed redundant pointer doc: `START_HERE.md`.
- Removed stale duplicate plan doc: `v2/V2_PLAN.md` (its purpose is now covered by `RESEARCH_TARGET.md` + this guide).
- Removed the tracked `archive/` tree to keep active repo surface minimal (history retained in git).
- Removed redundant legacy docs not needed for canonical run interpretation.
- Removed tracked generated artifacts:
  - `outputs/phase1_audit/phase1_audit_short_report.aux`
  - `outputs/phase1_audit/phase1_audit_short_report.log`
- Updated active docs to reference the new guide as the long-form onboarding memory.

## 9. Maintenance checklist for future edits

1. Update code first, then rerun canonical outputs.
2. Update `v2/outputs/V2_SUMMARY.md` via rebuild, not manual editing.
3. Keep narrative claims aligned to conservative gate values.
4. If docs conflict, `RESEARCH_TARGET.md` wins.
5. Keep onboarding centralized here; avoid spawning duplicate start docs.
