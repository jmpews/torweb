from backend.mongo_db.session import session, MongoSessionManager
from backend.mongo_db.server_status import ServerStatus

from backend.redis_db.utils import RateLimit

from .basehandler import BaseRequestHandler
import json

'''
主要包含一些高级的handler
'''

class Adv_BaseRequestHandler(BaseRequestHandler):
    '''
    mongo:记录url、session
    增加了url访问记录
    增加session,形成一个session属性进行调用,在finish时进行更新
    '''
    def __init__(self,application,request,**kwargs):
        BaseRequestHandler.__init__(self,application,request,**kwargs)
        self._session=None

    def prepare(self):
        # 增加
        self.url_count=ServerStatus.visitor_url_up(self.request.path)

    @property
    def session(self):
        if not self._session:
            self._session=MongoSessionManager.load_session_from_request(self)
        return self._session

    def on_finish(self):
        if self._session:
            MongoSessionManager.update_session(self._session.get_session_id(),self._session)

class Rate_BaseRequestHandler(BaseRequestHandler):
    '''
    redis:记录访问频率
    增加ip访问频率控制
    '''
    def __init__(self,application,request,**kwargs):
        RequestHandler.__init__(self,application,request,**kwargs)
        self._session=None

    def prepare(self):
        # 如果是获取socket上ip在nginx下是不可行的。
        if 'X-Real-IP' in self.request.headers:
            ip=self.request.headers['X-Real-IP']
        else:
            ip=self.request.remote_ip
        ttl=RateLimit.ratelimit(ip)
        if ttl:
            self.write(json.dumps({'error':True,'txt':'访问频率过快,请在'+str(ttl)+'秒后尝试!'}))
            self.finish()


