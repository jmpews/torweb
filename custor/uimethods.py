# -*- coding:utf-8 -*-

""" Tornado Template Module
"""

from settings.config import config
from custor.utils import TimeUtil

__all__ = ['datetime_delta', 'is_default_avatar']

def datetime_delta(handler, t):
    """
    display friendly time
    :param handler:
    :param t:
    :return:
    """
    if not t:
        return '???'
    return TimeUtil.datetime_delta(t)


def is_default_avatar(handler, avatar):
    """
     weather the avatar is default avatar
    :param handler:
    :param avatar:
    :return:
    """
    if avatar == config.default_avatar:
        return True
    if avatar is None:
        return True
    return False

