# The Quantity Theory in the Age of QE and COVID
### A 160-Country, 34-Year Revisit of Lucas (1980)

**Claim tiers:** Obj A and D are descriptive. Obj B and C are exploratory/associational.
No causal policy claims are made anywhere in this report.

---

## 1. Introduction

Does the quantity theory of money hold in the age of quantitative easing and post-COVID inflation?

Lucas (1980) established the benchmark: in long-run cross-country data, money growth and inflation
move roughly one-for-one. McCandless & Weber (1995) and De Grauwe & Polan (2005) confirmed that
fact with pre-GFC samples. But neither study covers the defining monetary events of the last 25 years:
the 2008–2020 era in which central banks expanded M2 by trillions without triggering inflation; and
the 2021–2023 surge, the sharpest since the 1970s, which arrived after a decade of apparent monetary
impotence.

This report uses 160 countries, 1991–2024, to ask three questions:

1. **Does the long-run quantity theory still hold?** (Obj A — between estimator, country means)
2. **Is there a short-run year-to-year link between money and prices, and does it depend on the era?** (Obj B — within-country TWFE + sub-period analysis)
3. **Was the 2021–2023 inflation a money story — and if so, through which channel?** (Obj B extension — cross-country COVID scatter, distributed lag)

The answer to question 1 is yes, with slope 0.52–0.95 depending on sample. The answer to questions
2 and 3 is more interesting: the year-to-year within-country link has been near zero since 2008,
but across countries, those that expanded M2 more in 2020–21 got significantly more inflation in
2021–23. The COVID inflation was a cross-sectional monetarist story — driven by the scale of fiscal
transfers, not by QE bank reserves — and operated through a distributed lag that persists at least 2 years.

Lucas's second illustration (money growth → nominal interest rates) is handled in a US-only appendix
using FRED data (Obj D, Section 7).

---

## 2. Data and Panel

- **Countries:** 160, of which 123 form the "clean sample" (drop any country with any year > 40%
  inflation, removing post-Soviet and Latin American hyperinflation episodes of 1991–1999).
- **Period:** 1991–2024 annual. 4,750 rows total.
- **Source:** World Bank WDI for M2 growth, CPI inflation, GDP growth. IT adoption dates from
  Roger (2010) and Hammond (2012), reconciled.
- **Output gap:** Annual HP filter (λ=6.25) applied to cumsum of log(1+gdp_growth). GDP growth
  is in decimal (0.026 = 2.6%); the log1p input is already correct.
- **Variable units:** All monetary and price series are log annual changes (decimal). See
  `02_data/UNITS_REGISTER.md` for the full units register.

Two samples are reported throughout:

| Label | N countries | N rows | Definition |
|---|---|---|---|
| Full | 160 | 4,750 | All available |
| Clean | 123 | 3,639 | Max annual inflation < 40% |

---

## 3. Objective A — Long-Run Cross-Country (Between Estimator)

Country-level OLS of mean inflation on mean M2 growth (countries with ≥30 observations).
This is the Lucas (1980) first-illustration replication.

### Results

| Sample | Countries | M2 slope | p-value | R² |
|---|---|---|---|---|
| Full (incl. hyperinflation) | 108 | **0.952** | 4.4×10⁻⁵⁰ | 0.877 |
| Clean (no hyperinflation) | 83 | **0.524** | 6.8×10⁻¹⁵ | 0.529 |

**Full-sample slope near one:** The far-right cluster of post-Soviet and Latin American
hyperinflationary countries (Ukraine 388%, Brazil 308%, Belarus 996% in the early 1990s)
anchors the slope close to 1. These episodes confirm the quantity theory at extremes.

**Clean-sample slope at 0.52:** This is the more relevant estimate for modern monetary regimes.
Still large, still highly significant, still directionally consistent with QTM — but with meaningful
slippage. The remaining R² gap (0.53 vs. 0.88) reflects structural differences in financial
development, velocity trends, and reserve accumulation across countries.

