# -*- coding:utf-8 -*-

"""
 Author: Helixcs
 Site: https://iliangqunru.bitcron.com/
 File: weibo_api.py
 Time: 5/19/18
"""

import requests
import re
from typing import Optional, List

Response = Optional[dict]

_GET_INDEX = "https://m.weibo.cn/api/container/getIndex"


class WeiboApiException(Exception):
    def __init__(self, message):
        self.message = message


def search_by_name(name: str) -> Response:
    """get summary info which searched by name,
     this api is like 'https://m.weibo.cn/api/container/getIndex?queryVal=<name sample as Helixcs>&containerid=100103type%3D3%26q%3D<name sample as Helixcs>'

    >>> from weibo_base import search_by_name
    >>> _response = search_by_name('Helixcs')
     :param name: nick name which you want to search
     :return json string including summary info
    """
    _params = {'queryVal': name, 'containerid': '100103type%3D3%26q%3D' + name}
    _response = requests.get(url=_GET_INDEX, params=_params)
    if _response.status_code == 200:
        return _response.json()
    return None


def weibo_getIndex(uid_value: str) -> Response:
    """
    get personal summary info which request by uid, and uid is got by 'search_by_name'
    this api is like 'https://m.weibo.cn/api/container/getIndex?type=uid&value=<uid_value sample as 1843242321>'

    >>> from weibo_base import  weibo_getIndex
    >>> _response = weibo_getIndex('1843242321')
    :param uid_value:
    :return:
    """
    _params = {"type": "uid", "value": uid_value}
    _response = requests.get(url=_GET_INDEX, params=_params)
    if _response.status_code == 200:
        return _response.json()
    return None


def weibo_tweets(containerid: str, page: int) -> Response:
    """
    get person weibo tweets which from contaninerid in page,
    this api is like 'https://m.weibo.cn/container/getIndex?containerid=<containerid>&page=<page>'
    >>> from weibo_base import  weibo_tweets
    >>> _response = weibo_tweets(contaierid='1076031843242321',page=1)
    :param containerid:
    :param page: page
    :return:
    """
    _params = {"containerid": containerid, "page": page}
    _response = requests.get(url=_GET_INDEX, params=_params)
    if _response.status_code == 200:
        return _response.json()
    return None


# =========== api component ==============


def exist_get_uid(search_by_name_response: str = None, name: str = "") -> dict:
    """
    whether name is exist in response which from search api, if exist ,return uid
    :param search_by_name_response:
    :param name:
    :return:
    """
    if not search_by_name_response or str(search_by_name_response) == '':
        search_by_name_response = search_by_name(name)
    # bad request
    if search_by_name_response.get('ok') != 1:
        return {"exist": False, "name": name, "uid": None}
    card_type = [card for card in search_by_name_response.get("data").get("cards") if card.get('card_type') == 11]
    if len(card_type) < 1:
        return {"exist": False, "name": name, "uid": None}

    user = card_type[0].get('card_group')[0].get('user')
    screen_name = user.get('screen_name')
    if screen_name == name:
        return {"exist": True, "name": name, "uid": user.get('id')}
    return {"exist": False, "name": name, "uid": None}


def get_tweet_containerid(weibo_get_index_response: str = None, uid: str = ""):
    """
    get weibo_containerid
    :param weibo_get_index_response:
    :param uid: uid
    :return: weibo_containerid
    """

    if weibo_get_index_response is None or str(weibo_get_index_response) == '':
        weibo_get_index_response = weibo_getIndex(uid)
    if weibo_get_index_response.get('ok') != 1:
        return None

    weibo_get_index_parser = WeiboGetIndexParser(get_index_api_response=weibo_get_index_response)
    return weibo_get_index_parser.tweet_containerid


# =========== Parser =====================


_JSONResponse = Optional[dict]
_StrFieldResponse = Optional[str]
_IntFieldResponse = Optional[int]


