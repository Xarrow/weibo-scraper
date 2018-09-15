# -*- coding:utf-8 -*-

"""
 Author: helixcs
 Site: https://iliangqunru.bitcron.com/
 File: weibo_scraper.py
 Time: 3/16/18
"""
import io
import os
import datetime
import sys
from docopt import docopt
from concurrent.futures import ThreadPoolExecutor
from typing import Iterator, Optional
from weibo_base import exist_get_uid, \
    get_tweet_containerid, weibo_tweets, weibo_getIndex, weibo_second, UserMeta, WeiboTweetParser, WeiboGetIndexParser, \
    FollowAndFollowerParser,rt_logger

try:
    assert sys.version_info.major == 3
    assert sys.version_info.minor >= 6
except AssertionError:
    raise RuntimeError('weibo-scrapy requires Python3.6+ !')

now = datetime.datetime.now()
CURRENT_TIME = now.strftime('%Y-%m-%d %H:%M:%S')
CURRENT_YEAR = now.strftime('%Y')
CURRENT_YEAR_WITH_DATE = now.strftime('%Y-%m-%d')

_TweetsResponse = Optional[Iterator[dict]]
_UserMetaResponse = Optional[UserMeta]
_WeiboGetIndexResponse = Optional[WeiboGetIndexParser]


class WeiBoScraperException(Exception):
    def __init__(self, message):
        self.message = message


def get_weibo_tweets_by_name(name: str, pages: int = None) -> _TweetsResponse:
    """
    Get weibo tweets by nick name without any authorization
    >>> from weibo_scraper import  get_weibo_tweets_by_name
    >>> for tweet in get_weibo_tweets_by_name(name='嘻红豆', pages=1):
    >>>     print(tweet)
    :param name: nick name which you want to search
    :param pages: pages ,default all pages
    :return: _TweetsResponse
    """
    if name == '':
        raise WeiBoScraperException("name from <get_weibo_tweets_by_name> can not be blank!")
    _egu_res = exist_get_uid(name=name)
    exist = _egu_res.get("exist")
    uid = _egu_res.get("uid")
    if exist:
        inner_tweet_containerid = get_tweet_containerid(uid=uid)
        yield from get_weibo_tweets(tweet_container_id=inner_tweet_containerid, pages=pages)
    else:
        yield None


def get_weibo_tweets(tweet_container_id: str, pages: int = None) -> _TweetsResponse:
    """
    Get weibo tweets from mobile without authorization,and this containerid exist in the api of

    Compatibility:
    New Api
    1. Search by Nname and get uid by this api "https://m.weibo.cn/api/container/getIndex?queryVal=来去之间&containerid=100103type%3D3%26q%3D来去之间"
    2. Get profile info by uid , https://m.weibo.cn/api/container/getIndex?type=uid&value=1111681197
    3. https://m.weibo.cn/api/container/getIndex?containerid=2302831111681197
    3. Get weibo tweets by container in node of "tabs" ,https://m.weibo.cn/api/container/getIndex?containerid=2304131111681197_-_&page=6891
    >>> from weibo_scraper import  get_weibo_tweets
    >>> for tweet in get_weibo_tweets(tweet_container_id='1076033637346297',pages=1):
    >>>     print(tweet)
    >>> ....
    :param tweet_container_id:  request weibo tweets directly by tweet_container_id
    :param pages :default None
    :return _TweetsResponse
    """

    # current_page_index = 1

    def gen(_inner_current_page=1):
        while True:
            if pages is not None and _inner_current_page > pages:
                break
            _response_json = weibo_tweets(containerid=tweet_container_id, page=_inner_current_page)
            # skip bad request
            if _response_json is None:
                continue
            # break failed response
            elif _response_json.get("ok") != 1:
                break
            # break end tweet
            elif _response_json.get('data').get("cards")[0].get('name') == '暂无微博':
                break
            _cards = _response_json.get('data').get("cards")
            for _card in _cards:
                # skip recommended tweets
                if _card.get("card_group"):
                    continue
                # just yield field of mblog
                yield _card
            _inner_current_page += 1

    yield from gen()


