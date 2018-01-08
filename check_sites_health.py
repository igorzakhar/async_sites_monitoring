import asyncio

from aiohttp import ClientSession
import aiofiles


async def load_urls4check(path):
    async with aiofiles.open(path, mode='r') as fp:
        return await fp.read()


async def fetch(url, session):
    async with session.get(url) as response:
        return response


async def get_servers_response(urls):
    async with ClientSession() as session:
        tasks = [
            asyncio.ensure_future(fetch(url, session))
            for url in urls
        ]
        return await asyncio.gather(*tasks)


def get_servers_response_status(responses):
    for response in responses:
        print(response.url, response.status)


async def run(path):
    content = await load_urls4check(path)
    urls_list = content.rstrip().split('\n')
    servers_respond = await get_servers_response(urls_list)
    return servers_respond


if __name__ == '__main__':
    path = 'urls.txt'
    loop = asyncio.get_event_loop()
    responses = loop.run_until_complete(run(path))
    get_servers_response_status(responses)
    loop.close()
