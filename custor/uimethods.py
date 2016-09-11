# -*- coding:utf-8 -*-

from custor.utils import TimeUtil
from settings.config import config

def datetime_delta(handler, t):
    if not t:
        return '???'
    return TimeUtil.datetime_delta(t)

def is_default_avatar(handler, avatar):
    if avatar == config.default_avatar:
        return True
    if avatar == None:
        return True
    return False

