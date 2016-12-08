# coding:utf-8
from app.cache import hot_post_cache, system_status_cache, topic_category_cache

from custor.handlers.basehandler import BaseRequestHandler
from custor.decorators import timeit, exception_deal, check_captcha
from custor.utils import get_cleaned_post_data, get_cleaned_query_data
from custor.utils import json_result, get_page_nav, get_page_number

from db.mysql_model.post import Post, PostTopic
from db.mysql_model.user import User

from custor.errors import RequestMissArgumentError, PageNotFoundError

from settings.language import MSG

from .utils import get_index_info, get_topic_index_info, get_index_user_info
import greenado

class IndexHandler(BaseRequestHandler):
    """
    index html
    """
    # time profile
    @greenado.groutine
    @timeit
    # exception capture
    @exception_deal([RequestMissArgumentError,]) # 也许这个参数有其他用处先留着
    def get(self, *args, **kwargs):
        # profiling 性能分析
        # from profiling.tracing import TracingProfiler
        #
        # # profile your program.
        # profiler = TracingProfiler()
        # profiler.start()
        current_page = get_cleaned_query_data(self, ['page',], blank=True)['page']
        posts, top_posts, pages = get_index_info(current_page)
        self.render('index/index.html',
                    index_user_info=get_index_user_info(self.current_user),
                    posts=posts,
                    top_posts = top_posts,
                    topic_category_cache=topic_category_cache,
                    hot_post_cache=hot_post_cache,
                    systatus=system_status_cache,
                    current_topic=None,
                    pages=pages,
                    pages_prefix_url='/?page=')

        # profiler.stop()
        # profiler.run_viewer()


class IndexTopicHandler(BaseRequestHandler):
    """
    topic index
    """
    @greenado.groutine
    def get(self, topic_id, *args, **kwargs):
        current_page = get_cleaned_query_data(self, ['page',], blank=True)['page']
        topic, posts, top_posts, pages = get_topic_index_info(topic_id, current_page)
        self.render('index/index.html',
                    index_user_info=get_index_user_info(self.current_user),
                    posts=posts,
                    top_posts=top_posts,
                    topic_category_cache=topic_category_cache,
                    hot_post_cache=hot_post_cache,
                    systatus=system_status_cache,
                    current_topic=topic,
                    pages=pages,
                    pages_prefix_url='/topic/'+topic.str+'?page=')


class RegisterHandler(BaseRequestHandler):
    """
    user register
    """
    @greenado.groutine
    def get(self, *args, **kwargs):
        if self.current_user:
            self.redirect('/')
        else:
            self.render('index/register.html')

    def post(self, *args, **kwargs):
        post_data = get_cleaned_post_data(self, ['username', 'email', 'password'])
        if User.get_by_username(username=post_data['username']):
            self.write(json_result(1, MSG.str('register_same_name')))
            return

        if User.get_by_email(email=post_data['email']):
            self.write(json_result(1, MSG.str('register_same_email')))
            return

        user = User.new(username=post_data['username'],
                 email=post_data['email'],
                 password=post_data['password'])
        self.write(json_result(0,{'username': user.username}))

class LoginHandler(BaseRequestHandler):
    """
    user login
    """
    @greenado.groutine
    def get(self, *args, **kwargs):
        if self.current_user:
            self.redirect('/')
        else:
            self.render('index/login.html')

    @greenado.groutine
    @timeit
    @exception_deal([RequestMissArgumentError,]) # 也许这个参数有其他用处先留着
    @check_captcha(-4, MSG.str('login_captcha_error')) # 检查验证码,返回(错误码, 错误信息)
    def post(self, *args, **kwargs):
        post_data = get_cleaned_post_data(self, ['username', 'password'])
        user = User.auth(post_data['username'], post_data['password'])
        if user:
            # self.set_secure_cookie('uuid', user.username)
            self.set_current_user(user.username)
            result = json_result(0, 'login success!')
        else:
            result = json_result(-1, MSG.str('login_password_error'))
        self.write(result)

class LogoutHandler(BaseRequestHandler):
    """
    user logout
    """
    @greenado.groutine
    def get(self, *args, **kwargs):
        if self.current_user:
            self.clear_cookie('uuid')
        self.redirect('/')
