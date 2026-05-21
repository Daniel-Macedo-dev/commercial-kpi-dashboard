import pandas as pd

from src.kpi_calculator import compute_all
from src.display_map import to_display


# ── Insights ──────────────────────────────────────────────────────────────────

def generate(df: pd.DataFrame, lang: str = "en") -> list[str]:
    if df.empty:
        return (
            ["Nenhum dado disponível para os filtros selecionados."]
            if lang == "pt"
            else ["No data available for the selected filters."]
        )

    kpis = compute_all(df)
    insights: list[str] = []

    achievement = kpis["target_achievement"]
    gap = kpis["gap_to_target"]

    if lang == "pt":
        best_region = to_display(kpis["best_region"], "region", lang)
        best_pl = to_display(kpis["best_product_line"], "product_line", lang)
        best_channel = to_display(kpis["best_channel"], "channel", lang)

        if achievement >= 1.0:
            insights.append(
                f"Atingimento de meta em {achievement:.1%} — a equipe está acima da meta. "
                "Mantenha o ritmo atual e identifique fatores de sucesso replicáveis."
            )
        elif achievement >= 0.9:
            insights.append(
                f"Atingimento de meta em {achievement:.1%} — próximo da meta, mas ainda não atingido. "
                f"Um gap de R\\$ {abs(gap):,.0f} ainda precisa ser fechado. Foque em oportunidades de alto potencial."
            )
        else:
            insights.append(
                f"Atingimento de meta em {achievement:.1%} — significativamente abaixo da meta. "
                f"O gap de receita é R\\$ {abs(gap):,.0f}. Investigue canais e regiões com baixo desempenho."
            )

        insights.append(
            f"A região com melhor desempenho é '{best_region}', liderando em receita total. "
            "Considere replicar suas práticas comerciais nas regiões de menor desempenho."
        )
        insights.append(
            f"'{best_pl}' é a linha de produto mais forte em receita. "
            "Garanta estoque adequado e foco dos representantes nessa linha."
        )

        conv_rate = kpis["conversion_rate"]
        if conv_rate < 0.30:
            insights.append(
                f"Taxa de conversão geral de {conv_rate:.1%} — abaixo do benchmark de 30%. "
                "Revise o funil de vendas quanto à qualificação e acompanhamento de leads."
            )
        elif conv_rate < 0.50:
            insights.append(
                f"Taxa de conversão geral de {conv_rate:.1%} — desempenho moderado. "
                "Há espaço para melhorar a qualidade dos leads e as táticas de conversão."
            )
        else:
            insights.append(
                f"Taxa de conversão geral de {conv_rate:.1%} — desempenho forte. "
                "A equipe está convertendo uma alta proporção de oportunidades identificadas."
            )

        insights.append(
            f"'{best_channel}' é o canal de maior receita. "
            "Avalie se outros canais podem se beneficiar de estratégias comerciais similares."
        )

        avg_discount = kpis["average_discount"]
        if avg_discount > 0.15:
            insights.append(
                f"Desconto médio de {avg_discount:.1%} — acima do limite de cautela de 15%. "
                "Descontos elevados podem comprimir a margem. Revise as políticas de aprovação."
            )
        elif avg_discount > 0.10:
            insights.append(
                f"Desconto médio de {avg_discount:.1%} — dentro do intervalo aceitável, mas vale monitorar. "
                "Certifique-se de que os descontos são usados de forma estratégica, não reativa."
            )
    else:
        best_region = kpis["best_region"]
        best_pl = kpis["best_product_line"]
        best_channel = kpis["best_channel"]

        if achievement >= 1.0:
            insights.append(
                f"Target achievement is {achievement:.1%} — the team is performing above target. "
                "Sustain the current momentum and identify replicable success factors."
            )
        elif achievement >= 0.9:
            insights.append(
                f"Target achievement is {achievement:.1%} — close to target but not yet there. "
                f"A gap of R\\$ {abs(gap):,.0f} remains. Focus on closing high-potential opportunities."
            )
        else:
            insights.append(
                f"Target achievement is {achievement:.1%} — significantly below target. "
                f"Revenue gap is R\\$ {abs(gap):,.0f}. Investigate underperforming channels and regions."
            )

        insights.append(
            f"The top-performing region is '{best_region}', leading in total revenue. "
            "Consider replicating its commercial practices in lower-performing regions."
        )
        insights.append(
            f"'{best_pl}' is the strongest product line by revenue. "
            "Ensure adequate inventory and sales rep focus for this line."
        )

        conv_rate = kpis["conversion_rate"]
        if conv_rate < 0.30:
            insights.append(
                f"Overall conversion rate is {conv_rate:.1%} — below the 30% benchmark. "
                "Review the sales funnel for qualification and follow-up effectiveness."
            )
        elif conv_rate < 0.50:
            insights.append(
                f"Overall conversion rate is {conv_rate:.1%} — moderate performance. "
                "There is room to improve lead quality and conversion tactics."
            )
        else:
            insights.append(
                f"Overall conversion rate is {conv_rate:.1%} — strong performance. "
                "The team is converting a high share of identified opportunities."
            )

        insights.append(
            f"'{best_channel}' is the highest-revenue channel. "
            "Evaluate whether other channels can benefit from similar commercial strategies."
        )

        avg_discount = kpis["average_discount"]
        if avg_discount > 0.15:
            insights.append(
                f"Average discount is {avg_discount:.1%} — above the 15% caution threshold. "
                "High discounting can erode margin. Review discount approval policies."
            )
        elif avg_discount > 0.10:
            insights.append(
                f"Average discount is {avg_discount:.1%} — within acceptable range but worth monitoring. "
                "Ensure discounts are being used strategically rather than reactively."
            )

    return insights


