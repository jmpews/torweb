# coding:utf-8
import config
from handlers.basehandlers.basehandler import BaseRequestHandler



class AnotherHandler(BaseRequestHandler):
    def get(self, *args, **kwargs):
        self.render('another.html')

