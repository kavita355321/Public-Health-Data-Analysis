"""Create transparent country, region and income-group public-health summaries."""

from pathlib import Path

import pandas as pd

from src.config import OUTPUT_DIR, PROCESSED_PATH


COMPLETE_COLUMNS = [
    "fully_vaccinated_per_hundred",
    "health_spending_pct_gdp",
    "deaths_per_million",
]


def select_latest_comparable_year(
    data: pd.DataFrame, minimum_complete_countries: int = 100
) -> int:
    """Choose the latest year with enough complete cross-country observations."""
    complete_counts = data.dropna(subset=COMPLETE_COLUMNS).groupby("year").size()
    eligible = complete_counts.loc[complete_counts >= minimum_complete_countries]
    if eligible.empty:
        raise ValueError(
            "No year has enough complete observations for a reliable comparison."
        )
    return int(eligible.index.max())


def percentile_score(series: pd.Series, higher_is_better: bool = True) -> pd.Series:
    """Convert a metric to a transparent zero-to-one percentile score."""
    score = series.rank(method="average", pct=True)
    return score if higher_is_better else 1 - score


def build_exploratory_equity_index(data: pd.DataFrame, year: int) -> pd.DataFrame:
    """Build a documented exploratory index without treating missing data as zero."""
    selected = data.loc[data["year"].eq(year)].dropna(subset=COMPLETE_COLUMNS).copy()
    selected = selected.loc[
        selected["fully_vaccinated_per_hundred"].between(0, 100)
        & selected["health_spending_pct_gdp"].ge(0)
        & selected["deaths_per_million"].ge(0)
    ].copy()
    selected["region"] = selected["region"].fillna("Not classified")
    selected["income_group"] = selected["income_group"].fillna("Not classified")

    selected["vaccination_percentile"] = percentile_score(
        selected["fully_vaccinated_per_hundred"]
    )
    selected["spending_percentile"] = percentile_score(
        selected["health_spending_pct_gdp"]
    )
    selected["mortality_percentile"] = percentile_score(
        selected["deaths_per_million"], higher_is_better=False
    )
    selected["exploratory_equity_index"] = (
        0.45 * selected["vaccination_percentile"]
        + 0.25 * selected["spending_percentile"]
        + 0.30 * selected["mortality_percentile"]
    )
    selected["rank"] = selected["exploratory_equity_index"].rank(
        ascending=False, method="min"
    ).astype(int)
    return selected.sort_values("rank").reset_index(drop=True)


def build_summary_tables(data: pd.DataFrame, year: int) -> dict[str, pd.DataFrame]:
    """Return country, region, income-group and KPI summaries for one year."""
    country = build_exploratory_equity_index(data, year)
    region = (
        country.groupby("region", dropna=False)
        .agg(
            countries=("iso_code", "nunique"),
            median_vaccination=("fully_vaccinated_per_hundred", "median"),
            median_health_spending=("health_spending_pct_gdp", "median"),
            median_deaths_per_million=("deaths_per_million", "median"),
            median_equity_index=("exploratory_equity_index", "median"),
        )
        .reset_index()
        .sort_values("median_equity_index", ascending=False)
    )
    income = (
        country.groupby("income_group", dropna=False)
        .agg(
            countries=("iso_code", "nunique"),
            median_vaccination=("fully_vaccinated_per_hundred", "median"),
            median_health_spending=("health_spending_pct_gdp", "median"),
            median_deaths_per_million=("deaths_per_million", "median"),
            median_equity_index=("exploratory_equity_index", "median"),
        )
        .reset_index()
        .sort_values("median_equity_index", ascending=False)
    )
    kpis = pd.DataFrame(
        {
            "metric": [
                "analysis_year",
                "countries_in_comparison",
                "median_fully_vaccinated_per_hundred",
                "median_health_spending_pct_gdp",
                "median_deaths_per_million",
            ],
            "value": [
                year,
                country["iso_code"].nunique(),
                country["fully_vaccinated_per_hundred"].median(),
                country["health_spending_pct_gdp"].median(),
                country["deaths_per_million"].median(),
            ],
        }
    )
    return {"country": country, "region": region, "income": income, "kpis": kpis}


def run_analysis(
    processed_path: Path = PROCESSED_PATH, output_dir: Path = OUTPUT_DIR
) -> tuple[int, dict[str, pd.DataFrame]]:
    """Read processed data and save all analytical tables."""
    data = pd.read_csv(processed_path)
    year = select_latest_comparable_year(data)
    tables = build_summary_tables(data, year)
    output_dir.mkdir(parents=True, exist_ok=True)
    tables["country"].to_csv(output_dir / "country_equity_index.csv", index=False)
    tables["region"].to_csv(output_dir / "regional_summary.csv", index=False)
    tables["income"].to_csv(output_dir / "income_group_summary.csv", index=False)
    tables["kpis"].to_csv(output_dir / "kpi_summary.csv", index=False)
    return year, tables


if __name__ == "__main__":
    selected_year, results = run_analysis()
    print(
        f"Saved analysis for {selected_year} using "
        f"{len(results['country'])} complete country records."
    )
