# ERRATA

Post-council audit fixes applied 2026-05-09.

---

## B-1 — HP filter unit error

**What was wrong:**
`build_output_gap` in notebooks 02 and 03 contained:
```python
level = np.log1p(growth.fillna(0.0) / 100.0).cumsum()
```
`gdp_growth` in the panel is already in decimal (e.g., 0.13 = 13%). The `/100` division shrunk the log-level series by a factor of 100, collapsing the HP cycle to near-zero variance. This caused `output_gap_hp` to be essentially a noise series with near-zero signal.

**What it affected:**
- Phillips curve output_gap coefficient was spuriously significant: previously p=0.041, should be p=0.081 (n.s.)
- The m2_growth coefficient (0.349) was not materially affected — it survives unchanged

**Exact fix:**
```python
# Before (bug):
level = np.log1p(growth.fillna(0.0) / 100.0).cumsum()

# After (fix):
level = np.log1p(growth.fillna(0.0)).cumsum()
```

**Cells changed:**
- `03_analysis_notebooks/02_panel_fe_iv_baseline.ipynb`, cell id `7b7596b9`
- `03_analysis_notebooks/03_short_run_lp_iv.ipynb`, cell id `477589c6`

**Downstream correction:**
- `summary.md`: output_gap p-value updated from "p=0.041" to "p=0.081 (n.s. — HP filter corrected)"
- `report_draft.md` and `executive_memo.md`: output_gap rows updated; framing changed from "augmented Phillips" to "AR(1)+M2 persistence regression"

---

## D-1 — Triple-diff missing lower-order interaction (and collinearity)

**What was wrong:**
The slope probe in notebook 04 used only the triple interaction `post_it * it_treated * m2_growth`, omitting lower-order terms. The spec's proposed fix (adding `post_it * m2_growth` as `post_it_m2`) was evaluated but found to introduce perfect collinearity:

- For IT-treated units (`it_treated=1` always): `post_it * m2_growth == post_it * it_treated * m2_growth` (identical)
- For never-adopters (`post_it=0` always): `post_it * m2_growth = 0` always

The rank of the design matrix with all four terms is 3, not 4.

**Correct fix applied:**
The proper full-rank specification includes two lower-order terms:
- `it_m2 = it_treated * m2_growth` — identifies pre-adoption slope difference between treated and never-adopters
- `post_treated_m2 = post_it * it_treated * m2_growth` — identifies post-adoption slope change for treated countries

`post_it_m2` is collinear and was not included.

**Before (bug — single interaction):**
```python
slope_df["post_treated_m2"] = slope_df["post_it"] * slope_df["it_treated"] * slope_df["m2_growth"]
formula = "inflation ~ 1 + m2_growth + post_treated_m2 + EntityEffects + TimeEffects"
```
Result: `post_treated_m2` coef = -0.458, p<0.001 (but conflates pre-trend slope difference with post-adoption change)

**After (fix — proper triple-diff, full rank):**
```python
slope_df["it_m2"]           = slope_df["it_treated"] * slope_df["m2_growth"]
slope_df["post_treated_m2"] = slope_df["post_it"] * slope_df["it_treated"] * slope_df["m2_growth"]
formula = "inflation ~ 1 + m2_growth + it_m2 + post_treated_m2 + EntityEffects + TimeEffects"
```
Result:
- `m2_growth` (never-adopters baseline): coef=0.636, p=0.002
- `it_m2` (pre-adoption slope diff, treated vs control): coef=0.212, p=0.281 (n.s.)
- `post_treated_m2` (post-adoption slope change for treated): coef=-0.485, p<0.001

**Cells changed:**
- `03_analysis_notebooks/04_did_it_event_study.ipynb`, cell id `8f269407` — full rewrite of slope probe

**Interpretation impact:**
The pre-adoption slope difference between IT and non-IT countries is n.s. (p=0.281), which is a useful parallel-trends-supporting observation. The post-adoption slope change remains large and significant (-0.485). Caution: the endogeneity caveat on IT adoption still applies.
