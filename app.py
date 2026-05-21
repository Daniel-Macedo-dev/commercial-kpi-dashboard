import pandas as pd
import streamlit as st

from src.data_loader import load_default, load_from_upload
from src.data_cleaning import clean
from src import kpi_calculator as kpi
from src import charts
from src.insights import generate as generate_insights

st.set_page_config(
    page_title="Commercial KPI Dashboard",
    page_icon="📊",
    layout="wide",
)

# ── Formatting helpers ────────────────────────────────────────────────────────

def _fmt_currency(value: float) -> str:
    if value < 0:
        return f"-R$ {abs(value):,.0f}"
    return f"R$ {value:,.0f}"


def _fmt_percent(value: float) -> str:
    return f"{value:.1%}"


def _fmt_number(value: float) -> str:
    return f"{value:,.0f}"


# ── Data loading ──────────────────────────────────────────────────────────────

@st.cache_data
def _load_default_cached() -> pd.DataFrame:
    return clean(load_default())


def load_data(uploaded_file) -> pd.DataFrame:
    if uploaded_file is not None:
        return clean(load_from_upload(uploaded_file))
    return _load_default_cached()


# ── Sidebar ───────────────────────────────────────────────────────────────────

def sidebar_filters(df: pd.DataFrame) -> dict:
    st.sidebar.header("Filters")

    date_min = df["Date"].min().date()
    date_max = df["Date"].max().date()

    date_start = st.sidebar.date_input(
        "Start date", value=date_min, min_value=date_min, max_value=date_max
    )
    date_end = st.sidebar.date_input(
        "End date", value=date_max, min_value=date_min, max_value=date_max
    )

    regions = st.sidebar.multiselect("Region", sorted(df["Region"].unique()))
    channels = st.sidebar.multiselect("Channel", sorted(df["Channel"].unique()))
    product_lines = st.sidebar.multiselect("Product Line", sorted(df["Product Line"].unique()))
    products = st.sidebar.multiselect("Product", sorted(df["Product"].unique()))

    return {
        "date_start": date_start,
        "date_end": date_end,
        "regions": regions,
        "channels": channels,
        "product_lines": product_lines,
        "products": products,
    }


def apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    mask = (
        (df["Date"] >= pd.Timestamp(filters["date_start"]))
        & (df["Date"] <= pd.Timestamp(filters["date_end"]))
    )
    if filters["regions"]:
        mask &= df["Region"].isin(filters["regions"])
    if filters["channels"]:
        mask &= df["Channel"].isin(filters["channels"])
    if filters["product_lines"]:
        mask &= df["Product Line"].isin(filters["product_lines"])
    if filters["products"]:
        mask &= df["Product"].isin(filters["products"])
    return df[mask]


# ── KPI cards ─────────────────────────────────────────────────────────────────

def render_kpi_cards(df: pd.DataFrame) -> None:
    k = kpi.compute_all(df)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Revenue",
        _fmt_currency(k["total_revenue"]),
        help="Sum of all revenue in the selected period and filters.",
    )
    col2.metric(
        "Total Target",
        _fmt_currency(k["total_target"]),
        help="Sum of all targets in the selected period and filters.",
    )

    achievement = k["target_achievement"]
    achievement_delta = achievement - 1.0
    col3.metric(
        "Target Achievement",
        _fmt_percent(achievement),
        delta=f"{achievement_delta:+.1%} vs goal",
        help="Total Revenue ÷ Total Target. Green = above 100%, red = below.",
    )

    gap = k["gap_to_target"]
    col4.metric(
        "Gap to Target",
        _fmt_currency(gap),
        help="Revenue minus Target. Positive = above target, negative = below.",
    )

    col5, col6, col7, col8 = st.columns(4)

    col5.metric(
        "Conversion Rate",
        _fmt_percent(k["conversion_rate"]),
        help="Total Conversions ÷ Total Opportunities.",
    )
    col6.metric(
        "Avg Ticket",
        _fmt_currency(k["average_ticket"]),
        help="Total Revenue ÷ Total Units Sold.",
    )
    col7.metric(
        "Avg Discount",
        _fmt_percent(k["average_discount"]),
        help="Mean discount rate across all records in the current selection.",
    )
    col8.metric(
        "Units Sold",
        _fmt_number(k["total_units_sold"]),
        help="Total units sold across all products.",
    )


# ── Charts ────────────────────────────────────────────────────────────────────

