# coding:utf-8

from settings.config import config
from db.mongo_db import DB_mongo

from custor.utils import random_str

import functools
import asyncio
import tornado.web
import greenado
from tornado.web import gen


class BaseSession(dict):
    """
    session store in dict
    """

    def __init__(self, session_id, data):
        self._session_id = session_id
        self.data = data
        super(BaseSession, self).__init__()

    def get_session_id(self):
        return self._session_id

    def __missing__(self):
        return None


class MongoSessionManager():
    """
    session manager
    """
    _collection = DB_mongo['session']

    def __init__(self, collection_name='sessions'):
        self._collection = DB_mongo[collection_name]

    @staticmethod
    def generate_session_id():
        return random_str(16)

    @classmethod
    def new_session(cls, session_id=None, data=None):
        """
        new session
        :param session_id:
        :param data:
        :return:
        """
        if not data:
            data = {}
        if not session_id:
            session_id = cls.generate_session_id()
        greenado.gyield(cls._collection.save({'_id': session_id, 'data': data}))
        # import pdb;pdb.set_trace()
        return BaseSession(session_id, {})


    @classmethod
    def load_session(cls, session_id=None):
        """
        load session
        :param session_id:
        :return:
        """
        data = {}
        if session_id:
            session_data = greenado.gyield(cls._collection.find_one({'_id': session_id}))
            if session_data:
                data = session_data['data']
                return BaseSession(session_id, data)
        future = tornado.web.Future()
        future.set_result(None)
        result = greenado.gyield(future)
        return result

    @classmethod
    def update_session(cls, session_id, data):
        greenado.gyield(cls._collection.update({'_id': session_id}, {'$set': {'data': data}}))

    @classmethod
    def load_session_from_request(cls, handler):
        session_id = handler.get_secure_cookie('session_id', None)
        if session_id:
            session_id = session_id.decode()
        s = MongoSessionManager.load_session(session_id)
        if s is not None:
            return s
        else:
            s = MongoSessionManager.new_session()
            handler.set_secure_cookie('session_id', s.get_session_id())
            return s


def session(request):
    @functools.wraps(request)
    def _func(handler, *args, **kwargs):
        s = MongoSessionManager.load_session_from_request(handler)
        setattr(handler, 'session', s.data)
        return_val = request(handler, *args, **kwargs)
        MongoSessionManager.update_session(s.get_session_id(), s.data)
        return return_val

    return _func
