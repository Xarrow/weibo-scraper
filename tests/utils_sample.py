# -*- coding:utf-8 -*-

"""
 Verion: 1.0
 Author: Helixcs
 Site: https://github.com/xarrow/
 File: utils_sample.py
 Time: 2022/8/1
"""
from weibo_base import RequestProxy, RequestProcessor, logger, MapRequestProcessorChains
import requests

requests_proxy = RequestProxy()


class SimpleInterceptorRequestProcessor(RequestProcessor):

    def ignore_exception(self):
        pass

    def before_request_intercept(self, prepped: requests.PreparedRequest, method: str, url: str, **kwargs):
        prepped.url = "https://baidu.com"
        logger.info("RQ : {}, {}, {}".format(method, url, kwargs))
        pass

    def after_request_intercept(self, response: requests.Response):
        logger.info("RS : {}".format(response.text))
        pass


if __name__ == '__main__':
    chains = MapRequestProcessorChains()
    processor = SimpleInterceptorRequestProcessor()
    chains.add_processor(processor)

    requests_proxy.set_request_processor_chains(chains)

    response = requests_proxy.get("https://baidu.com")
    import requests

    print(requests.get("https://baidu.com").text)

    pass
