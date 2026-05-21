import pandas as pd
import pytest

from src.kpi_calculator import (
    average_ticket,
    best_region,
    conversion_rate,
    gap_to_target,
    target_achievement,
    total_revenue,
    total_target,
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
