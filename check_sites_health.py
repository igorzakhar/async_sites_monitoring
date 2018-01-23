import asyncio
import argparse
from datetime import datetime, timezone
import re
from urllib.parse import urlparse

from aiohttp import ClientSession
import aiofiles
import dateutil.parser
import regex_map


async def load_urls4check(path):
    async with aiofiles.open(path, mode='r') as fp:
        urls = await fp.read()
        urls_list = urls.rstrip().split('\n')
        return urls_list


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
    return {
        'domain': domain,
        'http_status': http_status,
        'whois_info': whois_info
    }


async def check_sites_health(path_to_urls, loop):
    domains_list = await load_urls4check(path_to_urls)
    async with ClientSession(loop=loop) as session:
        tasks = [
            asyncio.ensure_future(get_status_for_each_url(domain, session))
            for domain in domains_list
        ]
        return await asyncio.gather(*tasks)


def parse_expiry_date(domain, whois_response):
    maxsplit = 2
    domain_chunks = domain.split('.', maxsplit)
    top_level_domain = domain_chunks[-1]
    pattern = getattr(regex_map, top_level_domain)
    expiration_date = re.search(
        pattern['expiration_date'],
        whois_response,
        re.IGNORECASE
    )
    expiration_date = expiration_date.group('date')
    return dateutil.parser.parse(expiration_date)


def print_results(check_sites_results):
    date_now = datetime.now(timezone.utc)
    status_string = '{:20s}: status code: {}, days until expiry: {} days ({})'
    for check_site in check_sites_results:
        expiry_date = parse_expiry_date(
            check_site['domain'],
            check_site['whois_info']
        )
        days_until_expiry = expiry_date - date_now
        print(status_string.format(
            check_site['domain'],
            check_site['http_status'],
            days_until_expiry.days,
            expiry_date.date()
        ))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, help="Path to file")
    args = parser.parse_args()
    if args.file:
        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(check_sites_health(args.file, loop))
        print_results(results)
        loop.close()
    else:
        print("You need to specify a file path with urls list")
