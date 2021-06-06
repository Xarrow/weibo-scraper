# -*- coding:utf-8 -*-

"""
 Verion: 1.0
 Author: Helixcs
 Site: https://github.com/Xarrow/weibo-scraper
 File: weibo_parser.py
 Time: 11/25/18
"""

import datetime
import re

from weibo_base.weibo_util import logger
from weibo_base.weibo_api import weibo_tweets, weibo_getIndex, WeiboApiException, weibo_comments
from weibo_base.weibo_typing import _JSONResponse, _StrFieldResponse, _IntFieldResponse
from typing import List, Optional

now = datetime.datetime.now()
CURRENT_TIME = now.strftime('%Y-%m-%d %H:%M:%S')
CURRENT_YEAR = now.strftime('%Y')
CURRENT_YEAR_WITH_DATE = now.strftime('%Y-%m-%d')


# ========== User Metadata ===============
class BaseParser(object):
    def __init__(self, raw_response: dict):
        self._get_time = CURRENT_TIME
        self._raw_response = raw_response

    @property
    def raw_response(self) -> _JSONResponse:
        return self._raw_response


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
    __slots__ = ["_comment_meta"]

    def __init__(self, comment_meta: _JSONResponse) -> None:
        self._comment_meta = comment_meta

    @property
    def raw_comment_meta(self) -> _JSONResponse:
        return self._comment_meta

    @raw_comment_meta.setter
    def raw_comment_meta(self, value: _JSONResponse):
        self._comment_meta = value

    @property
    def created_at(self) -> _StrFieldResponse:
        return None if self._comment_meta is None else self._comment_meta.get("created_at")

    @property
    def id(self) -> _StrFieldResponse:
        return None if self._comment_meta is None else self._comment_meta.get("id")

    @property
    def rootid(self) -> _JSONResponse:
        return None if self._comment_meta is None else self._comment_meta.get("rootid")

    @property
    def floor_number(self) -> _JSONResponse:
        return None if self._comment_meta is None else self._comment_meta.get("floor_number")

    @property
    def text(self) -> _JSONResponse:
        return None if self._comment_meta is None else self._comment_meta.get("text")

    @property
    def user(self) -> Optional[UserMeta]:
        return None if self._comment_meta is None else UserMeta(user_node=self._comment_meta.get("user"))

    @property
    def mid(self) -> _StrFieldResponse:
        return None if self._comment_meta is None else self._comment_meta.get("mid")

    @property
    def comments(self):
        return None if self._comment_meta is None else self._comment_meta.get("comments")

    @property
    def max_id(self) -> _IntFieldResponse:
        return None if self._comment_meta is None else self._comment_meta.get("max_id")

    @property
    def total_number(self) -> _IntFieldResponse:
        return None if self._comment_meta is None else self._comment_meta.get("total_number")

    @property
    def isLikedByMblogAuthor(self):
        return None if self._comment_meta is None else self._comment_meta.get("isLikedByMblogAuthor")

    @property
    def bid(self) -> _StrFieldResponse:
        return None if self._comment_meta is None else self._comment_meta.get("bid")

    @property
    def source(self) -> _StrFieldResponse:
        return None if self._comment_meta is None else self._comment_meta.get("source")

    @property
    def like_count(self) -> _IntFieldResponse:
        return None if self._comment_meta is None else self._comment_meta.get("like_count")

    def __repr__(self):
        return r"<CommentMeta id={} , mid = {} , text={} >".format(repr(self.id), repr(self.mid), repr(self.text))


_ListCommentMeta = List[CommentMeta]


