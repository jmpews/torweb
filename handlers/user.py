# coding:utf-8
import tornado.web
from backend.mysql_model.user import User, Profile
from backend.mysql_model.post import Post, PostReply
from handlers.basehandlers.basehandler import BaseRequestHandler

from utils.util import login_required
from utils.util import get_cleaned_post_data

import config

from utils.common_utils import TimeUtil

class UserProfileHandler(BaseRequestHandler):
    def get(self, user_id, *args, **kwargs):
        userinfo = {}
        user = User.get(User.id == user_id)
        profile = Profile.get_by_user(user)
        posts = Post.select().where(Post.user == user).limit(3)

        userinfo['id'] = user.id
        userinfo['username'] = user.username
        userinfo['website'] = profile.website
        userinfo['nickname'] = profile.nickname
        userinfo['reg_time'] = TimeUtil.datetime_format_date(profile.reg_time)
        userinfo['last_login_time'] = TimeUtil.datetime_format_date(profile.last_login_time)
        userinfo['posts'] = posts
        self.render('profile.html', userinfo=userinfo)

class UserProfileEditHandler(BaseRequestHandler):
    @login_required
    def get(self, *args, **kwargs):
        user = self.current_user
        profile = Profile.get_by_user(user)
        userinfo = {}
        userinfo['username'] = user.username
        userinfo['website'] = profile.website
        userinfo['nickname'] = profile.nickname

        self.render('profile_edit.html', userinfo=userinfo)

    @login_required
    def post(self, *args, **kwargs):
        post_data = get_cleaned_post_data(self, ['nickname', 'website'])
        user = self.current_user
        profile = Profile.get_by_user(user)
        profile.nickname = post_data['nickname']
        profile.website = post_data['website']
        profile.save()
        self.redirect('/user/edit')


class UserAvatarEditHandler(BaseRequestHandler):
    @login_required
    def post(self, *args, **kwargs):
        user = self.current_user
        avatar = self.request.files['avatar'][0]
        avatar_file_name = user.username + '.' + avatar['filename'].split('.')[-1]
        avatar_file = open(config.avatar_upload_path + avatar_file_name, 'wb')
        avatar_file.write(avatar['body'])
        user.avatar = avatar_file_name
        user.save()
        self.redirect('/user/edit')

