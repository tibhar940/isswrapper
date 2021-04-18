import datetime

import pandas as pd

from isswrapper.loaders.sitenews import SiteNews, sitenews

pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 1000)


if __name__ == "__main__":
    df = sitenews()
    print(df.shape)
    print(df.head())

    sn = SiteNews(lang="ru")
    sn.load()
    df = sn.df
    print(df.shape)
    print(df.head())
    print(df.info())

    sn = SiteNews(lang="ru")
    sn.load(ts1=datetime.datetime(2021, 3, 10))
    df = sn.df
    print(df.shape)
    print(df.tail())
    print(df.info())

    sn = SiteNews(lang="ru")
    sn.load(ts1=datetime.datetime(2021, 3, 10), ts2=datetime.datetime(2021, 4, 1))
    df = sn.df
    print(df.shape)
    print(df.tail())
    print(df.info())

    sn = SiteNews(lang="ru")
    sn.load(ts1=datetime.datetime(2021, 3, 10), ts2=datetime.datetime(2021, 4, 1), load_body=True)
    df = sn.df
    print(df.shape)
    print(df.tail())
    print(df.info())
    print(sn)
