# coding:utf-8
import json
from hashlib import md5
import random
from tornado.web import MissingArgumentError
from tornado.web import HTTPError

import functools
from urllib.parse import urlencode
import urllib.parse as urlparse

from utils import logger


class RequestArgumentError(Exception):
    def __init__(self, msg='Unknown', code=233):
        self.msg = msg
        self.code = code
        super(RequestArgumentError, self).__init__(code, msg)

    def __str__(self):
        return self.msg


def random_str(random_length=16):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    for i in range(len(chars)):
        str += random.choice(chars)
    return str


def clean_data(value):
    return value


def get_cleaned_post_data_httperror(handler, *args):
    '''
    获取post参数，在这个过程进行参数净化，如果缺少参数则raise HTTPError到BaseHandler的write_error()处理函数
    '''
    data = {}
    for k in args:
        try:
            data[k] = handler.get_body_argument(k)
        except MissingArgumentError:
            raise HTTPError(400)
    return data


def get_cleaned_query_data_httperror(handler, *args):
    '''
    同上
    '''
    data = {}
    for k in args:
        try:
            data[k] = handler.get_query_argument(k)
        except MissingArgumentError:
            raise HTTPError(400)
    return data


def get_cleaned_query_data(handler, args, blank=False):
    '''
    这个是自定义异常的，然后到get/post去catch然后异常处理，不如raise HTTPError来的通用.
    '''
    data = {}
    for k in args:
        try:
            data[k] = handler.get_query_argument(k)
        except MissingArgumentError:
            if blank:
                data[k] = None
            else:
                raise RequestArgumentError(k + 'arg not found')
    return data


def get_cleaned_post_data(handler, args, blank=False):
    '''
    这个是自定义异常的，然后到get/post去catch然后异常处理，不如raise HTTPError来的通用.
    '''
    data = {}
    for k in args:
        try:
            data[k] = handler.get_body_argument(k)
        except MissingArgumentError:
            if blank:
                data[k] = None
            else:
                raise RequestArgumentError(k + ' arg not found')
    return data


def login_required(method):
    from tornado.httpclient import HTTPError
    '''
    from "tornado.web.authenticated"
    `self.current_user`是一个@property
    '''

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            if self.request.method in ("GET", "HEAD"):
                url = self.get_login_url()
                if "?" not in url:
                    if urlparse.urlsplit(url).scheme:
                        # if login url is absolute, make next absolute too
                        next_url = self.request.full_url()
                    else:
                        next_url = self.request.uri
                    url += "?" + urlencode(dict(next=next_url))
                self.redirect(url)
                return
            raise HTTPError(403)
        return method(self, *args, **kwargs)

    return wrapper


def set_api_header(request):
    request.set_header('Access-Control-Allow-Origin', '*')
    request.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    request.set_header('Access-Control-Max-Age', 1000)
    request.set_header('Access-Control-Allow-Headers', '*')
    request.set_header('Content-type', 'application/json')


def json_result(error_code, data):
    if isinstance(data, str):
        result = {'errorcode': error_code, 'txt': data}
    else:
        result = {'errorcode': error_code, 'data': data}
    return json.dumps(result)

from threading import Thread


class MonitorWorker(Thread):
    def __init__(self, name, systatus):
        Thread.__init__(self)
        self.name = name
        self.systatus = systatus
    def run(self):
        logger.debug("start monitor system status...")
        import psutil, datetime, time
        while True:
            try:
                time.sleep(30)
                s1 = psutil.cpu_percent()
                s2 = psutil.virtual_memory()[2]
                try:
                    s3 = len(psutil.net_connections())
                except:
                    s3 = 'unkown'
                s4 = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d")
                #s4 = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
                #self.systatus = [s1, s2, s3, s4]
                self.systatus[0] = s1
                self.systatus[1] = s2
                self.systatus[2] = s3
                self.systatus[3] = s4
                print(self.systatus)
            except KeyboardInterrupt:
                break

def monitor_system_status(systatus):
    monitor = MonitorWorker('system', systatus)
    monitor.start()
