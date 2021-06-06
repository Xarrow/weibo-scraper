# -*- coding:utf-8 -*-

"""
 Verion: 1.0
 Since : 3.6
 Author: zhangjian
 Site: https://github.com/Xarrow/weibo-scraper
 File: cli
 Time: 2018/12/18
 
 Add New Functional cli
"""

import argparse
import os

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter


def cli():
    """weibo-cli"""
    weibo_scraper_name = "weibo-scraper"
    weibo_scraper_version = "1.0.7 beta"
    weibo_scraper_description = weibo_scraper_name + "-" + weibo_scraper_version
    parser = argparse.ArgumentParser(description=weibo_scraper_description,
                                     prog=weibo_scraper_name,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("-u", type=str, required=False, help="username [nickname] which want to exported")
    parser.add_argument("-p", type=int, required=False, default=None, help="pages which exported [ default 1 page ]")

    parser.add_argument("-o", type=str, required=False, default=os.getcwd(),
                        help="output file path which expected [ default 'current dir' ]")
    parser.add_argument("-f", "--format", type=str, required=False, default="txt",
                        help="format which expected [ default 'txt' ]")
    parser.add_argument("-efn", "--exported_file_name", required=False, default=None, help="file name which expected")
    parser.add_argument("-s", "--simplify", action="store_true", help="simplify available info")
    parser.add_argument("-d", "--debug", action="store_true", help="open debug mode")
    parser.add_argument("--more", action="store_true", help="more")
    parser.add_argument("-v", "--version", action="store_true", help="weibo scraper version")

    args = parser.parse_args()

    if args is None:
        print(args)

    if args.version:
        print(weibo_scraper_version)
        return

    if args.more:
        more_description = weibo_scraper_description
        more_description += " you can visit https://xarrow.github.io/weibo-scraper  in detail"
        return

    if args.u is None:
        parser.print_help()
        return

    name = args.u
    pages = args.p
    is_simplify = args.simplify
    persistence_format = args.format
    export_file_path = args.o
    export_file_name = args.exported_file_name
    is_debug = args.debug

    persistence.dispatch(name=name,
                         pages=pages,
                         is_simplify=is_simplify,
                         persistence_format=persistence_format,
                         export_file_path=export_file_path,
                         export_file_name=export_file_name,
                         is_debug=is_debug)


ws = ['<html>', '<body>', '<head>', '<title>', 'google', '-u']


class CompleterProxy(WordCompleter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_input = ""

    def get_completions(
            self, document, complete_event):
        self.user_input = document.text
        if self.user_input in ws:
            ws.remove(self.user_input)
        return super().get_completions(document=document, complete_event=complete_event)

    def bottom_toolbar(self):
        if self.user_input == '-u':
            return "Help: 微博名称"
        return "Help: " + self.user_input


if __name__ == '__main__':
    # html_completer = CompleterProxy(ws)
    # text = prompt('weibo-scraper: ', completer=html_completer, bottom_toolbar=html_completer.bottom_toolbar)
    # print("weibo-scraper ", text)
    # import persistence
    cli()
