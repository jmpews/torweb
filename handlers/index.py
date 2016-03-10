# coding:utf-8

from backend.mongo_db.session import session
from handlers.basehandlers.otherhandler import Adv_BaseRequestHandler
from handlers.basehandlers.basehandler import BaseRequestHandler


class IndexHandler(BaseRequestHandler):

    @session
    def get(self, *args, **kwargs):
        #self.redirect('static/index.html')
        self.session['key']='jmpews_key'
        self.render('index.html')

class Index2Handler(Adv_BaseRequestHandler):

    def get(self, *args, **kwargs):
        #self.redirect('static/index.html')
        self.session['key']='jmpews_key'
        self.render('index.html')

