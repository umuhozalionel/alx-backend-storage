#!/usr/bin/env python3
"""Module exercise - Contains the Cache class"""

import redis
import uuid
from typing import Union

class Cache:
    """Cache class to interact with Redis."""

    def __init__(self):
        """Initialize the Cache class."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using a random key and return the key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
