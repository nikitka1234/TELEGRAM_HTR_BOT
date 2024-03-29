import aiohttp


headers = {
    # 'Content-type': 'multipart/form-data'
}


async def post_request(file: str, file_id: int, tag: str, photo_number: int, caption: str = 'null'):
    url = f'http://176.53.160.122:8000/api/upload?file_id={file_id + photo_number}&tag={tag}&text={caption.lower()}'

    data = {
        "file_id": bytes(file_id + photo_number),
        "tag": tag,
        "file": open(file, 'rb'),
        "text": caption.lower()
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url,
                                headers=headers,
                                data=data) as resp:
            await resp.json()
