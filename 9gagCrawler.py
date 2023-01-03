import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time

url = "https://9gag.com/search/?query=climate%20change"

#page = requests.get(url)
#print(page.text)
driver = webdriver.Chrome(executable_path = r"C:\Users\Ellis\OneDrive\Restliche Dokumente, Rezepte, etc\_WS 22_23\VKW\Trummer\chromedriver.exe")
driver.get(url)
#print(driver.page_source)

# scrolling
lastHeight = driver.execute_script("return document.body.scrollHeight")
#print(lastHeight)

def crawlData(articles):
    #articles = soup.find_all("article")
    for article in articles:
        print("")
        print(article["id"])
        try:
            creatorID = article.find("a", class_ = "ui-post-creator__author")
            print(creatorID.contents[0])
        except:
            print("no id")
            continue
        try:
            headerText = article.find("h2")
            print(headerText.contents[0])
        except:
            print("no header")
            continue
        try:
            picture = article.find("picture")
            img = picture.find("img")
            print(img["src"])
        except:
            try:
                video = article.find("div", class_ = "post-view video-post")
                vid = video.find("video")
                print("found video")
            except:
                print("no img or video found")

pause = 1.5
for i in range(5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(pause)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    #print(soup)
    articles = soup.find_all("article")
    crawlData(articles)
    newHeight = driver.execute_script("return document.body.scrollHeight")
    if newHeight == lastHeight:
        break
    lastHeight = newHeight
    #print(lastHeight)







