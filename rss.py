# -*- coding: utf-8 -*-

from Feeds import *
from feedgen.feed import FeedGenerator

import sys

feed = FeedGenerator()

def addEntry(entries):
    for entry in reversed(entries):
        feedEntry = feed.add_entry()
        feedEntry.title(entry['title'])
        feedEntry.link(href=entry['link'])
        feedEntry.description(entry['description'])
        feedEntry.pubDate(entry['pubDate'])
    

if __name__ == '__main__':
    if sys.argv[1] == 'dmzj':
        feed.title('动漫之家新闻')
        feed.description('动漫之家新闻RSS')
        feed.link(href='http://news.dmzj.com')
        feed.logo('https://cdn.jsdelivr.net/gh/Apocalypsor/My-Feeds@master/assets/dmzj.ico')
        addEntry(dmzj.main())

        feed.rss_file('dist/dmzj.xml')