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


class ChatMessage(BaseModel):
    """
    A,B,C 都给D发送消息。 D有三种状态。 1. D在线 2. D不在线 3。 断线后重新连接

    对于D,需要针对这三种情况做处理
    """
    sender = ForeignKeyField(User, related_name='sender')
    receiver = ForeignKeyField(User, related_name='receiver')
    content = TextField(verbose_name='chat-content')
    is_read = BooleanField(default=False)
    time = DateTimeField(default=datetime.datetime.now)

    @staticmethod
    def get_recent_chat_message(current_user, other):
        '''
        获取双方对话的聊天记录
        :param userA:
        :param userB:
        :return:
        '''
        result = {}
        result['me_name'] = current_user.username
        result['me_avatar'] = current_user.avatar
        result['other_name'] = other.username
        result['other_id'] = other.id
        result['other_avatar'] = other.avatar
        result['unread_msg'] = ChatMessage.get_unread_message(current_user, other)
        result['msg'] = []
        # import pdb;pdb.set_trace()

        # () 注意需要全包
        recent_messages = (ChatMessage.select().where(((ChatMessage.sender == current_user) & (ChatMessage.receiver == other)) | ((ChatMessage.sender == other) & (ChatMessage.receiver == current_user))).order_by(ChatMessage.time).limit(10))
        for msg in recent_messages:
            d = '>' if msg.sender == current_user else '<'
            result['msg'].append([d, msg.content, TimeUtil.datetime_delta(msg.time)])
            result['update_time'] = str(msg.time)
        return result

    @staticmethod
    def get_unread_message(current_user, other):
        tmp = []
        unread_messages = ChatMessage.select().where(ChatMessage.receiver == current_user, ChatMessage.sender==other, ChatMessage.is_read == False).order_by(ChatMessage.time)
        for msg in unread_messages:
            tmp.append(['<',msg.content, TimeUtil.datetime_delta(msg.time)])
        return tmp

    @staticmethod
    def get_recent_user_list(current_user):
        '''
        获取所有未读的消息(都是发送给我的)
        :param me:
        :return:
        '''
        recent_user_list = {}
        recent_message = ChatMessage.select().where(ChatMessage.receiver == current_user, ChatMessage.is_read == False).order_by(ChatMessage.time)
        for msg in recent_message:
            sender = msg.sender
            if sender.id not in recent_user_list.keys():
                recent_user_list[sender.id]={}
                recent_user_list[sender.id]['other_name'] = sender.username
                recent_user_list[sender.id]['other_id'] = sender.id
                recent_user_list[sender.id]['other_avatar'] = sender.avatar
                recent_user_list[sender.id]['msg'] = []
            recent_user_list[sender.id]['msg'].append(['<', msg.content, TimeUtil.datetime_delta(msg.time)])
            recent_user_list[sender.id]['update_time'] = str(msg.time)
        return recent_user_list

