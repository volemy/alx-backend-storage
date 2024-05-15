#!/usr/bin/env python3
"""
This module defines a cache class that provides methods to store data using
randomly generated keys.
"""

import redis
import uuid
import functools import wraps
from typing import Union, Callable, Optional


def count_calls(method: Callable) -> Callable:
    """
    Decorator that takes a single argument and returns a callable
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.inc(key)
            return method(self, *args, **kwargs)
        return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs 
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = "{}:inputs".format(method.__qualname__)
        self._redis.rpush(input_key, str(args))

        output = method(*args, **kwargs)
        output_key = "{}:outputs".format(method.__qualname__)
        self._redis.rpush(output_key, output)

        return output
    return wrapper


def replay(method: Callable):
    """
    This method displays the history of calls of a particular function
    """
    input_key = "{}:inputs".format(method.__qualname__)
    output_key = "{}:outputs".format(method.__qualname__)

    inputs = self._redis.lrange(input_key, 0, -1)
    outputs = self._redis.lrange(output_key, 0. -1)

    print("{} was called {} times:".format(method.__qualname__, len(inputs)))
    for input_data, output_data in zip(inputs, outputs):
        args = eval(input_data.decode("utf-8"))
        print("Cache.{}(*{}) -> {}".format(method.__qualname__, args, output_data))

class Cache:
    def __init__(self):
        """
        This method initializes the cache class with a Redis client instance
        """
        self._redis = redis.Redis()
        self._redis.flushdb() # Flush the redis database

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        This function stores data in Redis using a randomly generated key
        """
        key = str(uuid.uuid4()) # Generate a random key
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable[[bytes], any]] = None) -> any:
        """
        This method retrives the value from redis using provided key.
        Returns returieved value, or None if the key does not exist.
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn:
            return fn(value)
        return value
    
    def get_str(self, key: str) -> str:
        """
        This method retrieves a string value from Redis using the provided key
        """
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """
        This method retrieves an integer value from Redis using the provided
        key.
        """
        return self.get(key, int)
