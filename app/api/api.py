# coding:utf-8

from app.cache import system_status_cache
from custor.handlers.basehandler import BaseRequestHandler
from custor.utils import json_result

import tornado.websocket

class SystemStatusHandler(BaseRequestHandler):
    '''
    返回系统状态缓存
    '''
    def get(self, *args, **kwargs):
        self.write(json_result(0, {
            'cpu_per': system_status_cache[0],
            'ram_per': system_status_cache[1],
            'net_conn': system_status_cache[2],
            'os_start': system_status_cache[3]}))

class WebSocketURLHandler(BaseRequestHandler):
    def get(self, *args, **kwargs):
        self.write(json_result(0, {'url': '.'}))


# 注意配置nginx
# proxy_http_version 1.1;
# proxy_redirect off;
# proxy_pass_header Server;
# proxy_set_header Host $http_host;
# proxy_set_header Upgrade $http_upgrade;
# proxy_set_header Connection "upgrade";
# proxy_set_header X-Real-IP $remote_addr;
# proxy_set_header X-Scheme $scheme;
# proxy_pass http://torweb;
class SystemStatusWebsocketHandler(tornado.websocket.WebSocketHandler):
    """
    使用websocket推送系统状态
    """

    # redis ?
    clients = []

    def check_origin(self, origin):
        return True

    def open(self):
        if self not in SystemStatusWebsocketHandler.clients:
            SystemStatusWebsocketHandler.clients.append(self)

    def on_close(self):
        if self in SystemStatusWebsocketHandler.clients:
            SystemStatusWebsocketHandler.clients.remove(self)

    @classmethod
    def write2all(cls, system_status_cache):
        for client in cls.clients:
            client.write_message(json_result(0, {
            'cpu_per': system_status_cache[0],
            'ram_per': system_status_cache[1],
            'net_conn': system_status_cache[2],
            'os_start': system_status_cache[3]}))