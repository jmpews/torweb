# coding:utf-8

from app.api.api import (
    SystemStatusHandler,
    SystemStatusWebsocketHandler,
    WebSocketURLHandler
)

urlprefix = r'/api'

urlpattern = (
    (r'/api/systemstatus', SystemStatusHandler),
    (r'/api/systemstatuswebsocket', SystemStatusWebsocketHandler),
    (r'/api/websocketurl', WebSocketURLHandler),
)
