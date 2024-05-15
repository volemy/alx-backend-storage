#!/usr/bin/env/ python3
"""
This module implements the get_page function.
"""

import redis
import requests
from functools import wraps


# connect redis
r = redis.Redis(decode_responses=True)


def count_url_acess(func):
    """
    Decorator function with a count
    """
    @wraps(func)
    def wrapper(url):
        count_key = f"count:{url}"
        r.incr(count_key)
        return func(url)
    return wrapper


def cache_response(func):
    """
    Decorator to cache the result of the get page function.
    """
    @wraps(func)
    def wrapper(url):
        cache_key = f"cache:{url}"
        cached_data = r.get(cache_key)
        if cached_data:
            return cached_data

        result = func(url)
        if isinstance(result, (bytes, bytearray)):
            result = result.decode('utf-8')
        r.setex(cache_key, 10, result)
        return result
    return wrapper


@count_url_access
@cache_response
def get_page(url: str) -> str:
    """
    This function fetches HTML content of a particular url and returns it.
    """
    response = requests.get(url)
    return response.text
