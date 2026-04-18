# Project Full Explanation Report

**Project:** Cross-country money growth, inflation, and growth analysis (Phase 0 -> Phase 2)  
**Owner:** Steven Chung  
**Prepared:** 2026-02-19

---

## 1. Why this report exists
This report documents what was actually done across all phases, what worked, what failed, what was learned, and why the project direction was changed.

---

## 2. Starting point and objective
Initial objective was to build a Lucas-style long-run cross-country macro project (money growth, inflation, GDP growth) as a portfolio piece.

Secondary objective evolved into improving credibility (not just significance), then deciding continue vs pivot with explicit rules.

### Canonical update (2026-04-18)
- Canonical execution path is now script-first: `python3 -m pip install -r requirements.txt` -> `python3 v2/run_v2_rebuild.py` -> `python3 v2/build_portfolio_graphs.py`.
- Historical notebook phases below remain useful provenance, but current claims should be sourced from V2 script outputs.
- Canonical first-stage interpretation is two-tier: relevance gate is clustered Wald chi2(1) > 3.8415 and p < 0.05, and strong-IV label is first-stage statistic >= 10.
- Claim boundary is unchanged: strong inflation association evidence, limited causal interpretation under weak-to-moderate instrument strength.

---

## 3. Phase-by-phase record

### Phase 0 (baseline pipeline)
What was done:
- Loaded World Bank data and built a clean country-year panel.
- Constructed growth variables (`m2_growth`, `inflation`, `gdp_growth`).
- Ran pooled and long-run cross-country regressions.
- Exported merged datasets for downstream work.

Core data state:
- Panel rows: 4,292
- Countries: 163
- Years: 1991-2020
- Duplicate country-year rows: 0

Main pattern observed:
- Money growth strongly related to inflation in many baseline specs.
- Money growth weak/non-significant for GDP growth.

Interpretation at this stage:
- Useful empirical signal, but mostly associational and not identification-complete.

---

### Phase 0.5A / 0.5B (window variants)
What was done:
- Created period-window variants and diagnostics.
- Added panel-style estimation attempts (`PanelOLS`) and export-ready panel files.

Why this mattered:
- It tested sensitivity to time window choices.
- It made clear that results can move with sample design.

---

### Phase 1 (structured notebook + runnable baseline)
Implemented notebook:
- `lucas_Phase 1.ipynb`

What it included:
- Plan-first structure.
- FE baseline and robustness core (winsorization, period split, LOCO).
- Guarded scaffolds for IV, dynamic panel, forecasting.
- Deterministic output exports.

Key baseline outputs from this stage:
- FE inflation (baseline): positive, significant.
- FE GDP growth (baseline): weak/non-significant.

Interpretation:
- Consistent directional signal for inflation.
- No robust growth effect.

---

### Phase 1.1 (gap fill: actual controls + IV data + second stage)
Added data files:
- `data/phase1_controls.csv`
- `data/phase1_instruments.csv`
- `data/phase1_data_sources.csv`

Implemented notebook:
- `lucas_Phase 1.1.ipynb`

What was done:
- Re-estimated FE + controls.
- Ran first-stage diagnostics and multiple IV specs.
- Built side-by-side model comparison tables.

Representative Phase 1.1 results:
- FE+controls inflation: `coef = 0.4988`, `p = 1.686e-4`
- FE+controls GDP growth: `coef = -0.0013`, `p = 0.1385`

First-stage diagnostics (selected):
- `instrument_m2_l1` (TWFE): F-proxy ~ 237.75 (strong)
- `instrument_m2_external_level` (TWFE): F-proxy ~ 11.00 (borderline but above 10 in that sample)

IV examples:
- `iv_twfe_lag`, inflation: significant positive effect
- `iv_twfe_external`, inflation: significant positive effect
- GDP growth IV effects: generally weak/non-significant

Interpretation:
- Inflation link persisted under multiple estimators.
- GDP-growth link remained weak.
- Identification quality still required a formal audit gate.

---

### Phase 1 Audit (formal continue-vs-pivot decision)
Implemented notebook:
- `lucas_Phase 1.audit.ipynb`