class WeiboCommentParser(object):
    """ weibo comments structure
        sample as :https://m.weibo.cn/comments/hotflow?id=4257059677028285&mid=4257059677028285
    """

    __slots__ = ['_comment_node']

    def __init__(self, comment_node: _JSONResponse) -> None:
        self._comment_node = comment_node

    @property
    def raw_comment_node(self):
        return self._comment_node

    @raw_comment_node.setter
    def raw_comment_node(self, value: _JSONResponse):
        self._comment_node = value

    @property
    def outer_data_node(self) -> _JSONResponse:
        if self._comment_node is None: return None
        if self._comment_node.get("data") is None:
            return None
        return self._comment_node.get("data")

    @property
    def total_number(self) -> _IntFieldResponse:
        return None if self.outer_data_node is None else self.outer_data_node.get("total_number")

    @property
    def comment_meta(self) -> _ListCommentMeta:
        return None if self.outer_data_node is None \
            else [CommentMeta(comment_meta=single_comment_node)
                  for single_comment_node in self.outer_data_node.get("data")]

    def __repr__(self):
        return r"<WeiboCommentParser raw_comment_node={} >".format(repr(self.raw_comment_node))


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
    __slots__ = ['_mblog_node', '_comment_parser']

    def __init__(self, mblog_node):
        self._mblog_node = mblog_node
        self._comment_parser = None

    @property
    def raw_mblog_node(self) -> _JSONResponse:
        return self._mblog_node

    @raw_mblog_node.setter
    def raw_mblog_node(self, value: _JSONResponse):
        self._mblog_node = value

    @property
    def comment_parser(self) -> WeiboCommentParser:
        return self._comment_parser

    @comment_parser.setter
    def comment_parser(self, value: WeiboCommentParser):
        if value is None:
            global comment_response
            try:
                comment_response = weibo_comments(id=self.id, mid=self.mid)
                self._comment_parser = WeiboCommentParser(comment_response)
            except Exception as ex:
                logger.error(
                    "MBlogMeta#comment_parser(settler) value is None , request weibo comments occurred an exception,"
                    "ex=%s , comment_response=%s" % (ex, comment_response))
                self._comment_parser = None
        else:
            self._comment_parser = value

    @property
    def created_at(self) -> _StrFieldResponse:
        created_at = self._mblog_node.get('created_at')
        # sample as "08-01" -> "2018-08-01"
        if len(created_at) < 9 and "-" in created_at:
            created_at = CURRENT_YEAR + "-" + created_at
        # sample as "几分钟"
        if not str(created_at).__contains__("-"):
            created_at = CURRENT_YEAR_WITH_DATE
        return created_at

    @property
    def id(self) -> _StrFieldResponse:
        return self._mblog_node.get('id') if self._mblog_node is not None else None

    @property
    def idstr(self) -> _StrFieldResponse:
        return self._mblog_node.get('idstr') if self._mblog_node is not None else None

    @property
    def mid(self) -> _StrFieldResponse:
        return self._mblog_node.get('mid') if self._mblog_node is not None else None

    @property
    def text(self) -> _StrFieldResponse:
        return self._mblog_node.get('text') if self._mblog_node is not None else None

    @property
    def source(self) -> _StrFieldResponse:
        return self._mblog_node.get('source') if self._mblog_node is not None else None

    @property
    def user(self) -> UserMeta:
        return UserMeta(user_node=self._mblog_node.get('user')) if self._mblog_node is not None else None

    @property
    def retweeted_status(self):
        return MBlogMeta(mblog_node=self._mblog_node.get('retweeted_status')) \
            if self._mblog_node.get('retweeted_status') else None

    @property
    def reposts_count(self) -> _IntFieldResponse:
        return self._mblog_node.get('reposts_count') if self._mblog_node is not None else None

    @property
    def comments_count(self) -> _IntFieldResponse:
        return self._mblog_node.get('comments_count') if self._mblog_node is not None else None

    @property
    def obj_ext(self) -> _StrFieldResponse:
        return self._mblog_node.get('obj_ext') if self._mblog_node is not None else None

    @property
    def raw_text(self) -> _StrFieldResponse:
        return self._mblog_node.get('raw_text') if self._mblog_node is not None else None

    @property
    def bid(self) -> _StrFieldResponse:
        return self._mblog_node.get('bid') if self._mblog_node is not None else None

    @property
    def pics_node(self):
        return [PicMeta(pic) for pic in self._mblog_node.get('pics')] \
            if self._mblog_node.get('pics') is not None else None


class TweetMeta(object):
    """ weibo tweet meta data"""

    __slots__ = ['_card_node', '_mblog']

    def __init__(self, card_node: dict) -> None:
        self._card_node = card_node
        self._mblog = MBlogMeta(mblog_node=self._card_node.get('mblog')) if self._card_node is not None else None

    @property
    def raw_card_node(self) -> dict:
        return self._card_node

    @raw_card_node.setter
    def raw_card_node(self, value: dict):
        self._card_node = value

    @property
    def itemid(self) -> _StrFieldResponse:
        return self._card_node.get('itemid') if self._card_node is not None else None

    @property
    def scheme(self) -> _StrFieldResponse:
        return self._card_node.get('scheme') if self._card_node is not None else None

    @property
    def mblog(self) -> MBlogMeta:
        return self._mblog

    @mblog.setter
    def mblog(self, value: MBlogMeta):
        self._mblog = value


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
    __slots__ = ['tweet_containerid', '_tweet_get_index_reponse', '_cards_node']

    def __init__(self, tweet_get_index_response: dict = None, tweet_containerid: str = None) -> None:
        if tweet_get_index_response is None and tweet_containerid is None:
            raise WeiboApiException(
                "WeiboTweetParser#__init__  tweet_get_index_response and tweet_containerid is none !")

        self.tweet_containerid = tweet_containerid

        self._tweet_get_index_reponse = weibo_tweets(containerid=tweet_containerid) \
            if tweet_get_index_response is None and tweet_containerid is not None \
            else tweet_get_index_response

        self._cards_node = [TweetMeta(card_node=card) for card in list(
            filter(lambda card: card.get('card_group') is None,
                   self._tweet_get_index_reponse.get('data').get('cards')))]

    @property
    def raw_tweet_response(self) -> _JSONResponse:
        return self._tweet_get_index_reponse

    @raw_tweet_response.setter
    def raw_tweet_response1(self, value: dict):
        self._tweet_get_index_reponse = value

    @property
    def card_list_info_node(self) -> _JSONResponse:
        return self._tweet_get_index_reponse.get('data').get('cardlistInfo')

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


# ========================= FollowAndFollower ============================

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


class RealTimeHotWordResponse(object):
    __slots__ = ['_sequence', '_desc', '_hot', '_url']

    def __init__(self, ):
        self._sequence = 0
        self._desc = ""
        self._hot = 0
        self._url = ""

    @property
    def sequence(self):
        return self._sequence

    @sequence.setter
    def sequence(self, sequence):
        self._sequence = sequence

    @property
    def desc(self):
        return self._desc

    @desc.setter
    def desc(self, desc):
        self._desc = desc

    @property
    def hot(self):
        return self._hot

    @hot.setter
    def hot(self, hot):
        self._hot = hot

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url

    def __repr__(self):
        return "<RealTimeHotWordResponse sequence=%r,desc=%r,hot=%r,url=%r,>" % (
            self._sequence, self._desc, self._hot, self._url,)
