from pathlib import Path

import pandas as pd

DEFAULT_DATA_PATH = Path(__file__).parent.parent / "data" / "sample_commercial_data.xlsx"

REQUIRED_COLUMNS = {
    "Date", "Region", "Channel", "Product Line", "Product",
    "Sales Representative", "Revenue", "Target", "Opportunities",
    "Conversions", "Units Sold", "Discount",
}


def load_from_file(file_path: Path) -> pd.DataFrame:
    if not file_path.exists():
        raise FileNotFoundError(
            f"Data file not found: {file_path}\n"
            "Run `python src/sample_data_generator.py` to generate the sample dataset."
        )
    try:
        df = pd.read_excel(file_path, engine="openpyxl")
    except Exception as exc:
        raise ValueError(f"Could not read Excel file '{file_path.name}': {exc}") from exc
    _validate_columns(df, file_path.name)
    return df


def load_from_upload(uploaded_file) -> pd.DataFrame:
    try:
        df = pd.read_excel(uploaded_file, engine="openpyxl")
    except Exception as exc:
        raise ValueError(f"Could not read uploaded file: {exc}") from exc
    _validate_columns(df, getattr(uploaded_file, "name", "uploaded file"))
    return df


def load_default() -> pd.DataFrame:
    return load_from_file(DEFAULT_DATA_PATH)


def _validate_columns(df: pd.DataFrame, source: str) -> None:
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(
            f"File '{source}' is missing required columns: {sorted(missing)}"
        )
