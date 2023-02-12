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
                    return await response.read()
            return await asyncio.gather(*[
                fetch(url) for url in urls
            ])
    # convert get_all back into synchronous context
    return sync.async_to_sync(get_all)(urls)

# import sys
# import os
# import json
# import asyncio
# import aiohttp

# def async_aiohttp_get_all(urls: list) -> list:
#     # Initialize connection pool
#     conn = aiohttp.TCPConnector(limit_per_host=100, limit=0, ttl_dns_cache=300)
#     PARALLEL_REQUESTS = 100
#     results = []

#     async def gather_with_concurrency(n):
#         semaphore = asyncio.Semaphore(n)
#         session = aiohttp.ClientSession(connector=conn)

#         # heres the logic for the generator
#         async def get(url):
#             async with semaphore:
#                 async with session.get(url, ssl=False) as response:
#                     obj = json.loads(await response.read())
#                     results.append(obj)
#         await asyncio.gather(*(get(url) for url in urls))
#         await session.close()

#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     loop.run_until_complete(gather_with_concurrency(PARALLEL_REQUESTS))
#     conn.close()

#     return results
