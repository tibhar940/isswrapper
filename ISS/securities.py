import requests
import json


def q(q='', lang='ru', engine='', market='', is_trading=None, group_by='', limit=100, start=0):
    url = 'https://iss.moex.com/iss/securities.json?q={0}&lang={1}&engine={2}&market={3}&is_trading={4}&group_by={5}\
    &limit={6}&start={7}'
    request = requests.get(url.format(q, lang, engine, market, is_trading, group_by, limit, start))
    result = json.loads(request.text)
    return result
