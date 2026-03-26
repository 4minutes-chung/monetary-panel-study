# V2 Rebuild Summary

## What changed
- Replaced approximate FE handling with exact FE formulas in IV estimation.
- Replaced plain first-stage t^2 proxies with clustered first-stage diagnostics from linearmodels.
- Enforced restricted controls in audited GDP specs (no gdp_pc_growth leakage).
- Expanded stability audit to leave-one-region-out across all available regions.

## Phase 1 Audit V2
- Recommendation: `GO_PIVOT_SHORT_RUN`
- Preferred first-stage stat (external IV, inflation spec): `4.2243`
- Max inflation drift across gate specs: `0.8750`
- Placebo significant tests (p<0.05): `1`

## Phase 2 LP-IV V2
- Recommendation flag: `EVIDENCE_WEAK_REVISIT_IDENTIFICATION`
- Primary IV mean first-stage stat: `4.2990`
- Primary IV inflation significant horizons (5%): `4`
- Primary IV GDP significant horizons (5%): `0`

## Claim boundary
- If first-stage remains below strong threshold, treat this as robust association evidence, not defended causal effect.