# Executive Memo (Simple Version, 2026-04-19)

## The question

Do countries with faster money growth also get higher inflation or faster GDP growth?

## Short answer

1. Yes for inflation in the core specs: the relationship is positive and statistically clear.
2. Not really for GDP growth: results are weak or not statistically reliable.
3. We frame this as association, not final causality, because the conservative identification gate fails.

## Data in one line

- 4,292 country-year observations
- 163 countries
- 1991 to 2020
- Variables are decimal rates (for example, `0.01 = 1` percentage point)
- Source: `04_current_results/tables/phase1_audit/data_audit_summary.csv`

## What we found (plain language)

### 1) Big-picture baseline (Phase 0 context)

- Pooled inflation: `0.6451` (`p=5.11e-07`)
- Pooled GDP growth: `-0.0010` (`p=0.8687`)
- Long-run country-average inflation (countries with `n>=30`, final `n=86`): `0.8909` (`p=2.84e-38`)
- Long-run country-average GDP growth: `0.0616` (`p=0.0320`)

Source status:

- These Phase 0 notebook-only exports are not present in the tracked final package. Keep this section as context only; current final claims should rely on `04_current_results/` evidence unless the notebook exports are regenerated.

### 2) Panel FE + IV baseline (Phase 1)

- FE baseline inflation: `0.5706` (`p=2.83e-06`)
- FE baseline GDP growth: `-0.0080` (`p=0.3951`)
- IV (external instrument) inflation: `1.0327` (`p=1.04e-04`)
- IV (external instrument) GDP growth: `-0.1196` (`p=0.1570`)
- First-stage (external instrument, country clustering): stat `4.2243`, `p=0.0398`
- Conservative first-stage for the gate (minimum across country and country+year clustering): stat `3.8016`, `p=0.0512`

Gate read:

- Conservative relevance gate fails (`3.8016 < 3.8415` and `p=0.0512 > 0.05`)
- Strong-IV (`stat>=10`) fails
- Stability drift and placebo diagnostics also fail the current scorecard, so the contract recommendation is `GO_PIVOT_SHORT_RUN`

Sources:

- `04_current_results/tables/phase1_audit/core_model_results.csv`
- `04_current_results/tables/phase1_audit/inference_sensitivity.csv`
- `04_current_results/tables/phase1_audit/audit_scorecard.csv`

### 3) Short-run LP-IV (Phase 2, primary external instrument)

Inflation response by horizon:

- `h0: 1.0327 (p=1.04e-04)`
- `h1: 0.6572 (p=0.0033)`
- `h2: 0.5697 (p=0.0238)`
- `h3: 0.5451 (p=0.0333)`

GDP growth at `h0`:

- `-0.1196 (p=0.1570)`

Minimum first-stage stat across primary inflation horizons:

- `4.2243`

Important caveats:

- Horizon p-values are unadjusted for multiple comparisons, so later horizons (`h2`, `h3`) are suggestive, not decisive.
- First-stage stats are below `10`, so IV/LP-IV p-values are weak-identification-sensitive.

Sources:

- `04_current_results/tables/short_run_lp/lp_iv_primary_results.csv`
- `04_current_results/tables/short_run_lp/interpretation_metrics.csv`

## How to read this responsibly

The inflation pattern is robust as an association.
The GDP growth pattern is weak.
With the current conservative gate failure, this is best treated as associational evidence and a short-run exploration, not a final causal claim.

## Reproducibility check

Notebook outputs and current script outputs previously matched exactly on key FE/IV/LP-primary numbers.

- Max absolute difference: `0.0`
- Notebook-vs-script parity was previously checked with max absolute difference `0.0`.
