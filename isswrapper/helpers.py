import json
import pandas as pd
import requests


meta_dict = {
    "datetime": "datetime64[ns]",
    "date": "datetime64[D]",
    "time": str,
    "string": str,
    "int64": "Int64",
    "int32": "Int32",
    "double": "float64",
}


def request_df(url: str, name: str) -> pd.DataFrame:
    request = requests.get(url)
    result = json.loads(request.text)

    data = result[name]["data"]
    columns = result[name]["columns"]
    meta = {k: meta_dict[v["type"]] for k, v in result[name]["metadata"].items()}

    df = pd.DataFrame(data=data, columns=columns).astype(meta)
    df.columns = df.columns.str.lower()
    return df


def request_cursor(url: str, name: str) -> dict:
    request = requests.get(url)
    result = json.loads(request.text)
    _ = result["{0}.cursor".format(name)]["data"][0]
    cursor = {"current": _[0], "total": _[1], "step": _[2]}
    return cursor
