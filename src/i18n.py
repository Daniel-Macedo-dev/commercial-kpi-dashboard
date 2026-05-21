"""UI translations for English (en) and Portuguese (pt)."""

_T: dict[str, dict[str, str]] = {
    "en": {
        # ── Page ──────────────────────────────────────────────────────────────
        "page_title": "Commercial KPI Dashboard",
        "subtitle": (
            "An interactive portfolio dashboard for commercial analytics. "
            "**All data is entirely fictional** and for demonstration purposes only."
        ),
        # ── Sidebar ───────────────────────────────────────────────────────────
        "language_label": "Language / Idioma",
        "data_source": "Data Source",
        "upload_label": "Upload Excel file (.xlsx)",
        "using_sample": (
            "Using the built-in **fictional sample dataset**.  \n"
            "Upload your own `.xlsx` file above to analyze your own data."
        ),
        # ── Filters ───────────────────────────────────────────────────────────
        "filters": "Filters",
        "date_range": "Date range",
        "region": "Region",
        "channel": "Channel",
        "product_line": "Product Line",
        "product": "Product",
        "select_all": "Select all",
        "choose_options": "Choose options",
        # ── KPI card labels ───────────────────────────────────────────────────
        "total_revenue": "Total Revenue",
        "total_target": "Total Target",
        "target_achievement": "Target Achievement",
        "gap_to_target": "Gap to Target",
        "conversion_rate": "Conversion Rate",
        "avg_ticket": "Avg Ticket",
        "avg_discount": "Avg Discount",
        "units_sold": "Units Sold",
        # ── KPI card help texts ───────────────────────────────────────────────
        "help_revenue": "Sum of all revenue in the selected period and filters.",
        "help_target": "Sum of all targets in the selected period and filters.",
        "help_achievement": "Total Revenue ÷ Total Target. Green = above 100%, red = below.",
        "help_gap": "Revenue minus Target. Positive = above target, negative = below.",
        "help_conversion": "Total Conversions ÷ Total Opportunities.",
        "help_ticket": "Total Revenue ÷ Total Units Sold.",
        "help_discount": "Mean discount rate across all records in the current selection.",
        "help_units": "Total units sold across all products.",
        "vs_goal": "vs goal",
        # ── Section headings ──────────────────────────────────────────────────
        "executive_summary": "Executive Summary",
        "revenue_trends": "Revenue Trends",
        "revenue_breakdown": "Revenue Breakdown",
        "sales_efficiency": "Sales Efficiency",
        "diagnostics": "Performance Diagnostics by Dimension",
        "diagnostics_caption": (
            "Revenue, Target, Achievement %, and Gap to Target broken down by "
            "Region, Channel, and Product Line for the current filter selection."
        ),
        "insights": "Automatic Insights",
        "export": "Export",
        "filtered_data": "Filtered Data",
        # ── Diagnostics tab labels ────────────────────────────────────────────
        "tab_region": "By Region",
        "tab_channel": "By Channel",
        "tab_product_line": "By Product Line",
        # ── Export buttons ────────────────────────────────────────────────────
        "btn_filtered": "Filtered Dataset (CSV)",
        "btn_kpi": "KPI Summary (CSV)",
        "btn_diagnostics": "Diagnostics by Dimension (CSV)",
        "help_btn_filtered": "All records matching the current filters.",
        "help_btn_kpi": "KPI totals for the current filter selection.",
        "help_btn_diagnostics": "Performance breakdown by Region, Channel, and Product Line.",
        # ── Messages ──────────────────────────────────────────────────────────
        "err_not_found": (
            "Sample dataset not found. "
            "Run `python src/sample_data_generator.py` to generate it, then restart the app."
        ),
        "err_invalid": "Could not load data: {msg}",
        "err_columns": (
            "Make sure your Excel file contains these required columns: "
            "**Date, Region, Channel, Product Line, Product, Sales Representative, "
            "Revenue, Target, Opportunities, Conversions, Units Sold, Discount.**"
        ),
        "warn_no_data": (
            "No data matches the selected filters. "
            "Try expanding the date range or clearing one or more filter selections."
        ),
        "rows_shown": "{n:,} rows shown",
        "no_summary": "No data available for summary.",
    },

    "pt": {
        # ── Page ──────────────────────────────────────────────────────────────
        "page_title": "Dashboard de KPIs Comerciais",
        "subtitle": (
            "Dashboard interativo de análise comercial para portfólio. "
            "**Todos os dados são fictícios** e apenas para fins de demonstração."
        ),
        # ── Sidebar ───────────────────────────────────────────────────────────
        "language_label": "Language / Idioma",
        "data_source": "Fonte de Dados",
        "upload_label": "Carregar arquivo Excel (.xlsx)",
        "using_sample": (
            "Usando o **conjunto de dados fictício** padrão.  \n"
            "Carregue seu próprio arquivo `.xlsx` acima para analisar seus dados."
        ),
        # ── Filters ───────────────────────────────────────────────────────────
        "filters": "Filtros",
        "date_range": "Período",
        "region": "Região",
        "channel": "Canal",
        "product_line": "Linha de Produto",
        "product": "Produto",
        "select_all": "Selecionar todos",
        "choose_options": "Escolha as opções",
        # ── KPI card labels ───────────────────────────────────────────────────
        "total_revenue": "Receita Total",
        "total_target": "Meta Total",
        "target_achievement": "Atingimento de Meta",
        "gap_to_target": "Gap para Meta",
        "conversion_rate": "Taxa de Conversão",
        "avg_ticket": "Ticket Médio",
        "avg_discount": "Desconto Médio",
        "units_sold": "Unidades Vendidas",
        # ── KPI card help texts ───────────────────────────────────────────────
        "help_revenue": "Soma de toda a receita no período e filtros selecionados.",
        "help_target": "Soma de todas as metas no período e filtros selecionados.",
        "help_achievement": "Receita Total ÷ Meta Total. Verde = acima de 100%, vermelho = abaixo.",
        "help_gap": "Receita menos Meta. Positivo = acima da meta, negativo = abaixo.",
        "help_conversion": "Total de Conversões ÷ Total de Oportunidades.",
        "help_ticket": "Receita Total ÷ Total de Unidades Vendidas.",
        "help_discount": "Taxa média de desconto em todos os registros da seleção atual.",
        "help_units": "Total de unidades vendidas em todos os produtos.",
        "vs_goal": "vs meta",
        # ── Section headings ──────────────────────────────────────────────────
        "executive_summary": "Sumário Executivo",
        "revenue_trends": "Tendência de Receita",
        "revenue_breakdown": "Detalhamento de Receita",
        "sales_efficiency": "Eficiência Comercial",
        "diagnostics": "Diagnóstico de Performance por Dimensão",
        "diagnostics_caption": (
            "Receita, Meta, Atingimento % e Gap por Região, Canal e "
            "Linha de Produto para a seleção de filtros atual."
        ),
        "insights": "Insights Automáticos",
        "export": "Exportar",
        "filtered_data": "Dados Filtrados",
        # ── Diagnostics tab labels ────────────────────────────────────────────
        "tab_region": "Por Região",
        "tab_channel": "Por Canal",
        "tab_product_line": "Por Linha de Produto",
        # ── Export buttons ────────────────────────────────────────────────────
        "btn_filtered": "Dados Filtrados (CSV)",
        "btn_kpi": "Resumo de KPIs (CSV)",
        "btn_diagnostics": "Diagnóstico por Dimensão (CSV)",
        "help_btn_filtered": "Todos os registros correspondentes aos filtros atuais.",
        "help_btn_kpi": "Totais de KPIs para a seleção de filtros atual.",
        "help_btn_diagnostics": "Detalhamento de performance por Região, Canal e Linha de Produto.",
        # ── Messages ──────────────────────────────────────────────────────────
        "err_not_found": (
            "Arquivo de dados não encontrado. "
            "Execute `python src/sample_data_generator.py` para gerá-lo e reinicie o app."
        ),
        "err_invalid": "Não foi possível carregar os dados: {msg}",
        "err_columns": (
            "Certifique-se de que seu arquivo Excel contenha estas colunas obrigatórias: "
            "**Date, Region, Channel, Product Line, Product, Sales Representative, "
            "Revenue, Target, Opportunities, Conversions, Units Sold, Discount.**"
        ),
        "warn_no_data": (
            "Nenhum dado corresponde aos filtros selecionados. "
            "Tente ampliar o intervalo de datas ou limpar uma ou mais seleções."
        ),
        "rows_shown": "{n:,} linhas exibidas",
        "no_summary": "Nenhum dado disponível para o resumo.",
    },
}

SUPPORTED_LANGS = list(_T.keys())


def t(lang: str, key: str, **kwargs: object) -> str:
    """Return the translated string for *lang* and *key*.

    Falls back to English when the key or language is missing.
    Named *kwargs* are interpolated into the string with str.format().
    """
    text: str = _T.get(lang, _T["en"]).get(key) or _T["en"].get(key, key)
    return text.format(**kwargs) if kwargs else text
