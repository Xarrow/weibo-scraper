# -*- coding:utf-8 -*-

"""
 Author: Helixcs
 Site: https://iliangqunru.bitcron.com/
 File: test_weibo_scraper.py
 Time: 5/11/18
"""
import unittest

import weibo_scraper

class TestWeiboScraper(unittest.TestCase):
    def test_get_weibo_tweets(self):
        result = weibo_scraper.get_weibo_tweets(container_id='1076031843242321')
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()