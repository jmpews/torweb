# coding:utf-8
from db.mysql_model import BaseModel
from db.mysql_model.user import User, Follower
from db.mysql_model.post import Post, PostReply

import datetime
from peewee import *


class Notification(BaseModel):
    ROLE = (
        (0, "administrator"),
    )
    opt = {
        'new-post': '1',
        'new-reply': '2'
    }
    user = ForeignKeyField(User, verbose_name="user", related_name="notification_user")
    opt = IntegerField(choices=ROLE, default=1, verbose_name="操作类型")
    msg = CharField(max_length=71)
    extra_user = ForeignKeyField(User, null=True, verbose_name="user", related_name="post")
    extra_post = ForeignKeyField(Post, null=True, verbose_name="post", related_name="reply")
    extra_post_reply = ForeignKeyField(PostReply, null=True, verbose_name="postreply", related_name="reply")
    create_time = DateTimeField(default=datetime.datetime.now, verbose_name="时间")
    is_read = BooleanField(default=False)

    @staticmethod
    def new_post(post):
        followers = Follower.select(Follower.follower).where(Follower.user == post.user)
        for follower in followers:
            Notification.create(user=follower.follower,
                                opt=1,
                                msg='发表新文章',
                                extra_user=post.user,
                                extra_post=post
                                )

    @staticmethod
    def new_reply(postreply, post):
        followers = Follower.select(Follower.follower).where(Follower.user == postreply.user)
        for follower in followers:
            Notification.create(user=follower.follower,
                                opt=2,
                                msg='发表新评论',
                                extra_user=postreply.user,
                                extra_post=post,
                                extra_post_reply=postreply,
                                )
