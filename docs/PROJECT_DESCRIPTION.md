# 🏥 Public Health Data Analysis and Forecasting – Project Description

## 📌 Project Title  
**Public Health: Analysis of Global Health Expenditure and COVID-19 Vaccination Trends**

---

## 🎯 Objective  
To explore and forecast global public health indicators with a focus on:

- 💰 Health expenditure as a percentage of GDP  
- 💉 COVID-19 vaccination rates and equity  
- 📈 Predictive modeling of future vaccination coverage

---

## 📖 Project Description  
This project leverages datasets from the **World Bank** and **Our World in Data (OWID)** to perform a comprehensive analysis at the intersection of economics and pandemic response. It combines data cleaning, visual storytelling, and predictive analytics to highlight health investment disparities and forecast key global health trends.

---

## 🔍 Key Components

### 1. 📊 **Data Sources**

- **World Bank:** Health expenditure (% of GDP)  
- **OWID:** COVID-19 vaccination and case data  
- **Country Metadata:** Region and income group classifications

---

### 2. 🛠️ **ETL Pipeline (`etl.py`)**  
Processes raw data files, filters relevant fields, merges datasets, and handles null values.

---

### 3. 📈 **Exploratory Data Analysis (`eda.py`)**  
Provides statistical summaries and visual insights:
- Time-series trends in health spending  
- Regional heatmaps of vaccination rates  
- Correlation matrices and scatter plots

---

### 4. 💡 **Health Analysis (`health_analysis.py`)**  
Compares vaccination coverage with national health investments.  
Highlights inequities across regions and income groups using both numerical analysis and data visualizations.

---

### 5. 🔮 **Forecasting Module (`forecast_vaccination.py`)**  
Implements linear regression and time-series forecasting (ARIMA) to project future vaccination rates based on historical trends.

---

## 🧰 Technologies Used

- **Python 3.10+**
- **Libraries:** `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`, `statsmodels`

---

## ✅ Outcomes

- 🔍 Revealed visual and statistical gaps in global health equity  
- 🧠 Built data-driven forecasts of future vaccination trends  
- 💼 Developed a reusable and modular codebase for public health analysis

---

## 🚀 Future Enhancements

- Expand forecasting to include hospitalization and death rates  
- Build an interactive dashboard using **Streamlit** or **Dash**  
- Integrate additional public health indicators (e.g., healthcare personnel, ICU beds)
