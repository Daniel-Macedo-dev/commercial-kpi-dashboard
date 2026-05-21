import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

_PALETTE = px.colors.qualitative.Set2
_CURRENCY_AXIS = dict(tickprefix="R$ ", tickformat=",.0f")

# ── Chart label translations ──────────────────────────────────────────────────

_LABELS: dict[str, dict[str, str]] = {
    "en": {
        "revenue": "Revenue",
        "target": "Target",
        "month": "Month",
        "amount_axis": "Amount (R$)",
        "revenue_axis": "Revenue (R$)",
        "conversion_rate": "Conversion Rate",
        "title_monthly_trend": "Monthly Revenue Trend",
        "title_monthly_vs": "Monthly Revenue vs Target",
        "title_by_region": "Revenue by Region",
        "title_by_channel": "Revenue by Channel",
        "title_by_pl": "Revenue by Product Line",
        "title_top_n": "Top {n} Products by Revenue",
        "title_conversion": "Conversion Rate by Channel",
    },
    "pt": {
        "revenue": "Receita",
        "target": "Meta",
        "month": "Mês",
        "amount_axis": "Valor (R$)",
        "revenue_axis": "Receita (R$)",
        "conversion_rate": "Taxa de Conversão",
        "title_monthly_trend": "Tendência Mensal de Receita",
        "title_monthly_vs": "Receita vs Meta Mensal",
        "title_by_region": "Receita por Região",
        "title_by_channel": "Receita por Canal",
        "title_by_pl": "Receita por Linha de Produto",
        "title_top_n": "Top {n} Produtos por Receita",
        "title_conversion": "Taxa de Conversão por Canal",
    },
}


def _lbl(lang: str, key: str, **kw: object) -> str:
    d = _LABELS.get(lang, _LABELS["en"])
    text = d.get(key, _LABELS["en"].get(key, key))
    return text.format(**kw) if kw else text


# ── Chart builders ────────────────────────────────────────────────────────────

def monthly_revenue_trend(df: pd.DataFrame, lang: str = "en") -> go.Figure:
    monthly = df.groupby("Month")["Revenue"].sum().reset_index().sort_values("Month")
    rev = _lbl(lang, "revenue")
    fig = px.line(
        monthly, x="Month", y="Revenue",
        title=_lbl(lang, "title_monthly_trend"),
        markers=True,
        color_discrete_sequence=_PALETTE,
    )
    fig.update_traces(
        hovertemplate=f"<b>%{{x}}</b><br>{rev}: R$ %{{y:,.0f}}<extra></extra>"
    )
    fig.update_layout(
        xaxis_title=_lbl(lang, "month"),
        yaxis_title=_lbl(lang, "revenue_axis"),
        xaxis_tickangle=-45,
        yaxis=_CURRENCY_AXIS,
        hovermode="x unified",
    )
    return fig


def monthly_target_vs_revenue(df: pd.DataFrame, lang: str = "en") -> go.Figure:
    monthly = (
        df.groupby("Month")[["Revenue", "Target"]].sum()
        .reset_index()
        .sort_values("Month")
    )
    rev = _lbl(lang, "revenue")
    tgt = _lbl(lang, "target")
    fig = go.Figure()
    fig.add_bar(
        x=monthly["Month"], y=monthly["Revenue"],
        name=rev,
        marker_color=_PALETTE[0],
        hovertemplate=f"<b>%{{x}}</b><br>{rev}: R$ %{{y:,.0f}}<extra></extra>",
    )
    fig.add_bar(
        x=monthly["Month"], y=monthly["Target"],
        name=tgt,
        marker_color=_PALETTE[1],
        hovertemplate=f"<b>%{{x}}</b><br>{tgt}: R$ %{{y:,.0f}}<extra></extra>",
    )
    fig.update_layout(
        title=_lbl(lang, "title_monthly_vs"),
        barmode="group",
        xaxis_title=_lbl(lang, "month"),
        yaxis_title=_lbl(lang, "amount_axis"),
        xaxis_tickangle=-45,
        yaxis=_CURRENCY_AXIS,
    )
    return fig


