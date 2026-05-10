# Units Register

One row per variable. All units verified against source data (macro_growth_merged.csv, FRED raw files).

| Variable | Raw unit | Transformation | Output unit | Verification note |
|---|---|---|---|---|
| `m2_growth` | Decimal fraction | None (already transformed at source) | Decimal (e.g., 0.10 = 10% growth) | US 2007: 0.111 = 11.1% — matches FRED M2SL YoY |
| `inflation` | Decimal fraction | None (already transformed at source) | Decimal (e.g., 0.03 = 3% CPI change) | US 2009: -0.004 = -0.4% — matches FRED CPIAUCSL |
| `gdp_growth` | Decimal fraction | None (already transformed at source) | Decimal (e.g., 0.026 = 2.6% real GDP growth) | US 2009: -0.026 = -2.6% — confirmed correct; NOT percent. This is load-bearing for B-1 fix. |
| `output_gap_hp` | Decimal fraction of GDP | HP filter (lambda=6.25) on cumsum(log1p(gdp_growth)); then * 100 | Percent of trend GDP (e.g., 0.5 = 0.5% above trend) | After B-1 fix: log1p(gdp_growth) is correct. Pre-fix used log1p(gdp_growth/100) which shrunk variance ~10000x. |
| `m2_ma` (US appendix) | Decimal fraction | 5-year centred moving average of log M2 YoY change | Decimal (e.g., 0.065 = 6.5% M2 growth) | Matches `us['m2_growth']` derived from FRED M2SL |
| `cpi_ma` / `inflation_ma` (US appendix) | Decimal fraction | 5-year centred moving average of log CPI YoY change | Decimal (e.g., 0.029 = 2.9% inflation) | Column is named `inflation_ma` in nb05 (not `cpi_ma`) — see ERRATA for NW cell fix |
| `tbill_dec` (US appendix) | Percent per annum | Divided by 100 at load (`us['tbill_dec'] = us['tbill'] / 100`) | Decimal (e.g., 0.044 = 4.4%) | FRED TB3MS is in percent; /100 applied in nb05 cell `2bbcf770` |
| `tbill_ma` (US appendix) | Decimal fraction | 5-year centred moving average of `tbill_dec` | Decimal annual rate | Consistent with `m2_ma` and `inflation_ma` scale |
| `lending_rate_pct` | Percent per annum | Country mean taken directly (no rate conversion in Obj A scatter) | Percent (e.g., 8.0 = 8.0%) | Lucas ii Obj A scatter uses percent scale; slope 0.49 is percent-on-decimal — interpret as: 1 pp M2 growth → 0.49 pp lending rate |
