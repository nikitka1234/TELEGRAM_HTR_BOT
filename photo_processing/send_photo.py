import aiohttp


url = 'https://example.com'


async def post_request():
    file = {'file': open('')}
    async with aiohttp.ClientSession() as session:
        async with session.post('http://example.com',
                                headers={'Authorization': 'Bearer 123456', 'Content-Type': 'image/jpg'},
                                data=file) as resp:
            response = await resp.json()
            print(response)
