# coding:utf-8
from custor.handlers.basehandler import BaseRequestHandler



class RecommendHandler(BaseRequestHandler):
    def get(self, *args, **kwargs):
        self.render('recommend/recommend.html')

