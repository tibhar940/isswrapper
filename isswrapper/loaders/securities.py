from isswrapper.helpers import request


def q(q="", lang="ru", engine="", market="", is_trading=None, group_by="", limit=100, start=0):
    """/iss/securities - https://iss.moex.com/iss/reference/5"""
    name = "securities"
    url = "https://iss.moex.com/iss/securities.json?q={0}&lang={1}&engine={2}&market={3}&is_trading={4}&group_by={5}\
    &limit={6}&start={7}"
    df = request(url.format(q, lang, engine, market, is_trading, group_by, limit, start), name)
    return df


def security_description(q="", lang="ru", start=0):
    """/iss/securities/[security] - https://iss.moex.com/iss/reference/13 (description)"""
    name = "description"
    url = "https://iss.moex.com/iss/securities/{0}.json?lang={1}&start={2}"
    df = request(url.format(q, lang, start), name)
    return df


def security_boards(q="", lang="ru", start=0):
    """/iss/securities/[security] - https://iss.moex.com/iss/reference/13 (boards)"""
    name = "boards"
    url = "https://iss.moex.com/iss/securities/{0}.json?lang={1}&start={2}"
    df = request(url.format(q, lang, start), name)
    return df


def security_indices(q="", lang="ru", only_actual=0):
    """/iss/securities/[security]/indices - https://iss.moex.com/iss/reference/160"""
    name = "indices"
    url = "https://iss.moex.com/iss//securities/{0}/indices.json?lang={1}&only_actual={2}"
    df = request(url.format(q, lang, only_actual), name)
    return df


def security_aggregates(q="", lang="ru", date=None):
    """/iss/securities/[security]/aggregates - https://iss.moex.com/iss/reference/214"""
    name = "aggregates"
    url = "http://iss.moex.com/iss/securities/{0}/aggregates.json?lang={1}&date={2}"
    if date:
        date = date.strftime("%Y-%m-%d")
    df = request(url.format(q, lang, date), name)
    return df


def security_bondyields(q="", boardid="", date=None):
    """/iss/securities/[security]/bondyields - https://iss.moex.com/iss/reference/713"""
    name = "yields"
    url = "http://iss.moex.com/iss/securities/{0}/bondyields.json?boardid={1}&date={2}"
    if date:
        date = date.strftime("%Y-%m-%d")
    df = request(url.format(q, boardid, date), name)
    return df
