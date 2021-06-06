# -*- coding:utf-8 -*-

"""
 Author: helixcs
 Site: https://github.com/Xarrow/weibo-scraper
 File: weibo_scraper.py
 Time: 3/16/18
"""
import datetime
import sys
from typing import Iterator, Optional, List, Dict

from weibo_base.weibo_api import weibo_tweets, weibo_getIndex, weibo_second, weibo_comments, realtime_hotword
from weibo_base.weibo_component import exist_get_uid, get_tweet_containerid
from weibo_base.weibo_parser import \
    WeiboCommentParser, \
    WeiboGetIndexParser, \
    UserMeta, \
    WeiboTweetParser, \
    FollowAndFollowerParser, \
    RealTimeHotWordResponse
from weibo_base.weibo_util import rt_logger, ws_handle, set_debug, WeiboScraperException

try:
    assert sys.version_info.major == 3
    assert sys.version_info.minor >= 6
except AssertionError:
    raise RuntimeError('weibo-scraper requires Python3.6+ !')

now = datetime.datetime.now()
CURRENT_TIME = now.strftime('%Y-%m-%d %H:%M:%S')
CURRENT_YEAR = now.strftime('%Y')
CURRENT_YEAR_WITH_DATE = now.strftime('%Y-%m-%d')

_TweetsResponse = Optional[Iterator[Dict]]
_UserMetaResponse = Optional[UserMeta]
_WeiboGetIndexResponse = Optional[WeiboGetIndexParser]


@ws_handle
def get_weibo_tweets_by_name(name: str, pages: int = None) -> _TweetsResponse:
    """
    Get raw weibo tweets by nick name without any authorization
    >>> from weibo_scraper import  get_weibo_tweets_by_name
    >>> for tweet in get_weibo_tweets_by_name(name='嘻红豆', pages=1):
    >>>     print(tweet)
    :param name: nick name which you want to search
    :param pages: pages ,default all pages
    :return: _TweetsResponse
    """
    if name == '':
        raise WeiboScraperException("`name` can not be blank!")
    res = exist_get_uid(name=name)
    exist = res.get("exist")
    uid = res.get("uid")
    if exist:
        inner_tweet_container_id = get_tweet_containerid(uid=uid)
        yield from get_weibo_tweets(tweet_container_id=inner_tweet_container_id, pages=pages)
    else:
        raise WeiboScraperException("`{name}` can not find!".format(name=name))

