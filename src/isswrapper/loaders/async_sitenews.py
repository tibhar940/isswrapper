import asyncio

import numpy as np
from isswrapper.util.async_helpers import fetch_data, safe_fetch, run_async
from isswrapper.util.helpers import preprocess_site_news_data, request_cursor
import nest_asyncio
import pandas as pd

nest_asyncio.apply()


async def fetch_sitenews_batched(
    n: int = 1000,
    base_url: str = "https://iss.moex.com/iss",
    endpoint: str = "/sitenews.json",
    batch_size: int = 50,
    n_semaphore: int = 5,
) -> list:
    """
    Fetches site news data asynchronously in batches from a specified API endpoint.


    :param n: The total number of records to fetch. If negative or zero, no data will be fetched.
    :type n: int, optional
    :param base_url: The base URL of the API to connect to.
    :type base_url: str, optional
    :param endpoint: The API endpoint to fetch site news data from, e.g., "/sitenews.json".
    :type endpoint: str, optional
    :param batch_size: The size of each batch for fetching data in parallel. For sitenews defaults to 50, other option don't work for now
    :type batch_size: int, optional
    :param n_semaphore: The limit of concurrency coroutines.
    :type n_semaphore: int, optional
    :return: A list of dictionaries containing the fetched site news data.
    :rtype: list
    """
    if n <= 0:
        return []
    sem = asyncio.Semaphore(n_semaphore)
    tasks = [
        safe_fetch(
            fetch_data,
            sem,
            base_url=base_url,
            endpoint=endpoint,
            params={"start": st, "lang": "ru"},
        )
        for st in np.arange(0, n, batch_size)
    ]
    results = await asyncio.gather(*tasks)

    return results


async def fetch_sitenews_body(
    news_ids: int,
    n_semaphore: int = 5,
):
    if not news_ids:
        return []
    sem = asyncio.Semaphore(n_semaphore)
    tasks = [
        safe_fetch(
            fetch_data,
            sem,
            base_url="https://iss.moex.com/iss",
            endpoint="/sitenews/{0}.json".format(id),
        )
        for id in news_ids
    ]
    results = await asyncio.gather(*tasks)
    return results


def load_all_news(n_semaphore: int = 5, load_content_df: bool = False) -> list:
    """
    Load all news from https://iss.moex.com/iss/sitenews.json

    :param run: if true creates event loop using asyncio.run(), defaults to False
    :type run: bool, optional
    :return: all pages of news
    :rtype: list
    """
    cursor = request_cursor("https://iss.moex.com/iss/sitenews.json", "sitenews")
    results = run_async(
        fetch_sitenews_batched,
        base_url="https://iss.moex.com/iss/sitenews",
        endpoint=".json",
        n=cursor["total"],
        batch_size=cursor["step"],
        n_semaphore=n_semaphore,
    )
    sitenews_df = pd.DataFrame(preprocess_site_news_data(results))
    if not load_content_df:
        return sitenews_df, None
    sitenews_ids = sitenews_df["id"].unique().tolist()
    body_raw_data = run_async(
        fetch_sitenews_body,
        news_ids=sitenews_ids,
        n_semaphore=n_semaphore,
    )
    body_df = pd.DataFrame(preprocess_site_news_data(body_raw_data, "content"))
    return sitenews_df, body_df


if __name__ == "__main__":
    import time

    st_time = time.time()
    # res = run_async(fetch_sitenews_body, news_ids=[63278, 63277, 63276, 63275, 63274])
    # res = run_async(
    #     safe_fetch,
    #     fetch_function=fetch_data,
    #     semaphore=asyncio.Semaphore(5),
    #     base_url="https://iss.moex.com/iss/sitenews",
    #     endpoint=".json",
    #     params={"start": 0, "lang": "ru"},
    # )

    res = load_all_news()
    print("__________________________________")
    print(len(res))
    print("______________________________")
    print(res)
    print("____________________")
    print(("--- %s seconds ---" % (time.time() - st_time)))
