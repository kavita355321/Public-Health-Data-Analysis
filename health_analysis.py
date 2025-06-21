#Health Equity Score Only
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler

# Load processed dataset
df = pd.read_csv(r'C:\Users\DELL\Desktop\Public Health\data\global_vax_equity.csv')

# Use latest available year
latest_year = df['year'].max()
df_latest = df[df['year'] == latest_year].copy()

# Fill missing values with zero for scoring
cols_to_scale = ['total_vaccinations', 'health_spending', 'new_deaths']
df_latest[cols_to_scale] = df_latest[cols_to_scale].fillna(0)

# Normalize using MinMaxScaler
scaler = MinMaxScaler()
scaled = scaler.fit_transform(df_latest[cols_to_scale])
df_latest[['vax_scaled', 'spend_scaled', 'death_scaled']] = scaled

# Invert deaths (lower is better)
df_latest['death_scaled'] = 1 - df_latest['death_scaled']

# Compute Health Equity Score (weights: 0.4, 0.4, 0.2)
df_latest['health_equity_score'] = (
    0.4 * df_latest['vax_scaled'] +
    0.4 * df_latest['spend_scaled'] +
    0.2 * df_latest['death_scaled']
)

# Plot Top 10 Countries by Health Equity Score
top10 = df_latest.sort_values('health_equity_score', ascending=False).head(10)
plt.figure(figsize=(10, 6))
sns.barplot(data=top10, y='location', x='health_equity_score', palette='Greens_d')
plt.title("Top 10 Countries by Health Equity Score")
plt.xlabel("Health Equity Score")
plt.tight_layout()
plt.show()

# Plot Bottom 10 Countries
bottom10 = df_latest.sort_values('health_equity_score').head(10)
plt.figure(figsize=(10, 6))
sns.barplot(data=bottom10, y='location', x='health_equity_score', palette='Reds_d')
plt.title("Bottom 10 Countries by Health Equity Score")
plt.xlabel("Health Equity Score")
plt.tight_layout()
plt.show()

# Save final dataset with scores
df_latest.to_csv(r'C:\Users\DELL\Desktop\Public Health\data\global_vax_equity.csv', index=False)
print("Final dataset with Health Equity Score saved.")
