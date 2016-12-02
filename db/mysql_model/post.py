# coding:utf-8
import datetime
from .user import User
from db.mysql_model import BaseModel
from peewee import *

from settings.config import config


class PostCategory(BaseModel):
    """
    class
    """
    name = CharField(verbose_name='name')
    str = CharField(unique=True, verbose_name='str')


class PostTopic(BaseModel):
    """
    sub class
    """
    category = ForeignKeyField(PostCategory, related_name='topics_category', null=True)
    name = CharField(verbose_name='name')
    str = CharField(unique=True, verbose_name='str')
    hot = BooleanField(default=False, verbose_name='hot topic')


class Post(BaseModel):
    """
    post
    """
    AUTH_READ = 0
    AUTH_MODIFY = 1
    AUTH_DELETE = 2
    AUTH_ALL = 3
    topic = ForeignKeyField(PostTopic, related_name='posts_topic')
    title = CharField(verbose_name='post-title')
    content = TextField(verbose_name='post-content')
    user = ForeignKeyField(User, verbose_name='who post this')
    create_time = DateTimeField(default=datetime.datetime.now, verbose_name='post-time')

    latest_reply_user = ForeignKeyField(User, null=True, related_name="reply_user", verbose_name='rt')
    latest_reply_time = DateTimeField(null=True, verbose_name='rt')

    visit_count = IntegerField(default=1, verbose_name='rt')
    reply_count = IntegerField(default=0, verbose_name='rt')
    collect_count = IntegerField(default=0, verbose_name='rt')

    top = BooleanField(default=False, verbose_name='top')
    essence = BooleanField(default=False, verbose_name='rt')

    is_delete = BooleanField(default=False, verbose_name='rt')

    def __str__(self):
        return "[%s-%s]" % (self.title, self.user)

    def logic_delete(self):
        self.is_delete = True
        self.save()

    def check_auth(self, user):
        if user.is_admin() or self.check_own(user):
            return True
        return False

    def check_own(self, user):
        if user and self.user == user:
            return True
        else:
            return False

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
    def list_top():
        """
        get top posts
        :return:
        """
        top_posts = Post.select().where(Post.top == True, Post.is_delete == False)
        top_posts_count = top_posts.count()
        return top_posts, top_posts_count

    @staticmethod
    def list_recently(page_limit=config.default_page_limit, page_number=1):
        """
        get recent posts
        :param page_limit: result num in per page
        :param page_number: current page number
        :return:
        """
        page_number_limit = Post.select().where(Post.is_delete == False).order_by(Post.latest_reply_time.desc()).count()
        posts = Post.select().where(Post.is_delete == False).order_by(Post.latest_reply_time.desc()).paginate(page_number, page_limit)
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
        """
        get recent posts of specific topic
        :param topic:
        :param page_limit:
        :param page_number:
        :return:
        """
        page_number_limit = Post.select().where(Post.topic == topic, Post.is_delete == False).order_by(Post.latest_reply_time.desc()).count()
        posts = Post.select().where(Post.topic == topic, Post.is_delete == False).order_by(Post.latest_reply_time.desc()).paginate(page_number, page_limit)
        return posts, page_number_limit

    def detail(self):
        """
        get post detail
        :return:
        """
        result = {}
        user = self.user
        result['title'] = self.title
        result['content'] = self.content
        result['topic'] = self.topic.name
        result['username'] = user.username
        result['nickname'] = user.nickname
        result['avatar'] = user.avatar
        result['create_time'] = self.create_time,
        result['visit_count'] = self.visit_count
        result['reply_count'] = self.reply_count
        result['collect_count'] = self.collect_count
        return result

    @staticmethod
    def get_detail_and_replys(post_id):
        """
        get post's detail and replys
        :param post_id:
        :return:
        """
        try:
            post = Post.get(Post.id == post_id, Post.is_delete == False)
        except Post.DoesNotExist:
            return None, None
        post.up_visit()
        post_replys = PostReply.list_all(post)
        return post, post_replys

    @staticmethod
    def get_by_id(post_id):
        """
        get post by id
        :param post_id:
        :return:
        """
        try:
            post = Post.get(Post.id == post_id, Post.is_delete == False)
        except Post.DoesNotExist:
            return None
        return post



class PostReply(BaseModel):
    """
    PostReply
    """
    post = ForeignKeyField(Post, verbose_name='post')
    user = ForeignKeyField(User, verbose_name='who reply this')
    content = TextField(verbose_name='content')
    create_time = DateTimeField(default=datetime.datetime.now, verbose_name='reply time')
    like_count = IntegerField(default=0, verbose_name='count of like')

    def __str__(self):
        return "[%s-%s]" % (self.user, self.content)

    def up_like(self):
        self.like_count += 1
        self.save()

    @staticmethod
    def list_all(post):
        postreplys = PostReply.select().where(PostReply.post == post)
        return postreplys


class CollectPost(BaseModel):
    """
    collect post
    """
    post = ForeignKeyField(Post, verbose_name='post')
    user = ForeignKeyField(User, verbose_name='who collect this')
    collect_time = DateTimeField(default=datetime.datetime.now, verbose_name='collect time')

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
