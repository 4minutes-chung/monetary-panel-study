# Econometric Caveats

## Identification

The preferred external instrument does not pass the conservative relevance gate once both country clustering and country+year clustering are considered.

Key numbers:

- Country-clustered first stage: `4.2243`, p-value `0.0398`.
- Country+year-clustered first stage: `3.8016`, p-value `0.0512`.
- Conservative gate: fail.

## Weak-IV Risk

The strong-IV threshold is `10.0`. The conservative first-stage statistic is below that threshold, so IV and LP-IV p-values should be read as weak-identification-sensitive.

## Stability Risk

The max inflation coefficient drift across gate specs is `0.8750`, above the `0.40` threshold. That means the sign is stable, but the magnitude is not stable enough for a precise causal elasticity claim.

## Placebo Risk

One placebo diagnostic is significant. This does not automatically invalidate the whole project, but it means the instrument story needs caution.

## Best Use Of The Results

Use the project to support:

- a strong money growth-inflation association,
- weak GDP growth evidence,
- a transparent identification audit,
- a motivation for better instruments or narrower designs.

Do not use it as a final causal policy multiplier.
