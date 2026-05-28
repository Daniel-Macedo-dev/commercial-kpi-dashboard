import pandas as pd
import pytest

from src.data_cleaning import clean


# ── fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def valid_df() -> pd.DataFrame:
    return pd.DataFrame({
        "Date": ["2025-01-15"],
        "Region": ["North"],
        "Channel": ["Hospital"],
        "Product Line": ["Medical Devices"],
        "Product": ["SurgiPro X1"],
        "Sales Representative": ["Alice Santos"],
        "Revenue": [50_000.0],
        "Target": [45_000.0],
        "Opportunities": [20],
        "Conversions": [10],
        "Units Sold": [50],
        "Discount": [0.10],
    })


@pytest.fixture
def cleaned_df(valid_df: pd.DataFrame) -> pd.DataFrame:
    return clean(valid_df)


# ── basic smoke ───────────────────────────────────────────────────────────────

def test_clean_returns_dataframe(valid_df: pd.DataFrame) -> None:
    assert isinstance(clean(valid_df), pd.DataFrame)


def test_clean_does_not_mutate_input(valid_df: pd.DataFrame) -> None:
    original_dtype = valid_df["Date"].dtype
    clean(valid_df)
    assert valid_df["Date"].dtype == original_dtype


# ── date coercion ─────────────────────────────────────────────────────────────

def test_clean_date_coerced_to_datetime(cleaned_df: pd.DataFrame) -> None:
    assert pd.api.types.is_datetime64_any_dtype(cleaned_df["Date"])


def test_clean_drops_invalid_date_rows() -> None:
    df = pd.DataFrame({
        "Date": ["2025-01-15", "not-a-date"],
        "Region": ["North", "South"],
        "Channel": ["Hospital", "Retail"],
        "Product Line": ["Medical Devices", "Medical Devices"],
        "Product": ["SurgiPro X1", "SurgiPro X1"],
        "Sales Representative": ["Alice Santos", "Alice Santos"],
        "Revenue": [50_000.0, 30_000.0],
        "Target": [45_000.0, 28_000.0],
        "Opportunities": [20, 15],
        "Conversions": [10, 8],
        "Units Sold": [50, 30],
        "Discount": [0.10, 0.05],
    })
    result = clean(df)
    assert len(result) == 1


def test_clean_valid_date_retained_after_drop() -> None:
    df = pd.DataFrame({
        "Date": ["2025-03-10", "bad-date"],
        "Region": ["North", "South"],
        "Channel": ["Hospital", "Retail"],
        "Product Line": ["Medical Devices", "Medical Devices"],
        "Product": ["SurgiPro X1", "SurgiPro X1"],
        "Sales Representative": ["Alice Santos", "Alice Santos"],
        "Revenue": [50_000.0, 30_000.0],
        "Target": [45_000.0, 28_000.0],
        "Opportunities": [20, 15],
        "Conversions": [10, 8],
        "Units Sold": [50, 30],
        "Discount": [0.10, 0.05],
    })
    result = clean(df)
    assert result["Date"].iloc[0] == pd.Timestamp("2025-03-10")


# ── numeric coercion ──────────────────────────────────────────────────────────

def test_clean_revenue_is_numeric(cleaned_df: pd.DataFrame) -> None:
    assert pd.api.types.is_numeric_dtype(cleaned_df["Revenue"])


def test_clean_invalid_numeric_filled_with_zero(valid_df: pd.DataFrame) -> None:
    df = valid_df.copy()
    df["Revenue"] = ["not_a_number"]
    result = clean(df)
    assert result["Revenue"].iloc[0] == pytest.approx(0.0)


# ── derived columns: existence ────────────────────────────────────────────────

def test_clean_adds_month_column(cleaned_df: pd.DataFrame) -> None:
    assert "Month" in cleaned_df.columns


def test_clean_adds_quarter_column(cleaned_df: pd.DataFrame) -> None:
    assert "Quarter" in cleaned_df.columns


def test_clean_adds_year_column(cleaned_df: pd.DataFrame) -> None:
    assert "Year" in cleaned_df.columns


def test_clean_adds_target_achievement_column(cleaned_df: pd.DataFrame) -> None:
    assert "Target Achievement" in cleaned_df.columns


def test_clean_adds_gap_to_target_column(cleaned_df: pd.DataFrame) -> None:
    assert "Gap to Target" in cleaned_df.columns


def test_clean_adds_conversion_rate_column(cleaned_df: pd.DataFrame) -> None:
    assert "Conversion Rate" in cleaned_df.columns


def test_clean_adds_average_ticket_column(cleaned_df: pd.DataFrame) -> None:
    assert "Average Ticket" in cleaned_df.columns


# ── derived columns: values ───────────────────────────────────────────────────

def test_clean_month_value_correct(cleaned_df: pd.DataFrame) -> None:
    # Date 2025-01-15 → "2025-01"
    assert cleaned_df["Month"].iloc[0] == "2025-01"


def test_clean_quarter_value_correct(cleaned_df: pd.DataFrame) -> None:
    # Date 2025-01-15 → "2025Q1"
    assert cleaned_df["Quarter"].iloc[0] == "2025Q1"


def test_clean_year_value_correct(cleaned_df: pd.DataFrame) -> None:
    assert cleaned_df["Year"].iloc[0] == 2025


def test_clean_target_achievement_correct(cleaned_df: pd.DataFrame) -> None:
    # 50_000 / 45_000
    assert cleaned_df["Target Achievement"].iloc[0] == pytest.approx(50_000 / 45_000)


def test_clean_gap_to_target_correct(cleaned_df: pd.DataFrame) -> None:
    # 50_000 - 45_000 = 5_000
    assert cleaned_df["Gap to Target"].iloc[0] == pytest.approx(5_000.0)


def test_clean_conversion_rate_correct(cleaned_df: pd.DataFrame) -> None:
    # 10 / 20 = 0.5
    assert cleaned_df["Conversion Rate"].iloc[0] == pytest.approx(0.5)


def test_clean_average_ticket_correct(cleaned_df: pd.DataFrame) -> None:
    # 50_000 / 50 = 1_000
    assert cleaned_df["Average Ticket"].iloc[0] == pytest.approx(1_000.0)


# ── derived columns: zero-denominator guards ──────────────────────────────────

def test_clean_target_achievement_zero_target(valid_df: pd.DataFrame) -> None:
    df = valid_df.copy()
    df["Target"] = [0.0]
    result = clean(df)
    assert result["Target Achievement"].iloc[0] == pytest.approx(0.0)


def test_clean_conversion_rate_zero_opportunities(valid_df: pd.DataFrame) -> None:
    df = valid_df.copy()
    df["Opportunities"] = [0]
    result = clean(df)
    assert result["Conversion Rate"].iloc[0] == pytest.approx(0.0)


def test_clean_average_ticket_zero_units(valid_df: pd.DataFrame) -> None:
    df = valid_df.copy()
    df["Units Sold"] = [0]
    result = clean(df)
    assert result["Average Ticket"].iloc[0] == pytest.approx(0.0)


# ── missing columns ───────────────────────────────────────────────────────────

def test_clean_missing_column_raises_value_error() -> None:
    df = pd.DataFrame({"Date": ["2025-01-15"], "Revenue": [100.0]})
    with pytest.raises(ValueError, match="missing required columns"):
        clean(df)
