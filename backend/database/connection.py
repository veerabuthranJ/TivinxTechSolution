from pymongo import MongoClient
from django.conf import settings

_client = None
_db = None


def get_client():
    global _client
    if _client is None:
        _client = MongoClient(settings.MONGODB_URI)
    return _client


def get_database():
    global _db
    if _db is None:
        client = get_client()
        _db = client[settings.MONGODB_DATABASE]
    return _db


def get_collection(name):
    return get_database()[name]


def close_connection():
    global _client, _db
    if _client:
        _client.close()
        _client = None
        _db = None
