from db.mongo_db.session import session, MongoSessionManager
from db.mongo_db.server_status import ServerStatus

from .basehandler import BaseRequestHandler

'''
主要包含一些高级的handler
'''


class Adv_BaseRequestHandler(BaseRequestHandler):
    '''
    mongo:记录url、session
    增加了url访问记录
    增加session,形成一个session属性进行调用,在finish时进行更新
    '''

    def __init__(self, application, request, **kwargs):
        BaseRequestHandler.__init__(self, application, request, **kwargs)
        self._session = None

    def prepare(self):
        # 增加
        self.url_count = ServerStatus.visitor_url_up(self.request.path)

    @property
    def session(self):
        if not self._session:
            self._session = MongoSessionManager.load_session_from_request(self)
        return self._session

    def on_finish(self):
        if self._session:
            MongoSessionManager.update_session(self._session.get_session_id(), self._session)


