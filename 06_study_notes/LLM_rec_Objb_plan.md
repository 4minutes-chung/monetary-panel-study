# LLM Council Recommendation: Objective B Re-Plan

Date: 2026-04-28
Status: Read-only strategic recommendation. Not yet implemented.
Companion file: `06_study_notes/LLM_rec_Objb_reading_list.md`

## What this document is

A consolidated recommendation produced by:
- `super-claude` (rigorous re-plan)
- `model-review-math-econ` (technical / identification critique)
- `llm-council` workflow: 5 advisors (Contrarian, First-Principles, Expansionist, Outsider, Executor) → 5 anonymous peer reviewers → chairman synthesis.

Question framed to the council: should Objective B (FE + IV + LP-IV for cross-country money growth → inflation and GDP, 163 countries × 1991–2020, 4,292 obs) be (a) shipped as-is, (b) hardened, or (c) restructured, given a 2–3 day deadline?

Current diagnostics (verbatim from `04_current_results/`):
- FE-TWFE inflation coef = 0.5706 (p = 2.83e-06); GDP coef = -0.008 (p = 0.395).
- IV-TWFE (`instrument_m2_external_level` = depth_base × FedFunds_mean): inflation coef = 1.033 (p = 1e-04); GDP coef = -0.120 (p = 0.157).
- First-stage clustered Wald χ²(1) = 4.22 (country) / 3.80 (country+year). Partial R² = 0.003.
- Strong-IV (≥10): FAIL. Conservative relevance (>3.84): FAIL.
- Stability drift 1991–2005 vs 2006–2020 = 87.5%. Lead placebo p = 0.039.
- LP-IV inflation horizons: 1.03, 0.66, 0.57, 0.55 (unadjusted, weak-IV-sensitive).
- Audit recommendation: `GO_PIVOT_SHORT_RUN`.

---

## Council Verdict

### Where the council agreed

1. Do not ship Objective B as a causal story. 5/5 advisors agree; the math review independently flags HARD FAIL on weak-IV inference, exclusion, LP-IV inference, stability, and tail-leverage.
2. The one robust fact in the package is the FE inflation slope: **0.5706 (p ≈ 3e-6, n = 4,292, 163 countries)**.
3. The instrument story is dead in the 2–3 day window. Lead placebo p = 0.039, partial R² = 0.003, depth_base is effectively time-invariant per country and absorbs into entity effects. No reading or inference upgrade fixes this in 48 hours.
4. The 87.5% stability drift is the most important quantitative finding in the audit. Pooled FE is internally inconsistent with this drift; the project currently understates it.

### Where the council clashed

| Advisor | Position | Reviewer judgment |
| --- | --- | --- |
| First-Principles | Restructure to between/within QTM decomposition; drop IV/LP-IV | Theoretically cleanest, but a 1–2 week rewrite |
| Executor | Harden + ship: add Anderson-Rubin + Olea-Pflueger; rewrite causal language | **Biggest blind spot** — weak-IV-robust inference does not fix exclusion violation; AR sets at R² = 0.003 are typically near-unbounded |
| Contrarian | Restructure to fragility/null-finding paper; β = 1.03 → 0.12 under tail trim is the actual finding | Sharpest econometric diagnosis, but fragility-paper publication ambition exceeds 48h |
| Expansionist | Restructure framing; audit framework is the deliverable; 3 portfolio artifacts | Right *long-horizon* repositioning, not the right 48h move |
| Outsider | 80/20 reorder: lead with FE 0.57, hyperinflation-trim column, "cannot-claim" box | **4/5 reviewers picked this** as the only option that fits the deadline |

### Blind spots the council caught (Round 2 + math review)

1. **Lead placebo p = 0.039 is an exclusion-restriction violation, not a weak-IV symptom.** Anderson-Rubin / Olea-Pflueger fix relevance, not exogeneity.
2. **Pooled FE is also misspecified given 87.5% drift.** None of the five advisors proposed split-sample FE as the *headline* table.
3. A 30-minute global-shock control test (e.g., region × year FE, or oil/commodity-cycle controls) is missing as a check on whether the 1991–2005 vs 2006–2020 break is a Volcker / GFC artifact.
4. AR confidence sets at partial R² = 0.003 are typically near-unbounded. Reporting them next to a failing placebo is cosmetic cover.
5. The audience question was never asked. Portfolio reader, referee, and committee each demand a different framing.
6. The β = 1.03 (IV) vs β = 0.57 (FE) gap is mechanically consistent with weak-IV bias toward the hyperinflation-leveraged subsample. The math review confirmed: top-1% trim collapses β from 0.57 to 0.12.

