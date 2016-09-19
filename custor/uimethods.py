# -*- coding:utf-8 -*-

from custor.utils import TimeUtil
from settings.config import config

"""
将方法注入到template模板中
"""

def datetime_delta(handler, t):
    '''
    时间友好显示
    :param handler:
    :param t:
    :return:
    '''
    if not t:
        return '???'
    return TimeUtil.datetime_delta(t)

def is_default_avatar(handler, avatar):
    '''
    判断用户头像是否是默认头像
    :param handler:
    :param avatar:
    :return:
    '''
    if avatar == config.default_avatar:
        return True
    if avatar == None:
        return True
    return False

