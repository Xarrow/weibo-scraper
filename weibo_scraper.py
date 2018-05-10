# -*- coding:utf-8 -*-

"""
 Author: helixcs
 Site: https://iliangqunru.bitcron.com/
 File: weibo_scraper.py
 Time: 3/16/18
"""

import threading
import requests
import datetime
from concurrent.futures import ThreadPoolExecutor

now = datetime.datetime.now()
CURRENT_TIME = now.strftime('%Y-%m-%d %H:%M:%S')
CURRENT_YEAR = now.strftime('%Y')
CURRENT_YEAR_WITH_DATE = now.strftime('%Y-%m-%d')
pool = ThreadPoolExecutor(20)


def get_weibo_tweets(container_id: str, pages: int = 25):
    """ get weibo tweets from mobile without authorization,and this containerid exist in the api of
    'https://m.weibo.cn/api/container/getIndex?type=uid&value=1843242321'

        :param container_id weibo container_id
        :param pages
    """
    api = "https://m.weibo.cn/api/container/getIndex"

    def gen_result(pages):
        """parse weibo content json"""

        while pages > 0:
            params = {"containerid": container_id, "page": pages}

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
                if len(created_at) < 9 and str(created_at).__contains__("-"):
                    created_at = CURRENT_YEAR + "-" + created_at
                if not str(created_at).__contains__("-"):
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
            pages += -1

        # t = threading.Thread(target=gen_result,args=(page,))
        # t.start()
        future = pool.submit(gen_result, pages)

    yield from gen_result(pages)