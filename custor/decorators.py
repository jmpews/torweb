# encoding:utf-8

import functools
import urllib.parse
import time
from tornado.concurrent import Future
from tornado.httpclient import HTTPError

from custor.utils import ColorPrint, get_cleaned_post_data, json_result, ThreadWorker
from custor.errors import RequestMissArgumentError, PageNotFoundError
from db.mysql_model import db_mysql


def run_with_thread_future(*args, **kwargs):
    """
    future with thread
    http://jmpews.github.io/posts/tornado-future-ioloop-yield.html
    :param args:
    :param kwargs:
    :return:
    """
    def wraps_func(func):
        @functools.wraps(func)
        def wraps_args(*args, **kwargs):
            future = Future()
            work = ThreadWorker(future, func, *args, **kwargs)
            work.start()
            return future
        return wraps_args
    return wraps_func


def exception_deal(exceptions):
    """
    catch `get` and `post` Exception
    捕获get, post函数异常
    :param exceptions:
    :return:
    """
    def wrapper_func(func):
        @functools.wraps(func)
        def wrapper_args(handler, *args, **kwargs):
            try:
                func(handler, *args, **kwargs)
            except Exception as ex:
                if isinstance(ex, PageNotFoundError):
                    handler.redirect(ex.redirect_url)
                elif isinstance(ex, RequestMissArgumentError):
                    handler.write(ex.msg)
                else:
                    raise ex
                # for e in exceptions:
                #     if isinstance(ex, e):
                #         handler.write('oh, catch exp in the args list...\n')
        return wrapper_args
    return wrapper_func


def timeit(func):
    """
    profile function cost
    :param func:
    :return:
    """
    def wrapper(*args, **kwargs):
        start = time.clock()
        func(*args, **kwargs)
        end = time.clock()
        # ColorPrint.print('> Profiler: '+func.__qualname__+'used: '+str((end - start) * 1e6) + 'us')
        ColorPrint.print("> Profiler: ["+func.__qualname__+"] used: "+str((end - start)) + "us")
    return wrapper


def check_captcha(errorcode, result):
    """
    check captcha. (attention @decorator order!)
    :param errorcode:
    :param result:
    :return:
    """
    def wrap_func(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            captcha_cookie = self.get_cookie('captcha', '')
            captcha = get_cleaned_post_data(self, ['captcha'], blank=True)['captcha']
            if not captcha or captcha != captcha_cookie:
                self.write(json_result(errorcode, result))
                return
            return method(self, *args, **kwargs)
        return wrapper
    return wrap_func


def login_required(method):
    """
    from "tornado.web.authenticated"
    `self.current_user`是一个@property
    :param method:
    :return:
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            if self.request.method in ("GET", "HEAD"):
                url = self.get_login_url()
                if "?" not in url:
                    if urllib.parse.urlsplit(url).scheme:
                        # if login url is absolute, make next absolute too
                        next_url = self.request.full_url()
                    else:
                        next_url = self.request.uri
                    url += "?" + urllib.parse.urlencode(dict(next=next_url))
                self.redirect(url)
                return
            raise HTTPError(403)
        return method(self, *args, **kwargs)

    return wrapper


def login_required_json(errorcode, result):
    """
    same as `login_required` but return json
    :param errorcode:
    :param result:
    :return:
    """
    def wrap_func(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            if not self.current_user:
                self.write(json_result(errorcode, result))
                return
            return method(self, *args, **kwargs)
        return wrapper
    return wrap_func


def ppeewwee(method):
    """
    peewee hook, connect before request ,release after done.
    :param method:
    :return:
    """
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        db_mysql.connect()
        method(*args, **kwargs)
        if not db_mysql.is_closed():
            db_mysql.close()
    return wrapper
