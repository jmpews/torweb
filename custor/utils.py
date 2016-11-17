# coding:utf-8
from tornado.web import MissingArgumentError, HTTPError
from custor.errors import RequestMissArgumentError, PageNotFoundError

import random
import json
import time, datetime
from threading import Thread


def random_str(random_length=16):
    """
    random character
    :param random_length:
    :return:
    """
    rs = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    # rs = ''.join([
    #     random.choice(chars)
    #     for i in range(random_length)
    # ])
    for i in range(random_length):
        rs += random.choice(chars)
    return rs


def random_captcha_str(random_length=16):
    """
    random character exclude captcha. ex: i,1; o,0
    生成随机字符 但是排除不适合做验证码的比如i,1; 0,o 等
    :param random_length:
    :return:
    """
    rs = ''
    chars = 'abcdefghjklmnpqrstuvwxyz123456789'
    for i in range(random_length):
        rs += random.choice(chars)
    return rs


def clean_data(value):
    """
    clean value
    :param value:
    :return:
    """
    return value


def get_cleaned_post_data_http_error(handler, *args):
    """
    get arg with `clean_data`, if miss arg, raise HTTPError, BaseHandler.write_error() will catch it.
    获取post参数，在这个过程进行参数净化，如果缺少参数则raise HTTPError 到 BaseHandler 的 write_error() 处理函数
    :param handler:
    :param args: 参数列表, exp: ['arg1', 'arg2']
    :return:
    """
    data = {}
    for k in args:
        try:
            data[k] = clean_data(handler.get_body_argument(k))
        except MissingArgumentError:
            raise HTTPError(400)
    return data


def get_cleaned_query_data_http_error(handler, *args):
    """
    同上
    :param handler:
    :param args:
    :return:
    """
    data = {}
    for k in args:
        try:
            data[k] = clean_data(handler.get_query_argument(k))
        except MissingArgumentError:
            raise HTTPError(400)
    return data


def get_cleaned_query_data(handler, args, blank=False):
    """
    with custom Exception, without `HTTPError`, maybe @decorator better
    ---
    这个是自定义异常的，然后到get/post去catch然后异常处理，不如raise HTTPError来的通用.
    这个也可以做成装饰器
    :param handler:
    :param args:
    :param blank: allow null
    :return:
    """
    data = {}
    for k in args:
        try:
            data[k] = clean_data(handler.get_query_argument(k))
        except MissingArgumentError:
            if blank:
                data[k] = None
            else:
                raise RequestMissArgumentError('[' + k + '] arg not found')
    return data


def get_cleaned_post_data(handler, args, blank=False):
    """
    same as `get_cleaned_query_data`
    :param handler:
    :param args:
    :param blank:
    :return:
    """
    data = {}
    for k in args:
        try:
            data[k] = clean_data(handler.get_body_argument(k))
        except MissingArgumentError:
            if blank:
                data[k] = None
            else:
                raise RequestMissArgumentError('[' + k + '] arg not found')
    return data


def get_cleaned_json_data(handler, args, blank=False):
    """
    same as `get_cleaned_query_data`
    :param handler:
    :param args: ['data.key', 'data.id']
    :param blank:
    :return:
    """
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


def get_cleaned_json_data_websocket(message, args, blank=False):
    """
    same as `get_cleaned_query_data`
    :param message:
    :param args:
    :param blank:
    :return:
    """
    tmp = json.loads(message)
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
    """
    allow cross domain request
    :param request:
    :return:
    """
    request.set_header('Access-Control-Allow-Origin', '*')
    request.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    request.set_header('Access-Control-Max-Age', 1000)
    request.set_header('Access-Control-Allow-Headers', '*')
    request.set_header('Content-type', 'application/json')


def json_result(error_code, data):
    """
    format result as `json`
    :param error_code:
    :param data:
    :return:
    """
    if isinstance(data, str):
        result = {'errorcode': error_code, 'txt': data}
    else:
        result = {'errorcode': error_code, 'data': data}
    return json.dumps(result)


def get_page_nav(current_page, result_count, page_limit):
    """
    page-nav
    model('cp': current_page, '<': prev-page, '>': next-page):
        < cp-2, cp-1, cp, cp+1, cp+2 >
    :param current_page:
    :param result_count: all the result count
    :param page_limit:
    :return:
    """
    pages = {'cp-2': 0, 'cp-1': 0, 'cp': current_page, 'cp+1': 0, 'cp+2': 0}
    if current_page - 1 >= 1:
        pages['cp-1'] = current_page - 1
    if current_page - 2 >= 1:
        pages['cp-2'] = current_page - 2

    if (current_page) * page_limit < result_count:
        pages['cp+1'] = current_page + 1
    if (current_page + 1) * page_limit < result_count:
        pages['cp+2'] = current_page + 2
    return pages


def get_page_number(current_page):
    if current_page:
        current_page = int(current_page)
        if current_page < 1:
            raise PageNotFoundError
        return current_page
    return 1


class TimeUtil:
    """
    display friendly time
    """
    @staticmethod
    def get_ago(ago):
        """
        get time of `age`
        :param ago:
        :return:
        """
        t = time.time() - ago
        return datetime.datetime.fromtimestamp(t)

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
    def current_str_date():
        return time.strftime('%Y-%m-%d', time.localtime())

    @staticmethod
    def datetime_delta(t):
        """
        show friendly time of `t`
        :param t:
        :return:
        """
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
            return TimeUtil.datetime_format(t, "%Y-%m-%d")


class ColorPrint:
    """
    color print
    """
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


class ThreadWorker(Thread):
    """
    Future
    """
    def __init__(self, future, func, *args, **kwargs):
        Thread.__init__(self)
        self.future = future
        self.func = func
        self.args = args
        self.kwargs = kwargs
        print('worker init...')

    def run(self):
        result = self.func(*self.args, **self.kwargs)
        self.future.set_result(result)
