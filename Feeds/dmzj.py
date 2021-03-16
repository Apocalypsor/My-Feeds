# -*- coding: utf-8 -*-

import datetime
import os

import requests
from bs4 import BeautifulSoup


def getContent(pageNum):
    items = []

    dmzjPage = requests.get(f"https://news.dmzj.com/p{pageNum + 1}.html", timeout=5)
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

        dmzjArticle = requests.get(item["link"], timeout=5)
        article = BeautifulSoup(dmzjArticle.text, "html.parser")
        desc = article.find("div", "news_content_con")

        try:
            allPics = desc.find_all("img")
            for pic in allPics:
                pic["src"] = pic["src"].replace(
                    "images.dmzj.com", "dmzj.apocalypse.workers.dev"
                )

            for c in desc.find_all(True):
                if c.has_attr("style"):
                    del c["style"]
        except AttributeError as e:
            print("No images!")

        item["description"] = str(desc)

        items.append(item)

    return items


def main(limit=4):
    from multiprocessing import Pool

    pool = Pool(processes=4)

    results = []

    for i in range(limit):
        print(f"Started process {i}")
        results.append(pool.apply_async(getContent, (i,)))

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
    feed = main(limit=2)
    print(feed)
