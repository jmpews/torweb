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