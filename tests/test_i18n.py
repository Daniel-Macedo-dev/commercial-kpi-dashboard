import pytest

from src.i18n import t, SUPPORTED_LANGS


def test_supported_langs_contains_en_and_pt() -> None:
    assert "en" in SUPPORTED_LANGS
    assert "pt" in SUPPORTED_LANGS


def test_english_key_returns_string() -> None:
    result = t("en", "page_title")
    assert isinstance(result, str)
    assert len(result) > 0


def test_portuguese_key_differs_from_english() -> None:
    assert t("pt", "page_title") != t("en", "page_title")


def test_missing_key_falls_back_to_key_name() -> None:
    result = t("en", "nonexistent_key_xyz")
    assert result == "nonexistent_key_xyz"


def test_missing_lang_falls_back_to_english() -> None:
    result = t("fr", "page_title")
    assert result == t("en", "page_title")


def test_kwargs_interpolated_rows_shown() -> None:
    result = t("en", "rows_shown", n=1234)
    assert "1,234" in result


def test_kwargs_interpolated_err_invalid() -> None:
    result = t("en", "err_invalid", msg="bad file")
    assert "bad file" in result


def test_pt_rows_shown_interpolation() -> None:
    result = t("pt", "rows_shown", n=500)
    assert "500" in result


def test_all_en_keys_present_in_pt() -> None:
    from src.i18n import _T
    en_keys = set(_T["en"].keys())
    pt_keys = set(_T["pt"].keys())
    missing = en_keys - pt_keys
    assert not missing, f"PT is missing keys: {missing}"
