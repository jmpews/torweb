# coding:utf-8
import tornado.websocket
from settings.config import config

from custor.handlers.basehandler import BaseRequestHandler, BaseWebsocketHandler
from custor.decorators import login_required_json, login_required, ppeewwee
from custor.utils import get_cleaned_post_data, get_cleaned_json_data, json_result, get_cleaned_json_data_websocket, TimeUtil
from custor.logger import logger

from db.mysql_model.common import Notification
from db.mysql_model.post import Post, PostReply, CollectPost
from db.mysql_model.user import User, Profile, Follower, ChatLog


class UserProfileHandler(BaseRequestHandler):
    """
    用户资料页面
    """
    def get(self, user_id, *args, **kwargs):
        user = User.get(User.id == user_id)
        profile = Profile.get_by_user(user)
        posts = Post.select().where(Post.user == user).limit(10)
        postreplys = PostReply.select().where(PostReply.user == user).limit(10)
        collectposts = CollectPost.select().where(CollectPost.user == user).limit(10)
        # 是否显示关注
        is_follow = True if Follower.is_follow(user, self.current_user) else False
        is_online = True if WebsocketChatHandler.is_online(user.username) else False
        print(WebsocketChatHandler.is_online(user.username))
        self.render('user/profile.html',
                    user=user,
                    profile=profile,
                    posts=posts,
                    postreplys=postreplys,
                    is_follow=is_follow,
                    is_online=is_online,
                    collectposts=collectposts)

class UserProfileEditHandler(BaseRequestHandler):
    """
    用户资料编辑页面
    """
    @login_required
    def get(self, *args, **kwargs):
        user = self.current_user
        profile = Profile.get_by_user(user)
        userinfo = {}
        userinfo['username'] = user.username
        userinfo['weibo'] = profile.weibo
        self.render('user/profile_edit.html', userinfo=userinfo)

    @login_required
    def post(self, *args, **kwargs):
        post_data = get_cleaned_post_data(self, ['weibo',])
        user = self.current_user
        profile = Profile.get_by_user(user)
        profile.weibo = post_data['weibo']
        profile.save()
        self.write(json_result(0, {'user': user.username}))


class UserAvatarEditHandler(BaseRequestHandler):
    """
    用户头像编辑处理
    """
    @login_required
    def post(self, *args, **kwargs):
        user = self.current_user
        # 上传的文件
        avatar = self.request.files['avatar'][0]
        avatar_file_name = user.username + '.' + avatar['filename'].split('.')[-1]
        avatar_file = open(config.avatar_upload_path + avatar_file_name, 'wb')
        avatar_file.write(avatar['body'])
        user.avatar = avatar_file_name
        user.save()
        self.redirect('/user/edit')

class UserNotificationHandler(BaseRequestHandler):
    """
    用户消息通知页面
    """
    @login_required
    def get(self, *args, **kwargs):
        user = self.current_user
        profile = Profile.get(Profile.user == user)
        notifications = Notification.select().where(Notification.user == user)
        self.render('user/profile_notification.html',
                    profile=profile,
                    notifications=notifications,
                    )

class UserFollowerHandler(BaseRequestHandler):
    """
    用户关注与粉丝页面
    """
    def get(self, user_id, *args, **kwargs):
        user = User.get(User.id == user_id)
        who_follow = Follower.select(Follower.follower).where(Follower.user == user)
        follow_who = Follower.select(Follower.user).where(Follower.follower == user)
        profile = Profile.get_by_user(user)
        is_follow = Follower.is_follow(user, self.current_user)
        self.render('user/profile_follower.html',
                    user=user,
                    profile=profile,
                    who_follow=who_follow,
                    follow_who=follow_who,
                    is_follow=is_follow)

class UserOptHandler(BaseRequestHandler):
    """
    跟用户API相关的操作
    和postreplyopthandelr设计的类似，api模式
    """
    @login_required_json(-3, 'login failed.')
    def post(self, *args, **kwargs):
        json_data = get_cleaned_json_data(self, ['opt', 'data'])
        data = json_data['data']
        opt = json_data['opt']

        # 关注用户
        if opt == 'follow-user':
            try:
                user = User.get(User.id == data['user'])
            except:
                self.write(json_result(1, '没有该用户'))
                return
            Follower.create(user=user, follower=self.current_user)
            self.write(json_result(0, 'success'))

        # 取关用户
        elif opt == 'unfollow-user':
            try:
                user = User.get(User.id == data['user'])
            except:
                self.write(json_result(1, '没有该用户'))
                return
            try:
                f = Follower.get(Follower.user == user, Follower.follower == self.current_user)
            except:
                self.write(json_result(1, '还没有关注他'))
                return
            f.delete_instance()
            self.write(json_result(0, 'success'))

        # 更新头像
        elif opt == 'update-avatar':
            import base64
            avatar = base64.b64decode(data['avatar'])
            user = self.current_user
            avatar_file_name = user.username + '.png'
            avatar_file = open(config.avatar_upload_path + avatar_file_name, 'wb')
            avatar_file.write(avatar)
            user.avatar = avatar_file_name
            user.save()
            self.write(json_result(0, 'success'))

        # 更新社区主题
        elif opt == 'update-theme':
            user = self.current_user
            user.theme = data['theme']
            user.save()
            self.write(json_result(0, 'success'))

        # 获取聊天记录
        elif opt == 'realtime-chat':
            user = self.current_user
            other_id = data['other']
            other = User.get(User.id == other_id)
            result = ChatLog.get_chat_log(user, other)
            self.write(json_result(0, result))

        # 发送消息
        elif opt == 'chat-to' :
            user = self.current_user
            other_id = data['other']
            other = User.get(User.id == other_id)
            content = data['content']
            ChatLog.create(me=user, other=other, content=content)
            self.write(json_result(0, 'success'))
        else:
            self.write(json_result(1, 'opt不支持'))


class WebsocketChatHandler(BaseWebsocketHandler):
    """
    使用websocket的实时聊天

    websocket real-time-chat
    """

    # redis ?
    clients = {}

    def check_origin(self, origin):
        return True

    @ppeewwee
    def open(self, *args, **kwargs):

        user = self.current_user
        if user.username not in WebsocketChatHandler.clients.keys():
            WebsocketChatHandler.clients[user.username] = self

    @ppeewwee
    def on_close(self):
        user = self.current_user

        if user.username in WebsocketChatHandler.clients.keys():
            WebsocketChatHandler.clients.pop(user.username)
        else:
            logger.debug("[{0}] not in Websocket.clients, but close.".format(user.username))

    @staticmethod
    def is_online(username):
        w = WebsocketChatHandler.clients.get(username, False)
        return w

    @ppeewwee
    def on_message(self, message):
        json_data = get_cleaned_json_data_websocket(message, ['opt', 'data'])
        data = json_data['data']
        opt = json_data['opt']
        if opt == 'chat-to':
            user = self.current_user
            # 目标用户
            other_id = data['other']
            other = User.get(User.id == other_id)
            content = data['content']
            cl = ChatLog.create(me=user, other=other, content=content)

            # push to [other]
            other_websocket = WebsocketChatHandler.is_online(other.username)
            if other_websocket:
                # <
                other_websocket.write_message(json_result(0, {'user_id': user.id, 'data': ['<', cl.content, TimeUtil.datetime_delta(cl.time)]}))
                # >
                self.write_message(json_result(1, {'user_id': other.id, 'data': ['>', cl.content, TimeUtil.datetime_delta(cl.time)]}))
            else:
                self.write_message(json_result(2, 'success.'))

        else:
            self.write_message(json_result(-1, 'not support opt.'))
