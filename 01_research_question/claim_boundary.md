# Claim Boundary

## What This Project Can Say

- Money growth and inflation have a strong positive association in this country panel.
- GDP growth does not show the same robust relationship.
- Short-run LP-IV estimates are useful as exploratory dynamics, especially for inflation horizons.

## What This Project Should Not Say

- Do not claim a final causal policy elasticity.
- Do not say the preferred IV is strong.
- Do not say the conservative relevance gate passes.
- Do not use the later LP-IV horizons as decisive evidence without multiple-testing caution.

## Why The Boundary Is Conservative

- Conservative first-stage stat: `3.8016`, below the `3.8415` relevance threshold.
- Conservative first-stage p-value: `0.0512`, above `0.05`.
- Strong-IV threshold: fails because the conservative stat is below `10`.
- Stability drift: max drift is `0.8750`, above the `0.40` gate.
- Placebo diagnostics: one placebo test is significant.

## Practical Wording

Use this:

- "The evidence supports a robust cross-country association between money growth and inflation."
- "GDP growth effects are weak in the main specifications."
- "The IV evidence is directionally informative but weak-identification-sensitive."

Avoid this:

- "Money growth causes inflation by X in all settings."
- "The instrument validates causal interpretation."
- "The GDP effect is established."
