# conding:utf-8

from app.api.api import (
    SystemStatusHandler
)

urlprefix = r'/api'

urlpattern = (
    (r'/api/systemstatus', SystemStatusHandler),
)
