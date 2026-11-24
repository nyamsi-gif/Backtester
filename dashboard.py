import streamlit as st
from data_loader import load_data
from strategies import ma_strat, momentum_strat, mean_r_strat
@st.cache_data
def get_data():
    return load_data()

prix, rendements =get_data()

# ── Barre latérale ──

st.title("📊 Backtester multi-actifs")
actifs=st.sidebar.multiselect("Actif(s)",options=list(prix.columns), default=['SPY'],)

strat_nom=st.sidebar.selectbox("Strategie",options=['MA Crossover', 'Momentum', 'Mean Reversion (RSI)'],)


# ── Fonction qui applique la stratégie choisie à un actif ──

def apply(actif):
    p=prix[actif]
    r=rendements[actif]
    if strat_nom =='MA Crossover':
        return ma_strat(p,r)
    if strat_nom =='Momentum':
        return momentum_strat(p,r)
    if strat_nom =='Mean Reversion (RSI)':
        return mean_r_strat(p,r)

# ── Affichage ──

if not actifs:
    st.warning("Sélectionner au moins un actif")
else:
    st.subheader(f"Performance cumulée — {strat_nom}")

# Construire la performance de chaque actif
perfs = {}
for actif in actifs:
        rdt_strat = apply(actif).dropna()
        perfs[actif] = (1 + rdt_strat).cumprod() * 100

# Transformer en DataFrame pour l'afficher
import pandas as pd
perf_df = pd.DataFrame(perfs)
st.line_chart(perf_df)

    

