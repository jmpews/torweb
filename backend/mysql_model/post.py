# coding:utf-8
import datetime
from .user import User
from backend.mysql_model import BaseModel
from peewee import *


class Post(BaseModel):
    title = CharField(verbose_name="帖子的标题")
    content = TextField(verbose_name="帖子内容")
    user = ForeignKeyField(User, verbose_name="发帖人")
    create_time = DateTimeField(default=datetime.datetime.now, verbose_name="发帖时间")
    reply_time = DateTimeField(default=datetime.datetime.now, verbose_name="回复时间")
    visit_count = IntegerField(default=1, verbose_name="帖子浏览数")
    reply_count = IntegerField(default=0, verbose_name="帖子回复数")
    collect_count = IntegerField(default=0, verbose_name="赞同数")

    def __str__(self):
        return "[%s-%s]" % (self.title, self.user)

    def up_collect(self):
        self.collect_count+=1
        self.save()

    def up_visit(self):
        self.visit_count+=1
        self.save()

    def up_reply(self,user='test'):
        self.reply_time = datetime.datetime.now()
        self.reply_count+=1
        self.save()


class PostReply(BaseModel):
    post = ForeignKeyField(Post, verbose_name="对应帖子")
    user = ForeignKeyField(User, verbose_name="回复者")
    content = TextField(verbose_name="回复内容")
    create_time = DateTimeField(default=datetime.datetime.now, verbose_name="回复时间")
    like_count = IntegerField(default=0, verbose_name="赞同数")

    def __str__(self):
        return "[%s-%s]" % (self.user, self.content)

    def up_like(self):
        self.like_count+=1
        self.save()
