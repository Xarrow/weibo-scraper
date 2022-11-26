# Weibo Scraper

[![PyPI](https://img.shields.io/pypi/v/weibo-scraper.svg)](https://pypi.org/project/weibo-scraper/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/weibo-scraper.svg)](https://docs.python.org/3/whatsnew/3.6.html)
[![Build Status](https://travis-ci.org/Xarrow/weibo-scraper.svg?branch=master)](https://travis-ci.org/Xarrow/weibo-scraper)
[![codecov](https://codecov.io/gh/Xarrow/weibo-scraper/branch/master/graph/badge.svg)](https://codecov.io/gh/Xarrow/weibo-scraper)

----

Simple weibo tweet scraper . Crawl weibo tweets without authorization.
There are many limitations in official API .
In general , we can inspect mobile site which has it's own API by Chrome.

----

# Why

1. Crawl weibo data in order to research big data .

2. Back up data for weibo's shameful blockade .

----

# Installation

### pip

```shell

$ pip install weibo-scraper

```

Or Upgrade it.

```shell

$ pip install --upgrade weibo-scraper

```

### pipenv

```shell

$ pipenv install weibo-scraper

```

Or Upgrade it.

```shell
$ pipenv update --outdated # show packages which are outdated

$ pipenv update weibo-scraper # just update weibo-scraper

```

Only Python 3.6+ is supported

----

# Usage

### CLI

```bash

$ weibo-scraper -h

usage: weibo-scraper [-h] [-u U] [-p P] [-o O] [-f FORMAT]
                     [-efn EXPORTED_FILE_NAME] [-s] [-d] [--more] [-v]

weibo-scraper-1.0.7-beta 🚀

optional arguments:
  -h, --help            show this help message and exit
  -u U                  username [nickname] which want to exported
  -p P                  pages which exported [ default 1 page ]
  -o O                  output file path which expected [ default 'current
                        dir' ]
  -f FORMAT, --format FORMAT
                        format which expected [ default 'txt' ]
  -efn EXPORTED_FILE_NAME, --exported_file_name EXPORTED_FILE_NAME
                        file name which expected
  -s, --simplify        simplify available info
  -d, --debug           open debug mode
  --more                more
  -v, --version         weibo scraper version

```

### API

1. Firstly , you can get weibo profile by `name` or `uid` .

```python
>> > from weibo_scraper import get_weibo_profile
>> > weibo_profile = get_weibo_profile(name='来去之间', )
>> > ....
```

You will get weibo profile response which is type of `weibo_base.UserMeta`, and this response include fields as below

field|chinese|type|sample|ext
---|---|---|---|---
id|用户id|str||
screen_name|微博昵称|Option[str]||
avatar_hd|高清头像|Option[str]|'https://ww2.sinaimg.cn/orj480/4242e8adjw8elz58g3kyvj20c80c8myg.jpg'|
cover_image_phone|手机版封面|Option[str]|'https://tva1.sinaimg.cn/crop.0.0.640.640.640/549d0121tw1egm1kjly3jj20hs0hsq4f.jpg'|
description| 描述|Option[str]||
follow_count|关注数|Option[int]|3568|
follower_count|被关注数|Option[int]|794803|
gender|性别|Option[str]|'m'/'f'|
raw_user_response|原始返回|Option[dict]||

2. Secondly , via `tweet_container_id` to get weibo tweets is a rare way to use but it also works well .

```python
>> > from weibo_scraper import get_weibo_tweets
>> > for tweet in get_weibo_tweets(tweet_container_id='1076033637346297', pages=1):
    >> > print(tweet)
>> > ....

```

3. Of Course , you can also get raw weibo tweets by nick name which is exist . And the param of `pages` is optional .

```python
>> > from weibo_scraper import get_weibo_tweets_by_name
>> > for tweet in get_weibo_tweets_by_name(name='嘻红豆', pages=1):
    >> > print(tweet)
>> > ....
```

3. If you want to get all tweets , you can set the param of `pages` as `None`

```python
>> > from weibo_scraper import get_weibo_tweets_by_name
>> > for tweet in get_weibo_tweets_by_name(name='嘻红豆', pages=None):
    >> > print(tweet)
>> > ....
```

4. You can also get formatted tweets via api of `weibo_scrapy.get_formatted_weibo_tweets_by_name`,

```python
>> > from weibo_scraper import get_formatted_weibo_tweets_by_name
>> > result_iterator = get_formatted_weibo_tweets_by_name(name='嘻红豆', pages=None)
>> > for user_meta in result_iterator:
    >> > if user_meta is not None:
    >> > for tweetMeta in user_meta.cards_node:
    >> > print(tweetMeta.mblog.text)
>> > ....
```

![img](asserts/weibo_tweets.png)

5. Get realtime hot words

```python
hotwords = weibo_scraper.get_realtime_hotwords()
for hw in hotwords:
    print(str(hw))
```

6. Get realtime hot words in every interval

```python
wt = Timer(name="realtime_hotword_timer", fn=weibo_scraper.get_realtime_hotwords, interval=1)
wt.set_ignore_ex(True)
wt.scheduler()
```

<!-- ---- -->

<!-- # Weibo Flasgger -->


<!-- [Weibo Flasgger](https://github.com/Xarrow/weibo-scraper/blob/search_name/samples/weibo_flasgger/FLASGGER_README.md) is a web api document for weibo scraper , and powered by flasgger . -->

<!-- ![img](https://raw.githubusercontent.com/rochacbruno/flasgger/master/docs/flasgger.png) -->

<!-- # P.S -->
<!-- 1. Inspiration from [Twitter-Scraper](https://github.com/kennethreitz/twitter-scraper) . -->

<!-- 2. For 'XIHONGDOU' . -->

<!-- 3. Welcome To Fork Me . -->

<!-- ---- -->

# LICENSE

MIT

This Project Powered By Jetbrains OpenSource License

![img](asserts/jetbrains.svg)