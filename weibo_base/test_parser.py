# -*- coding:utf-8 -*-

"""
 Verion: 1.0
 Author: Helixcs
 Site: https://iliangqunru.bitcron.com/
 File: test_parser.py
 Time: 6/8/18
"""
import logging
import sys
import os
import requests

level = logging.DEBUG
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
datefmt = '%Y-%m-%d %H:%M'
logging.basicConfig(level=level, format=format, datefmt=datefmt)
logger = logging.getLogger(__name__)

