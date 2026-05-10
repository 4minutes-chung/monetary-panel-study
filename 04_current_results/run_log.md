# Run Log

---

## 2026-05-09 — Post-council audit fixes

### Code fixes

**B-1 — HP filter unit error (nb02, nb03)**
- Fixed `build_output_gap`: removed erroneous `/100` from `np.log1p(growth.fillna(0.0) / 100.0)`
- gdp_growth is already decimal; the division shrunk HP cycle variance to near-zero
- After fix: output_gap_hp p-value in augmented Phillips moves from 0.041 → 0.081 (n.s.)
- m2_growth coefficient unchanged at 0.349, p=0.032

**D-1 — Triple-diff collinearity (nb04)**
- Original slope probe omitted lower-order interactions
- Spec's proposed `post_it_m2` term is perfectly collinear with `post_treated_m2` for this design
- Applied full-rank fix: `it_m2` (pre-adoption slope diff) + `post_treated_m2` (post-adoption change)
- New results: m2_growth=0.636 (p=0.002), it_m2=0.212 (p=0.281, n.s.), post_treated_m2=-0.485 (p<0.001)

### New diagnostic cells added (nb02)

- **Pesaran CD test**: CD=158.4, p≈0 — cross-sectional dependence confirmed
- **IPS panel unit root**: inflation W=-34.4 p≈0; m2_growth W=-36.3 p≈0 — both stationary; TWFE valid
- **Driscoll-Kraay SEs**: full sample coef=0.665, p=0.003 (survives); clean sample coef=0.040, p=0.145 (n.s.)
- **COVID robustness**: full 0.664/p=0.0002, clean 0.040/p=0.067 — excluding 2020-2021 changes nothing
- **Sample mismatch**: TWFE on 108-country Obj-A subset: coef=0.820, p<0.001; wedge is real, not composition artifact

### New diagnostic cell added (nb05)

- **Newey-West HAC**: M2→Inflation slope=0.474, t=1.884, p=0.060 (borderline); M2→T-bill slope=0.421, p=0.155 (n.s.)

### Documentation updates

- `04_current_results/summary.md`: updated Phillips output_gap, F-stat, RMSE period, nobs, added full diagnostic section
- `05_final_writing/executive_memo.md`: renamed Phillips to AR(1)+M2 regression; updated IV text; reframed wedge as descriptive decomposition; added NW/DK/COVID/mismatch notes; one-paragraph updated
- `05_final_writing/report_draft.md`: updated nobs (4,643→4,750), F-stat, RMSE (8.1%→7.4%, 2016-2020→2016-2024), output_gap rows, IV section, identification limits section
- Created `ERRATA.md` (project root) — documents B-1 and D-1 in full
- Created `02_data/UNITS_REGISTER.md` — one row per variable with unit verification

### Notebooks executed cleanly

- `02_panel_fe_iv_baseline.ipynb` — executed, no errors
- `03_short_run_lp_iv.ipynb` — executed, no errors
- `04_did_it_event_study.ipynb` — executed, no errors (D-1 fix resolved rank deficiency)
- `05_lucas_us_appendix.ipynb` — executed, no errors
