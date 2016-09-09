# coding:utf-8

from settings.config import config
from custor.handlers.basehandler import BaseRequestHandler
from custor.utils import get_cleaned_post_data, get_cleaned_json_data, json_result, login_required, login_required_json
from db.mysql_model.common import Notification
from db.mysql_model.post import Post, PostReply, CollectPost
from db.mysql_model.user import User, Profile, Follower


class UserProfileHandler(BaseRequestHandler):
    '''
    用户资料页面
    '''
    def get(self, user_id, *args, **kwargs):
        user = User.get(User.id == user_id)
        profile = Profile.get_by_user(user)
        posts = Post.select().where(Post.user == user).limit(10)
        postreplys = PostReply.select().where(PostReply.user == user).limit(10)
        collectposts = CollectPost.select().where(CollectPost.user == user).limit(10)
        # 是否显示关注
        is_follow = Follower.is_follow(user, self.current_user)

        self.render('user/profile.html',
                    user=user,
                    profile=profile,
                    posts=posts,
                    postreplys=postreplys,
                    is_follow=is_follow,
                    collectposts=collectposts)

class UserProfileEditHandler(BaseRequestHandler):
    '''
    用户资料编辑页面
    '''
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
    '''
    用户头像编辑处理
    '''
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
    ''''
    用户消息通知页面
    '''
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
    '''
    用户关注与粉丝页面
    '''
    def get(self, user_id, *args, **kwargs):
        user = User.get(User.id == user_id)
        who_follow = Follower.select(Follower.follower).where(Follower.user == user)
        follow_who = Follower.select(Follower.user).where(Follower.follower == user)
        print(who_follow, follow_who)
        profile = Profile.get_by_user(user)
        is_follow = Follower.is_follow(user, self.current_user)
        self.render('user/profile_follower.html',
                    user=user,
                    profile=profile,
                    who_follow=who_follow,
                    follow_who=follow_who,
                    is_follow=is_follow)

class UserOptHandler(BaseRequestHandler):
    '''
    跟用户API相关的操作
    和postreplyopthandelr设计的类似，api模式
    '''
    @login_required_json(-3, 'login failed.')
    def post(self, *args, **kwargs):
        # 这个函数有点意思, 一直做参数安全clean
        json_data = get_cleaned_json_data(self, ['opt', 'data'])
        data = json_data['data']
        opt = json_data['opt']
        if opt == 'follow-user':
            try:
                user = User.get(User.id == data['user'])
            except:
                self.write(json_result(1, '没有该用户'))
                return
            Follower.create(user=user, follower=self.current_user)
            self.write(json_result(0, 'success'))
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
        elif opt == 'update-theme':
            user = self.current_user
            user.theme = data['theme']
            user.save()
            self.write(json_result(0, 'success'))
        else:
            self.write(json_result(1, 'opt不支持'))

