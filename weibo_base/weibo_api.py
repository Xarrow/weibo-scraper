# -*- coding:utf-8 -*-

"""
 Author: Helixcs
 Site: https://iliangqunru.bitcron.com/
 File: weibo_api.py
 Time: 5/19/18
"""

import requests
import re
import datetime
from typing import Optional, List

now = datetime.datetime.now()
CURRENT_TIME = now.strftime('%Y-%m-%d %H:%M:%S')
CURRENT_YEAR = now.strftime('%Y')
CURRENT_YEAR_WITH_DATE = now.strftime('%Y-%m-%d')

Response = Optional[dict]

_GET_INDEX = "https://m.weibo.cn/api/container/getIndex"
_GET_SECOND = "https://m.weibo.cn/api/container/getSecond"
_COMMENTS_HOTFLOW = "https://m.weibo.cn/comments/hotflow"


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


def weibo_containerid(containerid: str, page: int) -> Response:
    """

    :param containerid:
    :param page:
    :return:
    """
    _params = {"containerid": containerid, "page": page}
    _response = requests.get(url=_GET_INDEX, params=_params)
    if _response.status_code == 200:
        return _response.json()
    return None


def weibo_second(containerid: str, page: int) -> Response:
    """
    https://m.weibo.cn/api/container/getSecond
    :param containerid:
    :param page:
    :return:
    """
    _params = {"containerid": containerid, "page": page}
    _response = requests.get(url=_GET_SECOND, params=_params)
    if _response.status_code == 200:
        return _response.json()
    return None


def weibo_comments(id: str, mid: str) -> Response:
    """
    https://m.weibo.cn/comments/hotflow?id=4257059677028285&mid=4257059677028285
    get comments from userId and mid
    :param id:          userId
    :param mid:         mid
    :return:
    """
    _params = {"id": id, "mid": mid}
    _response = requests.get(url=_COMMENTS_HOTFLOW, params=_params)
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


# ========== User Metadata ===============

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
               "profile_image_url = {}>".format(repr(self.id), repr(self.screen_name), repr(self.description),
                                                repr(self.gender),
                                                repr(self.avatar_hd), repr(self.profile_image_url))


# ============== Comments Metadata======================

class CommentMeta(object):
    __slots__ = ["single_comment_node"]

    def __init__(self, single_comment_node: _JSONResponse) -> None:
        self.single_comment_node = single_comment_node

    @property
    def raw_single_comment_node(self) -> _JSONResponse:
        return self.single_comment_node

    @property
    def created_at(self) -> _StrFieldResponse:
        return None if self.single_comment_node is None else self.single_comment_node.get("created_at")

    @property
    def id(self) -> _StrFieldResponse:
        return None if self.single_comment_node is None else self.single_comment_node.get("id")

    @property
    def rootid(self) -> _JSONResponse:
        return None if self.single_comment_node is None else self.single_comment_node.get("rootid")

    @property
    def floor_number(self) -> _JSONResponse:
        return None if self.single_comment_node is None else self.single_comment_node.get("floor_number")

    @property
    def text(self) -> _JSONResponse:
        return None if self.single_comment_node is None else self.single_comment_node.get("text")

    @property
    def user(self) -> Optional[UserMeta]:
        return None if self.single_comment_node is None else UserMeta(user_node=self.single_comment_node.get("user"))

    @property
    def mid(self) -> _StrFieldResponse:
        return None if self.single_comment_node is None else self.single_comment_node.get("mid")

    @property
    def comments(self):
        return None if self.single_comment_node is None else self.single_comment_node.get("comments")

    @property
    def max_id(self) -> _IntFieldResponse:
        return None if self.single_comment_node is None else self.single_comment_node.get("max_id")

    @property
    def total_number(self) -> _IntFieldResponse:
        return None if self.single_comment_node is None else self.single_comment_node.get("total_number")

    @property
    def isLikedByMblogAuthor(self):
        return None if self.single_comment_node is None else self.single_comment_node.get("isLikedByMblogAuthor")

    @property
    def bid(self) -> _StrFieldResponse:
        return None if self.single_comment_node is None else self.single_comment_node.get("bid")

    @property
    def source(self) -> _StrFieldResponse:
        return None if self.single_comment_node is None else self.single_comment_node.get("source")

    @property
    def like_count(self) -> _IntFieldResponse:
        return None if self.single_comment_node is None else self.single_comment_node.get("like_count")

    def __repr__(self):
        return r"<CommentMeta id={} , mid = {} , text={} >".format(repr(self.id), repr(self.mid), repr(self.text))


