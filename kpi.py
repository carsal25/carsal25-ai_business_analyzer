
import pandas as pd
import numpy as np

def compute_kpis_from_df(df: pd.DataFrame) -> pd.DataFrame:
    cols = [c.lower() for c in df.columns]
    df.columns = cols
    latest = df.iloc[-1]
    def safe(col):
        return latest[col] if col in df.columns and not pd.isna(latest[col]) else np.nan
    revenue = safe('totalrevenue') or safe('revenue')
    ebit = safe('ebit') or safe('operatingincome')
    net_income = safe('netincome')
    assets = safe('totalassets')
    liabilities = safe('totalliab')
    equity = safe('totalstockholderequity') or safe('equity')
    cash = safe('cashandcashequivalents') or safe('cash')
    debt = safe('shorttermdebt') or 0 + safe('longtermdebt') or 0
    kpis = {
        'revenue': revenue,
        'ebit': ebit,
        'net_income': net_income,
        'ebit_margin_pct': (ebit/revenue*100) if revenue else np.nan,
        'net_margin_pct': (net_income/revenue*100) if revenue else np.nan,
        'roa_pct': (net_income/assets*100) if assets else np.nan,
        'roe_pct': (net_income/equity*100) if equity else np.nan,
        'debt_to_equity': (debt/equity) if equity else np.nan,
        'cash_ratio': (cash/debt) if debt else np.nan
    }
    df_out = pd.DataFrame([kpis])
    for c in df_out.columns:
        if pd.api.types.is_numeric_dtype(df_out[c]):
            df_out[c] = df_out[c].round(3)
    return df_out
