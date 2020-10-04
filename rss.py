# -*- coding: utf-8 -*-

import os
import sys

from feedgen.feed import FeedGenerator

from Feeds import *

feed = FeedGenerator()


def addEntry(entries):
    for entry in entries:
        feedEntry = feed.add_entry()
        feedEntry.title(entry['title'])
        feedEntry.link(href=entry['link'])
        feedEntry.description(entry['description'])
        feedEntry.pubDate(entry['pubDate'])


if __name__ == '__main__':
    os.makedirs('dist', exist_ok=True)

    if sys.argv[1] == 'dmzj':
        feed.title('动漫之家新闻')
        feed.description('动漫之家新闻RSS')
        feed.link(href='http://news.dmzj.com')
        feed.logo('https://cdn.jsdelivr.net/gh/Apocalypsor/My-Feeds/assets/dmzj.ico')
        addEntry(dmzj.main())

        feed.rss_file('dist/dmzj.xml')

    if sys.argv[1] == 'acg178':
        feed.title('178动漫')
        feed.description('178动漫RSS')
        feed.link(href='https://acg.178.com/')
        feed.logo('https://cdn.jsdelivr.net/gh/Apocalypsor/My-Feeds/assets/acg178.ico')
        addEntry(acg178.main())

        feed.rss_file('dist/acg178.xml')
