# -*- coding:utf-8 -*-

"""
 Verion: 1.0
 Author: Helixcs
 Site: https://github.com/xarrow/
 File: utils_sample.py
 Time: 2022/8/1
"""
import weibo_scraper
from weibo_base import RequestProcessor, logger, MapRequestProcessorChains, RQWrapper, RequestProxy, set_debug, \
    request_proxy
import requests

requests_proxy = RequestProxy()
set_debug()


class SimpleInterceptorRequestProcessor(RequestProcessor):

    def ignore_exception(self):
        pass

    def before_request_intercept(self, rq_wrapper: RQWrapper):
        logger.debug("RQ : {}, {}".format(rq_wrapper.method, rq_wrapper.url))
        pass

    def after_request_intercept(self, response: requests.Response):
        logger.debug("RS : {}".format(response.text))
        pass


if __name__ == '__main__':
    chains = MapRequestProcessorChains()
    processor = SimpleInterceptorRequestProcessor()
    chains.add_processor(processor)
    requests_proxy.set_request_processor_chains(chains)

    response = requests_proxy.get("https://baidu.com")
    print(response.text)

    request_proxy.set_request_processor_chains(chains)
    followers = weibo_scraper.get_follows_and_followers(name="嘻红豆", pages=1)
    for i in followers:
        print(i.follow_and_follower_response)
