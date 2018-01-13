import asyncio
import re
from urllib.parse import urlparse

from aiohttp import ClientSession
import aiofiles
import dateutil.parser
import regex_map


async def load_urls4check(path):
    async with aiofiles.open(path, mode='r') as fp:
        urls = await fp.read()
        urls = urls.rstrip().split('\n')
        return urls


async def fetch_response_status(url, session):
    async with session.get(url) as response:
        return response.status


async def whois_me(domain):
    domain = urlparse(domain).netloc
    process = await asyncio.create_subprocess_exec(
        *['whois', domain],
        stdout=asyncio.subprocess.PIPE
    )
    result, _ = await process.communicate()
    return result.decode('utf-8')


async def get_status_for_each_url(domain, session):
    http_status = await fetch_response_status(domain, session)
    whois_info = await whois_me(domain)
    return domain, http_status, whois_info


async def check_sites_health(path_to_urls, loop):
    domains_list = await load_urls4check(path_to_urls)
    async with ClientSession(loop=loop) as session:
        tasks = [
            asyncio.ensure_future(get_status_for_each_url(domain, session))
            for domain in domains_list
        ]
        return await asyncio.gather(*tasks)


def parse_expiration_date(domain, whois_response):
    domain_chunks = domain.split('.', 2)
    top_level_domain = domain_chunks[-1]
    pattern = getattr(regex_map, top_level_domain)
    expiration_date = re.search(
        pattern['expiration_date'],
        whois_response,
        re.IGNORECASE
    )
    expiration_date = expiration_date.group('date')
    return dateutil.parser.parse(expiration_date)


def print_results(results):
    for result in results:
        print(
            result[0],
            result[1],
            parse_expiration_date(result[0], result[2])
        )


if __name__ == '__main__':
    path = 'urls.txt'
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(check_sites_health(path, loop))
    print_results(results)
    loop.close()
