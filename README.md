# Money Growth, Inflation, and GDP Growth

This is an economics research folder, organized for reading and later analysis.

Start here: `00_START_HERE.md`.

## Coffee Chat Version

- Money growth and inflation move together strongly in this country panel.
- GDP growth links are weaker and not robust.
- Causal language stays limited because the conservative identification gate fails.

## Clean Reading Flow

1. `00_START_HERE.md`
2. `01_research_question/research_target.md`
3. `04_current_results/summary.md`
4. `04_current_results/tables/phase1_audit/audit_scorecard.csv`
5. `04_current_results/tables/phase1_audit/core_model_results.csv`
6. `05_final_writing/executive_memo.md`
7. `06_study_notes/econometric_caveats.md`

## Folder Map

- `01_research_question/`: research question, claim boundary, reading guide.
- `02_data/`: raw, analysis-ready, and supporting data.
- `03_analysis_notebooks/`: the three economics notebooks.
- `04_current_results/`: current tables, figures, and summary.
- `05_final_writing/`: memo, appendix, report draft, policy brief.
- `06_study_notes/`: notes for learning and later analysis.
- `90_reproduction_scripts/`: optional scripts to rebuild results.

## Optional Rebuild

```bash
python3 -m pip install -r 90_reproduction_scripts/requirements.txt
python3 90_reproduction_scripts/run_rebuild.py
python3 90_reproduction_scripts/build_graphs.py
python3 -m pytest tests -q
```
