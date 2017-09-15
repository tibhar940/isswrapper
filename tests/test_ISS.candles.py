import pandas as pd
import datetime

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

from ISS.candles import candles, Candles

# c = candles(engine='stock', market='shares')
# print(c.shape)
# print(c.head())

c = candles(engine='stock', market='shares', securityid='SBER')
print(c.shape)
print(c.head())

c = candles(engine='stock', market='shares', securityid='SBER', interval=1)
print(c.shape)
print(c.head())

c = candles(engine='stock', market='shares', securityid='SBER', interval=60)
print(c.shape)
print(c.head())

c = candles(engine='stock', market='shares', securityid='SBER', interval=24)
print(c.shape)
print(c.head())

c = candles(engine='stock', market='shares', boardid='TQBR', securityid='SBER')
print(c.shape)
print(c.head())

c = candles(engine='stock', market='shares', boardid='TQBR', securityid='SBER', dt1=datetime.date(2017, 9, 1))
print(c.shape)
print(c.head())

c = candles(
    engine='stock', market='shares', boardid='TQBR', securityid='SBER',
    dt1=datetime.date(2017, 9, 1), dt2=datetime.date(2017, 9, 5))
print(c.shape)
print(c.head())
print(c.info())

C = Candles(
    engine='stock', market='shares', boardid='TQBR', securityid='SBER',
    dt1=datetime.date(2017, 1, 1), interval=24)
print(C)
C.load()
print(C)
print(C.candles.head())
print(C.candles.tail())
print(C.candles.shape[0])

C = Candles(
    engine='stock', market='shares', boardid='TQBR', securityid='SBER',
    dt1=datetime.date(2013, 8, 1), dt2=datetime.date(2017, 9, 5), interval=24)
print(C)
C.load()
print(C)
print(C.candles.head())
print(C.candles.tail())
print(C.candles.shape[0])