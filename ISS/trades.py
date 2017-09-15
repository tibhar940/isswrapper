import pandas as pd
from ISS.helpers import request

# /iss/engines/[engine]/markets/[market]/trades
# /iss/engines/[engine]/markets/[market]/securities/[security]/trades
# /iss/engines/[engine]/markets/[market]/boards/[board]/trades
# /iss/engines/[engine]/markets/[market]/boardgroups/[boardgroup]/trades
# /iss/engines/[engine]/markets/[market]/boardgroups/[boardgroup]/securities/[security]/trades


def trades(engine=None, market=None, boardid=None, securityid=None, limit=5000, reversed=0, previous_session=0, tradeno=0, start=0):
    """/iss/engines/.../trades - https://iss.moex.com/iss/reference/55"""
    name = 'trades'
    url = 'https://iss.moex.com/iss/engines/{0}/markets/{1}/trades.json?limit={4}&resersed={5}&previous_session={6}&tradeno={7}&start={8}'
    if boardid:
        url = 'https://iss.moex.com/iss/engines/{0}/markets/{1}/boards/{2}/trades.json?limit={4}&resersed={5}&previous_session={6}&tradeno={7}&start={8}'
    if securityid:
        url = 'https://iss.moex.com/iss/engines/{0}/markets/{1}/securities/{3}/trades.json?limit={4}&resersed={5}&previous_session={6}&tradeno={7}&start={8}'
    trades = request(url.format(engine, market, boardid, securityid, limit, reversed, previous_session, tradeno, start), name)
    trades.columns = trades.columns.str.lower()
    return trades


class Trades(object):

    def __init__(self, engine=None, market=None, boardid=None, securityid=None, reversed=0, previous_session=0, tradeno=0):
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

    @property
    def trades(self):
        return self.__trades

    def load(self):
        data = []
        while self.__len == self.__limit:
            t = trades(engine=self.__engine, market=self.__market, boardid=self.__boardid, securityid=self.__securityid, limit=self.__limit, start=self.__start)
            data.append(t)
            self.__len = t.shape[0]
            self.__start += self.__len
        self.__trades = pd.concat(data)
        del data