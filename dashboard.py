import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from data_loader import load_data
from strategies import ma_strat, momentum_strat, mean_r_strat

@st.cache_data
def get_data():
    return load_data()

prix, rendements = get_data()

st.title("📊 Backtester multi-actifs")

# ── Barre latérale ──
actifs = st.sidebar.multiselect("Actif(s)", options=list(prix.columns), default=['SPY'])
strat_nom = st.sidebar.selectbox("Stratégie",
    options=['MA Crossover', 'Momentum', 'Mean Reversion (RSI)'])

# ── Applique la stratégie choisie à un actif ──
def apply(actif):
    p = prix[actif]
    r = rendements[actif]
    if strat_nom == 'MA Crossover':
        return ma_strat(p, r)
    if strat_nom == 'Momentum':
        return momentum_strat(p, r)
    if strat_nom == 'Mean Reversion (RSI)':
        return mean_r_strat(p, r)

# ── Calcule les métriques de risque d'une série de rendements ──
def metriques_risque(rdt, rf=0.04):
    ann_ret = rdt.mean() * 252
    ann_vol = rdt.std() * np.sqrt(252)
    downside = rdt[rdt < 0].std() * np.sqrt(252)
    cumul = (1 + rdt).cumprod()
    dd = (cumul - cumul.cummax()) / cumul.cummax()
    max_dd = dd.min()
    return {
        'Rdt ann. (%)' : round(ann_ret * 100, 1),
        'Vol ann. (%)' : round(ann_vol * 100, 1),
        'Sharpe'       : round((ann_ret - rf) / ann_vol, 2),
        'Sortino'      : round((ann_ret - rf) / downside, 2),
        'Max DD (%)'   : round(max_dd * 100, 1),
        'Calmar'       : round(ann_ret / abs(max_dd), 2),
        'VaR 95% (%)'  : round(np.percentile(rdt, 5) * 100, 2),
        'Win rate (%)' : round((rdt > 0).mean() * 100, 1),
    }

# ── Affichage ──
if not actifs:
    st.warning("Sélectionner au moins un actif")
else:
    rdts    = {actif: apply(actif).dropna()      for actif in actifs}
    rdts_bh = {actif: rendements[actif].dropna() for actif in actifs}

    tab_perf, tab_risque = st.tabs(["Performance", "Risque"])

    with tab_perf:
        st.subheader(f"Performance cumulée — {strat_nom} vs Buy & Hold")
        fig, ax = plt.subplots(figsize=(11, 5))
        for actif in actifs:
            perf_strat = (1 + rdts[actif]).cumprod() * 100
            perf_bh    = (1 + rdts_bh[actif]).cumprod() * 100
            ligne = ax.plot(perf_strat.index,
    

