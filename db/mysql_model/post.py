# coding:utf-8
import datetime
from .user import User
from db.mysql_model import BaseModel
from peewee import *

from settings.config import config


class PostCategory(BaseModel):
    """
    总分类
    """
    name = CharField(verbose_name='标题')
    str = CharField(unique=True, verbose_name='str')


class PostTopic(BaseModel):
    """
    分类下的主题
    """
    category = ForeignKeyField(PostCategory, related_name='topics_category', null=True)
    name = CharField(verbose_name='标题')
    str = CharField(unique=True, verbose_name='str')
    hot = BooleanField(default=False, verbose_name='热门主题')


class Post(BaseModel):
    AUTH_READ = 0
    AUTH_MODIFY = 1
    AUTH_DELETE = 2
    AUTH_ALL = 3
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

    top = BooleanField(default=False, verbose_name='置顶')
    essence = BooleanField(default=False, verbose_name='精华')

    is_delete = BooleanField(default=False, verbose_name='是否删除')

    def __str__(self):
        return "[%s-%s]" % (self.title, self.user)

    def check_auth(self, user):
        if not user:
            return 1, 0, 0
        elif self.user == user:
            return 1, 1 , 1

    def check_own(self, user):
        if user and self.user == user:
            return True
        else:
            return False

    def up_collect(self):
        '''
        收藏帖子
        :return:
        '''
        self.collect_count += 1
        self.save()

    def up_visit(self):
        '''
        浏览数
        :return:
        '''
        self.visit_count += 1
        self.save()

    def update_latest_reply(self, postreply):
        '''
        更新最近回复
        :param postreply:
        :return:
        '''
        self.latest_reply_user = postreply.user
        self.latest_reply_time = postreply.create_time
        self.reply_count += 1
        self.save()

    @staticmethod
    def list_top():
        '''
        获取指定帖子,可以用trick缓存
        :param self:
        :return:
        '''
        top_posts = Post.select().where(Post.top == True, Post.is_delete == False)
        top_posts_count = top_posts.count()
        return top_posts, top_posts_count

    @staticmethod
    def list_recently(page_limit=config.default_page_limit, page_number=1):
        '''
        列出最近帖子
        :param page_limit: 每一页帖子数量
        :param page_number: 当前页
        :return:
        '''
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
        '''
        列出当前主题下的梯子
        :param topic: 具体主题
        :param page_limit: 每一页帖子数量
        :param page_number: 当前页
        :return:
        '''
        page_number_limit = Post.select().where(Post.topic == topic, Post.is_delete == False).order_by(Post.latest_reply_time.desc()).count()
        posts = Post.select().where(Post.topic == topic, Post.is_delete == False).order_by(Post.latest_reply_time.desc()).paginate(page_number, page_limit)
        return posts, page_number_limit

    def detail(self):
        '''
        获取帖子详情
        :return:
        '''
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

    @staticmethod
    def get_detail_and_replys(post_id):
        try:
            post = Post.get(Post.id == post_id, Post.is_delete == False)
        except Post.DoesNotExist:
            return None, None
        post.up_visit()
        post_replys = PostReply.list_all(post)
        return post, post_replys

    @staticmethod
    def get_detail(post_id):
        try:
            post = Post.get(Post.id == post_id, Post.is_delete == False)
        except Post.DoesNotExist:
            return None
        return post



class PostReply(BaseModel):
    '''
    回复
    '''
    post = ForeignKeyField(Post, verbose_name="对应帖子")
    user = ForeignKeyField(User, verbose_name="回复者")
    content = TextField(verbose_name="回复内容")
    create_time = DateTimeField(default=datetime.datetime.now, verbose_name="回复时间")
    like_count = IntegerField(default=0, verbose_name="赞同数")

    def __str__(self):
        return "[%s-%s]" % (self.user, self.content)

    def up_like(self):
        '''
        赞同
        :return:
        '''
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
    '''
    收藏帖子
    '''
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
