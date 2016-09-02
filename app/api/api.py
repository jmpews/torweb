# coding:utf-8

from app.cache import system_status_cache
from custor.handlers.basehandler import BaseRequestHandler
from custor.utils import json_result


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
