# -*- coding:utf-8 -*-

from .common_utils import TimeUtil


def datetime_delta(handler, t):
    if not t:
        return '???'
    return TimeUtil.datetime_delta(t)
