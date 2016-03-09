# -*- coding:utf-8 -*-
import logging, os, sys


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
