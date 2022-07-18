import aiohttp


headers = {

}


async def post_request(file: str, file_id: int, tag: str, photo_number: int):
    url = f'http://176.53.160.122:8000/api/upload?file_id={file_id + photo_number}&tag={tag}'

    data = {
        "file_id": bytes(file_id + photo_number),
        "tag": tag,
        "file": open(file, 'rb')
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url,
                                headers=headers,
                                data=data) as resp:
            response = await resp.json()
            print(response)
