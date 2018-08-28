# -*- coding:utf-8 -*-

"""
 Author: Helixcs
 Site: https://iliangqunru.bitcron.com/
 File: weibo_util.py
 Time: 5/19/18
 Descripton:  weibo_util is in common use
"""
from contextlib import contextmanager
from time import time


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

