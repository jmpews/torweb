# coding:utf-8
import tornado.web
from backend.mysql_model.user import User, Profile
from backend.mysql_model.common import Notification
from backend.mysql_model.post import Post, PostReply, CollectPost
from handlers.basehandlers.basehandler import BaseRequestHandler

from utils.util import login_required
from utils.util import get_cleaned_post_data

import config


class UserProfileHandler(BaseRequestHandler):
    def get(self, user_id, *args, **kwargs):
        user = User.get(User.id == user_id)
        profile = Profile.get_by_user(user)
        posts = Post.select().where(Post.user == user).limit(10)
        postreplys = PostReply.select().where(PostReply.user == user).limit(10)
        collectposts = CollectPost.select().where(CollectPost.user == user).limit(10)

        self.render('profile.html',
                    user=user,
                    profile=profile,
                    posts=posts,
                    postreplys=postreplys,
                    collectposts=collectposts)

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

class UserNotificationHandler(BaseRequestHandler):
    @login_required
    def get(self, *args, **kwargs):
        user = self.current_user
        profile = Profile.get(Profile.user == user)
        notifications = Notification.select().where(Notification.user == user)
        self.render('profile_notification.html',
                    profile=profile,
                    notifications=notifications,
                    )

class UserFollowerHandler(BaseRequestHandler):
    def get(self, *args, **kwargs):
        pass

