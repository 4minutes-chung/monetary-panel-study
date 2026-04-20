# Executive Memo (2026-04-19)

## Research Question

Across countries, how strongly is money growth associated with inflation and GDP growth, and what can be claimed under current identification checks?

## Data Scope

- Panel coverage: 4,292 country-year observations
- Countries: 163
- Years: 1991 to 2020
- Variable scale: growth and inflation are decimal rates (for example, `0.01 = 1` percentage point).
- Source table: `outputs/notebook_phase0/phase0_sample_summary.csv`

## Headline Findings

1. Inflation is strongly and consistently positively associated with money growth.
2. GDP growth relationships are weak or statistically fragile across baseline and IV specifications.
3. Identification relevance is present, but instruments are not strong by the `>=10` threshold, so claims remain associational.

## Core Evidence

### Phase 0 motivation (Lucas-style replication)

- Pooled inflation association: coefficient `0.6451`, `p = 5.11e-07`.
  - Source: `outputs/notebook_phase0/phase0_pooled_results.csv` (`model=pooled_inflation`).
- Pooled GDP growth association: coefficient `-0.0010`, `p = 0.8687`.
  - Source: `outputs/notebook_phase0/phase0_pooled_results.csv` (`model=pooled_gdp_growth`).
- Long-run country-average inflation association (n>=30 countries): coefficient `0.8909`, `p = 2.84e-38` (86 countries).
  - Source: `outputs/notebook_phase0/phase0_longrun_results.csv` (`model=longrun_inflation_country_avg`).
- Long-run country-average GDP growth association: coefficient `0.0616`, `p = 0.0320`.
  - Source: `outputs/notebook_phase0/phase0_longrun_results.csv` (`model=longrun_gdp_country_avg`).

### Phase 1 baseline FE and IV layer

- FE baseline inflation: coefficient `0.5706`, `p = 2.83e-06`.
  - Source: `outputs/notebook_phase1/phase1_fe_results.csv` (`model=fe_baseline`, `outcome=inflation`).
- FE baseline GDP growth: coefficient `-0.0080`, `p = 0.3951`.
  - Source: `outputs/notebook_phase1/phase1_fe_results.csv` (`model=fe_baseline`, `outcome=gdp_growth`).
- IV (external instrument) inflation: coefficient `1.0327`, `p = 1.04e-04`.
  - Source: `outputs/notebook_phase1/phase1_iv_results.csv` (`outcome=inflation`, `instrument=instrument_m2_external_level`).
- IV (external instrument) GDP growth: coefficient `-0.1196`, `p = 0.1570`.
  - Source: `outputs/notebook_phase1/phase1_iv_results.csv` (`outcome=gdp_growth`, `instrument=instrument_m2_external_level`).
- First stage for external instrument: statistic `4.2243`, `p = 0.0398`.
  - Source: `outputs/notebook_phase1/phase1_iv_results.csv` (same external instrument row).
- Gate read:
  - Relevance gate (`chi2(1)>3.8415`, equivalently `p<0.05` for `chi2(1)`): pass.
  - Strong-IV label (`stat>=10`): fail.
  - Source: `outputs/notebook_phase1/phase1_gate_read.csv`.

### Phase 2 short-run LP-IV layer (primary external instrument)

- Inflation LP-IV coefficients are positive and significant for horizons `h=0..3`:
  - `h0: 1.0327 (p=1.04e-04)`
  - `h1: 0.6572 (p=0.0033)`
  - `h2: 0.5697 (p=0.0238)`
  - `h3: 0.5451 (p=0.0333)`
- GDP growth LP-IV at `h0`: `-0.1196 (p=0.1570)`.
- Minimum first-stage stat across primary inflation horizons: `4.2243`.
- Horizon p-values are unadjusted for multiple comparisons; later-horizon significance (`h2`, `h3`) should be treated as suggestive rather than definitive.
- Because first-stage statistics remain below `10` across primary horizons, IV/LP-IV p-values are weak-identification-sensitive.
- Source tables:
  - `outputs/notebook_phase2/phase2_lp_iv_primary_results.csv`
  - `outputs/notebook_phase2/phase2_interpretation_metrics.csv`

## Claim Boundary

Current evidence supports a robust inflation association with money growth and weak/non-robust GDP growth association.
Given first-stage relevance without strong-IV strength, this memo treats results as associational rather than definitive causal estimates.

## Reproducibility Note

A parity check against canonical v2 outputs found exact numerical agreement on headline FE/IV/LP-primary coefficients and first-stage statistics (`max absolute diff = 0.0`).

- Parity report: `docs/NOTEBOOK_V2_PARITY_2026-04-19.md`
