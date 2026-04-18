# Executive Memo (Econometrics Side Project)

**Date:** April 17, 2026  
**Project:** Cross-country money growth, inflation, and GDP-growth evidence (V2 closeout)  
**Decision status:** Close current phase within 3 days; treat next phase as optional research extension.

## 1) Decision in one sentence
The evidence is strong enough to close this as a high-quality **associational econometrics case study** with policy relevance, but not as a fully defended cross-country causal elasticity.

## 2) Research question
Across countries, how strongly is money growth associated with inflation and GDP growth, and what can policymakers reasonably infer from this evidence?

## 3) Data and empirical design
- Panel: 163 countries, 1991-2020, 4,292 country-year observations.
- Outcomes: inflation and GDP growth.
- Exposure: money growth (`m2_growth`).
- Designs used:
  - Two-way fixed effects (baseline and restricted controls),
  - IV-TWFE (lag and external instruments),
  - short-run LP-IV horizons for inflation (h=0..3), GDP static at h=0.

## 4) Core empirical findings
- FE baseline inflation estimate: **0.571** (p < 0.001).
- FE baseline GDP-growth estimate: **-0.008** (p = 0.395, not significant).
- IV external instrument inflation estimate: **1.033** (p < 0.001).
- IV external first-stage statistic (inflation spec): **4.224**.
  - Relevance gate (chi2(1) > 3.8415, p < 0.05): pass.
  - Strong-IV label (>=10): fail.
- Primary LP-IV inflation responses are positive and significant for h=0..3, but first-stage remains weak-to-moderate (~4.2-4.9).
- GDP response remains weak (static h=0 not significant).

## 5) What is credible to claim
Credible:
- Money growth has a robust cross-country association with inflation across multiple specifications.
- GDP-growth effects are not robust in this design.
- The project uses strong research governance: explicit audit gates, placebo checks, stability checks, and no-overclaiming boundaries.

Not yet credible:
- A universal, high-confidence causal policy multiplier from money growth to inflation or growth.

## 6) Policy interpretation
- Monetary expansion should be treated as an inflation-risk signal, especially in fragile macro environments.
- This evidence does not support a reliable growth-boost narrative from money growth shocks.
- Policy use should combine this cross-country evidence with country-level institutional diagnostics and context.

## 7) Next research agenda (optional Phase 3)
Prioritize identification upgrades, not extra model complexity:
- Event/regime-based monetary shocks,
- heterogeneity by inflation regime and macro state,
- institution-aware designs for stronger exclusion logic.

## 8) Closeout recommendation
Mark this project as:
**Closed (Phase Complete, Next Phase Optional)**.

This preserves portfolio credibility by emphasizing empirical discipline, transparent limitations, and a concrete forward research agenda.