_ListCommentMeta = List[CommentMeta]


class WeiboCommentsParser(object):
    """ weibo comments structure
        sample as :https://m.weibo.cn/comments/hotflow?id=4257059677028285&mid=4257059677028285
    """

    __slots__ = ['comments_node']

    def __init__(self, comments_node: _JSONResponse) -> None:
        self.comments_node = comments_node

    @property
    def outer_data_node(self) -> _JSONResponse:
        if self.comments_node.get("data") is None:
            return None
        return self.comments_node.get("data")

    @property
    def total_number(self) -> _IntFieldResponse:
        return None if self.outer_data_node is None else self.outer_data_node.get("total_number")

    @property
    def comment_meta(self) -> _ListCommentMeta:
        return None if self.outer_data_node is None \
            else [CommentMeta(single_comment_node=single_comment_node)
                  for single_comment_node in self.outer_data_node.get("data")]


class PicMeta(object):
    def __init__(self, pic_node: dict) -> None:
        self.pic_node = pic_node

    @property
    def raw_pics(self) -> _JSONResponse:
        return self.pic_node

    @property
    def pid(self) -> _StrFieldResponse:
        return self.pic_node.get('pid') if self.pic_node.get('pid') is not None else None

    @property
    def url(self) -> _StrFieldResponse:
        return self.pic_node.get("url") if self.pic_node.get("url") is not None else None

    @property
    def large_url(self) -> _StrFieldResponse:
        return self.pic_node.get('large').get('url') if self.pic_node.get('large') is not None else None


class MBlogMeta(object):
    __slots__ = ['mblog_node',]

    def __init__(self, mblog_node):
        self.mblog_node = mblog_node

    @property
    def raw_mblog(self) -> _JSONResponse:
        return self.mblog_node

    @property
    def created_at(self) -> _StrFieldResponse:
        created_at = self.mblog_node.get('created_at')
        # sample as "08-01" -> "2018-08-01"
        if len(created_at) < 9 and "-" in created_at:
            created_at = CURRENT_YEAR + "-" + created_at
        # sample as "几分钟"
        if not str(created_at).__contains__("-"):
            created_at = CURRENT_YEAR_WITH_DATE
        return created_at

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

    @property
    def pics_node(self):
        return [PicMeta(pic) for pic in self.mblog_node.get('pics')] if self.mblog_node.get(
            'pics') is not None else None


class TweetMeta(object):
    """ weibo tweet meta data"""

    __slots__ = ['card_node', '_comment_parser', ]

    def __init__(self, card_node: dict) -> None:
        self.card_node = card_node

    @property
    def raw_card_node(self) -> dict:
        return self.card_node

    @raw_card_node.setter
    def raw_card_node(self ,value:dict):
        self.raw_card_node = value

    @property
    def itemid(self) -> _StrFieldResponse:
        return self.card_node.get('itemid')

    @property
    def scheme(self) -> _StrFieldResponse:
        return self.card_node.get('scheme')

    @property
    def mblog(self) -> MBlogMeta:
        return MBlogMeta(mblog_node=self.card_node.get('mblog'))

    @property
    def comment_parser(self) -> WeiboCommentsParser:
        return self._comment_parser

    @comment_parser.setter
    def comment_parser(self, value: WeiboCommentsParser):
        self._comment_parser = value


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
    __slots__ = ['tweet_containerid', 'tweet_get_index_reponse', '_cards_node']

    def __init__(self, tweet_get_index_response: dict = None, tweet_containerid: str = None) -> None:
        if tweet_get_index_response is None and tweet_containerid is None:
            raise WeiboApiException("WeiboTweetParser#__init__  tweet_get_index_response and tweet_containerid is none !")

        self.tweet_containerid = tweet_containerid

        self.tweet_get_index_reponse = weibo_tweets(containerid=tweet_containerid) \
            if tweet_get_index_response is None and tweet_containerid is not None \
            else tweet_get_index_response

        self._cards_node = [TweetMeta(card_node=card) for card in list(
            filter(lambda card: card.get('card_group') is None, self.tweet_get_index_reponse.get('data').get('cards')))]

    @property
    def raw_tweet_response(self) -> _JSONResponse:
        return self.tweet_get_index_reponse

    @raw_tweet_response
    def raw_tweet_response(self ,value:dict):
        self.tweet_get_index_reponse = value

    @property
    def card_list_info_node(self) -> _JSONResponse:
        return self.tweet_get_index_reponse.get('data').get('cardlistInfo')

    @property
    def cards_node(self) -> _ListTweetMetaFieldResponse:
        # skip  recommended weibo tweet
        return self._cards_node

    @cards_node.setter
    def cards_node(self, value):
        self._cards_node = value

    @property
    def tweet_containerid_node(self) -> _StrFieldResponse:
        return self.card_list_info_node.get('containerid')

    @property
    def total(self) -> _IntFieldResponse:
        return self.card_list_info_node.get('page')

    def __repr__(self):
        return r"<WeiboTweetParser tweet_container_id = {} >".format(repr(self.tweet_containerid_node))


