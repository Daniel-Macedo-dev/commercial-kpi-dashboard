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


def _fmt_currency(value: float) -> str:
    return f"R$ {value:,.0f}"


def _fmt_percent(value: float) -> str:
    return f"{value:.1%}"


def _fmt_number(value: float) -> str:
    return f"{value:,.0f}"


@st.cache_data
def _load_default_cached() -> pd.DataFrame:
    return clean(load_default())


def load_data(uploaded_file) -> pd.DataFrame:
    if uploaded_file is not None:
        return clean(load_from_upload(uploaded_file))
    return _load_default_cached()


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


def render_kpi_cards(df: pd.DataFrame) -> None:
    k = kpi.compute_all(df)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", _fmt_currency(k["total_revenue"]))
    col2.metric("Total Target", _fmt_currency(k["total_target"]))
    col3.metric("Target Achievement", _fmt_percent(k["target_achievement"]))
    col4.metric("Gap to Target", _fmt_currency(k["gap_to_target"]))

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Conversion Rate", _fmt_percent(k["conversion_rate"]))
    col6.metric("Avg Ticket", _fmt_currency(k["average_ticket"]))
    col7.metric("Avg Discount", _fmt_percent(k["average_discount"]))
    col8.metric("Units Sold", _fmt_number(k["total_units_sold"]))


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


def render_insights(df: pd.DataFrame) -> None:
    st.subheader("Automatic Insights")
    for insight in generate_insights(df):
        st.info(insight)


def render_data_table(df: pd.DataFrame) -> None:
    st.subheader("Filtered Data")
    display_cols = [
        "Date", "Region", "Channel", "Product Line", "Product",
        "Sales Representative", "Revenue", "Target", "Target Achievement",
        "Gap to Target", "Opportunities", "Conversions", "Conversion Rate",
        "Units Sold", "Average Ticket", "Discount",
    ]
    cols_present = [c for c in display_cols if c in df.columns]
    st.dataframe(
        df[cols_present].sort_values("Date", ascending=False),
        use_container_width=True,
    )
    st.caption(f"{len(df):,} rows shown")


def main() -> None:
    st.title("Commercial KPI Dashboard")
    st.markdown(
        "An interactive portfolio dashboard for commercial analytics. "
        "**All data is entirely fictional** and for demonstration purposes only."
    )

    st.sidebar.title("Data Source")
    uploaded = st.sidebar.file_uploader("Upload Excel file (.xlsx)", type=["xlsx"])
    if uploaded is None:
        st.sidebar.info("Using default sample dataset.")

    try:
        df = load_data(uploaded)
    except (FileNotFoundError, ValueError) as exc:
        st.error(str(exc))
        st.stop()

    filters = sidebar_filters(df)
    filtered = apply_filters(df, filters)

    if filtered.empty:
        st.warning("No data matches the selected filters. Adjust the filters and try again.")
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
