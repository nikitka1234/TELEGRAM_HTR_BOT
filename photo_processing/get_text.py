import aiohttp


async def get_request():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://example.com') as resp:
            response = await resp.read()
            print(response)