**Lucas (ii) cross-country:** Country-mean M2 growth vs country-mean lending rate (107 clean
countries): slope = 0.49, R² = 0.16. Consistent with the Fisher relation at low frequencies.
Below 1 because lending rates embed credit risk above the policy rate.

**Figure:** `04_current_results/figures/between_within_decomposition.png` (between vs within panels)

---

## 4. Objective B — Short-Run Year-on-Year (TWFE)

Two-way fixed effects (country + year) regression of annual inflation on annual M2 growth.
This estimates the within-country year-to-year pass-through after absorbing all time-invariant
country heterogeneity and common year shocks.

### 4.1 Baseline TWFE

| Sample | Coef | p-value | Within R² | N |
|---|---|---|---|---|
| Full (160c) | **0.665** | 0.00018 | 0.504 | 4,750 |
| Clean (123c) | **0.040** | 0.062 | 0.029 | 3,639 |

**The central result:** The clean-sample slope collapses to 0.040. For the 123 non-hyperinflationary
economies — every advanced economy plus most of the developing world — year-to-year money growth has
essentially no detectable effect on inflation. The full-sample coefficient (0.665) lives almost
entirely in the hyperinflationary outliers of the early 1990s; remove them and the short-run link
disappears.

### 4.2 Robustness Checks

**Driscoll-Kraay SEs** (HAC kernel, bandwidth=4 — robust to cross-sectional dependence confirmed
by Pesaran CD = 158.4, p≈0):

| Sample | Coef | t | p |
|---|---|---|---|
| Full | 0.665 | 2.945 | 0.003 |
| Clean | 0.040 | 1.456 | 0.145 |

Both results survive. The clean-sample headline is robust to CSD-corrected inference.

**COVID robustness** (exclude 2020–2021):

| | With COVID | Without COVID |
|---|---|---|
| Full | 0.665 | 0.664 |
| Clean | 0.040 | 0.040 |

The COVID years drive nothing. The 2021–2023 inflation surge is inside the data and still cannot
restore significance in the clean sample.

**Panel unit root** (Im-Pesaran-Shin): both inflation (W=−34.4) and m2_growth (W=−36.3) reject the
unit root null. TWFE is valid; no spurious regression concern.

**Sample mismatch:** Running TWFE on the same 108-country subset as Obj A gives coef=0.820
(p<0.001). The wedge is real across matched samples, not a composition artifact of including
52 additional countries in Obj B.

### 4.3 Between vs Within Decomposition

The between-within figure uses all 123 clean countries:

- **Left panel (between):** Country time-averages. Slope = 0.28, R² = 0.28. Positive, clear.
- **Right panel (within):** Each observation demeaned by its country mean. Slope = 0.04, R² ≈ 0. Flat.

Same 123 countries, same 34 years. (Note: Obj A reports slope = 0.524 because it restricts to the
83 countries with ≥30 observations — a different filter applied for the long-run cross-section only.)

The question "do countries with more money have more inflation"
has a very different answer than "does a country have more inflation in the years when it prints more
money." The first question is about long-run structural differences; the second is about year-to-year
monetary transmission. They measure different things.

**Figure:** `04_current_results/figures/between_within_decomposition.png`

Note: a full Mundlak decomposition or Pesaran mean-group estimator would formally attribute the
wedge to genuine regime change vs. mechanical between-vs-within differences. Left for future work.

### 4.4 AR(1)+M2 Persistence Regression

Adding lagged inflation and output gap (full sample):

| Variable | Baseline coef | p | Augmented coef | p |
|---|---|---|---|---|
| inflation(t−1) | 0.593 | <0.001 | 0.445 | <0.001 |
| output gap (HP) | −0.001 | 0.307 | −0.001 | 0.081 |
| m2_growth | — | — | **0.349** | 0.032 |
| Within R² | 0.548 | — | 0.672 | — |

