import pandas as pd
import pytest

from src.insights import build_dimension_diagnostics, generate_executive_summary


@pytest.fixture
def sample_df() -> pd.DataFrame:
    return pd.DataFrame({
        "Revenue": [100_000.0, 200_000.0, 50_000.0, 80_000.0],
        "Target": [90_000.0, 180_000.0, 100_000.0, 70_000.0],
        "Region": ["North", "South", "North", "East"],
        "Channel": ["Hospital", "Retail", "Online", "Hospital"],
        "Product Line": ["Medical Devices", "Patient Care", "Clinical Products", "Medical Devices"],
        "Opportunities": [20, 30, 10, 15],
        "Conversions": [10, 20, 3, 12],
        "Units Sold": [50, 100, 20, 40],
        "Discount": [0.10, 0.20, 0.05, 0.08],
    })


# ── build_dimension_diagnostics ───────────────────────────────────────────────

def test_diagnostics_returns_three_keys(sample_df: pd.DataFrame) -> None:
    result = build_dimension_diagnostics(sample_df)
    assert set(result.keys()) == {"Region", "Channel", "Product Line"}


def test_diagnostics_required_columns(sample_df: pd.DataFrame) -> None:
    result = build_dimension_diagnostics(sample_df)
    for df in result.values():
        assert "Revenue" in df.columns
        assert "Target" in df.columns
        assert "Achievement %" in df.columns
        assert "Gap to Target" in df.columns


def test_diagnostics_empty_df() -> None:
    assert build_dimension_diagnostics(pd.DataFrame()) == {}


def test_diagnostics_region_revenue_aggregation(sample_df: pd.DataFrame) -> None:
    result = build_dimension_diagnostics(sample_df)
    region_df = result["Region"]
    north_revenue = region_df.loc[region_df["Region"] == "North", "Revenue"].values[0]
    # North: 100_000 + 50_000 = 150_000
    assert north_revenue == pytest.approx(150_000.0)


def test_diagnostics_achievement_above_target(sample_df: pd.DataFrame) -> None:
    result = build_dimension_diagnostics(sample_df)
    region_df = result["Region"]
    # South: 200_000 / 180_000 ≈ 1.111
    south_ach = region_df.loc[region_df["Region"] == "South", "Achievement %"].values[0]
    assert south_ach == pytest.approx(200_000 / 180_000)


def test_diagnostics_gap_to_target(sample_df: pd.DataFrame) -> None:
    result = build_dimension_diagnostics(sample_df)
    region_df = result["Region"]
    # North: (100_000 + 50_000) - (90_000 + 100_000) = 150_000 - 190_000 = -40_000
    north_gap = region_df.loc[region_df["Region"] == "North", "Gap to Target"].values[0]
    assert north_gap == pytest.approx(-40_000.0)


def test_diagnostics_sorted_by_revenue_descending(sample_df: pd.DataFrame) -> None:
    result = build_dimension_diagnostics(sample_df)
    revenues = result["Region"]["Revenue"].tolist()
    assert revenues == sorted(revenues, reverse=True)


def test_diagnostics_zero_target_does_not_crash() -> None:
    df = pd.DataFrame({
        "Revenue": [1000.0],
        "Target": [0.0],
        "Region": ["North"],
        "Channel": ["Hospital"],
        "Product Line": ["Medical Devices"],
    })
    result = build_dimension_diagnostics(df)
    assert result["Region"]["Achievement %"].values[0] == 0.0


# ── generate_executive_summary ────────────────────────────────────────────────

def test_executive_summary_returns_list(sample_df: pd.DataFrame) -> None:
    result = generate_executive_summary(sample_df)
    assert isinstance(result, list)
    assert len(result) >= 4


def test_executive_summary_empty_df() -> None:
    assert generate_executive_summary(pd.DataFrame()) == []


def test_executive_summary_item_structure(sample_df: pd.DataFrame) -> None:
    result = generate_executive_summary(sample_df)
    for item in result:
        assert "label" in item
        assert "text" in item
        assert "status" in item
        assert item["status"] in ("good", "warning", "bad", "neutral")


def test_executive_summary_revenue_label_present(sample_df: pd.DataFrame) -> None:
    result = generate_executive_summary(sample_df)
    labels = [item["label"] for item in result]
    assert "Revenue Performance" in labels


def test_executive_summary_above_target_status() -> None:
    df = pd.DataFrame({
        "Revenue": [200_000.0],
        "Target": [100_000.0],
        "Region": ["North"],
        "Channel": ["Hospital"],
        "Product Line": ["Medical Devices"],
        "Opportunities": [10],
        "Conversions": [6],
        "Units Sold": [50],
        "Discount": [0.05],
    })
    result = generate_executive_summary(df)
    rev_item = next(i for i in result if i["label"] == "Revenue Performance")
    assert rev_item["status"] == "good"


def test_executive_summary_below_target_status() -> None:
    df = pd.DataFrame({
        "Revenue": [70_000.0],
        "Target": [100_000.0],
        "Region": ["North"],
        "Channel": ["Hospital"],
        "Product Line": ["Medical Devices"],
        "Opportunities": [10],
        "Conversions": [2],
        "Units Sold": [30],
        "Discount": [0.20],
    })
    result = generate_executive_summary(df)
    rev_item = next(i for i in result if i["label"] == "Revenue Performance")
    assert rev_item["status"] == "bad"


def test_executive_summary_single_region_skips_underperformer() -> None:
    df = pd.DataFrame({
        "Revenue": [100_000.0],
        "Target": [90_000.0],
        "Region": ["North"],
        "Channel": ["Hospital"],
        "Product Line": ["Medical Devices"],
        "Opportunities": [10],
        "Conversions": [5],
        "Units Sold": [20],
        "Discount": [0.05],
    })
    result = generate_executive_summary(df)
    labels = [item["label"] for item in result]
    assert "Underperforming Dimension" not in labels
