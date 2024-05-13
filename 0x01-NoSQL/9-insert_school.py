#!/usr/bin/env python3
"""
This contains a function that inserts a new document in a collection based on
kwargs.
"""


def insert_school(mongo_collection, **kwargs):
    """
    This function inserts a new document into a mongoDB collection
    and returns a new _id of new document
    """
    r = mongo_collection.insert_one(kwargs)
    return r.inserted_id
