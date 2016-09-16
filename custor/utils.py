# coding:utf-8

import json
import random
from tornado.web import MissingArgumentError
from tornado.web import HTTPError
from custor.errors import RequestMissArgumentError, PageNotFoundError

import functools
from urllib.parse import urlencode
import urllib.parse as urlparse

import time, datetime

def random_str(random_length=16):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    for i in range(random_length):
        str += random.choice(chars)
    return str

def random_captcha_str(random_length=16):
    str = ''
    chars = 'abcdefghjklmnpqrstuvwxyz123456789'
    for i in range(random_length):
        str += random.choice(chars)
    return str

def clean_data(value):
    '''
    清洗参数
    :param value:
    :return:
    '''
    return value


def get_cleaned_post_data_http_error(handler, *args):
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


def get_cleaned_query_data_http_error(handler, *args):
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

    这个也可以做成装饰器
    '''
    data = {}
    for k in args:
        try:
            data[k] = handler.get_query_argument(k)
        except MissingArgumentError:
            if blank:
                data[k] = None
            else:
                raise RequestMissArgumentError('[' + k + '] arg not found')
    return data


def get_cleaned_post_data(handler, args, blank=False):
    '''
    同上

    这个也可以做成装饰器
    '''
    data = {}
    for k in args:
        try:
            data[k] = handler.get_body_argument(k)
        except MissingArgumentError:
            if blank:
                data[k] = None
            else:
                raise RequestMissArgumentError('[' + k + '] arg not found')
    return data

def get_cleaned_json_data(handler, args, blank=False):
    '''
    同上

    这个也可以做成装饰器
    '''
    tmp = json.loads(handler.request.body.decode())
    data = {}
    for k in args:
        tmp_x = tmp
        for t in k.split('.'):
            tmp_x = tmp_x.get(t)
        if tmp_x:
            data[k] = tmp_x
        elif not tmp_x and blank:
            data[k] = None
        else:
            raise RequestMissArgumentError('[' + k + '] arg not found')
    return data





def set_api_header(request):
    '''
    设置允许跨域请求
    :param request:
    :return:
    '''
    request.set_header('Access-Control-Allow-Origin', '*')
    request.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    request.set_header('Access-Control-Max-Age', 1000)
    request.set_header('Access-Control-Allow-Headers', '*')
    request.set_header('Content-type', 'application/json')


def json_result(error_code, data):
    '''
    格式化结果为json
    :param error_code:
    :param data:
    :return:
    '''
    if isinstance(data, str):
        result = {'errorcode': error_code, 'txt': data}
    else:
        result = {'errorcode': error_code, 'data': data}
    return json.dumps(result)

def get_page_nav(current_page, page_number_limit, page_limit):
    '''
    页脚导航
    :param current_page:
    :param page_number_limit: 当前结果集的数据量
    :param page_limit: 每一页数据量
    :return:
    # 页导航(cp:当前页, <:前一页, >:后一页)
    # 模型: < cp-2, cp-1, cp, cp+1, cp+2A >
    # 这里如果换成列表存放，在模板里面会好操作一点
    '''
    pages = {'cp-2': 0, 'cp-1': 0, 'cp': current_page, 'cp+1': 0, 'cp+2': 0}
    #import pdb; pdb.set_trace()
    if current_page-1 >= 1:
        pages['cp-1'] = current_page-1
    if current_page-2 >= 1:
        pages['cp-2'] = current_page-2

    if (current_page)*page_limit < page_number_limit:
        pages['cp+1'] = current_page+1
    if (current_page+1)*page_limit < page_number_limit:
        pages['cp+2'] = current_page+2
    return pages

def get_page_number(current_page):
    if current_page:
        current_page = int(current_page)
        if current_page < 1:
            raise PageNotFoundError
        return current_page
    return 1

class TimeUtil:
    '''
    时间友好化显示
    '''
    @staticmethod
    def get_weekday(date):
        week_day_dict = {
            0: '星期一',
            1: '星期二',
            2: '星期三',
            3: '星期四',
            4: '星期五',
            5: '星期六',
            6: '星期日',
        }
        day = date.weekday()
        return week_day_dict[day]

    @staticmethod
    def datetime_format(value, format="%Y-%m-%d %H:%M"):
        return value.strftime(format)

    @staticmethod
    def datetime_format_date(value, format="%Y-%m-%d"):
        return value.strftime(format)

    @staticmethod
    def current_str_date():
        return time.strftime('%Y-%m-%d', time.localtime())

    @staticmethod
    def current_str_datetime():
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    @staticmethod
    def datetime_delta(t):
        now = datetime.datetime.now()
        time_date = now.date() - t.date()
        days = time_date.days
        seconds = (now - t).seconds
        # 星期一 8:00
        if days <= 6:
            if days < 1:
                if seconds < 60:
                    return '几秒前'
                elif seconds < 3600:
                    return '%s分钟前' % int(seconds / 60)
                else:
                    return TimeUtil.datetime_format(t, '%H:%M')
            if days < 2:
                return '昨天 ' + TimeUtil.datetime_format(t, '%H:%M')
            return TimeUtil.get_weekday(t) + ' ' + TimeUtil.datetime_format(t, '%H:%M')
        else:
            return TimeUtil.datetime_format(time, "%Y-%m-%d")

class ColorPrint:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def print(arg):
        print(ColorPrint.OKGREEN + arg + ColorPrint.ENDC)


from threading import Thread
class ThreadWorker(Thread):
    '''
    线程Future
    '''

    def __init__(self, future, func, *args, **kwargs):
        Thread.__init__(self)
        self.future =future
        self.func =func
        self.args = args
        self.kwargs = kwargs
        print('worker init...')

    def run(self):
        result = self.func(*self.args, **self.kwargs)
        self.future.set_result(result)

