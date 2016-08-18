#!/usr/bin/env python
# coding:utf-8

import tornado.web
import tornado.ioloop
from os import path
from sys import argv

import config
from utils.util import monitor_system_status
from handlers.basehandlers.basehandler import ErrorHandler
from handlers.index import IndexHandler, LoginHandler, RegisterHandler, IndexTopicHandler
from handlers.post import PostDetailHandler, PostAddHandler, PostReplyAddHandler, PostReplyOptHandler
from handlers.api import SystemStatusHandler
from handlers.user import UserProfileHandler, UserProfileEditHandler, UserAvatarEditHandler, UserNotificationHandler, UserFollowerHandler
from handlers.cache import update_cache

from utils import ui_methods

handlers = [
    (r'/', IndexHandler),
    (r'/topic/(\w+)', IndexTopicHandler),
    (r'/login', LoginHandler),
    (r'/register', RegisterHandler),
    (r'/post/(\d+)', PostDetailHandler),
    (r'/post/add', PostAddHandler),
    (r'/postreply/add', PostReplyAddHandler),

    # 对post和reply的操作
    (r'/postreplyopt', PostReplyOptHandler),


    (r'/user/(\d+)/follower', UserFollowerHandler),
    (r'/user/(\d+)', UserProfileHandler),
    (r'/user/edit', UserProfileEditHandler),
    (r'/user/notification', UserNotificationHandler),
    (r'/user/follower', UserFollowerHandler),
    (r'/user/avatar/edit', UserAvatarEditHandler),

    (r'/api/systemstatus', SystemStatusHandler),

    (r'/avatar/(.*)', tornado.web.StaticFileHandler, {"path": "static/images/avatars"}),
    (r'/assets/(.*)', tornado.web.StaticFileHandler, {"path": "frontend/src/assets"}),
]

ui_build_methods = {
    'datetime_delta': ui_methods.datetime_delta
}

application = tornado.web.Application(
    handlers=handlers,
    ui_methods=ui_build_methods,
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
    update_cache()
    application.listen(config.PORT)
    print('Server started at port %s' % config.PORT)
    tornado.ioloop.IOLoop.instance().start()
