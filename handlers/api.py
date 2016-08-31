# coding:utf-8
import tornado.web
import config
from handlers.basehandlers.basehandler import BaseRequestHandler

from utils.util import json_result


class SystemStatusHandler(BaseRequestHandler):
    def get(self, *args, **kwargs):
        t = config.sys_status
        self.write(json_result(0, {
            'cpu_per': t[0],
            'ram_per': t[1],
            'net_conn': t[2],
            'os_start': t[3]}))
