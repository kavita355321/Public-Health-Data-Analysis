from pathlib import Path

import pandas as pd

from src.etl import prepare_owid_country_year, prepare_world_bank_health_spending


def test_owid_aggregation_excludes_aggregate_rows(tmp_path: Path) -> None:
    source = pd.DataFrame(
        {
            "iso_code": ["AAA", "AAA", "OWID_WRL"],
            "continent": ["Region", "Region", None],
            "location": ["Country A", "Country A", "World"],
            "date": ["2022-01-01", "2022-12-31", "2022-12-31"],
            "total_vaccinations": [10, 100, 500],
            "people_fully_vaccinated_per_hundred": [5, 70, 60],
            "new_cases": [10, 20, 100],
            "new_deaths": [1, 2, 5],
            "population": [1_000_000, 1_000_000, 5_000_000],
        }
    )
    path = tmp_path / "owid.csv"
    source.to_csv(path, index=False)

    result = prepare_owid_country_year(path)

    assert len(result) == 1
    assert result.loc[0, "iso_code"] == "AAA"
    assert result.loc[0, "new_deaths"] == 3
    assert result.loc[0, "deaths_per_million"] == 3


def test_world_bank_wide_data_is_converted_to_country_year(tmp_path: Path) -> None:
    path = tmp_path / "world_bank.csv"
    path.write_text(
        "metadata\nmetadata\nmetadata\nmetadata\n"
        "Country Name,Country Code,Indicator Name,Indicator Code,2021,2022,Unnamed: 6\n"
        "Country A,AAA,Health spending,TEST,5.2,5.5,\n",
        encoding="utf-8",
    )

    result = prepare_world_bank_health_spending(path)

    assert result["year"].tolist() == [2021, 2022]
    assert result["health_spending_pct_gdp"].tolist() == [5.2, 5.5]

