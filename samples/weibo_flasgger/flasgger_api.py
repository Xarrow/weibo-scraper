# -*- coding:utf-8 -*-

"""
 Author: Helixcs
 Site: https://github.com/Xarrow/weibo-scraper
 File: flasgger_api.py
 Time: 5/24/18
"""
import logging
from flask import Flask, jsonify, request, make_response, render_template
from flasgger import Swagger, swag_from

from weibo_base.weibo_api import *

level = logging.DEBUG
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
datefmt = '%Y-%m-%d %H:%M'
logging.basicConfig(level=level, format=format, datefmt=datefmt)
logger = logging.getLogger(__name__)

app = Flask(__name__)

DEFAULT_CONFIG = {
    "headers": [],
    "specs": [{
        "endpoint": 'apispec_1',
        "route": '/apispec_1.json',
        "rule_filter": lambda rule: True,  # all in
        "model_filter": lambda tag: True,  # all in
    }
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/"
}

# see :https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#contactObject
TEMPLATE = {
    "swagger": "2.0",
    "info": {
        "title": "Weibo Scraper API",
        "description": "weibo scraper 接口列表",
        "host": "127.0.0.1:5002",
        "basePath": "/",
        "schemes": [
            "http", "https"
        ],
        "consumes": ['application/json'],
        "tags": ["zhangjian", ],
        "contact": {
            "name": "Helixcs",
            "email": "zhangjian12424@gmail.com",
            "url": "https://xarrow.github.io/weibo-scraper",
        },
        "version": "1.0.4"
    },
}

THIS_PAGE_CONFIG = Swagger.DEFAULT_CONFIG
THIS_PAGE_CONFIG.update({"specs_route": "/"})
swagger = Swagger(app=app, config=THIS_PAGE_CONFIG, template=TEMPLATE)


@app.route("/api/weiboBase/search_by_name/<name>", methods=["GET"])
@swag_from("ymls/search_by_name.yml")
def search_by_name_api(name):
    return jsonify(search_by_name(name=name))


@app.route("/api/weiboBase/weibo_getIndex/<uid_value>", methods=['GET'])
@swag_from('ymls/weibo_getIndex.yml')
def weibo_getIndex_api(uid_value):
    return jsonify(weibo_getIndex(uid_value=uid_value))


@app.route("/api/weiboBase/weibo_tweets/<containerid>/<page>", methods=["GET"])
@swag_from('ymls/weibo_tweets.yml')
def weibo_tweets_api(containerid, page):
    return jsonify(weibo_tweets(containerid=containerid, page=page))


#  weibo component api

@app.route('/api/weiboComponet/exist_get_uid/<name>')
@swag_from('ymls/exist_get_uid.yml')
def exist_get_uid_api(name):
    return jsonify(exist_get_uid(name=name))


@app.route('/api.weiboComponent/get_weibo_containerid/<uid>', methods=["GET"])
@swag_from("ymls/get_weibo_containerid.yml")
def get_weibo_containerid_api(uid):
    return jsonify(get_weibo_containerid(uid=uid))


app.run(port=5001, debug=True)
