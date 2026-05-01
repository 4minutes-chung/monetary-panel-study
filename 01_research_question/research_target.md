# Research Target Contract (Master Source of Truth)

## 0. Contract Authority

This file is the single contract for:

- research question and objective structure,
- claim tiers and interpretation limits,
- canonical run order and output targets,
- definition of done for the current cycle.

If any other document conflicts with this file, this file wins.

## 1. Research Question

Across countries, how does money growth relate to inflation and GDP growth?

The report follows a single arc on one panel:

1. Lucas (1980) intro — what the long-run cross-country fact is supposed to look like.
2. Empirical step-by-step on money:
   - Objective A: AVERAGE — country-mean (long-run) estimate.
   - Objective B: YoY — within-country (short-run) dynamic estimate.
3. Policy regime layer:
   - Objective C: inflation-targeting (IT) adoption as a regime moderator on the YoY slope.

The contribution is the wedge between the AVERAGE estimate (Obj A) and the YoY estimate (Obj B), with IT used to ask whether the regime moderates that gap.

## 2. Objectives

### Objective A — AVERAGE (Lucas-style, long-run)

- Country-mean money growth vs country-mean inflation, n ≈ 163 (aligns with Lucas’s **first** quantity-theoretic illustration in cross-section / long-average spirit).
- Country-mean money growth vs country-mean **GDP growth** — **descriptive only**; this is **not** Lucas’s **second** illustration. In Lucas (1980), the second illustration is money growth vs **nominal interest rates** (U.S. T-bill rate with filtered quarterly data). The current panel lacks a harmonized nominal rate series, so that leg is **out of scope** until extended. Extension options (paths, time budgets, pitfalls) are spelled out here: **`02_data/supporting/lucas_ii_nominal_rate_plan.md`**.

#### Lucas (ii) — how to proceed when unsure

Default under time constraint: stay on **Path A** in `lucas_ii_nominal_rate_plan.md` (no new data—clear verbal caveat only). Use **Path B** for a credible **US‑only appendix** (~1–3 hours). Reserve **Path C** for multi‑country merges only if you revisit the repo as data work—not required for YoY Obj B/C.

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

From project root:

1. Read `README.md` and `CODE_GUIDE.md`.
2. Run or inspect notebooks in `03_analysis_notebooks/`.
3. Use outputs in `04_current_results/` for claims.
4. Optional rebuild:
   - `python3 -m pip install -r 90_reproduction_scripts/requirements.txt`
   - `python3 90_reproduction_scripts/run_rebuild.py`
   - `python3 90_reproduction_scripts/build_graphs.py`

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
