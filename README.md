# Commercial KPI Dashboard

An interactive Streamlit dashboard for commercial analytics, built as a portfolio project.
Displays fictional sales data with KPIs, charts, filters, and automatic business insights.

> **Data disclaimer:** All data used in this project is entirely fictional and randomly generated.
> This project is not affiliated with, endorsed by, or representative of any real company.

---

## Features

- **KPI cards** — Total Revenue, Target Achievement, Gap to Target, Conversion Rate, Avg Ticket, Avg Discount
- **Interactive filters** — Date range, Region, Channel, Product Line, Product
- **7 Plotly charts** — Monthly trend, Revenue vs Target, breakdown by Region/Channel/Product Line, Top Products, Conversion Rate by Channel
- **Automatic insights** — Rule-based business commentary on target performance, top segments, conversion, and discount levels
- **Excel upload** — Use the default sample dataset or upload your own `.xlsx` file with the same column structure
- **Filtered data table** — Paginated view of the records matching the active filters

---

## Tech Stack

| Layer | Library |
|-------|---------|
| Dashboard | Streamlit |
| Data | Pandas, OpenPyXL |
| Charts | Plotly |
| Numerics | NumPy |
| Tests | Pytest |

---

## Project Structure

```
KPI/
├── app.py                      # Streamlit entry point (orchestration only)
├── requirements.txt
├── README.md
├── data/
│   └── sample_commercial_data.xlsx   # Generated fictional dataset
├── src/
│   ├── sample_data_generator.py      # Generates the fictional Excel dataset
│   ├── data_loader.py                # Loads Excel from file or Streamlit upload
│   ├── data_cleaning.py              # Cleans data and adds derived columns
│   ├── kpi_calculator.py             # Pure KPI functions (no Streamlit dependency)
│   ├── charts.py                     # Plotly chart builders
│   └── insights.py                   # Rule-based insight generation
├── tests/
│   └── test_kpi_calculator.py        # Unit tests for KPI logic
├── assets/
└── docs/
```

---

## Getting Started

### 1. Create and activate a virtual environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Generate the sample dataset

```bash
python src/sample_data_generator.py
```

This creates `data/sample_commercial_data.xlsx` with 400 rows of fictional commercial data.

### 4. Run the dashboard

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

### 5. Run the tests

```bash
python -m pytest
```

---

## Dataset Columns

| Column | Description |
|--------|-------------|
| Date | Transaction date |
| Region | Sales region (North, Northeast, Midwest, Southeast, South) |
| Channel | Sales channel (Hospital, Distributor, Retail, Online, Clinic) |
| Product Line | Fictional product category |
| Product | Fictional product name |
| Sales Representative | Fictional rep name |
| Revenue | Revenue amount (R$) |
| Target | Revenue target (R$) |
| Opportunities | Number of sales opportunities |
| Conversions | Number of converted opportunities |
| Units Sold | Units sold |
| Discount | Discount rate applied (0–25%) |

---

## Portfolio Relevance

This project demonstrates skills relevant to **commercial analytics**, **sales excellence**, and **data analyst / BI internship** roles:

- End-to-end data pipeline: loading, cleaning, transformation, and aggregation
- KPI design and calculation for a sales context
- Interactive dashboard development with Streamlit and Plotly
- Modular, testable Python code structure
- Rule-based insight generation from business data
