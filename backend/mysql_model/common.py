# coding:utf-8
from backend.mysql_model import BaseModel
from peewee import *


class Notification(BaseModel):
    ROLE = (
        (0, "administrator"),
    )

    user = ForeignKeyField(User, verbose_name="user")
    opt = IntegerField(choices=ROLE, default=1, verbose_name="操作类型")
    msg = CharField(max_length=71)
    extra_user = ForeignKeyField(User, verbose_name="user")
    extra_post = ForeignKeyField(Post, verbose_name="post")
    is_read = BooleanField(default=False)
