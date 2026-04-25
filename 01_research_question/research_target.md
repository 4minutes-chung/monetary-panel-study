# Research Target Contract (Master Source of Truth)

## 0. Contract Authority

This file is the only contract for:

- research objective and claim boundary,
- canonical run order,
- identification gate definitions,
- what "done" means.

If any other document conflicts with this file, this file wins.

Rule for other docs:

- `00_START_HERE.md` is the first reading page.
- `01_research_question/reading_guide.md` is the detailed process memory.
- `01_research_question/claim_boundary.md` is the plain-language claim boundary.
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

## 4. Canonical Execution Path

From project root:

1. Read `00_START_HERE.md`.
2. Run or inspect notebooks in `03_analysis_notebooks/`.
3. Use current results in `04_current_results/` for claims.
4. Optional rebuild:
   - `python3 -m pip install -r 90_reproduction_scripts/requirements.txt`
   - `python3 90_reproduction_scripts/run_rebuild.py`
   - `python3 90_reproduction_scripts/build_graphs.py`

## 5. Canonical Outputs

- `04_current_results/summary.md`
- `04_current_results/tables/phase1_audit/`
- `04_current_results/tables/short_run_lp/`
- `04_current_results/figures/`
- `05_final_writing/`

## 6. Definition Of Done

A cycle is done only when all conditions hold:

1. Clean run reproduces canonical outputs.
2. Scorecard and summary use the same conservative gate logic.
3. Docs reference only existing files and current commands.
4. Narrative language matches measured diagnostics.

## 7. Current Cycle Status

- Current repo layout is research-first and study-oriented.
- Current focus is reading, interpretation, and later analysis.

## 8. Next Practical Actions

1. Maintain a single report draft that references canonical tables and figures.
2. Keep README in coffee-chat guidance mode, not method-heavy mode.
3. Avoid duplicate entrypoint docs that can drift from this contract.
