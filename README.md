# Money Growth, Inflation, and GDP Growth

Single-report research repo with one arc on one panel:

1. Intro: Lucas (1980) — long-run cross-country money-inflation slope as benchmark.
2. Objective A — AVERAGE: Lucas-style country-mean estimate (descriptive).
3. Objective B — YoY: within-country short-run dynamics, FE + Phillips + LP-IV (exploratory).
4. Objective C — IT regime: inflation-targeting adoption as a moderator on the YoY slope (exploratory probe).

The headline contribution is the **wedge between the AVERAGE and YoY estimates**, with IT used to ask whether the regime explains the gap.

## Start Here

1. `LEARNING_PLAN.md` (7‑day ownership plan + repo map, if you want to learn the stack)
2. `01_research_question/research_target.md` (master contract)
3. `01_research_question/claim_boundary.md` (language guardrails)
4. `01_research_question/reading_guide.md` — pointer to docs + vault study guide + `reading_list.md` (literature themes)
5. `04_current_results/summary.md` (current results narrative)
6. `05_final_writing/report_draft.md` (single-report writeup)
7. `CODE_GUIDE.md` (technical runbook for code, tests, and folder rules)

## Executive Read (Coffee Chat)

- AVERAGE (Obj A): money growth and inflation are strongly associated in long-run cross-country data; GDP links are weaker.
- YoY (Obj B): within-country short-run estimates are smaller and sensitivity-dependent — that gap is the headline.
- IT regime (Obj C): adoption appears to moderate the YoY slope; reported as exploratory probe with caveats.
- Identification gates stay conservative throughout, so interpretation remains non-causal.
- Lucas (1980) leg (ii)—money vs **nominal interest rates**—is not in the cross-country CSV; extension options live in **`02_data/supporting/lucas_ii_nominal_rate_plan.md`** (stay on Path A if time‑boxed).

## Folder Management

- `01_research_question/`: contract docs and claim boundaries.
- `02_data/`: raw, analysis-ready, and supporting inputs.
- `03_analysis_notebooks/`: objective notebooks (`01` to `04`).
- `04_current_results/`: canonical outputs (tables, figures, summary).
- `05_final_writing/`: final report and companion writing.
- `90_reproduction_scripts/`: rebuild and graph-generation scripts.
- `tests/`: reproducibility and utility tests.

## Rebuild

```bash
python3 -m pip install -r 90_reproduction_scripts/requirements.txt
python3 90_reproduction_scripts/run_rebuild.py
python3 90_reproduction_scripts/build_graphs.py
python3 -m pytest tests -q
```

## Claim-Tier Policy

- `causal`: causal language allowed with explicit assumptions.
- `associational`: descriptive associations only.
- `exploratory`: pattern discussion only.

When `claim_tier != causal`, avoid policy-effect and counterfactual-effect claims.
