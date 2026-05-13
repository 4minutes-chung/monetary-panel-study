# Data Sources and Usage

This note documents which external data sources are used in the project, and how each source is used in the analysis.

## 1. Main Analysis Data (used for core findings)

Primary source: **World Bank, World Development Indicators (WDI)**  
Coverage in this project: cross-country annual panel, 1991-2024.

Core variables:

- `FM.LBL.BMNY.ZG` — Broad money growth (annual %), proxy used as `m2_growth`.
- `FP.CPI.TOTL.ZG` — CPI inflation (annual %), used as `inflation`.
- `NY.GDP.MKTP.KD.ZG` — Real GDP growth (annual %), used as `gdp_growth`.

These three series define the core cross-country money-inflation analysis in notebook 01.

## 2. Supplementary and Support Data

### 2.1 Supplementary nominal-rate proxy

Source: **World Bank WDI**

- `FR.INR.LEND` — Lending interest rate (%).

Use: supplementary nominal-rate comparison in notebook 01.

### 2.2 Control variables (robustness layer)

Source: **World Bank WDI**

- `NE.TRD.GNFS.ZS` — Trade (% of GDP), `trade_open`.
- `NY.GDP.PCAP.KD.ZG` — GDP per capita growth, `gdp_pc_growth`.
- `SP.POP.GROW` — Population growth, `pop_growth`.
- `NE.GDI.TOTL.ZS` — Gross capital formation (% of GDP), `investment_share`.

Use: robustness/control specifications in short-run notebooks.

### 2.3 IT regime dates (event-study layer)

Sources:

- Roger (2010), IMF WP 10/8.
- Hammond (2012), Bank of England handbook/compilation.

Use: inflation-targeting adoption timing in the regime/event-study layer.

### 2.4 U.S. appendix and rate-shock support series

Source: **FRED (Federal Reserve Economic Data)**

- `M2SL` — M2 money stock.
- `CPIAUCSL` — CPI (all urban consumers).
- `TB3MS` — 3-month Treasury bill rate.
- `FEDFUNDS` — Effective federal funds rate.

Use:

- `M2SL`, `CPIAUCSL`, `TB3MS`: U.S. low-frequency appendix (notebook 05).
- `FEDFUNDS`: support input for the external-rate Bartik-style instrument file.

## 3. Data source links and Methodology

- World Bank WDI: https://data.worldbank.org/
- FRED: https://fred.stlouisfed.org/

- I downloaded and import data through API and csv. Then cleaned them to form csv file as in '02_data'. All data are downloaded for research purposes only.