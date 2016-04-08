# coding:utf-8
import sys
import time
from hashlib import md5
from backend.mysql_model import BaseModel, DBSession
from sqlalchemy import Column, Integer, BigInteger, String, Float, ForeignKey, Boolean,DateTime, func, VARCHAR
from utils.util import random_str



class USER_LEVEL:
    BAN = 0
    NORMAL = 10
    ADMIN = 100


class User(BaseModel):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(VARCHAR(16), index=True)
    password = Column(VARCHAR(32))
    # 密码加盐
    salt = Column(VARCHAR(64))
    # token
    key = Column(VARCHAR(64), index=True)
    # 用户等级
    level = Column(Integer)

    # default current time
    reg_time = Column(DateTime,default=func.now())
    key_time = Column(BigInteger)

    __tablename__ = 'users'

    def is_admin(self):
        return self.level == USER_LEVEL.ADMIN

    # 刷新token和时间
    def refresh_key(self):
        session = DBSession()
        self.key = random_str(32)
        self.key_time = int(time.time())
        session.add(self)
        session.commit()
        session.close()


    # 设置密码
    def set_password(self, new_password):
        salt = random_str()
        password_md5 = md5(new_password.encode('utf-8')).hexdigest()
        password_final = md5((password_md5 + salt).encode('utf-8')).hexdigest()
        session = DBSession()
        self.salt = salt
        self.password = password_final
        session.add(self)
        session.commit()
        session.close()

    # 创建新的用户
    @classmethod
    def new(cls, username, password):
        salt = random_str()
        password_md5 = md5(password.encode('utf-8')).hexdigest()
        password_final = md5((password_md5 + salt).encode('utf-8')).hexdigest()
        level = USER_LEVEL.ADMIN if cls.count() == 0 else USER_LEVEL.NORMAL  # 首个用户赋予admin权限
        the_time = int(time.time())
        session = DBSession()
        ret = User(username=username, password=password_final,openid=openid , salt=salt, level=level, key=random_str(32),
                          key_time = the_time, )
        session.add(ret)
        session.commit()
        session.close()
        return ret

    @classmethod
    def password_change(cls, username, password, new_password):
        u = cls.auth(username, password)
        if u:
            u.set_password(new_password)
            u.refresh_key()
            return u

    @classmethod
    def auth(cls, username, password):
        session = DBSession()
        u = session.query(cls).filter(cls.username==username).first()
        session.close()
        if not u:
            return False
        password_md5 = md5(password.encode('utf-8')).hexdigest()
        password_final = md5((password_md5 + u.salt).encode('utf-8')).hexdigest()

        if u.password == password_final:
            return u

    @classmethod
    def exist(cls, username):
        session = DBSession()
        r = session.query(cls).filter(cls.username==username).count() > 0
        session.close()
        return r

    @classmethod
    def get_by_key(cls, key):
        session = DBSession()
        the_key = str(key or b'', 'utf-8')
        r = session.query(cls).filter(cls.key==the_key).first()
        session.close()

    @classmethod
    def get_by_username(cls, username):
        session = DBSession()
        r = session.query(cls).filter(cls.username==username).first()
        session.close()
        return r

    @classmethod
    def count(cls):
        session = DBSession()
        r = session.query(cls).filter(cls.level>0).count()
        return r
