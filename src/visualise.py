"""Generate portfolio-ready figures from the validated analysis tables."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.config import FIGURE_DIR


PALETTE = "viridis"


def save_figures(
    country: pd.DataFrame,
    region: pd.DataFrame,
    year: int,
    figure_dir: Path = FIGURE_DIR,
) -> None:
    """Save five clear figures and close each figure for automated execution."""
    figure_dir.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid", context="notebook")

    plt.figure(figsize=(11, 6))
    ordered = region.sort_values("median_vaccination", ascending=False)
    sns.barplot(
        data=ordered,
        x="median_vaccination",
        y="region",
        hue="region",
        palette=PALETTE,
        legend=False,
    )
    plt.title(f"Median Full Vaccination Coverage by Region ({year})")
    plt.xlabel("People fully vaccinated per 100 residents")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(figure_dir / "vaccination_by_region.png", dpi=160)
    plt.close()

    plt.figure(figsize=(11, 6))
    sns.boxplot(
        data=country,
        x="income_group",
        y="health_spending_pct_gdp",
        hue="income_group",
        palette=PALETTE,
        legend=False,
    )
    plt.title(f"Health Spending by World Bank Income Group ({year})")
    plt.xlabel("")
    plt.ylabel("Current health expenditure (% of GDP)")
    plt.xticks(rotation=18, ha="right")
    plt.tight_layout()
    plt.savefig(figure_dir / "spending_by_income_group.png", dpi=160)
    plt.close()

    plt.figure(figsize=(11, 7))
    sns.scatterplot(
        data=country,
        x="health_spending_pct_gdp",
        y="fully_vaccinated_per_hundred",
        hue="region",
        size="population",
        sizes=(30, 280),
        alpha=0.75,
    )
    plt.title(f"Health Spending and Full Vaccination Coverage ({year})")
    plt.xlabel("Current health expenditure (% of GDP)")
    plt.ylabel("People fully vaccinated per 100 residents")
    plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left", borderaxespad=0)
    plt.tight_layout()
    plt.savefig(figure_dir / "spending_vs_vaccination.png", dpi=160)
    plt.close()

    top_bottom = pd.concat([country.head(10), country.tail(10)]).sort_values(
        "exploratory_equity_index"
    )
    plt.figure(figsize=(11, 8))
    sns.barplot(
        data=top_bottom,
        x="exploratory_equity_index",
        y="location",
        hue="exploratory_equity_index",
        palette=PALETTE,
        legend=False,
    )
    plt.title(f"Exploratory Equity Index: Highest and Lowest Scores ({year})")
    plt.xlabel("Exploratory index (0-1)")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(figure_dir / "equity_index_comparison.png", dpi=160)
    plt.close()

    correlation_columns = [
        "fully_vaccinated_per_hundred",
        "health_spending_pct_gdp",
        "deaths_per_million",
        "exploratory_equity_index",
    ]
    plt.figure(figsize=(8, 6))
    sns.heatmap(
        country[correlation_columns].corr(),
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        square=True,
    )
    plt.title(f"Correlation of Comparison Metrics ({year})")
    plt.tight_layout()
    plt.savefig(figure_dir / "correlation_heatmap.png", dpi=160)
    plt.close()

