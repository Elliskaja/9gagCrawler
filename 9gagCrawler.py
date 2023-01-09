import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import hashlib

url = "https://9gag.com/search/?query=climate%20change"

driver = webdriver.Chrome(executable_path = r"C:\Users\Ellis\OneDrive\Restliche Dokumente, Rezepte, etc\_WS 22_23\VKW\Trummer\chromedriver.exe")
driver.get(url)

# scrolling
last_height = driver.execute_script("return document.body.scrollHeight")

num_iterations = 1

def get_creator_id(article): 
    creator_id = article.find("a", class_ = "ui-post-creator__author")
    return creator_id.contents[0]

def get_header_text(article):
    header_text = article.find("h2")
    return header_text.contents[0]

def get_img(article):
    img_src = article.find("picture").find("img")
    return img_src["src"]

def download_img(img_url, img_path):
    img = requests.get(img_url).content
    with open(img_path, 'wb') as handler: 
        handler.write(img)

def get_checksum(img_path):
    with open(img_path, 'rb') as handler:    
        hash = hashlib.sha256()
        while chunk := handler.read(1024):
            hash.update(chunk)
        return hash.hexdigest()

def get_comment_count(article):
    comment_count = article.find("a", class_ = "comment badge-evt").find("span")
    return comment_count.contents[0]

def crawlData(articles):
    metadata = []
    for article in articles:
        article_meta = {}
        article_meta["id"] = article["id"]
        print("")
        print(article["id"])

        try:
            article_meta["creatorID"] = get_creator_id(article)
        except:
            print("no id")
            continue

        try:
            article_meta["header_text"] = get_header_text(article)
        except:
            print("no header")
            continue

        try:
            article_meta["comment_count"] = get_comment_count(article)
        except:
            print("no comments")
            continue

        try:
            article_meta["imgSrc"] = get_img(article)
        except:
            continue

        img_path = f'images\{article["id"]}.jpg'
        download_img(article_meta["imgSrc"], img_path)

        article_meta["checksum"] = get_checksum(img_path)

        metadata.append(article_meta)
    return metadata

all_meta = []       

pause = 1.5
for i in range(num_iterations):
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





