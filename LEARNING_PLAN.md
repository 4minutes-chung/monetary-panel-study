# Monetary Panel 

This file captures the agreed framing: **what the project is**, **why a 7‑day plan**, **benefits**, **how each day ties to folders/code**, and **where canonical docs live**.

---

## What it is (one paragraph)

This repo is a **cross-country monetary panel workflow** (163 countries, 1991–2020): **Lucas-style long‑run country means (Obj A)** → **year‑on‑year within‑country dynamics: FE / IV / Phillips curve / holdout inflation forecast / LP‑IV (Obj B)** → **inflation‑targeting regime probes with explicit caveats (Obj C)**. Empirical results largely **replicate standard macro literature**; the distinguishing piece is **discipline**: conservative gates (first stage, drift, placebo), bounded claim tiers, reproducible rebuild (`run_rebuild.py` + tests), and an explicit **long‑run vs short‑run wedge** story—not a novelty claim on causal policy effects.

---

## Why a 7‑day plan

You already built the code. The gap is **retrieval under pressure** (interviews, Q&A), not more features. Seven days (~3 hrs/day ≈ **21 hours**) converts “I coded it” into “I defend any number without notes.” Daily **artifacts** (paragraph, diagram, slide, memorized diagnostics, recorded pitch) prove progress.

---

## Benefits (payoff ladder)

| Horizon | Benefit |
|---------|---------|
| **Day 8** | 60‑sec pitch + 12 hostile questions cold; refusal of causal hype with named diagnostics |
| **1–3 months** | One sharp interview/portfolio narrative; audit habit portable to Macro Risk / HSI / other repos |
| **3–12 months** | 8‑paper econ canon in active recall; reuse same retrieval routine on other projects in **hours** instead of weeks |
| **Beyond** | Habit: build → gate → bound claims → ship (fewer brittle “everything is significant” projects) |

**Not promised:** new economics; a causal IT paper; journals. **Promised:** defensible narration + repeatable study method.

---

## Repo map — objectives → notebooks → outputs

| Objective | Meaning | Notebook | Main outputs |
|-----------|---------|-----------|---------------|
| **A — AVERAGE** | Long‑run Lucas‑style cross‑country slopes | `03_analysis_notebooks/01_lucas_replication.ipynb` | Notebook exports (`03_analysis_notebooks/exports/phase0/`), figure `04_current_results/figures/13_country_means_m2_vs_inflation.png` |
| **B — YoY** | Within‑country FE/IV + Phillips + forecast + LP‑IV | `02_panel_fe_iv_baseline.ipynb`, `03_short_run_lp_iv.ipynb` | `04_current_results/tables/phase1_audit/*.csv` (incl. `phillips_*.csv`), `tables/short_run_lp/*.csv`, figures e.g. `06_*`, `08_*`, `14_phillips_forecast.png` |
| **C — IT regime** | Exploratory event‑study / slope probes | `04_did_it_event_study.ipynb` | Narrative + tables as run; IT stratified LP: `lp_iv_it_stratified.csv` |

**Contract (language + scope):** `01_research_question/research_target.md`, `01_research_question/claim_boundary.md`  
**Current numbers:** `04_current_results/summary.md`  
**Report:** `05_final_writing/report_draft.md`  
**Repro:** `90_reproduction_scripts/run_rebuild.py`, `build_graphs.py`, `tests/`

**Data:** `02_data/analysis_ready/macro_growth_merged.csv`, `02_data/supporting/*`

**Personal study vault (outside this repo):**  
`~/Steven_Chung/Lessons across projects/Cross_Country_Monetary_Project/STUDY_GUIDE_2026-04-29.md` (reading list, interview script, deeper notes)

---

## 7‑day plan (concrete)

~3 hours/day. Each day has **read → repo step → artifact**.