def render_charts(df: pd.DataFrame) -> None:
    st.subheader("Revenue Trends")
    col1, col2 = st.columns(2)
    col1.plotly_chart(charts.monthly_revenue_trend(df), use_container_width=True)
    col2.plotly_chart(charts.monthly_target_vs_revenue(df), use_container_width=True)

    st.subheader("Revenue Breakdown")
    col3, col4 = st.columns(2)
    col3.plotly_chart(charts.revenue_by_region(df), use_container_width=True)
    col4.plotly_chart(charts.revenue_by_channel(df), use_container_width=True)

    col5, col6 = st.columns(2)
    col5.plotly_chart(charts.revenue_by_product_line(df), use_container_width=True)
    col6.plotly_chart(charts.top_products(df), use_container_width=True)

    st.subheader("Sales Efficiency")
    st.plotly_chart(charts.conversion_rate_by_channel(df), use_container_width=True)


# ── Insights ──────────────────────────────────────────────────────────────────

def render_insights(df: pd.DataFrame) -> None:
    st.subheader("Automatic Insights")
    for insight in generate_insights(df):
        st.info(insight)


# ── Data table ────────────────────────────────────────────────────────────────

_DISPLAY_COLS = [
    "Date", "Region", "Channel", "Product Line", "Product",
    "Sales Representative", "Revenue", "Target", "Target Achievement",
    "Gap to Target", "Opportunities", "Conversions", "Conversion Rate",
    "Units Sold", "Average Ticket", "Discount",
]
_PCT_COLS = ["Target Achievement", "Conversion Rate", "Discount"]
_CURRENCY_COLS = ["Revenue", "Target", "Gap to Target", "Average Ticket"]


def _build_display_df(df: pd.DataFrame) -> pd.DataFrame:
    cols = [c for c in _DISPLAY_COLS if c in df.columns]
    display = df[cols].sort_values("Date", ascending=False).copy()
    for col in _PCT_COLS:
        if col in display.columns:
            display[col] = display[col] * 100
    return display.reset_index(drop=True)


def _get_styler(display_df: pd.DataFrame):
    fmt: dict = {}
    for col in _CURRENCY_COLS:
        if col in display_df.columns:
            fmt[col] = lambda v: f"-R$ {abs(v):,.0f}" if v < 0 else f"R$ {v:,.0f}"
    for col in _PCT_COLS:
        if col in display_df.columns:
            fmt[col] = "{:.1f}%"
    if "Date" in display_df.columns:
        fmt["Date"] = lambda x: x.strftime("%d/%m/%Y") if hasattr(x, "strftime") else str(x)
    return display_df.style.format(fmt)


def render_data_table(df: pd.DataFrame) -> None:
    st.subheader("Filtered Data")
    display_df = _build_display_df(df)
    styler = _get_styler(display_df)
    st.dataframe(styler, use_container_width=True, hide_index=True)
    st.caption(f"{len(df):,} rows shown")


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    st.title("Commercial KPI Dashboard")
    st.markdown(
        "An interactive portfolio dashboard for commercial analytics. "
        "**All data is entirely fictional** and for demonstration purposes only."
    )

    st.sidebar.title("Data Source")
    uploaded = st.sidebar.file_uploader("Upload Excel file (.xlsx)", type=["xlsx"])
    if uploaded is None:
        st.sidebar.info(
            "Using the built-in **fictional sample dataset**.  \n"
            "Upload your own `.xlsx` file above to analyze your own data."
        )

    try:
        df = load_data(uploaded)
    except FileNotFoundError:
        st.error(
            "Sample dataset not found. "
            "Run `python src/sample_data_generator.py` to generate it, then restart the app."
        )
        st.stop()
    except ValueError as exc:
        st.error(f"Could not load data: {exc}")
        st.info(
            "Make sure your Excel file contains these required columns: "
            "**Date, Region, Channel, Product Line, Product, Sales Representative, "
            "Revenue, Target, Opportunities, Conversions, Units Sold, Discount.**"
        )
        st.stop()

    filters = sidebar_filters(df)
    filtered = apply_filters(df, filters)

    if filtered.empty:
        st.warning(
            "No data matches the selected filters. "
            "Try expanding the date range or clearing one or more filter selections."
        )
        st.stop()

    render_kpi_cards(filtered)
    st.divider()
    render_charts(filtered)
    st.divider()
    render_insights(filtered)
    st.divider()
    render_data_table(filtered)


if __name__ == "__main__":
    main()
