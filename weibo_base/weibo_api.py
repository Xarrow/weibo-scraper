# -*- coding:utf-8 -*-

"""
 Author: Helixcs
 Site: https://iliangqunru.bitcron.com/
 File: weibo_api.py
 Time: 5/19/18
"""

import requests
from typing import Optional

Response = Optional[str]

_GET_INDEX = "https://m.weibo.cn/api/container/getIndex"


class WeiboApiException(Exception):
    def __init__(self, message):
        self.message = message


def search_by_name(name: str) -> Response:
    """get summary info which searched by name,
     this api is like 'https://m.weibo.cn/api/container/getIndex?queryVal=<name sample as Helixcs>&containerid=100103type%3D3%26q%3D<name sample as Helixcs>'

    >>> from weibo_base import search_by_name
    >>> _response = search_by_name('Helixcs')
    >>> ..._response
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
    >>> ..._response
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
    >>> ..._response
    :param contaierid: containerid
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


def get_weibo_containerid(weibo_getIndex_response: str = None, uid: str = ""):
    """
    get weibo_containerid
    :param uid: uid
    :return: weibo_containerid
    """
    if weibo_getIndex_response is None or str(weibo_getIndex_response) == '':
        weibo_getIndex_response = weibo_getIndex(uid)
    if weibo_getIndex_response.get('ok') != 1:
        return None
    tabs = weibo_getIndex_response.get('data').get('tabsInfo').get('tabs')
    for tab in tabs:
        if tab.get('tab_type') == 'weibo':
            return tab.get('containerid')
    return None
