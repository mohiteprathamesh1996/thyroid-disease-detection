import pymongo
from thyroid.constant.database import DATABASE_NAME
from thyroid.constant.env_variable import *
import os
import certifi
ca = certifi.where()

class MongoDBClient:
    client = None
    def __init__(self, database_name = DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                MongoDBClient.client = pymongo.MongoClient(
                    MONGO_DB_URL, 
                    tlsCAFile = ca
                    )

            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
        except Exception as e:
            raise e