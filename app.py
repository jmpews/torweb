#!/usr/bin/env python
# coding:utf-8

import tornado.web
import tornado.ioloop
from os import path
from sys import argv

import config
from utils.util import monitor_system_status
from handlers.basehandlers.basehandler import ErrorHandler
from handlers.index import IndexHandler, LoginHandler, RegisterHandler
from handlers.post import PostDetailHandler, PostAddHandler
from handlers.api import SystemStatusHandler
from handlers.user import UserProfileHandler, UserProfileEditHandler

handlers = [
    (r'/', IndexHandler),
    (r'/login', LoginHandler),
    (r'/register', RegisterHandler),
    (r'/post/(\d+)', PostDetailHandler),
    (r'/post/add', PostAddHandler),

    (r'/user/(\d+)', UserProfileHandler),
    (r'/user/edit', UserProfileEditHandler),

    (r'/api/systemstatus', SystemStatusHandler),

    (r'/assets/(.*)', tornado.web.StaticFileHandler, {"path": "frontend/src/assets"}),
]

application = tornado.web.Application(
    handlers=handlers,
    default_handler_class=ErrorHandler,
    debug=config.DEBUG,
    static_path=path.join(path.dirname(path.abspath(__file__)), 'static'),
    template_path="frontend/src",
    login_url='/login',
    cookie_secret=config.COOKIE_SECRET,
)

config.app = application

if __name__ == "__main__":
    if len(argv) > 1 and  argv[1][:6] == '-port=':
        config.PORT = int(argv[1][6:])

    monitor_system_status(config.sys_status)
    application.listen(config.PORT)
    print('Server started at port %s' % config.PORT)
    tornado.ioloop.IOLoop.instance().start()
