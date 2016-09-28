# coding:utf-8
import time, datetime
from hashlib import md5
from db.mysql_model import BaseModel
from settings.config import config
from peewee import *
from custor.utils import random_str, TimeUtil


class USER_LEVEL:
    BAN = 0
    NORMAL = 10
    ADMIN = 100


class User(BaseModel):
    ROLE = (
        (0, "administrator"),
    )

    # id = Column(Integer, primary_key=True, autoincrement=True)
    username = CharField(index=True, unique=True, max_length=16)
    nickname = CharField(max_length=16, null=True)
    email = CharField(max_length=32)
    avatar = CharField(max_length=20, null=True)
    theme = CharField(max_length=16, null=True)
    role = IntegerField(choices=ROLE, default=1, verbose_name="用户角色")
    password = CharField(max_length=32)
    # 密码加盐
    salt = CharField(max_length=64)
    # token
    key = CharField(index=True, max_length=64)
    # 用户等级
    level = IntegerField()

    # default current time
    reg_time = DateTimeField(default=datetime.datetime.now)
    key_time = BigIntegerField()

    def __str__(self):
        return "[%s-%s]" % (self.nickname, self.username)

    def is_admin(self):
        return self.level == USER_LEVEL.ADMIN

    # 刷新token和时间
    def refresh_key(self):
        self.key = random_str(32)
        self.key_time = int(time.time())
        self.save()

    # 设置密码
    def set_password(self, new_password):
        salt = random_str()
        password_md5 = md5(new_password.encode('utf-8')).hexdigest()
        password_final = md5((password_md5 + salt).encode('utf-8')).hexdigest()
        self.salt = salt
        self.password = password_final
        self.save()

    # 创建新的用户
    @staticmethod
    def new(username, password, email, nickname='', avatar=config.default_avatar):
        salt = random_str()
        password_md5 = md5(password.encode('utf-8')).hexdigest()
        password_final = md5((password_md5 + salt).encode('utf-8')).hexdigest()
        level = USER_LEVEL.NORMAL  # 首个用户赋予admin权限
        the_time = int(time.time())
        u = User.create(username=username,
                        nickname=nickname,
                        email=email,
                        avatar=avatar,
                        password=password_final,
                        salt=salt, level=level,
                        key=random_str(32),
                        key_time=the_time)
        u.save()
        p = Profile.create(user=u)
        p.save()
        return u

    @staticmethod
    def password_change(username, password, new_password):
        u = User.auth(username, password)
        if u:
            u.set_password(new_password)
            u.refresh_key()
            return u
        return False

    @staticmethod
    def auth(username, password):
        try:
            u = User.get(User.username == username)
        except DoesNotExist:
            return False
        else:
            password_md5 = md5(password.encode('utf-8')).hexdigest()
            password_final = md5((password_md5 + u.salt).encode('utf-8')).hexdigest()
            if u.password == password_final:
                return u
        return False

    @staticmethod
    def exist(username):
        try:
            r = User.get(User.username == username).count() > 0
        except DoesNotExist:
            return False
        else:
            return r

    @staticmethod
    def get_by_key(key):
        the_key = str(key or b'', 'utf-8')
        try:
            r = User.get(User.key == the_key)
        except DoesNotExist:
            return None
        else:
            return r

    @staticmethod
    def get_by_username(username):
        try:
            r = User.get(User.username == username)
        except DoesNotExist:
            return None
        else:
            return r

    @staticmethod
    def get_by_email(email):
        try:
            r = User.get(User.email == email)
        except DoesNotExist:
            return False
        else:
            return r

    @staticmethod
    def count():
        try:
            r = User.select().where(User.level > 0).count()
        except DoesNotExist:
            return 0
        else:
            return r

    def get_theme_by_cookie_user(self, handler):
        theme_color = handler.get_cookie('theme', '')
        if theme_color != '':
            return '.' + theme_color
        if self.theme:
            handler.set_cookie('theme', self.theme)
            return '.' + self.theme
        return '.color3'



class Profile(BaseModel):
    user = ForeignKeyField(User, related_name='user_profile')
    nickname = CharField(max_length=16, default="")
    weibo = CharField(max_length=64, default="")
    website = CharField(max_length=64, default="")
    reg_time = DateTimeField(default=datetime.datetime.now)
    last_login_time = DateTimeField(default=datetime.datetime.now)

    def get_by_user(user):
        try:
            r = Profile.get(Profile.user == user)
        except DoesNotExist:
            return False
        else:
            return r


class Follower(BaseModel):
    user = ForeignKeyField(User, related_name='who_follow_this')
    follower = ForeignKeyField(User, verbose_name='this_follow_who')
    follow_time = DateTimeField(default=datetime.datetime.now)

    @staticmethod
    def is_follow(user, current_user):
        is_follow = None
        if current_user and user != current_user:
            is_follow = True
            try:
                Follower.get(Follower.user == user, Follower.follower == current_user)
            except Follower.DoesNotExist:
                is_follow = False
        return is_follow


class ChatLog(BaseModel):
    me = ForeignKeyField(User, related_name='who-send')
    other = ForeignKeyField(User, related_name='send-who')
    content = TextField(verbose_name='chat-content')
    time = DateTimeField(default=datetime.datetime.now)

    @staticmethod
    def get_chat_log(me, other):
        '''
        获取双方对话的聊天记录
        :param self:
        :param other:
        :return:
        '''
        result = {'me': '', 'other': '', 'logs': []}
        result['me'] = me.username
        result['other'] = other.username
        result['me_avatar'] = me.avatar
        result['other_avatar'] = other.avatar
        # import pdb;pdb.set_trace()

        # () 注意需要全包
        chatlogs = (ChatLog.select().where(((ChatLog.me == me) & (ChatLog.other == other)) | ((ChatLog.me == other) & (ChatLog.other == me))).order_by(ChatLog.time.desc()).limit(10))
        for cl in chatlogs:
            d = '>' if cl.me == me else '<'
            result['logs'].append([d, cl.content, TimeUtil.datetime_delta(cl.time)])
        return result
