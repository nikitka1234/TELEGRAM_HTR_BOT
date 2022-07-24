import aiohttp
import re

r_str = r'.*?(?=\,"size"|$)'
r_str1 = r'.name.*'


async def get_history(tag: str, limit: int = 10):
    url = f'http://176.53.160.122:8000/api/get?tag={tag}&limit={limit}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            response = await resp.read()

            result = response.decode('UTF-8').split('},{')

            for x in range(0, len(result)):
                match = re.search(r_str, result[x])
                match = re.search(r_str1, str(match.group(0)))

                if match != None:
                    result[x] = match.group(0).split(':')[1]

            return result
            # print(response.decode('UTF-8'))
