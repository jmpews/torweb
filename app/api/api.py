#coding:utf-8

from app.cache import system_status_cache

from custor.handlers.basehandler import BaseRequestHandler
from custor.utils import json_result

import tornado.websocket

class SystemStatusHandler(BaseRequestHandler):
    """
    ajax请求系统状态
    """
    def get(self, *args, **kwargs):
        self.write(json_result(0, {
            'cpu_per': system_status_cache[0],
            'ram_per': system_status_cache[1],
            'net_conn': system_status_cache[2],
            'os_start': system_status_cache[3]}))

class WebSocketURLHandler(BaseRequestHandler):
    """
    获取websocket_url(因为js在简历websocket server时必须制定绝对的地址,可控性差)
    """
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
            SystemStatusWebsocketHandler.write2(self, system_status_cache)

    def on_close(self):
        if self in SystemStatusWebsocketHandler.clients:
            SystemStatusWebsocketHandler.clients.remove(self)

    @staticmethod
    def write2(client, system_status_cache):
        client.write_message(json_result(0, {
            'cpu_per': system_status_cache[0],
            'ram_per': system_status_cache[1],
            'net_conn': system_status_cache[2],
            'os_start': system_status_cache[3]}))

    @classmethod
    def write2all(cls, system_status_cache):
        '''
        推送给所有用户
        :param system_status_cache:
        :return:
        '''
        for client in cls.clients:
            client.write_message(json_result(0, {
            'cpu_per': system_status_cache[0],
            'ram_per': system_status_cache[1],
            'net_conn': system_status_cache[2],
            'os_start': system_status_cache[3]}))