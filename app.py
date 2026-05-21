import pandas as pd
import streamlit as st

from src.data_loader import load_default, load_from_upload
from src.data_cleaning import clean
from src import kpi_calculator as kpi
from src import charts
from src import display_map as dm
from src.i18n import t, SUPPORTED_LANGS
from src.insights import (
    generate as generate_insights,
    generate_executive_summary,
    build_dimension_diagnostics,
)

st.set_page_config(
    page_title="Commercial KPI Dashboard",
    page_icon="📊",
    layout="wide",
)

# ── Formatting helpers ────────────────────────────────────────────────────────

def _fmt_currency(value: float) -> str:
    if value < 0:
        return f"-R\\$ {abs(value):,.0f}"
    return f"R\\$ {value:,.0f}"


def _fmt_compact(value: float) -> str:
    """Compact currency for KPI cards: R$ 1.2M / R$ 450K / R$ 9,800."""
    abs_val = abs(value)
    if abs_val >= 1_000_000:
        formatted = f"R\\$ {abs_val / 1_000_000:.1f}M"
    elif abs_val >= 1_000:
        formatted = f"R\\$ {abs_val / 1_000:.0f}K"
    else:
        formatted = f"R\\$ {abs_val:,.0f}"
    return f"-{formatted}" if value < 0 else formatted


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


# ── Display copy ──────────────────────────────────────────────────────────────

def _make_display_df(df: pd.DataFrame, lang: str) -> pd.DataFrame:
    """Return a copy of df with categorical values translated for display.

    Calculations always use the raw df; charts and tables use this copy.
    """
    if lang != "pt":
        return df
    copy = df.copy()
    copy["Region"] = dm.translate_series(copy["Region"], "region", lang)
    copy["Channel"] = dm.translate_series(copy["Channel"], "channel", lang)
    copy["Product Line"] = dm.translate_series(copy["Product Line"], "product_line", lang)
    return copy


# ── Sidebar ───────────────────────────────────────────────────────────────────

def sidebar_lang() -> str:
    lang_labels = {"en": "English", "pt": "Português"}
    options = SUPPORTED_LANGS
    selected = st.sidebar.selectbox(
        "Language / Idioma",
        options=options,
        format_func=lambda x: lang_labels.get(x, x),
        key="lang_selector",
    )
    st.sidebar.divider()
    return selected


def sidebar_filters(df: pd.DataFrame, lang: str) -> dict:
    st.sidebar.header(t(lang, "filters"))

    date_min = df["Date"].min().date()
    date_max = df["Date"].max().date()

    date_start = st.sidebar.date_input(
        t(lang, "start_date"), value=date_min, min_value=date_min, max_value=date_max
    )
    date_end = st.sidebar.date_input(
        t(lang, "end_date"), value=date_max, min_value=date_min, max_value=date_max
    )

    placeholder = t(lang, "choose_options")

    raw_regions = sorted(df["Region"].unique())
    sel_regions_disp = st.sidebar.multiselect(
        t(lang, "region"),
        options=dm.translate_options(raw_regions, "region", lang),
        placeholder=placeholder,
    )
    regions = dm.raw_selections(sel_regions_disp, "region", lang)

    raw_channels = sorted(df["Channel"].unique())
    sel_channels_disp = st.sidebar.multiselect(
        t(lang, "channel"),
        options=dm.translate_options(raw_channels, "channel", lang),
        placeholder=placeholder,
    )
    channels = dm.raw_selections(sel_channels_disp, "channel", lang)

    raw_pls = sorted(df["Product Line"].unique())
    sel_pls_disp = st.sidebar.multiselect(
        t(lang, "product_line"),
        options=dm.translate_options(raw_pls, "product_line", lang),
        placeholder=placeholder,
    )
    product_lines = dm.raw_selections(sel_pls_disp, "product_line", lang)

    # Products: brand names kept in English across all modes
    products = st.sidebar.multiselect(
        t(lang, "product"),
        sorted(df["Product"].unique()),
        placeholder=placeholder,
    )

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

def render_kpi_cards(df: pd.DataFrame, lang: str) -> None:
    k = kpi.compute_all(df)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(
        t(lang, "total_revenue"),
        _fmt_compact(k["total_revenue"]),
        help=t(lang, "help_revenue"),
    )
    col2.metric(
        t(lang, "total_target"),
        _fmt_compact(k["total_target"]),
        help=t(lang, "help_target"),
    )
    achievement = k["target_achievement"]
    col3.metric(
        t(lang, "target_achievement"),
        _fmt_percent(achievement),
        delta=f"{achievement - 1.0:+.1%} {t(lang, 'vs_goal')}",
        help=t(lang, "help_achievement"),
    )
    col4.metric(
        t(lang, "gap_to_target"),
        _fmt_compact(k["gap_to_target"]),
        help=t(lang, "help_gap"),
    )

    col5, col6, col7, col8 = st.columns(4)
    col5.metric(
        t(lang, "conversion_rate"),
        _fmt_percent(k["conversion_rate"]),
        help=t(lang, "help_conversion"),
    )
    col6.metric(
        t(lang, "avg_ticket"),
        _fmt_compact(k["average_ticket"]),
        help=t(lang, "help_ticket"),
    )
    col7.metric(
        t(lang, "avg_discount"),
        _fmt_percent(k["average_discount"]),
        help=t(lang, "help_discount"),
    )
    col8.metric(
        t(lang, "units_sold"),
        _fmt_number(k["total_units_sold"]),
        help=t(lang, "help_units"),
    )


