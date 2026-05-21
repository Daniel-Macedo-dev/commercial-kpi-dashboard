import pandas as pd


def total_revenue(df: pd.DataFrame) -> float:
    return float(df["Revenue"].sum())


def total_target(df: pd.DataFrame) -> float:
    return float(df["Target"].sum())


def target_achievement(df: pd.DataFrame) -> float:
    t = total_target(df)
    return float(total_revenue(df) / t) if t != 0 else 0.0


def gap_to_target(df: pd.DataFrame) -> float:
    return float(total_revenue(df) - total_target(df))


def total_opportunities(df: pd.DataFrame) -> int:
    return int(df["Opportunities"].sum())


def total_conversions(df: pd.DataFrame) -> int:
    return int(df["Conversions"].sum())


def conversion_rate(df: pd.DataFrame) -> float:
    opps = total_opportunities(df)
    return float(total_conversions(df) / opps) if opps != 0 else 0.0


def total_units_sold(df: pd.DataFrame) -> int:
    return int(df["Units Sold"].sum())


def average_ticket(df: pd.DataFrame) -> float:
    units = total_units_sold(df)
    return float(total_revenue(df) / units) if units != 0 else 0.0


def average_discount(df: pd.DataFrame) -> float:
    return float(df["Discount"].mean()) if not df.empty else 0.0


def best_by_revenue(df: pd.DataFrame, column: str) -> str:
    if df.empty or column not in df.columns:
        return "N/A"
    return str(df.groupby(column)["Revenue"].sum().idxmax())


def best_region(df: pd.DataFrame) -> str:
    return best_by_revenue(df, "Region")


def best_product_line(df: pd.DataFrame) -> str:
    return best_by_revenue(df, "Product Line")


def best_channel(df: pd.DataFrame) -> str:
    return best_by_revenue(df, "Channel")


def compute_all(df: pd.DataFrame) -> dict:
    return {
        "total_revenue": total_revenue(df),
        "total_target": total_target(df),
        "target_achievement": target_achievement(df),
        "gap_to_target": gap_to_target(df),
        "total_opportunities": total_opportunities(df),
        "total_conversions": total_conversions(df),
        "conversion_rate": conversion_rate(df),
        "total_units_sold": total_units_sold(df),
        "average_ticket": average_ticket(df),
        "average_discount": average_discount(df),
        "best_region": best_region(df),
        "best_product_line": best_product_line(df),
        "best_channel": best_channel(df),
    }
