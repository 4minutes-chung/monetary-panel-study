# Data Expansion Options

## Current Data Audit

| Dimension | State | Problem |
|---|---|---|
| Core panel | 163 countries, 1991–2020 — m2_growth, inflation, gdp_growth | Clean, no missingness |
| Controls | trade_open (15% missing), investment_share (17% missing) | Thin but tolerable |
| Instrument | depth × fedfunds level | Conservative stat = 3.8, barely relevant — explains failed gate |
| Institutional structure | Nothing | No exchange rate regime, no IT adoption, no income group split, no CBI |
| Crisis / hyperinflation flag | None | Congo 740%, Brazil 350% early 1990s pooled with everything else |

The sample size is not the problem — 163 × 30 is fine. The gap is that there are no structural or institutional variables, so the analysis cannot go beyond "the correlation exists."

---

## Path A — Keep topic, add data

Add three datasets; existing code and infrastructure stay intact.

| Dataset | Source | What it enables |
|---|---|---|
| Exchange rate regime | Ilzetzki, Reinhart & Rogoff (2019) — free on their website | Split pegs vs floats — core Mundell-Fleming heterogeneity |
| Inflation targeting adoption dates | Roger (2010) IMF WP, or Fatás & Rose dataset | IT event-study; does targeting structurally change the pass-through? |
| Crisis / hyperinflation flag | Define m2_growth > 1.0, or use Reinhart-Rogoff crisis data | Remove regime-collapse episodes before re-running main specs |

**New Objective B (Path A):**
Does the money-inflation pass-through differ by exchange rate regime and monetary framework, and are results robust after excluding hyperinflation episodes?

Answerable with FE heterogeneity regressions. No strong IV required.

---

## Path B — Rethink topic

> Do countries that adopt inflation targeting show a structural break in the money-inflation relationship?

- Unit: country; event = IT adoption date
- Method: LP event-study around adoption date
- Obj A = pre-adoption cross-section (Lucas-style); Obj B = dynamic post-adoption path
- Data needed: IT adoption dates only — everything else already exists
- Identification is cleaner: adoption date is a policy event, more plausibly exogenous than depth × fedfunds

Requires rethinking notebooks 02 and 03 from scratch.

---

## Recommendation

**Path A is lower risk.** Existing work stays relevant; adding exchange rate regime + crisis flag converts the project from a correlation study into a heterogeneity study in a well-established area. Weak IV stays weak, but FE heterogeneity regressions do not require a strong instrument.

**Path B is more intellectually clean** but means rebuilding the estimation notebooks. Worth it if this is meant to be a standalone research piece rather than a portfolio macro panel exercise.
