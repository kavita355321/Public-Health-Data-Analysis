import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#1. Load the Cleaned Dataset
df = pd.read_csv(r'C:\Users\DELL\Desktop\Public Health\data\global_vax_equity.csv')

#2. Basic Summary
print(df.info())
print(df.describe())
print(df['year'].value_counts().sort_index())

#3.Trend Over Time: Global Vaccination Progress
global_vax = df.groupby('year')['total_vaccinations'].sum().reset_index()

plt.figure(figsize=(10, 5))
sns.lineplot(data=global_vax, x='year', y='total_vaccinations', marker='o')
plt.title("Global Total Vaccinations Over Time")
plt.ylabel("Total Vaccinations")
plt.grid(True)
plt.tight_layout()
plt.show()

#4.Regional Breakdown: Vaccinations by Region
regional_vax = df.groupby(['Region', 'year'])['total_vaccinations'].sum().reset_index()

plt.figure(figsize=(12, 6))
sns.lineplot(data=regional_vax, x='year', y='total_vaccinations', hue='Region', marker='o')
plt.title("Vaccinations by Region Over Time")
plt.ylabel("Total Vaccinations")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 5. Income Group vs Health Spending
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x='IncomeGroup', y='health_spending')
plt.title("Health Spending % of GDP by Income Group")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#6.Correlation Heatmap
numeric_cols = ['total_vaccinations', 'new_cases', 'new_deaths', 'health_spending']
corr = df[numeric_cols].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title("Correlation Between Health Metrics")
plt.tight_layout()
plt.show()