def get_formatted_weibo_tweets_by_name(name: str, pages: int = None) -> _TweetsResponse:
    """
    Get formatted weibo tweets by nick name without any authorization
    >>> from weibo_scraper import  get_formatted_weibo_tweets_by_name
    >>> result_iterator = get_formatted_weibo_tweets_by_name(name='嘻红豆', pages=None)
    >>> for user_meta in result_iterator:
    >>>     for tweetMeta in user_meta.cards_node:
    >>>         print(tweetMeta.mblog.text)
    :param name: nick name which you want to search
    :param pages: pages ,default all pages
    :return:  _TweetsResponse
    """
    if name == '':
        raise WeiBoScraperException("name from <get_weibo_tweets_by_name> can not be blank!")
    _egu_res = exist_get_uid(name=name)
    exist = _egu_res.get("exist")
    uid = _egu_res.get("uid")
    if exist:
        inner_tweet_containerid = get_tweet_containerid(uid=uid)
        yield from get_weibo_tweets_formatted(tweet_container_id=inner_tweet_containerid, pages=pages)
    else:
        yield None


def get_weibo_tweets_formatted(tweet_container_id: str, pages: int = None) -> _TweetsResponse:

    """
    Get weibo formatted tweets

    Compatibility:
    New Api
    1. Get uid by searching name via "https://m.weibo.cn/api/container/getIndex?queryVal=来去之间&containerid=100103type%3D3%26q%3D来去之间"
    2. Get weibo profile containerid by uid via "https://m.weibo.cn/api/container/getIndex?type=uid&value=1111681197"
    3. Get weibo tweet containerid by profile containerid via "https://m.weibo.cn/api/container/getIndex?containerid=2302831111681197"
    3. Get weibo tweets by weet containerid via "https://m.weibo.cn/api/container/getIndex?containerid=2304131111681197_-_&page=6891"
    >>> from weibo_scraper import  get_weibo_tweets_formatted
    >>> for tweet in get_weibo_tweets_formatted(tweet_container_id='1076033637346297',pages=1):
    >>>     print(tweet)
    >>> ....
    :param tweet_container_id:  request weibo tweets directly by tweet_container_id
    :param pages :default None
    :return _TweetsResponse
    """

    def gen(_inner_current_page=1):
        while True:
            if pages is not None and _inner_current_page > pages:
                break
            _response_json = weibo_tweets(containerid=tweet_container_id, page=_inner_current_page)
            # skip bad request
            if _response_json is None:
                continue
            elif _response_json.get("ok") != 1:
                break
            weibo_tweet_parser = WeiboTweetParser(tweet_get_index_response=_response_json)
            yield weibo_tweet_parser
            _inner_current_page += 1

    yield from gen()


def weibo_get_index_parser(name: str = None, uid: str = None) -> _WeiboGetIndexResponse:
    """
    Get weibo get index parser
    :param name:  name
    :param uid:  uid
    :return: _WeiboGetIndexResponse
    """
    if uid is not None:
        _uid = uid
    elif name is not None:
        _egu_response = exist_get_uid(name=name)
        if not _egu_response.get('exist'):
            return None
        _uid = _egu_response.get('uid')
    else:
        return None
    _weibo_get_index_response_parser = WeiboGetIndexParser(get_index_api_response=weibo_getIndex(uid_value=_uid))
    if _weibo_get_index_response_parser.raw_response is None \
            or _weibo_get_index_response_parser.raw_response.get('data') == 0:
        return None
    return _weibo_get_index_response_parser


def get_weibo_profile(name: str = None, uid: str = None) -> _UserMetaResponse:
    """
    Get weibo profile
    >>> from weibo_scraper import get_weibo_profile
    >>> weibo_profile = get_weibo_profile(name='嘻红豆',)
    >>> ...weibo_profile
    :param uid: uid
    :param name: name
    :return: UserMeta
    """
    weibo_get_index_parser_response = weibo_get_index_parser(name=name, uid=uid)
    return weibo_get_index_parser_response.user if weibo_get_index_parser_response is not None else None


FOLLOWER_FLAG = 1

FOLLOW_FLAG = 0


def get_follows_and_followers(name: str = None, uid: str = None, pages: int = None, invoke_flag: int = FOLLOW_FLAG):

    """
    Get follows and followers by name or uid limit by pages
    :param invoke_flag: 0-follow , 1-follower
    :param name:
    :param uid:
    :param pages:
    :return:
    """

    def gen_follows_and_followers(_inner_current_page=1, _total_items=0):
        while True:
            # stop max pages
            if pages is not None and _inner_current_page > pages:
                break
            if invoke_flag == FOLLOW_FLAG:
                _weibo_follows_and_followers_second_response = weibo_second(
                    containerid=weibo_get_index_parser_response.follow_containerid_second,
                    page=_inner_current_page)
            else:
                _weibo_follows_and_followers_second_response = weibo_second(
                    containerid=weibo_get_index_parser_response.follower_containerid_second,
                    page=_inner_current_page)
            # skip bad request
            if _weibo_follows_and_followers_second_response is None:
                continue
            # stop end page
            if _weibo_follows_and_followers_second_response.get('ok') == 0:
                break
            _follow_and_follower_parser = FollowAndFollowerParser(
                follow_and_follower_response=_weibo_follows_and_followers_second_response)
            yield _follow_and_follower_parser
            _inner_current_page += 1

    weibo_get_index_parser_response = weibo_get_index_parser(name=name, uid=uid)
    if weibo_get_index_parser_response is None:
        yield None
    else:
        yield from gen_follows_and_followers()