### Math review (model-review-math-econ) verdicts

| Section | Verdict |
| --- | --- |
| Weak-IV inference (clustered χ²(1) is wrong; should be Olea-Pflueger or Lee-McCrary tF) | HARD FAIL |
| Instrument exclusion (`depth_base × FedFunds_mean` post-TWFE; depth time-invariant; FFR has direct non-monetary channels) | HARD FAIL |
| LP-IV inference (no lag-augmentation; weak-IV propagates across horizons; multiple testing) | HARD FAIL |
| Stability and placebo (87.5% drift rejects pooled-FE homogeneity; lead placebo points to instrument autocorrelation) | HARD FAIL |
| Clustering and dof (4.22 → 3.80 under two-way is the standard dof penalty) | SOFT FAIL |
| Decimal unit and tail effects (β headline is hyperinflation-leverage-driven; tail trim → 0.12) | HARD FAIL |

---

## The Recommendation

**Do Outsider's reorder. Add one regime-split table the council missed. Refuse the rest.**

### Adopt
- Outsider's 80/20 reorder of the final package. The package leads with the robust FE result, with hyperinflation-trim and regime-split columns next to it. IV / LP-IV is moved to a clearly labeled Diagnostics & Limits section.

### Add (round-2 catch missed by all 5 advisors)
- The **regime-split FE table is the headline diagnostic, not pooled FE alone**. This converts the 87.5% drift from a failure into a finding: "the cross-country money-inflation slope is regime-dependent — strong pre-2005, near-zero post-2005."

### Refuse (in the 48h window)
- Executor's AR / Olea-Pflueger bolt-on. Cosmetic over an exclusion violation.
- Contrarian's fragility-paper publication ambition.
- First-Principles' full QTM rewrite.
- Expansionist's three-artifact repositioning (good idea, but post-deadline).

---

## Concrete inclusion list for the final package

- **Headline table** in `05_final_writing/report_draft.md` Section 5.1: FE inflation slope with three columns side-by-side
  1. full sample (current 0.5706)
  2. hyperinflation top-1% trim (≈ 0.12 per the existing `spec_stability_table.csv`)
  3. 1991–2005 vs 2006–2020 split (existing `spec_gate_table.csv`).
- **One scatter** for the front matter: country-mean money growth vs country-mean inflation, QTM 45° reference line, hyperinflation tail flagged.
- **One "cannot-claim" box** with the verbatim text from `01_research_question/claim_boundary.md`.
- **Diagnostics & Limits section**: relabel everything currently in `04_current_results/tables/phase1_audit/` as transparency assets, not headline evidence.
- **One new sentence** for `05_final_writing/report_draft.md` Section 5: "the cross-country money-inflation slope is regime-dependent — strong pre-2005, near-zero post-2005 — which is consistent with Sargent & Surico (2011) and Teles–Uhlig–Valle e Azevedo (2016)."

---

## The one thing to do first

Reorder the final package so the FE 0.57 slope, with hyperinflation-trim and regime-split columns, is the first table a 30-second reader sees — and the IV / LP-IV is below the fold in a Diagnostics & Limits section. Nothing else in the next 48 hours.

---

## Stop list (do not do in this window)

1. No new instrument hunt.
2. No shift-share / Bartik construction.
3. No narrative monetary shocks.
4. No Bayesian VAR pivot.
5. No new dataset / data collection.
6. No bolt-on weak-IV-robust bands as cosmetic cover for an exclusion failure.
7. No fragility-paper publication framing in this window.

---

## Sequencing (post-deadline, optional)

- After ship: convert the same artifacts into Expansionist's three repositioning files (`audit_discipline_note.md`, `regime_pass_through_brief.md`, `interview_narrative.md`). 1–2 weeks.
- Only after that: First-Principles' between/within QTM rewrite or Contrarian's fragility framing.
