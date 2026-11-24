import streamlit as st
import pandas_datareader as pdr
import yfinance as yf
import pandas as pd

st.title("🌅 Market Monitor")

fin = pd.Timestamp.today().normalize()
debut = fin - pd.DateOffset(years=5)

# ── Récupération des données ──
@st.cache_data
def taux_fred(series):
    data = pdr.get_data_fred(list(series.keys()), start=debut, end=fin)
    return data.rename(columns=series).ffill()

@st.cache_data
def niveaux_yf(tickers):
    data = yf.download(list(tickers.keys()), start=debut, end=fin,
                       auto_adjust=True, progress=False)['Close']
    return data.rename(columns=tickers).ffill()

def tableau_variation(data, unite='%'):
    dernier, veille = data.iloc[-1], data.iloc[-2]
    var = (dernier - veille) * 100 if unite == 'bps' else (dernier / veille - 1) * 100
    return pd.DataFrame({'Niveau': dernier.round(2), f'Var 1j ({unite})': var.round(2)})

# ── Choix de la période (filtre le début) ──
PERIODES = {'1 mois': 21, '3 mois': 63, '6 mois': 126, '1 an': 252, '5 ans': 9999}

def render_tab(data, unite, perf=True):
    # Menu de sélection des actifs
    choix = st.multiselect("Actifs", list(data.columns),
                           default=list(data.columns)[:2], key=unite+str(perf))
    # Menu de période
    periode = st.selectbox("Période", list(PERIODES.keys()), index=3, key='p'+unite+str(perf))
    n = PERIODES[periode]

    # Tableau des niveaux / variations
    st.dataframe(tableau_variation(data, unite))

    if not choix:
        st.warning("Sélectionne au moins un actif.")
        return

    # Filtrer sur la période choisie
    sous_data = data[choix].tail(n)

    st.subheader("Évolution")
    if perf:
        # Prix → performance base 100
        st.line_chart(sous_data / sous_data.iloc[0] * 100)
    else:
        # Taux → on affiche le niveau brut (pas de base 100)
        st.line_chart(sous_data)

# ── Univers ──
TAUX_US = {'DGS3MO':'US 3M','DGS2':'US 2Y','DGS5':'US 5Y','DGS10':'US 10Y',
           'DGS30':'US 30Y','SOFR':'SOFR','EFFR':'Fed Funds'}
FX = {'EURUSD=X':'EUR/USD','GBPUSD=X':'GBP/USD','USDJPY=X':'USD/JPY','DX-Y.NYB':'Dollar Index'}
ACTIONS = {'^GSPC':'S&P 500','^STOXX50E':'Eurostoxx 50','^FCHI':'CAC 40','^N225':'Nikkei'}
CREDIT = {'LQD':'IG US','HYG':'HY US','IGLN.L':'IG EU','IHYG.L':'HY EU'}

# ── Onglets ──
t1, t2, t3, t4 = st.tabs(["Taux US", "FX", "Actions", "Crédit"])
with t1: render_tab(taux_fred(TAUX_US), 'bps', perf=False)   # taux = niveau brut
with t2: render_tab(niveaux_yf(FX), '%', perf=True)
with t3: render_tab(niveaux_yf(ACTIONS), '%', perf=True)
with t4: render_tab(niveaux_yf(CREDIT), '%', perf=True)