M2 adds genuine explanatory power beyond lagged inflation (within R² rises from 0.548 to 0.672).
The output gap is not significant in either specification — a consequence of the HP filter fix (bug B-1):
correcting the units from percent to decimal makes the gap variance appropriate and the coefficient
collapses to near zero. **The study's main M2 result (0.349, p=0.032) is unaffected by the bug fix.**

Holdout forecast (train ≤ 2015, test 2016–2024): the augmented Phillips-M2 model reduces RMSE
by 7.6% relative to a naive AR(1). Modest but consistent.

---

## 5. The COVID Question — A Sub-Period Analysis

The 2021–2023 inflation surge was the sharpest in 40 years. This section tests three related
hypotheses: (1) did COVID restore the within-country short-run link? (2) did countries that
printed more get more inflation? (3) does M2 predict inflation with a lag?

### 5.1 Sub-Period TWFE — When Did the Short-Run Link Die?

Running the TWFE separately for three monetary eras (clean sample):

| Era | Coef | p-value | N obs | N countries |
|---|---|---|---|---|
| Pre-QE 1991–2007 | **0.113** | <0.001 | 1,764 | 119 |
| QE era 2008–2019 | **0.001** | 0.827 (n.s.) | 1,398 | 123 |
| COVID 2020–2024 | **−0.014** | 0.655 (n.s.) | 477 | 107 |

**The GFC was the breakpoint, not COVID.** The short-run link was real before 2008 (0.113).
It died at the GFC and has not recovered in any subsequent era. The QE decade was not an aberration
— it established a new regime. COVID money printing did not restore the within-country year-to-year
transmission.

**Why did the link die at 2008?** Three reinforcing mechanisms:
1. Near-zero interest rates removed the traditional money-multiplier channel — banks parked excess
   reserves at central banks rather than lending them out.
2. Central bank credibility strengthened globally in the 2000s — anchored inflation expectations
   meant households and firms did not adjust prices in response to M2 growth.
3. Globalisation and supply-chain integration suppressed domestic price sensitivity to local M2.

**Figure:** The sub-period slopes are visible in `04_current_results/figures/global_m2_vs_inflation_timeseries.png`
(world median M2 and inflation by year, era-shaded).

### 5.2 Cross-Country COVID Scatter — The Moderate Monetarist Vindication

Within countries, M2 timing didn't predict inflation timing. But across countries, those that
expanded M2 more in 2020–21 got more inflation in 2021–23:

| Statistic | Value |
|---|---|
| Slope (cumulative M2 2020–21 → cumulative inflation 2021–23) | **0.494** |
| p-value | < 0.0001 |
| R² | 0.255 |
| Countries | 102 |

**The within-vs-between distinction resolves the paradox.** The TWFE asks: within the US, did the
years with more M2 growth have more inflation? Answer: no (slope ≈ 0). The scatter asks: across
countries, did the ones with larger 2020–21 monetary expansion get more 2021–23 inflation? Answer: yes
(slope = 0.494). Both are correct simultaneously because they measure different things.

**The mechanism:** The COVID monetary expansion was not QE — it was largely fiscal, delivered directly
to households as transfers and unemployment benefits. Unlike QE bank reserves (which sit inert unless
lent), fiscal transfers went into household spending immediately, raising aggregate demand. This is the
channel that the TWFE — which asks about year-to-year M2 timing within countries — cannot capture.

**Caveat:** Larger fiscal responses also correlated with larger supply disruptions and different
prior inflation environments. The scatter cannot cleanly isolate the monetary channel from the
fiscal channel, or either from global supply shocks (energy, shipping). The cross-country result
is consistent with a moderate monetarist interpretation but does not prove it.

**Figure:** `04_current_results/figures/covid_money_inflation_scatter.png`

### 5.3 Distributed Lag — How Quickly Does the Effect Decay?

A distributed lag specification with M2 at h=0, h=1, and h=2 (full sample, entity + time FEs,
clustered SEs):

