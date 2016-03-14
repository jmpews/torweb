# coding:utf-8
import tornado.web
import json
from backend.mongo_db.session import session
from backend.mysql_model.user import User
from handlers.basehandlers.basehandler import BaseRequestHandler

from utils.util import set_api_header, json_result
from utils.util import get_cleaned_post_data

class IndexHandler(BaseRequestHandler):

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render('index.html')

class LoginHandler(BaseRequestHandler):

    def get(self, *args, **kwargs):
        self.render('login.html')

    def post(self, *args, **kwargs):
        post_data=get_cleaned_post_data(self,'username','password')
        user=User.auth(post_data['username'],post_data['password'])
        if user:
            self.set_secure_cookie('user',user.username)
            result=json_result(0,'login success!')
        else:
            result=json_result(-1,'login failed!')
        self.write(result)