| Day | Read (e.g. NotebookLM) | Repo | Daily artifact |
|-----|------------------------|------|----------------|
| 1 | Lucas (1980); Sargent–Surico (2011) | `summary.md` + `01_lucas_replication.ipynb` | 3 lines: what AVG is; why drift matters |
| 2 | Galí–Gertler (1999) | `02_panel_fe_iv_baseline.ipynb` (cells 0–6) + `core_model_results.csv` | Sketch: FE → IV → first‑stage |
| 3 | Atkeson–Ohanian (2001); Stock–Watson (2007) | Notebook 02 Phillips/forecast cell + `phillips_results.csv`, `phillips_forecast_skill.csv`, `14_phillips_forecast.png` | One slide: money vs gap on holdout |
| 4 | Jordà (2005); Andrews–Stock–Sun (2019) | `03_short_run_lp_iv.ipynb` + `lp_iv_primary_results.csv` | Memorize: F≈3.80, drift≈0.875, placebo hit — what each implies |
| 5 | Roger (2010); Hammond (2012); CS (2021) | `04_did_it_event_study.ipynb` + `lp_iv_it_stratified.csv` | 3 reasons Obj C is exploratory not causal |
| 6 | — | All `phase1_audit/*.csv` + `report_draft.md` | Trace any `summary.md` number → source file in &lt;10 s |
| 7 | Closed book | Re‑pitch + 12‑question battery (see below) | One clean 60‑s recording |

**Prerequisite:** block 7 calendar slots (~3 hr each) or the plan usually dies by day 3.

---

## Five numbers to own

- Sample / panel scale (see `summary.md` opening narrative)  
- Conservative first‑stage statistic (two‑way clustered) ~**3.80** vs gate  
- Max inflation **drift** ~**0.875** vs internal threshold  
- **Placebo** significance (honest disclosure)  
- Phillips holdout forecast: **≈16% RMSE gain** augmented vs naive AR(1) (see `phillips_forecast_skill.csv`)

Exact strings live in `04_current_results/summary.md` after rebuild.

---

## Twelve-question retrieval battery (same repo, same docs)

Practice cold; on fumble, open only the file in the mapping you used elsewhere (audit CSVs, notebooks, `research_target.md`). Goal: answer each without notes.

1. What does Lucas (1980) claim vs your Obj A?  
2. Why is the **AVG vs YoY wedge** the spine?  
3. Preferred IV first stage — value and why gate fails?  
4. What is drift and why does high drift block tight causal language?  
5. Placebo significant — why not trash the project?  
6. Why does **money** help forecast more than **output gap** here?  
7. What do country FE and year FE absorb?  
8. What is LP and why use it for short‑run dynamics?  
9. Why Holm across inflation horizons?  
10. Why is Obj C not a valid causal IT evaluation?  
11. Sample definition (countries, years, rows)?  
12. If one more month: what would you improve (instruments / design / scope)?

---

## One-line mental model

**`02_data` → notebooks `01`→`04` → `04_current_results` proves what you say; `01_research_question` governs claims; `90_reproduction_scripts` + `tests` guarantee reproducibility.**

---

## Consistency cheatsheet (inside this repo)

- **Obj letters** (`research_target.md`): **A** = AVERAGE/long-run (**notebook `01`**); **B** = YoY (**`02`** FE/IV + Phillips + forecast, **`03`** LP-IV); **C** = IT probe (**`04`**).
- **Lucas (ii)** (money ↔ **nominal interest rate**): not in the pooled panel unless you extend — see **`02_data/supporting/lucas_ii_nominal_rate_plan.md`** (Path A/B/C).
- **“Phase 1 / Phase 2” in CLI** (`run_rebuild.py`): pipeline stages (**audit** vs **LP-IV block**), not the same labels as notebooks’ old “Phase 0/1/2” titles.
- **Claims:** trust **`04_current_results/`** + contract docs; memo/executive numbers are illustrative unless they match those CSVs.

*Last aligned with repo layout and shared plan: 2026-04-29.*
