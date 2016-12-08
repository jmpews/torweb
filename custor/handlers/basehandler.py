# coding:utf-8
from custor.utils import json_result
from custor.errors import RequestMissArgumentError
from custor.logger import logger

from settings.config import config

from db.mysql_model import db_mysql
from db.mysql_model.user import User
from db.mongo_db.session import MongoSessionManager

from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler

from greenlet import greenlet


class BaseRequestHandler(RequestHandler):
    """
    base handler
    """
    def redirect404(self):
        self.redirect(config.default_404_url)

    def redirect404_json(self):
        self.write(json_result(-1, '数据提交错误'))

    def prepare(self):
        """
        peewee的连接池, request-hook(请求前连接)
        :return:
        """
        db_mysql.connect()
        return super(BaseRequestHandler, self).prepare()

    def get(self, *args, **kwargs):
        # try:
        super(BaseRequestHandler, self).get(*args, **kwargs)
        # except Exception as e:
        #     logger.error(e)

    def write_error(self, status_code, **kwargs):
        """
        默认错误处理函数
        :param status_code:
        :param kwargs:
        :return:
        """
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

    def get_current_user(self):
        """
        :return:
        """
        # username = self.get_secure_cookie('uuid')
        if greenlet.getcurrent().parent:
            session = MongoSessionManager.load_session_from_request(self)
            username = session.data.get('username', None)
            if not username:
                return None
            user = User.get_by_username(username)
            return user
        return None

    def set_current_user(self, username):
        session = MongoSessionManager.load_session_from_request(self)
        session.data['username'] = username
        MongoSessionManager.update_session(session.get_session_id(), session.data)

    def get_login_url(self):
        """
        获取登陆url
        :return:
        """
        return config.LOGIN_URL

    def success(self, data, errorcode=0):
        """
        成功返回
        :param data:
        :param errorcode:
        :return:
        """
        self.write(json_result(errorcode, data))
        self.finish()

    def error(self, data, errorcode=-1):
        """
        失败返回
        :param data:
        :param errorcode:
        :return:
        """
        self.write(json_result(errorcode, data))
        self.finish()

    def on_finish(self):
        """
        peewee的request-hook(请求完成后关闭)
        :return:
        """
        if not db_mysql.is_closed():
            db_mysql.close()
        return super(BaseRequestHandler, self).on_finish()


class BaseWebsocketHandler(WebSocketHandler):
    """
    基础handler
    """
    def get_current_user(self):
        """
        获取当前用户
        :return:
        """
        username = self.get_secure_cookie('uuid')
        if not username:
            return None
        user = User.get_by_username(username)
        return user


class ErrorHandler(BaseRequestHandler):
    """
    默认404处理
    """

    def prepare(self):
        super(BaseRequestHandler, self).prepare()
        if 'X-Real-IP' in self.request.headers:
            ip = self.request.headers['X-Real-IP']
        else:
            ip = self.request.remote_ip
        logger.error(self.request.uri + "-FROM IP:" + ip)
        self.set_status(404)
        self.redirect("/static/404.html")

    def write_error(self, status_code, **kwargs):
        pass
