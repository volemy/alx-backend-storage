#!/usr/bin/env python3
"""
Python script that provides some stats about nginx logs stored in MongoDB
"""
from pymongo import MongoClient


def log_stats():
    """
    This method provides some stats about Nginx logs stored in MongoDB
    """
    Client = MongoClient('mongodb://127.0.0.1:27017')
    Collection = client.logs.nginx

    T_logs = collection.count_documents({})
    print(f"{T_logs} logs")

    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE',]
    print("Methods:")
    for method in methods:
        method_count = collection.count_documents({'method': method})
        print(f"\tmethod {method}: {method_count}"
    
    status_checks = collection.count_documents({'method': 'GET': 'path': '/status'})
    print(f"{status_checks} status check")
