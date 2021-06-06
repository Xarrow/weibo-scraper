# -*- coding:utf-8 -*-

"""
 Verion: 1.0
 Author: Helixcs
 Site: https://github.com/Xarrow/weibo-scraper
 File: weibo_component.py
 Time: 11/25/18
"""
# =========== api component ==============
from typing import Dict
from weibo_base.weibo_api import search_by_name
from weibo_base.weibo_parser import weibo_getIndex, WeiboGetIndexParser


def exist_get_uid(search_by_name_response: str = None, name: str = "") -> Dict:
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
