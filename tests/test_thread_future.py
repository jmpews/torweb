# coding:utf-8

import sys, os
import tornado.ioloop
from tornado import gen

sys.path.append(os.path.dirname(sys.path[0]))

import time
from custor.decorators import run_with_thread_future

@run_with_thread_future(None)
def thread_sleep(self, args):
    time.sleep(5)

@gen.coroutine
def sleep_coroutine():
    yield thread_sleep(None, None)
    print('sleep finish.')


sleep_coroutine()
print('continue other work.')

tornado.ioloop.IOLoop.instance().start()
