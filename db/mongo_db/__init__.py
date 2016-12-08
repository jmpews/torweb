# coding:utf-8

from settings.config import config
import motor.motor_tornado

# from pymongo import MongoClient
# client = MongoClient(config.BACKEND_MONGO['host'], config.BACKEND_MONGO['port'])
client = motor.motor_tornado.MotorClient(config.BACKEND_MONGO['host'], config.BACKEND_MONGO['port'])
DB_mongo = client[config.APP_NAME]
