"""Create a clearly labelled exploratory vaccination trend scenario."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

from src.config import FIGURE_DIR, OUTPUT_DIR


def build_country_trend_scenario(
    data: pd.DataFrame, country: str = "India", horizon: int = 3
) -> tuple[pd.DataFrame, dict[str, float]]:
    """Fit a simple linear scenario; this is not a production forecast."""
    history = (
        data.loc[
            data["location"].eq(country)
            & data["fully_vaccinated_per_hundred"].notna(),
            ["year", "fully_vaccinated_per_hundred"],
        ]
        .drop_duplicates("year")
        .sort_values("year")
    )
    if len(history) < 3:
        raise ValueError(f"At least three annual observations are required for {country}.")

    model = LinearRegression()
    features = history[["year"]]
    target = history["fully_vaccinated_per_hundred"]
    model.fit(features, target)
    fitted = np.clip(model.predict(features), 0, 100)
    future_years = np.arange(history["year"].max() + 1, history["year"].max() + horizon + 1)
    future = np.clip(model.predict(pd.DataFrame({"year": future_years})), 0, 100)

    result = pd.concat(
        [
            history.assign(series="actual").rename(
                columns={"fully_vaccinated_per_hundred": "value"}
            ),
            pd.DataFrame(
                {"year": future_years, "value": future, "series": "trend_scenario"}
            ),
        ],
        ignore_index=True,
    )
    metrics = {
        "observations": float(len(history)),
        "in_sample_mae": float(np.mean(np.abs(target.to_numpy() - fitted))),
        "in_sample_r_squared": float(model.score(features, target)),
        "annual_slope": float(model.coef_[0]),
    }
    return result, metrics


def save_country_trend_scenario(
    data: pd.DataFrame,
    country: str = "India",
    output_dir: Path = OUTPUT_DIR,
    figure_dir: Path = FIGURE_DIR,
) -> None:
    """Save scenario data, diagnostics and a chart with an explicit caveat."""
    scenario, metrics = build_country_trend_scenario(data, country=country)
    output_dir.mkdir(parents=True, exist_ok=True)
    figure_dir.mkdir(parents=True, exist_ok=True)
    scenario.to_csv(output_dir / "india_vaccination_trend_scenario.csv", index=False)
    pd.DataFrame([metrics]).to_csv(output_dir / "trend_scenario_diagnostics.csv", index=False)

    actual = scenario.loc[scenario["series"].eq("actual")]
    future = scenario.loc[scenario["series"].eq("trend_scenario")]
    plt.figure(figsize=(10, 5.5))
    plt.plot(actual["year"], actual["value"], marker="o", label="Observed")
    plt.plot(
        future["year"],
        future["value"],
        marker="o",
        linestyle="--",
        label="Exploratory linear scenario",
    )
    plt.ylim(0, 105)
    plt.title(f"{country}: Full Vaccination Coverage Trend Scenario")
    plt.xlabel("Year")
    plt.ylabel("People fully vaccinated per 100 residents")
    plt.figtext(
        0.5,
        0.01,
        "Illustrative scenario only; limited annual observations do not support a reliable forecast.",
        ha="center",
        fontsize=9,
    )
    plt.legend()
    plt.tight_layout(rect=(0, 0.05, 1, 1))
    plt.savefig(figure_dir / "india_vaccination_trend_scenario.png", dpi=160)
    plt.close()

