# conding:utf-8
from app.dashboard.dashboard import  (
    IndexHandler
)

urlprefix = r''

urlpattern = (
    (r'/db', IndexHandler),
)
