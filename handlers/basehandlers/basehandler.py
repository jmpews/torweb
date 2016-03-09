from utils.util import set_api_header
from tornado.web import RequestHandler
from utils import logger
import json
import config

class BaseRequestHandler(RequestHandler):
    '''
    重写了异常处理
    '''
    def write_error(self, status_code, **kwargs):
        if not config.DEBUG:
            self.redirect("/static/500.html")

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
