# -*- coding:utf-8 -*-

"""
 Verion: 1.0
 Author: Helixcs
 Site: https://iliangqunru.bitcron.com/
 File: real_invoker.py
 Time: 11/23/18
"""
import logging
import sys
import os
import requests

import weibo_scraper

level = logging.DEBUG
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
datefmt = '%Y-%m-%d %H:%M'
logging.basicConfig(level=level, format=format, datefmt=datefmt)
logger = logging.getLogger(__name__)
logger.setLevel(level)
#
for i in weibo_scraper.get_formatted_weibo_tweets_by_name(name='嘻红豆',with_comments=True,pages=None):
    for j in i.cards_node:
        print(str(j.mblog.comment_parser))
