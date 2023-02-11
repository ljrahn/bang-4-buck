import aiohttp
import asyncio
from asgiref import sync


def async_aiohttp_get_all(urls: list) -> list:
    """
    performs asynchronous get requests
    :param urls: a list of all the urls to make a request to
    :returns: list of tuples where each index in the list is the (json response, status code) of a corresponding request 
    """
    async def get_all(urls):
        async with aiohttp.ClientSession() as session:
            async def fetch(url):
                async with session.get(url) as response:
                    return await response.json(), response.status
            return await asyncio.gather(*[
                fetch(url) for url in urls
            ])
    # convert get_all back into synchronous context
    return sync.async_to_sync(get_all)(urls)
