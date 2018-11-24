# -*- coding:utf-8 -*-

"""
 Author: Helixcs
 Site: https://iliangqunru.bitcron.com/
 File: weibo_util.py
 Time: 5/19/18
 Descripton:  weibo_util is in common use
"""
import logging

from contextlib import contextmanager
from time import time

level = logging.DEBUG
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
datefmt = '%Y-%m-%d %H:%M'
logging.basicConfig(level=level, format=format, datefmt=datefmt)
logger = logging.getLogger(__name__)
logger.setLevel(level)

is_debug = logger.level == logging.DEBUG


def rt_logger(func):
    def func_wrapper(*args, **kwargs):
        __start_time = int(time() * 1000)
        __response = func(*args, **kwargs)
        __end_time = int(time() * 1000)
        print("==> [rt_logger] func: [ %s ], execute spend: [ %s ms ] ." % (func.__name__, (__end_time - __start_time)))
        return __response

    return func_wrapper


@contextmanager
def open_file(file_name: str):
    file = open(file=file_name, mode='wb')
    yield file
    file.flush()
    file.close()
