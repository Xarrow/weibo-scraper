# -*- coding:utf-8 -*-

"""
 Author: Helixcs
 Site: https://github.com/Xarrow/weibo-scraper
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

    # def test_weibo_getIndex(self):
    #     """Helixcs need login to get cookies"""
    #     result = weibo_api.weibo_getIndex(uid_value='1843242321')
    #     self.assertIsNotNone(result)

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
        # Helixcs need login to get cookies
        # common weibo id , uid is from Helixcs
        # test_result = get_tweet_containerid(uid="1843242321")
        # print('Containerid from Helixcs is : ', test_result)  # 1076031843242321
        # self.assertIsNotNone(test_result)

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
        print(result)

    def test_get_weibo_tweets_by_name(self):
        result_iterator = weibo_scraper.get_weibo_tweets_by_name(name='嘻红豆', pages=1)
        for i in result_iterator:
            print(i)
        result_iterator2 = weibo_scraper.get_weibo_tweets_by_name(name='nicknameisnotexist', pages=1)
        for i in result_iterator2:
            print(i)

    def test_get_containerid_from_second_profile(self):
        result_iterator = weibo_scraper.get_weibo_tweets_by_name(name='来去之间', pages=1)
        for i in result_iterator:
            print(i)
        self.assertIsNotNone(result_iterator)

    def test_weibo_get_index_parser(self):
        # test get weibo profile
        get_inex_response = weibo_getIndex(uid_value='1111681197')
        wgip = WeiboGetIndexParser(get_index_api_response=get_inex_response)
        print(wgip)

    def test_weibo_parser(self):
        # Helixcs need login to get cookies SUB
        # tweet_response = weibo_scraper.weibo_tweets(containerid='1076031843242321', page=1)
        # wp = WeiboTweetParser(tweet_get_index_response=tweet_response)
        # print(wp)
        pass

    def test_get_weibo_profile(self):
        wp = weibo_scraper.get_weibo_profile(name='嘻红豆')
        print(wp.raw_user_response)

        wp_uid = weibo_scraper.get_weibo_profile(uid='3637346297')
        print(wp_uid.raw_user_response)

    def test_follows_and_followers(self):
        for user in weibo_scraper.get_follows(name='嘻红豆', max_item_limit=1):
            print(user)

        print("==" * 10)
        for user in weibo_scraper.get_followers(name='嘻红豆', max_item_limit=1):
            print(user)

    def test_comments_request_with_structure(self):
        """
        https://m.weibo.cn/comments/hotflow?id=4257059677028285&mid=4257059677028285
        :return:
        """

        weibo_comments_res = weibo_comments(id="4257059677028285", mid='4257059677028285')
        wcp = WeiboCommentParser(weibo_comments_res)
        print(wcp.comment_meta)

    def test_txt_export(self):
        from persistence import persistence
        persistence.dispatch(name='嘻红豆', pages=1, is_simplify=True, persistence_format="txt",
                             export_file_name="梁群茹2txt", is_debug=True)

    def test_weibo_tweets_with_comments(self):
        """weibo comments"""
        for i in weibo_scraper.get_formatted_weibo_tweets_by_name(name='嘻红豆', with_comments=True, pages=1):
            for j in i.cards_node:
                print(str(j.mblog.comment_parser))


if __name__ == '__main__':
    unittest.main()
