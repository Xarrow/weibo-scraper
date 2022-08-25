# -*- coding:utf-8 -*-

"""
 Verion: 1.0
 Author: Helixcs
 Site: https://github.com/Xarrow/weibo-scraper
 File: __init__.py.py
 Time: 5/27/18
"""

import sys
import os
import weibo_scraper
from weibo_scraper import set_debug
from weibo_base.weibo_component import exist_get_uid, get_tweet_containerid
from weibo_base.weibo_util import Timer
import logging

set_debug()

if __name__ == '__main__':

    #  获取用户信息
    uid = exist_get_uid(name='嘻红豆')
    print(uid)
    containerid = get_tweet_containerid(uid=uid.get('uid'))
    print(containerid)
    #
    # wp = weibo_scraper.get_weibo_profile(name='嘻红豆')
    # print(wp.raw_user_response)
    #
    # #  根据昵称获取微博
    # result = weibo_scraper.get_weibo_tweets_by_name(name="嘻红豆", pages=1)
    # for tweet in result:
    #     print(tweet)
    #
    # #  根据 containerid 获取微博
    # result = weibo_scraper.get_weibo_tweets(tweet_container_id=containerid, pages=1)
    # for tweet in result:
    #     print(tweet)

    # followers = weibo_scraper.get_follows_and_followers(name="嘻红豆", pages=1)
    # for i in followers:
    #     print(i.follow_and_follower_response)
    #
    #
    # def loop_hotwords():
    #     hotwords = weibo_scraper.get_realtime_hotwords()
    #     for hw in hotwords:
    #         print(str(hw))
    #     pass
    #
    #
    # wt = Timer(name="realtime_hotword_timer", fn=loop_hotwords, interval=10)
    # wt.set_ignore_ex(True)
    # wt.scheduler()
