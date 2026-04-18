# V2 Rebuild Summary

## What changed
- Kept exact FE formulas for IV estimation.
- Kept exact calendar-year horizon matching (no row-shift approximation).
- Added explicit no-partial-export checks for LP-IV outputs.
- Added inference sensitivity table comparing one-way vs two-way clustering on key IV spec.
- Clarified weak-IV read: first-stage is reported as clustered Wald chi2(1), not classic F-stat.

## Phase 1 Audit V2
- Recommendation: `GO_PIVOT_SHORT_RUN`
- Preferred first-stage stat (external IV, inflation spec): `4.2243`
- Preferred first-stage p-value: `0.0398`
- Preferred first-stage strong-IV threshold (>=10): `FAIL`
- Max inflation drift across gate specs: `0.8750`
- Placebo significant tests (p<0.05): `1`

## Phase 2 LP-IV V2
- Recommendation flag: `EVIDENCE_WEAK_REVISIT_IDENTIFICATION`
- Primary IV inflation significant horizons (5%): `4`
- Primary IV GDP significant horizons (5%): `0` (static h=0 only)

## Claim boundary
- Treat this as strong cross-country association evidence.
- Causal interpretation remains limited while first-stage strength is weak/moderate.