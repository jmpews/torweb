# coding:utf-8
from backend.mysql_model import BaseModel
from backend.mysql_model.user import User
from backend.mysql_model.post import Post, PostReply
from peewee import *


class Notification(BaseModel):
    ROLE = (
        (0, "administrator"),
    )

    user = ForeignKeyField(User, verbose_name="user", related_name="user")
    opt = IntegerField(choices=ROLE, default=1, verbose_name="操作类型")
    msg = CharField(max_length=71)
    extra_user = ForeignKeyField(User, verbose_name="user", related_name="post")
    extra_post = ForeignKeyField(Post, verbose_name="post", related_name="reply")
    extra_post_reply = ForeignKeyField(PostReply, verbose_name="postreply", related_name="reply")
    is_read = BooleanField(default=False)
