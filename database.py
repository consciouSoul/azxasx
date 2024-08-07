from pymongo import MongoClient


class Database:
    def __init__(self, MONGO_URI: str, db_name: str):
        self.db = MongoClient(MONGO_URI)[db_name]

    def getCollection(self, collection: str):
        return self.db[collection]

    def insertOne(self, collection: str, data: dict):
        return self.db[collection].insert_one(data)

    def findOne(self, collection: str, query: dict):
        return self.db[collection].find_one(query)

    def find(self, collection: str, query: dict):
        return [i for i in self.db[collection].find(query)]

    def update(self, collection: str, query: dict, data: dict):
        return self.db[collection].update_one(query, {"$set": data}, upsert=True)