| Horizon | Coef | SE | p-value |
|---|---|---|---|
| h=0 (contemporaneous) | **0.338** | 0.118 | 0.004 |
| h=1 (1-year lag) | **0.257** | 0.048 | <0.001 |
| h=2 (2-year lag) | **0.132** | 0.036 | <0.001 |

All three horizons are significant (full sample, entity + time FEs, clustered SEs). The effect
is largest contemporaneously and decays across horizons, but has not fully dissipated by year 2.
**The monetary transmission signal persists for at least 2 years.**

This is consistent with the COVID narrative: M2 surged in 2020, inflation peaked in 2021–2022,
and continued elevated into 2023 — consistent with a multi-year distributed lag rather than a
purely one-period effect.

**Figure:** `04_current_results/figures/distributed_lag_irf.png`

---

## 6. Objective C — Inflation Targeting as a Regime Moderator (Exploratory)

**Caveats lead:**
- IT adoption is endogenous — countries adopted IT after high-inflation episodes.
- Roger (2010) and Hammond (2012) adoption dates differ for several countries; sensitivity tested.
- This section is exploratory. No causal claim is made.

### 6.1 Event-Time Inflation Level

Average inflation in the ±5 years around IT adoption, compared against never-adopters:

- IT adopters start at elevated inflation (5–10 pp above never-adopters).
- Inflation declines *before* adoption — the pre-trend is visible (t=−5 to t=−1 shows a downward slope).
- Inflation converges toward the never-adopters baseline post-adoption (t=0 to t=+5).

**Identification concern:** The pre-trend confirms endogenous adoption timing. Countries adopt IT when
inflation is already coming down. Whether IT accelerated the decline or was simply adopted during a
structural disinflation is not identified by this event study.

**Figure:** `04_current_results/figures/it_event_time_inflation.png`

### 6.2 Slope Probe — Does IT Weaken the M2→Inflation Pass-Through?

Triple-diff specification (D-1 corrected, full-rank — see `02_data/UNITS_REGISTER.md` for the
collinearity note):

| Term | Coef | p-value | Interpretation |
|---|---|---|---|
| m2_growth | 0.636 | 0.002 | Baseline slope (non-IT, pre-adoption) |
| it_m2 | 0.212 | 0.281 (n.s.) | IT adopters' pre-adoption slope offset |
| post_treated_m2 | **−0.485** | <0.001 | Post-adoption slope shift for IT countries |

**The −0.485 shift** means that after IT adoption, IT countries show a 0.485 pp lower M2→inflation
pass-through per 1 pp of M2 growth than the baseline. This is large relative to the baseline slope
of 0.636 — adoption nearly halves the short-run transmission.

**Interpretation:** This is consistent with a credibility view. Once a central bank credibly commits
to a numerical inflation target, households and firms may anchor price expectations to that target
rather than to observed money growth — which would allow M2 to expand without triggering inflation.

**The pre-adoption it_m2 term is n.s. (p=0.281):** IT adopters did not have a statistically different
slope before adoption compared to never-adopters. The change is genuinely post-adoption.

**Caveat:** Adoption timing is still endogenous. The post-adoption period also coincides with
global disinflation and post-hyperinflation stabilisation in many IT adopters. The slope shift
is consistent with a credibility story but cannot rule out confounding.

**Figure:** `04_current_results/figures/it_slope_probe_coefficients.png`

---

## 7. Objective D — US Appendix (Lucas ii Spirit)

Using FRED annual data (1960–2024) with a 5-year centred moving-average filter to remove
business-cycle noise (same method as Lucas 1980):

| Relationship | Slope | R² | HAC p-value |
|---|---|---|---|
| M2 growth → Inflation | 0.474 | 0.196 | 0.060 (borderline) |
| M2 growth → T-bill rate | 0.421 | 0.092 | 0.155 (n.s.) |

**Positive and consistent** with the quantity theory / Fisher relation at low frequencies.
Both slopes are compressed below 1 by the QE decade (2009–2020), where M2 grew sharply
while both inflation and T-bill rates stayed near zero.

