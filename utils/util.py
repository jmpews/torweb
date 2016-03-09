import json
from hashlib import md5
import random
from tornado.web import MissingArgumentError
class RequestArgumentError(Exception):
    def __init__(self,msg):
        super(RequestArgumentError, self).__init__(msg)
        self.msg=msg
    def __str__(self):
        return self.msg

def random_str(random_length=16):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    for i in range(len(chars)):
        str+=random.choice(chars)
    return str


def clean_data(value):
    return value

def get_cleaned_post_data(handler,*args):
    data={}
    for k in args:
        try:
            data[k]=handler.get_body_argument(k)
        except MissingArgumentError:
            raise RequestArgumentError('Completion information')
    return data

def get_cleaned_query_data(handler,*args):
    data={}
    for k in args:
        try:
            data[k]=handler.get_query_argument(k)
        except MissingArgumentError:
            raise RequestArgumentError('Completion information')
    return data

def set_api_header(request):
    request.set_header('Access-Control-Allow-Origin', '*')
    request.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    request.set_header('Access-Control-Max-Age', 1000)
    request.set_header('Access-Control-Allow-Headers', '*')
    request.set_header('Content-type', 'application/json')

