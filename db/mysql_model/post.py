# coding:utf-8
import datetime
from .user import User
from db.mysql_model import BaseModel
from peewee import *

from settings.config import config


class PostCategory(BaseModel):
    name = CharField(verbose_name='标题')
    str = CharField(verbose_name='str', unique=True)


class PostTopic(BaseModel):
    category = ForeignKeyField(PostCategory, related_name='topics_category', null=True)
    name = CharField(verbose_name='标题')
    str = CharField(verbose_name='str', unique=True)


class Post(BaseModel):
    topic = ForeignKeyField(PostTopic, related_name='posts_topic')
    title = CharField(verbose_name="帖子的标题")
    content = TextField(verbose_name="帖子内容")
    user = ForeignKeyField(User, verbose_name="发帖人")
    create_time = DateTimeField(default=datetime.datetime.now, verbose_name="发帖时间")
    latest_reply_user = ForeignKeyField(User, null=True, related_name="reply_user", verbose_name="最后回复用户")
    latest_reply_time = DateTimeField(null=True, verbose_name="最近回复时间")
    visit_count = IntegerField(default=1, verbose_name="帖子浏览数")
    reply_count = IntegerField(default=0, verbose_name="帖子回复数")
    collect_count = IntegerField(default=0, verbose_name="赞同数")

    def __str__(self):
        return "[%s-%s]" % (self.title, self.user)

    def up_collect(self):
        self.collect_count += 1
        self.save()

    def up_visit(self):
        self.visit_count += 1
        self.save()

    def update_latest_reply(self, postreply):
        self.latest_reply_user = postreply.user
        self.latest_reply_time = postreply.create_time
        self.reply_count += 1
        self.save()

    @staticmethod
    def list_recently(page_limit=config.default_page_limit, page_number=1):
        page_number_limit = Post.select().order_by(Post.latest_reply_time).count()
        posts = Post.select().order_by(Post.latest_reply_time).paginate(page_number, page_limit)
        # result = []
        # for post in posts:
        #     result.append({
        #         'id': post.id,
        #         'topic': post.topic,
        #         'title': post.title,
        #         'user': post.user,
        #         'create_time': TimeUtil.datetime_delta(post.create_time),
        #         'lastest_reply': post.lastest_reply,
        #         'visit_count': post.visit_count,
        #         'reply_count': post.reply_count,
        #         'collect_count': post.collect_count
        #     })
        return posts, page_number_limit


    @staticmethod
    def list_by_topic(topic, page_limit=config.default_page_limit, page_number=1):
        page_number_limit = Post.select().where(Post.topic == topic).order_by(Post.latest_reply_time).count()
        posts = Post.select().where(Post.topic == topic).order_by(Post.latest_reply_time).paginate(page_number, page_limit)
        return posts, page_number_limit

    def detail(self):
        result = {}
        result['title'] = self.title
        result['content'] = self.content
        result['topic'] = self.topic.name
        result['username'] = self.user.username
        result['nickname'] = self.user.nickname
        result['avatar'] = self.user.avatar
        result['create_time'] = self.create_time,
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

    #  对user进行展开，方便API设计
    # 'user': reply.user 展开为
    # 'username': reply.user.username
    @staticmethod
    def list_all(post):
        postreplys = PostReply.select().where(PostReply.post == post)
        return postreplys


class CollectPost(BaseModel):
    post = ForeignKeyField(Post, verbose_name="对应帖子")
    user = ForeignKeyField(User, verbose_name="收藏者")
    collect_time = DateTimeField(default=datetime.datetime.now, verbose_name="收藏时间")

    @staticmethod
    def is_collect(post, user):
        if not user:
            return False
        try:
            CollectPost.get(CollectPost.post==post, CollectPost.user==user)
        except DoesNotExist:
            return False
        else:
            return True
