import aiohttp
import re


r_str = r'.*?(?=\,"name"|$)'
r_str1 = r'.text.*'


async def get_text(tag: str, name: str):
    url = f'http://176.53.160.122:8000/api/get?tag={tag}&name={name}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            response = await resp.read()

            result = response.decode('UTF-8')

            match = re.search(r_str, result)
            match = re.search(r_str1, str(match.group(0)))

            return match.group(0).split(':')[1]
