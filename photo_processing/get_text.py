import asyncio
import aiohttp


async def get_request(id: int):
    url = f'http://127.0.0.1:8000/api/get?id={id}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            response = await resp.read()
            print(response)

asyncio.run(get_request(5))
