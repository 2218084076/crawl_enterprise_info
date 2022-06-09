import asyncio
import random

import aiohttp

from config import settings


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://b2b.11467.com/',
                               headers=settings.HEADERS) as response:
            print(response.status)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
