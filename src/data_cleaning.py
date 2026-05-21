import pandas as pd

NUMERIC_COLUMNS = ["Revenue", "Target", "Opportunities", "Conversions", "Units Sold", "Discount"]
REQUIRED_COLUMNS = [
    "Date", "Region", "Channel", "Product Line", "Product",
    "Sales Representative", *NUMERIC_COLUMNS,
]


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    _check_required_columns(df)

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    null_dates = df["Date"].isna().sum()
    if null_dates:
        print(f"Warning: {null_dates} rows with unparseable dates dropped.")
    df = df.dropna(subset=["Date"])

    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df = _add_derived_columns(df)
    return df


def _check_required_columns(df: pd.DataFrame) -> None:
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"DataFrame is missing required columns: {missing}")


def _add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    df["Quarter"] = df["Date"].dt.to_period("Q").astype(str)
    df["Year"] = df["Date"].dt.year

    safe_target = df["Target"].replace(0, pd.NA)
    df["Target Achievement"] = (df["Revenue"] / safe_target).fillna(0)

    df["Gap to Target"] = df["Revenue"] - df["Target"]

    safe_opps = df["Opportunities"].replace(0, pd.NA)
    df["Conversion Rate"] = (df["Conversions"] / safe_opps).fillna(0)

    safe_units = df["Units Sold"].replace(0, pd.NA)
    df["Average Ticket"] = (df["Revenue"] / safe_units).fillna(0)

    return df
