import asyncio
import aiohttp


url = 'http://127.0.0.1:8000/api/upload/'


async def post_request():
    file = {'file': 'tmp\\example\\example.jpg'}

    async with aiohttp.ClientSession() as session:
        async with session.post(url,
                                headers={'Authorization': 'Bearer 123456', 'Content-Type': 'image/jpg'},
                                data=file) as resp:
            response = await resp.json()
            print(response)

asyncio.run(post_request())
