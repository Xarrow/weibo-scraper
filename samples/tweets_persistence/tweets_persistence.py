# -*- coding:utf-8 -*-

"""
 Verion: 1.0
 Author: Helixcs
 Site: https://iliangqunru.bitcron.com/
 File: tweets_persistence.py
 Time: 6/9/18
 Reference : https://www.toptal.com/python/python-design-patterns
"""
import logging
from contextlib import contextmanager

from weibo_scraper import *

level = logging.DEBUG
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
datefmt = '%Y-%m-%d %H:%M'
logging.basicConfig(level=level, format=format, datefmt=datefmt)
logger = logging.getLogger(__name__)


@contextmanager
def open_file(file_name: str = r'template/weibo_tweets.html'):
    file = open(file=file_name, mode='wb')
    yield file
    file.flush()
    file.close()


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
        with open_file(file_name='template/xihongdou.html') as f:
            tweets_iterator = get_formatted_weibo_tweets_by_name(name='嘻红豆', pages=None)
            for tweet_parser in tweets_iterator:
                for tweetMeta in tweet_parser.cards_node:
                    f.write(bytes("="*100+"<br/>"+tweetMeta.mblog.text + "<br/>"+tweetMeta.scheme+"<br/>", encoding='utf-8'))
                    if tweetMeta.mblog.pics_node is None:
                        pass
                    else:
                        for pic in tweetMeta.mblog.pics_node:
                            f.write(bytes('='*100+"<br/><img src='"+pic.large_url+"'/><br/>",encoding='utf-8'))


filePst = FilePersistence()
tPst = TweetsPersistence(action=filePst)
tPst.persistence()

