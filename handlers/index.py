# coding:utf-8

#from backend.mongo_db.session import session
#from handlers.basehandlers.otherhandler import Adv_BaseReuqestHandler
from handlers.basehandlers.basehandler import BaseRequestHandler


class IndexHandler(BaseRequestHandler):

    #@session
    def get(self, *args, **kwargs):
        #self.redirect('static/index.html')
        self.render('index.html')


    def post(self, *args, **kwargs):
        #sessions=MongoSessionManager.load_session_request(self)
        #sessions['test']='test_load'
        #MongoSessionManager.update_session(sessions.get_session_id(),sessions)
        #self.write('test')
        pass