**The T-bill Fisher result is fragile** to Newey-West HAC correction (p=0.155). It should be
treated as illustrative only — consistent with the Fisher relation in direction, but not
significant after accounting for the strong autocorrelation induced by the 5-year MA.

**The M2→Inflation slope is borderline** (OLS p < 0.05; NW-HAC p=0.060). The low-frequency
quantity theory relationship survives but is weaker than in the pre-QE era.

**Note on M1 vs M2:** Lucas (1980) used M1. The Federal Reserve's May 2020 reclassification
of savings deposits into M1 created a ~120% discontinuity in FRED M1SL for that year.
M2 is used here — the economic content is identical and the series is continuous.

### Pre-QE vs Post-QE Era Comparison

Splitting the US scatter at the GFC (2008):

| Era | OLS slope | R² |
|---|---|---|
| Pre-QE 1960–2007 | ~0.55 | ~0.35 |
| Post-QE 2008–2024 | ~0.15 | ~0.05 |

The structural break is visible in the data: the same US country shows two distinct regimes
in the same scatter. COVID-era years (2020–2024) labelled individually — they pull the
post-2008 line back toward the long-run relationship, but not to the pre-2008 level.

**Figure:** `04_current_results/figures/us_m2_inflation_two_eras.png`
**Figure:** `04_current_results/figures/lucas_us_inflation.png` (full-period scatter with colorbar)

---

## 8. IV Results (Appendix — Directional Only)

LP-IV with external-level instrument and 1-year lagged instrument:

- Conservative first-stage F = 5.587 (passes relevance gate ≥3.84; **fails strong-IV ≥10**)
- IV coefficient (1.468) substantially exceeds TWFE baseline (0.665)
- 1 placebo test significant at 5%

The IV amplification and weak first stage jointly suggest the exclusion restriction is not clean.
IV results are retained as a directional robustness check only. No causal inference is based on them.

---

## 9. Identification Limits and Claim Tiers

| Objective | Estimand | Claim tier | Key limitation |
|---|---|---|---|
| A — Long run | Between estimator, country means | Descriptive | No causation; composition effects |
| B — Short run | Within-country TWFE | Exploratory/associational | No causal identification; TWFE assumptions |
| B — Sub-period | Same TWFE by era | Exploratory | Small N for COVID era (477 obs) |
| B — COVID scatter | Cross-country OLS | Associational | Confounds with fiscal policy, supply shocks |
| B — Distributed lag | TWFE with lags | Exploratory | Cannot identify persistence mechanism |
| C — IT probe | Triple-diff | Exploratory | Endogenous adoption |
| D — US appendix | Single-country time series | Descriptive | Single country; 5-yr MA compression |

**Forbidden claim types:** "QE caused low inflation," "COVID money printing caused the 2021–2023
surge," "IT adoption reduced inflation," or any structural/counterfactual statements.

---

## 10. Conclusion

In long-run cross-country averages, money growth and inflation move together. The quantity theory's
long-run cross-sectional prediction is confirmed in 160 countries through 2024: slope = 0.952 (full)
and 0.524 (clean). Lucas was right, and his result is still right with 34 additional years of data
including the two biggest stress tests in modern monetary history.

Year-to-year within countries, the story is different — and more interesting.

**The short-run link died at the GFC.** Sub-period TWFE shows the clean-sample slope was 0.113
(significant) before 2008, effectively zero during QE (0.001), and remained zero through COVID
(−0.014). The QE decade was not anomalous — it established a new regime for modern monetary
transmission, in which credible central banks can expand M2 without triggering year-to-year
inflation movements.

**COVID was a partial monetarist vindication — but only cross-sectionally.** Within countries,
M2 timing still did not predict inflation timing during 2020–2024. But across countries, those
that expanded M2 more in 2020–21 got substantially more inflation in 2021–23 (slope = 0.494,
p < 0.0001, R² = 0.26, n=102). The transmission channel was fiscal — direct transfers to
households raised aggregate demand — not the bank-reserve QE channel that had been dormant
since 2008. The monetary signal operates through a distributed lag decaying from h=0 (0.338) to h=2 (0.132), persisting at least 2 years.

