#!/usr/bin/env python3
"""
This module defines a cache class that provides methods to store data using
randomly generated keys.
"""

import redis
import uuid
import functools
from typing import Union, Callable, Optional


class Cache:
    def __init__(self):
        """
        This method initializes the cache class with a Redis client instance
        """
        self._redis = redis.Redis()
        self._redis.flushdb() # Flush the redis database
        self._call_counts = {} # Initializes call counts dictionary

    @functool.lru_cache()
    def __get_keys(self, method: Callable) -> str:
        """
        This method gets the key for the call count of provided method.
        """
        return method.__qualname__

    def count_calls(self, method: Callable) -> Callable:
        """
        Decorator to vount the number of times a method is called
        """
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            key = self.__get_key(method)
            self._redis.incr(key)
            result = method(*args, **kwargs)
            self._call_counts[key] = self._redis.get(key)
            return result
        return wrapper

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

    def get_call_count(self, method: Callable) -> int:
        """
        This method gets the number of times provided method has been called
        """
        key = self.__get_key(method)
        return int(self._call_counts.get(key, 0))

cache = Cache()
cache.store = cache.count_calls(cache.store)
