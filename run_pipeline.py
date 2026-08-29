"""Run the complete reproducible public-health workflow."""

from src.analysis import run_analysis
from src.config import ensure_output_directories
from src.etl import run_etl
from src.trend_scenario import save_country_trend_scenario
from src.visualise import save_figures


def main() -> None:
    ensure_output_directories()
    processed = run_etl()
    year, tables = run_analysis()
    save_figures(tables["country"], tables["region"], year)
    save_country_trend_scenario(processed)
    print(
        f"Pipeline complete: {len(processed):,} country-year rows; "
        f"{len(tables['country'])} countries in the {year} comparison."
    )


if __name__ == "__main__":
    main()

