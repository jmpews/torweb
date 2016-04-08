import config
from backend.mongo_db import DB_mongo

from utils.util import random_str

import functools

class BaseSession(dict):
    '''
    session字典存储
    '''

    def __init__(self,session_id,data):
        self._session_id=session_id
        self.data=data
        super(BaseSession, self).__init__()

    def get_session_id(self):
        return self._session_id

    def __missing__(self):
        return None


class MongoSessionManager():
    '''
    在纠结到底是使用类方法,还是实例方法
    '''
    _collection=DB_mongo['session']

    def __init__(self,collection_name='sessions'):
        self._collection=DB_mongo[collection_name]

    @staticmethod
    def generate_session_id():
        return random_str(16)

    # 创建session
    @classmethod
    def new_session(cls,session_id=None,data=None):
        if not data:
            data={}
        if not session_id:
            session_id= cls.generate_session_id()
        cls._collection.save({'_id':session_id,'data':data})
        return BaseSession(session_id,{})

    # 读取session,不存在返回None
    @classmethod
    def load_session(cls,session_id= None):
        data={}
        if session_id:
            session_data=cls._collection.find({'_id':session_id})
            if session_data:
                data = session_data['data']
                return BaseSession(session_id,data)
        return None

    # 更新session
    @classmethod
    def update_session(cls,session_id,data):
        cls._collection.update({'_id':session_id},{'$set':{'data':data}})

    # 从request读取session,不存在则创建
    @classmethod
    def load_session_from_request(cls,handler):
        s = MongoSessionManager.load_session(handler.get_secure_cookie('session_id',''))
        if s:
            return s
        else:
            s = MongoSessionManager.new_session(handler.get_secure_cookie('session_id',''))
            handler.set_secure_cookie('session_id',s.get_session_id())
            return s

# session语法糖
def session(request):
    @functools.wraps(request)
    def _func(handler,*args, **kwargs):
        s = MongoSessionManager.load_session_from_request(handler)
        setattr(handler,'session',s.data)
        return_val = request(handler, *args, **kwargs)
        MongoSessionManager.update_session(s.get_session_id(),s.data)
        return return_val
    return _func
