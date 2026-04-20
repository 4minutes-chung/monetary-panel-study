# Executive Memo (Simple Version, 2026-04-19)

## The question

Do countries with faster money growth also get higher inflation or faster GDP growth?

## Short answer

1. Yes for inflation: the relationship is strong and stable across our main specs.
2. Not really for GDP growth: results are weak or not statistically reliable.
3. We still frame this as association, not final causality, because instrument strength is limited.

## Data in one line

- 4,292 country-year observations
- 163 countries
- 1991 to 2020
- Variables are decimal rates (for example, `0.01 = 1` percentage point)
- Source: `outputs/notebook_phase0/phase0_sample_summary.csv`

## What we found (plain language)

### 1) Big-picture baseline (Phase 0)

- Pooled inflation: `0.6451` (`p=5.11e-07`)
- Pooled GDP growth: `-0.0010` (`p=0.8687`)
- Long-run country-average inflation (countries with `n>=30`, final `n=86`): `0.8909` (`p=2.84e-38`)
- Long-run country-average GDP growth: `0.0616` (`p=0.0320`)

Sources:

- `outputs/notebook_phase0/phase0_pooled_results.csv`
- `outputs/notebook_phase0/phase0_longrun_results.csv`

### 2) Panel FE + IV baseline (Phase 1)

- FE baseline inflation: `0.5706` (`p=2.83e-06`)
- FE baseline GDP growth: `-0.0080` (`p=0.3951`)
- IV (external instrument) inflation: `1.0327` (`p=1.04e-04`)
- IV (external instrument) GDP growth: `-0.1196` (`p=0.1570`)
- First-stage (external instrument): stat `4.2243`, `p=0.0398`

Gate read:

- Relevance gate passes (`chi2(1)>3.8415`, same idea as `p<0.05` for `chi2(1)`)
- Strong-IV (`stat>=10`) fails

Sources:

- `outputs/notebook_phase1/phase1_fe_results.csv`
- `outputs/notebook_phase1/phase1_iv_results.csv`
- `outputs/notebook_phase1/phase1_gate_read.csv`

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

- `outputs/notebook_phase2/phase2_lp_iv_primary_results.csv`
- `outputs/notebook_phase2/phase2_interpretation_metrics.csv`

## How to read this responsibly

The inflation pattern is robust as an association.
The GDP growth pattern is weak.
With current first-stage strength, this is best treated as associational evidence, not a final causal claim.

## Reproducibility check

Notebook outputs and v2 headline outputs match exactly on key FE/IV/LP-primary numbers.

- Max absolute difference: `0.0`
- Report: `docs/NOTEBOOK_V2_PARITY_2026-04-19.md`
