# -*- coding: utf-8 -*-
import os
import logging
from logging.handlers import RotatingFileHandler
import sys

# logging config
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def get_logger(splider_name):
    '''
      日志路径在爬虫同目录的logs目录下
      每个日志文件最多10M
      错误日志单独提取一份
    '''
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        print("=====loger has handlers=====")
        return logger

    formatter = logging.Formatter('%(asctime)s [%(levelname)-8s]: %(message)s')

    # handler_file_warning = logging.FileHandler(os.path.join(BASE_DIR,"logs/%s.error.log"%(".".join(splider_name.split('.')[:-1]))))
    handler_file_warning = RotatingFileHandler(os.path.join(BASE_DIR, "logs/{}.error.log".format(splider_name)),
                                               mode='a', maxBytes=10 * 1024 * 1024, backupCount=2, encoding=None,
                                               delay=0)
    handler_file_warning.setLevel(logging.WARNING)
    handler_file_warning.setFormatter(formatter)
    logger.addHandler(handler_file_warning)

    # handler_file_normal = logging.FileHandler(os.path.join(BASE_DIR,"logs/%s.log"%(".".join(splider_name.split('.')[:-1]))))
    handler_file_normal = RotatingFileHandler(os.path.join(BASE_DIR, "logs/{}.log".format(splider_name)),
                                              mode='a', maxBytes=10 * 1024 * 1024, backupCount=5, encoding=None,
                                              delay=0)
    handler_file_normal.setLevel(logging.DEBUG)
    handler_file_normal.setFormatter(formatter)
    logger.addHandler(handler_file_normal)

    handler_console = logging.StreamHandler(sys.stdout)
    handler_console.formatter = formatter
    logger.addHandler(handler_console)

    return logger

if __name__ == "__main__":
    print(BASE_DIR)