# ── Executive summary ─────────────────────────────────────────────────────────

_STATUS_FN = {
    "good": st.success,
    "warning": st.warning,
    "bad": st.error,
    "neutral": st.info,
}


def render_executive_summary(df: pd.DataFrame, lang: str) -> None:
    st.subheader(t(lang, "executive_summary"))
    # Always pass raw df — insights.py translates dimension names internally
    items = generate_executive_summary(df, lang=lang)
    if not items:
        st.info(t(lang, "no_summary"))
        return
    for item in items:
        render_fn = _STATUS_FN.get(item["status"], st.info)
        render_fn(f"**{item['label']}:** {item['text']}")


# ── Charts ────────────────────────────────────────────────────────────────────

def render_charts(display_df: pd.DataFrame, lang: str) -> None:
    """Render all Plotly charts. Receives a display df with translated values."""
    st.subheader(t(lang, "revenue_trends"))
    col1, col2 = st.columns(2)
    col1.plotly_chart(charts.monthly_revenue_trend(display_df, lang), use_container_width=True)
    col2.plotly_chart(charts.monthly_target_vs_revenue(display_df, lang), use_container_width=True)

    st.subheader(t(lang, "revenue_breakdown"))
    col3, col4 = st.columns(2)
    col3.plotly_chart(charts.revenue_by_region(display_df, lang), use_container_width=True)
    col4.plotly_chart(charts.revenue_by_channel(display_df, lang), use_container_width=True)

    col5, col6 = st.columns(2)
    col5.plotly_chart(charts.revenue_by_product_line(display_df, lang), use_container_width=True)
    col6.plotly_chart(charts.top_products(display_df, lang=lang), use_container_width=True)

    st.subheader(t(lang, "sales_efficiency"))
    st.plotly_chart(charts.conversion_rate_by_channel(display_df, lang), use_container_width=True)


# ── Performance diagnostics ───────────────────────────────────────────────────

_DIM_CATEGORY = {"Region": "region", "Channel": "channel", "Product Line": "product_line"}


def render_diagnostics(df: pd.DataFrame, lang: str) -> None:
    st.subheader(t(lang, "diagnostics"))
    st.caption(t(lang, "diagnostics_caption"))
    # Aggregate on raw df to keep calculations correct
    diagnostics = build_dimension_diagnostics(df)
    if not diagnostics:
        return

    tab_labels = [
        t(lang, "tab_region"),
        t(lang, "tab_channel"),
        t(lang, "tab_product_line"),
    ]
    tabs = st.tabs(tab_labels)
    headers = dm.col_headers(lang)

    for tab, (dim, diag_df) in zip(tabs, diagnostics.items()):
        with tab:
            display = diag_df.copy()
            display["Achievement %"] = display["Achievement %"] * 100

            # Translate dimension values for display
            cat = _DIM_CATEGORY.get(dim, "")
            if cat:
                display[dim] = dm.translate_series(display[dim], cat, lang)

            styler = display.style.format({
                "Revenue": "R$ {:,.0f}",
                "Target": "R$ {:,.0f}",
                "Achievement %": "{:.1f}%",
                "Gap to Target": lambda v: f"-R$ {abs(v):,.0f}" if v < 0 else f"R$ {v:,.0f}",
            })

            if headers:
                new_labels = [headers.get(c, c) for c in display.columns]
                styler = styler.relabel_index(new_labels, axis="columns")

            st.dataframe(styler, use_container_width=True, hide_index=True)


# ── Insights ──────────────────────────────────────────────────────────────────

def render_insights(df: pd.DataFrame, lang: str) -> None:
    st.subheader(t(lang, "insights"))
    for insight in generate_insights(df, lang=lang):
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


