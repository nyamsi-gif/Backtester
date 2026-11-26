# ── Affichage ──
if not actifs:
    st.warning("Sélectionner au moins un actif")
else:
    # Rendements stratégie ET buy & hold pour chaque actif
    rdts    = {actif: apply(actif).dropna()      for actif in actifs}   # stratégie
    rdts_bh = {actif: rendements[actif].dropna() for actif in actifs}   # buy & hold

    tab_perf, tab_risque = st.tabs(["Performance", "Risque"])

    # ===== ONGLET PERFORMANCE =====
    with tab_perf:
        st.subheader(f"Performance cumulée — {strat_nom} vs Buy & Hold")
        fig, ax = plt.subplots(figsize=(11, 5))
        for actif in actifs:
            perf_strat = (1 + rdts[actif]).cumprod() * 100
            perf_bh    = (1 + rdts_bh[actif]).cumprod() * 100
            ligne = ax.plot(perf_strat.index, perf_strat, label=f"{actif} — {strat_nom}")
            # Buy & hold en pointillés, même couleur que la stratégie de l'actif
            ax.plot(perf_bh.index, perf_bh, linestyle='--', alpha=0.6,
                    color=ligne[0].get_color(), label=f"{actif} — B&H")
        ax.axhline(100, color='gray', linewidth=0.5)
        ax.set_ylabel("Base 100")
        ax.legend()
        st.pyplot(fig)

    # ===== ONGLET RISQUE =====
    with tab_risque:
        # Tableau 1 : métriques de la stratégie
        st.subheader(f"Métriques de risque — {strat_nom}")
        tab_strat = pd.DataFrame({a: metriques_risque(r) for a, r in rdts.items()}).T
        st.dataframe(tab_strat)

        # Tableau 2 : métriques du buy & hold (pour comparer)
        st.subheader("Métriques de risque — Buy & Hold")
        tab_bh = pd.DataFrame({a: metriques_risque(r) for a, r in rdts_bh.items()}).T
        st.dataframe(tab_bh)

        # Drawdown : stratégie (plein) + buy & hold (pointillés)
        st.subheader("Drawdown")
        fig2, ax2 = plt.subplots(figsize=(11, 3))
        for actif in actifs:
            for rdt, style in [(rdts[actif], '-'), (rdts_bh[actif], '--')]:
                cumul = (1 + rdt).cumprod()
                dd = (cumul - cumul.cummax()) / cumul.cummax()
                lbl = f"{actif}" if style == '-' else f"{actif} B&H"
                ax2.plot(dd.index, dd * 100, linestyle=style, label=lbl)
        ax2.axhline(0, color='black', linewidth=0.5)
        ax2.set_ylabel("Drawdown (%)")
        ax2.legend()
        st.pyplot(fig2)

        # Volatilité rolling 30j (stratégie uniquement, pour rester lisible)
        st.subheader("Volatilité rolling (30j, annualisée)")
        fig3, ax3 =

    

