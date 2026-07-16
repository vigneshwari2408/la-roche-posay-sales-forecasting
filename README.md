# La Roche-Posay — Sales Forecasting & Data Analysis

**Tools:** Python · pandas · scikit-learn · PyTorch · Excel (LINEST) · SQLite · Star Schema  
**Context:** MSc Data Analytics for Business — KEDGE Business School (2025)

---

## Overview

End-to-end sales forecasting project for La Roche-Posay using 86 days of real daily sales data (Oct 1 – Dec 25, 2021). Built and compared four forecasting models, then extended the project with a full relational data model and star schema for BI reporting.

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

| Model | Method | Test MAPE |
|---|---|---|
| Model 1 — Global Average | Single mean of all training data | ~24% |
| Model 2 — Day-of-Week Average | Separate mean per weekday | ~18% |
| Model 3 — Linear Regression | Sales = intercept + Holiday + Weekend + Newsletter terms | ~13% |
| Model 4 — PyTorch LSTM | Sequence model (window = 7 days) | competitive with LR |

**Linear Regression coefficients (from LINEST / sklearn):**
- Intercept approx 2,504 (baseline quiet weekday)
- Holiday approx -414 (fewer customers on holidays)
- Weekend approx positive (higher weekend traffic)
- Newsletter = strongest positive driver

**Key finding:** Newsletter campaigns were the single strongest lever for boosting daily sales — even more than weekends.

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

The schema supports multi-market analysis (France, Germany, UK, Spain, Italy) across 5 sales channels (Website, Pharmacy, Mobile App, Amazon, Clinic). Full schema documentation: data/schema.md

---

## How to Run

```bash
git clone https://github.com/vigneshwari2408/la-roche-posay-sales-forecasting.git
cd la-roche-posay-sales-forecasting
pip install pandas numpy scikit-learn torch openpyxl
python notebooks/sales_forecasting.py
```

Note: the script expects the source Excel file at the path specified in the read_excel call. Update this to point to your local copy of the dataset.

---

## Skills Demonstrated

- Forecasting model comparison (baseline to regression to deep learning)
- Feature engineering with binary indicators
- MAPE as evaluation metric for business forecasting
- Excel financial modelling with LINEST
- Relational data modelling (star schema, SQLite)
- End-to-end project documentation

---

## About

**Vigneshwari Nalla** — MSc Data Analytics for Business, KEDGE Business School  
[LinkedIn](https://linkedin.com/in/vigna24) · [Portfolio](https://vigneshwari2408.github.io/vigneshwari-portfolio/)
