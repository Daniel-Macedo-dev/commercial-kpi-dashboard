import pandas as pd

from src.kpi_calculator import compute_all


def generate(df: pd.DataFrame) -> list[str]:
    if df.empty:
        return ["No data available for the selected filters."]

    kpis = compute_all(df)
    insights: list[str] = []

    # Target achievement
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

    # Best region
    insights.append(
        f"The top-performing region is '{kpis['best_region']}', leading in total revenue. "
        "Consider replicating its commercial practices in lower-performing regions."
    )

    # Best product line
    insights.append(
        f"'{kpis['best_product_line']}' is the strongest product line by revenue. "
        "Ensure adequate inventory and sales rep focus for this line."
    )

    # Conversion rate
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

    # Best channel
    insights.append(
        f"'{kpis['best_channel']}' is the highest-revenue channel. "
        "Evaluate whether other channels can benefit from similar commercial strategies."
    )

    # Discount warning
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
