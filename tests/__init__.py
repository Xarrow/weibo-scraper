# -*- coding=utf-8 -*-
"""
 @Author xuanji.zj
 @Email xuanji.zj@alibaba-inc.com
 @Time 2021/6/6 7:38 下午
 @desc  Add New Functions In __init__.py
 
"""

import sys
import os
import weibo_scraper
from weibo_scraper import set_debug
from weibo_base.weibo_component import exist_get_uid, get_tweet_containerid
from weibo_base.weibo_util import Timer
import logging

if __name__ == '__main__':
    set_debug()
    #  Test RequestProxy

    # uid = exist_get_uid(name='嘻红豆')
    # print(uid)
    # containerid = get_tweet_containerid(uid=uid.get('uid'))
    # print(containerid)
    #
    # result = weibo_scraper.get_weibo_tweets_by_name(name="嘻红豆", pages=1)
    # for tweet in result:
    #     print(tweet)
    # result = weibo_scraper.get_weibo_tweets(tweet_container_id=containerid, pages=1)
    # for tweet in result:
    #     print(tweet)
    #
    # wp = weibo_scraper.get_weibo_profile(name='嘻红豆')
    # print(wp.raw_user_response)
    #
    # hotwords = weibo_scraper.get_realtime_hotwords()
    # for hw in hotwords:
    #     print(str(hw))
    # pass
    #
    # wt = Timer(name="realtime_hotword_timer", fn=weibo_scraper.get_realtime_hotwords, interval=1)
    # wt.set_ignore_ex(True)
    # wt.scheduler()
