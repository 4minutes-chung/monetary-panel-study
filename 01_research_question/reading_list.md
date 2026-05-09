# Reading list

**Arc:** Lucas intro → **Obj A** (AVERAGE) → **Obj B** (YoY: Phillips, forecast, LP-IV) → **Obj C** (IT probe) → **Obj D** (US-only Lucas ii appendix: money vs nominal rate). Notebooks: **`01`** · **`02`** · **`03`** · **`04`** · **`05`**.  
Authority if anything clashes: **`research_target.md`**.

Read **1 → 20** in order, or jump by topic using the index at the bottom.

---

## All readings (single order)

1. **Lucas, R.E. (1980)** — *Two Illustrations of the Quantity Theory of Money* — *American Economic Review* — Long-run money–inflation (i); (ii) is money vs **nominal interest rate** (US T-bill, low-frequency MA filter). Obj A does (i)-style country means; **Obj D** (`05_lucas_us_appendix.ipynb`) now implements (ii) for the US using FRED data — the gap previously noted in `lucas_ii_nominal_rate_plan.md` is being filled.

2. **McCandless, G.T. Jr. & Weber, W.E. (1995)** — *Some Monetary Facts* — *Minneapolis Fed Quarterly Review* — Cross-country long-run money / inflation facts; matches spirit of Obj A plots.

3. **De Grauwe, P. & Polan, M. (2005)** — *Is Inflation Always and Everywhere a Monetary Phenomenon?* — *Scandinavian Journal of Economics* — Strong correlation in high-inflation countries, weaker in low; links to IT / anchored-inflation stories.

4. **Sargent, T.J. & Surico, P. (2011)** — *Two Illustrations of the Quantity Theory of Money* — *American Economic Review* — Money–inflation link weakens when inflation is low and expectations anchored; bridges Obj A long averages to skeptical YoY pass-through.

5. **Galí, J. & Gertler, M. (1999)** — *Inflation dynamics: A structural econometric analysis* — *Journal of Monetary Economics* — Phillips / NK inflation block; aligns with lag inflation + gap in **`02`**.

6. **Atkeson, A. & Ohanian, L.E. (2001)** — *Are Phillips curves useful for forecasting inflation?* — *Federal Reserve Bank of Minneapolis Quarterly Review* — Simple beats fancy for inflation forecasts; backs the RMSE comparison in **`02`** / `phillips_forecast_skill.csv`.

7. **Stock, J.H. & Watson, M.W. (2007)** — *Why has U.S. inflation become harder to forecast?* — *Journal of Money, Credit and Banking* (supplement) — Persistence, instability; read with Atkeson–Ohanian.

8. **Jordà, Ò. (2005)** — *Estimation and inference of impulse responses by local projections* — *Journal of the American Statistical Association* — LP math; maps to **`03`** horizons, **not** the IT event-study in **`04`**.

9. **Bernanke, B.S. & Mishkin, F.S. (1997)** — *Inflation Targeting: A New Framework for Monetary Policy?* — *Journal of Economic Perspectives* — What IT is meant to do.

10. **Roger, S. (2010)** — *Inflation Targeting Turns 20* — *Finance & Development* (IMF) — Survey + adoption dates narrative; lines up with **`it_adoption_dates.csv`**.

11. **Mishkin, F.S. & Schmidt-Hebbel, K. (2007)** — *Does Inflation Targeting Make a Difference?* — NBER Working Paper 12876 — Broad cross-country IT evidence.

12. **Ball, L. & Sheridan, N. (2005)** — *Does Inflation Targeting Matter?* — In *The Inflation-Targeting Debate* (Bernanke & Woodford, eds.) — Skeptical: IT vs non-IT not so different.

13. **Lin, H-F. & Ye, X. (2009)** — *Does Inflation Targeting Really Make a Difference?* — *Journal of Monetary Economics* — Matching / selection; more positive on IT than Ball–Sheridan; read as counterweight to **12**.

14. **Callaway, B. & Sant'Anna, P.H.C. (2021)** — *Difference-in-differences with multiple time periods* — *Journal of Econometrics* — Staggered DiD; why naive TWFE on IT can mislead.

15. **Sun, L. & Abraham, S. (2021)** — *Estimating dynamic treatment effects in event studies with heterogeneous treatment effects* — *Journal of Econometrics* — Event-study / heterogeneity; pair with **14**.

16. **Borusyak, K., Jaravel, X. & Spiess, J. (2024)** — *Revisiting event-study designs: Robust and efficient estimation* — *Review of Economic Studies* — Imputation-style event study; optional robustness read for Obj C.

17. **Nakamura, E. & Steinsson, J. (2018)** — *Identification in Macroeconomics* — *Journal of Economic Perspectives* — Why strong associations ≠ causal macro thesis; read before overselling IV.

18. **Stock, J.H. & Yogo, M. (2005)** — *Testing for Weak Instruments in Linear IV Regression* — In *Identification and Inference for Econometric Models* — F-stat / weak-IV language behind gate tables in **`04_current_results`**.

19. **Abadie, A. (2021)** — *Using synthetic controls: Feasibility, data requirements, and methodological aspects* — *Journal of Economic Literature* — If IT DiD feels too coarse, single-country synthetic control as alternative design.

20. **Ramey, V. (2016)** — *Macroeconomic shocks and their propagation* — *Handbook of Macroeconomics*, Ch. 2 — LP-IV and shocks in survey form; complements **`03`**.

---

## Weekend shortcut (still the full list above — just a priority cue)

If time is tight, read **1–4** then **5–7** then **17** first; add **8** before talking LP-IV; add **9–16** before pitching IT Obj C; **19–20** when the project stays open.

---

## Topic → item numbers

| Topic | # |
|------|---|
| Quantity theory / Obj A | 1–4 |
| Phillips / forecast / Obj B | 5–7 |
| LP (notebook **`03`**) | 8 |
| IT / Obj C (substance) | 9–13 |
| Staggered DiD / event study | 14–16 |
| Identification / weak IV | 17–18 |
| Optional design depth | 19–20 |
| US Lucas ii / Obj D (notebook **`05`**) | 1 |

---

## Other docs

- **`START.md`** (repo root) — 7-day schedule + 12 questions (references item **#s** here).  
- **`reading_guide.md`** — short read order.
