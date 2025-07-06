# 🏥 Public Health Data Analysis & Forecasting

## 📊 Overview
This project analyzes global public health spending and COVID-19 vaccination trends using real-world datasets from **Our World in Data (OWID)** and the **World Bank**. The goal is to understand disparities in health investment and predict future vaccination coverage across countries.

---

## 🧩 Project Structure

Public-Health-Data-Analysis
→ data
   → owid-covid-data.csv              # Raw COVID data
   → global_vax_equity.csv            # Final merged dataset
   → API_SH.XPD.CHEX.GD.ZS_DS2_en_.csv # Health expenditure data
   → Metadata_Country_API_.csv        # Metadata (region, income)
→ eda.py                              # Exploratory Data Analysis
→ etl.py                              # Data Cleaning & Transformation
→ health_analysis.py                 # Core Analysis (Spending vs Outcomes)
→ forecast_vaccination.py            # Forecasting Vaccination Rates
→ __pycache__                        # Python bytecode (can be ignored)

---

## 🚀 Key Features

- ✅ Cleans and merges global COVID-19 and health spending data
- 📊 Performs EDA to highlight regional and income-level disparities
- 🔮 Forecasts future vaccination trends using regression techniques
- 📉 Reveals inequity in public health investment and impact

---

## 📁 Data Sources

- **World Bank** – Health expenditure (% of GDP)  
  [https://data.worldbank.org/indicator/SH.XPD.CHEX.GD.ZS](https://data.worldbank.org/indicator/SH.XPD.CHEX.GD.ZS)

- **Our World in Data (OWID)** – COVID-19 vaccination and case data  
  [https://ourworldindata.org/covid-vaccinations](https://ourworldindata.org/covid-vaccinations)

---

## 🛠️ Dependencies

- Python 3.10+
- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- statsmodels

Install all dependencies using:

```bash
pip install -r requirements.txt

📈 How to Use
# Step 1: Run ETL and generate merged dataset
python etl.py

# Step 2: Explore data through EDA visuals
python eda.py

# Step 3: Analyze health spending impact and equity
python health_analysis.py

# Step 4: Forecast future vaccination coverage
python forecast_vaccination.py


## 👩‍💻 About Me
**Kavita**
🎓 BSc Hons. Computer Science | Delhi University  
📫 Email: kavita355321@gmail.com  
📍 New Delhi, India
