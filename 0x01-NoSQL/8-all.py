#!/usr/bin/env python3
"""
This lists all documents in a collection
"""


def list_all(mongo_collection):
    """
    This method lists all documents in a MongoDB collection and returns,
    list of documents or an empty list if no doc are found
    """
    docs = mongo_collection.find()
    return [doc for doc in docs] 
