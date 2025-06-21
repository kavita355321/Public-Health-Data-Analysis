#ETL (Extract-Transform-Load)
import pandas as pd

# Load OWID COVID-19 dataset
df_owid = pd.read_csv('owid-covid-data.csv')
print(df_owid[['iso_code', 'location', 'date', 'total_vaccinations']].head())

# Extract year from date
df_owid['year'] = pd.to_datetime(df_owid['date']).dt.year

# Group by year and country for COVID stats
df_owid_yearly = df_owid.groupby(['iso_code', 'location', 'year']).agg({
    'total_vaccinations': 'max',
    'new_cases': 'sum',
    'new_deaths': 'sum'
}).reset_index()
print(df_owid_yearly.head())

# Load World Bank Health Expenditure data
df_health = pd.read_csv(r"C:\Users\DELL\Desktop\Public Health\API_SH.XPD.CHEX.GD.ZS_DS2_en_csv_v2_4817.csv", skiprows=4)
df_health = df_health.drop(columns=['Indicator Name', 'Indicator Code'])

# Filter year columns only
valid_years = [col for col in df_health.columns if col.isdigit()]
df_health_long = df_health.melt(id_vars=['Country Name', 'Country Code'],
                                value_vars=valid_years,
                                var_name='year', value_name='health_spending')
df_health_long['year'] = df_health_long['year'].astype(int)
df_health_long = df_health_long.rename(columns={'Country Name': 'location'})
print(df_health_long.head())

# Merge OWID and Health Expenditure data
df_merged = pd.merge(df_owid_yearly, df_health_long, on=['location', 'year'], how='inner')
print(df_merged.head())

# Load and prepare World Bank metadata
df_meta = pd.read_csv(r"C:\Users\DELL\Desktop\Public Health\Metadata_Country_API_SH.XPD.CHEX.GD.ZS_DS2_en_csv_v2_4817.csv")
df_meta = df_meta.rename(columns={'Country Code': 'iso_code', 'TableName': 'location'})

# Merge in metadata for Region and Income Group
df_final = pd.merge(df_merged, df_meta[['iso_code', 'Region', 'IncomeGroup']], on='iso_code', how='left')
print(df_final.head())

# Save the final cleaned dataset
df_final.to_csv(r'C:\Users\DELL\Desktop\Public Health\data/global_vax_equity.csv', index=False)
print(r"Final dataset saved to: C:\Users\DELL\Desktop\Public Health\data/global_vax_equity.csv")

