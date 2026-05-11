# Start — learn this repo

**Numbers:** `04_current_results/summary.md` · **Research contract:** `01_research_question/research_target.md` · **Papers:** `01_research_question/reading_list.md`

## Setup

```bash
pip install pandas numpy statsmodels linearmodels scipy matplotlib
```

## Notebook order

| Step | File | What it does |
| ---- | ---- | ------------ |
| 1 | `03_analysis_notebooks/01_lucas_replication.ipynb` | Obj A — long-run between estimator, Lucas scatter |
| 2 | `03_analysis_notebooks/02_panel_fe_iv_baseline.ipynb` | Obj B — TWFE, sub-period, COVID scatter, distributed lag |
| 3 | `03_analysis_notebooks/03_short_run_lp_iv.ipynb` | LP-IV (appendix — directional only) |
| 4 | `03_analysis_notebooks/04_did_it_event_study.ipynb` | Obj C — IT event study, slope probe |
| 5 | `03_analysis_notebooks/05_lucas_us_appendix.ipynb` | Obj D — US FRED replication |

Run in order. Each notebook writes figures to `04_current_results/figures/`.

## Five numbers to own

Open `04_current_results/summary.md` and find:

1. Long-run slope clean sample (Obj A)
2. Short-run TWFE clean sample (Obj B)
3. Sub-period slopes — pre-QE, QE era, COVID
4. COVID cross-country scatter slope
5. IT post-adoption slope shift (Obj C)

## Twelve questions (practice cold)

1. Lucas (1980) vs Obj A — what's the same, what's new?
2. Why does the between slope (0.52) dwarf the within slope (0.04)?
3. IV first stage — value + why it fails the strong-IV gate?
4. Why Driscoll-Kraay SEs, not clustered?
5. What does the Pesaran CD test tell you?
6. Why does COVID show up cross-sectionally but not within-country?
7. Country FE vs year FE — what does each absorb?
8. What is a local projection?
9. Why Holm correction on LP horizons?
10. Why is Obj C not a causal IT claim?
11. Sample: countries, years, rows?
12. One more month — what would you fix first?

## Map

`01` = Obj A · `02`+`03` = Obj B · `04` = Obj C · `05` = Obj D · outputs = `04_current_results/`
