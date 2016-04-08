import config
from backend.mongo_db import DB_mongo
import datetime
class CommentDB():
    '''
    微信后台comment记录
    '''
    _collection=DB_mongo['comment']
    @classmethod
    def add_comment(cls,openid,content):
        cls._collection.update({'openid':openid},{'$push':{'content':{'txt':content,'time':datetime.datetime.now()}}},upsert=True)


