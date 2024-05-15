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

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        This function stores data in Redis using a randomly generated key
        """
        key = str(uuid.uuid4()) # Generate a random key
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable[[bytes], Any]] = None) -> any:
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
    
    def get_str(self, key: str) -> Optional[str]:
        """
        This method retrieves a string value from Redis using the provided key
        """
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_init(self, key: str) -> Optional[int]:
        """
        This method retrieves an integer value from Redis using the provided
        key.
        """
        return self.get(key, int)
