# Research Target Contract (Master Source of Truth)

## 0. Contract Authority

This file is the only contract for:

- research objective and claim boundary,
- canonical run order,
- identification gate definitions,
- what "done" means.

If any other document conflicts with this file, this file wins.

Rule for other docs:

- `README.md` is a reading guide.
- `START_HERE.md` is a lightweight pointer only.
- memos/decks must inherit numbers and caveats from this contract.

## 1. Canonical Research Target

Primary question:
Across countries, how strongly is money growth associated with inflation and GDP growth, and what can be claimed under credible identification checks?

Objective A:

- Replicate Lucas-style long-run cross-country comparison on the current panel window.

Objective B:

- Estimate FE and IV relationships for inflation and GDP growth.
- Estimate LP-IV short-run dynamics for inflation (h=0..3) and GDP growth (h=0).

## 2. Claim Boundary

- Baseline interpretation is associational.
- Causal language stays conservative unless gates are passed.
- If first-stage strength is weak-to-moderate, do not overclaim.

## 3. Identification Gate Framework (Canonical)

Preferred IV for gate decisions: `instrument_m2_external_level` in inflation core IV spec.

Two clustering checks are always computed for first-stage diagnostics:

- one-way: country clustering,
- two-way: country + year clustering.

Canonical pass/fail gate is conservative:

- conservative first-stage stat = min(one-way stat, two-way stat),
- conservative first-stage p = max(one-way p, two-way p).

Gate definitions:

- Relevance gate: conservative stat > 3.8415 and conservative p < 0.05.
- Strong-IV label: conservative stat >= 10.0.

Placebo rule:

- permutation placebo p-value must be empirical two-sided randomization p-value,
- both placebo checks should remain non-significant for comfort.

## 4. Canonical Execution Path (Notebook-First)

From project root:

1. `python3 -m pip install -r requirements.txt`
2. Run `notebooks/phase_0_objA_lucas_replication.ipynb` (Run All)
3. Run `notebooks/phase_1_objB_baseline.ipynb` (Run All)
4. Run `notebooks/phase_2_objB_short_run.ipynb` (Run All)
5. Optional parity rebuild:
	- `python3 v2/run_v2_rebuild.py`
	- `python3 v2/build_portfolio_graphs.py`

## 5. Canonical Outputs

- `outputs/notebook_phase0/`
- `outputs/notebook_phase1/`
- `outputs/notebook_phase2/`
- `v2/outputs/V2_SUMMARY.md`
- `v2/outputs/phase1_audit_v2/`
- `v2/outputs/phase2_short_run_v2/`
- `v2/outputs/portfolio_graphs/`

## 6. Definition Of Done

A cycle is done only when all conditions hold:

1. Clean run reproduces canonical outputs.
2. Scorecard and summary use the same conservative gate logic.
3. Docs reference only existing files and current commands.
4. Narrative language matches measured diagnostics.

## 7. Current Cycle Status

- Step 0 to Step 6 recovery work is complete.
- Current focus is consistency, readability, and final packaging.

## 8. Next Practical Actions

1. Maintain a single report draft that references canonical tables and figures.
2. Keep README in coffee-chat guidance mode, not method-heavy mode.
3. Keep START_HERE minimal to avoid duplicate instructions.
