#!/usr/bin/env python3
"""
This contains a function that changes all topics of a school document based
on the name.
"""


def update_topics(mongo_collection, name, topics):
    """
    This function changes all topics of a school document on the name
    name(string) will be school name to update and topics will be lists of
    topics approached in the schhol.
    """
    mongo_collection.update_many(
            {'name': name},
            {'$set': {'topics': topics}}
    )