@ws_handle
def get_weibo_tweets(tweet_container_id: str, pages: int = None) -> _TweetsResponse:
    """
    Get weibo tweets from mobile without authorization,and this containerid exist in the api of

    Compatibility:
    New Api
    1. Search by Nname and get uid by this api "https://m.weibo.cn/api/container/getIndex?queryVal=来去之间&containerid=100103type%3D3%26q%3D来去之间"
    2. Get profile info by uid , https://m.weibo.cn/api/container/getIndex?type=uid&value=1111681197
    3. https://m.weibo.cn/api/container/getIndex?containerid=2302831111681197
    4. Get weibo tweets by container in node of "tabs" ,https://m.weibo.cn/api/container/getIndex?containerid=2304131111681197_-_&page=6891
    >>> from weibo_scraper import  get_weibo_tweets
    >>> for tweet in get_weibo_tweets(tweet_container_id='1076033637346297',pages=1):
    >>>     print(tweet)
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

@ws_handle
def get_formatted_weibo_tweets_by_name(name: str,
                                       with_comments: bool = False,
                                       pages: int = None) -> _TweetsResponse:
    """
    Get formatted weibo tweets by nick name without any authorization
    >>> from weibo_scraper import  get_formatted_weibo_tweets_by_name
    >>> result_iterator = get_formatted_weibo_tweets_by_name(name='嘻红豆', pages=None)
    >>> for user_meta in result_iterator:
    >>>     for tweetMeta in user_meta.cards_node:
    >>>         print(tweetMeta.mblog.text)
    :param name: nick name which you want to search
    :param with_comments , with comments
    :param pages: pages ,default all pages
    :return:  _TweetsResponse
    """
    if name == '':
        raise WeiboScraperException("name can not be blank!")
    egu_res = exist_get_uid(name=name)
    exist = egu_res.get("exist")
    uid = egu_res.get("uid")
    if exist:
        inner_tweet_containerid = get_tweet_containerid(uid=uid)
        yield from get_weibo_tweets_formatted(tweet_container_id=inner_tweet_containerid,
                                              with_comments=with_comments,
                                              pages=pages)
    else:
        raise WeiboScraperException("`{name}` can not find!".format(name=name))

@ws_handle
def get_weibo_tweets_formatted(tweet_container_id: str, with_comments: bool, pages: int = None,
                               max_item_limit: int = None) -> _TweetsResponse:
    """
    Get weibo formatted tweets by container id

    Compatibility:
    New Api
    1. Get uid by searching name via "https://m.weibo.cn/api/container/getIndex?queryVal=来去之间&containerid=100103type%3D3%26q%3D来去之间"
    2. Get weibo profile containerid by uid via "https://m.weibo.cn/api/container/getIndex?type=uid&value=1111681197"
    3. Get weibo tweet containerid by profile containerid via "https://m.weibo.cn/api/container/getIndex?containerid=2302831111681197"
    3. Get weibo tweets by weet containerid via "https://m.weibo.cn/api/container/getIndex?containerid=2304131111681197_-_&page=6891"
    >>> from weibo_scraper import  get_weibo_tweets_formatted
    >>> for tweet in get_weibo_tweets_formatted(tweet_container_id='1076033637346297',pages=1):
    >>>     print(tweet)
    :param max_item_limit:
    :param with_comments:
    :param tweet_container_id:  request weibo tweets directly by tweet_container_id
    :param pages :default None
    :return _TweetsResponse
    """
    # TODO max items limit
    current_total_item = 0

    def weibo_tweets_gen(_inner_current_page=1):
        while True:
            if pages is not None and _inner_current_page > pages:
                break
            tweet_response_json = weibo_tweets(containerid=tweet_container_id, page=_inner_current_page)
            # skip bad request
            if tweet_response_json is None:
                continue
            elif tweet_response_json.get("ok") != 1:
                break
            weibo_tweet_parser = WeiboTweetParser(tweet_get_index_response=tweet_response_json)
            yield weibo_tweet_parser
            _inner_current_page += 1

    def weibo_comments_gen():
        wtg = weibo_tweets_gen()
        for i in wtg:
            for j in i.cards_node:
                id = j.mblog.id
                mid = j.mblog.mid
                global comment_response
                try:
                    comment_response = weibo_comments(id=id, mid=mid)
                    tweet_comment_parser = WeiboCommentParser(comment_response)
                    j.mblog.comment_parser = tweet_comment_parser
                except Exception as ex:
                    logger.error(
                        "#get_weibo_tweets_formatted.weibo_comments_gen request weibo comment occurred an exception, ex=%s,comment_response=%s" % (
                            ex, comment_response))
                    j.mblog.comment_parser = None
                    pass
            yield i

    if with_comments:
        yield from weibo_comments_gen()
    else:
        yield from weibo_tweets_gen()


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

@ws_handle
def get_weibo_profile(name: str = None, uid: str = None) -> _UserMetaResponse:
    """
    Get weibo profile
    >>> from weibo_scraper import get_weibo_profile
    >>> weibo_profile = get_weibo_profile(name='嘻红豆',)
    :param uid: uid
    :param name: name
    :return: UserMeta
    """
    weibo_get_index_parser_response = weibo_get_index_parser(name=name, uid=uid)
    return weibo_get_index_parser_response.user if weibo_get_index_parser_response is not None else None


FOLLOWER_FLAG = 1

FOLLOW_FLAG = 0


def get_follows_and_followers(name: str = None,
                              uid: str = None,
                              pages: int = None,
                              invoke_flag: int = FOLLOW_FLAG):
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
        yield []
    else:
        yield from gen_follows_and_followers()


def get_follows(name: str = None, uid: str = None, pages: int = None, max_item_limit: int = None):
    """

    :param max_item_limit:
    :param name:
    :param uid:
    :param pages:
    :return:
    """
    current_total_pages = 0
    follows_iterator = get_follows_and_followers(name=name, uid=uid, pages=pages)
    for follow in follows_iterator:
        if follow is None:
            yield None
        else:
            for user in follow.user_list:
                if max_item_limit is not None and current_total_pages >= max_item_limit:
                    return
                yield user
                current_total_pages += 1


def get_followers(name: str = None,
                  uid: str = None,
                  pages: int = None,
                  max_item_limit: int = None):
    """
    Get weibo follower by name, 粉丝
    XIHONGDOU's fans
    https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_3637346297&page=0
    https://m.weibo.cn/api/container/getSecond?containerid=1005053637346297_-_FOLLOWERS&page=0

    :param max_item_limit:
    :param pages:
    :param uid:
    :param name:
    :return:

    """
    current_total_pages = 0
    followers_iterator = get_follows_and_followers(name=name, uid=uid, pages=pages, invoke_flag=1)
    for follower in followers_iterator:
        if follower is None:
            yield None
        else:
            for user in follower.user_list:
                if max_item_limit is not None and current_total_pages >= max_item_limit:
                    return
                yield user
                current_total_pages += 1


@ws_handle
def get_realtime_hotwords() -> List[RealTimeHotWordResponse]:
    """
    get real time hot words
    """
    hot_words = realtime_hotword()
    if None is hot_words:
        return []

    index = 1
    response = []
    for item in hot_words.get('data').get('cards')[0].get('card_group'):
        if item.get('promotion'):
            continue
        rthr = RealTimeHotWordResponse()
        rthr.sequence = index
        rthr.desc = item.get('desc')
        rthr.hot = 0 if item.get('desc_extr') is None else item.get('desc_extr')
        rthr.url = item.get('scheme')
        response.append(rthr)
        index += 1

    return response
# -------------------- simplify method name ----------------
