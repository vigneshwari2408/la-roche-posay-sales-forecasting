# La Roche-Posay — Sales Forecasting & Data Analysis

**Tools:** Python · pandas · scikit-learn · PyTorch · Excel (LINEST) · SQLite · Star Schema  
**Context:** MSc Data Analytics for Business — KEDGE Business School (2025)

---

## Overview

End-to-end sales forecasting project for La Roche-Posay using a daily sales workbook covering Oct 1 – Dec 25, 2021 (74 days with observed sales, plus 12 days to forecast). Built and compared three forecasting models in Excel and Python, plus a PyTorch LSTM script (not yet run; see Limitations), then extended the project with a full relational data model and star schema for BI reporting.

**Business question:** Can we predict daily sales using calendar and marketing signals — day of week, holidays, and newsletter campaigns?

---

## Dataset

| Split | Period | Rows |
|---|---|---|
| Learning | Oct 1 – Nov 28, 2021 | 59 |
| Testing | Nov 29 – Dec 13, 2021 | 15 |
| Forecast | Dec 14 – Dec 25, 2021 | 12 |

**Features:** is_holiday, is_weekend, newsletter  
**Target:** Daily sales (units)

---

## Models & Results

| Model | Method | Test MAPE (script) | Test MAPE (Excel sheets) |
|---|---|---|---|
| Model 1 — Global Average | Single mean of all training data | 17.2% | 17.9% |
| Model 2 — Day-of-Week Average | Separate mean per weekday | 12.7% | 12.4% |
| Model 3 — Linear Regression | Sales = intercept + Holiday + Weekend + Newsletter terms | 9.1% | 9.1% |
| Model 4 — PyTorch LSTM | Sequence model (window = 7 days) | not run | not applicable |

Test window: 15 days (Nov 29 – Dec 13, 2021). The small gap between the script and the Excel sheets for Models 1 and 2 is not yet explained.

**Linear Regression coefficients (from LINEST / sklearn):**
- Intercept approx 2,504 (baseline quiet weekday)
- Holiday approx -414 (fewer customers on holidays)
- Weekend about +1,265 units
- Newsletter about +3,133 units (largest of the three effects)

**Key finding:** In this dataset, newsletter days had the largest estimated effect on daily sales, larger than weekends. Treat it as indicative: only 3 of the 59 learning days and 1 of the 15 test days had a newsletter, and the test window had no holidays.

---

## Project Structure
```
la-roche-posay-sales-forecasting/
├── notebooks/sales_forecasting.py                  # All 4 models: Global Avg, DoW, Linear Regression, LSTM
├── excel/La_Roche_Posay_Sales_Forecasting.xlsx     # Full Excel workbook with LINEST models
├── data/schema.md                                  # Star schema documentation
└── README.md
```
---

## Data Model

Designed a star schema for BI reporting across e-commerce and retail channels:

**Fact tables:** fact_sales, fact_orders, fact_inventory, fact_reviews, fact_campaign  
**Dimension tables:** dim_customer, dim_product, dim_date, dim_channel, dim_location

The schema is designed for multi-market analysis (France, Germany, UK, Spain, Italy) across 5 sales channels (Website, Pharmacy, Mobile App, Amazon, Clinic). `data/larocheposay.db` contains the 10 tables with 5 sample rows each; no analysis has been run on them. Full schema documentation: data/schema.md

---

## How to Run

```bash
git clone https://github.com/vigneshwari2408/la-roche-posay-sales-forecasting.git
cd la-roche-posay-sales-forecasting
pip install pandas numpy scikit-learn torch openpyxl
python notebooks/sales_forecasting.py
```

The script reads the "Raw Data" sheet of `excel/La_Roche_Posay_Sales_Forecasting.xlsx` relative to its own location, so no path edit is needed.

---

## Limitations

- **Small sample:** 59 learning days, 15 test days. MAPE on 15 days is volatile.
- **Newsletter effect:** estimated from 3 newsletter days in the learning period.
- **Holidays:** the test window contains none, so the holiday effect is not tested out of sample.
- **Day names:** the workbook's "Day Name" column is one day later than the calendar dates (2021-10-01 was a Friday, labelled Saturday). The weekend flags match the real calendar; the day-of-week model groups by the day number, so its grouping is unaffected.
- **Data origin:** the workbook's notes refer to a professor's module example. This README does not claim the data is company data.
- **LSTM:** the script includes it, but its results have not been checked or reported here. Its test windows also use actual lagged sales, which the regression does not, so it would not be a like-for-like comparison.

---

## Skills Demonstrated

- Forecasting model comparison (baselines to regression)
- Feature engineering with binary indicators
- MAPE as evaluation metric for business forecasting
- Excel financial modelling with LINEST
- Relational data modelling (star schema, SQLite)
- End-to-end project documentation

---

Made by **Vigneshwari Nalla (Vee)** · MSc Data Analytics for Business, KEDGE Business School
[website](https://vigneshwari2408.github.io/vigneshwari-portfolio/) · [linkedin](https://www.linkedin.com/in/vigna24/) · [all projects](https://github.com/vigneshwari2408)
