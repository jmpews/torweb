# coding:utf-8

from db.mysql_model import BaseModel
from settings.config import config
from custor.utils import random_str, TimeUtil

import time, datetime
from hashlib import md5
from peewee import *


class USER_ROLE:
    NORMAL = 1
    ADMIN = 0


class User(BaseModel):
    """
    Base User Model
    """
    ROLE = (
        (0, "administrator"),
    )

    # id = Column(Integer, primary_key=True, autoincrement=True)
    username = CharField(index=True, unique=True, max_length=16)
    nickname = CharField(max_length=16, null=True)
    email = CharField(max_length=32)
    avatar = CharField(max_length=20, null=True)
    theme = CharField(max_length=16, null=True)
    role = IntegerField(choices=ROLE, default=1, verbose_name="user role")
    password = CharField(max_length=32)
    # password salt
    salt = CharField(max_length=64)
    # token
    key = CharField(index=True, max_length=64)
    # user level
    level = IntegerField()

    # default current time
    reg_time = DateTimeField(default=datetime.datetime.now)
    key_time = BigIntegerField()

    def __str__(self):
        return "[%s-%s]" % (self.nickname, self.username)

    def is_admin(self):
        return self.role == USER_ROLE.ADMIN

    def refresh_key(self):
        """refresh token"""
        self.key = random_str(32)
        self.key_time = int(time.time())
        self.save()

    def set_password(self, new_password):
        """set password"""
        salt = random_str()
        password_md5 = md5(new_password.encode('utf-8')).hexdigest()
        password_final = md5((password_md5 + salt).encode('utf-8')).hexdigest()
        self.salt = salt
        self.password = password_final
        self.save()

    @staticmethod
    def new(username, password, email, nickname='', avatar=config.default_avatar):
        """
        new user
        :param username:
        :param password:
        :param email:
        :param nickname: optional
        :param avatar: optional
        :return:
        """
        salt = random_str()
        password_md5 = md5(password.encode('utf-8')).hexdigest()
        password_final = md5((password_md5 + salt).encode('utf-8')).hexdigest()
        level = USER_ROLE.NORMAL
        the_time = int(time.time())
        u = User.create(username=username,
                        nickname=nickname,
                        email=email,
                        avatar=avatar,
                        password=password_final,
                        salt=salt,
                        level=level,
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
        except User.DoesNotExist:
            return None
        else:
            password_md5 = md5(password.encode('utf-8')).hexdigest()
            password_final = md5((password_md5 + u.salt).encode('utf-8')).hexdigest()
            if u.password == password_final:
                return u
            else:
                return False

    @staticmethod
    def exist(username):
        try:
            r = User.get(User.username == username).count() > 0
        except User.DoesNotExist:
            return False
        else:
            return r

    @staticmethod
    def get_by_key(key):
        the_key = str(key or b'', 'utf-8')
        try:
            r = User.get(User.key == the_key)
        except User.DoesNotExist:
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
            return None
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
        """
        get theme cookie, use for change theme
        :param handler:
        :return:
        """
        theme_color = handler.get_cookie('theme', '')
        if theme_color != '':
            return '.' + theme_color
        if self.theme:
            handler.set_cookie('theme', self.theme)
            return '.' + self.theme
        return '.color3'


class Profile(BaseModel):
    """
    User Profile
    """
    user = ForeignKeyField(User, related_name='user_profile')
    nickname = CharField(max_length=16, default="")
    weibo = CharField(max_length=64, default="")
    website = CharField(max_length=64, default="")
    reg_time = DateTimeField(default=datetime.datetime.now)
    last_login_time = DateTimeField(default=datetime.datetime.now)

    @staticmethod
    def get_by_user(user):
        try:
            r = Profile.get(Profile.user == user)
        except DoesNotExist:
            return None
        else:
            return r


class Follower(BaseModel):
    """
    following and follower
    """
    user = ForeignKeyField(User, related_name='who_follow_this')
    follower = ForeignKeyField(User, verbose_name='this_follow_who')
    follow_time = DateTimeField(default=datetime.datetime.now)

    @staticmethod
    def is_follow(user, current_user):
        is_follow = False
        if current_user and user != current_user:
            is_follow = True
            try:
                Follower.get(Follower.user == user, Follower.follower == current_user)
            except Follower.DoesNotExist:
                is_follow = False
        return is_follow


class ChatMessage(BaseModel):
    """
    chat messsage

    @sender: who send the message
    @receiver: the message send to who
    @content: ...
    @is_read: ...
    @time: ...
    """
    sender = ForeignKeyField(User, related_name='sender')
    receiver = ForeignKeyField(User, related_name='receiver')
    content = TextField(verbose_name='chat-content')
    is_read = BooleanField(default=False)
    time = DateTimeField(default=datetime.datetime.now)

    @staticmethod
    def get_recent_chat_message(current_user, other):
        """
        get the recent message between `current_user` and `other`
        :param current_user:
        :param other:
        :return:
        """
        result = {}
        result['name'] = other.username
        result['id'] = other.id
        result['avatar'] = other.avatar
        result['msg'] = ChatMessage.get_unread_message(current_user, other)
        result['msg'] = []

        recent_messages = (ChatMessage.select().where(((ChatMessage.sender == current_user) & (ChatMessage.receiver == other)) | ((ChatMessage.sender == other) & (ChatMessage.receiver == current_user))).order_by(ChatMessage.time).limit(10))
        for msg in recent_messages:
            d = '>' if msg.sender == current_user else '<'
            result['msg'].append([d, msg.content, TimeUtil.datetime_delta(msg.time)])
        return result

    @staticmethod
    def get_unread_message(current_user, other):
        """
        get the unread message between `current_user` and `other`
        :param current_user:
        :param other:
        :return:
        """
        tmp = []
        unread_messages = ChatMessage.select().where(ChatMessage.receiver == current_user,
                                                     ChatMessage.sender == other,
                                                     ChatMessage.is_read == False
                                                     ).order_by(ChatMessage.time)
        for msg in unread_messages:
            tmp.append(['<',msg.content, TimeUtil.datetime_delta(msg.time)])
        return tmp

    @staticmethod
    def get_recent_user_list(current_user):
        """
        get the recent user who chat with `current_user`
        :param current_user:
        :return:
        """
        recent_user_list = {}

        user_id_list = []
        recent_user_list['user_id_list'] = user_id_list

        tmp_recent_user_list = []

        one_day_ago = TimeUtil.get_ago(60*60*24*10*10)

        ol = ChatMessage.select(ChatMessage.sender, ChatMessage.receiver).where(((ChatMessage.sender == current_user) | (ChatMessage.receiver == current_user)) & (ChatMessage.time > one_day_ago)).group_by(ChatMessage.sender, ChatMessage.receiver).limit(10)

        for u in ol:
            if u.sender == current_user:
                other = u.receiver
            else:
                other = u.sender

            if other.id in user_id_list:
                continue

            user_id_list.append(other.id)
            unread_count = ChatMessage.select().where(ChatMessage.sender == u.sender,
                                                      ChatMessage.receiver == u.receiver).count()

            recent_user_list[other.id] = {}
            recent_user_list[other.id]['other_name'] = other.username
            recent_user_list[other.id]['other_id'] = other.id
            recent_user_list[other.id]['other_avatar'] = other.avatar

            tmp_recent_user_list.append({
                'id': other.id,
                'avatar': other.avatar,
                'name': other.username
            })

        recent_user_list['user_id_list'] = user_id_list

        return tmp_recent_user_list