# ── Dimension diagnostics ─────────────────────────────────────────────────────

def _aggregate_dimension(df: pd.DataFrame, dim: str) -> pd.DataFrame:
    grouped = (
        df.groupby(dim)
        .agg(Revenue=("Revenue", "sum"), Target=("Target", "sum"))
        .reset_index()
    )
    safe_target = grouped["Target"].replace(0, pd.NA)
    grouped["Achievement %"] = (grouped["Revenue"] / safe_target).fillna(0)
    grouped["Gap to Target"] = grouped["Revenue"] - grouped["Target"]
    return grouped.sort_values("Revenue", ascending=False).reset_index(drop=True)


def build_dimension_diagnostics(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """
    Return a dict mapping each dimension name to an aggregated diagnostic DataFrame.

    Columns per DataFrame: <dim>, Revenue, Target, Achievement %, Gap to Target.
    Achievement % is stored as a decimal (0.975 = 97.5%); callers format as needed.
    """
    if df.empty:
        return {}
    return {
        "Region": _aggregate_dimension(df, "Region"),
        "Channel": _aggregate_dimension(df, "Channel"),
        "Product Line": _aggregate_dimension(df, "Product Line"),
    }


# ── Executive summary ─────────────────────────────────────────────────────────

def generate_executive_summary(df: pd.DataFrame, lang: str = "en") -> list[dict]:
    """
    Return a list of executive summary findings.

    Each dict has:
      label  – short title string
      text   – business-friendly narrative sentence
      status – 'good' | 'warning' | 'bad' | 'neutral'
    """
    if df.empty:
        return []

    kpis = compute_all(df)
    items: list[dict] = []

    achievement = kpis["target_achievement"]
    gap = kpis["gap_to_target"]
    revenue = kpis["total_revenue"]
    target = kpis["total_target"]

    if lang == "pt":
        best_region_disp = to_display(kpis["best_region"], "region", lang)
        best_pl_disp = to_display(kpis["best_product_line"], "product_line", lang)
        best_channel_disp = to_display(kpis["best_channel"], "channel", lang)

        # 1. Revenue performance
        if achievement >= 1.0:
            rev_text = (
                f"Receita total de R\\$ {revenue:,.0f} atingiu {achievement:.1%} da "
                f"meta de R\\$ {target:,.0f} — a equipe está acima do objetivo."
            )
            rev_status = "good"
        elif achievement >= 0.9:
            rev_text = (
                f"Receita total de R\\$ {revenue:,.0f} está em {achievement:.1%} da "
                f"meta de R\\$ {target:,.0f}. Um gap de R\\$ {abs(gap):,.0f} ainda precisa ser fechado."
            )
            rev_status = "warning"
        else:
            rev_text = (
                f"Receita total de R\\$ {revenue:,.0f} representa {achievement:.1%} da "
                f"meta de R\\$ {target:,.0f} — significativamente abaixo do objetivo, "
                f"com um deficit de R\\$ {abs(gap):,.0f}."
            )
            rev_status = "bad"
        items.append({"label": "Performance de Receita", "text": rev_text, "status": rev_status})

        # 2. Main positive drivers
        items.append({
            "label": "Principais Drivers Positivos",
            "text": (
                f"A região '{best_region_disp}' e a linha de produto '{best_pl_disp}' "
                f"lideraram a geração de receita. O canal '{best_channel_disp}' foi o "
                "canal de vendas com melhor desempenho no período selecionado."
            ),
            "status": "neutral",
        })

        # 3. Underperforming dimension
        region_diag = _aggregate_dimension(df, "Region")
        if len(region_diag) > 1:
            worst = region_diag.loc[region_diag["Achievement %"].idxmin()]
            worst_pct = worst["Achievement %"]
            worst_gap = worst["Gap to Target"]
            worst_region_disp = to_display(worst["Region"], "region", lang)
            items.append({
                "label": "Dimensão com Baixo Desempenho",
                "text": (
                    f"A região '{worst_region_disp}' tem o menor atingimento, em {worst_pct:.1%}, "
                    f"com um gap de R\\$ {abs(worst_gap):,.0f} em relação à meta. "
                    "Priorizar essa área para intervenção comercial pode acelerar a recuperação."
                ),
                "status": "warning" if worst_pct >= 0.85 else "bad",
            })

        # 4. Conversion performance
        conv_rate = kpis["conversion_rate"]
        total_conv = kpis["total_conversions"]
        total_opp = kpis["total_opportunities"]
        if conv_rate >= 0.5:
            conv_text = (
                f"Taxa de conversão de {conv_rate:.1%} ({total_conv:,} de {total_opp:,} oportunidades) "
                "reflete forte desempenho do funil de vendas."
            )
            conv_status = "good"
        elif conv_rate >= 0.3:
            conv_text = (
                f"Taxa de conversão de {conv_rate:.1%} ({total_conv:,} de {total_opp:,} oportunidades) "
                "é moderada. Melhorar a qualificação de leads e o acompanhamento pode elevar essa métrica."
            )
            conv_status = "warning"
        else:
            conv_text = (
                f"Taxa de conversão de {conv_rate:.1%} ({total_conv:,} de {total_opp:,} oportunidades) "
                "está abaixo do benchmark. Uma revisão da qualidade do pipeline e do processo de vendas é recomendada."
            )
            conv_status = "bad"
        items.append({"label": "Performance de Conversão", "text": conv_text, "status": conv_status})

        # 5. Discount behaviour
        avg_discount = kpis["average_discount"]
        if avg_discount > 0.15:
            disc_text = (
                f"Desconto médio de {avg_discount:.1%} ultrapassa o limite de cautela de 15%. "
                "Descontos elevados podem comprimir a margem — revisar as políticas de aprovação é recomendado."
            )
            disc_status = "bad"
        elif avg_discount > 0.10:
            disc_text = (
                f"Desconto médio de {avg_discount:.1%} está dentro do intervalo aceitável, mas vale monitorar. "
                "Certifique-se de que os descontos refletem intenção estratégica, não pressão de preço reativa."
            )
            disc_status = "warning"
        else:
            disc_text = (
                f"Desconto médio de {avg_discount:.1%} está em nível saudável. "
                "A equipe está mantendo boa disciplina de precificação."
            )
            disc_status = "good"
        items.append({"label": "Comportamento de Desconto", "text": disc_text, "status": disc_status})

    else:
        # 1. Revenue performance
        if achievement >= 1.0:
            rev_text = (
                f"Total revenue of R\\$ {revenue:,.0f} reached {achievement:.1%} of the "
                f"R\\$ {target:,.0f} target — the team is performing above goal."
            )
            rev_status = "good"
        elif achievement >= 0.9:
            rev_text = (
                f"Total revenue of R\\$ {revenue:,.0f} is at {achievement:.1%} of the "
                f"R\\$ {target:,.0f} target. A gap of R\\$ {abs(gap):,.0f} remains to close."
            )
            rev_status = "warning"
        else:
            rev_text = (
                f"Total revenue of R\\$ {revenue:,.0f} stands at {achievement:.1%} of the "
                f"R\\$ {target:,.0f} target — significantly below goal with a R\\$ {abs(gap):,.0f} shortfall."
            )
            rev_status = "bad"
        items.append({"label": "Revenue Performance", "text": rev_text, "status": rev_status})

        # 2. Main positive drivers
        items.append({
            "label": "Main Positive Drivers",
            "text": (
                f"The '{kpis['best_region']}' region and '{kpis['best_product_line']}' product line "
                f"led revenue generation. The '{kpis['best_channel']}' channel was the "
                "strongest-performing sales channel in the selected period."
            ),
            "status": "neutral",
        })

        # 3. Underperforming dimension (only meaningful with more than one region)
        region_diag = _aggregate_dimension(df, "Region")
        if len(region_diag) > 1:
            worst = region_diag.loc[region_diag["Achievement %"].idxmin()]
            worst_pct = worst["Achievement %"]
            worst_gap = worst["Gap to Target"]
            items.append({
                "label": "Underperforming Dimension",
                "text": (
                    f"The '{worst['Region']}' region has the lowest achievement at {worst_pct:.1%}, "
                    f"with a gap of R\\$ {abs(worst_gap):,.0f} vs its target. "
                    "Prioritising this area for commercial intervention may accelerate recovery."
                ),
                "status": "warning" if worst_pct >= 0.85 else "bad",
            })


        # 4. Conversion performance
        conv_rate = kpis["conversion_rate"]
        total_conv = kpis["total_conversions"]
        total_opp = kpis["total_opportunities"]
        if conv_rate >= 0.5:
            conv_text = (
                f"Conversion rate of {conv_rate:.1%} ({total_conv:,} of {total_opp:,} opportunities) "
                "reflects strong funnel performance."
            )
            conv_status = "good"
        elif conv_rate >= 0.3:
            conv_text = (
                f"Conversion rate of {conv_rate:.1%} ({total_conv:,} of {total_opp:,} opportunities) "
                "is moderate. Improving lead qualification and follow-up could lift this metric."
            )
            conv_status = "warning"
        else:
            conv_text = (
                f"Conversion rate of {conv_rate:.1%} ({total_conv:,} of {total_opp:,} opportunities) "
                "is below benchmark. A review of pipeline quality and the sales process is recommended."
            )
            conv_status = "bad"
        items.append({"label": "Conversion Performance", "text": conv_text, "status": conv_status})

        # 5. Discount behaviour
        avg_discount = kpis["average_discount"]
        if avg_discount > 0.15:
            disc_text = (
                f"Average discount of {avg_discount:.1%} exceeds the 15% caution threshold. "
                "High discounting can compress margin — reviewing approval policies is advisable."
            )
            disc_status = "bad"
        elif avg_discount > 0.10:
            disc_text = (
                f"Average discount of {avg_discount:.1%} is within acceptable range but worth monitoring. "
                "Ensure discounts reflect strategic intent rather than reactive price pressure."
            )
            disc_status = "warning"
        else:
            disc_text = (
                f"Average discount of {avg_discount:.1%} is at a healthy level. "
                "The team is maintaining good pricing discipline."
            )
            disc_status = "good"
        items.append({"label": "Discount Behaviour", "text": disc_text, "status": disc_status})

    return items
