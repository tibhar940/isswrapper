import pandas as pd
import datetime

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

from ISS.trades import trades, Trades

t = trades(engine='stock', market='shares')
print(t.shape)
print(t.head())

t = trades(engine='stock', market='shares', limit=100)
print(t.shape)
print(t.head())

t = trades(engine='stock', market='shares', boardid='TQBR')
print(t.shape)
print(t.head())

t = trades(engine='stock', market='shares', securityid='SBER')
print(t.shape)
print(t.head())

T = Trades(engine='stock', market='shares')
print(T)
T.load()
print(T)
print(T.trades.head())

T = Trades(engine='stock', market='shares', securityid='LKOH')
print(T)
T.load()
print(T)
print(T.trades.head())

T = Trades(engine='stock', market='shares', boardid='TQBR')
print(T)
T.load()
print(T)
print(T.trades.head())
print(T.trades.info())