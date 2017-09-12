import requests
import json
import pandas as pd


def request(url, name):
    request = requests.get(url)
    result = json.loads(request.text)
    data = pd.DataFrame(data=result[name]['data'], columns=result[name]['columns'])
    return data