from tornado.web import RequestHandler
from backend.mysql_model.user import User
from utils import logger
from utils.util import set_api_header,json_result, RequestArgumentError
import json
import config

class BaseRequestHandler(RequestHandler):
    '''
    重写了异常处理
    '''
    def write_error(self, status_code, **kwargs):
        if 'exc_info' in kwargs:
            # 参数缺失异常
            if isinstance(kwargs['exc_info'][1],RequestArgumentError):
                self.write(json_result(kwargs['exc_info'][1].code,kwargs['exc_info'][1].msg))
                return

        if status_code==400:
            self.write(json_result(400,'缺少参数'))
            return
        if not config.DEBUG:
            self.redirect("/static/500.html")

    def get_current_user(self):
        username = self.get_secure_cookie('uuid')
        if not username:
            return None
        user=User.get_by_username(username)
        return user

class ErrorHandler(BaseRequestHandler):
    '''
    默认404处理
    '''
    def prepare(self):
        if 'X-Real-IP' in self.request.headers:
            ip=self.request.headers['X-Real-IP']
        else:
            ip=self.request.remote_ip
        logger.error(self.request.uri+"-FROM IP:"+ip)
        self.set_status(404)
        self.redirect("/static/404.html")
    def write_error(self):
        pass
