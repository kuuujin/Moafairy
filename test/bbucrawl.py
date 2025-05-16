from bs4 import BeautifulSoup
import urllib.request

Bbuurl = 'https://www.ppomppu.co.kr/hotdeal/'

Html = urllib.request.urlopen(Bbuurl)


# BeautifulSoup 객체 생성
soup = BeautifulSoup(Html, 'html.parser')

# 20개만 반복해서 제목과 정보를 출력
for i in range(20):
    