class UserMeta(object):
    """weibo user meta data """

    def __init__(self, user_node: dict):
        self.user_node = user_node

    @property
    def raw_user_response(self) -> _JSONResponse:
        return self.user_node

    @property
    def id(self) -> _StrFieldResponse:
        return self.user_node.get('id')

    @property
    def screen_name(self) -> _StrFieldResponse:
        return self.user_node.get('screen_name')

    @property
    def profile_image_url(self) -> _StrFieldResponse:
        return self.user_node.get('profile_image_url')

    @property
    def profile_url(self) -> _StrFieldResponse:
        return self.user_node.get('profile_url')

    @property
    def description(self) -> _StrFieldResponse:
        return self.user_node.get('description')

    @property
    def gender(self) -> _StrFieldResponse:
        return self.user_node.get('gender')

    @property
    def followers_count(self) -> _IntFieldResponse:
        return self.user_node.get('followers_count')

    @property
    def follow_count(self) -> _IntFieldResponse:
        return self.user_node.get('follow_count')

    @property
    def cover_image_phone(self) -> _StrFieldResponse:
        return self.user_node.get('cover_image_phone')

    @property
    def avatar_hd(self) -> _StrFieldResponse:
        return self.user_node.get('avatar_hd')

    def __repr__(self):
        return "<UserMeta uid={} , screen_name={} , description={} , gender={} , avatar_hd={} ," \
               "profile_image_url = {}>".format(repr(self.id),repr(self.screen_name),repr(self.description),repr(self.gender),
                                                repr(self.avatar_hd),repr(self.profile_image_url))


class MBlogMeta(object):
    def __init__(self, mblog_node):
        self.mblog_node = mblog_node

    @property
    def raw_mblog(self) -> _JSONResponse:
        return self.mblog_node

    @property
    def created_at(self) -> _StrFieldResponse:
        return self.mblog_node.get('created_at')

    @property
    def id(self) -> _StrFieldResponse:
        return self.mblog_node.get('id')

    @property
    def idstr(self) -> _StrFieldResponse:
        return self.mblog_node.get('idstr')

    @property
    def mid(self) -> _StrFieldResponse:
        return self.mblog_node.get('mid')

    @property
    def text(self) -> _StrFieldResponse:
        return self.mblog_node.get('text')

    @property
    def source(self) -> _StrFieldResponse:
        return self.mblog_node.get('source')

    @property
    def user(self) -> UserMeta:
        return UserMeta(user_node=self.mblog_node.get('user'))

    @property
    def retweeted_status(self):
        return MBlogMeta(mblog_node=self.mblog_node.get('retweeted_status')) if self.mblog_node.get(
            'retweeted_status') else None

    @property
    def reposts_count(self) -> _IntFieldResponse:
        return self.mblog_node.get('reposts_count')

    @property
    def comments_count(self) -> _IntFieldResponse:
        return self.mblog_node.get('comments_count')

    @property
    def obj_ext(self) -> _StrFieldResponse:
        return self.mblog_node.get('obj_ext')

    @property
    def raw_text(self) -> _StrFieldResponse:
        return self.mblog_node.get('raw_text')

    @property
    def bid(self) -> _StrFieldResponse:
        return self.mblog_node.get('bid')


class TweetMeta(object):
    """ weibo tweet meta data"""

    def __init__(self, card_node: dict) -> None:
        self.card_node = card_node

    @property
    def raw_card(self) -> dict:
        return self.card_node

    @property
    def itemid(self) -> _StrFieldResponse:
        return self.card_node.get('itemid')

    @property
    def scheme(self) -> _StrFieldResponse:
        return self.card_node.get('scheme')

    @property
    def mblog(self) -> MBlogMeta:
        return MBlogMeta(mblog_node=self.card_node.get('mblog'))


_ListTweetMetaFieldResponse = List[TweetMeta]

"""
- data:
    - cardlistInfo:
        - containerid
        
    - cards: 
        - mblog:
            - retweeted_status
                ....
            - user
                .... 
"""


class WeiboTweetParser(object):
    def __init__(self, tweet_get_index_response: dict = None, tweet_containerid: str = None) -> None:
        self.tweet_containerid = tweet_containerid
        self.tweet_get_index_reponse = weibo_tweets(containerid=tweet_containerid) \
            if tweet_get_index_response is None and tweet_containerid is not None else tweet_get_index_response

    @property
    def raw_tweet_response(self) -> _JSONResponse:
        return self.tweet_get_index_reponse

    @property
    def card_list_info_node(self) -> _JSONResponse:
        return self.tweet_get_index_reponse.get('data').get('cardlistInfo')

    @property
    def cards_node(self) -> _ListTweetMetaFieldResponse:
        # skip  recommended weibo tweet
        return [TweetMeta(card_node=card) for card in list(filter(lambda card:card.get('card_group') is None,self.tweet_get_index_reponse.get('data').get('cards')))]

    @property
    def tweet_containerid_node(self) -> _StrFieldResponse:
        return self.card_list_info_node.get('containerid')

    @property
    def total(self) -> _IntFieldResponse:
        return self.card_list_info_node.get('page')

    def __repr__(self):
        return r"<WeiboTweetParser tweet_container_id = {} >".format(repr(self.tweet_containerid_node))


