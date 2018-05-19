# -*- coding:utf-8 -*-

"""
 Author: helixcs
 Site: https://iliangqunru.bitcron.com/
 File: weibo_scraper.py
 Time: 3/16/18
"""

import threading

import math
import requests
import datetime
from concurrent.futures import ThreadPoolExecutor

from weibo_base import exist_get_uid, get_weibo_containerid, weibo_tweets

import sys

try:
    assert sys.version_info.major == 3
    assert sys.version_info.minor >= 6
except AssertionError:
    raise RuntimeError('weibo-scrapy requires Python3.6+ !')

now = datetime.datetime.now()
CURRENT_TIME = now.strftime('%Y-%m-%d %H:%M:%S')
CURRENT_YEAR = now.strftime('%Y')
CURRENT_YEAR_WITH_DATE = now.strftime('%Y-%m-%d')
pool = ThreadPoolExecutor(20)


class WeiBoScraperException(Exception):
    def __init__(self, message):
        self.message = message


class WeiboScraperParse():
    def __init__(self, name, uid, weibo_containerid, pages):
        self.name = name
        self.uid = uid
        self.weibo_containerid = weibo_containerid
        self.pages = pages

    @property
    def name(self):
        return self.name


def get_weibo_tweets_by_name(name: str, pages: int = None):
    """
    Get weibo tweets by nick name without any authorization
    >>> from weibo_scraper import  get_weibo_tweets_by_name
    >>> for tweet in get_weibo_tweets_by_name(name='Helixcs', pages=2):
    >>>     print(tweet)
    :param name: nick name which you want to search
    :param pages: pages ,default 10
    :return:
    """

    def _pre_get_total_pages(weibo_containerid):
        _weibo_tweets_response = weibo_tweets(containerid=weibo_containerid, page=1)
        if _weibo_tweets_response is None or _weibo_tweets_response.get('ok') != 1:
            raise WeiBoScraperException("prepare get total pages failed , please set pages  or try again")
        _total_tweets = _weibo_tweets_response.get('data').get('cardlistInfo').get('total')
        return math.ceil(_total_tweets / 10)

    if name == '':
        raise WeiBoScraperException("name from <get_weibo_tweets_by_name> can not be blank!")
    _egu_res = exist_get_uid(name=name)
    exist = _egu_res.get("exist")
    uid = _egu_res.get("uid")
    if exist:
        weibo_containerid = get_weibo_containerid(uid=uid)
        if pages is None:
            pages = _pre_get_total_pages(weibo_containerid=weibo_containerid)
        yield from get_weibo_tweets(container_id=weibo_containerid, pages=pages)


def get_weibo_tweets(container_id: str, pages: int):
    """
    Get weibo tweets from mobile without authorization,and this containerid exist in the api of
    'https://m.weibo.cn/api/container/getIndex?type=uid&value=1843242321'

        :param container_id :weibo container_id
        :param pages :default 25
    """
    api = "https://m.weibo.cn/api/container/getIndex"

    def gen_result(pages):
        """parse weibo content json"""
        _current_page = 1
        while pages+1 > _current_page:
            params = {"containerid": container_id, "page": _current_page}

            _response = requests.get(url=api, params=params)
            # skip bad request
            if _response.status_code != 200:
                continue

            _response_json = _response.json()
            _containerid = _response_json.get("data").get("cardlistInfo").get("containerid")
            cards = _response_json.get('data').get("cards")
            for _cards in cards:
                # skip recommended tweets
                if _cards.get("card_group"):
                    continue

                # =========== simple parse target fields below ============

                itemid = _cards.get("itemid")
                scheme = _cards.get("scheme")

                created_at = _cards.get('mblog').get("created_at")
                # 05-08
                if len(created_at) < 9 and str(created_at).__contains__("-"):
                    created_at = CURRENT_YEAR + "-" + created_at
                # 11 分钟之前
                elif not str(created_at).__contains__("-"):
                    created_at = CURRENT_YEAR_WITH_DATE
                mid = _cards.get('mblog').get("mid")
                text = _cards.get('mblog').get("text")
                source = _cards.get('mblog').get("source")
                userid = _cards.get('mblog').get("user").get("id")
                reposts_count = _cards.get('mblog').get("reposts_count")
                comments_count = _cards.get('mblog').get("comments_count")
                attitudes_count = _cards.get('mblog').get("attitudes_count")
                raw_text = ""
                if _cards.get('mblog').get("raw_text"):
                    raw_text = _cards.get('mblog').get("raw_text")

                bid = _cards.get('mblog').get("bid")

                pics_dict = {}
                if _cards.get('mblog').get("pics"):
                    pics = str(_cards.get('mblog').get("pics"))
                    pics_dict['weibo_pics'] = pics

                mblog = str(_cards.get('mblog'))
                # just yield field of mblog
                yield mblog
            _current_page += 1

        # t = threading.Thread(target=gen_result,args=(page,))
        # t.start()
        future = pool.submit(gen_result, pages)

    yield from gen_result(pages)
