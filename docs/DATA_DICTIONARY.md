# Data dictionary

## Processed analytical table

| Field | Description |
|---|---|
| `iso_code` | ISO-3 country code used for joins |
| `location` | OWID country name |
| `continent` | OWID continent |
| `year` | Calendar year |
| `total_vaccinations` | Maximum cumulative vaccine doses reported during the year |
| `fully_vaccinated_per_hundred` | Maximum people fully vaccinated per 100 residents during the year |
| `new_cases` | Sum of available daily reported cases during the year |
| `new_deaths` | Sum of available daily reported deaths during the year |
| `population` | Population estimate used for rate calculation |
| `cases_per_million` | Annual reported cases per million residents |
| `deaths_per_million` | Annual reported deaths per million residents |
| `health_spending_pct_gdp` | Current health expenditure as a percentage of GDP |
| `region` | World Bank region |
| `income_group` | World Bank income classification |

## Country comparison additions

| Field | Description |
|---|---|
| `vaccination_percentile` | Country percentile for full-vaccination coverage |
| `spending_percentile` | Country percentile for health spending as a share of GDP |
| `mortality_percentile` | Inverse percentile for reported deaths per million |
| `exploratory_equity_index` | Weighted exploratory score from zero to one |
| `rank` | Descending rank of the exploratory score |

