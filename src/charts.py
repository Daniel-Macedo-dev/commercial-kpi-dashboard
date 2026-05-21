import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

_PALETTE = px.colors.qualitative.Set2


def monthly_revenue_trend(df: pd.DataFrame) -> go.Figure:
    monthly = df.groupby("Month")["Revenue"].sum().reset_index().sort_values("Month")
    fig = px.line(
        monthly, x="Month", y="Revenue",
        title="Monthly Revenue Trend",
        markers=True,
        color_discrete_sequence=_PALETTE,
    )
    fig.update_layout(xaxis_title="Month", yaxis_title="Revenue (R$)", xaxis_tickangle=-45)
    return fig


def monthly_target_vs_revenue(df: pd.DataFrame) -> go.Figure:
    monthly = (
        df.groupby("Month")[["Revenue", "Target"]].sum()
        .reset_index()
        .sort_values("Month")
    )
    fig = go.Figure()
    fig.add_bar(x=monthly["Month"], y=monthly["Revenue"], name="Revenue", marker_color=_PALETTE[0])
    fig.add_bar(x=monthly["Month"], y=monthly["Target"], name="Target", marker_color=_PALETTE[1])
    fig.update_layout(
        title="Monthly Revenue vs Target",
        barmode="group",
        xaxis_title="Month",
        yaxis_title="Amount (R$)",
        xaxis_tickangle=-45,
    )
    return fig


def revenue_by_region(df: pd.DataFrame) -> go.Figure:
    by_region = (
        df.groupby("Region")["Revenue"].sum()
        .reset_index()
        .sort_values("Revenue", ascending=False)
    )
    fig = px.bar(
        by_region, x="Region", y="Revenue",
        title="Revenue by Region",
        color="Region",
        color_discrete_sequence=_PALETTE,
    )
    fig.update_layout(showlegend=False, yaxis_title="Revenue (R$)")
    return fig


def revenue_by_channel(df: pd.DataFrame) -> go.Figure:
    by_channel = df.groupby("Channel")["Revenue"].sum().reset_index()
    fig = px.pie(
        by_channel, names="Channel", values="Revenue",
        title="Revenue by Channel",
        color_discrete_sequence=_PALETTE,
    )
    return fig


def revenue_by_product_line(df: pd.DataFrame) -> go.Figure:
    by_pl = (
        df.groupby("Product Line")["Revenue"].sum()
        .reset_index()
        .sort_values("Revenue", ascending=True)
    )
    fig = px.bar(
        by_pl, x="Revenue", y="Product Line",
        orientation="h",
        title="Revenue by Product Line",
        color="Product Line",
        color_discrete_sequence=_PALETTE,
    )
    fig.update_layout(showlegend=False, xaxis_title="Revenue (R$)")
    return fig


def top_products(df: pd.DataFrame, n: int = 10) -> go.Figure:
    by_product = (
        df.groupby("Product")["Revenue"].sum()
        .nlargest(n)
        .reset_index()
        .sort_values("Revenue", ascending=True)
    )
    fig = px.bar(
        by_product, x="Revenue", y="Product",
        orientation="h",
        title=f"Top {n} Products by Revenue",
        color_discrete_sequence=_PALETTE,
    )
    fig.update_layout(xaxis_title="Revenue (R$)")
    return fig


def conversion_rate_by_channel(df: pd.DataFrame) -> go.Figure:
    by_channel = (
        df.groupby("Channel")[["Conversions", "Opportunities"]]
        .sum()
        .reset_index()
    )
    safe_opps = by_channel["Opportunities"].replace(0, pd.NA)
    by_channel["Conversion Rate"] = (by_channel["Conversions"] / safe_opps).fillna(0)
    fig = px.bar(
        by_channel.sort_values("Conversion Rate", ascending=False),
        x="Channel", y="Conversion Rate",
        title="Conversion Rate by Channel",
        color="Channel",
        color_discrete_sequence=_PALETTE,
        text_auto=".1%",
    )
    fig.update_layout(showlegend=False, yaxis_tickformat=".0%", yaxis_title="Conversion Rate")
    return fig
