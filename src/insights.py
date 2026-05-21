import pandas as pd

from src.kpi_calculator import compute_all


# ── Existing insights ─────────────────────────────────────────────────────────

def generate(df: pd.DataFrame) -> list[str]:
    if df.empty:
        return ["No data available for the selected filters."]

    kpis = compute_all(df)
    insights: list[str] = []

    achievement = kpis["target_achievement"]
    gap = kpis["gap_to_target"]
    if achievement >= 1.0:
        insights.append(
            f"Target achievement is {achievement:.1%} — the team is performing above target. "
            "Sustain the current momentum and identify replicable success factors."
        )
    elif achievement >= 0.9:
        insights.append(
            f"Target achievement is {achievement:.1%} — close to target but not yet there. "
            f"A gap of R$ {abs(gap):,.0f} remains. Focus on closing high-potential opportunities."
        )
    else:
        insights.append(
            f"Target achievement is {achievement:.1%} — significantly below target. "
            f"Revenue gap is R$ {abs(gap):,.0f}. Investigate underperforming channels and regions."
        )

    insights.append(
        f"The top-performing region is '{kpis['best_region']}', leading in total revenue. "
        "Consider replicating its commercial practices in lower-performing regions."
    )
    insights.append(
        f"'{kpis['best_product_line']}' is the strongest product line by revenue. "
        "Ensure adequate inventory and sales rep focus for this line."
    )

    conv_rate = kpis["conversion_rate"]
    if conv_rate < 0.30:
        insights.append(
            f"Overall conversion rate is {conv_rate:.1%} — below the 30% benchmark. "
            "Review the sales funnel for qualification and follow-up effectiveness."
        )
    elif conv_rate < 0.50:
        insights.append(
            f"Overall conversion rate is {conv_rate:.1%} — moderate performance. "
            "There is room to improve lead quality and conversion tactics."
        )
    else:
        insights.append(
            f"Overall conversion rate is {conv_rate:.1%} — strong performance. "
            "The team is converting a high share of identified opportunities."
        )

    insights.append(
        f"'{kpis['best_channel']}' is the highest-revenue channel. "
        "Evaluate whether other channels can benefit from similar commercial strategies."
    )

    avg_discount = kpis["average_discount"]
    if avg_discount > 0.15:
        insights.append(
            f"Average discount is {avg_discount:.1%} — above the 15% caution threshold. "
            "High discounting can erode margin. Review discount approval policies."
        )
    elif avg_discount > 0.10:
        insights.append(
            f"Average discount is {avg_discount:.1%} — within acceptable range but worth monitoring. "
            "Ensure discounts are being used strategically rather than reactively."
        )

    return insights


# ── Dimension diagnostics ─────────────────────────────────────────────────────

def _aggregate_dimension(df: pd.DataFrame, dim: str) -> pd.DataFrame:
    """Aggregate Revenue and Target by a single dimension; compute achievement and gap."""
    grouped = (
        df.groupby(dim)
        .agg(Revenue=("Revenue", "sum"), Target=("Target", "sum"))
        .reset_index()
    )
    safe_target = grouped["Target"].replace(0, pd.NA)
    grouped["Achievement %"] = (grouped["Revenue"] / safe_target).fillna(0)
    grouped["Gap to Target"] = grouped["Revenue"] - grouped["Target"]
    return grouped.sort_values("Revenue", ascending=False).reset_index(drop=True)


