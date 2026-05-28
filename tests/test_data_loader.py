import io
from pathlib import Path

import pandas as pd
import pytest

from src.data_loader import REQUIRED_COLUMNS, _validate_columns, load_from_file, load_from_upload


# ── helpers ───────────────────────────────────────────────────────────────────

def _make_valid_df() -> pd.DataFrame:
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


class _FakeUpload(io.BytesIO):
    """Minimal file-like object with a .name attribute, mimicking Streamlit UploadedFile."""
    def __init__(self, data: bytes, name: str = "test.xlsx") -> None:
        super().__init__(data)
        self.name = name


def _to_xlsx_bytes(df: pd.DataFrame) -> bytes:
    buf = io.BytesIO()
    df.to_excel(buf, index=False, engine="openpyxl")
    return buf.getvalue()


# ── _validate_columns ─────────────────────────────────────────────────────────

def test_validate_columns_passes_with_all_required_columns() -> None:
    _validate_columns(_make_valid_df(), "test.xlsx")  # must not raise


def test_validate_columns_raises_on_missing_column() -> None:
    df = pd.DataFrame({"Date": ["2025-01-15"]})
    with pytest.raises(ValueError):
        _validate_columns(df, "test.xlsx")


def test_validate_columns_error_message_includes_column_name() -> None:
    df = pd.DataFrame({"Date": ["2025-01-15"]})
    with pytest.raises(ValueError) as exc_info:
        _validate_columns(df, "test.xlsx")
    assert "Region" in str(exc_info.value)


def test_validate_columns_raises_with_multiple_missing() -> None:
    df = pd.DataFrame({"Date": ["2025-01-15"], "Revenue": [100.0]})
    with pytest.raises(ValueError) as exc_info:
        _validate_columns(df, "test.xlsx")
    assert "missing required columns" in str(exc_info.value)


def test_validate_columns_source_name_in_error_message() -> None:
    df = pd.DataFrame({"Date": ["2025-01-15"]})
    with pytest.raises(ValueError) as exc_info:
        _validate_columns(df, "my_file.xlsx")
    assert "my_file.xlsx" in str(exc_info.value)


# ── REQUIRED_COLUMNS ──────────────────────────────────────────────────────────

def test_required_columns_contains_all_expected() -> None:
    expected = {
        "Date", "Region", "Channel", "Product Line", "Product",
        "Sales Representative", "Revenue", "Target", "Opportunities",
        "Conversions", "Units Sold", "Discount",
    }
    assert REQUIRED_COLUMNS == expected


# ── load_from_upload ──────────────────────────────────────────────────────────

def test_load_from_upload_reads_valid_excel() -> None:
    upload = _FakeUpload(_to_xlsx_bytes(_make_valid_df()))
    result = load_from_upload(upload)
    assert isinstance(result, pd.DataFrame)


def test_load_from_upload_returns_correct_row_count() -> None:
    upload = _FakeUpload(_to_xlsx_bytes(_make_valid_df()))
    result = load_from_upload(upload)
    assert len(result) == 1


def test_load_from_upload_raises_on_missing_required_column() -> None:
    df = pd.DataFrame({"Date": ["2025-01-15"], "Revenue": [100.0]})
    upload = _FakeUpload(_to_xlsx_bytes(df))
    with pytest.raises(ValueError, match="missing required columns"):
        load_from_upload(upload)


def test_load_from_upload_uses_name_attribute_in_error() -> None:
    df = pd.DataFrame({"Date": ["2025-01-15"]})
    upload = _FakeUpload(_to_xlsx_bytes(df), name="my_upload.xlsx")
    with pytest.raises(ValueError) as exc_info:
        load_from_upload(upload)
    assert "my_upload.xlsx" in str(exc_info.value)


# ── load_from_file ────────────────────────────────────────────────────────────

def test_load_from_file_reads_valid_excel(tmp_path: Path) -> None:
    file_path = tmp_path / "test.xlsx"
    _make_valid_df().to_excel(file_path, index=False, engine="openpyxl")
    result = load_from_file(file_path)
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 1


def test_load_from_file_raises_file_not_found(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_from_file(tmp_path / "nonexistent.xlsx")


def test_load_from_file_raises_on_missing_required_column(tmp_path: Path) -> None:
    df = pd.DataFrame({"Date": ["2025-01-15"], "Revenue": [100.0]})
    file_path = tmp_path / "bad.xlsx"
    df.to_excel(file_path, index=False, engine="openpyxl")
    with pytest.raises(ValueError, match="missing required columns"):
        load_from_file(file_path)
