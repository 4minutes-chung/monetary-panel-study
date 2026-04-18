# Research Target and Repo Recovery Plan

## 1. Canonical research target

Primary research question:
Across countries, how strongly is money growth associated with inflation and GDP growth, and what can be claimed under credible identification checks?

Objective A: Lucas replication baseline

- Replicate the Lucas-style long-run cross-country comparison on the current panel window.
- Reproduce core descriptive and long-run comparison tables from code, not manual notebook edits.

Objective B: Monetary extension

- Estimate panel FE and IV relationships for inflation and GDP growth.
- Estimate short-run LP-IV dynamics for inflation (h=0..3) and GDP growth (h=0 baseline).
- Keep causal claims conditional on diagnostics.

Claim boundary:

- Default interpretation is associational evidence.
- Upgrade to stronger causal language only if identification gates are passed.

## 2. Definition of done

A run is done only when all are true:

1. A clean run from project root reproduces all canonical v2 tables and figures.
2. One canonical scorecard exists with one unambiguous gate framework.
3. Documentation references only existing files and current commands.
4. Narrative claims match the measured gate results.

## 3. Delivery mode for this cycle

Decision for current closeout cycle: notebook-first delivery, script-verified parity.

Why:

- You want the work organized as a readable research story in three phase notebooks.
- Notebooks are better for interview/demo flow and phase-by-phase explanation.
- Existing v2 scripts still provide a reproducibility backstop and consistency check.

Policy:

- Primary phase narrative lives in three notebooks: notebooks/phase_0_objA_lucas_replication.ipynb, notebooks/phase_1_objB_baseline.ipynb, notebooks/phase_2_objB_short_run.ipynb.
- Any headline claim used in memo/deck must be traceable to exported notebook tables or v2 outputs.
- v2 scripts remain the parity-check path, not discarded.

## 4. Canonical execution path (notebook-first)

From project root:

1. python3 -m pip install -r requirements.txt
2. Run notebooks/phase_0_objA_lucas_replication.ipynb (Run All)
3. Run notebooks/phase_1_objB_baseline.ipynb (Run All)
4. Run notebooks/phase_2_objB_short_run.ipynb (Run All)
5. Optional parity check: python3 v2/run_v2_rebuild.py && python3 v2/build_portfolio_graphs.py

Canonical high-level outputs for this cycle:

- outputs/notebook_phase0/
- outputs/notebook_phase1/
- outputs/notebook_phase2/
- v2/outputs/V2_SUMMARY.md
- v2/outputs/phase1_audit_v2/
- v2/outputs/phase2_short_run_v2/
- v2/outputs/portfolio_graphs/

### 4.1 Notebook map by objective

- Notebook 1 (Phase 0, Obj A motivation): notebooks/phase_0_objA_lucas_replication.ipynb -> Lucas-style replication and long-run cross-country comparison.
- Notebook 2 (Phase 1, Obj B baseline): notebooks/phase_1_objB_baseline.ipynb -> FE and IV baseline model layer for inflation and GDP growth.
- Notebook 3 (Phase 2, Obj B short-run): notebooks/phase_2_objB_short_run.ipynb -> LP-IV short-run dynamics and policy-interpretation layer.

## 5. Step-by-step recovery plan

### Step 0: Stabilize repository state

- [x] Snapshot and classify current git changes into: keep, archive, drop.
- [x] Resolve accidental deletes and path anomalies before new edits.
- [x] Confirm one branch as active recovery branch.

Step 0 snapshot file:

- RECOVERY_STEP0_GIT_TRIAGE.md

### Step 1: Set single source of truth

- [x] Declare v2 pipeline as canonical analysis path.
- [x] Mark legacy phase outputs as archive or historical.
- [x] Remove contradictory statements across docs.

### Step 2: Unify identification gates

- [x] Define first-stage gate framework explicitly: relevance gate is first-stage Wald chi2(1) > 3.8415 and p < 0.05, and strong-IV label is first-stage statistic >= 10.0.
- [x] Keep that framework in code, scorecard CSV, and narrative docs.
- [x] Add a short interpretation note for weak-IV cases.

### Step 2.5: Build notebook phase chain

- [x] Create Notebook 1 for Obj A motivation (Lucas replication).
- [x] Create Notebook 2 for Obj B baseline model layer.
- [x] Create Notebook 3 for Obj B short-run LP-IV layer.
- [x] Keep notebook outputs exportable by phase folder.

### Step 3: Clean project structure

- [ ] Separate research inputs, scripts, outputs, and deliverables clearly.
- [ ] Move legacy generated artifacts to an archive folder if needed.
- [ ] Ensure ignore rules match what should not be tracked.

### Step 4: Rebuild and verify

- [x] Run script parity commands end-to-end.
- [ ] Run notebook phase chain end-to-end.
- [ ] Validate notebook exports against v2 headline metrics.

### Step 5: Documentation hardening

- [x] Fix stale absolute paths and outdated notebook references.
- [x] Add a short "where to start" section for future-you.
- [x] Keep one concise claim boundary statement reused everywhere.

### Step 6: Final research package

- [ ] Produce one executive memo and one technical appendix from canonical outputs.
- [ ] Ensure all numbers in memo are traceable to output tables.

## 6. Immediate next actions

1. Run the three new notebooks end-to-end and lock their outputs.
2. Complete Step 0 git triage safely (legacy notebook restore/archive decision).
3. Execute Step 3 structural cleanup after Step 0 decision.
4. Finalize Step 6 package from canonical outputs.
