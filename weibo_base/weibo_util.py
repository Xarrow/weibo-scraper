# -*- coding:utf-8 -*-

"""
 Author: Helixcs
 Site: https://github.com/Xarrow/weibo-scraper
 File: weibo_util.py
 Time: 5/19/18
 Descripton:  weibo_util is in common use
"""
import logging
import threading
import sys
from abc import abstractmethod

import requests
from contextlib import contextmanager
from time import time

from requests import sessions

level = logging.INFO
ws_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
ws_datefmt = '%Y-%m-%d %H:%M'
logging.basicConfig(level=level, format=ws_format, datefmt=ws_datefmt)
logger = logging.getLogger(__name__)
logger.setLevel(level)


class WeiboApiException(Exception):
    def __init__(self, message):
        self.message = message


class WeiboScraperException(Exception):
    def __init__(self, message):
        self.message = message


def set_debug():
    logger.setLevel(logging.DEBUG)


def rt_logger(func):
    def func_wrapper(*args, **kwargs):
        __start_time = int(time() * 1000)
        __response = func(*args, **kwargs)
        __end_time = int(time() * 1000)
        is_debug = logger.level == logging.DEBUG
        if is_debug:
            logger.debug("[ws] [rt_logger] func: [ %s ], args:[ %s ] execute spend: [ %s ms ] ." % (
                func.__name__, (args, kwargs), (__end_time - __start_time)))
        return __response

    return func_wrapper


def api_ex_handle(func):
    pass


def ws_handle(func):
    def func_wrapper(*args, **kwargs):
        is_debug = logger.level == logging.DEBUG
        start_time = int(time() * 1000)
        response = None
        try:
            response = func(*args, **kwargs)
            return response
        except WeiboApiException as ex:
            pass
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            _ext = []
            _ = set()
            handle_exec_tb(exc_tb, _ext, _)
            logger.error("[exception] function:[{0}] exception , params:{1}, response:{2} ,ex:{4}, stack:{3}".format(
                func.__name__,
                (args, kwargs),
                ex,
                response,
                _ext))
            raise ex
        finally:
            if is_debug:
                logger.debug(
                    "[invoke process] function:[{0}] , params:{1}, response:{2} ".format(
                        func.__name__,
                        (args, kwargs),
                        response))

                end_time = int(time() * 1000)
                logger.debug("[cost time] function:[%s], args:[%s] execute spend:[%s ms]" % (
                    func.__name__,
                    (args, kwargs),
                    (end_time - start_time)))

    return func_wrapper


def handle_exec_tb(tb_exec, _ext: list, cls_methods_tag_set: set):
    if not hasattr(tb_exec, "tb_frame"):
        return
    _fileName = _cls_methods_tag = tb_exec.tb_frame.f_code.co_filename
    _parameters = {}
    for k, v in tb_exec.tb_frame.f_locals.items():
        if isinstance(v, object):
            if k == 'func':
                v = v.__name__
                _cls_methods_tag += "_" + v
                if _cls_methods_tag in cls_methods_tag_set:
                    return
                cls_methods_tag_set.add(_cls_methods_tag)
            else:
                v = str(v)
        _parameters[k] = v
    _ret = {"fname": _fileName,
            "lineno": tb_exec.tb_lineno,
            "parameters": _parameters}
    _ext.append(_ret)
    handle_exec_tb(tb_exec.tb_next, _ext, cls_methods_tag_set)


# todo
#  AntiStrategy
#  反爬虫策略
class AntiStrategy(object):
    def do_strategy(self):
        raise "do_strategy not implemented"


class SleepStrategy(AntiStrategy):
    def do_strategy(self):
        pass


class ProxyStrategy(AntiStrategy):
    def do_strategy(self):
        pass


# RequestProcessor
class RequestProcessor(object):
    def __init__(self, ):
        pass

    def processor_name(self):
        """
        default current processor class name
        :return:
        """
        return self.__class__.__name__

    @abstractmethod
    def ignore_exception(self, ):
        raise "ignore_exception not implemented"

    @abstractmethod
    def before_request_intercept(self, prepped, method: str, url: str, **kwargs):
        raise "before_request_intercept not implemented"

    @abstractmethod
    def after_request_intercept(self, response: requests.Response):
        raise "before_request_intercept not implemented"


# RequestProcessorChains
class RequestProcessorChains(object):

    @abstractmethod
    def add_processor(self, requestProcessor: RequestProcessor):
        pass

    @abstractmethod
    def remove_processor(self, requestProcessor: RequestProcessor):
        pass

    @abstractmethod
    def clear(self, ):
        pass

    @abstractmethod
    def execute_before_intercept(self, prepped, method: str, url: str, **kwargs):
        pass

    @abstractmethod
    def execute_after_intercept(self, response: requests.Response):
        pass


class MapRequestProcessorChains(RequestProcessorChains):
    def __init__(self):
        self._chains = {}
        super().__init__()

    def add_processor(self, requestProcessor: RequestProcessor):
        self._chains[requestProcessor.processor_name()] = requestProcessor
        pass

    def remove_processor(self, requestProcessor: RequestProcessor):
        self._chains.pop(requestProcessor.processor_name())
        pass

    def clear(self):
        self._chains.clear()
        pass

    def execute_before_intercept(self, prepped, method: str, url: str, **kwargs):
        for item in self._chains.items():
            processor_name = item[0]
            processor = item[1]
            processor.before_request_intercept(prepped, method, url, **kwargs)

    def execute_after_intercept(self, response: requests.Response):
        for item in self._chains.items():
            processor_name = item[0]
            processor = item[1]
            processor.after_request_intercept(response)


