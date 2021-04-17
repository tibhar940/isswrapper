import pandas as pd

from isswrapper.helpers import request


def candles(engine=None, market=None, boardid=None, securityid=None, start=0, dt1="", dt2="", interval=10):
    """/iss/engines/.../candles"""
    name = "candles"
    if dt1:
        dt1 = dt1.strftime("%Y-%m-%d")
    if dt2:
        dt2 = dt2.strftime("%Y-%m-%d")
    if securityid:
        url = "https://iss.moex.com/iss/engines/{0}/markets/{1}/securities/{3}/candles.json?start={4}&from={5}&till={6}&interval={7}"
        if boardid:
            url = "https://iss.moex.com/iss/engines/{0}/markets/{1}/boards/{2}/securities/{3}/candles.json?start={4}&from={5}&till={6}&interval={7}"
        candles = request(url.format(engine, market, boardid, securityid, start, dt1, dt2, interval), name)
    else:
        raise AttributeError("securityid must be specified")
    candles.loc[:, "begin"] = pd.to_datetime(candles["begin"], format="%Y-%m-%d %H:%M:%S")
    candles.loc[:, "end"] = pd.to_datetime(candles["end"], format="%Y-%m-%d %H:%M:%S")
    return candles


class Candles(object):
    def __init__(self, engine=None, market=None, boardid=None, securityid=None, dt1="", dt2="", interval=10):
        self.__engine = engine
        self.__market = market
        self.__boardid = boardid
        self.__securityid = securityid
        self.__dt1 = dt1
        self.__dt2 = dt2
        self.__interval = interval
        self.__start = 0
        self.__len = 500
        self.__limit = 500
        self.__candles = pd.DataFrame()

    engine = property(lambda self: self.__engine)
    market = property(lambda self: self.__market)
    boardid = property(lambda self: self.__boardid)
    securityid = property(lambda self: self.__securityid)
    dt1 = property(lambda self: self.__dt1)
    dt2 = property(lambda self: self.__dt2)
    interval = property(lambda self: self.__interval)
    candles = property(lambda self: self.__candles)

    def load(self):
        data = []
        while self.__len == self.__limit:
            c = candles(
                engine=self.__engine,
                market=self.__market,
                boardid=self.__boardid,
                securityid=self.__securityid,
                start=self.__start,
                dt1=self.__dt1,
                dt2=self.__dt2,
                interval=self.__interval,
            )
            data.append(c)
            self.__len = c.shape[0]
            self.__start += self.__len
        self.__candles = pd.concat(data)
        del data

    def __str__(self):
        return """------------------------------------------------------------------
Candles ({4} entries, begin: {5}, end: {6}, interval: {7})
engine: {0}, market: {1}, boardid: {2}, securityid: {3}
------------------------------------------------------------------""".format(
            self.__engine,
            self.__market,
            self.__boardid,
            self.__securityid,
            self.__candles.shape[0],
            self.__dt1,
            self.__dt2,
            self.__interval,
        )
