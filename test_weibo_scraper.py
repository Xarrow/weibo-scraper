# -*- coding:utf-8 -*-

"""
 Author: Helixcs
 Site: https://iliangqunru.bitcron.com/
 File: test_weibo_scraper.py
 Time: 5/11/18
"""
import unittest

import weibo_scraper
from weibo_base import *


class TestWeiboScraper(unittest.TestCase):
    def test_get_weibo_tweets(self):
        result = weibo_scraper.get_weibo_tweets(tweet_container_id='1076031843242321', pages=1)
        for tweet in result:
            print(tweet)
        self.assertIsNotNone(result)

    def test_weibo_base_search_name(self):
        result = weibo_api.search_by_name("Helixcs")
        self.assertIsNotNone(result)

    def test_weibo_getIndex(self):
        result = weibo_api.weibo_getIndex('1843242321')
        self.assertIsNotNone(result)

    def test_is_name_exist(self):
        result = exist_get_uid(name="Helixcs")
        print(result)  # 1843242321
        self.assertIsNotNone(result)

        love_result1 = exist_get_uid(name="嘻红豆")
        print(love_result1)  # 3637346297
        self.assertIsNotNone(love_result1)

        love_result2 = exist_get_uid(search_by_name_response='', name='嘻红豆')
        print(love_result2)
        self.assertIsNotNone(love_result2)

        test_result = exist_get_uid(name='暴走大事件')
        print(test_result)  # None
        self.assertIsNotNone(test_result)

    def test_get_weibo_containerid(self):
        # common weibo id , uid is from Helixcs
        test_result = get_tweet_containerid(uid="1843242321")
        print('Containerid from Helixcs is : ', test_result)  # 1076031843242321
        self.assertIsNotNone(test_result)

        # second profile for weibo api , uid is from 来去之间
        test_result2 = get_tweet_containerid(uid='1111681197')
        print('Containerid from 来去之间 is : ', test_result2)  # 2304131111681197_-_
        self.assertIsNotNone(test_result2)

        # second profile for weibo api , uid is from 嘻红豆
        test_result3 = get_tweet_containerid(uid='3637346297')
        print('Containerid from 嘻红豆 is:', test_result3)
        self.assertIsNotNone(test_result3)

    def test_weibo_tweets(self):
        result = weibo_tweets(containerid='1076033637346297', page=1)
        # print(result)

    def test_get_weibo_tweets_by_name(self):
        result_iterator = weibo_scraper.get_weibo_tweets_by_name(name='嘻红豆', pages=1)
        # for i in result_iterator:
        #     print(i)
        result_iterator2 = weibo_scraper.get_weibo_tweets_by_name(name='nicknameisnotexist', pages=1)
        # for i in result_iterator2:
        #     print(i)

    def test_get_containerid_from_second_profile(self):
        result_iterator = weibo_scraper.get_weibo_tweets_by_name(name='来去之间', pages=1)
        for i in result_iterator:
            print(i)
        self.assertIsNotNone(result_iterator)


    def test_weibo_parser(self):
        tweet_response =  weibo_scraper.weibo_tweets(containerid='1076031843242321',page=1)
        wp = WeiboTweetParser(tweet_get_index_response=tweet_response)
        print(wp)



if __name__ == '__main__':
    unittest.main()
