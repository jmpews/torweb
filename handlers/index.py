# coding:utf-8
import tornado.web
import config
from backend.mysql_model.user import User
from backend.mysql_model.post import Post, PostTopic
from handlers.basehandlers.basehandler import BaseRequestHandler
from handlers.cache import catetopic

from utils.util import json_result
from utils.util import get_cleaned_post_data


class IndexHandler(BaseRequestHandler):
    def get(self, *args, **kwargs):
        posts = Post.list_recently()

        self.render('index.html',
                    posts=posts,
                    catetopic=catetopic,
                    systatus=config.sys_status,
                    current_topic=None)


class IndexTopicHandler(BaseRequestHandler):
    def get(self, topic_id, *args, **kwargs):
        topic = PostTopic.get(PostTopic.str == topic_id)
        posts = Post.list_by_topic(topic)
        self.render('index.html',
                    posts=posts,
                    catetopic=catetopic,
                    systatus=config.sys_status,
                    current_topic=topic)


class RegisterHandler(BaseRequestHandler):
    def get(self, *args, **kwargs):
        if self.current_user:
            self.redirect('/')
        else:
            self.render('register.html')


class LoginHandler(BaseRequestHandler):
    def get(self, *args, **kwargs):
        if self.current_user:
            self.redirect('/')
        else:
            self.render('login.html')

    def post(self, *args, **kwargs):
        post_data = get_cleaned_post_data(self, ['username', 'password'])
        # try:
        #    post_data=get_cleaned_post_data(self,['username','password'])
        # except RequestArgumentError as e:
        #    self.write(json_result(e.code,e.msg))
        #    return
        user = User.auth(post_data['username'], post_data['password'])
        if user:
            self.set_secure_cookie('uuid', user.username)
            result = json_result(0, 'login success!')
            self.redirect('/')
        else:
            result = json_result(-1, 'login failed!')
            self.redirect('/login')
            # write as json
            # self.write(result)
