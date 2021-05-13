# -*- coding: utf-8 -*-

import datetime
import os

import requests
from bs4 import BeautifulSoup


def downloadPic(url, headers):
    i = 0

    print("Downloading:", url)
    while i < 10:
        try:
            res = requests.get(url, headers=headers, timeout=10)

            folder = "dist/images/dmzj/" + url.split("/news/")[1]
            os.makedirs(os.path.dirname(folder), exist_ok=True)

            with open(folder, "wb") as f:
                f.write(res.content)

            break

        except:
            i += 1


def getContent(pageNum, download):
    items = []

    dmzjPage = requests.get(f"https://news.dmzj.com/p{pageNum + 1}.html", timeout=20)
    content = BeautifulSoup(dmzjPage.text, "html.parser")
    for news in content.find_all("div", "briefnews_con_li"):

        detail = news.find("div", "li_img_de")
        dateStr = detail.find("p", "head_con_p_o").get_text()

        date = datetime.datetime.fromisoformat(
            dateStr.split()[0] + " " + dateStr.split()[1]
        )

        pubDate = date.strftime("%a, %d %b %Y %H:%M:%S +0800")
        timestamp = date.timestamp()

        item = {
            "title": detail.h3.a["title"],
            "link": detail.h3.a["href"],
            "pubDate": pubDate,
            "timestamp": timestamp,
        }

        if "http" not in item["link"]:
            item["link"] = (
                    "https://news.dmzj.com/article" + item["link"].split("/article")[1]
            )

        t = 0
        while t < 5:
            try:
                dmzjArticle = requests.get(item["link"], timeout=10)
                break
            except:
                t += 1

        article = BeautifulSoup(dmzjArticle.text, "html.parser")
        desc = article.find("div", "news_content_con")

        if desc:
            allPics = desc.find_all("img")
            if allPics and download:
                headers = {
                    "Host": "images.dmzj.com",
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
                    "Referer": item["link"],
                }
    
                for pic in allPics:
                    downloadPic(pic["src"], headers)
                    pic["src"] = (
                            "https://feedx.pages.dev/images/dmzj/"
                            + pic["src"].split("/resource/news/")[1]
                    )
    
            for c in desc.find_all(True):
                if c.has_attr("style"):
                    del c["style"]
    
            item["description"] = str(desc)
    
            items.append(item)

    return items


def main(limit=8, download=True):
    from multiprocessing import Pool

    pool = Pool(processes=limit)

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

    def takeTimestamp(elem):
        return elem["timestamp"]

    items.sort(key=takeTimestamp)

    return items


if __name__ == "__main__":
    feed = main(limit=2, download=False)
    print(feed)
