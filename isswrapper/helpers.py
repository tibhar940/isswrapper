import json

import pandas as pd
import requests


def request(url, name):
    request = requests.get(url)
    result = json.loads(request.text)
    df = pd.DataFrame(data=result[name]["data"], columns=result[name]["columns"])
    df.columns = df.columns.str.lower()
    return df
