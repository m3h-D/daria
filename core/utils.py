import os
from pymongo import MongoClient


class MongoHelper:
    def __init__(self, db_name=None):
        self.client = MongoClient(os.getenv("MONGO_HOST"))
        self.db = self.client[db_name or os.getenv("MONGODB_NAME")]
        
    def collection(self, collection_name):
        return self.db[collection_name]