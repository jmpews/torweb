#coding:utf-8
from custor.handlers.basehandler import BaseRequestHandler
from custor.utils import json_result, get_cleaned_post_data, get_cleaned_query_data, get_page_number, get_page_nav, get_cleaned_json_data

from settings.config import config

from db.mysql_model.post import Post, PostTopic
from db.mysql_model.user import User

from custor.decorators import login_required_json

def obj2dict(obj, keys):
    tmp = {}
    for k in keys:
        tmp[k] = getattr(obj, k)
    return tmp


class IndexHandler(BaseRequestHandler):
    """
    后台面板首页
    """
    def get(self, *args, **kwargs):
        user_count = User.select().count()
        post_count = Post.select().count()
        self.render('dashboard/pages/index.html',
                    user_count=user_count,
                    post_count=post_count)

class UserIndexHandler(BaseRequestHandler):
    def get(self, *args, **kwargs):
        users = User.select()
        self.render('dashboard/pages/db-user-list.html',
                    users=users)

class PostIndexHandler(BaseRequestHandler):
    def get(self, *args, **kwargs):
        posts = Post.select()
        self.render('dashboard/pages/db-post-list.html',
                    posts=posts)

    # @login_required_json(-3, 'login failed.')
    def post(self, *args, **kwargs):
        json_data = get_cleaned_json_data(self, ['opt', 'data'])
        data = json_data['data']
        opt = json_data['opt']

        # 关注用户
        if opt == 'get-post-list':
            data = []
            posts = Post.select()
            for p in posts:
                tp = obj2dict(p, ['id', 'title'])
                data.append(tp)
            self.write(json_result(0, data))
