# -*- coding:utf-8 -*-

"""
 Author: Helixcs
 Site: https://github.com/Xarrow/weibo-scraper
 File: weibo_api.py
 Time: 5/19/18
"""
from typing import Optional
from weibo_base.weibo_util import RequestProxy, WeiboApiException

requests = RequestProxy()
Response = Optional[dict]

_GET_INDEX = "https://m.weibo.cn/api/container/getIndex"
_GET_SECOND = "https://m.weibo.cn/api/container/getSecond"
_COMMENTS_HOTFLOW = "https://m.weibo.cn/comments/hotflow"


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
    if _response.status_code == 200 and _response.json().get("ok") == 1:
        return _response.json()
    raise WeiboApiException(
        "weibo_tweets request failed, url={0},params={1},response={2}".format(_GET_INDEX, _params,
                                                                              _response if _response is None else _response.text))


def weibo_containerid(containerid: str, page: int) -> Response:
    """

    :param containerid:
    :param page:
    :return:
    """
    _params = {"containerid": containerid, "page": page}
    _response = requests.get(url=_GET_INDEX, params=_params)
    if _response.status_code == 200 and _response.json().get("ok") == 1:
        return _response.json()
    raise WeiboApiException(
        "weibo_containerid request failed, url={0},params={1},response={2}".format(_GET_INDEX, _params, _response))


def weibo_second(containerid: str, page: int) -> Response:
    """
    https://m.weibo.cn/api/container/getSecond
    :param containerid:
    :param page:
    :return:
    """
    _params = {"containerid": containerid, "page": page}
    _response = requests.get(url=_GET_SECOND, params=_params)
    if _response.status_code == 200 and _response.json().get("ok") == 1:
        return _response.json()
    raise WeiboApiException(
        "weibo_second request failed, url={0},params={1},response={2}".format(_GET_SECOND, _params, _response))


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
    if _response.status_code == 200 and _response.json().get("ok") == 1:
        return _response.json()
    raise WeiboApiException(
        "weibo_comments request failed, url={0},params={1},response={2}".format(_COMMENTS_HOTFLOW, _params, _response))


def realtime_hotword():
    _params = {"containerid": "106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtimehot"}
    _response = requests.get(url=_GET_INDEX, params=_params)

    if _response.status_code == 200 and _response.json().get("ok") == 1:
        return _response.json()
    raise WeiboApiException(
        "weibo_comments request failed, url={0},params={1},response={2}".format(_COMMENTS_HOTFLOW, _params, _response))


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
            if r_login.json().get('retcode') == 50050011:
                errurl = r_login.json().get('data').get('errurl')
                self.phone_verify(errurl)
            else:
                raise Exception("login_for_sso failed !", r_login.text)

        self.cookies = r_login.cookies.get_dict()

    def phone_verify(self, errurl):
        print(errurl)
        req = self.request.get(errurl)
        print(req.text)
        pass

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
        """
        check cookie
        """
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

# =========== unit test=============
# wv = WeiboV2("13515105572", "Weious136")
#
# wv.login_for_sso()
# from weibo_base.weibo_util import Timer, TimerManager, rt_logger
#
#
# @rt_logger
# def hw():
#     for item in realtime_hotword().get('data').get('cards')[0].get('card_group'):
#         if item.get('promotion'):
#             continue
#         print(item.get('desc'), 0 if item.get('desc_extr') is None else item.get('desc_extr'), item.get('scheme'))
#
#
# wt = Timer(name="realtime_hotword_timer", fn=hw, interval=60)
# wt.set_ignore_ex(True)
# wt.scheduler()

# print(requests.post(url="https://httpbin.org/post",json={"da":"da"}).json())
# print(requests.get("https://twitter.com").text)
