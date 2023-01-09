import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import hashlib

url = "https://9gag.com/search/?query=climate%20change"

#page = requests.get(url)
#print(page.text)
driver = webdriver.Chrome(executable_path = r"C:\Users\Ellis\OneDrive\Restliche Dokumente, Rezepte, etc\_WS 22_23\VKW\Trummer\chromedriver.exe")
driver.get(url)
#print(driver.page_source)

# scrolling
last_height = driver.execute_script("return document.body.scrollHeight")
#print(last_height)

def crawlData(articles):
    #articles = soup.find_all("article")
    metadata = []
    for article in articles:
        article_meta = {}
        article_meta["id"] = article["id"]
        print("")
        print(article["id"])
        try:
            creator_id = article.find("a", class_ = "ui-post-creator__author")
            print(creator_id.contents[0])
            article_meta["creatorID"] = creator_id.contents[0]
        except:
            print("no id")
            continue
        try:
            header_text = article.find("h2")
            print(header_text.contents[0])
            article_meta["header_text"] = header_text.contents[0]
        except:
            print("no header")
            continue
        try:
            picture = article.find("picture")
            img = picture.find("img")
            print(img["src"])
            article_meta["imgSrc"] = img["src"]
            img2 = requests.get(img["src"]).content
            with open(f'images\{article["id"]}.jpg', 'wb') as handler: 
                handler.write(img2)
            with open(f'images\{article["id"]}.jpg', 'rb') as handler:    
                hash = hashlib.sha256()
                while chunk := handler.read(1024):
                    hash.update(chunk)
                article_meta["checksum"] = hash.hexdigest()
                pass
        except:
            continue
            #try:
            #    video = article.find("div", class_ = "post-view video-post")
            #    vid = video.find("video")
            #    print("found video")
            #except:
            #    print("no img or video found")

        metadata.append(article_meta)
    return metadata

all_meta = []       

pause = 1.5
for i in range(1):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(pause)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    #print(soup)
    articles = soup.find_all("article")
    all_meta += crawlData(articles)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    #print(last_height)

df = pd.DataFrame(all_meta)
df.to_csv("imgData.csv")





