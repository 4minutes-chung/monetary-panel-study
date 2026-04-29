# LLM Council Reading List: Objective B Hardening

Date: 2026-04-28
Companion file: `06_study_notes/LLM_rec_Objb_plan.md`
Source: synthesis of `super-claude`, `model-review-math-econ`, and the 5 LLM-council advisors.

## How to read this list

Items are split into three tiers:

1. **48-hour core** — read this week. Each one fixes a specific weakness in the current Objective B.
2. **Next-cycle** — useful if Objective B is revisited beyond the deadline.
3. **Skip in this window** — books and surveys flagged as out-of-budget (kept for traceability).

For each item: a 1-line "what it gives you that you currently lack."

---

## Tier 1 — 48-hour core (read first)

### 1. Teles, P., Uhlig, H., & Valle e Azevedo, J. (2016). *Is the Quantity Theory Still Alive?* Economic Journal.
- Fixes: the regime-dependence framing for your 87.5% stability drift.
- Use: empirical template for "money-inflation relationship has weakened post-1990s." Justifies the split-sample headline table directly.
- Single most useful paper for your 2–3 day window.

### 2. Sargent, T. J., & Surico, P. (2011). *Two Illustrations of the Quantity Theory of Money.* American Economic Review.
- Fixes: regime-break interpretation of the 1991–2005 vs 2006–2020 coefficient collapse.
- Use: cite once, in one new sentence in `05_final_writing/report_draft.md` Section 5.

### 3. De Grauwe, P., & Polan, M. (2005). *Is Inflation Always and Everywhere a Monetary Phenomenon?* Scandinavian Journal of Economics.
- Fixes: between vs within distinction; explains why pooled cross-country slopes overweight high-inflation regimes.
- Use: justifies the hyperinflation-trim column in the headline table without changing the model.

### 4. Andrews, I., Stock, J. H., & Sun, L. (2019). *Weak Instruments in IV Regression: Theory and Practice.* Annual Review of Economics.
- Fixes: justifies *dropping* IV from the headline.
- Use: read only the intro and the "what AR confidence sets do and don't fix" section. Cite once, to motivate why you do not report AR sets at partial R² = 0.003.

### 5. Lee, D. S., McCrary, J., Moreira, M. J., & Porter, J. (2022). *Valid t-ratio Inference for IV.* American Economic Review.
- Fixes: tells you what nominal-5% IV t-tests actually require. The "t-ratio = 4.05" rule.
- Use: one footnote / one paragraph in your Diagnostics & Limits section. At your F ≈ 4, your nominal-5% IV t-stats are not 5%-valid; this is the citation.

---

## Tier 2 — next cycle (after the deadline, only if revisiting)

### 6. Olea, J. L. M., & Pflueger, C. (2013). *A Robust Test for Weak Instruments.* Journal of Business and Economic Statistics.
- Fixes: the right "first-stage F" to report under heteroskedasticity / clustering. Replaces the χ²(1) / "≥10" rule.
- Skip in 48h: implementing the Olea-Pflueger effective F properly takes more than the deadline allows; the current package's "≥10" heuristic is wrong but the conservative gate already fails by other criteria.

### 7. Stock, J. H., & Watson, M. W. (2018). *Identification and Estimation of Dynamic Causal Effects in Macroeconomics Using External Instruments.* Economic Journal.
- Fixes: the LP-IV inference framework you are missing.
- Skip in 48h: needed only if LP-IV stays in the headline. Per the council, it should not.

### 8. Plagborg-Møller, M., & Wolf, C. K. (2021). *Local Projections and VARs Estimate the Same Impulse Responses.* Econometrica.
- Fixes: gives you the equivalence result that justifies the LP-IRF as a descriptive object even when point identification is weak.
- Skip in 48h: useful for a future "stylized fact" framing of the LP-IRF (Expansionist's `regime_pass_through_brief.md`).

### 9. Montiel Olea, J. L., & Plagborg-Møller, M. (2021). *Local Projection Inference is Simpler and More Robust Than You Think.* Econometrica.
- Fixes: lag-augmentation for LP-IV inference.
- Skip in 48h: only relevant if LP-IV is rebuilt.

### 10. Borusyak, K., Hull, P., & Jaravel, X. (2022). *Quasi-Experimental Shift-Share Research Designs.* Review of Economic Studies.
- Fixes: the right way to think about your `depth_base × FedFunds_mean` instrument as a shift-share / Bartik exposure.
- Skip in 48h: contrarian advisor wanted this for a fragility paper. Council majority says do not pursue in this window.

---

## Tier 3 — skip in this window (reference only)

- **Aizenman, Chinn & Ito (2010s Trilemma indexes)** — relevant only if reconstructing the external instrument.
- **Mertens & Ravn (2013 narrative monetary shocks)** — relevant only if constructing narrative shocks (council stop list).
- **Romer & Romer (2004 narrative shocks)** — same as above.
- **Nakamura & Steinsson (2018 monetary policy effects)** — relevant only for a high-frequency monetary shock pivot.
- **Estrella & Mishkin (1997)** — older long-run money-inflation literature; covered already by McCandless–Weber.
- **McCandless, G. T., & Weber, W. E. (1995). Some Monetary Facts. Minneapolis Fed Quarterly Review.** — cite if convenient; the long-run cross-country fact is already widely known.
- **Rambachan & Roth (2023, honest DiD)** — relevant only if Objective B becomes a parallel-trends design; not the case here.

---

## Practical reading slots (2–3 day budget)

Suggested slotting against the finish plan in `LLM_rec_Objb_plan.md`:

| Slot | Item | Time | Output that depends on this |
| --- | --- | --- | --- |
| Day 1 morning | Teles–Uhlig–VeA (#1) | 90 min | Regime-split headline table; new sentence in report Section 5 |
| Day 1 afternoon | Sargent–Surico (#2), De Grauwe–Polan (#3) | 60–90 min | Hyperinflation-trim column; tail-leverage interpretation |
| Day 2 morning | Andrews–Stock–Sun (#4) intro only | 30 min | Diagnostics & Limits paragraph: why AR sets are not reported |
| Day 2 afternoon | Lee–McCrary–Moreira–Porter (#5) one paragraph | 15 min | One-sentence footnote on nominal IV t-stats |
| Day 3 | No new reading | — | Final QA |

---

## Cross-reference

This reading list is purely advisory. The final package's claim boundary is fixed by:
- `01_research_question/research_target.md`
- `01_research_question/claim_boundary.md`

Citations land in:
- `05_final_writing/report_draft.md` Section 5 (headline result + regime sentence)
- `05_final_writing/technical_appendix.md` (Diagnostics & Limits citations)
- `06_study_notes/econometric_caveats.md` (existing file; can absorb the weak-IV-robust caveat)
