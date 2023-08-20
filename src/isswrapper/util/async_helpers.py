import asyncio
import httpx
import numpy as np


async def safe_fetch(fetch_function, semaphore, *args, **kwargs):
    """
    Safely fetch data using a provided semaphore to limit concurrent coroutines.

    This function wraps a given fetching function with a semaphore, which helps limit
    the number of coroutines that can run concurrently. It's particularly useful
    when you want to control the number of simultaneous requests to a server.

    :param fetch_function: The fetching function to be executed asynchronously.
    :type fetch_function: async function
    :param semaphore: The configured semaphore for limiting concurrency.
    :type semaphore: asyncio.Semaphore
    :param args: Arguments to be passed to the fetching function.
    :param kwargs: Keyword arguments to be passed to the fetching function.
    :return: The result of the fetch_function, often a JSON dictionary.
    :rtype: dict
    """
    async with semaphore:
        return await fetch_function(*args, **kwargs)


async def fetch_data(base_url: str, endpoint: str = "", params: dict = None) -> dict:
    """
    Fetches data asynchronously from a specified API endpoint.

    This function uses the httpx library to send an HTTP GET request to the specified
    API endpoint and retrieves the response in JSON format. It is designed to work
    asynchronously, making it suitable for handling multiple concurrent requests.

    :param base_url: The base URL of the API to connect to, e.g., "https://iss.moex.com/iss" for sitenews
    :type base_url: str
    :param endpoint: The API endpoint to fetch data from, e.g., "/sitenews.json".
    :type endpoint: str, optional
    :param params: Optional request parameters to include in the request.
    :type params: dict, optional
    :return: A dictionary containing the JSON response data.
    :rtype: dict
    """
    async with httpx.AsyncClient(base_url=base_url) as client:
        response = await client.get(endpoint, params=params)
        return response.json()


def run_async(func, *args, **kwargs):
    """
    Run an asynchronous function synchronously using asyncio.run().

    This function provides a convenient way to run an asynchronous function
    synchronously using the asyncio.run() function. It takes an asynchronous
    function `func` along with its arguments and keyword arguments, and executes
    it in an event loop using asyncio.run().

    :param func: The asynchronous function to be executed.
    :type func: callable
    :param args: Arguments to be passed to the asynchronous function.
    :param kwargs: Keyword arguments to be passed to the asynchronous function.
    :return: The result returned by the asynchronous function.
    """
    return asyncio.run(func(*args, **kwargs))


if __name__ == "__main__":
    sem = asyncio.Semaphore(5)
    res = run_async(
        safe_fetch,
        fetch_function=fetch_data,
        semaphore=sem,
        base_url="https://iss.moex.com/iss",
        endpoint="/sitenews/{0}.json".format(29287),
    )
