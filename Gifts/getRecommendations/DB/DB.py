from pymongo import MongoClient

def get_client():
    client = MongoClient('localhost', 27017)
    return client