def get_follows(name: str = None, uid: str = None, pages: int = None, max_entry_limit: int = None):
    """

    :param max_entry_limit:
    :param name:
    :param uid:
    :param pages:
    :param max_pages_limit:
    :return:
    """
    current_total_pages = 0
    follows_iterator = get_follows_and_followers(name=name, uid=uid, pages=pages)
    for follow in follows_iterator:
        if follow is None:
            yield None
        else:
            for user in follow.user_list:
                if max_entry_limit is not None and current_total_pages >= max_entry_limit:
                    return
                yield user
                current_total_pages += 1


def get_followers(name: str = None, uid: str = None, pages: int = None, max_entry_limit: int = None):
    """
    Get weibo follower by name, 粉丝
    XIHONGDOU's fans
    https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_3637346297&page=0
    https://m.weibo.cn/api/container/getSecond?containerid=1005053637346297_-_FOLLOWERS&page=0

    :param max_entry_limit:
    :param pages:
    :param uid:
    :param name:
    :return:

    """
    current_total_pages = 0
    followers_iterator = get_follows_and_followers(name=name, uid=uid, pages=pages,invoke_flag=1)
    for follower in followers_iterator:
        if follower is None:
            yield None
        else:
            for user in follower.user_list:
                if max_entry_limit is not None and current_total_pages >= max_entry_limit:
                    return
                yield user
                current_total_pages += 1


# -------------------- simplify method name ----------------

def formated_tweets_by_name(*args,**kwargs):
    pass


def say_hi():
    print("Hi")


from samples import  tweets_persistence


def cli():
    """weibo-cli"""
    weibo_scraper_with_version = "weibo-scraper 1.0.6 🚀"
    weibo_scraper_supported_formats = "txt pickle".split()
    formats_lst = ', '.join(weibo_scraper_supported_formats)

    cli_doc = """
Usage:
    weibo-scraper.py -u <name>
    weibo-scraper.py -u <name> --si
    weibo-scraper.py -u <name> [-p <pages>] [-f <format>] [-o <exported_file_path>] [-fname <exported_file_name>] [--si] [--debug] [--more]
    weibo-scraper.py -h [--help]
    weibo-scraper.py -v [--version]
Options:
  -u                           weibo nickname which exported.
  -p --pages                   pages which exported [ default one page ].
  -f --format                  format which exported [ default "txt" , support for %(formats_lst)s ].
  -o                           output file path which expected [ default "current dir" ].
  -fname                       file name which expected .
  -si --simplify               simplify available info [ default "True" ].
  --debug                      open debug mode .
  --more                       show more .
  -h --help                    show this screen .
  -v --version                 show version.
Supported Formats:
   %(formats_lst)s
    """%dict(formats_lst=formats_lst)
    @rt_logger
    def export_to_file():
        arguments = docopt(cli_doc,version=weibo_scraper_with_version)
        name = arguments.get("<name>")
        pages = int(arguments.get("<pages>") or 1)
        format = arguments.get("<format>") or "txt"
        is_simplify = arguments.get("--si") or False
        exported_file_path = arguments.get("<exported_file_path>") or os.getcwd()
        exported_file_name = arguments.get("<exported_file_name>")
        is_debug = arguments.get("--debug") or False
        more = arguments.get("--more")

        if more:
            more_description = weibo_scraper_with_version
            here = os.path.abspath(os.path.dirname(__file__))
            with io.open(os.path.join(here,"README.md"), encoding="UTF-8") as f:
                more_description += "\n" + f.read()
            print(more_description)
            pass
        tweets_persistence.dispatch(name=name,
                                    pages=pages,
                                    is_simplify=is_simplify,
                                    persistence_format=format,
                                    export_file_path=exported_file_path,
                                    export_file_name=exported_file_name,
                                    is_debug=is_debug,)
    export_to_file()


if __name__ == '__main__':
    cli()