Audit scope:
- Data/leakage checks
- Fixed model set only
- First-stage and weak-IV diagnostics
- Placebo tests
- Stability checks
- Hard pass/fail scorecard

Hard thresholds used in the legacy notebook audit:
- Preferred first-stage F >= 10
- Inflation sign positive in >= 4/5 gate specs
- Inflation drift < 40%
- GDP effect weak across core specs
- Placebos not significant

Note:
- The threshold block above describes the Phase 1 notebook audit as historically run.
- The current canonical V2 gate uses clustered Wald chi2(1) diagnostics and reports both relevance and strong-IV status separately.

Scorecard outcome:
- Fail: preferred first-stage F (`9.4689 < 10`)
- Fail: drift (`0.8750 > 0.40`)
- Fail: placebo criterion (1 significant placebo)
- Pass: inflation sign consistency
- Pass: GDP weak-effect consistency

Decision:
- **`GO_PIVOT_SHORT_RUN`**

Why this is important:
- The project did not rely on favorable coefficients alone.
- It used an explicit kill-switch for fragile evidence.

---

### Phase 2 (pivot: short-run policy effectiveness)
Implemented notebook:
- `lucas_Phase 2_short_run.ipynb`
- Executed: `lucas_Phase 2_short_run.executed.ipynb`

Method:
- Panel local projections + IV
- Horizons: h = 0,1,2,3
- Outcomes: inflation and GDP growth
- Primary IV: `instrument_m2_external_level`
- Sensitivity IV: `instrument_m2_l1`

Key findings:
- Primary external IV short-run first-stage was weak on average (mean F ~ 3.06).
- Under primary IV, inflation effects were positive but not 5% significant across horizons.
- Under lag-IV sensitivity, first stage was very strong and inflation responses were significant at all horizons.
- GDP responses mostly weak/non-significant (one horizon significant in lag-IV sensitivity).

Interpretation:
- Short-run framing is more aligned with the policy-effectiveness question.
- Instrument quality remains the central bottleneck.
- Results are informative, but not yet final causal evidence.

---

## 4. How well the plan was implemented
Overall implementation quality: **strong but not perfect**.

What was done well:
- End-to-end execution from baseline to audit gate to pivot.
- Clear thresholds and decision logic.
- Reproducible script-first V2 pipeline plus historical notebook exports.
- Good separation of evidence vs interpretation.

What was imperfect:
- Some heavy notebook runs were slow/unstable under full FE/IV loops and required practical runtime adjustments.
- Weak-IV robust inference remains partial.
- Primary short-run external IV is not yet strong enough for high-confidence policy claims.

Net assessment:
- The process quality is portfolio-strong.
- Identification strength is not yet portfolio-final.

---

## 5. Main conclusions
1. **You did meaningful work.** This is not a "nothing done" project.
2. **The strongest achievement is decision quality**, not just coefficients.
3. **Long-run branch was correctly stress-tested and gated.**
4. **Pivot decision was correct** under your own rules.
5. **Current frontier problem is instrument credibility** in short-run design.

---

## 6. Learning summary (most important)
- High R-squared or significant coefficients are insufficient.
- Robustness stability + placebo behavior + first-stage strength should drive decisions.
- A strong applied project is one where weak narratives are killed early and replaced with stronger designs.
- You converted a potentially overfit story into an auditable research workflow.

---

## 7. Recommended next step framing (for later execution)
Not implementing new work in this report. For the next stage, the key learning-driven focus should be:
- Upgrade identification for short-run design before adding model complexity.
- Keep the same audit gate structure for any new spec.
- Prioritize one defensible causal path over many partially-defensible variants.

---

## 8. Related files (current canonical path)
Canonical scripts:
- `v2/run_v2_rebuild.py`
- `v2/build_portfolio_graphs.py`

Canonical outputs:
- `v2/outputs/V2_SUMMARY.md`
- `v2/outputs/phase1_audit_v2/`
- `v2/outputs/phase2_short_run_v2/`
- `v2/outputs/portfolio_graphs/`

Historical outputs kept for reference:
- `outputs/phase1_1/`
- `outputs/phase1_audit/`
- `outputs/phase2_short_run/`

Historical notebook work remains part of project history, but is not required for canonical reruns.

