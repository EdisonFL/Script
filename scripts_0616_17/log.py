# -*- coding: utf-8 -*-
import logging
import os
import sys
from time import strftime
import threading


# 自定义日志类
class MyLog:
    instance = None
    _lock = threading.Lock()

    def __init__(self, filename=None):
        if filename is None:
            filename = ''

        # 输出日志路径
        _PATH = os.path.expanduser('~/Desktop/logging/') + strftime('%Y-%m-%d')
        # 设置日志格式
        _FMT = '%(asctime)s.%(msecs)03d[%(levelname)s]| %(message)s'
        # _FMT = '%(asctime)s| %(message)s'
        # 和时间格式
        # _data_formatter = '%H:%M:%S'
        _data_formatter = "%Y-%m-%d %H:%M:%S"

        self.logger = logging.getLogger()
        self.formatter = logging.Formatter(fmt=_FMT, datefmt=_data_formatter)
        if not os.path.exists(_PATH):
            os.makedirs(_PATH)
        self.log_filename = '{0}/{1}_{2}.log'.format(_PATH, filename, strftime("%Y-%m-%d %H:%M:%S"))
        # print(self.log_filename)
        self.logger.addHandler(self.get_file_handler(self.log_filename))
        # self.logger.addHandler(self.get_console_handler())
        # 设置日志的默认级别
        self.logger.setLevel(logging.INFO)

    # 输出到文件handler的函数定义
    def get_file_handler(self, filename):
        filehandler = logging.FileHandler(filename, encoding="utf-8")
        filehandler.setFormatter(self.formatter)
        return filehandler

    # 输出到控制台handler的函数定义
    def get_console_handler(self):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.formatter)
        return console_handler

    # def __new__(cls, *args, **kwargs):
    #     with cls._lock:
    #         if cls.instance is None:
    #             cls.instance = super().__new__(cls)
    #             return cls.instance
    #         return cls.instance


if __name__ == '__main__':
    log = MyLog()
    log2 = MyLog()
    print(log is log2)
