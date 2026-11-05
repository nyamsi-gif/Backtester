import numpy as np 
def rdt(rendements):
    return ((1+rendements).prod()-1)*100

def vol(rendements):
    return rendements.std()*np.sqrt(252)*100

def sharpe(rendements,rf=0.04):
    return (rendements.mean()*252-rf)/(rendements.std()*np.sqrt(252))

def max_drawdown(rendements):
    cummul=(1+rendements).cumprod()
    sommet=cummul.cummax()
    drawdowns=(cummul-sommet)/sommet
    max_dd=drawdowns.min()
    return(max_dd)

def resume(rendements, nom='Stratégie'):
    """Affiche toutes les métriques d'un coup."""
    print(f'── {nom} ──')
    print(f'  Rendement total : {rdt(rendements):+.1f} %')
    print(f'  Volatilité      : {vol(rendements):.1f} %')
    print(f'  Sharpe          : {sharpe(rendements):.2f}')
    print(f'  Max Drawdown    : {max_drawdown(rendements)*100:.1f} %')
    

if __name__ == '__main__':
    from data_loader import load_data
    prix, rendements = load_data()
    resume(rendements['SPY'], nom='SPY Buy & Hold') 
