# coding:utf-8
import datetime
from .user import User
from backend.mysql_model import BaseModel
from peewee import *

from utils.common_utils import TimeUtil


class Post(BaseModel):
    CATEGORY = (
        (0, '漏洞研究'),
        (1, 'Web安全'),
        (2, '开发模式'),
    )
    category = IntegerField(choices=CATEGORY, default=2, verbose_name="帖子类别")
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

    def get_category(self):
        for c in Post.CATEGORY:
            if c[0] == self.category:
                return c[1]

    def up_collect(self):
        self.collect_count += 1
        self.save()

    def up_visit(self):
        self.visit_count += 1
        self.save()

    def up_reply(self, user='test'):
        self.reply_time = datetime.datetime.now()
        self.reply_count += 1
        self.save()

    @staticmethod
    def list_recently(num=10):
        posts = Post.select().order_by(Post.reply_time).limit(10)
        result = []
        for post in posts:
            result.append({
                'id': post.id,
                'category': post.get_category(),
                'title': post.title,
                'username': post.user.username,
                'create_time': TimeUtil.datetime_delta(post.create_time),
                'reply_time': TimeUtil.datetime_delta(post.reply_time),
                'visit_count': post.visit_count,
                'reply_count': post.reply_count,
                'collect_count': post.collect_count
            })
        return result

    def detail(self):
        result = {}
        result['title'] = self.title
        result['content'] = self.content
        result['category'] = self.get_category()
        result['username'] = self.user.username
        result['create_time'] = TimeUtil.datetime_delta(self.create_time),
        result['reply_time'] = TimeUtil.datetime_delta(self.reply_time),
        result['visit_count'] = self.visit_count
        result['reply_count'] = self.reply_count
        result['collect_count'] = self.collect_count
        return result


class PostReply(BaseModel):
    post = ForeignKeyField(Post, verbose_name="对应帖子")
    user = ForeignKeyField(User, verbose_name="回复者")
    content = TextField(verbose_name="回复内容")
    create_time = DateTimeField(default=datetime.datetime.now, verbose_name="回复时间")
    like_count = IntegerField(default=0, verbose_name="赞同数")

    def __str__(self):
        return "[%s-%s]" % (self.user, self.content)

    def up_like(self):
        self.like_count += 1
        self.save()

    @staticmethod
    def list_all(post):
        result = []
        postreplys = PostReply.select().where(PostReply.post == post)
        for reply in postreplys:
            result.append({
                'username': reply.user.username,
                'content': reply.content,
                'create_time': TimeUtil.datetime_delta(reply.create_time),
                'like_count': reply.like_count
            })
        return result
