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
import time
import os

from weibo_scraper import get_formatted_weibo_tweets_by_name

level = logging.DEBUG
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
datefmt = '%Y-%m-%d %H:%M'
logging.basicConfig(level=level, format=format, datefmt=datefmt)
logger = logging.getLogger(__name__)

DEFAULT_EXPORT_FILENAME = "export_%s" % int(time.time())
DEFAULT_EXPORT_PATH = os.getcwd()


class WeiboScraperPersistenceException(Exception):
    def __init__(self, message):
        self.message = message


@contextmanager
def open_file(file_name: str):
    file = open(file=file_name, mode='wb')
    yield file
    file.flush()
    file.close()


class BaseAction(object):
    def __init__(self,name:str,pages:int=None):
        if name is None or name == '':
            raise WeiboScraperPersistenceException("JSON persistence need param of 'name' which you want to search!")
        self.name = name
        self.pages = pages

    def execute(self, *args, **kwargs):
        pass


class TweetsPersistence(object):
    def __init__(self, action: BaseAction):
        self.action = action

    def persistence(self, *args, **kwargs):
        # TODO function to AOP
        self.action.execute(*args, **kwargs)


class FilePersistence(BaseAction):
    def execute(self):
        with open_file(file_name='template/小麻花就是我啊.html') as f:
            tweets_iterator = get_formatted_weibo_tweets_by_name(name='小麻花就是我啊', pages=None)
            for tweet_parser in tweets_iterator:
                for tweetMeta in tweet_parser.cards_node:
                    f.write(bytes("=" * 100 + "<br/>" + tweetMeta.mblog.text + "<br/>" + tweetMeta.scheme + "<br/>",
                                  encoding='UTF-8'))
                    if tweetMeta.mblog.pics_node is None:
                        pass
                    else:
                        for pic in tweetMeta.mblog.pics_node:
                            f.write(bytes('=' * 100 + "<br/><img src='" + pic.large_url + "'/><br/>", encoding='utf-8'))


class CSVPersistence(BaseAction):
    """export as csv"""
    pass


class SQLPersistence(BaseAction):
    """ export as SQL"""
    pass


class JSONPersistence(BaseAction):
    """ export as JSON"""

    def __init__(self,
                 export_file_path: str = DEFAULT_EXPORT_PATH,
                 export_file_name: str = DEFAULT_EXPORT_FILENAME + '.json',
                 name: str = None,
                 pages: int = None, ) -> None:
        super().__init__(name,pages)
        self.export_file_path = export_file_path
        self.export_file_name = self.name + "_" + export_file_name

    def execute(self, *args, **kwargs):
        with open_file(file_name=os.path.join(self.export_file_path, self.export_file_name)) as json_file:
            tweets_iterator = get_formatted_weibo_tweets_by_name(name=self.name, pages=self.pages)
            for tweets_parser in tweets_iterator:
                for tweet_meta in tweets_parser.cards_node:
                    json_file.write(bytes(str(tweet_meta.raw_card), encoding='utf-8'))
                    json_file.write(bytes('\t\t\n', encoding='utf-8'))
        pass


# filePst = FilePersistence()
jsonPst = JSONPersistence(name=None, pages=None)
# jsonPst.execute()
tPst = TweetsPersistence(action=jsonPst)
tPst.persistence(pages=1)
