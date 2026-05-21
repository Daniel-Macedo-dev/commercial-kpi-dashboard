# Commercial KPI Dashboard

> Interactive commercial analytics dashboard built with Python and Streamlit.
> Fictional sample data included — portfolio project, no real company data.

[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/streamlit-1.x-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/plotly-charts-3F4F75?logo=plotly&logoColor=white)](https://plotly.com)
[![pytest](https://img.shields.io/badge/tests-82%20passing-brightgreen?logo=pytest&logoColor=white)](tests/)
[![data](https://img.shields.io/badge/data-fictional%20only-orange)](data/)

> **Disclaimer:** All data in this project is entirely fictional and randomly generated. This project is not affiliated with, endorsed by, or representative of any real company.

---

## Preview

![Dashboard Screenshot](assets/screenshot.png)

_Screenshot not yet captured. To add it: run `streamlit run app.py`, open `http://localhost:8501`, take a full-page capture, and save it as `assets/screenshot.png`._

---

## Quick Review

For recruiters and interviewers — get the dashboard running in under two minutes:

```bash
pip install -r requirements.txt           # 1. install dependencies
python src/sample_data_generator.py       # 2. generate fictional dataset
streamlit run app.py                      # 3. open http://localhost:8501
python -m pytest -v                       # 4. run all 25 unit tests
```

Things to explore in the running dashboard:
- Use the **sidebar filters** to narrow by date range, Region, Channel, or Product Line
- Read the **Executive Summary** for colour-coded business findings (green/yellow/red)
- Check the **Performance Diagnostics** tabs for region, channel, and product line breakdowns
- Click a **download button** to export the filtered dataset or KPI summary as CSV
- Upload a custom `.xlsx` file via the sidebar (see [expected schema](#using-your-own-excel-file) below)

---

## Business Problem

Sales and commercial teams need a clear view of how revenue compares to targets, where conversions are happening, which regions and channels are leading or lagging, and whether discounting is within acceptable boundaries. Traditionally this analysis lives in static Excel reports.

This dashboard replaces that workflow with an interactive, filter-driven view that updates all KPIs, charts, diagnostics, and insights in real time as the user applies filters.

---

## What the Dashboard Analyses

- **Revenue vs Target** — total performance and gap across any filtered subset
- **Target Achievement %** — at overall, regional, channel, and product line level
- **Conversion Rate** — from opportunity to closed deal, across channels
- **Discount Behaviour** — average discount and whether it is within safe thresholds
- **Top Products and Regions** — ranked by revenue contribution
- **Underperforming Segments** — automatically identified and flagged in the executive summary

---

## Key Features

| Feature | Description |
|---------|-------------|
| KPI cards | 8 headline metrics with formatted currency, %, and contextual delta on Target Achievement |
| Executive Summary | Colour-coded narrative findings (revenue, drivers, conversion, discount) |
| 7 Plotly charts | Monthly trend, Revenue vs Target, Region/Channel/Product Line breakdowns, Top Products, Conversion by Channel |
| Performance Diagnostics | Tabbed tables showing Revenue, Target, Achievement %, and Gap by Region, Channel, and Product Line |
| Automatic Insights | 5–6 rule-based business commentary items |
| Sidebar filters | Date range, Region, Channel, Product Line, Product — all reactive |
| Excel upload | Bring your own `.xlsx` file; sample dataset used by default |
| CSV exports | Filtered dataset, KPI summary, and diagnostics — all reflecting current filters |
| Formatted data table | Discount, Achievement %, and Conversion Rate shown as % (not raw decimals) |
| Bilingual UI | Full English / Português toggle — all labels, filter controls (expander+checkboxes avoid hardcoded English "Select all"), localized date range selector (Month/Year/Day controls with Portuguese month names avoid English calendar labels), charts, diagnostics, and insights. Fictional dataset values remain in English internally; translated values are display-only and do not affect filtering, calculations, or CSV exports. |

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
├── app.py                           # Streamlit entry point (orchestration only)
├── requirements.txt
├── README.md
├── .streamlit/
│   └── config.toml                  # Visual theme
├── data/
│   └── sample_commercial_data.xlsx  # Generated fictional dataset (400 rows)
├── src/
│   ├── sample_data_generator.py     # Generates the fictional Excel dataset
│   ├── data_loader.py               # Loads Excel from file or Streamlit upload
│   ├── data_cleaning.py             # Cleans data and adds derived columns
│   ├── kpi_calculator.py            # Pure KPI functions (no Streamlit dependency)
│   ├── charts.py                    # Plotly chart builders
│   └── insights.py                  # Insights, executive summary, diagnostics
├── tests/
│   ├── test_kpi_calculator.py       # Unit tests for KPI logic
│   └── test_insights.py             # Unit tests for summary and diagnostics
├── assets/
│   └── screenshot.png               # Place dashboard screenshot here
└── docs/
```

---

## Getting Started

### 1. Create and activate a virtual environment

```bash
# Windows — PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Windows — Command Prompt / Git Bash
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python -m venv .venv
source .venv/bin/activate
```

> **PowerShell note:** if you see an execution policy error, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once and try again.

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

Open `http://localhost:8501` in your browser. The sample dataset loads automatically.

### 5. Run the tests

```bash
python -m pytest -v
```

---

## Using the Sample Dataset

When no file is uploaded, the dashboard loads `data/sample_commercial_data.xlsx` automatically. This dataset contains:

- ~17 months of fictional sales records (Jan 2025 – May 2026)
- 5 regions, 5 channels, 5 product lines, 20 products, 10 fictional sales reps
- 400 rows with randomised but realistic revenue, targets, opportunities, conversions, and discounts

---

## Using Your Own Excel File

Upload any `.xlsx` file via the **Data Source** panel in the sidebar. Your file must contain these columns (exact names, case-sensitive):

| Column | Type | Description |
|--------|------|-------------|
| Date | Date | Transaction or period date |
| Region | Text | Sales region name |
| Channel | Text | Sales channel (e.g. Hospital, Retail) |
| Product Line | Text | Product category |
| Product | Text | Product name |
| Sales Representative | Text | Rep name or ID |
| Revenue | Number | Revenue amount |
| Target | Number | Revenue target |
| Opportunities | Integer | Number of opportunities in the period |
| Conversions | Integer | Number of conversions |
| Units Sold | Integer | Units sold |
| Discount | Number | Discount rate (0.0 to 1.0, e.g. 0.15 for 15%) |

If any required column is missing, the app shows a clear error listing exactly which columns are absent.

---

## Validation and Tests

The project includes 82 unit tests across five files:

- **`tests/test_kpi_calculator.py`** — all 13 KPI functions, including zero-division edge cases
- **`tests/test_insights.py`** — `build_dimension_diagnostics` (aggregation, achievement, gap, sorting) and `generate_executive_summary` (structure, status logic, single-region edge case)
- **`tests/test_i18n.py`** — translation lookup, language fallback, kwargs interpolation, and PT/EN key parity
- **`tests/test_display_map.py`** — value mapping (all regions, channels, product lines), reverse mapping, unknown-value fallback, filter round-trip, and column header translation
- **`tests/test_date_utils.py`** — `months_for()` (12 entries, language fallback, EN/PT values) and `make_date()` (valid days, clamping for short months, leap year handling)

Business logic lives entirely in `src/` modules with no Streamlit dependency — it can be imported, tested, and reused independently.

```bash
python -m pytest -v
```

---

## MVP Status

The dashboard is fully functional and portfolio-ready:

- KPIs display with formatted currency (R$), percentages, and thousands separators
- Target Achievement card shows a coloured delta vs the 100% goal
- Data table formats Discount, Conversion Rate, and Target Achievement as percentages
- All 7 Plotly charts include formatted axis ticks (R$ prefix) and hover tooltips
- Executive Summary provides colour-coded narrative findings (green/yellow/red)
- Performance Diagnostics tabs show dimension-level breakdown by Region, Channel, and Product Line
- 3 CSV export buttons reflect the current filter state
- Visual theme is neutral and professional — not based on any real company's branding

---

## Portfolio Relevance

This project demonstrates skills relevant to **commercial analytics**, **sales excellence**, **BI analyst**, and **data internship** roles:

- End-to-end data pipeline: loading, cleaning, transformation, aggregation
- KPI design and calculation for a commercial/sales context
- Interactive dashboard development with Streamlit and Plotly
- Performance diagnostics: identifying leaders and laggards by dimension
- Rule-based insight and narrative generation from business data
- Professional data formatting (currency, percentages, thousands separators)
- Modular, testable Python code with separation of business logic from UI
- CSV export for stakeholder use outside the dashboard

> The visual theme is neutral and not based on any real company's branding or design guidelines.
