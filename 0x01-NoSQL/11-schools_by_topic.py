#!/usr/bin/env python3
"""
This function returns the list of school having specific topic
"""


def schools_by_topic(mongo_collection, topic):
    """
    This function returns a list of school documents with specific topic
    with topic(string) topic to be searched
    """
    Sch = mongo_collection.find({'topics': topic})
    return Sch
