# Lucas (1980), second illustration — nominal interest rates

**Lucas says (informally):** in long/low-frequency variation, shifts in money growth show up roughly one-for-one in **inflation** and in **nominal interest rates**, not necessarily in GDP growth.  
The paper implements **law (ii)** with **US quarterly** M1, CPI, **90‑day Treasury bill**, and moving-average filters.

**Current repo:** Obj A mirrors **money–inflation / money–GDP** with no harmonised **nominal rate** column in `macro_growth_merged.csv`. That omission is deliberate until you attach a credible rate series.

This file gives **three handles** ordered by effort. Pick one; none are required for the rest of the project to stay honest.

---

## Path A — No new data (0 min) — recommended if time‑boxed)

**What you do:** Nothing in code.

**What you say when asked:** Obj A aligns with Lucas’s **first** cross-average idea (money ↔ inflation); Lucas’s **second** leg needs **money-market / policy nominal rates**. The panel deliberately omits harmonised annual rates across 163 economies; GDP is descriptive only—not Lucas II.

**Evidence in repo:** `research_target.md` (Obj A), `01_lucas_replication.ipynb` prose, `report_draft.md` Obj A sentence.

---

## Path B — US appendix only (~1–3 hours total) — best “minimal inclusion”

**Goal:** Echo Lucas’s literal **money + inflation + nominal rate** trio for **United States only**, annual 1991–2020 aligned with panel years (not a replicate of Lucas’s filters—call it pedagogical appendix).

**Steps (manual is fine):**

1. Pull **annual** nominal short rate compatible with textbook QTM/Fisher intuition, e.g.:
   - FRED **`TB3MS`** (monthly 3‑month T‑bill secondary market, take **December** observation or yearly average → one number per calendar year).
   - Or **`DGS3MO`** (daily, average to annual).
   - CSV export: https://fred.stlouisfed.org/series/TB3MS → **Download → CSV**.
2. Build `Country Name,year,policy_nominal_decimal` matching existing panel decimals (`0.04` = **4 ppt** per annum if annualised nominal rate exported as percentage—**align units**: if FRED CSV is `"3.5"` meaning 3.5%, convert with `divide by 100` to match GDP/inflation as decimals already in merged file).
3. Left‑join onto US rows only; keep other countries NaN rate.
4. In **`01_lucas_replication.ipynb`** (optional new cell cluster after country plots):
   - scatter or lowess: **mean/median money growth vs mean nominal rate** over window, OR year‑scatter for US subsample only with same filters as neighbours.
   - Export one PNG + one row CSV to `exports/phase0/` for personal deck.

**Claims:** Appendix, descriptive, single country—“not pooled cross‑country Lucas II.”

**Pitfalls:** Currency / rate definition churn; inconsistent annualisation vs your **GDP growth decimals** column.

---

## Path C — Full panel nominal rates (~2–5 days R&D before coding)

**Goal:** Harmonised yearly nominal rate aligned with IMF IFS deposit/money‑market/policy rate or World Bank composites.

**Rough sequence:**

| Step | Risk |
|---|---|
| Decide definition (policy corridor midpoint vs treasury vs money market deposit) — **countries differ.** | Aggregation bias |
| Build country–year scrape or bulk download API + map ISO to `Country Name` | Manual matching pain |
| Missingness audit (many Low‑income blanks) → document `n_obs` thresholds like Obj A GDP filter | Surviving sample shrinks badly |
| Only then merge **one** nominal rate column v1 into merge script that builds `macro_growth_merged.csv` | Re-run full pipeline QA |

Until Path C completes, canonical claims stay Path A wording.

---

## What *not* to do under time pressure

- Don’t retrofit GDP scatter as Lucas II (already documented as wrong analogy).
- Don’t silently mix **levels** (% points) vs **growth rates** in one regression axis without documenting.

---

## If you freeze here

You are **consistent** claiming: reproduced spirit of Lucas **(i)** in cross‑country averages; **(ii)** documented as deliberate gap with actionable extension roadmap (this file). That’s honest side‑project optics without PhD ambition.
