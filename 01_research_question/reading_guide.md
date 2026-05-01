# Reading Guide

## Read the repo in this order

1. `README.md` — project arc and start-here pointers.
2. `01_research_question/research_target.md` — master contract (Lucas → AVERAGE → YoY → IT regime).
3. `01_research_question/claim_boundary.md` — language guardrails per objective.
4. `04_current_results/summary.md` — current results narrative with diagnostics.
5. `LEARNING_PLAN.md` — 7‑day plan and repo-benefits summary at repo root.
6. `05_final_writing/report_draft.md` — single-report writeup, 7 sections.
7. `CODE_GUIDE.md` — technical runbook for code, tests, and folder rules.

## Read the literature (NotebookLM-ready)

- **Thematic bibliography (tracked in-repo):** `01_research_question/reading_list.md`
- **7‑day path + interview script (personal vault):** `/Users/stevenchung/Steven_Chung/Lessons across projects/Cross_Country_Monetary_Project/STUDY_GUIDE_2026-04-29.md`

Use `reading_list.md` for citations by topic; use the vault study guide for pacing and rehearsal.

## Rebuild

```bash
python3 90_reproduction_scripts/run_rebuild.py
python3 90_reproduction_scripts/build_graphs.py
python3 -m pytest tests -q
```
