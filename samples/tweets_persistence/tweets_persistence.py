# -*- coding:utf-8 -*-

"""
 Verion: 1.0
 Author: Helixcs
 Site: https://iliangqunru.bitcron.com/
 File: tweets_persistence.py
 Time: 6/9/18
"""
import logging
from contextlib import contextmanager

from weibo_scraper import *

level = logging.DEBUG
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
datefmt = '%Y-%m-%d %H:%M'
logging.basicConfig(level=level, format=format, datefmt=datefmt)
logger = logging.getLogger(__name__)


class BaseAction(object):
    def execute(self):
        pass

class TweetsPersistence(object):
    def __init__(self, action: BaseAction):
        self.action = action

    def persistence(self):
        self.action.execute()


class FilePersistence(BaseAction):
    def execute(self):
        print("file execute")


filePst = FilePersistence()
tPst = TweetsPersistence(action=filePst)
tPst.persistence()

# @contextmanager
# def open_file(file_name: str = r'template/1.html'):
#     file = open(file=file_name, mode='wb+')
#     yield file
#     file.flush()
#     file.close()
#
#
# tweets_iterator = get_formatted_weibo_tweets_by_name(name='嘻红豆', pages=None)
# for tweet_parser in tweets_iterator:
#     for tweetMeta in tweet_parser.cards_node:
#         with open_file() as f:
#             f.write(tweetMeta.mblog.text.encode("utf-8"))
#         print(tweetMeta.mblog.text)


# def get_weibo_follows(name:str=None,)
# import time

# if __name__ == '__main__':
#     startTime = time.time()
#     # weibo_profile = get_weibo_profile(name='嘻红豆',)
#     # print(weibo_profile)
#     #
#     result_iterator = get_formatted_weibo_tweets_by_name(name='嘻红豆', pages=None)
#     for user_meta in result_iterator:
#         for tweetMeta in user_meta.cards_node:
#             print(tweetMeta.mblog.text)
#
#     # from weibo_scraper import  get_weibo_tweets_by_name
#     # for tweet in get_weibo_tweets_by_name(name='崔永元', pages=None):
#     #     print(tweet)
#     endTime = time.time()
#     print(endTime - startTime)
