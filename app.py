
import streamlit as st
import pandas as pd
import numpy as np
from kpi import compute_kpis_from_df
from prompt import build_prompt
import datetime
import yfinance as yf

st.set_page_config(page_title="AI Business Analyzer (v2)", layout="wide")
st.title("AI Business Analyzer — v2")
st.write("Analisi automatica di rischio e redditività aziendale con contesto macroeconomico e dati online.")

mode = st.radio("Scegli modalità di input dati", ["📂 Carica file Excel/CSV", "🌐 Società quotata (Yahoo Finance)"])

if mode == "📂 Carica file Excel/CSV":
    uploaded = st.file_uploader("Carica bilancio (Excel o CSV)", type=["xlsx","csv"])
    if uploaded:
        if uploaded.name.endswith(".csv"):
            df = pd.read_csv(uploaded)
        else:
            df = pd.read_excel(uploaded)
        st.success("File caricato con successo.")
    else:
        st.stop()

else:
    ticker_input = st.text_input("Inserisci ticker (es. ENEL.MI, ISP.MI, AAPL, MSFT):")
    if st.button("Recupera dati da mercato"):
        try:
            t = yf.Ticker(ticker_input)
            bs = t.balance_sheet
            is_ = t.financials
            df = is_.T.merge(bs.T, left_index=True, right_index=True, how="outer").reset_index()
            df.rename(columns={"index":"date"}, inplace=True)
            st.success(f"Dati recuperati per {ticker_input}")
        except Exception as e:
            st.error(f"Errore nel recupero dati: {e}")
            st.stop()
    else:
        st.stop()

st.subheader("📊 Dati finanziari")
st.dataframe(df.head())

# Calcolo KPI
st.markdown("---")
st.subheader("📈 Indicatori chiave (KPI)")
kpi_df = compute_kpis_from_df(df)
st.dataframe(kpi_df)

# Macro snapshot (placeholder for now)
macro = {"inflation_yy":2.6,"bce_rate_pct":3.75,"gdp_growth_yy":0.4,"credit_spread_bps":120}
country = st.selectbox("Paese", ["Italy","Germany","France","Spain","UK"])
sector = st.text_input("Settore", "Manufacturing")
as_of = datetime.date.today()

# Prompt for GPT
prompt_text = build_prompt(df, kpi_df, macro, sector, country, str(as_of))
st.markdown("---")
st.subheader("🧠 Prompt AI per analisi testuale")
st.text_area("Prompt GPT (da inviare via API)", prompt_text, height=300)

# Download
st.download_button("Scarica KPI CSV", data=kpi_df.to_csv(index=False).encode("utf-8"), file_name="kpi.csv")
st.download_button("Scarica prompt GPT", data=prompt_text.encode("utf-8"), file_name="prompt.txt")
st.info("Versione 2 — include recupero automatico dei bilanci per società quotate via Yahoo Finance.")
