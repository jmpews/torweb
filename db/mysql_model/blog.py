# coding:utf-8
from db.mysql_model import BaseModel

import datetime
from settings.config import config
from peewee import *


class BlogPostCategory(BaseModel):
    """
    blog post category
    """
    name = CharField(verbose_name='title')
    str = CharField(verbose_name='str', unique=True)
    @staticmethod
    def get_by_name(str):
        try:
            cate = BlogPostCategory.get(BlogPostCategory.name==str)
        except BlogPostCategory.DoesNotExist:
            cate = BlogPostCategory.create(name=str, str=str)
        return cate


class BlogPost(BaseModel):
    """
    blog文章
    """
    title = CharField(max_length=71, verbose_name='post的标题')
    slug = CharField(max_length=32, verbose_name='slug站点url')
    category = ForeignKeyField(BlogPostCategory, related_name='posts_category', verbose_name='post的分类')
    content = TextField(verbose_name='md内容')
    create_time = DateTimeField(default=datetime.datetime.now, verbose_name="时间")
    is_del = BooleanField(default=False, verbose_name='逻辑删除')

    @staticmethod
    def get_by_slug(slug):
        try:
            post = BlogPost.get(BlogPost.slug == slug)
        except BlogPost.DoesNotExist:
            return None
        return post

    @staticmethod
    def list_recently(page_limit=config.default_page_limit, page_number=1):
        """
        列出最近文章
        :param page_limit: 默认每页数量
        :param page_number: 当前页
        :return:
        """
        page_number_limit = BlogPost.select().order_by(BlogPost.create_time.desc()).count()
        posts = BlogPost.select().where(BlogPost.is_del == False).order_by(BlogPost.create_time.desc()).paginate(page_number, page_limit)
        return posts, page_number_limit


    @staticmethod
    def list_by_category(category, page_limit=config.default_page_limit, page_number=1):
        """
        根据分类获取当前分类
        :param category: 当前分类
        :param page_limit:
        :param page_number:
        :return:
        """
        page_number_limit = BlogPost.select().where(BlogPost.category == category).order_by(BlogPost.create_time.desc()).count()
        posts = BlogPost.select().where(BlogPost.category == category, BlogPost.is_del == False).order_by(BlogPost.create_time.desc()).paginate(page_number, page_limit)
        return posts, page_number_limit


    @staticmethod
    def list_by_label(label_name, page_limit=config.default_page_limit, page_number=1):
        """
        根据标签获取当前
        :param label: 当前标签
        :param page_limit:
        :param page_number:
        :return:
        """
        page_number_limit = BlogPostLabel.select().where(BlogPostLabel.name == label_name).count()
        labels = BlogPostLabel.select(BlogPostLabel.post).where(BlogPostLabel.name == label_name, BlogPostLabel.is_del == False).paginate(page_number, page_limit)
        posts = []
        for label in labels:
            posts.append(label.post)
        return posts, page_number_limit

class BlogPostLabel(BaseModel):
    name = CharField(verbose_name='标签名')
    post = ForeignKeyField(BlogPost, related_name='labels_post', verbose_name='文章对应标签')
    is_del = BooleanField(default=False, verbose_name='逻辑删除')

    @staticmethod
    def add_post_label(labels, post):
        """
        给post添加标签
        :param labels: ','分割标签
        :param post:
        :return:
        """
        for label in labels.split(','):
            try:
                blogpostlabel = BlogPostLabel.get(BlogPostLabel.name == label, BlogPostLabel.post == post)
                blogpostlabel.is_del = False
                blogpostlabel.save()
            except BlogPostLabel.DoesNotExist:
                tmp = BlogPostLabel.create(name=label,
                                       post=post)
    @staticmethod
    def update_post_label(labels, post):
        """
        删除之前标签,重新添加标签
        :param labels:
        :param post:
        :return:
        """
        q = BlogPostLabel.update(is_del=True).where(BlogPostLabel.post == post)
        q.execute()
        BlogPostLabel.add_post_label(labels, post)

    @staticmethod
    def get_post_label(post):
        """
        获取post的标签
        :param post:
        :return:
        """
        labels = BlogPostLabel.select(BlogPostLabel.name).where(BlogPostLabel.post == post, BlogPostLabel.is_del == False)
        tmp = []
        for label in labels:
            tmp.append(label.name)
        return ','.join(tmp)
