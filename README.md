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

**Features:** `is_holiday`, `is_weekend`, `newsletter`  
**Target:** Daily sales (units)

---

## Models & Results

| Model | Method | Test MAPE |
|---|---|---|
| Model 1 — Global Average | Single mean of all training data | ~24% |
| Model 2 — Day-of-Week Average | Separate mean per weekday | ~18% |
| Model 3 — Linear Regression | `Sales = β₀ + β₁·Holiday + β₂·Weekend + β₃·Newsletter` | ~13% |
| Model 4 — PyTorch LSTM | Sequence model (window = 7 days) | competitive with LR |

**Linear Regression coefficients (from LINEST / sklearn):**
- Intercept β₀ ≈ 2,504 (baseline quiet weekday)
- Holiday β₁ ≈ −414 (fewer customers on holidays)
- Weekend β₂ ≈ positive (higher weekend traffic)
- Newsletter β₃ = strongest positive driver

**Key finding:** Newsletter campaigns were the single strongest lever for boosting daily sales — even more than weekends.

---

## Project Structure

```
├── notebooks/
│   └── sales_forecasting.py       # All 4 models: Global Avg, DoW, Linear Regression, LSTM
├── excel/
│   └── La_Roche_Posay_Sales_Forecasting.xlsx  # Full Excel workbook with LINEST models
├── data/
│   └── schema.md                  # Star schema documentation
├── assets/
│   └── star_schema.png            # Data model diagram
└── README.md
```

---

## Data Model

Designed a star schema for BI reporting across e-commerce and retail channels:

**Fact tables:** `fact_sales`, `fact_orders`, `fact_inventory`, `fact_reviews`, `fact_campaign`  
**Dimension tables:** `dim_customer`, `dim_product`, `dim_date`, `dim_channel`, `dim_location`

The schema supports multi-market analysis (France, Germany, UK, Spain, Italy) across 5 sales channels (Website, Pharmacy, Mobile App, Amazon, Clinic).

---

## How to Run

```bash
# Clone the repo
git clone https://github.com/vigna24/la-roche-posay-sales-forecasting.git
cd la-roche-posay-sales-forecasting

# Install dependencies
pip install pandas numpy scikit-learn torch openpyxl

# Run all models
python notebooks/sales_forecasting.py
```

> **Note:** The script expects the source Excel file at the path specified in `df_raw = pd.read_excel(...)`. Update this to point to your local copy of the dataset.

---

## Skills Demonstrated

- Forecasting model comparison (baseline → regression → deep learning)
- Feature engineering with binary indicators
- MAPE as evaluation metric for business forecasting
- Excel financial modelling with LINEST
- Relational data modelling (star schema, SQLite)
- End-to-end project documentation

---

## About

**Vigneshwari Nalla** — MSc Data Analytics for Business, KEDGE Business School  
[LinkedIn](https://linkedin.com/in/vigna24) · [Portfolio](https://vigna2408.github.io)
