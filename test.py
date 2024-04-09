from bs4 import BeautifulSoup
import urllib.request

Fmurl = 'https://www.fmkorea.com/hotdeal'

Html = urllib.request.urlopen(Fmurl)


# BeautifulSoup 객체 생성
soup = BeautifulSoup(Html, 'html.parser')

# 20번 반복해서 제목과 정보를 출력
for i in range(20):
    # 제목 추출
    title = soup.find_all('h3', class_='title')[i].text.strip()

    # hotdeal_info 클래스 내용 전부 추출
    product_info = soup.find_all('div', class_='hotdeal_info')[i].find_all('a', class_='strong')

    # 정보를 리스트로 반환
    store = product_info[0].text
    price = product_info[1].text
    shipping = product_info[2].text

    # 게시판 등록 시간 추출
    timestamp = soup.find_all('span', class_='regdate')[i].text.strip()

    # 결과 출력
    print(f"Title {i + 1}: {title}")
    print(f"Store {i + 1}: {store}")
    print(f"Price {i + 1}: {price}")
    print(f"Shipping {i + 1}: {shipping}")
    print(f"Timestamp {i + 1}: {timestamp}")
    print()

