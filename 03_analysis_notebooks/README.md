# Notebook Guide

This folder contains the analysis notebooks. The paper should be read by claims, not by every exploratory branch.

## Run Order

| Order | Notebook | Role |
|---:|---|---|
| 1 | `01_lucas96_mcweber_replication.ipynb` | Long-run country-average money-inflation benchmark, Lucas (1996) / McCandless-Weber framing |
| 2 | `02_money_inflation_twfe.ipynb` | Main short-run TWFE spine: full/clean sample, pre/post-2008, compact robustness, between-vs-within |
| 3 | `02b_money_inflation_exploratory.ipynb` | Appendix diagnostics: Driscoll-Kraay sensitivity and cumulative distributed-lag scaffold |
| 4 | `03_short_run_lp_iv.ipynb` | LP-IV appendix, directional only |
| 5 | `04_did_it_event_study.ipynb` | Inflation-targeting appendix, exploratory only |
| 6 | `05_lucas_us_appendix.ipynb` | Lucas (1980)-inspired U.S. appendix |

## Main vs Appendix

Main evidence:

- Notebook 01 long-run country-average association.
- Notebook 02 clean-sample TWFE and pre/post-2008 split.
- Notebook 02 between-vs-within figure.

Appendix evidence:

- Notebook 02b inference sensitivity and cumulative lag scaffold.
- Notebook 03 LP-IV.
- Notebook 04 inflation-targeting event study.
- Notebook 05 U.S. low-frequency appendix.

## Guardrails

- TWFE estimates are descriptive within-country associations, not causal effects.
- Distributed-lag estimates are reduced-form associations, not impulse responses.
- IV results are weak/directional and should not be used as headline identification.
- Inflation-targeting adoption is endogenous.
- COVID results are descriptive stress evidence only.
