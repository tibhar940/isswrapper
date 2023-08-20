import json

# from lxml import html
import pandas as pd
import requests
import datetime

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
    request = requests.get(url, timeout=30)
    result = json.loads(request.text)

    data = result[name]["data"]
    columns = result[name]["columns"]
    meta = {k: meta_dict[v["type"]] for k, v in result[name]["metadata"].items()}

    df = pd.DataFrame(data=data, columns=columns).astype(meta)
    df.columns = df.columns.str.lower()
    return df


def request_cursor(url: str, name: str) -> dict:
    request = requests.get(url, timeout=30)
    result = json.loads(request.text)
    _ = result["{0}.cursor".format(name)]["data"][0]
    cursor = {"current": _[0], "total": _[1], "step": _[2]}
    return cursor


def convert_data_with_metadata(data, metadata, columns):
    converted_data = []
    type_handlers = {
        "int64": int,
        "int32": int,
        "int": int,
        "string": str,
        "datetime": lambda x: datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
        # expandable
    }
    for row in data:
        converted_row = {}
        for col_name, col_value, col_type in zip(
            columns, row, [metadata[col]["type"] for col in columns]
        ):
            handler = type_handlers.get(col_type, lambda x: x)
            converted_row[col_name] = handler(col_value)

        converted_data.append(converted_row)

    return converted_data


def preprocess_site_news_data(raw_data: list, name: str = "sitenews"):
    processed_data = []

    for entry in raw_data:
        site_news_metadata = entry[name]["metadata"]
        site_news_columns = entry[name]["columns"]
        site_news_data = entry[name]["data"]
        converted_site_news_data = convert_data_with_metadata(
            site_news_data, site_news_metadata, site_news_columns
        )
        processed_data.extend(converted_site_news_data)

    return processed_data
