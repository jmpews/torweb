# coding:utf-8
import tornado.web
from backend.mysql_model.user import User
from backend.mysql_model.post import Post, PostReply
from handlers.basehandlers.basehandler import BaseRequestHandler

from utils.util import login_required
from utils.util import get_cleaned_post_data


# 帖子详情
class UserProfileHandler(BaseRequestHandler):
    def get(self, user_id, *args, **kwargs):
        userinfo = {}
        user = User.get(User.id==user_id)
        userinfo['username'] = user.username

        self.render('profile.html')

