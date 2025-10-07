
import pandas as pd
def build_prompt(fin_df, kpi_df, macro, sector, country, analysis_date):
    kpis = kpi_df.to_dict(orient='records')[0]
    kpi_lines = "\n".join([f"- {k}: {v}" for k,v in kpis.items()])
    macro_lines = "\n".join([f"- {k}: {v}" for k,v in macro.items()])
    prompt = f"""Sei un analista finanziario esperto.
Valuta la redditività, la solidità e il rischio dell'azienda sulla base dei dati seguenti.
Fornisci un breve report (max 400 parole) in italiano.

Data analisi: {analysis_date}
Paese: {country}
Settore: {sector}

Indicatori finanziari:
{kpi_lines}

Contesto macroeconomico:
{macro_lines}

Struttura del report:
1. Sintesi iniziale (20-30 parole)
2. Valutazione combinata di rischio e redditività (basso/medio/alto)
3. Commento qualitativo (max 3 paragrafi)
4. Raccomandazioni (3 bullet point)
"""
    return prompt
