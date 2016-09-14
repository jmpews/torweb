# coding:utf-8
from db.mysql_model import BaseModel

import datetime
from settings.config import config
from peewee import *


class BlogPostCategory(BaseModel):
    name = CharField(verbose_name='标题')
    str = CharField(verbose_name='str', unique=True)
    @staticmethod
    def get_by_name(str):
        try:
            cate = BlogPostCategory.get(BlogPostCategory.name==str)
        except BlogPostCategory.DoesNotExist:
            cate = BlogPostCategory.create(name=str, str=str)
        return cate


class BlogPost(BaseModel):
    title = CharField(max_length=71, verbose_name='post的标题')
    category = ForeignKeyField(BlogPostCategory, related_name='posts_category', verbose_name='post的分类')
    content = TextField(verbose_name='md内容')
    create_time = DateTimeField(default=datetime.datetime.now, verbose_name="时间")
    is_del = BooleanField(default=False, verbose_name='逻辑删除')


    @staticmethod
    def list_recently(page_limit=config.default_page_limit, page_number=1):
        page_number_limit = BlogPost.select().order_by(BlogPost.create_time).count()
        posts = BlogPost.select().where(BlogPost.is_del == False).order_by(BlogPost.create_time).paginate(page_number, page_limit)
        return posts, page_number_limit


    @staticmethod
    def list_by_topic(category, page_limit=config.default_page_limit, page_number=1):
        page_number_limit = BlogPost.select().where(BlogPost.category == category).order_by(BlogPost.create_time).count()
        posts = BlogPost.select().where(BlogPost.category == category, BlogPost.is_del == False).order_by(BlogPost.create_time).paginate(page_number, page_limit)
        return posts, page_number_limit

class BlogPostLabel(BaseModel):
    name = CharField(verbose_name='标签名')
    post = ForeignKeyField(BlogPostCategory, related_name='labels_post', verbose_name='文章对应标签')
    is_del = BooleanField(default=False, verbose_name='逻辑删除')

    @staticmethod
    def add_post_label(labels, post):
        for label in labels.split(','):
            tmp = BlogPostLabel.create(name=label,
                                       post=post)
    @staticmethod
    def update_post_label(labels, post):
        BlogPostLabel.update(is_del=True).where(BlogPostLabel.post == post)
        BlogPostLabel.update_post_label(labels, post)
