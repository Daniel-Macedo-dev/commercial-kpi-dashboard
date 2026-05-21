from datetime import date

import pytest

from src.date_utils import make_date, months_for


# ── months_for ────────────────────────────────────────────────────────────────

def test_months_for_en_has_twelve_entries() -> None:
    assert len(months_for("en")) == 12


def test_months_for_pt_has_twelve_entries() -> None:
    assert len(months_for("pt")) == 12


def test_months_for_en_first_is_january() -> None:
    assert months_for("en")[0] == "January"


def test_months_for_en_last_is_december() -> None:
    assert months_for("en")[11] == "December"


def test_months_for_pt_first_is_janeiro() -> None:
    assert months_for("pt")[0] == "Janeiro"


def test_months_for_pt_last_is_dezembro() -> None:
    assert months_for("pt")[11] == "Dezembro"


def test_months_for_unknown_lang_falls_back_to_english() -> None:
    assert months_for("fr") == months_for("en")


def test_months_for_en_and_pt_differ() -> None:
    assert months_for("en") != months_for("pt")


# ── make_date ─────────────────────────────────────────────────────────────────

def test_make_date_valid_day() -> None:
    assert make_date(2025, 6, 15) == date(2025, 6, 15)


def test_make_date_clamps_day_in_april() -> None:
    # April has 30 days; day=31 is clamped to 30
    assert make_date(2025, 4, 31) == date(2025, 4, 30)


def test_make_date_clamps_day_in_february_non_leap() -> None:
    # 2025 is not a leap year; February has 28 days
    assert make_date(2025, 2, 30) == date(2025, 2, 28)


def test_make_date_allows_feb_29_in_leap_year() -> None:
    # 2024 is a leap year
    assert make_date(2024, 2, 29) == date(2024, 2, 29)


def test_make_date_last_day_december() -> None:
    assert make_date(2025, 12, 31) == date(2025, 12, 31)


def test_make_date_day_1_always_valid() -> None:
    for month in range(1, 13):
        assert make_date(2025, month, 1) == date(2025, month, 1)
