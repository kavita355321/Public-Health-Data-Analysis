"""Build a reproducible country-year public-health analysis dataset."""

from pathlib import Path

import numpy as np
import pandas as pd

from src.config import METADATA_PATH, OWID_PATH, PROCESSED_PATH, WORLD_BANK_PATH


OWID_COLUMNS = [
    "iso_code",
    "continent",
    "location",
    "date",
    "total_vaccinations",
    "people_fully_vaccinated_per_hundred",
    "new_cases",
    "new_deaths",
    "population",
]


def prepare_owid_country_year(path: Path = OWID_PATH) -> pd.DataFrame:
    """Aggregate OWID daily records to one validated row per country and year."""
    data = pd.read_csv(path, usecols=OWID_COLUMNS, low_memory=False)
    data["date"] = pd.to_datetime(data["date"], errors="coerce")
    data = data.loc[
        data["continent"].notna()
        & data["date"].notna()
        & data["iso_code"].str.fullmatch(r"[A-Z]{3}", na=False)
    ].copy()
    data["year"] = data["date"].dt.year.astype(int)

    annual = (
        data.groupby(["iso_code", "location", "continent", "year"], as_index=False)
        .agg(
            total_vaccinations=("total_vaccinations", "max"),
            fully_vaccinated_per_hundred=(
                "people_fully_vaccinated_per_hundred",
                "max",
            ),
            new_cases=("new_cases", lambda values: values.sum(min_count=1)),
            new_deaths=("new_deaths", lambda values: values.sum(min_count=1)),
            population=("population", "max"),
        )
        .sort_values(["iso_code", "year"])
        .reset_index(drop=True)
    )

    valid_population = annual["population"].where(annual["population"] > 0)
    annual["cases_per_million"] = annual["new_cases"] / valid_population * 1_000_000
    annual["deaths_per_million"] = annual["new_deaths"] / valid_population * 1_000_000
    annual["fully_vaccinated_per_hundred"] = annual[
        "fully_vaccinated_per_hundred"
    ].clip(lower=0, upper=100)
    return annual


def prepare_world_bank_health_spending(path: Path = WORLD_BANK_PATH) -> pd.DataFrame:
    """Convert the World Bank wide health-spending file to country-year format."""
    data = pd.read_csv(path, skiprows=4)
    year_columns = [column for column in data.columns if str(column).isdigit()]
    long_data = data.melt(
        id_vars=["Country Name", "Country Code"],
        value_vars=year_columns,
        var_name="year",
        value_name="health_spending_pct_gdp",
    ).rename(
        columns={
            "Country Name": "world_bank_country",
            "Country Code": "iso_code",
        }
    )
    long_data["year"] = pd.to_numeric(long_data["year"], errors="coerce")
    long_data["health_spending_pct_gdp"] = pd.to_numeric(
        long_data["health_spending_pct_gdp"], errors="coerce"
    )
    long_data = long_data.dropna(subset=["year"])
    long_data["year"] = long_data["year"].astype(int)
    return long_data


def prepare_country_metadata(path: Path = METADATA_PATH) -> pd.DataFrame:
    """Return one region and income classification per World Bank country code."""
    metadata = pd.read_csv(path)
    metadata = metadata.rename(
        columns={
            "Country Code": "iso_code",
            "Region": "region",
            "IncomeGroup": "income_group",
        }
    )
    return metadata[["iso_code", "region", "income_group"]].drop_duplicates(
        subset="iso_code"
    )


def build_analysis_dataset(
    owid_path: Path = OWID_PATH,
    world_bank_path: Path = WORLD_BANK_PATH,
    metadata_path: Path = METADATA_PATH,
) -> pd.DataFrame:
    """Merge OWID outcomes with World Bank spending and classifications."""
    owid = prepare_owid_country_year(owid_path)
    spending = prepare_world_bank_health_spending(world_bank_path)
    metadata = prepare_country_metadata(metadata_path)

    merged = owid.merge(spending, on=["iso_code", "year"], how="left")
    merged = merged.merge(metadata, on="iso_code", how="left")
    merged = merged.drop(columns=["world_bank_country"])
    merged = merged.replace([np.inf, -np.inf], np.nan)
    merged = merged.sort_values(["year", "location"]).reset_index(drop=True)

    if merged.duplicated(["iso_code", "year"]).any():
        raise ValueError("Duplicate country-year rows were produced by the ETL pipeline.")
    return merged


def run_etl(output_path: Path = PROCESSED_PATH) -> pd.DataFrame:
    """Run the ETL pipeline and save the processed country-year dataset."""
    data = build_analysis_dataset()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(output_path, index=False)
    return data


if __name__ == "__main__":
    result = run_etl()
    print(f"Saved {len(result):,} country-year rows to {PROCESSED_PATH}")

