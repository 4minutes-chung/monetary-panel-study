"""Fetch cross-country lending interest rates from the World Bank API.

Indicator choice: World Bank FR.INR.LEND, lending interest rate (% per year),
is used as the broad cross-country nominal rate proxy. Values are retained in
percent and are not converted to decimals or log changes.
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

import pandas as pd
import requests


BASE_URL = "https://api.worldbank.org/v2/country/all/indicator/FR.INR.LEND"
START_YEAR = 1991
END_YEAR = 2024
API_DATE_RANGE = "1990:2024"
PER_PAGE = 1000
MAX_RETRIES = 3
REQUEST_TIMEOUT = (10, 90)

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
OUTPUT_PATH = SCRIPT_DIR / "intl_lending_rates.csv"
MACRO_PANEL_PATH = REPO_ROOT / "02_data" / "analysis_ready" / "macro_growth_merged.csv"


def fetch_world_bank_page(page: int) -> list[Any]:
    """Fetch one paginated World Bank response."""
    params = {
        "format": "json",
        "date": API_DATE_RANGE,
        "per_page": PER_PAGE,
        "page": page,
    }

    last_error: Exception | None = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(BASE_URL, params=params, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            body = response.json()
            if not isinstance(body, list) or len(body) < 2:
                raise ValueError(f"Unexpected World Bank response on page {page}: {body!r}")
            return body
        except (requests.RequestException, ValueError) as exc:
            last_error = exc
            if attempt == MAX_RETRIES:
                break
            time.sleep(2**attempt)

    raise RuntimeError(f"Failed to fetch World Bank page {page}") from last_error


def fetch_lending_rates() -> pd.DataFrame:
    """Download and clean long lending-rate panel data."""
    all_rows: list[dict[str, object]] = []
    page = 1
    pages = None

    while pages is None or page <= pages:
        body = fetch_world_bank_page(page)
        metadata = body[0]
        records = body[1] or []

        pages = int(metadata["pages"])
        for record in records:
            value = record.get("value")
            if value is None:
                continue

            year = int(record["date"])
            if year < START_YEAR or year > END_YEAR:
                continue

            all_rows.append(
                {
                    "Country Name": record["country"]["value"],
                    "year": year,
                    "lending_rate_pct": float(value),
                }
            )

        page += 1

    rates = pd.DataFrame(all_rows, columns=["Country Name", "year", "lending_rate_pct"])
    if rates.empty:
        return rates

    country_obs = rates.groupby("Country Name")["lending_rate_pct"].transform("count")
    rates = rates.loc[country_obs >= 5].copy()
    rates = rates.sort_values(["Country Name", "year"], kind="mergesort")
    rates = rates.reset_index(drop=True)

    return rates


def count_macro_country_matches(rates: pd.DataFrame) -> int:
    """Count countries in macro_growth_merged.csv matched on Country Name."""
    macro = pd.read_csv(MACRO_PANEL_PATH, usecols=["Country Name"])
    macro_countries = macro["Country Name"].dropna().drop_duplicates()
    rate_countries = set(rates["Country Name"].dropna().unique())
    return int(macro_countries.isin(rate_countries).sum())


def main() -> None:
    rates = fetch_lending_rates()
    rates.to_csv(OUTPUT_PATH, index=False)

    print(
        "Data source: World Bank FR.INR.LEND, lending interest rate "
        "(% per year), used as a cross-country nominal rate proxy."
    )
    print(f"Total rows: {len(rates)}")
    print(f"Number of unique countries: {rates['Country Name'].nunique()}")
    if rates.empty:
        print("Year range: NA")
    else:
        print(f"Year range: {int(rates['year'].min())}-{int(rates['year'].max())}")
    print(
        "Number of countries in macro_growth_merged.csv matched on Country Name: "
        f"{count_macro_country_matches(rates)}"
    )


if __name__ == "__main__":
    main()
