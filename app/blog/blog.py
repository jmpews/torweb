# coding:utf-8
from custor.handlers.basehandler import BaseRequestHandler
from custor.utils import json_result, get_cleaned_post_data, get_cleaned_query_data, get_page_number, get_page_nav, get_cleaned_json_data
from settings.config import config

from db.mysql_model.blog import BlogPostCategory, BlogPostLabel, BlogPost
import markdown
from peewee import *
# from markdown2 import Markdown
# markdowner = Markdown(extras=['fenced-code-blocks', 'code-friendly'])

class BlogIndexHandler(BaseRequestHandler):
    def get(self, *args, **kwargs):
        current_page = get_cleaned_query_data(self, ['page',], blank=True)['page']
        current_page = get_page_number(current_page)
        posts, page_number_limit = BlogPost.list_recently(page_number=current_page)
        for post in posts:
            post.labels = BlogPostLabel.get_post_label(post)
        pages = get_page_nav(current_page, page_number_limit, config.default_page_limit)

        # 使用到联合、分组等查询
        # select category_id, blogpostcategory.name, count(blogpost.id) from blogpost inner join blogpostcategory on blogpost.category_id=blogpostcategory.id group by category_id;
        categorys = BlogPost.select(BlogPostCategory.name, fn.COUNT(BlogPost.id).alias('count'))\
            .join(BlogPostCategory, on=(BlogPostCategory.id == BlogPost.category))\
            .group_by(BlogPost.category)
        for category in categorys:
            category.name = category.category.name

        labels = BlogPostLabel.select(BlogPostLabel.name, fn.COUNT(BlogPostLabel.post).alias('count')).where(BlogPostLabel.is_del == False).group_by(BlogPostLabel.name)
        self.render('blog/index.html',
                    posts=posts,
                    labels=labels,
                    categorys=categorys,
                    pages=pages,
                    pages_prefix_url = '/blog?page=')

class BlogIndexCategoryHandler(BaseRequestHandler):
    def get(self, category_name, *args, **kwargs):
        try:
            category = BlogPostCategory.get(BlogPostCategory.name == category_name)
        except BlogPostCategory.DoesNotExist:
            self.redirect("/static/404.html")
            return
        current_page = get_cleaned_query_data(self, ['page',], blank=True)['page']
        current_page = get_page_number(current_page)
        posts, page_number_limit = BlogPost.list_by_category(category, page_number=current_page)
        for post in posts:
            post.labels = BlogPostLabel.get_post_label(post)
        pages = get_page_nav(current_page, page_number_limit, config.default_page_limit)

        # 使用到联合、分组等查询
        # select category_id, blogpostcategory.name, count(blogpost.id) from blogpost inner join blogpostcategory on blogpost.category_id=blogpostcategory.id group by category_id;
        categorys = BlogPost.select(BlogPostCategory.name, fn.COUNT(BlogPost.id).alias('count'))\
            .join(BlogPostCategory, on=(BlogPostCategory.id == BlogPost.category))\
            .group_by(BlogPost.category)
        for category in categorys:
            category.name = category.category.name

        labels = BlogPostLabel.select(BlogPostLabel.name, fn.COUNT(BlogPostLabel.post).alias('count')).where(BlogPostLabel.is_del == False).group_by(BlogPostLabel.name)
        self.render('blog/index.html',
                    posts=posts,
                    labels=labels,
                    categorys=categorys,
                    pages=pages,
                    pages_prefix_url = '/blog/categoray/'+category_name+'?page=')

class BlogIndexLabelHandler(BaseRequestHandler):
    def get(self, label_name, *args, **kwargs):
        current_page = get_cleaned_query_data(self, ['page',], blank=True)['page']
        current_page = get_page_number(current_page)
        posts, page_number_limit = BlogPost.list_by_label(label_name, page_number=current_page)
        for post in posts:
            post.labels = BlogPostLabel.get_post_label(post)
        pages = get_page_nav(current_page, page_number_limit, config.default_page_limit)
        categorys = BlogPostCategory.select()
        labels = BlogPostLabel.select().where(BlogPostLabel.is_del == False)
        self.render('blog/index.html',
                    posts=posts,
                    labels=labels,
                    categorys=categorys,
                    pages=pages,
                    pages_prefix_url = '/blog/label/'+ label_name+'?page=')

class BlogPostDetailHandler(BaseRequestHandler):
    def get(self, post_id, *args, **kwargs):

        post = BlogPost.get(BlogPost.id == post_id)
        # post.content_html = markdowner.convert(post.content)
        post.content_html = markdown.markdown(post.content, extensions=['markdown.extensions.fenced_code', ])
        post.category_name = post.category.name
        post.labels  = BlogPostLabel.get_post_label(post)
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
        post = BlogPost.get(BlogPost.id == post_id, BlogPost.is_del == False)
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
        post = BlogPost.get(BlogPost.id == post_id, BlogPost.is_del == False)
        post.is_del = True
        post.save()
        self.write(json_result(0, {'post': post.id}))

class BlogPostOptHandler(BaseRequestHandler):
    def get(self, *args, **kwargs):
        posts = BlogPost.select()
        tmp = []
        for post in posts:
            post.labels = BlogPostLabel.get_post_label(post)
            post.category_name = post.category.name
        self.render('blog/post-opt.html',
                    posts=posts)
    def post(self, *args, **kwargs):
        json_data = get_cleaned_json_data(self, ['opt', 'data'])
        data = json_data['data']
        opt = json_data['opt']
        if opt == 'get-post':
            try:
                post = BlogPost.get(BlogPost.id == int(data['post']), BlogPost.is_del == False)
            except:
                self.write(json_result(1, '不存在该post'))
                return
            else:
                self.write(json_result(0, {'title': post.title,
                               'content': post.content,
                               'labels': BlogPostLabel.get_post_label(post),
                               'category': post.category.name}))
                return
        elif opt == 'update-post':
            try:
                post = BlogPost.get(BlogPost.id == int(data['post']), BlogPost.is_del == False)
            except:
                self.write(json_result(1, '不存在该post'))
                return
            else:
                cate = BlogPostCategory.get_by_name(data['category'])
                post.category = cate
                post.title = data['title']
                post.content = data['content']
                post.save()
                BlogPostLabel.update_post_label(data['labels'], post)
                self.write(json_result(0, 'success'))
                return
        elif opt == 'create-post':
            cate = BlogPostCategory.get_by_name(data['category'])
            post = BlogPost.create(title=data['title'],
                                   category=cate,
                                   content=data['content'])
            BlogPostLabel.add_post_label(data['labels'], post)
            self.write(json_result(0, 'success'))
            return
        else:
            self.write(json_result(1, 'opt不支持'))