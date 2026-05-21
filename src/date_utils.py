"""Pure date helpers for the localized date picker.

All functions are side-effect free and Streamlit-independent so they
can be unit-tested without a running app context.
"""

import calendar
from datetime import date

_MONTHS_EN: list[str] = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]

_MONTHS_PT: list[str] = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
]


def months_for(lang: str) -> list[str]:
    """Return the list of 12 month names for the given language code.

    Falls back to English for any unrecognised language code.
    """
    return _MONTHS_PT if lang == "pt" else _MONTHS_EN


def make_date(year: int, month: int, day: int) -> date:
    """Create a date, clamping day to a valid value for the given month/year.

    Prevents ValueError when a day that was valid for one month is kept
    in session state after the user switches to a shorter month.
    """
    max_day = calendar.monthrange(year, month)[1]
    return date(year, month, min(day, max_day))
