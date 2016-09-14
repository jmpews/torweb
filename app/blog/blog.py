# coding:utf-8
from custor.handlers.basehandler import BaseRequestHandler
from custor.utils import json_result, get_cleaned_post_data, get_cleaned_query_data, get_page_number, get_page_nav
from settings.config import config

from db.mysql_model.blog import BlogPost, BlogPostLabel

from db.mysql_model.blog import BlogPostCategory, BlogPostLabel, BlogPost

class BlogIndexHandler(BaseRequestHandler):
    def get(self, *args, **kwargs):
        current_page = get_cleaned_query_data(self, ['page',], blank=True)['page']
        current_page = get_page_number(current_page)
        posts, page_number_limit = BlogPost.list_recently(page_number=current_page)
        pages = get_page_nav(current_page, page_number_limit, config.default_page_limit)
        self.render('blog/index.html',
                    posts=posts)

class BlogPostDetailHandler(BaseRequestHandler):
    def get(self, post_id, *args, **kwargs):
        post = BlogPost.get(BlogPost.id == post_id)
        self.render('blog/post-detail.html',
                    post=post)

class BlogPostAddHandler(BaseRequestHandler):
    def post(self, *args, **kwargs):
        post_data = get_cleaned_post_data(self, ['title', 'category', 'label', 'content'])
        cate = BlogPostCategory.get_by_name(post_data['category'])
        post = BlogPost.create(title=post_data['title'],
                                   category=cate,
                                   content=post_data['content'])
        BlogPostLabel.add_post_label(post_data['lable'], post)
        self.write(json_result(0, {'post': post.id}))

class BlogPostModifyHandler(BaseRequestHandler):
    def post(self, *args, **kwargs):
        post_id = get_cleaned_post_data(self, ['blogpost'])['blogpost']
        post_data = get_cleaned_post_data(self, ['title', 'category', 'label', 'content'])
        post = BlogPost.get(BlogPost.id == post_id, BlogPost.is_del != 0)
        cate = BlogPostCategory.get_by_name(post_data['category'])
        post.category = cate
        post.title = post_data['title']
        post.content = post_data['content']
        post.save()
        BlogPostLabel.update_post_label(post_data['label'], post)
        self.write(json_result(0, {'post': post.id}))

class BlogPostDeleteHandler(BaseRequestHandler):
    def post(self, *args, **kwargs):
        post_id = get_cleaned_post_data(self, ['blogpost'])['blogpost']
        post = BlogPost.get(BlogPost.id == post_id, BlogPost.is_del != 0)
        post.is_del = True
        post.save()
        self.write(json_result(0, {'post': post.id}))
