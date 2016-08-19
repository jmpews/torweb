import config

from pymongo import MongoClient

client = MongoClient(config.BACKEND_MONGO)
DB_mongo = client[config.APP_NAME]
