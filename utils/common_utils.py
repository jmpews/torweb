# -*- coding:utf-8 -*-
import logging, os, sys
import time
import datetime


class Logger:
    def __init__(self, log_path, level=logging.DEBUG):
        self.logger = logging.getLogger(log_path)
        out_format = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')

        file_log_handler = logging.FileHandler(log_path)
        file_log_handler.setFormatter(out_format)
        # file_log_handler.setLevel(level)

        steam_log_handler = logging.StreamHandler(sys.stdout)
        steam_log_handler.setFormatter(out_format)

        # steam_log_handler.setLevel(level)
        self.logger.addHandler(steam_log_handler)
        self.logger.addHandler(file_log_handler)
        self.logger.setLevel(level)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def war(self, message):
        self.logger.warn(message)

    def error(self, message):
        self.logger.error(message)

    def cri(self, message):
        self.logger.critical(message)

    def exc(self, message):
        self.logger.exception(message)


class TimeUtil:
    def get_weekday(date):
        week_day_dict = {
            0: '星期一',
            1: '星期二',
            2: '星期三',
            3: '星期四',
            4: '星期五',
            5: '星期六',
            6: '星期日',
        }
        day = date.weekday()
        return week_day_dict[day]

    def datetime_format(value, format="%Y-%m-%d %H:%M"):
        return value.strftime(format)

    def datetime_format_date(value, format="%Y-%m-%d"):
        return value.strftime(format)

    def current_str_date():
        return time.strftime('%Y-%m-%d', time.localtime())

    def current_str_datetime():
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    def datetime_delta(t):
        now = datetime.datetime.now()
        time_date = now.date() - t.date()
        days = time_date.days
        seconds = (now - t).seconds
        # 星期一 8:00
        if days <= 6:
            if days < 1:
                if seconds < 60:
                    return '几秒前'
                elif seconds < 3600:
                    return '%s分钟前' % int(seconds / 60)
                else:
                    return TimeUtil.datetime_format(t, '%H:%M')
            if days < 2:
                return '昨天 ' + TimeUtil.datetime_format(t, '%H:%M')
            return TimeUtil.get_weekday(t) + ' ' + TimeUtil.datetime_format(t, '%H:%M')
        else:
            return TimeUtil.datetime_format(time, "%Y-%m-%d")