def render_data_table(df: pd.DataFrame, lang: str) -> None:
    st.subheader(t(lang, "filtered_data"))
    display_df = _build_display_df(df)

    # Translate categorical values in the display copy
    for col, cat in [("Region", "region"), ("Channel", "channel"), ("Product Line", "product_line")]:
        if col in display_df.columns:
            display_df[col] = dm.translate_series(display_df[col], cat, lang)

    styler = _get_styler(display_df)

    # Relabel column headers for PT mode (relabel_index changes display only)
    headers = dm.col_headers(lang)
    if headers:
        new_labels = [headers.get(c, c) for c in display_df.columns]
        styler = styler.relabel_index(new_labels, axis="columns")

    st.dataframe(styler, use_container_width=True, hide_index=True)
    st.caption(t(lang, "rows_shown", n=len(df)))


# ── Exports ───────────────────────────────────────────────────────────────────

def _kpi_summary_csv(k: dict) -> bytes:
    rows = [
        ("Total Revenue (R$)", round(k["total_revenue"], 2)),
        ("Total Target (R$)", round(k["total_target"], 2)),
        ("Target Achievement (%)", round(k["target_achievement"] * 100, 2)),
        ("Gap to Target (R$)", round(k["gap_to_target"], 2)),
        ("Total Opportunities", k["total_opportunities"]),
        ("Total Conversions", k["total_conversions"]),
        ("Conversion Rate (%)", round(k["conversion_rate"] * 100, 2)),
        ("Total Units Sold", k["total_units_sold"]),
        ("Average Ticket (R$)", round(k["average_ticket"], 2)),
        ("Average Discount (%)", round(k["average_discount"] * 100, 2)),
        ("Best Region", k["best_region"]),
        ("Best Product Line", k["best_product_line"]),
        ("Best Channel", k["best_channel"]),
    ]
    return pd.DataFrame(rows, columns=["Metric", "Value"]).to_csv(index=False).encode("utf-8-sig")


def _diagnostics_csv(df: pd.DataFrame) -> bytes:
    diagnostics = build_dimension_diagnostics(df)
    frames = []
    for dim, diag_df in diagnostics.items():
        copy = diag_df.copy()
        copy.insert(0, "Dimension", dim)
        copy.rename(columns={dim: "Category"}, inplace=True)
        copy["Achievement %"] = (copy["Achievement %"] * 100).round(2)
        copy["Revenue"] = copy["Revenue"].round(2)
        copy["Target"] = copy["Target"].round(2)
        copy["Gap to Target"] = copy["Gap to Target"].round(2)
        frames.append(copy)
    return pd.concat(frames, ignore_index=True).to_csv(index=False).encode("utf-8-sig")


def render_exports(filtered: pd.DataFrame, lang: str) -> None:
    st.subheader(t(lang, "export"))
    k = kpi.compute_all(filtered)

    col1, col2, col3 = st.columns(3)
    col1.download_button(
        label=t(lang, "btn_filtered"),
        data=filtered.to_csv(index=False).encode("utf-8-sig"),
        file_name="kpi_filtered_data.csv",
        mime="text/csv",
        help=t(lang, "help_btn_filtered"),
    )
    col2.download_button(
        label=t(lang, "btn_kpi"),
        data=_kpi_summary_csv(k),
        file_name="kpi_summary.csv",
        mime="text/csv",
        help=t(lang, "help_btn_kpi"),
    )
    col3.download_button(
        label=t(lang, "btn_diagnostics"),
        data=_diagnostics_csv(filtered),
        file_name="kpi_diagnostics.csv",
        mime="text/csv",
        help=t(lang, "help_btn_diagnostics"),
    )


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    lang = sidebar_lang()

    st.title(t(lang, "page_title"))
    st.markdown(t(lang, "subtitle"))

    st.sidebar.title(t(lang, "data_source"))
    uploaded = st.sidebar.file_uploader(t(lang, "upload_label"), type=["xlsx"])
    if uploaded is None:
        st.sidebar.info(t(lang, "using_sample"))

    try:
        df = load_data(uploaded)
    except FileNotFoundError:
        st.error(t(lang, "err_not_found"))
        st.stop()
    except ValueError as exc:
        st.error(t(lang, "err_invalid", msg=str(exc)))
        st.info(t(lang, "err_columns"))
        st.stop()

    filters = sidebar_filters(df, lang)
    filtered = apply_filters(df, filters)

    if filtered.empty:
        st.warning(t(lang, "warn_no_data"))
        st.stop()

    # Display copy: translated categorical values for charts and tables.
    # All calculations (KPI cards, exports, insights) use the raw filtered df.
    display_filtered = _make_display_df(filtered, lang)

    render_kpi_cards(filtered, lang)
    st.divider()
    render_executive_summary(filtered, lang)
    st.divider()
    render_charts(display_filtered, lang)
    st.divider()
    render_diagnostics(filtered, lang)
    st.divider()
    render_insights(filtered, lang)
    st.divider()
    render_exports(filtered, lang)
    st.divider()
    render_data_table(filtered, lang)


if __name__ == "__main__":
    main()
