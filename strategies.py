import pandas as pd
import numpy as np

def ma_strat(prix,rendements,MH=50,MB=20):
   mh=prix.rolling(MH).mean()
   mb=prix.rolling(MB).mean()
   position=(mb>mh).astype(int)
   position=position.shift(1).fillna(0)
   rdt_strat=position*rendements
   return rdt_strat

def momentum_strat(prix,rendements,lookback=21):
   momentum=prix.pct_change(lookback)
   position=(momentum>0).astype(int)
   position=position.shift(1).fillna(0)
   rdt_strat=position*rendements
   return rdt_strat

def mean_r_strat(prix, rendements, periode=14):
   delta=prix.diff()
   gain=delta.clip(lower=0)
   perte=-delta.clip(upper=0)
   moy_gains=gain.rolling(periode).mean()
   moy_pertes=perte.rolling(periode).mean()
   rs=moy_gains/moy_pertes
   rsi=100-(100/(1+rs))

   position = pd.Series(np.nan, index=prix.index)
   position[rsi<30]=1
   position[rsi>70]=0
   position = position.ffill().fillna(0)  
   position = position.shift(1).fillna(0)

   rdt=position*rendements

   return rdt





if __name__ == '__main__':
    from data_loader import load_data
    prix, rendements = load_data()
    print(ma_strat(prix['SPY'],rendements['SPY'],MH=50,MB=30))




