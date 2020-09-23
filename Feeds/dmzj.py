# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

import os
import datetime

def downloadPic(url, headers):
    i = 0
    
    while i < 3:
        try:
            pic = requests.get(url, headers=headers, timeout=5) 
        except:
            i += 1

    if i < 3:
        folder = 'dist/assets/dmzj/' + url.split('https://images.dmzj.com/resource/news/')[1]
        os.makedirs(os.path.dirname(folder), exist_ok=True)
        with open(folder, 'wb') as f:
            f.write(pic.content)
        
        url = url.replace('https://images.dmzj.com/resource/news/', 'https://cdn.jsdelivr.net/gh/Apocalypsor/My-Feeds@feeds/assets/dmzj/')


def getContent(pageNum, download):
    items = []
    
    dmzjPage = requests.get(f'http://news.dmzj.com/p{pageNum + 1}.html')
    content = BeautifulSoup(dmzjPage.text, 'html.parser')
    for news in content.find_all('div', 'briefnews_con_li'):
    
        detail = news.find('div', 'li_img_de')
        dateStr = detail.find('p', 'head_con_p_o').get_text()
        
        date = datetime.datetime.fromisoformat(dateStr.split()[0] + ' ' + dateStr.split()[1])

        pubDate = date.strftime('%a, %d %b %Y %H:%M:%S +0800')
        timestamp = date.timestamp()
        
        item = {
            'title': detail.h3.a["title"],
            'link': detail.h3.a["href"],
            'pubDate': pubDate,
            'timestamp': timestamp
        }
        
        dmzjArticle = requests.get(item['link'])
        article = BeautifulSoup(dmzjArticle.text, 'html.parser')
        disc= article.find_all('div', 'news_content_con')[0]
            
        allPics = disc.find_all('img')
        if allPics and download:
            headers = {
                'Host': 'images.dmzj.com', 
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15', 
                'Referer': item['link']
            }
            
            for pic in allPics:
                downloadPic(pic['src'], headers)

        item['description'] = str(disc)
        
        items.append(item)

            
    return items

def main(limit=4, download=True):
    from multiprocessing import Pool
    pool = Pool(processes=4)
    
    results = []
    
    for i in range(limit):
        print(f"Started process {i}")
        results.append(pool.apply_async(getContent, (i, download)))
    
    pool.close()
    pool.join()
    print("Subprocess done.")
    
    items = []
    for r in results:
        items += r.get()
    
    return items
    
if __name__ == '__main__':
    feed = main(limit=2, download=False)
    print(feed)
