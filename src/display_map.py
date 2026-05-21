"""Display-name mappings: English dataset values ↔ Portuguese UI labels.

Raw dataset values are never mutated. This module translates categorical
values for display only and reverse-maps user selections back to raw values
for filtering and calculations.

Product names are intentionally kept in English across all UI languages
because they are fictional brand identifiers, not descriptive category labels.
"""

import pandas as pd

# ── Raw → Portuguese value maps ───────────────────────────────────────────────

_REGIONS: dict[str, str] = {
    "North": "Norte",
    "Northeast": "Nordeste",
    "Midwest": "Centro-Oeste",
    "Southeast": "Sudeste",
    "South": "Sul",
}

_CHANNELS: dict[str, str] = {
    "Hospital": "Hospital",
    "Distributor": "Distribuidor",
    "Retail": "Varejo",
    "Online": "Online",
    "Clinic": "Clínica",
}

_PRODUCT_LINES: dict[str, str] = {
    "Medical Devices": "Dispositivos Médicos",
    "Hospital Solutions": "Soluções Hospitalares",
    "Consumer Health Simulation": "Simulação de Saúde do Consumidor",
    "Clinical Products": "Produtos Clínicos",
    "Patient Care": "Cuidados ao Paciente",
}

_MAPS: dict[str, dict[str, str]] = {
    "region": _REGIONS,
    "channel": _CHANNELS,
    "product_line": _PRODUCT_LINES,
}

# ── Column headers for display copies ────────────────────────────────────────

_COL_HEADERS_PT: dict[str, str] = {
    "Date": "Data",
    "Region": "Região",
    "Channel": "Canal",
    "Product Line": "Linha de Produto",
    "Product": "Produto",
    "Sales Representative": "Representante",
    "Revenue": "Receita",
    "Target": "Meta",
    "Target Achievement": "Atingimento",
    "Gap to Target": "Gap para Meta",
    "Opportunities": "Oportunidades",
    "Conversions": "Conversões",
    "Conversion Rate": "Taxa de Conversão",
    "Units Sold": "Unidades Vendidas",
    "Average Ticket": "Ticket Médio",
    "Discount": "Desconto",
    "Achievement %": "Atingimento %",
}


# ── Public helpers ────────────────────────────────────────────────────────────

def to_display(raw: str, category: str, lang: str) -> str:
    """Translate a single raw dataset value to its UI display label."""
    if lang != "pt":
        return raw
    return _MAPS.get(category, {}).get(raw, raw)


def to_raw(display: str, category: str, lang: str) -> str:
    """Reverse-map a display label back to its raw dataset value."""
    if lang != "pt":
        return display
    reverse = {v: k for k, v in _MAPS.get(category, {}).items()}
    return reverse.get(display, display)


def translate_series(series: pd.Series, category: str, lang: str) -> pd.Series:
    """Return a new Series with translated display values (original unchanged)."""
    if lang != "pt":
        return series
    mapping = _MAPS.get(category, {})
    return series.map(lambda x: mapping.get(x, x))


def translate_options(options: list[str], category: str, lang: str) -> list[str]:
    """Translate a list of raw option values for display in a sidebar widget."""
    if lang != "pt":
        return options
    mapping = _MAPS.get(category, {})
    return [mapping.get(v, v) for v in options]


def raw_selections(display_selections: list[str], category: str, lang: str) -> list[str]:
    """Map a list of user-selected display values back to raw dataset values."""
    if lang != "pt":
        return display_selections
    reverse = {v: k for k, v in _MAPS.get(category, {}).items()}
    return [reverse.get(s, s) for s in display_selections]


def col_headers(lang: str) -> dict[str, str]:
    """Return old→new column name mapping for display copies in the given lang."""
    if lang != "pt":
        return {}
    return _COL_HEADERS_PT.copy()
