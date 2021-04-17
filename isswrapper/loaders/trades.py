import pandas as pd

from isswrapper.helpers import request


def trades(
    engine=None,
    market=None,
    boardid=None,
    securityid=None,
    limit=5000,
    reversed=0,
    previous_session=0,
    tradeno=0,
    start=0,
):
    """/iss/engines/.../trades"""
    name = "trades"
    url = "https://iss.moex.com/iss/engines/{0}/markets/{1}/trades.json?limit={4}&resersed={5}&previous_session={6}&tradeno={7}&start={8}"
    if boardid:
        url = "https://iss.moex.com/iss/engines/{0}/markets/{1}/boards/{2}/trades.json?limit={4}&resersed={5}&previous_session={6}&tradeno={7}&start={8}"
    if securityid:
        url = "https://iss.moex.com/iss/engines/{0}/markets/{1}/securities/{3}/trades.json?limit={4}&resersed={5}&previous_session={6}&tradeno={7}&start={8}"
    trades = request(
        url.format(engine, market, boardid, securityid, limit, reversed, previous_session, tradeno, start), name
    )
    trades.columns = trades.columns.str.lower()
    trades.loc[:, "systime"] = pd.to_datetime(trades["systime"], format="%Y-%m-%d %H:%M:%S")
    return trades


class Trades(object):
    def __init__(
        self, engine=None, market=None, boardid=None, securityid=None, reversed=0, previous_session=0, tradeno=0
    ):
        self.__engine = engine
        self.__market = market
        self.__boardid = boardid
        self.__securityid = securityid
        self.__reversed = reversed
        self.__previous_session = previous_session
        self.__tradeno = tradeno
        self.__start = 0
        self.__len = 5000
        self.__limit = 5000
        self.__trades = pd.DataFrame(columns=["secid", "systime"])

    engine = property(lambda self: self.__engine)
    market = property(lambda self: self.__market)
    boardid = property(lambda self: self.__boardid)
    securityid = property(lambda self: self.__securityid)
    trades = property(lambda self: self.__trades)

    def load(self):
        data = []
        while self.__len == self.__limit:
            t = trades(
                engine=self.__engine,
                market=self.__market,
                boardid=self.__boardid,
                securityid=self.__securityid,
                limit=self.__limit,
                start=self.__start,
            )
            data.append(t)
            self.__len = t.shape[0]
            self.__start += self.__len
        self.__trades = pd.concat(data)
        del data

    def __str__(self):
        return """------------------------------------------------------------------
Trades ({4} trades, {5} securityids, time: {6})
engine: {0}, market: {1}, boardid: {2}, securityid: {3}
------------------------------------------------------------------""".format(
            self.__engine,
            self.__market,
            self.__boardid,
            self.__securityid,
            self.__trades.shape[0],
            self.__trades["secid"].nunique(),
            self.__trades["systime"].max(),
        )
