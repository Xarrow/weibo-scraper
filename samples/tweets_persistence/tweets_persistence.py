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
import pickle

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
    def __init__(self,
                 name: str,
                 pages: int = None,
                 export_file_path: str = None,
                 export_file_name: str = None,
                 export_file_suffix: str = None,
                 is_simplify: bool = None):
        """
        BaseAction
        :param name:                weibo name which wants to search and persistence
        :param pages:               max pages which requests
        :param export_file_path:    export file path
        :param export_file_name:    export file name
        :param export_file_suffix:  export file suffix , examples : txt , sql , html
        :param is_simplify:         whether export pure weibo tweets
        """
        if name is None or name == '':
            raise WeiboScraperPersistenceException("persistence need param of 'name' which you want to search!")

        self.name = name
        self.pages = pages
        self.export_file_path = export_file_path or DEFAULT_EXPORT_PATH
        self.export_file_name = export_file_name or DEFAULT_EXPORT_FILENAME
        self.export_file_suffix = export_file_suffix or "txt"
        self.export_file_suffix = "." + self.export_file_suffix if not self.export_file_suffix.startswith(
            ".") else self.export_file_suffix
        # reset export_file_name
        # sample as "嘻红豆_export_1534784328.json"
        self.export_file_name = self.name + "_" + self.export_file_name + self.export_file_suffix
        self.is_simplfy = True if is_simplify is None else is_simplify

    def execute(self, *args, **kwargs):
        # 父类执行
        pass


class TweetsPersistence(object):
    def __init__(self, action: BaseAction):
        self.action = action

    def persistence(self, *args, **kwargs):
        # TODO function to AOP
        self.action.execute(*args, **kwargs)


# -------------------------- implement ------------------------

class HTMLPersistence(BaseAction):
    """ export as html file """
    def __init__(self,
                 name: str = None,
                 pages: int = None,
                 export_file_suffix: str = "json",
                 is_simplify:bool = False) -> None:
        super().__init__(name=name,
                         pages=pages,
                         export_file_path=None,
                         export_file_name=None,
                         export_file_suffix=export_file_suffix,
                         is_simplify=is_simplify)




class FilePersistence(BaseAction):
    def __init__(self,
                 name: str = None,
                 pages: int = None,
                 export_file_suffix: str = "txt",
                 is_simplify:bool = False) -> None:
        super().__init__(name=name,
                         pages=pages,
                         export_file_path=None,
                         export_file_name=None,
                         export_file_suffix=export_file_suffix,
                         is_simplify=is_simplify)


    def execute(self):
        with open_file(file_name='template/weibo_scraper_index.html') as f:
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
                 name: str = None,
                 pages: int = None,
                 export_file_suffix: str = "json",
                 is_simplify:bool = False) -> None:
        super().__init__(name=name,
                         pages=pages,
                         export_file_path=None,
                         export_file_name=None,
                         export_file_suffix=export_file_suffix,
                         is_simplify=is_simplify)

    def fetch_data(self,*args,**kwargs):
        tweets_iterator = get_formatted_weibo_tweets_by_name(name=self.name, pages=self.pages)
        for tweets_parser in tweets_iterator:
            for tweet_meta in tweets_parser.cards_node:
                yield tweet_meta

    # more faster
    # 1.2 sec
    def execute(self):
        with open_file(file_name=os.path.join(self.export_file_path,self.export_file_name)) as json_file:
            for tweet_meta in self.fetch_data():
                if self.is_simplfy:
                    single_line = "id: " + tweet_meta.mblog.id + "\t\t" + \
                                  "source: " + tweet_meta.mblog.source + "\t\t" + \
                                  "text: " + tweet_meta.mblog.text + "\t\t"
                    if tweet_meta.mblog.pics_node and len(tweet_meta.mblog.pics_node) > 0:
                        single_line += "pics: "
                        for pic in tweet_meta.mblog.pics_node:
                            single_line = single_line + pic.large_url + "\t\t"
                else:
                    single_line = str(tweet_meta.raw_card)
                json_file.write(bytes(single_line, encoding='utf-8'))
                json_file.write(bytes('\t\t\n', encoding='utf-8'))



    def execute1(self, *args, **kwargs):
        # 重写父类 execute
        #  override
        with open_file(file_name=os.path.join(self.export_file_path, self.export_file_name)) as json_file:
            tweets_iterator = get_formatted_weibo_tweets_by_name(name=self.name, pages=self.pages)
            for tweets_parser in tweets_iterator:
                for tweet_meta in tweets_parser.cards_node:
                    if self.is_simplfy:
                        single_line = "id: " + tweet_meta.mblog.id + "\t\t" + \
                                      "source: " + tweet_meta.mblog.source + "\t\t" + \
                                      "text: " + tweet_meta.mblog.text + "\t\t"
                        if tweet_meta.mblog.pics_node and len(tweet_meta.mblog.pics_node) > 0:
                            single_line += "pics: "
                            for pic in tweet_meta.mblog.pics_node:
                                single_line = single_line + pic.large_url + "\t\t"
                    else:
                        single_line = str(tweet_meta.raw_card)
                    json_file.write(bytes(single_line, encoding='utf-8'))
                    json_file.write(bytes('\t\t\n', encoding='utf-8'))
        pass


start_time = time.time()
# filePst = FilePersistence()
jsonPst = JSONPersistence(name='Linux中国', pages=30,is_simplify=True)
# jsonPst.execute()
tPst = TweetsPersistence(action=jsonPst)
tPst.persistence()
end_time = time.time()
logger.info("%s",(end_time-start_time))