def build_dimension_diagnostics(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """
    Return a dict mapping each dimension name to an aggregated diagnostic DataFrame.

    Columns per DataFrame: <dim>, Revenue, Target, Achievement %, Gap to Target.
    Achievement % is stored as a decimal (0.975 = 97.5%); callers format as needed.
    """
    if df.empty:
        return {}
    return {
        "Region": _aggregate_dimension(df, "Region"),
        "Channel": _aggregate_dimension(df, "Channel"),
        "Product Line": _aggregate_dimension(df, "Product Line"),
    }


# ── Executive summary ─────────────────────────────────────────────────────────

def generate_executive_summary(df: pd.DataFrame) -> list[dict]:
    """
    Return a list of executive summary findings.

    Each dict has:
      label  – short title string
      text   – business-friendly narrative sentence
      status – 'good' | 'warning' | 'bad' | 'neutral'
    """
    if df.empty:
        return []

    kpis = compute_all(df)
    items: list[dict] = []

    # 1. Revenue performance
    achievement = kpis["target_achievement"]
    gap = kpis["gap_to_target"]
    revenue = kpis["total_revenue"]
    target = kpis["total_target"]

    if achievement >= 1.0:
        rev_text = (
            f"Total revenue of R$ {revenue:,.0f} reached {achievement:.1%} of the "
            f"R$ {target:,.0f} target — the team is performing above goal."
        )
        rev_status = "good"
    elif achievement >= 0.9:
        rev_text = (
            f"Total revenue of R$ {revenue:,.0f} is at {achievement:.1%} of the "
            f"R$ {target:,.0f} target. A gap of R$ {abs(gap):,.0f} remains to close."
        )
        rev_status = "warning"
    else:
        rev_text = (
            f"Total revenue of R$ {revenue:,.0f} stands at {achievement:.1%} of the "
            f"R$ {target:,.0f} target — significantly below goal with a R$ {abs(gap):,.0f} shortfall."
        )
        rev_status = "bad"
    items.append({"label": "Revenue Performance", "text": rev_text, "status": rev_status})

    # 2. Main positive drivers
    items.append({
        "label": "Main Positive Drivers",
        "text": (
            f"The '{kpis['best_region']}' region and '{kpis['best_product_line']}' product line "
            f"led revenue generation. The '{kpis['best_channel']}' channel was the "
            "strongest-performing sales channel in the selected period."
        ),
        "status": "neutral",
    })

    # 3. Underperforming dimension (only meaningful with more than one region)
    region_diag = _aggregate_dimension(df, "Region")
    if len(region_diag) > 1:
        worst = region_diag.loc[region_diag["Achievement %"].idxmin()]
        worst_pct = worst["Achievement %"]
        worst_gap = worst["Gap to Target"]
        items.append({
            "label": "Underperforming Dimension",
            "text": (
                f"The '{worst['Region']}' region has the lowest achievement at {worst_pct:.1%}, "
                f"with a gap of R$ {abs(worst_gap):,.0f} vs its target. "
                "Prioritising this area for commercial intervention may accelerate recovery."
            ),
            "status": "warning" if worst_pct >= 0.85 else "bad",
        })

    # 4. Conversion performance
    conv_rate = kpis["conversion_rate"]
    total_conv = kpis["total_conversions"]
    total_opp = kpis["total_opportunities"]
    if conv_rate >= 0.5:
        conv_text = (
            f"Conversion rate of {conv_rate:.1%} ({total_conv:,} of {total_opp:,} opportunities) "
            "reflects strong funnel performance."
        )
        conv_status = "good"
    elif conv_rate >= 0.3:
        conv_text = (
            f"Conversion rate of {conv_rate:.1%} ({total_conv:,} of {total_opp:,} opportunities) "
            "is moderate. Improving lead qualification and follow-up could lift this metric."
        )
        conv_status = "warning"
    else:
        conv_text = (
            f"Conversion rate of {conv_rate:.1%} ({total_conv:,} of {total_opp:,} opportunities) "
            "is below benchmark. A review of pipeline quality and the sales process is recommended."
        )
        conv_status = "bad"
    items.append({"label": "Conversion Performance", "text": conv_text, "status": conv_status})

    # 5. Discount behaviour
    avg_discount = kpis["average_discount"]
    if avg_discount > 0.15:
        disc_text = (
            f"Average discount of {avg_discount:.1%} exceeds the 15% caution threshold. "
            "High discounting can compress margin — reviewing approval policies is advisable."
        )
        disc_status = "bad"
    elif avg_discount > 0.10:
        disc_text = (
            f"Average discount of {avg_discount:.1%} is within acceptable range but worth monitoring. "
            "Ensure discounts reflect strategic intent rather than reactive price pressure."
        )
        disc_status = "warning"
    else:
        disc_text = (
            f"Average discount of {avg_discount:.1%} is at a healthy level. "
            "The team is maintaining good pricing discipline."
        )
        disc_status = "good"
    items.append({"label": "Discount Behaviour", "text": disc_text, "status": disc_status})

    return items
