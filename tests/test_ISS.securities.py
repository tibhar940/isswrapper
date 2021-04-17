import datetime

import pandas as pd

pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 1000)

from isswrapper.loaders.securities import (
    q,
    security_aggregates,
    security_boards,
    security_bondyields,
    security_description,
    security_indices,
)

s = q("MOEX")
print(s.head())

d = security_description("MOEX")
print(d.head())

b = security_boards("MOEX")
print(b.head())

i = security_indices("MOEX")
print(i.head())

a = security_aggregates("MOEX")
print(a.head())

a = security_aggregates("MOEX", date=datetime.date(2017, 9, 8))
print(a.head())

by = security_bondyields("SU25081RMFS9")
print(by.head())

by = security_bondyields("SU25081RMFS9", date=datetime.date(2017, 9, 8))
print(by.head())
