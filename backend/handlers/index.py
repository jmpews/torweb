# coding:utf-8
import tornado.web
import config
from db.mysql_model.user import User
from db.mysql_model.post import Post, PostTopic
from handlers.basehandlers.basehandler import BaseRequestHandler
from handlers.cache import catetopic, cache_hot_post

from utils.util import json_result
from utils.util import get_cleaned_post_data, get_cleaned_query_data

def get_page_nav(current_page, page_number_limit, page_limit=config.default_page_limit):
    # 页导航(cp:当前页, <:前一页, >:后一页)
    # 模型: < cp-2, cp-1, cp, cp+1, cp+2A >
    # 这里如果换成列表存放，在模板里面会好操作一点
    pages = {'cp-2': 0, 'cp-1': 0, 'cp': current_page, 'cp+1': 0, 'cp+2': 0}
    #import pdb; pdb.set_trace()
    if current_page-1 >= 1:
        pages['cp-1'] = current_page-1
    if current_page-2 >= 1:
        pages['cp-2'] = current_page-2

    if (current_page)*page_limit < page_number_limit:
        pages['cp+1'] = current_page+1
    if (current_page+1)*page_limit < page_number_limit:
        pages['cp+2'][1] = current_page+2
    return pages

class IndexHandler(BaseRequestHandler):
    def get(self, *args, **kwargs):
        current_page = get_cleaned_query_data(self, ['page',], blank=True)['page']
        if current_page:
            current_page = int(current_page)
            if current_page < 1:
                self.redirect("/static/404.html")
                return
            posts, page_number_limit = Post.list_recently(page_number=current_page)
        else:
            current_page = 1
            posts, page_number_limit = Post.list_recently()
        if not posts:
            self.redirect("/static/404.html")
            return
        pages = get_page_nav(current_page, page_number_limit)
        self.render('index.html',
                    posts=posts,
                    catetopic=catetopic,
                    cache_hot_post=cache_hot_post,
                    systatus=config.sys_status,
                    current_topic=None,
                    pages=pages,
                    pages_prefix_url='/?page=')


class IndexTopicHandler(BaseRequestHandler):
    def get(self, topic_id, *args, **kwargs):
        try:
            topic = PostTopic.get(PostTopic.str == topic_id)
        except PostTopic.DoesNotExist:
            self.redirect("/static/404.html")
            return
        current_page = get_cleaned_query_data(self, ['page',], blank=True)['page']
        if current_page:
            current_page = int(current_page)
            if current_page < 1:
                self.redirect("/static/404.html")
                return
            posts, page_number_limit = Post.list_by_topic(topic, page_number=current_page)
        else:
            current_page = 1
            posts, page_number_limit = Post.list_by_topic(topic)
        if not posts:
            self.redirect("/static/404.html")
            return
        pages = get_page_nav(current_page, page_number_limit)
        self.render('index.html',
                    posts=posts,
                    catetopic=catetopic,
                    cache_hot_post=cache_hot_post,
                    systatus=config.sys_status,
                    current_topic=topic,
                    pages=pages,
                    pages_prefix_url='/topic/'+topic.str+'?page=')


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
