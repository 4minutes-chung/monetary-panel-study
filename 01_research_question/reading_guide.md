# Reading Guide

This repo is now organized for economics reading first and reproduction second.

## Fast Reading Order

1. `00_START_HERE.md`
2. `01_research_question/research_target.md`
3. `01_research_question/claim_boundary.md`
4. `04_current_results/summary.md`
5. `04_current_results/tables/phase1_audit/audit_scorecard.csv`
6. `04_current_results/tables/phase1_audit/core_model_results.csv`
7. `05_final_writing/executive_memo.md`
8. `06_study_notes/econometric_caveats.md`

## What We Learned

- Inflation and money growth show a strong positive association in core specs.
- GDP growth effects are weaker and less robust.
- Identification remains sensitive around first-stage thresholds.
- Conservative gates currently require cautious, associational interpretation.

Current diagnostic snapshot:

- Recommendation: `GO_PIVOT_SHORT_RUN`
- Conservative first-stage stat: `3.8016`
- Conservative first-stage p-value: `0.0512`
- Clustering relevance agreement: `False`

## Folder Map

- `01_research_question/`: question, contract, claim boundary, and this guide.
- `02_data/raw/`: source data downloads.
- `02_data/analysis_ready/`: merged analysis panel.
- `02_data/supporting/`: controls, instruments, region map, data source notes.
- `03_analysis_notebooks/`: three economics notebooks.
- `04_current_results/`: current summary, tables, and figures.
- `05_final_writing/`: memo, technical appendix, report draft, policy brief.
- `06_study_notes/`: learning notes and future analysis questions.
- `90_reproduction_scripts/`: optional rebuild scripts.

## Rebuild Path

From project root:

```bash
python3 -m pip install -r 90_reproduction_scripts/requirements.txt
python3 90_reproduction_scripts/run_rebuild.py
python3 90_reproduction_scripts/build_graphs.py
```

## Claim Discipline

- `01_research_question/research_target.md` is the contract.
- `01_research_question/claim_boundary.md` is the plain-English guardrail.
- `04_current_results/tables/phase1_audit/audit_scorecard.csv` is the gate table.
- Final writing should cite `04_current_results/`.

## Maintenance Checklist

1. Update analysis or data.
2. Rerun `90_reproduction_scripts/run_rebuild.py`.
3. Rerun `90_reproduction_scripts/build_graphs.py`.
4. Update `05_final_writing/` only after checking the scorecard.
5. Keep stale material out of the active reading path.
