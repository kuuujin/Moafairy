from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
browser = webdriver.Chrome(options=options)

browser.get('https://www.algumon.com/')
actions = browser.find_element(By.CSS_SELECTOR , 'body')

Itemselector = "/html/body/div[6]/div[2]/ul/li/div[1]/div[2]/div/p[2]/span/a"
Priceselector = "/html/body/div[6]/div[2]/ul/li/div[1]/div[2]/p[1]"
Linkselector = "/html/body/div[6]/div[2]/ul/li/div[1]/div[2]/div/p[2]/span/a"


def crawling(count):
    items, prices, links = [], [], []
    
    for _ in range(count):
        for i in browser.find_elements(By.XPATH, Itemselector):
            items.append(i.text)
        for i in browser.find_elements(By.XPATH, Priceselector):
            prices.append(i.text)
        for i in browser.find_elements(By.XPATH, Linkselector):
            links.append(i.get_attribute("href"))
        actions.send_keys(Keys.END)
        time.sleep(2)
    
    # 길이 확인
    if not (len(items) == len(prices) == len(links)):
        print("오류: 상품, 가격, 링크의 수가 일치하지 않습니다.")
    
    return items, prices, links

def main():
    items, prices, links = crawling(4)
    print("가져온 상품 수: ", len(items))
    for i in range(len(items)):
        try:
            print("상품: ", items[i])
            print("가격: ", prices[i])
            print("주소: ", links[i])
            print('\n')
        except IndexError:
            print(f"오류: {i}번째 아이템의 정보를 가져오는데 실패했습니다.")
    
if __name__=="__main__":
    main()
