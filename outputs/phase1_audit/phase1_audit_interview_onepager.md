# Phase 1 Interview One-Pager (Script)

## 15-Second opener
I built a cross-country monetary project, audited it with hard thresholds, and then made a disciplined pivot. The audit result was `GO_PIVOT_SHORT_RUN` because IV strength, stability drift, and placebo tests failed the gate.

## 60-Second narrative
1. I started with long-run panel evidence and got a consistent positive money-growth to inflation signal.
2. I did not treat significance as success. I ran a formal audit with fixed rules: first-stage strength, sign stability, drift threshold, GDP-neutrality consistency, and placebo validity.
3. Three criteria failed:
- Preferred first-stage was below threshold (`F≈9.47 < 10`).
- Coefficient drift was too large (`~87.5%`, threshold `<40%`).
- One placebo test was significant.
4. So I pivoted to a short-run design using panel local projections + shock IV (horizons 0-3), which is a better fit for policy-effectiveness questions.

## Why this is useful (business-facing)
- It demonstrates model risk discipline, not p-hacking.
- It shows I can turn a weak/fragile research path into a stronger applied path quickly.
- It produces chart-ready outputs for communication (Power BI-friendly tables + IRF-style figures).

## If asked “what did you learn?”
- High R-squared or strong coefficients are not enough.
- Identification quality and robustness stability are the real decision criteria.
- A good analyst kills weak narratives early and reallocates effort.

## If asked “what are you doing next?”
- I’m executing the short-run project with LP-IV on annual panel data.
- Outcomes: inflation and GDP growth at horizons 0,1,2,3.
- Deliverables: reproducible notebook, impulse-response tables/plots, and concise interpretation memo.

## 20-Second close
The strongest signal from this project is not the original coefficient. It is the audit process and the decision quality: explicit gates, transparent failure conditions, and a clean pivot to a more defensible design.
