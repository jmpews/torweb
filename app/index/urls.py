# conding:utf-8

from app.index.index import (
    IndexHandler,
    IndexTopicHandler,
    RegisterHandler,
    LoginHandler,
    LogoutHandler,
)

urlprefix = r''

urlpattern = (
    (r'/', IndexHandler),
    (r'/index', IndexHandler),
    (r'/topic/([\w-]+)', IndexTopicHandler),
    (r'/login', LoginHandler),
    (r'/logout', LogoutHandler),
    (r'/register', RegisterHandler),
)
