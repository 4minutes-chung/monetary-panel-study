# Economist Policy Brief (V2)

## Research Question
Across countries, how strongly is money growth linked to inflation and GDP growth, and what can policymakers infer from that evidence?

## Data and Design
- Panel: 163 countries, 1991-2020, 4,292 country-year observations.
- Core outcomes: inflation, GDP growth.
- Core exposure: money growth (`m2_growth`).
- Methods:
  - TWFE baseline and controls,
  - IV-TWFE with lag and external instruments,
  - short-run LP-IV horizons for inflation (h=0..3), GDP static at h=0.

## Main Findings
1. Inflation relationship is strong and persistent.
2. GDP-growth relationship is weak and not robust.
3. Preferred external-IV first-stage passes a relevance gate (chi2(1) > 3.8415, p < 0.05) but fails the strong-IV threshold (>=10).
4. Short-run inflation responses are statistically positive in the primary LP-IV path, but identification strength remains limited.

## Interpretation Boundary
This project supports a **robust cross-country association** between money growth and inflation.  
It does **not** yet establish a high-confidence causal policy elasticity for all settings.

## Policy Takeaways
1. Treat money growth as an inflation-risk signal, especially in vulnerable macro regimes.
2. Avoid using these estimates alone to justify growth-targeted monetary expansion.
3. Pair quantitative cross-country evidence with country-specific institutional diagnostics.

## Practical Use in Interviews or Portfolio Reviews
- Strong point: rigorous audit discipline and explicit no-overclaiming boundary.
- Honest limitation: instrument quality still constrains causal interpretation.
- Next-step research plan: improve identification via event/regime designs and heterogeneity splits.
