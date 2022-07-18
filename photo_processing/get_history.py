import aiohttp


async def get_history(tag: str, limit: int = 10):
    url = f'http://176.53.160.122:8000/api/get?tag={tag}&limit={limit}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            response = await resp.read()
            return response
            # print(response.decode('UTF-8'))
