#!/usr/bin/env python3
""" Main file """

from web import get_page, redis_client

urls = [
    "http://slowwly.robertomurray.co.uk",
    "http://slowwly.robertomurray.co.uk/delay/1000/url/http://www.example.com",
    "http://slowwly.robertomurray.co.uk/delay/1000/url/http://www.example.com",
]

for url in urls:
    print(f"Fetching {url}")
    content = get_page(url)
    print(f"Content: {content[:100]}")
    print(f"Access count for {url}: {redis_client.get(f'count:{url}').decode('utf-8')}")
