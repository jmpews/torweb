#encoding:utf-8

import sys, os

sys.path.append(os.path.dirname(sys.path[0]))

from tornado.httpclient import AsyncHTTPClient
from tornado import gen
import tornado.ioloop

@gen.coroutine
def fetch_coroutine(url):
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(url)
    print('test')
    print(response)

# fetch_coroutine('http://sxu.today')

tornado.ioloop.IOLoop.instance().start()