class WeiboGetIndexParser(object):
    __slots__ = ['get_index_api_response', 'uid']

    def __init__(self, get_index_api_response: dict = None, uid: str = None) -> None:
        if get_index_api_response is None and uid is None:
            raise WeiboApiException("In WeiboGetIndexParser , get_index_api_response and uid can not be None . ")
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
            _weibo_containerid = list(filter(lambda tab: tab.get('tab_type') == 'weibo', self.tabs_node))[0].get(
                'containerid')
            if _weibo_containerid.__contains__('WEIBO_SECOND_PROFILE_WEIBO'):
                return re.findall(r'(.+?)WEIBO_SECOND_PROFILE_WEIBO_PAY_BILL',
                                  list(filter(lambda tab: tab.get('tab_type') == 'weibo', self.tabs_node))[0].get(
                                      'containerid'))[0]
            else:
                return _weibo_containerid
        elif isinstance(self.tabs_node, dict):
            _response_include_tweetid = weibo_tweets(containerid=self.profile_containerid, page=0)
            _cards = _response_include_tweetid.get('data').get('cards')
            return re.findall(r'containerid=(.+?)WEIBO_SECOND',
                              list(filter(lambda _card: _card.get('itemid') == 'more_weibo', _cards))[0]
                              .get('scheme'))[0]
        else:
            return None

    @property
    def follow_containerid_second(self):
        return re.findall(r'lfid=(.+?$)', self.scheme_node)[0] + '_-_FANS' if self.scheme_node is not None else None

    @property
    def follower_containerid_second(self):
        return re.findall(r'lfid=(.+?$)', self.scheme_node)[
                   0] + '_-_FOLLOWERS' if self.scheme_node is not None else None

    @property
    def follower_containerid(self):
        return re.findall(r'containerid=(.+?)&luicode', self.fans_scheme_node)[0].replace("_intimacy", "")

    @property
    def follow_containerid(self):
        return re.findall(r'containerid=(.+?)&luicode', self.follow_scheme_node)[0].replace("recomm", "")

    def __repr__(self):
        return r"<WeiboGetIndexParser uid={} >".format(repr(self.user.id))


# ------------------------------- FollowAndFollower ------------------

class FollowAndFollowerParser(object):
    __slots__ = ['follow_and_follower_response', 'follow_and_follower_containerid']

    def __init__(self, follow_and_follower_response: dict, follow_and_follower_containerid: str = None):
        self.follow_and_follower_response = follow_and_follower_response
        self.follow_and_follower_containerid = follow_and_follower_containerid if follow_and_follower_containerid is not None else self.containerid

    @property
    def raw_follow_and_follower_response(self):
        return self.follow_and_follower_response

    @property
    def is_validate(self):
        if self.raw_follow_and_follower_response is None:
            return False
        if self.raw_follow_and_follower_response.get('ok') == 0:
            return False
        return True

    @property
    def data_node(self):
        return self.raw_follow_and_follower_response.get('data') if self.is_validate else None

    @property
    def count(self):
        return self.data_node.get('count') if self.data_node is not None else None

    @property
    def user_list(self):
        if self.data_node is None:
            return None
        return [UserMeta(user_node=card.get('user')) for card in self.data_node.get('cards')]

    @property
    def containerid(self):
        return self.raw_follow_and_follower_response.get('data').get('cardlistInfo').get('containerid')

    def __repr__(self):
        return "<FollowAndFollowerParser container={} >".format(repr(self.containerid))


# ----------------------------------- 前方高能 ---------------------------
HEADER = {
    "Connection": "keep-alive",
    "Host": "passport.weibo.cn",
    "Upgrade-Insecure-Requests": "1",
    "Referer": "https://passport.weibo.cn/signin/login?entry=mweibo&r=http%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt=",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36"
}