class WeiboGetIndexParser(object):
    def __init__(self, get_index_api_response: dict = None, uid: str = None) -> None:
        if get_index_api_response is None and uid is None:
            raise WeiboApiException ("In WeiboGetIndexParser , get_index_api_response and uid can not be None . ")
        elif get_index_api_response is not None:
            self.get_index_api_response = get_index_api_response
            self.uid = self.user_info_node.get('id')
        elif uid is not None:
            self.uid = uid
            self.get_index_api_response = weibo_getIndex(uid_value=self.uid)

    @property
    def raw_response(self) -> _JSONResponse:
        return self.get_index_api_response

    @property
    def user_info_node(self) -> _JSONResponse:
        return self.get_index_api_response.get('data').get('userInfo')

    @property
    def tabs_node(self) -> _JSONResponse:
        return self.get_index_api_response.get('data').get('tabsInfo').get('tabs')

    @property
    def fans_scheme_node(self) -> str:
        return self.get_index_api_response.get('data').get('fans_scheme')

    @property
    def follow_scheme_node(self) -> str:
        return self.get_index_api_response.get('data').get('follow_scheme')

    @property
    def scheme_node(self) -> _StrFieldResponse:
        return self.get_index_api_response.get('data').get('scheme')

    @property
    def user(self):
        """structure is similary with user"""
        return UserMeta(user_node=self.user_info_node)

    @property
    def profile_containerid(self) -> _StrFieldResponse:
        # weibo second profile api
        if isinstance(self.tabs_node, dict):
            return self.tabs_node.get('0').get('containerid')
        # weibo first profile api
        elif isinstance(self.tabs_node, list):
            return list(filter(lambda item: item.get('tab_type') == 'profile', self.tabs_node))[0].get('containerid')
        return None

    @property
    def weibo_containerid(self) -> _StrFieldResponse:
        # weibo second profile api
        if isinstance(self.tabs_node, dict):
            return self.tabs_node.get('1').get('containerid')
        # weibo first profile api
        elif isinstance(self.tabs_node, list):
            return list(filter(lambda item: item.get('tab_type') == 'weibo', self.tabs_node))[0]
        return None

    # this property is not exist in first weibo profile api
    @property
    def album_containerid(self) -> _StrFieldResponse:
        return self.tabs_node.get('3').get('containerid') if isinstance(self.tabs_node, dict) else None

    # two sample api
    # https://m.weibo.cn/api/container/getIndex?type=uid&value=1111681197
    # https://m.weibo.cn/api/container/getIndex?type=uid&value=1843242321
    @property
    def tweet_containerid(self):
        if isinstance(self.tabs_node, list):
            _weibo_containerid =  list(filter(lambda tab: tab.get('tab_type') == 'weibo', self.tabs_node))[0].get('containerid')
            if _weibo_containerid.__contains__('WEIBO_SECOND_PROFILE_WEIBO'):
                return re.findall(r'(.+?)WEIBO_SECOND_PROFILE_WEIBO_PAY_BILL',list(filter(lambda tab: tab.get('tab_type') == 'weibo', self.tabs_node))[0].get('containerid'))[0]
            else:
                return _weibo_containerid
        elif isinstance(self.tabs_node, dict):
            _response_include_tweetid = weibo_tweets(containerid=self.profile_containerid, page=0)
            _cards = _response_include_tweetid.get('data').get('cards')
            return re.findall(r'containerid=(.+?)WEIBO_SECOND',
                              list(filter(lambda _card: _card.get('itemid') == 'more_weibo', _cards))[0].get('scheme'))[0]
        else:
            return None

    @property
    def follow_containerid(self):
        return re.findall(r'lfid=(.+?$)',self.scheme_node)[0]+'_-_FANS' if self.scheme_node is not None else None
    @property
    def follower_containerid(self):
        return re.findall(r'lfid=(.+?$)',self.scheme_node)[0]+'_-_FOLLOWERS' if self.scheme_node is not None else None

    def __repr__(self):
        return r"<WeiboGetIndexParser uid={} >".format(repr(self.user.id))
