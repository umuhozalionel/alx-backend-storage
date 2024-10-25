#!/usr/bin/env python3
""" Main file """

from exercise import Cache

cache = Cache()
cache.store(b"first")
print(cache._redis.get(cache.store.__qualname__))
cache.store(b"second")
cache.store(b"third")
print(cache._redis.get(cache.store.__qualname__))
