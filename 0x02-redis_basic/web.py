#!/usr/bin/env python3
"""Web module to fetch and cache pages."""

import requests
import redis
from typing import Callable
from functools import wraps

redis_client = redis.Redis()

def cache_with_expiry(ttl: int):
    """Decorator to cache the result of a function for a specific time."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            url = args[0]
            cache_key = f"count:{url}"
            cached_result = redis_client.get(cache_key)

            if cached_result:
                return cached_result.decode('utf-8')

            result = func(*args, **kwargs)
            redis_client.setex(cache_key, ttl, result)
            return result

        return wrapper
    return decorator

@cache_with_expiry(10)
def get_page(url: str) -> str:
    """Fetches HTML content of a URL and caches it."""
    redis_client.incr(f"count:{url}")
    response = requests.get(url)
    return response.text
