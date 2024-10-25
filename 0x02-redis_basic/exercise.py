#!/usr/bin/env python3
"""Module exercise - Contains the Cache class"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps

def count_calls(method: Callable) -> Callable:
    """Decorator that counts the number of times a method is called."""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function that increments the count and calls the method."""
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper

def call_history(method: Callable) -> Callable:
    """Decorator to store history of inputs and outputs for a particular function."""
    input_key = f"{method.__qualname__}:inputs"
    output_key = f"{method.__qualname__}:outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function to store inputs and outputs."""
        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))
        return output

    return wrapper

def replay(method: Callable) -> None:
    """Display the history of calls of a particular function."""
    redis_instance = redis.Redis()
    input_key = f"{method.__qualname__}:inputs"
    output_key = f"{method.__qualname__}:outputs"
    inputs = redis_instance.lrange(input_key, 0, -1)
    outputs = redis_instance.lrange(output_key, 0, -1)
    
    print(f"{method.__qualname__} was called {len(inputs)} times:")
    for input, output in zip(inputs, outputs):
        input = input.decode("utf-8")
        output = output.decode("utf-8")
        print(f"{method.__qualname__}(*{input}) -> {output}")

class Cache:
    """Cache class to interact with Redis."""

    def __init__(self):
        """Initialize the Cache class."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using a random key and return the key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis and convert it back to the desired format using fn.
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn is not None:
            return fn(value)
        return value

    def get_str(self, key: str) -> Union[str, None]:
        """Retrieve a string from Redis."""
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> Union[int, None]:
        """Retrieve an integer from Redis."""
        return self.get(key, int)
