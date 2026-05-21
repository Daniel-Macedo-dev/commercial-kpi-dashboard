import pandas as pd
import pytest

from src.display_map import (
    to_display,
    to_raw,
    translate_series,
    translate_options,
    raw_selections,
    col_headers,
)


# ── to_display ────────────────────────────────────────────────────────────────

def test_to_display_pt_region() -> None:
    assert to_display("North", "region", "pt") == "Norte"


def test_to_display_pt_channel() -> None:
    assert to_display("Retail", "channel", "pt") == "Varejo"


def test_to_display_pt_product_line() -> None:
    assert to_display("Medical Devices", "product_line", "pt") == "Dispositivos Médicos"


def test_to_display_en_passthrough() -> None:
    assert to_display("North", "region", "en") == "North"


def test_to_display_unknown_value_fallback() -> None:
    assert to_display("Unknown Region", "region", "pt") == "Unknown Region"


def test_to_display_unknown_category_fallback() -> None:
    assert to_display("North", "country", "pt") == "North"


# ── to_raw ────────────────────────────────────────────────────────────────────

def test_to_raw_pt_region() -> None:
    assert to_raw("Norte", "region", "pt") == "North"


def test_to_raw_pt_channel() -> None:
    assert to_raw("Varejo", "channel", "pt") == "Retail"


def test_to_raw_en_passthrough() -> None:
    assert to_raw("Norte", "region", "en") == "Norte"


def test_to_raw_unknown_display_fallback() -> None:
    assert to_raw("Região Desconhecida", "region", "pt") == "Região Desconhecida"


# ── translate_options / raw_selections round-trip ─────────────────────────────

def test_translate_options_pt() -> None:
    raw = ["North", "South", "Midwest"]
    disp = translate_options(raw, "region", "pt")
    assert disp == ["Norte", "Sul", "Centro-Oeste"]


def test_translate_options_en_unchanged() -> None:
    raw = ["North", "South"]
    assert translate_options(raw, "region", "en") == raw


def test_raw_selections_round_trip() -> None:
    raw = ["North", "Midwest", "Southeast"]
    displayed = translate_options(raw, "region", "pt")
    recovered = raw_selections(displayed, "region", "pt")
    assert recovered == raw


def test_raw_selections_en_passthrough() -> None:
    assert raw_selections(["North"], "region", "en") == ["North"]


# ── translate_series ──────────────────────────────────────────────────────────

def test_translate_series_pt() -> None:
    s = pd.Series(["North", "South", "North", "Midwest"])
    result = translate_series(s, "region", "pt")
    assert list(result) == ["Norte", "Sul", "Norte", "Centro-Oeste"]


def test_translate_series_en_unchanged() -> None:
    s = pd.Series(["North", "South"])
    result = translate_series(s, "region", "en")
    pd.testing.assert_series_equal(result, s)


def test_translate_series_unknown_value_fallback() -> None:
    s = pd.Series(["North", "Unknown"])
    result = translate_series(s, "region", "pt")
    assert result.iloc[1] == "Unknown"


# ── col_headers ───────────────────────────────────────────────────────────────

def test_col_headers_pt_returns_dict() -> None:
    h = col_headers("pt")
    assert isinstance(h, dict)
    assert h["Region"] == "Região"
    assert h["Revenue"] == "Receita"
    assert h["Achievement %"] == "Atingimento %"


def test_col_headers_en_returns_empty() -> None:
    assert col_headers("en") == {}


# ── Full channel map coverage ─────────────────────────────────────────────────

@pytest.mark.parametrize("raw,expected", [
    ("Hospital", "Hospital"),
    ("Distributor", "Distribuidor"),
    ("Retail", "Varejo"),
    ("Online", "Online"),
    ("Clinic", "Clínica"),
])
def test_channel_translations(raw: str, expected: str) -> None:
    assert to_display(raw, "channel", "pt") == expected


@pytest.mark.parametrize("raw,expected", [
    ("North", "Norte"),
    ("Northeast", "Nordeste"),
    ("Midwest", "Centro-Oeste"),
    ("Southeast", "Sudeste"),
    ("South", "Sul"),
])
def test_region_translations(raw: str, expected: str) -> None:
    assert to_display(raw, "region", "pt") == expected


@pytest.mark.parametrize("raw,expected", [
    ("Medical Devices", "Dispositivos Médicos"),
    ("Hospital Solutions", "Soluções Hospitalares"),
    ("Consumer Health Simulation", "Simulação de Saúde do Consumidor"),
    ("Clinical Products", "Produtos Clínicos"),
    ("Patient Care", "Cuidados ao Paciente"),
])
def test_product_line_translations(raw: str, expected: str) -> None:
    assert to_display(raw, "product_line", "pt") == expected
