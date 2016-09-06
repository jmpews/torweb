#encoding:utf-8
from custor.utils import set_api_header, json_result, ThreadWorker
from custor.errors import RequestMissArgumentError, PageNotFoundError
from custor.logger import logger

from settings.config import config
from custor.utils import ColorPrint

from db.mysql_model import db_mysql
from db.mysql_model.user import User

from tornado.web import RequestHandler
from tornado.concurrent import Future
import functools
import time


def run_with_future(*args, **kwargs):
    '''
    如何利用future和线程的配合
    http://jmpews.github.io/posts/tornado-future-ioloop-yield.html
    :param args:
    :param kwargs:
    :return:
    '''
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
    '''
    捕获get, post函数异常
    :param exceptions:
    :return:
    '''
    def wrapper_func(func):
        # 保存原函数信息
        @functools.wraps(func)
        def wrapper_args(handler, *args, **kwargs):
            try:
                func(handler, *args, **kwargs)
            except Exception as ex:
                if isinstance(ex, PageNotFoundError):
                    handler.redirect(ex.redirect_url)
                elif isinstance(ex, RequestMissArgumentError):
                    handler.write(ex.msg)
                # for e in exceptions:
                #     if isinstance(ex, e):
                #         handler.write('oh, catch exp in the args list...\n')
        return wrapper_args
    return wrapper_func

def timeit(func):
    '''
    计算函数执行时间
    :param func:
    :return:
    '''
    def wrapper(*args, **kwargs):
        start = time.clock()
        func(*args, **kwargs)
        end = time.clock()
        end = time.clock()
        # ColorPrint.print('> Profiler: '+func.__qualname__+'used: '+str((end - start) * 1e6) + 'us')
        ColorPrint.print('> Profiler: '+func.__qualname__+'used: '+str((end - start)) + 'us')
    return wrapper

class BaseRequestHandler(RequestHandler):
    '''
    Peewee-Request-Hook-Connect
    '''

    def prepare(self):
        db_mysql.connect()
        return super(BaseRequestHandler, self).prepare()

    '''
    重写了异常处理
    '''

    # @exception_deal([RequestMissArgumentError,])
    def get(self, *args, **kwargs):
        # try:
        super(BaseRequestHandler, self).get(*args, **kwargs)
        # except Exception as e:
        #     logger.error(e)

    def write_error(self, status_code, **kwargs):
        if 'exc_info' in kwargs:
            # 参数缺失异常
            if isinstance(kwargs['exc_info'][1], RequestMissArgumentError):
                self.write(json_result(kwargs['exc_info'][1].code, kwargs['exc_info'][1].msg))
                return

        if status_code == 400:
            self.write(json_result(400, '缺少参数'))
            return
        if not config.DEBUG:
            self.redirect("/static/500.html")

    '''
    获取当前用户
    '''

    def get_current_user(self):
        username = self.get_secure_cookie('uuid')
        if not username:
            return None
        user = User.get_by_username(username)
        return user

    '''
    Peewee-Request-Hook-Close
    '''

    def on_finish(self):
        if not db_mysql.is_closed():
            db_mysql.close()
        return super(BaseRequestHandler, self).on_finish()


class ErrorHandler(BaseRequestHandler):
    '''
    默认404处理
    '''

    def prepare(self):
        super(BaseRequestHandler, self).prepare()
        if 'X-Real-IP' in self.request.headers:
            ip = self.request.headers['X-Real-IP']
        else:
            ip = self.request.remote_ip
        logger.error(self.request.uri + "-FROM IP:" + ip)
        self.set_status(404)
        self.redirect("/static/404.html")

    def write_error(self):
        pass
