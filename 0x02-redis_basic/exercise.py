#!/usr/bin/env python3
"""
This module defines a cache class that provides methods to store data using
randomly generated keys.
"""

import redis
import uuid
import functools import wraps
from typing import Union, Callable, Optional, Any


def count_calls(method: Callable) -> Callable:
    """
    Decorator that takes a single argument and returns a callable
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ wrapper function"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs 
    """
    input_key = method.__qualname__ + ":inputs"
    output_key = method.__qualname__ + ":outputs"

    @wraps(method)
    def wrapper(self, *args) -> bytes:
        """ wrapper function"""

        self._redis.rpush(input_key, str(args))
        output = method(self, *args)
        self._redis.rpush(output_key, (output)
        return output
    return wrapper


def replay(method: Callable) -> None:
    """
    This method displays the history of calls of a particular function
    """
    method_name = method.__qualname__
    cache = redis.Redis()

    Call = cache.get(method_name).decode("utf-8")


    inputs = self._redis.lrange(method_name + ":inputs", 0, -1)
    outputs = self._redis.lrange(method_name + ":outputs", 0, -1)

    print(f"{method_name} was called {call} times:")

    for input_data, output_data in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(name,
              input_data.decode('utf-8'), output_data.decode('utf-8)))


class Cache:
    """
    Method class  for storing and retrieving data
    """

    def __init__(self):
        """
        This method initializes the cache class with a Redis client instance
        """
        self._redis = redis.Redis()
        self._redis.flushdb() # Flush the redis database
    
    @count_calls
    @call_history
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
