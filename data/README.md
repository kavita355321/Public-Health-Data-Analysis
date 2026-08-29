# Data notes

This project stores source snapshots so another reviewer can reproduce the published outputs without downloading data from an external API.

| File | Provider | Purpose |
|---|---|---|
| `raw/owid-covid-data.csv.gz` | Our World in Data | Daily country vaccination, case, death and population measures through 14 August 2024 |
| `raw/world_bank_health_spending.csv` | World Bank | Current health expenditure as a percentage of GDP (`SH.XPD.CHEX.GD.ZS`) |
| `raw/world_bank_country_metadata.csv` | World Bank | Region and income-group classifications |
| `processed/global_health_equity.csv` | Generated | Validated country-year analytical table |

The pipeline reads the compressed OWID file directly; it does not need to be manually extracted.

## Why the main comparison uses 2022

The World Bank snapshot contains substantially fewer non-missing values after 2022. The code therefore selects the most recent year with at least 100 countries that have vaccination, health-spending and reported-mortality measures. With these snapshots, that year is 2022 and the final comparison includes 184 countries.

## Data licensing

The original datasets remain subject to their providers' terms. See the [OWID data licence](https://ourworldindata.org/how-to-use-our-world-in-data) and [World Bank data terms](https://www.worldbank.org/en/about/legal/terms-of-use-for-datasets). The repository's MIT licence applies to the original project code, not to third-party source data.

