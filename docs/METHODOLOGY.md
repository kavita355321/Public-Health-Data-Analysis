# Methodology

## Unit of analysis

The processed table contains one row per ISO-3 country and calendar year. OWID aggregate groups are removed because they do not represent individual countries.

Daily measures are aggregated as follows:

- `total_vaccinations`: maximum reported cumulative value in each country-year.
- `fully_vaccinated_per_hundred`: maximum reported cumulative coverage in each country-year.
- `new_cases` and `new_deaths`: sum of available daily values in each country-year.
- `population`: maximum recorded population estimate in each country-year.
- cases and deaths per million: annual totals divided by population and multiplied by one million.

World Bank health expenditure is reshaped to country-year format and joined using ISO-3 code plus year. Country classifications are joined using ISO-3 code.

## Comparison-year rule

The analysis selects the latest year containing at least 100 countries with all of the following:

- full vaccination per 100 residents;
- current health expenditure as a percentage of GDP;
- reported deaths per million.

This objective completeness rule selects 2022 from the supplied snapshots and avoids presenting a newer but highly incomplete year.

## Missing values

Missing values remain missing. A country is excluded from a comparison that requires a missing measure; missing observations are never interpreted as zero. World Bank classifications that are unavailable are displayed as `Not classified`.

## Exploratory index

Each component is converted to a percentile rank among complete country records:

- vaccination coverage: higher percentile is better;
- health expenditure: higher percentile is better;
- reported deaths per million: lower percentile is better.

The combined score is:

`0.45 × vaccination percentile + 0.25 × spending percentile + 0.30 × inverse mortality percentile`

The weighting deliberately gives vaccination coverage the largest role. It is an analyst-defined sensitivity tool, not a validated clinical, economic or policy index. Reported mortality is affected by surveillance, testing, certification and reporting systems, so a favourable score may partly reflect incomplete reporting.

## Trend scenario

A simple ordinary least-squares line is fitted to India's annual full-vaccination coverage and extended three years. Predictions are clipped to the valid 0–100 range.

Only four annual observations are available. The output therefore describes a mathematical continuation of a historical trend, not a reliable forecast. It excludes population subgroups, dose definitions, saturation dynamics, policy changes, vaccine supply and epidemiological developments.

## Interpretation standard

Results are descriptive. Correlations indicate association and do not establish causation. Country ranks should be used to identify questions for deeper investigation, never as standalone evidence of programme quality.