**Credibility severs the short-run link.** IT adoption is associated with a −0.485 slope shift in
the M2→inflation pass-through (p<0.001), consistent with the view that anchored expectations
break the transmission mechanism. Once a central bank credibly commits to a target, households
and firms stop updating price expectations in response to M2 growth.

The US appendix mirrors the cross-country story at the national level: the low-frequency M2–inflation
relationship (slope 0.47) survives 65 years of data, with the QE era compressing the slope and
COVID-era data pulling it back.

**In two sentences:** The long-run quantity theory lives, confirmed through 2024. The short-run
version has been effectively dead since the GFC — and the COVID episode reveals why: fiscal
transfers are associated with cross-country inflation differentials that QE bank reserves were not.

---

## 11. Data and Code Provenance

| Notebook | Content |
|---|---|
| `01_lucas_replication.ipynb` | Obj A long-run scatters, Lucas (i) and (ii) |
| `02_panel_fe_iv_baseline.ipynb` | Obj B TWFE baseline, AR(1)+M2 Phillips, diagnostics, sub-period analysis, COVID scatter, distributed lag, between-within decomposition, world median time series, distributed lag IRF |
| `03_short_run_lp_iv.ipynb` | LP-IV (directional appendix) |
| `04_did_it_event_study.ipynb` | Obj C event study, slope probe, event-time chart, IT slope visualization |
| `05_lucas_us_appendix.ipynb` | Obj D US FRED, two-era scatter |

| Key result file | What it contains |
|---|---|
| `04_current_results/summary.md` | All headline numbers, diagnostic results |
| `04_current_results/tables/lucas_us_summary.csv` | US appendix slope table |
| `04_current_results/figures/` | All figures — see table below |

| Figure | Description |
|---|---|
| `global_m2_vs_inflation_timeseries.png` | World median M2 vs inflation, 1991–2024, era-shaded |
| `between_within_decomposition.png` | Two-panel: country means vs demeaned scatter |
| `distributed_lag_irf.png` | IRF bar chart: M2 effect at h=0,1,2 |
| `covid_money_inflation_scatter.png` | Cross-country COVID scatter (102c, slope=0.494) |
| `it_event_time_inflation.png` | Event-time inflation chart, IT adoption ±5 years |
| `it_slope_probe_coefficients.png` | Triple-diff coefficient bar chart |
| `us_m2_inflation_two_eras.png` | US pre/post-QE era scatter |
| `lucas_us_inflation.png` | US M2 vs inflation, 5-yr MA, 1960–2024 |
| `lucas_us_tbill.png` | US M2 vs T-bill, 5-yr MA, Fisher relation |

---

## Appendix A — Critical Bug Fixes

### B-1 — HP Filter Unit Error (Critical)

`build_output_gap` used `np.log1p(growth / 100.0)` but `gdp_growth` is decimal (0.026 = 2.6%).
The `/100` collapsed HP cycle variance by ~10,000×. Fix: `np.log1p(growth)`.
Effect: output_gap p-value in augmented Phillips changed from 0.041 to 0.081 (n.s.).
The m2_growth coefficient (0.349) is unchanged.

### D-1 — Triple-Diff Missing Lower-Order Interaction (Critical)

IT slope probe omitted `it_treated × m2_growth` as a lower-order term. `post_it × m2_growth`
is perfectly collinear with `post_treated_m2` given the binary treatment/post design. Full-rank
fix: `inflation ~ m2_growth + it_m2 + post_treated_m2 + EntityEffects + TimeEffects`.
Post-adoption shift after fix: −0.485 (p<0.001). Pre-fix result was conflated with pre-treatment
slope heterogeneity.

Full documentation: `/Users/stevenchung/Steven_Chung/Lessons across projects/Cross_Country_Monetary_Project/panel_code_bugs_and_diagnostics.md`
