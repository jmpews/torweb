# -*- coding:utf-8 -*-

from custor.utils import TimeUtil

def datetime_delta(handler, t):
    if not t:
        return '???'
    return TimeUtil.datetime_delta(t)
