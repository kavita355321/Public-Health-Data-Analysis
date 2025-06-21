#Forecast Vaccination Using Linear Regression
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import numpy as np

# Load data
df = pd.read_csv(r'C:\Users\DELL\Desktop\Public Health\data\global_vax_equity.csv')

# Choose country and prepare time-based data
country = "India"
df_country = df[df['location'] == country].groupby('year')['total_vaccinations'].sum().reset_index()

# Prepare features
X = df_country[['year']]
y = df_country['total_vaccinations']

# Fit linear regression
model = LinearRegression()
model.fit(X, y)

# Predict existing and future years (e.g., next 3 years)
future_years = pd.DataFrame({'year': list(range(X['year'].min(), X['year'].max() + 4))})
future_preds = model.predict(future_years)

# Plot
plt.figure(figsize=(10, 5))
sns.scatterplot(data=df_country, x='year', y='total_vaccinations', label="Actual", color="blue")
plt.plot(future_years['year'], future_preds, color='orange', linestyle='--', label="Forecast (Linear)")
plt.title(f"Vaccination Forecast for {country} (Linear Regression)")
plt.xlabel("Year")
plt.ylabel("Total Vaccinations")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
