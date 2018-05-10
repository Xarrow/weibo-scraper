Weibo Scraper
================

Simple weibo scraper. Crawl weibo tweets by containedId without authorization.
There are many limitations in official API .
In general , we can inspect mobile site which has it's own API by Chrome.

Usage
=====

.. code-block:: pycon
    >>> from weibo_scraper import get_weibo_tweets
    >>> for tweet in weibo_scraper.get_weibo_tweets(container_id='1076031843242321',page=10)
    P.S. Very Thanks For Twiiter-Scraper
Installation
============

.. code-block:: shell
    $ pip install weibo-scraper

Only Python 3.6+ is supported

LICENSE
=======

MIT