# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request
from datetime import datetime
import datetime
import re
import sys
import io
#sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'UTF-8')
#sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'UTF-8')
Count = 1
Today = datetime.datetime.now()
Fmurl = 'https://www.city.kr/index.php?mid=ln'



# 20번 반복해서 제목과 정보를 출력
for Count in range(int(50000/10)):
    Page_parameter ='&page=%d'%Count
    Fmurl_page = Fmurl + Page_parameter
    Html = urllib.request.urlopen(Fmurl_page)
    # BeautifulSoup 객체 생성
    soup = BeautifulSoup(Html, 'html.parser')
    Count = Count + 1
    for i in range(1,20):
        title,category,timestamp = [] , [] , []
        title = soup.find_all('a', class_='hx')[i].text.strip()
        #category = soup.find_all('table', class_='divsn text_over')[i].find_all('a').text.strip()
        #product_info = soup.find_all('div', class_='hotdeal_info')[i].find_all('a', class_='strong')
        timestamp = soup.find_all('td', class_='time')[i].text.strip()
        # 핫딜 게시판 에서 오늘 작성된 게시판은 %H : % M 식으로 크롤링 되어서 날짜 필터링 수정
        if re.match(r'^\d{2}:\d{2}$', timestamp):
            To_date=Today.strftime("%Y.%m.%d")
            To_date=datetime.datetime.strptime(To_date,'%Y.%m.%d')
        else:
            To_date=datetime.datetime.strptime(timestamp,'%Y/%m/%d')
            To_date=To_date.strftime("%Y.%m.%d")
            To_date=datetime.datetime.strptime(To_date,'%Y.%m.%d')
        if  ((Today-To_date).days >= 20): # 일차가 1년을 넘으면 반복문 중단
            break
        else:
            print(f"Title : {title}")
            print(f"Time: {timestamp}")
            continue
        # # 정보를 리스트로 반환
        # store = product_info[0].text
        # price = product_info[1].text
        # shipping = product_info[2].text

        # 게시판 등록 시간 추출
        #timestamp = soup.find_all('span', class_='regdate')[i].text.strip()

        # 결과 출력
      
        # print(f"Store {i + 1}: {store}")
        # print(f"Price {i + 1}: {price}")
        # print(f"Shipping {i + 1}: {shipping}")

        

