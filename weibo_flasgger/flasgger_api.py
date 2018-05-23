# -*- coding:utf-8 -*-

"""
 Author: Helixcs
 Site: https://iliangqunru.bitcron.com/
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

TEMPLATE = {
    "swagger": "2.0",
    "info": {
        "title": "Weibo-Scraper API",
        "description": "weibo-scraper 接口",
        "contact": {
            "responsibleOrganization": "None",
            "responsibleDeveloper": "Helixcs",
            "email": "zhangjian12424@gmail.com",
            "url": "https://github.io/weibo-scraper",
        },
        "version": "0.0.1"
    },
    "host": "localhost",  # overrides localhost:500
    "basePath": "/",  # base bash for blueprint registration
    "schemes": [
        "http",
        "https"
    ],
    "operationId": "getmyData"
}

THIS_PAGE_CONFIG=Swagger.DEFAULT_CONFIG
THIS_PAGE_CONFIG.update({"specs_route": "/"})
swagger = Swagger(app=app,config=THIS_PAGE_CONFIG,template=TEMPLATE)


@app.route("/api/weiboBase/search_by_name/<name>", methods=["GET", "POST"])
@swag_from("ymls/search_by_name.yml")
def weibo_base(name):
    return jsonify(search_by_name(name=name))


app.run(port=5001, debug=True)