AFTER_HEADER = {
    "Accept": "application/json, text/plain, */*",
    "Host": "m.weibo.cn",
    "Origin": "https://m.weibo.cn",
    "Referer": "https://m.weibo.cn/u/",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

PC_HEADER = {
    "Host": "weibo.com",
    "Origin": "https://weibo.com",
    "Referer": "https://weibo.com/ZhangJianForV/home?topnav=1&wvr=6",
    "User-Agent": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.25 (KHTML, like Gecko) Version/11.0 Mobile/15A5304j Safari/604.1",
    "X-Requested-With": "XMLHttpRequest"
}


class WeiboV2(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.request = requests.session()
        self.cookies = None
        self.st = None
        self.userid = None

    def login_for_sso(self):
        login_url = 'https://passport.weibo.cn/sso/login'
        data = {
            'username': self.username,
            'password': self.password,
            'savestate': '1',
            'r': 'http://weibo.cn/',
            'ec': '0',
            'pagerefer': '',
            'entry': 'mweibo',
            'wentry': '',
            'loginfrom': '',
            'client_id': '',
            'code': '',
            'qq': '',
            'mainpageflag': '1',
            'hff': '',
            'hfp': ''
        }
        headers = HEADER
        r_login = self.request.post(url=login_url, data=data, headers=headers)
        if not r_login.text.__contains__('20000000'):
            raise Exception("login_for_sso failed !")

        self.cookies = r_login.cookies.get_dict()

    def get_uid(self):
        """get uid"""
        response = self.request.get(url='https://m.weibo.cn/', cookies=self.cookies)
        if response.status_code == 200 and response.text.__contains__('uid') > 0:
            self.userid = response.text[response.text.index('"uid":"') + len('"uid":"'):response.text.index('","ctrl"')]

    def get_st(self):
        """get st """
        r = self.request.get(url='https://m.weibo.cn/u/' + self.userid, cookies=self.cookies)
        if r.status_code == 200 and r.text.__contains__("st") > 0:
            _response = r.text
            if str(_response).__contains__("st: '") > 0:
                self.st = _response[_response.index("st: '") + len("st: '"):_response.index("',\n            login:")]
            elif str(_response).__contains__('"st":"') > 0:
                self.st = _response[_response.index('"st":"') + len('"st":"'):_response.index('","isInClient')]

    def check_cookie_expired(self):
        """check cookies whether expired"""
        response = self.request.get(url='https://m.weibo.cn/', cookies=self.cookies)
        if response.status_code == 200:
            return response.text.__contains__(self.userid)
        return False

    def check_cookies(self):
        '''check cookie'''
        if self.cookies is None or not self.check_cookie_expired():
            return False
        return True

    def re_login(self):
        """login retry"""
        self.login_for_sso()
        self.get_uid()
        self.get_st()

    def _weibo_getIndex(self, userid):
        """
        微博概要内容API
        https://m.weibo.cn/api/container/getIndex?type=uid&value=3637346297
        :param value:
        :return:
        """
        api = 'http://m.weibo.cn/api/container/getIndex'
        param = {"type": "uid", "value": userid}
        return self.request.get(url=api, params=param)

    def _weibo_content(self, containerid, page=1):
        """
        微博内容API
        1076033637346297
        https://m.weibo.cn/api/container/getIndex?containerid=1076033637346297
        :param containerid:
        :return:
        """
        api = "https://m.weibo.cn/api/container/getIndex"
        params = {"containerid": containerid, "page": page}
        return self.request.get(url=api, params=params)

    def send_words_on_pc(self, word):
        """
        PC端发送微博
        https://weibo.com/aj/mblog/add
        =======================
            title:有什么新鲜事想告诉大家?
            location:v6_content_home
            text:[doge]
            appkey:
            style_type:1
            pic_id:
            tid:
            pdetail:
            rank:0
            rankid:
            pub_source:page_2
            longtext:1
            topic_id:1022:
            pub_type:dialog
            _t:0
        :param word:
        :return:
        """
        api = 'https://weibo.com/aj/mblog/add?ajwvr=6&__rnd=1511200888604'
        data = {
            "title": "有什么新鲜事想告诉大家?",
            "location": "v6_content_home",
            "text": word,
            "appkey": "",
            "style_type": "1",
            "pic_id": "",
            "tid": "",
            "pdetail": "",
            "rank": "0",
            "rankid": "",
            "pub_source": "page_2",
            "longtext": "1",
            "topic_id": "1022:",
            "pub_type": "dialog",
            "_t": 0
        }
        return self.request.post(url=api, data=data, cookies=self.cookies, headers=PC_HEADER).text
