# -*- coding: utf-8 -*-

import datetime

import requests
from bs4 import BeautifulSoup


def getContent():
    items = []
    acg = requests.get('https://acg.178.com/')
    contents = BeautifulSoup(acg.text, 'html.parser')

    for news in contents.find_all('p', 'textbox'):
        link = 'https://acg.178.com' + news.a['href']

        pubDate = ''
        timestamp = ''

        for s in news.next_siblings:
            if s != '\n':
                date = s.find('span', 'time')['data-time']
                date = datetime.datetime.fromisoformat(date)
                pubDate = date.strftime('%a, %d %b %Y %H:%M:%S +0800')
                timestamp = date.timestamp()

        item = {
            'title': news.a.string,
            'link': link,
            'pubDate': pubDate,
            'timestamp': timestamp
        }

        acgArticle = requests.get(link)
        article = BeautifulSoup(acgArticle.text, 'html.parser')

        desc = article.find('div', 'bd')
        for c in desc.find_all(True):
            if c.has_attr('style'):
                del c['style']

        description = ''
        for d in desc.find_all('p'):
            description += str(d)

        item['description'] = str(description)

        items.append(item)

    return items


def main():
    items = getContent()

    def takeTimestamp(elem):
        return elem['timestamp']

    items.sort(key=takeTimestamp)

    return items


if __name__ == '__main__':
    feed = main()
    print(feed)
