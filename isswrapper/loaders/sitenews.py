import datetime

import pandas as pd
from tqdm import tqdm

from isswrapper.helpers import request_cursor, request_df


def sitenews(start: int = 0, lang: str = "ru") -> pd.DataFrame:
    """/iss/sitenews"""
    name = "sitenews"
    url = "https://iss.moex.com/iss/sitenews.json?start={0}&lang={1}"
    df = request_df(url.format(start, lang), name)
    return df


def sitenews_body(id: int) -> pd.DataFrame:
    """/iss/sitenews/<id>"""
    name = "content"
    url = "https://iss.moex.com/iss/sitenews/{0}.json?"
    df = request_df(url.format(id), name).loc[:, ["id", "body"]]
    return df


class SiteNews(object):
    def __init__(self, lang: str = "ru"):
        self.__start = 0
        self.__end = 200
        self.__name = "sitenews"
        self.__lang = lang
        self.__url = "https://iss.moex.com/iss/sitenews.json?start={0}&lang={1}"
        self.__cursor = request_cursor(self.__url.format(self.__start, self.__lang), self.__name)
        self.__current = self.__cursor["current"]
        self.__step = self.__cursor["step"]
        self.__df = pd.DataFrame()

    df = property(lambda self: self.__df)

    def load(self, ts1: datetime.datetime = None, ts2: datetime.datetime = None, load_body: bool = False):
        if not ts2:
            ts2 = datetime.datetime.now() + datetime.timedelta(days=1)
        if not ts1:
            ts1 = datetime.datetime.now() - datetime.timedelta(days=2)

        ts_current = datetime.datetime.now()
        with tqdm(desc="load site news") as pbar:
            while ts_current > ts1:
                df = sitenews(start=self.__current, lang=self.__lang)
                ts_current = df["published_at"].min()
                df = df[df["published_at"].between(ts1, ts2)]
                self.__df = self.__df.append(df).reset_index(drop=True)
                self.__current += self.__step
                pbar.update(1)

        if load_body:
            if "body" in self.__df:
                ids_to_process = self.__df[self.__df["body"].isnull()]["id"].unique()
                body_df = self.__df[~self.__df["body"].isnull()].loc[:, ["id", "body"]]
                self.__df = self.__df.drop(columns=["body"])
            else:
                body_df = pd.DataFrame()
                ids_to_process = self.__df["id"].unique()
            for id in tqdm(ids_to_process, desc="Load site news body"):
                df = sitenews_body(id)
                body_df = body_df.append(df)

            self.__df = pd.merge(self.__df, body_df, how="left", on="id")

    def __str__(self):
        return """Total news loaded: {0}""".format(len(self.__df))
