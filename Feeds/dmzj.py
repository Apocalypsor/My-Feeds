# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

import os
import datetime

def getContent(limit=5):
    items = []

    for pageNum in range(limit):
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
            disc= article.find_all('div', 'news_content_con')[0]
            
            allPics = disc.find_all('img')
            if allPics:
                for pics in allPics:
                    headers = {
                        'Host': 'images.dmzj.com', 
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15', 
                        'Referer': item['link']
                    }
                    
                    url = pics['src']
                    print(f'Downloading: {url}')
                    pic = requests.get(url, headers=headers)
                    folder = 'dist/assets/dmzj/' + pics['src'].split('https://images.dmzj.com/resource/news/')[1]
                    os.makedirs(os.path.dirname(folder), exist_ok=True)
                    with open(folder, 'wb') as f:
                        f.write(pic.content)

            item['description'] = str(disc)
            
            items.append(item)
            
    return items
        
if __name__ == '__main__':
    feed = getContent(limit=1)
    print(feed)