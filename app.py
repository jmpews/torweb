#!/usr/bin/env python
# coding:utf-8

from os import path

import tornado.web
import tornado.ioloop
from tornado.options import define, options, parse_command_line

def runserver():
    # define("port", default=8888, help="run on the given port", type=int)
    define("config", default='', help="config", type=str)
    parse_command_line()

    # maybe we can log with file
    # parse_config_file()

    import settings.config
    config = settings.config.load_config(options.config)
    settings.config.config = config

    from app.cache import update_cache
    update_cache()

    from custor.handlers.basehandler import ErrorHandler
    from app import urls
    handlers =()
    handlers += urls.urlpattern
    handlers += tuple((x[0], tornado.web.StaticFileHandler, x[1]) for x in config.STATIC_PATH)

    from custor import uimethods
    ui_build_methods = {
        'datetime_delta': uimethods.datetime_delta
    }

    application = tornado.web.Application(
        handlers=handlers,
        ui_methods=ui_build_methods,
        default_handler_class=ErrorHandler,
        debug=config.DEBUG,
        static_path=config.static_path,
        template_path=config.TEMPLATE_PATH,
        login_url=config.LOGIN_URL,
        cookie_secret=config.COOKIE_SECRET,
    )


    application.listen(config.PORT)
    from custor.logger import logger
    logger.debug('Server started at port %s' % config.PORT)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    runserver()


