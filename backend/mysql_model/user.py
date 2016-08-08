# coding:utf-8
import time, datetime
from hashlib import md5
from backend.mysql_model import BaseModel
from peewee import *
from utils.util import random_str


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
    nickname = CharField(max_length=16)
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
    def new(username, nickname, password):
        salt = random_str()
        password_md5 = md5(password.encode('utf-8')).hexdigest()
        password_final = md5((password_md5 + salt).encode('utf-8')).hexdigest()
        level = USER_LEVEL.NORMAL  # 首个用户赋予admin权限
        the_time = int(time.time())
        u = User.create(username=username, nickname=nickname, password=password_final, salt=salt, level=level,
                          key=random_str(32), key_time=the_time, )
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


class Profile(BaseModel):
    user = ForeignKeyField(User, related_name='user_profile')
    nickname = CharField(max_length=16, default="")
    weibo = CharField(max_length=16, default="")
    website = CharField(max_length=16, default="")
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
    follow = ForeignKeyField(User, verbose_name='this_follow_who')
    follow_time = DateTimeField(default=datetime.datetime.now)

