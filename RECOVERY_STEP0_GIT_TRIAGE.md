# Step 0 Git Triage Snapshot

Date: 2026-04-18
Branch: main
HEAD: 2266503

## Current state summary

The repository is in a mixed migration state with:

- Many tracked files deleted from working tree (especially notebooks).
- Many generated outputs modified after rebuild runs.
- Many new untracked canonical files (README, requirements, v2 script/docs/deliverables).

This is not fatal, but it is high-risk for accidental loss unless changes are classified before cleanup.

## Critical anomalies

1. Notebook deletion risk

- No physical .ipynb files currently exist in the working tree.
- Git still tracks multiple notebook paths as deleted.

1. Legacy filename anomaly

- Three tracked notebook paths include a leading-space filename prefix:

  - " lucas_Phase 0.ipynb"
  - " lucas_Phase 0.5A.ipynb"
  - " lucas_Phase 0.5B.ipynb"

- This can create path confusion and accidental command mistakes.

1. Mixed output generations

- outputs/phase2_short_run/* changed.
- v2/outputs/* changed.
- Untracked v2 portfolio graphs and memo files exist.

## Classification frame (to execute in Step 1)

A. Canonical keep (active path)

- v2/run_v2_rebuild.py
- v2/build_portfolio_graphs.py
- requirements.txt
- README.md
- v2/outputs/* (only if generated from canonical commands)

B. Historical keep but archive

- outputs/phase1/*
- outputs/phase1_1/*
- outputs/phase1_audit/*
- outputs/phase2_short_run/*
- legacy PDFs/LaTeX artifacts not used by canonical pipeline

C. Decision-required before write actions

- Whether deleted notebooks should be restored from HEAD, kept deleted, or moved to archive once restored.
- Whether leading-space legacy notebook names should be normalized (requires careful git path operations).

## Safe next actions (no destructive operation)

1. Decide notebook policy:

- Option R: Restore notebooks for historical traceability.
- Option D: Keep notebooks deleted and remove references.
- Option A: Restore then archive under a historical folder.

1. Apply one canonical gate definition across:

- v2/run_v2_rebuild.py
- v2 scorecard CSVs
- narrative docs

1. Perform structural cleanup only after notebook decision.

## Notes

No destructive command has been executed in this step.

## Progress update (2026-04-18)

- Canonical entrypoint documented in `README.md`, `RESEARCH_TARGET.md`, and `READING_GUIDE.md`.
- Gate framework unified as two-tier (`chi2(1)>3.8415` relevance, `>=10` strong-IV label) across:

  - `v2/run_v2_rebuild.py`
  - `v2/outputs/phase1_audit_v2/tables/audit_scorecard_v2.csv`
  - `v2/outputs/V2_SUMMARY.md`

- Stale absolute-path references were removed from active documentation.

## Step 0 resolution (2026-04-18)

- Decision applied: Option A (restore then archive).
- Legacy notebooks were restored from HEAD and moved under:

  - `archive/notebooks_legacy/`

- This preserves notebook history while removing root-level notebook clutter.
- Leading-space legacy filenames are now isolated in the archive folder and no longer block active workflow.

## Step 0 decision commands (safe templates)

Option R (restore notebooks for historical traceability):

```bash
git restore -- ' lucas_Phase 0.ipynb' ' lucas_Phase 0.5A.ipynb' ' lucas_Phase 0.5B.ipynb' \
  'lucas_Phase 1.ipynb' 'lucas_Phase 1.executed.ipynb' 'lucas_Phase 1.1.ipynb' 'lucas_Phase 1.1.executed.ipynb' \
  'lucas_Phase 1.audit.ipynb' 'lucas_Phase 2_short_run.ipynb' 'lucas_Phase 2_short_run.executed.ipynb'
```

Option D (keep notebooks deleted, script-only tree):

```bash
# No restore command needed. Keep markdown/docs notebook references historical only.
```

Option A (restore then archive under historical folder):

```bash
mkdir -p archive/notebooks_legacy
git restore -- ' lucas_Phase 0.ipynb' ' lucas_Phase 0.5A.ipynb' ' lucas_Phase 0.5B.ipynb' \
  'lucas_Phase 1.ipynb' 'lucas_Phase 1.executed.ipynb' 'lucas_Phase 1.1.ipynb' 'lucas_Phase 1.1.executed.ipynb' \
  'lucas_Phase 1.audit.ipynb' 'lucas_Phase 2_short_run.ipynb' 'lucas_Phase 2_short_run.executed.ipynb'
mv -- ' lucas_Phase 0.ipynb' ' lucas_Phase 0.5A.ipynb' ' lucas_Phase 0.5B.ipynb' archive/notebooks_legacy/
mv -- 'lucas_Phase 1.ipynb' 'lucas_Phase 1.executed.ipynb' 'lucas_Phase 1.1.ipynb' 'lucas_Phase 1.1.executed.ipynb' archive/notebooks_legacy/
mv -- 'lucas_Phase 1.audit.ipynb' 'lucas_Phase 2_short_run.ipynb' 'lucas_Phase 2_short_run.executed.ipynb' archive/notebooks_legacy/
```
