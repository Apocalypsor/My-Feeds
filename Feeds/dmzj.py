# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

import datetime

def getContent()
    items = []

    for pageNum in range(7):
        dmzjPage = requests.get(f'http://news.dmzj.com/p{pageNum + 1}.html')
        content = BeautifulSoup(dmzjPage.text, 'html.parser')
        for news in content.find_all('div', 'briefnews_con_li'):
    
            detail = news.find('div', 'li_img_de')
            dateStr = detail.find('p', 'head_con_p_o').get_text()
        
            date = datetime.date.fromisoformat(dateStr.split()[0])
            time = datetime.time.fromisoformat(dateStr.split()[1])

            pubDate = date.strftime('%a, %d %b %Y ') + time.strftime('%H:%M:%S +0800')
        
            item = {
                'title': detail.h3.a["title"],
                'link': detail.h3.a["href"],
                'pubDate': pubDate
            }
        
            dmzjArticle = requests.get(item['link'])
            article = BeautifulSoup(dmzjArticle.text, 'html.parser')
            item['description'] = article.find_all('div', 'news_content_con')[0].prettify()
        
            items.append(item)
            
        return items
        
if __name__ == '__main__':
    feed = getContent()
    print(feed)