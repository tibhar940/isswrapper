from isswrapper.util.helpers import request_cursor, request_df, request_dict

import datetime
import pandas as pd
from tqdm import tqdm

from collections import defaultdict
from typing import Any


# def sitenews_d(start: int = 0, lang: str = "ru") -> pd.DataFrame:
#     """/iss/sitenews"""
#     name = "sitenews"
#     url = "https://iss.moex.com/iss/sitenews.json?start={0}&lang={1}"
#     d_dict = request_dict(url.format(start, lang), name)
#     return d_dict


def sitenews(start: int = 0, lang: str = "ru") -> pd.DataFrame:
    """/iss/sitenews"""
    name = "sitenews"
    url = "https://iss.moex.com/iss/sitenews.json?start={0}&lang={1}"
    df = request_df(url.format(start, lang), name)
    return df


# def sitenews_body_dict(id: int) -> str:
#     """/iss/sitenews/<id>"""
#     name = "content"
#     url = "https://iss.moex.com/iss/sitenews/{0}.json?"
#     body = request_dict(url.format(id), name)
#     return body


def sitenews_body(id: int) -> pd.DataFrame:
    """/iss/sitenews/<id>"""
    name = "content"
    url = "https://iss.moex.com/iss/sitenews/{0}.json?"
    df = request_df(url.format(id), name).loc[:, ["id", "body"]]
    return df


# Tried to optimize things with dict instead creating
# Dataframe After each iteration
# class SiteNews_1(object):
#     def __init__(self, lang: str = "ru"):
#         self.__start = 0
#         self.__end = 200
#         self.__name = "sitenews"
#         self.__lang = lang
#         self.__url = "https://iss.moex.com/iss/sitenews.json?start={0}&lang={1}"
#         self.__cursor = request_cursor(
#             self.__url.format(self.__start, self.__lang), self.__name
#         )
#         self.__current = self.__cursor["current"]
#         self.__step = self.__cursor["step"]
#         self.__df = pd.DataFrame()

#     df = property(lambda self: self.__df)

#     def load(
#         self,
#         ts1: datetime.datetime = None,
#         ts2: datetime.datetime = None,
#         d_filter: Any = None,
#         load_body: bool = False,
#     ):
#         """
#         Loading news from site within given date range.
#         Don't return anything, instead fill self.df DataFrame.

#         :param ts1: starting date, defaults to None
#         :type ts1: datetime.datetime, optional
#         :param ts2: ending date, defaults to None
#         :type ts2: datetime.datetime, optional
#         :param load_body: adds news body to df, defaults to False
#         :type load_body: bool, optional
#         :param d_filter: filtering function like [d_filter(df)->filtered_df], defaults to None
#         :type d_filter: Any, optional
#         """
#         if not ts2:
#             ts2 = datetime.datetime.now() + datetime.timedelta(days=1)
#         if not ts1:
#             ts1 = datetime.datetime.now() - datetime.timedelta(days=2)

#         ts_current = datetime.datetime.now()
#         sn_gdt = []
#         columns = []
#         with tqdm(desc="load site news") as pbar:
#             while ts_current > ts1:
#                 data, columns = sitenews_d(start=self.__current, lang=self.__lang)
#                 sn_gdt.extend(data)
#                 ts_current = datetime.datetime.strptime(
#                     data[-1][3], "%Y-%m-%d %H:%M:%S"
#                 )

#                 self.__current += self.__step

#                 pbar.update(1)

#         tmp_df = pd.DataFrame(sn_gdt, columns=columns)
#         tmp_df["published_at"] = tmp_df["published_at"].apply(
#             lambda x: datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
#         )
#         tmp_df["modified_at"] = tmp_df["modified_at"].apply(
#             lambda x: datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
#         )
#         tmp_df = tmp_df[tmp_df["published_at"].between(ts1, ts2)]
#         if load_body:
#             n_ids = tmp_df["id"].unique().tolist()
#             b_dict = {"id": n_ids, "body": []}
#             with tqdm(desc="load site body") as pbar:
#                 for b_id in n_ids:
#                     t_body = sitenews_body_dict(b_id)[0][0][3]
#                     b_dict["body"].append(t_body)
#                     pbar.update(1)
#             tmp_df = pd.merge(tmp_df, pd.DataFrame(b_dict), how="inner", on="id")
#         if d_filter:
#             tmp_df = d_filter(tmp_df)
#         self.__df = tmp_df

#     def __str__(self):
#         return """Total news loaded: {0}""".format(len(self.__df))


class SiteNews(object):
    def __init__(self, lang: str = "ru"):
        self.__start = 0
        self.__end = 200
        self.__name = "sitenews"
        self.__lang = lang
        self.__url = "https://iss.moex.com/iss/sitenews.json?start={0}&lang={1}"
        self.__cursor = request_cursor(
            self.__url.format(self.__start, self.__lang), self.__name
        )
        self.__current = self.__cursor["current"]
        self.__step = self.__cursor["step"]
        self.__df = pd.DataFrame()

    df = property(lambda self: self.__df)

    def load(
        self,
        ts1: datetime.datetime = None,
        ts2: datetime.datetime = None,
        d_filter: Any = None,
        load_body: bool = False,
    ):
        """
        Loading news from site within given date range.
        Don't return anything, instead fill self.df DataFrame.

        :param ts1: starting date, defaults to None
        :type ts1: datetime.datetime, optional
        :param ts2: ending date, defaults to None
        :type ts2: datetime.datetime, optional
        :param load_body: adds news body to df, defaults to False
        :type load_body: bool, optional
        :param d_filter: filtering function like [d_filter(df)->filtered_df], defaults to None
        :type d_filter: Any, optional
        """
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
                self.__df = pd.concat([self.__df, df], ignore_index=True)

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
                body_df = pd.concat([body_df, df], ignore_index=True)

            self.__df = pd.merge(self.__df, body_df, how="left", on="id")

        if d_filter:
            self.__df = d_filter(self.__df)

    def __str__(self):
        return """Total news loaded: {0}""".format(len(self.__df))


if __name__ == "__main__":
    sn_instance = SiteNews_1()
    filter = lambda x: x[
        x["title"].str.contains("Об изменении риск-параметров на фондовом рынке")
    ]
    sn_instance.load(ts1=datetime.datetime(2022, 1, 1), d_filter=filter, load_body=True)

    print(sn_instance.df.head())
