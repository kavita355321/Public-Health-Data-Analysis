import pandas as pd

from src.analysis import (
    build_exploratory_equity_index,
    select_latest_comparable_year,
)


def sample_data() -> pd.DataFrame:
    rows = []
    for year in [2021, 2022]:
        for index in range(3):
            rows.append(
                {
                    "year": year,
                    "iso_code": f"A{index:02d}",
                    "location": f"Country {index}",
                    "continent": "Region",
                    "region": "Region",
                    "income_group": "Income",
                    "fully_vaccinated_per_hundred": 50 + index + year - 2021,
                    "health_spending_pct_gdp": 5 + index,
                    "deaths_per_million": 100 - index,
                    "population": 1_000_000,
                }
            )
    return pd.DataFrame(rows)


def test_latest_comparable_year_uses_coverage_threshold() -> None:
    assert select_latest_comparable_year(sample_data(), minimum_complete_countries=3) == 2022


def test_equity_index_is_bounded_and_ranked() -> None:
    result = build_exploratory_equity_index(sample_data(), 2022)
    assert result["exploratory_equity_index"].between(0, 1).all()
    assert result["rank"].tolist() == sorted(result["rank"].tolist())


def test_missing_values_are_excluded_not_changed_to_zero() -> None:
    data = sample_data()
    data.loc[(data["year"] == 2022) & (data["iso_code"] == "A00"), "health_spending_pct_gdp"] = None
    result = build_exploratory_equity_index(data, 2022)
    assert "A00" not in result["iso_code"].tolist()

