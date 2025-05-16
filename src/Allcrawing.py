from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
import datetime
import re
import requests
from difflib import SequenceMatcher
import redis
CONST_SCROLL_COUNT=1 # 동적 사이트 스크롤 횟수 디폴트 지정

Count = 1   # 페이지 파라미터 값 초기화 하기위한 변수
Today = datetime.datetime.now() # 게시글 등록시간 계산을 위한 변수
Url = '' # Url 변수 초기화
Page_parameter='' # Page_parameter 변수 초기화
Titles ,  Prices , Timestamps , Links , Categories , Results = [],[],[],[],[],[] # 각 리턴 변수 초기화 및 전역변수화



def fm():
    Url = 'https://www.fmkorea.com/index.php?mid=hotdeal'
    Html = urllib.request.urlopen(Url)
    soup = BeautifulSoup(Html, 'html.parser')
    for i in range(10):
        Title = soup.find_all('h3', class_='title')[i].text.strip()
        Titles.append(Title)

        Link = soup.find_all('a', class_='hotdeal_var8')[i]
        Link = 'https://www.fmkorea.com'+Link.get('href')
        Links.append(Link)

        product_info = soup.find_all('div', class_='hotdeal_info')[i].find_all('a', class_='strong')

        Price = product_info[1].text
        Prices.append(Price)

        Timestamp = soup.find_all('span', class_='regdate')[i].text.strip()
        Timestamps.append(Timestamp) 

        Category = soup.find_all('span',class_='category')[i].text.strip()
        Categories.append(Category)
        time.sleep(5)
    
    return Titles, Prices , Timestamps , Links , Categories


def bbom(CONST_SCROLL_COUNT):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("headless")
    browser = webdriver.Chrome(options=options)
    browser.get('https://www.ppomppu.co.kr/hotdeal/')
    actions = browser.find_element(By.CSS_SELECTOR , 'body')

    Itemselector = "div.wrapper > div.contents > div.container > div > div.hotDeal_goods > ul > li:not(.item.grid-item.on) > p > a:nth-child(2)"
    Priceselector = "div.wrapper > div.contents > div.container > div > div.hotDeal_goods > ul > li:not(.item.grid-item.on) > p > span:nth-child(1)"
    Linkselector = "div.wrapper > div.contents > div.container > div > div.hotDeal_goods > ul > li:not(.item.grid-item.on) > div.view > a"

    for _ in range(CONST_SCROLL_COUNT):
        
        for i in browser.find_elements(By.CSS_SELECTOR, Itemselector):
            Titles.append(i.text)
        for i in browser.find_elements(By.CSS_SELECTOR, Priceselector):
            Prices.append(i.text)
        for i in browser.find_elements(By.CSS_SELECTOR, Linkselector):
            Links.append(i.get_attribute("href"))        
            Timestamps.append('')
            Categories.append('')
        actions.send_keys(Keys.END)
    time.sleep(5)
    return Titles, Prices, Links, Timestamps, Categories


def ruli():
    Url = 'https://bbs.ruliweb.com/market/board/1020'
    Page_parameter ='?page=%d'%Count
    Url_page = Url + Page_parameter
    Html = urllib.request.urlopen(Url_page)
    # BeautifulSoup 객체 생성
    soup = BeautifulSoup(Html, 'html.parser')
    for i in range(8,18):         # 10개의 목록 출력
        Title = soup.find_all('a', class_='deco')[i].text.strip()
        Titles.append(Title)
        Category = soup.find_all('td', class_='divsn text_over')[i].find('a').text.strip()
        Categories.append(Category)
        Timestamp = soup.find_all('td', class_='time')[i].text.strip()
        Timestamps.append(Timestamp)
        Link = soup.find_all('a', class_='deco')[i]
        Link = Link.get('href')
        Links.append(Link)
        Price = ''
        Prices.append(Price)
        # # 핫딜 게시판 에서 오늘 작성된 게시판은 %H : % M 식으로 크롤링 되어서 날짜 필터링 수정

        
        
        
    return Titles, Prices, Timestamp, Links, Categories

def quasar():
    Url = 'https://quasarzone.com/bbs/qb_saleinfo'
    req = requests.get(Url)
    Html = req.text
    soup = BeautifulSoup(Html,'html.parser')


    for i in range(10):
        Title = soup.find_all('span', class_='ellipsis-with-reply-cnt')[i].text.strip()
        Titles.append(Title)
            
        Link = soup.find_all('a', class_='thumb')[i]
        Link = 'https://quasarzone.com'+Link.get('href')
        Links.append(Link)
        product_info = soup.find_all('div', class_='market-info-sub')[i].find_all('span')
        Timestamp = soup.find_all('span', class_='date')[i].text.strip()
        Timestamps.append(Timestamp)

        Category = product_info[0].text.strip()
        Categories.append(Category)
        Price = product_info[1].find('span', class_='text-orange').text.strip()
        Prices.append(Price)
        
        
        
    return Titles,Prices,Categories,Timestamps,Links
    
    

def redis_append(Titles,Prices,Categories,Timestamps,Links):
  rd = redis.StrictRedis(host='localhost', port=6379, db=0)
  rd.flushall()
  for i in range(len(Titles)):
    if Timestamps[i] == '':
        rd.hset('product:{}'.format(i+1), 'title', Titles[i])
        rd.hset('product:{}'.format(i+1), 'timestamp', Timestamps[i])
        rd.hset('product:{}'.format(i+1), 'price', Prices[i])
        rd.hset('product:{}'.format(i+1), 'category', Categories[i])
        rd.hset('product:{}'.format(i+1), 'link', Links[i])
        continue
    try:
        To_date = datetime.datetime.strptime(Timestamps[i], '%Y.%m.%d')
    except ValueError:
        # Timestamps[i]가 시간 형식인 경우 처리
        To_date = datetime.datetime.strptime(Timestamps[i], '%H:%M')
        To_date = To_date.replace(year=Today.year, month=Today.month, day=Today.day)
    if (Today - To_date).days > 2:
        break
    else:
        rd.hset('product:{}'.format(i+1), 'title', Titles[i])
        rd.hset('product:{}'.format(i+1), 'timestamp', Timestamps[i])
        rd.hset('product:{}'.format(i+1), 'price', Prices[i])
        rd.hset('product:{}'.format(i+1), 'category', Categories[i])
        rd.hset('product:{}'.format(i+1), 'link', Links[i])

        

    
      
  
  

def main():
  fm()
  ruli()
  bbom(CONST_SCROLL_COUNT)
  quasar()
  redis_append(Titles,Prices,Categories,Timestamps,Links)
  print("갱신완료")

if __name__=="__main__":
    main()


