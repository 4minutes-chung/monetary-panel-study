# AI Handoff: Econometric Findings Log (2026-04-21)

Purpose: preserve high-signal review findings and their resolution state so future contributors do not regress fixes.

Scope: canonical `v2` pipeline and portfolio graph generation.

Status: `RESOLVED` (patched in code on 2026-04-24).

## Finding 1 (P1) - Resolved

- File: `v2/run_v2_rebuild.py` (permutation placebo branch)
- Issue fixed: permutation placebo now uses empirical two-sided randomization p-value against an explicit observed statistic.
- Implementation note:
  - Added `empirical_two_sided_pvalue`.
  - Null distribution is generated from repeated derangement-based permutations.
  - Output table now stores null mean/std and permutation count for auditability.

## Finding 2 (P1) - Resolved

- File: `v2/run_v2_rebuild.py` (scorecard gate logic)
- Issue fixed: scorecard now uses conservative gate metrics built from one-way and two-way clustering checks.
- Implementation note:
  - Conservative first-stage stat is `min(country, country_year)`.
  - Conservative first-stage p-value is `max(country, country_year)`.
  - Scorecard includes explicit agreement check across clustering choices.
  - Summary text now reports both clustering stats plus the conservative canonical metric.

## Finding 3 (P3) - Resolved

- File: `v2/build_portfolio_graphs.py` (`chart_lp_first_stage`)
- Issue fixed: first-stage horizon chart now plots outcome-specific series (`instrument | outcome`) instead of pooling across outcomes.
- Implementation note:
  - Grouping key updated to `instrument + outcome + horizon`.
  - Title explicitly indicates instrument-by-outcome diagnostic paths.

## Coordination Note For Other AI Agents

Before editing `v2/run_v2_rebuild.py` or `v2/build_portfolio_graphs.py`:

1. Read this file and preserve these fixes.
2. Keep gate logic aligned to conservative clustering definitions in `RESEARCH_TARGET.md`.
3. Re-run:
  - `python3 v2/run_v2_rebuild.py`
  - `python3 v2/build_portfolio_graphs.py`
4. Confirm updated outputs in:
  - `v2/outputs/phase1_audit_v2/tables/`
  - `v2/outputs/phase2_short_run_v2/tables/`
  - `v2/outputs/portfolio_graphs/`
