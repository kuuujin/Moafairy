from bs4 import BeautifulSoup as soup
import urllib.request

Fmurl = 'https://www.fmkorea.com/hotdeal'

Html = urllib.request.urlopen(Fmurl)
SoupFm = soup(Html,'html.parser')

product_name = SoupFm.find('h3', class_='title').find('a').text.strip()
print(f"상품명: {product_name}")

# 2. 가격 추출
price = SoupFm.find('span', class_='hotdeal_info', string='가격:').find_next('a').string.strip()
print(f"가격: {price}")

# 3. 배송료 추출
shipping_fee = SoupFm.find('span', class_='hotdeal_info', string='배송:').find_next('a').string.strip()
print(f"배송료: {shipping_fee}")

# 4. 등록 시간 추출
regdate = SoupFm.find('span', class_='regdate').text.strip()
print(f"등록 시간: {regdate}")