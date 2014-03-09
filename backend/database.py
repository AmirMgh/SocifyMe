#simple driver to connect to mongo
from pymongo import MongoClient

def connect_to_mong():
    db = MongoClient().ar
    return db
