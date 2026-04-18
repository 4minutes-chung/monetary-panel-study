# Repository Layout (Post-Cleanup)

## Active workflow (canonical)

- Root active inputs: `macro_growth_merged.csv`, `m2_raw.csv`, `cpi_raw.csv`, `gdp_raw.csv`.
- Notebook-first analysis: `notebooks/`.
- Script parity and portfolio graphs: `v2/`.
- Current guidance docs: `START_HERE.md`, `README.md`, `RESEARCH_TARGET.md`.

## Archived historical materials

- Legacy notebooks: `archive/notebooks_legacy/`.
- Legacy derived datasets: `archive/legacy_data/`.
- Legacy reports and TeX artifacts: `archive/legacy_reports/`.
- Reference papers and source downloads: `archive/references/`.
- Legacy narrative notes: `docs/legacy_notes/`.

## Practical rule

If a file is not required for the notebook-first run path or v2 parity scripts, keep it in `archive/` or `docs/legacy_notes/` rather than root.
