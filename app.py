#!/usr/bin/env python
# coding:utf-8

import tornado.web
import tornado.ioloop
from tornado.options import define, options, parse_command_line
import signal
import threading
import time


def close_server():
    from custor.logger import logger
    MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 0
    deadline = time.time() + MAX_WAIT_SECONDS_BEFORE_SHUTDOWN

    def stop_loop():
        now = time.time()
        io_loop = tornado.ioloop.IOLoop.instance()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            io_loop.add_timeout(now + 1, stop_loop)
        else:
            io_loop.stop()
            logger.info('...Shutdown...')
            signal.pthread_kill(threading.current_thread().ident, 9)
    stop_loop()
    logger.info("...close_httpserver():ready...")


# handle signal
def server_shutdown_handler(sig, frame):
    from custor.logger import logger
    logger.warn('...Caught signal: {0}'.format(sig))
    tornado.ioloop.IOLoop.instance().add_callback(close_server)


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
    handlers = ()
    handlers += urls.urlpattern
    handlers += tuple((x[0], tornado.web.StaticFileHandler, x[1]) for x in config.STATIC_PATH)

    from custor import uimethods
    ui_build_methods = {
        'datetime_delta': uimethods.datetime_delta,
        'is_default_avatar': uimethods.is_default_avatar
    }

    application = tornado.web.Application(
        handlers=handlers,
        ui_methods=ui_build_methods,
        default_handler_class=ErrorHandler,
        debug=config.DEBUG,
        template_path=config.TEMPLATE_PATH,
        login_url=config.LOGIN_URL,
        cookie_secret=config.COOKIE_SECRET,
    )

    # added signal callback to interrupt app
    signal.signal(signal.SIGINT, server_shutdown_handler)
    signal.signal(signal.SIGTERM, server_shutdown_handler)

    application.listen(config.PORT)
    from custor.logger import logger
    logger.debug('Server started at port %s' % config.PORT)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    runserver()


