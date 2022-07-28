import aiohttp


headers = {
    # 'Content-type': 'multipart/form-data'
}


async def start_processing(file_id: int):
    url = f'http://176.53.160.122:8000/api/get?file_id={file_id}'

    data = {
        "file_id": bytes(file_id),
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url,
                                headers=headers,
                                data=data) as resp:
            await resp.json()
