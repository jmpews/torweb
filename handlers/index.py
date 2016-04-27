# coding:utf-8
import tornado.web
from backend.mysql_model.user import User
from backend.mysql_model.post import Post
from handlers.basehandlers.basehandler import BaseRequestHandler

from utils.util import json_result
from utils.util import get_cleaned_post_data,RequestArgumentError

class IndexHandler(BaseRequestHandler):

    def get(self, *args, **kwargs):
        posts=Post.list_recently()
        self.render('index.html', posts=posts)

class LoginHandler(BaseRequestHandler):

    def get(self, *args, **kwargs):
        self.render('login.html')

    def post(self, *args, **kwargs):
        post_data=get_cleaned_post_data(self,['username','password'])
        #try:
        #    post_data=get_cleaned_post_data(self,['username','password'])
        #except RequestArgumentError as e:
        #    self.write(json_result(e.code,e.msg))
        #    return
        user=User.auth(post_data['username'],post_data['password'])
        if user:
            self.set_secure_cookie('uuid',user.username)
            result=json_result(0,'login success!')
            self.redirect('/')
        else:
            result=json_result(-1,'login failed!')
            self.redirect('/login')
        # write as json
        #self.write(result)