def revenue_by_region(df: pd.DataFrame, lang: str = "en") -> go.Figure:
    by_region = (
        df.groupby("Region")["Revenue"].sum()
        .reset_index()
        .sort_values("Revenue", ascending=False)
    )
    rev = _lbl(lang, "revenue")
    fig = px.bar(
        by_region, x="Region", y="Revenue",
        title=_lbl(lang, "title_by_region"),
        color="Region",
        color_discrete_sequence=_PALETTE,
    )
    fig.update_traces(
        hovertemplate=f"<b>%{{x}}</b><br>{rev}: R$ %{{y:,.0f}}<extra></extra>"
    )
    fig.update_layout(
        showlegend=False,
        yaxis_title=_lbl(lang, "revenue_axis"),
        yaxis=_CURRENCY_AXIS,
    )
    return fig


def revenue_by_channel(df: pd.DataFrame, lang: str = "en") -> go.Figure:
    by_channel = df.groupby("Channel")["Revenue"].sum().reset_index()
    rev = _lbl(lang, "revenue")
    fig = px.pie(
        by_channel, names="Channel", values="Revenue",
        title=_lbl(lang, "title_by_channel"),
        color_discrete_sequence=_PALETTE,
    )
    fig.update_traces(
        hovertemplate=f"<b>%{{label}}</b><br>{rev}: R$ %{{value:,.0f}}<br>Share: %{{percent}}<extra></extra>",
        textinfo="label+percent",
    )
    return fig


def revenue_by_product_line(df: pd.DataFrame, lang: str = "en") -> go.Figure:
    by_pl = (
        df.groupby("Product Line")["Revenue"].sum()
        .reset_index()
        .sort_values("Revenue", ascending=True)
    )
    rev = _lbl(lang, "revenue")
    fig = px.bar(
        by_pl, x="Revenue", y="Product Line",
        orientation="h",
        title=_lbl(lang, "title_by_pl"),
        color="Product Line",
        color_discrete_sequence=_PALETTE,
    )
    fig.update_traces(
        hovertemplate=f"<b>%{{y}}</b><br>{rev}: R$ %{{x:,.0f}}<extra></extra>"
    )
    fig.update_layout(
        showlegend=False,
        xaxis_title=_lbl(lang, "revenue_axis"),
        xaxis=_CURRENCY_AXIS,
    )
    return fig


def top_products(df: pd.DataFrame, n: int = 10, lang: str = "en") -> go.Figure:
    by_product = (
        df.groupby("Product")["Revenue"].sum()
        .nlargest(n)
        .reset_index()
        .sort_values("Revenue", ascending=True)
    )
    rev = _lbl(lang, "revenue")
    fig = px.bar(
        by_product, x="Revenue", y="Product",
        orientation="h",
        title=_lbl(lang, "title_top_n", n=n),
        color_discrete_sequence=_PALETTE,
    )
    fig.update_traces(
        hovertemplate=f"<b>%{{y}}</b><br>{rev}: R$ %{{x:,.0f}}<extra></extra>"
    )
    fig.update_layout(
        xaxis_title=_lbl(lang, "revenue_axis"),
        xaxis=_CURRENCY_AXIS,
    )
    return fig


def conversion_rate_by_channel(df: pd.DataFrame, lang: str = "en") -> go.Figure:
    by_channel = (
        df.groupby("Channel")[["Conversions", "Opportunities"]]
        .sum()
        .reset_index()
    )
    safe_opps = by_channel["Opportunities"].replace(0, pd.NA)
    by_channel["Conversion Rate"] = (by_channel["Conversions"] / safe_opps).fillna(0)
    conv = _lbl(lang, "conversion_rate")
    fig = px.bar(
        by_channel.sort_values("Conversion Rate", ascending=False),
        x="Channel", y="Conversion Rate",
        title=_lbl(lang, "title_conversion"),
        color="Channel",
        color_discrete_sequence=_PALETTE,
        text_auto=".1%",
    )
    fig.update_traces(
        hovertemplate=f"<b>%{{x}}</b><br>{conv}: %{{y:.1%}}<extra></extra>"
    )
    fig.update_layout(
        showlegend=False,
        yaxis_tickformat=".0%",
        yaxis_title=conv,
    )
    return fig
