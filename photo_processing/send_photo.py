# import asyncio
import aiohttp


headers = {

}


async def post_request(file: str, file_id: int):
    url = f'http://176.53.160.122:8000/api/upload?file_id={file_id}'

    data = {
        "file_id": bytes(file_id),
        "file": open(file, 'rb')
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url,
                                headers=headers,
                                data=data) as resp:
            response = await resp.json()
            print(response)

# asyncio.run(post_request('C:\\Users\\mrkim\\PycharmProjects\\HTR_BOT\\tmp\\example\\example.jpg', 5))