class SocketsProxyRequestProcessor(RequestProcessor):
    def __init__(self):
        super().__init__()

    def before_request_intercept(self, prepped, method: str, url: str, **kwargs):
        pass

    def after_request_intercept(self, response: requests.Response):
        pass


# todo
class RQWrapper(object):
    def __init__(self, method, url, **kwargs):
        pass


class RequestProxy(object):
    def __init__(self, ):
        self._request_processor_chains = None
        super().__init__()

    def set_request_processor_chains(self, requestProcessorChains: RequestProcessorChains):
        self._request_processor_chains = requestProcessorChains

    @staticmethod
    def session() -> requests.Session:
        requests.get()
        return requests.Session()

    def requests_proxy(self, method, url, **kwargs) -> requests.Response:
        """
        request proxy
        """
        with sessions.Session() as session:
            req = requests.Request(method=method, url=url)
            prepped = session.prepare_request(req)
            # before
            if self._request_processor_chains:
                self._request_processor_chains.execute_before_intercept(prepped, method, url, **kwargs)
            # request
            response = session.request(method=method, url=url, **kwargs)
            # after
            if self._request_processor_chains:
                self._request_processor_chains.execute_after_intercept(response)

            return response

    def get(self, url, params=None, **kwargs) -> requests.Response:
        """
        @see requests.sessions.Session
        """
        kwargs.setdefault('allow_redirects', True)
        return self.requests_proxy('GET', url, params=params, **kwargs)

    def post(self, url, data=None, json=None, **kwargs) -> requests.Response:
        return self.requests_proxy('POST', url, data=data, json=json, **kwargs)


@contextmanager
def open_file(file_name: str):
    file = open(file=file_name, mode='wb')
    yield file
    file.flush()
    file.close()


class Timer(object):
    __slots__ = ['_name', '_timer', '_fn', '_interval', '_ignore_ex', '_on_result', '_on_exception',
                 '_args', '_kwargs']

    def __init__(self,
                 name,
                 fn,
                 interval=7,
                 *args,
                 **kwargs):
        """
        :param name:  timer name
        :param fn:    function which scheduler
        :param interval:  scheduler interval, default 7s
        :param args:      args in function
        :param kwargs:    kwargs in function
        """
        #
        self._name = name
        # Thread.Timer
        self._timer = None
        # function which callable
        self._fn = fn
        # timer interval default 7s
        self._interval = interval
        # whether ignore invoke exception
        self._ignore_ex = False
        self._on_result = None
        self._on_exception = None
        # function args
        self._args = args
        # function kwargs
        self._kwargs = kwargs

    @property
    def name(self):
        return self._name

    def set_name(self, name):
        self._name = name
        return self

    @property
    def fn(self):
        return self._fn

    def set_fn(self, fn):
        self._fn = fn
        return self

    @property
    def interval(self, ):
        return self._interval

    def set_interval(self, interval):
        self._interval = interval
        return self

    @property
    def ignore_ex(self):
        return self._ignore_ex

    def set_ignore_ex(self, ignore_ex):
        self._ignore_ex = ignore_ex
        return self

    @property
    def on_result(self):
        return self._on_result

    def set_on_result(self, fn):
        self._on_result = fn
        return self

    @property
    def on_exception(self):
        return self._on_exception

    def set_on_exception(self, fn):
        self._on_exception = fn
        return self

    def alive(self):
        if self._timer is None:
            return False
        return self._timer.is_alive()

    def scheduler(self):
        try:
            res = self._fn(*self._args, **self._kwargs)
            if self._on_result:
                self._on_result(res)
        except Exception as ex:
            if self._on_exception:
                self._on_exception(ex)
            if not self._ignore_ex:
                # stop timer
                raise ex
        self._timer = threading.Timer(self._interval, self.scheduler, )
        self._timer.start()

    def cancel(self):
        if self._timer:
            self._timer.cancel()


class TimerManager(object):
    def __init__(self, ):
        self._timers_container = {}
        self._executed = False

    def all_timers(self):
        return self._timers_container

    def add_timer(self, timer):
        self._timers_container[timer.name] = timer
        return self

    def execute(self):
        """
        scheduler all timer in manager
        :return: None
        """
        if self._executed:
            return
        for name, timer in self._timers_container.items():
            if timer.alive():
                continue
            timer.scheduler()
        self._executed = True

    def cancel_timer(self, timer_name=None, ):
        """
        cancel timer , and  nacos timer still in container
        it can execute again.
        :param timer_name:
        :return: None
        """
        timer = self._timers_container.get(timer_name)
        if timer:
            timer.cancel()

    def cancel(self):
        """
        cancel all timer in container
        :return: None
        """
        for _, timer in self._timers_container.items():
            timer.cancel()

    def stop_timer(self, timer_name):
        """
        cancel nacos timer and remove it from timer container
        :param timer_name:
        :return: None
        """
        self.cancel_timer(timer_name)
        self._timers_container.pop(timer_name)

    def stop(self):
        """
        remove all timer, and it can not execute again
        """
        self.cancel()
        self._timers_container.clear()
