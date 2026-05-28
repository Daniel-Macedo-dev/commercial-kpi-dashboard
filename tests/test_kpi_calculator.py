import pandas as pd
import pytest

from src.kpi_calculator import (
    average_discount,
    average_ticket,
    best_channel,
    best_product_line,
    best_region,
    compute_all,
    conversion_rate,
    gap_to_target,
    target_achievement,
    total_conversions,
    total_opportunities,
    total_revenue,
    total_target,
    total_units_sold,
)


@pytest.fixture
def sample_df() -> pd.DataFrame:
    return pd.DataFrame({
        "Revenue": [100_000.0, 200_000.0, 150_000.0],
        "Target": [120_000.0, 180_000.0, 160_000.0],
        "Opportunities": [20, 30, 25],
        "Conversions": [10, 15, 20],
        "Units Sold": [50, 100, 75],
        "Region": ["North", "South", "North"],
    })


def test_total_revenue(sample_df: pd.DataFrame) -> None:
    assert total_revenue(sample_df) == 450_000.0


def test_total_target(sample_df: pd.DataFrame) -> None:
    assert total_target(sample_df) == 460_000.0


def test_target_achievement(sample_df: pd.DataFrame) -> None:
    assert target_achievement(sample_df) == pytest.approx(450_000 / 460_000)


def test_gap_to_target(sample_df: pd.DataFrame) -> None:
    assert gap_to_target(sample_df) == pytest.approx(-10_000.0)


def test_conversion_rate(sample_df: pd.DataFrame) -> None:
    # 45 conversions / 75 opportunities
    assert conversion_rate(sample_df) == pytest.approx(45 / 75)


def test_average_ticket(sample_df: pd.DataFrame) -> None:
    # 450_000 revenue / 225 units
    assert average_ticket(sample_df) == pytest.approx(450_000 / 225)


def test_best_region(sample_df: pd.DataFrame) -> None:
    # North: 100_000 + 150_000 = 250_000 > South: 200_000
    assert best_region(sample_df) == "North"


def test_target_achievement_zero_target() -> None:
    df = pd.DataFrame({"Revenue": [100.0], "Target": [0.0]})
    assert target_achievement(df) == 0.0


def test_conversion_rate_zero_opportunities() -> None:
    df = pd.DataFrame({"Opportunities": [0], "Conversions": [0], "Revenue": [0.0]})
    assert conversion_rate(df) == 0.0


def test_average_ticket_zero_units() -> None:
    df = pd.DataFrame({"Revenue": [1000.0], "Units Sold": [0]})
    assert average_ticket(df) == 0.0


# ── total_opportunities ───────────────────────────────────────────────────────

def test_total_opportunities(sample_df: pd.DataFrame) -> None:
    # 20 + 30 + 25
    assert total_opportunities(sample_df) == 75


# ── total_conversions ─────────────────────────────────────────────────────────

def test_total_conversions(sample_df: pd.DataFrame) -> None:
    # 10 + 15 + 20
    assert total_conversions(sample_df) == 45


# ── total_units_sold ──────────────────────────────────────────────────────────

def test_total_units_sold(sample_df: pd.DataFrame) -> None:
    # 50 + 100 + 75
    assert total_units_sold(sample_df) == 225


# ── average_discount ──────────────────────────────────────────────────────────

def test_average_discount() -> None:
    df = pd.DataFrame({"Discount": [0.05, 0.15, 0.25]})
    assert average_discount(df) == pytest.approx(0.15)


def test_average_discount_empty_df() -> None:
    assert average_discount(pd.DataFrame()) == 0.0


# ── best_product_line ─────────────────────────────────────────────────────────

def test_best_product_line() -> None:
    df = pd.DataFrame({
        "Product Line": ["Medical Devices", "Patient Care", "Medical Devices"],
        "Revenue": [80_000.0, 200_000.0, 50_000.0],
    })
    # Patient Care: 200_000; Medical Devices: 130_000
    assert best_product_line(df) == "Patient Care"


# ── best_channel ──────────────────────────────────────────────────────────────

def test_best_channel() -> None:
    df = pd.DataFrame({
        "Channel": ["Hospital", "Retail", "Hospital"],
        "Revenue": [100_000.0, 150_000.0, 80_000.0],
    })
    # Hospital: 180_000; Retail: 150_000
    assert best_channel(df) == "Hospital"


# ── compute_all ───────────────────────────────────────────────────────────────

_COMPUTE_ALL_DF = pd.DataFrame({
    "Revenue": [100_000.0],
    "Target": [90_000.0],
    "Opportunities": [20],
    "Conversions": [10],
    "Units Sold": [50],
    "Discount": [0.10],
    "Region": ["North"],
    "Product Line": ["Medical Devices"],
    "Channel": ["Hospital"],
})

_EXPECTED_KEYS = {
    "total_revenue", "total_target", "target_achievement", "gap_to_target",
    "total_opportunities", "total_conversions", "conversion_rate",
    "total_units_sold", "average_ticket", "average_discount",
    "best_region", "best_product_line", "best_channel",
}


def test_compute_all_returns_expected_keys() -> None:
    assert set(compute_all(_COMPUTE_ALL_DF).keys()) == _EXPECTED_KEYS


def test_compute_all_values_correct() -> None:
    result = compute_all(_COMPUTE_ALL_DF)
    assert result["total_revenue"] == pytest.approx(100_000.0)
    assert result["total_target"] == pytest.approx(90_000.0)
    assert result["target_achievement"] == pytest.approx(100_000 / 90_000)
    assert result["gap_to_target"] == pytest.approx(10_000.0)
    assert result["total_opportunities"] == 20
    assert result["total_conversions"] == 10
    assert result["conversion_rate"] == pytest.approx(0.5)
    assert result["total_units_sold"] == 50
    assert result["average_ticket"] == pytest.approx(2_000.0)
    assert result["average_discount"] == pytest.approx(0.10)
    assert result["best_region"] == "North"
    assert result["best_product_line"] == "Medical Devices"
    assert result["best_channel"] == "Hospital"
