import pandas as pd

from isswrapper.loaders.securities import (
    security_aggregates,
    security_boards,
    security_bondyields,
    security_description,
    security_indices,
)

pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 1000)


if __name__ == "__main__":
    result = security_description("SBER")
    print("==============================================================")
    print(result)

    result = security_boards("SBER")
    print("==============================================================")
    print(result)

    result = security_indices("SBER")
    print("==============================================================")
    print(result)

    result = security_aggregates("SBER")
    print("==============================================================")
    print(result)

    result = security_bondyields("SU26215RMFS2")
    print("==============================================================")
    print(result)
