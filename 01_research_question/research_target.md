# Research Target Contract (Master Source of Truth)

## 0. Contract Authority

This file is the single contract for:

- research question and objective structure,
- claim tiers and interpretation limits,
- canonical run order and output targets,
- definition of done for the current cycle.

If any other document conflicts with this file, this file wins.

## 1. Research Question

Does the quantity theory of money — the long-run one-for-one mapping between money growth and inflation — hold in the post-QE, post-COVID era?

The canonical cross-country evidence (McCandless & Weber 1995; De Grauwe & Polan 2005) predates the 2008 financial crisis, quantitative easing, and the 2021–2023 inflation surge. This project updates that evidence with 160 countries through 2023 — a sample that contains both the "money without inflation" QE decade and the sharpest inflation episode in 40 years.

The report follows a single arc on one panel:

1. Lucas (1980) intro — the long-run cross-country benchmark; what a one-for-one money-inflation relationship is supposed to look like.
2. Empirical decomposition on that benchmark:
   - Objective A: AVERAGE — country-mean (long-run) estimate. Does the long-run fact survive 1991–2023?
   - Objective B: YoY — within-country (short-run) dynamic estimate. How much of money growth actually becomes inflation year-to-year?
3. Regime layer:
   - Objective C: inflation-targeting adoption as a moderator on the YoY slope. Does IT explain why short-run pass-through weakened?
4. US reference:
   - Objective D: Lucas's second illustration (money growth vs nominal interest rate) for the United States — the Fisher chain that cross-country data cannot test.

The central finding is the **wedge between Obj A and Obj B**: the long-run association is strong and robust; the short-run pass-through is smaller, regime-dependent, and weaker in the post-GFC sample. IT is one candidate explanation. The COVID surge is the out-of-sample test.

**Why the sample period matters:** M2 expanded massively after 2008 via QE (central bank reserves, not circulating money), and inflation remained low until 2021. That structural break in the money-inflation link is inside this panel and not present in the two canonical papers.

## 2. Objectives

### Objective A — AVERAGE (Lucas-style, long-run)

- Country-mean money growth vs country-mean inflation — 105 countries with ≥30 annual observations. Aligns with Lucas’s **first** quantity-theoretic illustration.
- Country-mean money growth vs country-mean **GDP growth** — descriptive only; not Lucas’s second illustration.
- Lucas’s **second** illustration (money vs nominal interest rate) is handled by **Objective D** (US-only, `05_lucas_us_appendix.ipynb`). Cross-country nominal rates are not harmonized in this panel.

### Objective B — YoY (within-country, short-run)

- Pooled / two-way fixed-effect inflation regression on money growth.
- Phillips-style block: lagged inflation + output gap predicting current inflation.
- Local projection IV (LP-IV) for short-run dynamics, with fixed-sample lock across horizons and Holm familywise correction across inflation horizons.
- IT may appear here only as a stratified comparison (adopter vs never-adopter).
- Exploratory. Quantifies the short-run pass-through.

### Objective C — IT regime layer (exploratory probe)

- Headline probe: slope-shift interaction `post_it × treated × m2_growth` on inflation.
- Companion: TWFE level event-study, kept explicitly as an exploratory appendix object.
- Caveats lead the section: adoption is endogenous to prior inflation, dates differ across Roger (2010) vs Hammond (2012), level-shift and slope-shift are distinct estimands.
- No headline causal claim in this cycle.

## 3. Claim Tier Discipline

- Objective A: descriptive.
- Objective B: exploratory.
- Objective C: exploratory probe (not causal).
- If identification gates fail, claims stay non-causal regardless of sign or significance.

## 4. Identification Gate Framework

Preferred IV for gate decisions: `instrument_m2_external_level` in the inflation core IV spec.

Two clustering checks are always computed:

- country clustering,
- country + year clustering.

Conservative gate values:

- conservative first-stage stat = min(one-way stat, two-way stat),
- conservative first-stage p = max(one-way p, two-way p).

Canonical gates:

- relevance gate: conservative stat > 3.8415 and conservative p < 0.05,
- strong-IV label: conservative stat ≥ 10.0.

Placebo rule:

- placebo p must be empirical two-sided randomization p,
- placebo diagnostics must be disclosed.

## 5. Canonical Execution Path

1. Read `README.md` and this file.
2. Open and run notebooks in `03_analysis_notebooks/` (order: `01` → `02` → `03` → `04` → `05`).
3. Use outputs in `04_current_results/` for claims.

## 6. Canonical Outputs

- `04_current_results/summary.md`
- `04_current_results/tables/phase1_audit/`
- `04_current_results/tables/short_run_lp/`
- `04_current_results/figures/`
- `05_final_writing/`

## 7. Definition of Done

A cycle is done only when:

1. Clean run reproduces canonical outputs.
2. Scorecard and summary use the same conservative gate logic.
3. The YoY block reports fixed-sample and familywise-adjusted inference.
4. The IT regime section opens with caveats before any treatment-effect number.
5. Narrative language matches measured diagnostics and claim tiers.

---

## 8. Objective D — US-Only Lucas (ii) Appendix (added 2026-05-03)

**Purpose:** Replicate Lucas (1980)'s second illustration for the United States only — money growth vs nominal interest rates in low-frequency / moving-average filtered data. This is the leg the cross-country panel cannot do (no harmonized rate series). Framed explicitly as a pedagogical appendix, not a cross-country claim.

**Estimand:** Low-frequency co-movement between M2 growth, CPI inflation, and the nominal short rate (US only, annual 1960–2024 or longest available).

**Data sources (all FRED):**

| Series         | FRED code  | Notes                        |
| -------------- | ---------- | ---------------------------- |
| M2 money stock | `M2SL`     | Monthly, seasonally adjusted |
| CPI all items  | `CPIAUCSL` | Monthly, seasonally adjusted |
| 3-month T-bill | `TB3MS`    | Monthly, secondary market    |

Annualise by taking December observation or annual average — document which.

**Method:**

1. Compute annual log changes: `m2_growth = log(M2_t / M2_{t-1})`, same for `inflation` from CPI.
2. Convert T-bill from percent to decimal (`/ 100`).
3. Apply a centred moving-average filter (window = 5 years) to each series — this is the "low-frequency" filter Lucas used to strip business-cycle noise.
4. Scatter plots:
   - Plot A: filtered M2 growth vs filtered inflation (should be near 45-degree line).
   - Plot B: filtered M2 growth vs T-bill rate (Fisher / QTM prediction).
5. Add OLS fit line + R² to each scatter.

**Outputs:**

- Notebook: `03_analysis_notebooks/05_lucas_us_appendix.ipynb`
- Figures: `04_current_results/figures/lucas_us_inflation.png`, `lucas_us_tbill.png`
- One-row CSV summary: `04_current_results/tables/lucas_us_summary.csv` (slope, R², n)

**Claim tier:** Descriptive / pedagogical. Single country, no causal claim. Label as appendix in the report.

**Framing in report:** "Lucas's second illustration links money growth to nominal interest rates using US quarterly data. We reproduce the spirit of that exercise using annual FRED data and a 5-year moving-average filter. The results are consistent with the Fisher relation but are single-country descriptive evidence only."

**What not to do:**

- Do not pool with the cross-country panel.
- Do not label this as a replication of Lucas's exact filters (he used a different MA specification).
- Do not make policy claims.
