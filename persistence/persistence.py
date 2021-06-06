# -*- coding:utf-8 -*-

"""
 Verion: 1.0
 Author: Helixcs
 Site: https://github.com/Xarrow/weibo-scraper
 File: persistence.py
 Time: 6/9/18
 Reference : https://www.toptal.com/python/python-design-patterns
"""
import logging
from contextlib import contextmanager
import time
import os
import pickle

from weibo_scraper import get_formatted_weibo_tweets_by_name
from weibo_base import rt_logger,logger,is_debug


DEFAULT_EXPORT_FILENAME = "export_%s" % int(time.time())
DEFAULT_EXPORT_PATH = os.getcwd()
DEFAULT_DOT = "."


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
            raise WeiboScraperPersistenceException("persistence need param of 'name' which you want to search !")

        self.name = name
        self.pages = pages
        self.export_file_path = export_file_path or DEFAULT_EXPORT_PATH
        self.export_file_name = export_file_name
        self.export_file_suffix = export_file_suffix
        self.export_file_suffix = DEFAULT_DOT + self.export_file_suffix if not self.export_file_suffix.startswith(
            DEFAULT_DOT) else self.export_file_suffix

        if self.export_file_path is not None:
            if not os.path.isdir(self.export_file_path):
                raise WeiboScraperPersistenceException("export file path is not a dir !")
        # reset export_file_name
        # sample as "嘻红豆_export_1534784328.json" or custom file name "嘻红豆.txt"
        self.export_file_name = self.export_file_name if self.export_file_name is not None else self.name + "_" + DEFAULT_EXPORT_FILENAME
        self.export_file_name = self.export_file_name + self.export_file_suffix if not self.export_file_name.__contains__(
            DEFAULT_DOT) else self.export_file_name
        self.is_simplfy = True if is_simplify is None else is_simplify

    def fetch_data(self, *args, **kwargs):
        pass

    def execute(self, *args, **kwargs):
        # 父类执行
        pass


class WeiboTweetsAction(BaseAction):
    """ weibo tweets action"""

    def fetch_data(self, *args, **kwargs):
        tweets_iterator = get_formatted_weibo_tweets_by_name(name=self.name, pages=self.pages)
        for tweets_parser in tweets_iterator:
            for tweet_meta in tweets_parser.cards_node:
                yield tweet_meta


class WeiboFollowerAndFansAction(BaseAction):
    """ weibo followers and fans action"""

    def fetch_data(self, *args, **kwargs):
        pass


class TweetsPersistence(object):
    def __init__(self, action: BaseAction):
        self.action = action

    @rt_logger
    def execute_with_de(self, *args, **kwargs):
        self.action.execute(*args, **kwargs)

    def persistence(self, *args, **kwargs):
        # TODO function to AOP
        if is_debug:
            self.execute_with_de(*args, **kwargs)
        else:
            self.action.execute(*args, **kwargs)


# -------------------------- implement ------------------------

class HTMLPersistenceImpl(WeiboTweetsAction):
    """ export as html file """

    def __init__(self,
                 name: str = None,
                 pages: int = None,
                 export_file_path=None,
                 export_file_name=None,
                 export_file_suffix: str = "html",
                 is_simplify: bool = False) -> None:
        super().__init__(name=name,
                         pages=pages,
                         export_file_path=export_file_path,
                         export_file_name=export_file_name,
                         export_file_suffix=export_file_suffix,
                         is_simplify=is_simplify)

    def execute(self, *args, **kwargs):
        #  do nothing
        pass


class SerializablePersistenceImpl(WeiboTweetsAction):
    def __init__(self,
                 name: str = None,
                 pages: int = None,
                 export_file_path=None,
                 export_file_name=None,
                 export_file_suffix: str = "pickle",
                 is_simplify: bool = False) -> None:
        super().__init__(name=name,
                         pages=pages,
                         export_file_path=export_file_path,
                         export_file_name=export_file_name,
                         export_file_suffix=export_file_suffix,
                         is_simplify=is_simplify)

    def execute(self, *args, **kwargs):
        with open_file(file_name=os.path.join(self.export_file_path, self.export_file_name)) as pickle_file:
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
                single_line += "\t\t\n"
                pickle.dump(single_line, pickle_file)
        pass


class TxtPersistenceImpl(WeiboTweetsAction):
    """ export as txt file """

    def __init__(self,
                 name: str = None,
                 pages: int = None,
                 export_file_path=None,
                 export_file_name=None,
                 export_file_suffix: str = "txt",
                 is_simplify: bool = False) -> None:
        super().__init__(name=name,
                         pages=pages,
                         export_file_path=export_file_path,
                         export_file_name=export_file_name,
                         export_file_suffix=export_file_suffix,
                         is_simplify=is_simplify)

    def execute(self):
        with open_file(file_name=os.path.join(self.export_file_path, self.export_file_name)) as text_file:
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
                    # FIXME  upgrade weibo_base.py
                    single_line = str(tweet_meta.raw_card_node)

                single_line += "\t\t\n"
                text_file.write(bytes(single_line, encoding='utf-8'))


class CSVPersistenceImpl(BaseAction):
    """export as csv file"""
    pass


class SQLPersistenceImpl(BaseAction):
    """ export as sql file """
    pass


class JSONPersistenceImpl(WeiboTweetsAction):
    """ export as json file"""

    def __init__(self,
                 name: str = None,
                 pages: int = None,
                 export_file_path=None,
                 export_file_name=None,
                 export_file_suffix: str = "json",
                 is_simplify: bool = False) -> None:
        super().__init__(name=name,
                         pages=pages,
                         export_file_path=export_file_path,
                         export_file_name=export_file_name,
                         export_file_suffix=export_file_suffix,
                         is_simplify=is_simplify)

    def execute(self):
        with open_file(file_name=os.path.join(self.export_file_path, self.export_file_name)) as json_file:
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


def dispatch(name: str, pages: int = None, is_simplify: bool = True, persistence_format: str = "txt",
             export_file_path: str = None, export_file_name: str = None, is_debug: bool = False):
    # if not is_debug:
    #     logger.getLogger().setLevel(logging.DEBUG)
    if persistence_format == 'txt':
        pst = TxtPersistenceImpl(name=name, pages=pages, is_simplify=is_simplify, export_file_path=export_file_path,
                                 export_file_name=export_file_name)
    elif persistence_format == 'sql':
        pst = SQLPersistenceImpl(name=name, pages=pages, is_simplify=is_simplify, export_file_path=export_file_path,
                                 export_file_name=export_file_name)
    elif persistence_format == 'html':
        pst = HTMLPersistenceImpl(name=name, pages=pages, is_simplify=is_simplify, export_file_path=export_file_path,
                                  export_file_name=export_file_name)
    elif persistence_format == 'csv':
        pst = CSVPersistenceImpl(name=name, pages=pages, is_simplify=is_simplify, export_file_path=export_file_path,
                                 export_file_name=export_file_name)
    elif persistence_format == 'pickle':
        pst = SerializablePersistenceImpl(name=name, pages=pages, is_simplify=is_simplify,
                                          export_file_path=export_file_path, export_file_name=export_file_name)
    elif persistence_format == 'json':
        pst = JSONPersistenceImpl(name=name, pages=pages, is_simplify=is_simplify, export_file_path=export_file_path,
                                  export_file_name=export_file_name)
    else:
        raise WeiboScraperPersistenceException("Unknown persistence format in [txt, sql ,html, csv, pickle]")
    tpst = TweetsPersistence(action=pst)
    tpst.persistence()
