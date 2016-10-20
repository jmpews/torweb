# conding:utf-8
from app.dashboard.dashboard import  (
    IndexHandler,
    PostIndexHandler,
    UserIndexHandler,
)

urlprefix = r''

urlpattern = (
    (r'/db', IndexHandler),
    (r'/db/post', PostIndexHandler),
    (r'/db/user', UserIndexHandler),
)
