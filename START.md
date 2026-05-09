# Start — learn this repo

**Contract:** `01_research_question/research_target.md` · **numbers:** `04_current_results/summary.md` · **papers:** `01_research_question/reading_list.md`

## 7 days (~3 hr/day)

| Day | Do |
|-----|-----|
| 1 | `pip install -r 90_reproduction_scripts/requirements.txt` → run `03_analysis_notebooks/00_data_refresh_and_rebuild.ipynb` (or `run_rebuild.py`) → `pytest tests`. Read `research_target`, `claim_boundary`, `summary.md`. Run `03_analysis_notebooks/01_lucas_replication.ipynb`. Papers **1–2** from `reading_list.md`. |
| 2 | Notebook **`02`** through FE/IV. Papers **3–4**. |
| 3 | Notebook **`02`** Phillips cell + open `phillips_*.csv`. Papers **5–7**. |
| 4 | `audit_scorecard.csv`, `spec_stability_table.csv`, `placebo_tests.csv`. Notebook **`03`**. Papers **8**, **17–18**. |
| 5 | **`04`** IT notebook + `it_adoption_dates.csv`. Papers **9–13**, optional **14–16**. |
| 6 | `report_draft.md`, trace 3 numbers from `summary.md` to CSVs. Catch-up reading. |
| 7 | 60s pitch + **12 questions** below, no notes. |

Fallback week: do days **1, 3, 4, 7** only.

## Five numbers (after rebuild)

Open `summary.md` — conservative F-stat, drift, placebo line, Phillips RMSE story, sample line.

## Twelve questions (practice cold)

1. Lucas (1980) vs Obj A?  
2. AVG vs YoY wedge?  
3. IV first stage — value + why gate fails?  
4. Drift — what is it?  
5. Placebo hit — trash project?  
6. Money vs output gap in forecast?  
7. Country FE vs year FE?  
8. What is LP?  
9. Why Holm on horizons?  
10. Why Obj C not causal IT?  
11. Sample (countries, years, rows)?  
12. One month more — what would you fix?

## Tiny map

`01` = Obj A · `02`+`03` = Obj B · `04` = Obj C · outputs = `04_current_results/`

Lucas interest-rate leg: not in panel — `02_data/supporting/lucas_ii_nominal_rate_plan.md`
