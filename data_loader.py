"""Télécharge et nerroie les donnèes de marché"""
import yfinance as yf
import pandas as pd 

UNIVERS={'SPY'      : 'Equity US',
    '^STOXX50E': 'Equity EU',
    '^KS11'    : 'Equity KR',
    'EURUSD=X' : 'FX EURUSD',
    'USDJPY=X' : 'FX USDJPY',
    'GBPUSD=X' : 'FX GBPUSD',
    'LQD'      : 'IG US',
    'IGLN.L'   : 'IG EU',
    'HYG'      : 'HY US',
    'IHYG.L'   : 'HY EU',}

def load_data(start='2019-01-01',end='2024-12-31'):
   tickers=list(UNIVERS.keys())
   raw=yf.download(tickers,start,end,auto_adjust=True,progress=False)['Close']
   prix=raw.ffill().dropna()
   rendements=prix.pct_change().dropna()
   return prix,rendements 

if __name__ == '__main__':
    prix, rendements = load_data()
    print('Données chargées :', prix.shape)
    print('\nDerniers prix :')
    print(prix.tail(3).round(2))
    print('\nDerniers rendements :')
    print(rendements.tail(3).round(4))


